// Package observability demonstrates a bounded stdlib-only HTTP observation
// boundary: JSON slog records plus atomic metrics exposed by expvar.
package observability

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"errors"
	"expvar"
	"log/slog"
	"net/http"
	"sync/atomic"
	"time"
)

type requestIDContextKey struct{}

// Metrics stores bounded, process-local counters. It deliberately has no
// labels: application-specific high-cardinality dimensions belong elsewhere.
type Metrics struct {
	requestsTotal         atomic.Int64
	errorsTotal           atomic.Int64
	inFlight              atomic.Int64
	latencyNanosecondsSum atomic.Int64
}

// Snapshot is the JSON shape exposed through expvar.
type Snapshot struct {
	RequestsTotal         int64 `json:"requests_total"`
	ErrorsTotal           int64 `json:"errors_total"`
	InFlight              int64 `json:"in_flight"`
	LatencyNanosecondsSum int64 `json:"latency_nanoseconds_sum"`
}

// Snapshot returns a coherent-enough monitoring view; individual counters are
// atomic but are not a transaction across fields.
func (m *Metrics) Snapshot() Snapshot {
	if m == nil {
		return Snapshot{}
	}
	return Snapshot{
		RequestsTotal:         m.requestsTotal.Load(),
		ErrorsTotal:           m.errorsTotal.Load(),
		InFlight:              m.inFlight.Load(),
		LatencyNanosecondsSum: m.latencyNanosecondsSum.Load(),
	}
}

// String implements expvar.Var and renders the bounded metrics object.
func (m *Metrics) String() string {
	encoded, err := json.Marshal(m.Snapshot())
	if err != nil {
		return "{}"
	}
	return string(encoded)
}

// Publish registers metrics under name in the default expvar registry. It
// returns an error instead of allowing expvar.Publish to panic on a duplicate.
// Call it once during startup, then expose AdminHandler only on a private
// listener.
func Publish(name string, metrics *Metrics) error {
	if name == "" {
		return errors.New("expvar metrics name is required")
	}
	if metrics == nil {
		return errors.New("metrics are required")
	}
	if expvar.Get(name) != nil {
		return errors.New("expvar metrics name is already registered")
	}
	expvar.Publish(name, metrics)
	return nil
}

// AdminHandler returns the stdlib expvar handler. It exposes runtime values
// too, so it must be mounted only on a private administration listener.
func AdminHandler() http.Handler {
	return expvar.Handler()
}

// Middleware returns a standard net/http middleware using the injected JSON
// logger and metrics. It never places a logger in context.Context.
func Middleware(logger *slog.Logger, metrics *Metrics) (func(http.Handler) http.Handler, error) {
	if logger == nil {
		return nil, errors.New("logger is required")
	}
	if metrics == nil {
		return nil, errors.New("metrics are required")
	}
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			requestID, err := newRequestID()
			if err != nil {
				http.Error(w, "internal server error", http.StatusInternalServerError)
				return
			}
			started := time.Now()
			metrics.requestsTotal.Add(1)
			metrics.inFlight.Add(1)
			defer metrics.inFlight.Add(-1)

			w.Header().Set("X-Request-ID", requestID)
			recorder := &responseRecorder{ResponseWriter: w}
			next.ServeHTTP(recorder, r.WithContext(context.WithValue(r.Context(), requestIDContextKey{}, requestID)))

			duration := time.Since(started)
			metrics.latencyNanosecondsSum.Add(duration.Nanoseconds())
			status := recorder.statusCode()
			level := slog.LevelInfo
			if status >= http.StatusInternalServerError {
				metrics.errorsTotal.Add(1)
				level = slog.LevelError
			}
			logger.LogAttrs(r.Context(), level, "http request completed",
				slog.String("request_id", requestID),
				slog.String("method", r.Method),
				slog.Int("status", status),
				slog.Int64("duration_ns", duration.Nanoseconds()),
			)
		})
	}, nil
}

// RequestID returns the random ID injected by Middleware for correlation.
func RequestID(ctx context.Context) (string, bool) {
	requestID, ok := ctx.Value(requestIDContextKey{}).(string)
	return requestID, ok
}

type responseRecorder struct {
	http.ResponseWriter
	status int
}

func (r *responseRecorder) WriteHeader(status int) {
	if r.status == 0 {
		r.status = status
	}
	r.ResponseWriter.WriteHeader(status)
}

func (r *responseRecorder) Write(body []byte) (int, error) {
	if r.status == 0 {
		r.WriteHeader(http.StatusOK)
	}
	return r.ResponseWriter.Write(body)
}

func (r *responseRecorder) statusCode() int {
	if r.status == 0 {
		return http.StatusOK
	}
	return r.status
}

func newRequestID() (string, error) {
	bytes := make([]byte, 16)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}
