// Package openapivalidation demonstrates bounded OpenAPI request and response
// validation for a standard net/http handler.
package openapivalidation

import (
	"bytes"
	"context"
	_ "embed"
	"encoding/json"
	"errors"
	"fmt"
	"log/slog"
	"net/http"
	"reflect"

	"github.com/getkin/kin-openapi/openapi3"
	"github.com/getkin/kin-openapi/openapi3filter"
	"github.com/getkin/kin-openapi/routers"
	legacyrouter "github.com/getkin/kin-openapi/routers/legacy"
)

var errResponseTooLarge = errors.New("OpenAPI response exceeds configured limit")

// ExampleSpec is the embedded, startup-validatable contract used by this recipe.
//
//go:embed openapi.yaml
var ExampleSpec []byte

// Config supplies a pre-embedded or application-owned OpenAPI document and its
// resource/authentication policy.
type Config struct {
	Spec               []byte
	AuthenticationFunc openapi3filter.AuthenticationFunc
	MaxBodyBytes       int64
	Logger             *slog.Logger
}

// Validator holds a startup-validated document and its route resolver.
type Validator struct {
	router       routers.Router
	authenticate openapi3filter.AuthenticationFunc
	maxBodyBytes int64
	logger       *slog.Logger
}

// New loads and validates the OpenAPI document at startup. A real non-nil
// AuthenticationFunc is mandatory; the explicit Noop helper is rejected.
func New(ctx context.Context, config Config) (*Validator, error) {
	if len(config.Spec) == 0 {
		return nil, errors.New("OpenAPI document is required")
	}
	if config.MaxBodyBytes <= 0 {
		return nil, errors.New("OpenAPI body limit must be positive")
	}
	if config.AuthenticationFunc == nil {
		return nil, errors.New("OpenAPI authentication function is required")
	}
	if reflect.ValueOf(config.AuthenticationFunc).Pointer() == reflect.ValueOf(openapi3filter.NoopAuthenticationFunc).Pointer() {
		return nil, errors.New("OpenAPI noop authentication function is not allowed")
	}
	if config.Logger == nil {
		config.Logger = slog.Default()
	}

	loader := openapi3.NewLoader()
	document, err := loader.LoadFromData(config.Spec)
	if err != nil {
		return nil, fmt.Errorf("load OpenAPI document: %w", err)
	}
	if err := document.Validate(ctx); err != nil {
		return nil, fmt.Errorf("validate OpenAPI document: %w", err)
	}
	if err := validateFallbackResponses(document); err != nil {
		return nil, err
	}
	router, err := legacyrouter.NewRouter(document)
	if err != nil {
		return nil, fmt.Errorf("build OpenAPI router: %w", err)
	}
	return &Validator{
		router:       router,
		authenticate: config.AuthenticationFunc,
		maxBodyBytes: config.MaxBodyBytes,
		logger:       config.Logger,
	}, nil
}

// Middleware validates a bounded incoming request, buffers a bounded outgoing
// response, then validates status, headers, and body before writing it.
// Streaming, hijacking, flushing, and oversized responses are intentionally
// unsupported by this all-or-nothing boundary.
func (v *Validator) Middleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		route, pathParams, err := v.router.FindRoute(r)
		if err != nil {
			writeContractError(w, http.StatusNotFound, "not found")
			return
		}

		r.Body = http.MaxBytesReader(w, r.Body, v.maxBodyBytes)
		if route.Operation.RequestBody == nil && r.ContentLength != 0 {
			writeContractError(w, http.StatusBadRequest, "invalid request")
			return
		}
		requestInput := &openapi3filter.RequestValidationInput{
			Request:    r,
			PathParams: pathParams,
			Route:      route,
			Options:    &openapi3filter.Options{AuthenticationFunc: v.authenticate},
		}
		if err := openapi3filter.ValidateRequest(r.Context(), requestInput); err != nil {
			var maxBytesError *http.MaxBytesError
			if errors.As(err, &maxBytesError) {
				writeContractError(w, http.StatusRequestEntityTooLarge, "request body too large")
				return
			}
			writeContractError(w, http.StatusBadRequest, "invalid request")
			return
		}

		buffered := newBufferedResponseWriter(v.maxBodyBytes)
		next.ServeHTTP(buffered, r)
		if buffered.exceeded {
			v.logInvalidResponse(r, buffered.statusCode())
			writeContractError(w, http.StatusInternalServerError, "internal server error")
			return
		}

		responseInput := &openapi3filter.ResponseValidationInput{
			RequestValidationInput: requestInput,
			Status:                 buffered.statusCode(),
			Header:                 buffered.Header().Clone(),
			Options:                &openapi3filter.Options{IncludeResponseStatus: true},
		}
		responseInput.SetBodyBytes(buffered.body.Bytes())
		if err := openapi3filter.ValidateResponse(r.Context(), responseInput); err != nil {
			v.logInvalidResponse(r, buffered.statusCode())
			writeContractError(w, http.StatusInternalServerError, "internal server error")
			return
		}
		copyBufferedResponse(w, buffered)
	})
}

func validateFallbackResponses(document *openapi3.T) error {
	for path, pathItem := range document.Paths.Map() {
		for method, operation := range pathItem.Operations() {
			for _, status := range []string{
				fmt.Sprint(http.StatusBadRequest),
				fmt.Sprint(http.StatusRequestEntityTooLarge),
				fmt.Sprint(http.StatusInternalServerError),
			} {
				if operation.Responses.Value(status) == nil {
					return fmt.Errorf("OpenAPI operation %s %s must declare fallback response %s", method, path, status)
				}
			}
		}
	}
	return nil
}

func (v *Validator) logInvalidResponse(r *http.Request, status int) {
	// Deliberately omit validation detail and body: both can contain sensitive data.
	v.logger.Error("OpenAPI response validation failed", slog.String("method", r.Method), slog.Int("status", status))
}

type bufferedResponseWriter struct {
	header   http.Header
	status   int
	body     bytes.Buffer
	maxBytes int64
	exceeded bool
}

func newBufferedResponseWriter(maxBytes int64) *bufferedResponseWriter {
	return &bufferedResponseWriter{header: make(http.Header), maxBytes: maxBytes}
}

func (w *bufferedResponseWriter) Header() http.Header {
	return w.header
}

func (w *bufferedResponseWriter) WriteHeader(status int) {
	if w.status == 0 {
		w.status = status
	}
}

func (w *bufferedResponseWriter) Write(body []byte) (int, error) {
	if w.status == 0 {
		w.status = http.StatusOK
	}
	if int64(w.body.Len()+len(body)) > w.maxBytes {
		w.exceeded = true
		return 0, errResponseTooLarge
	}
	return w.body.Write(body)
}

func (w *bufferedResponseWriter) statusCode() int {
	if w.status == 0 {
		return http.StatusOK
	}
	return w.status
}

func copyBufferedResponse(destination http.ResponseWriter, source *bufferedResponseWriter) {
	for key, values := range source.Header() {
		destination.Header()[key] = append([]string(nil), values...)
	}
	destination.WriteHeader(source.statusCode())
	if _, err := destination.Write(source.body.Bytes()); err != nil {
		return
	}
}

func writeContractError(w http.ResponseWriter, status int, message string) {
	for key := range w.Header() {
		w.Header().Del(key)
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	if err := json.NewEncoder(w).Encode(map[string]string{"error": message}); err != nil {
		return
	}
}
