package openapivalidation

import (
	"bytes"
	"context"
	"errors"
	"log/slog"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/getkin/kin-openapi/openapi3filter"
)

func TestMiddlewareValidatesRequestAndResponse(t *testing.T) {
	t.Parallel()
	validator := newTestValidator(t, 1024)
	called := false
	handler := validator.Middleware(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		called = true
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_, _ = w.Write([]byte(`{"id":1}`))
	}))
	request := newWidgetRequest(`{"name":"coffee"}`)
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, request)
	if !called || response.Code != http.StatusCreated || response.Body.String() != `{"id":1}` {
		t.Fatalf("called/status/body = %t/%d/%q", called, response.Code, response.Body.String())
	}
}

func TestMiddlewareRejectsInvalidRequest(t *testing.T) {
	t.Parallel()
	validator := newTestValidator(t, 1024)
	handler := validator.Middleware(http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		t.Fatal("next handler ran for invalid request")
	}))
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, newWidgetRequest(`{}`))
	if response.Code != http.StatusBadRequest || response.Body.String() != "{\"error\":\"invalid request\"}\n" {
		t.Fatalf("status/body = %d/%q", response.Code, response.Body.String())
	}
}

func TestMiddlewareHidesInvalidResponse(t *testing.T) {
	t.Parallel()
	var logs bytes.Buffer
	validator, err := New(context.Background(), Config{
		Spec:               ExampleSpec,
		AuthenticationFunc: testAuthentication,
		MaxBodyBytes:       1024,
		Logger:             slog.New(slog.NewJSONHandler(&logs, nil)),
	})
	if err != nil {
		t.Fatalf("New: %v", err)
	}
	handler := validator.Middleware(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		_, _ = w.Write([]byte(`{"secret":"must-not-leak"}`))
	}))
	response := httptest.NewRecorder()
	handler.ServeHTTP(response, newWidgetRequest(`{"name":"coffee"}`))
	if response.Code != http.StatusInternalServerError || response.Body.String() != "{\"error\":\"internal server error\"}\n" {
		t.Fatalf("status/body = %d/%q", response.Code, response.Body.String())
	}
	if bytes.Contains(response.Body.Bytes(), []byte("secret")) || bytes.Contains(logs.Bytes(), []byte("secret")) {
		t.Fatal("invalid response content leaked")
	}
}

func TestMiddlewareRejectsOversizedRequest(t *testing.T) {
	t.Parallel()
	validator := newTestValidator(t, 8)
	response := httptest.NewRecorder()
	validator.Middleware(http.HandlerFunc(func(http.ResponseWriter, *http.Request) {
		t.Fatal("next handler ran for oversized request")
	})).ServeHTTP(response, newWidgetRequest(`{"name":"coffee"}`))
	if response.Code != http.StatusRequestEntityTooLarge {
		t.Fatalf("status = %d, want %d", response.Code, http.StatusRequestEntityTooLarge)
	}
}

func TestNewRejectsMissingOrNoopAuthentication(t *testing.T) {
	t.Parallel()
	if _, err := New(context.Background(), Config{Spec: ExampleSpec, MaxBodyBytes: 1}); err == nil {
		t.Fatal("New accepted nil authentication function")
	}
	if _, err := New(context.Background(), Config{Spec: ExampleSpec, MaxBodyBytes: 1, AuthenticationFunc: openapi3filter.NoopAuthenticationFunc}); err == nil {
		t.Fatal("New accepted noop authentication function")
	}
	if _, err := New(context.Background(), Config{Spec: []byte("not: [an OpenAPI document"), MaxBodyBytes: 1, AuthenticationFunc: testAuthentication}); err == nil {
		t.Fatal("New accepted invalid OpenAPI document")
	}
	missingFallback := bytes.Replace(ExampleSpec, []byte("        '500':\n          $ref: '#/components/responses/Error'\n"), nil, 1)
	if _, err := New(context.Background(), Config{Spec: missingFallback, MaxBodyBytes: 1, AuthenticationFunc: testAuthentication}); err == nil {
		t.Fatal("New accepted a contract without fallback responses")
	}
}

func newTestValidator(t *testing.T, maxBodyBytes int64) *Validator {
	t.Helper()
	validator, err := New(context.Background(), Config{
		Spec: ExampleSpec, AuthenticationFunc: testAuthentication, MaxBodyBytes: maxBodyBytes,
	})
	if err != nil {
		t.Fatalf("New: %v", err)
	}
	return validator
}

func newWidgetRequest(body string) *http.Request {
	request := httptest.NewRequest(http.MethodPost, "/widgets", bytes.NewBufferString(body))
	request.Header.Set("Content-Type", "application/json")
	request.Header.Set("Authorization", "Bearer test")
	return request
}

func testAuthentication(_ context.Context, input *openapi3filter.AuthenticationInput) error {
	if input.RequestValidationInput.Request.Header.Get("Authorization") != "Bearer test" {
		return errors.New("missing bearer token")
	}
	return nil
}
