package observability

import (
	"bytes"
	"encoding/json"
	"expvar"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
)

func TestMiddlewareLogsAndCounts(t *testing.T) {
	t.Parallel()
	var logs bytes.Buffer
	logger := slog.New(slog.NewJSONHandler(&logs, nil))
	metrics := &Metrics{}
	middleware, err := Middleware(logger, metrics)
	if err != nil {
		t.Fatalf("Middleware: %v", err)
	}
	handler := middleware(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestID, ok := RequestID(r.Context())
		if !ok || len(requestID) != 32 {
			t.Fatalf("RequestID = %q, %t", requestID, ok)
		}
		w.WriteHeader(http.StatusInternalServerError)
	}))
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/private?token=do-not-log", nil))
	if response.Code != http.StatusInternalServerError {
		t.Fatalf("status = %d, want %d", response.Code, http.StatusInternalServerError)
	}
	if len(response.Header().Get("X-Request-ID")) != 32 {
		t.Fatalf("X-Request-ID = %q", response.Header().Get("X-Request-ID"))
	}
	snapshot := metrics.Snapshot()
	if snapshot.RequestsTotal != 1 || snapshot.ErrorsTotal != 1 || snapshot.InFlight != 0 {
		t.Fatalf("metrics = %#v", snapshot)
	}
	if bytes.Contains(logs.Bytes(), []byte("do-not-log")) {
		t.Fatal("logger included query string")
	}
	var record map[string]any
	if err := json.Unmarshal(logs.Bytes(), &record); err != nil {
		t.Fatalf("decode JSON log: %v", err)
	}
	if record["request_id"] != response.Header().Get("X-Request-ID") {
		t.Fatalf("log request ID = %v", record["request_id"])
	}
}

func TestMetricsConcurrentRequests(t *testing.T) {
	t.Parallel()
	metrics := &Metrics{}
	middleware, err := Middleware(slog.New(slog.NewJSONHandler(&bytes.Buffer{}, nil)), metrics)
	if err != nil {
		t.Fatalf("Middleware: %v", err)
	}
	handler := middleware(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) { w.WriteHeader(http.StatusNoContent) }))

	const requests = 100
	var waitGroup sync.WaitGroup
	for range requests {
		waitGroup.Add(1)
		go func() {
			defer waitGroup.Done()
			handler.ServeHTTP(httptest.NewRecorder(), httptest.NewRequest(http.MethodGet, "/", nil))
		}()
	}
	waitGroup.Wait()
	snapshot := metrics.Snapshot()
	if snapshot.RequestsTotal != requests || snapshot.InFlight != 0 {
		t.Fatalf("metrics = %#v", snapshot)
	}
}

func TestPublishAndAdminHandler(t *testing.T) {
	metrics := &Metrics{}
	const name = "kit_recipe_observability_metrics"
	if err := Publish(name, metrics); err != nil {
		t.Fatalf("Publish: %v", err)
	}
	if expvar.Get(name) == nil {
		t.Fatal("published metrics are unavailable")
	}
	if err := Publish(name, metrics); err == nil {
		t.Fatal("Publish allowed duplicate name")
	}
	response := httptest.NewRecorder()
	AdminHandler().ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/debug/vars", nil))
	if response.Code != http.StatusOK || !bytes.Contains(response.Body.Bytes(), []byte(name)) {
		t.Fatalf("admin response status/body = %d/%s", response.Code, response.Body.String())
	}
}

func TestMiddlewareRejectsMissingDependencies(t *testing.T) {
	t.Parallel()
	if _, err := Middleware(nil, &Metrics{}); err == nil {
		t.Fatal("Middleware accepted nil logger")
	}
	if _, err := Middleware(slog.Default(), nil); err == nil {
		t.Fatal("Middleware accepted nil metrics")
	}
}
