package main

import (
	"bytes"
	"fmt"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"os"

	observability "go-agent-kit-v2/recipes/recipe-observability-slog-expvar"
)

func main() {
	metrics := &observability.Metrics{}
	if err := observability.Publish("kit_observability_probe", metrics); err != nil {
		fail(err)
	}
	middleware, err := observability.Middleware(slog.New(slog.NewJSONHandler(&bytes.Buffer{}, nil)), metrics)
	if err != nil {
		fail(err)
	}
	response := httptest.NewRecorder()
	middleware(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.WriteHeader(http.StatusNoContent)
	})).ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/", nil))
	if response.Code != http.StatusNoContent || len(response.Header().Get("X-Request-ID")) != 32 {
		fail(fmt.Errorf("instrumented response is invalid"))
	}
	admin := httptest.NewRecorder()
	observability.AdminHandler().ServeHTTP(admin, httptest.NewRequest(http.MethodGet, "/debug/vars", nil))
	if admin.Code != http.StatusOK || !bytes.Contains(admin.Body.Bytes(), []byte("kit_observability_probe")) {
		fail(fmt.Errorf("expvar metrics are unavailable"))
	}
	fmt.Println("observability: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "observability:", err)
	os.Exit(1)
}
