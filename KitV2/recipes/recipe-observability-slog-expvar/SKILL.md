---
name: recipe-observability-slog-expvar
description: "Instrument net/http with injected JSON slog logs, server-generated request IDs, atomic bounded request/error/in-flight/latency metrics, and an expvar admin handler. Use for minimum private-process observability; not for public metrics endpoints, logger-in-context, tracing, Prometheus, or OpenTelemetry."
category: recipe
tags: [observability, slog, expvar, http, metrics, logging]
last-verified: 2026-08-05
---

# recipe-observability-slog-expvar — JSON logs and private metrics

## Goal and use case

Add the minimal observability of a `net/http` service: a server-generated
random ID, an injected `slog` JSON log, and atomic request, error, in-flight
request, and latency-sum counters. The `expvar` handler exposes the values on
a private admin listener only.

## Prerequisites and architecture

Create a `*slog.Logger` with a `JSONHandler`, a `Metrics` instance, call
`Publish` once at startup, and mount `AdminHandler` on a non-public
port/interface (mTLS, local socket, or isolated admin network). `expvar` also
exposes standard runtime information: it must never be routed by the main
internet-facing server.

The middleware does not put a logger into `context.Context`; it only stores
the correlation ID there, and it never logs query strings, headers, or bodies.

## Components and choices

- `log/slog` — standard structured JSON logs, injected logger.
- `expvar` — stdlib exposure, deliberately local and without an exporter.
- `sync/atomic` — lock-free counters, no labels or high-cardinality
  dimensions.
- `crypto/rand` — correlation ID not controlled by the client.

Pattern: `pattern:observability:structured-logging`.

## Rejected alternatives

- Logger in the context: hidden dependency and needless propagation.
- Client-provided ID: allows collision/spoofing; this recipe generates its own
  and returns it in `X-Request-ID`.
- Prometheus, OpenTelemetry, and exporters: distinct infrastructure needs,
  outside this minimal layer.
- Public `/debug/vars` or metrics with dynamic user ID/path: unbounded
  exposure or cardinality.

## Complete example

```go
metrics := &observability.Metrics{}
if err := observability.Publish("orders_metrics", metrics); err != nil {
	return err
}
middleware, err := observability.Middleware(slog.New(slog.NewJSONHandler(os.Stdout, nil)), metrics)
if err != nil {
	return err
}
publicServer := &http.Server{Addr: ":8080", Handler: middleware(app)}
privateServer := &http.Server{Addr: "127.0.0.1:9090", Handler: observability.AdminHandler()}
```

Do not replace `127.0.0.1:9090` with a public address without an explicit
security decision and access control.

## Best practices and pitfalls

- Log only bounded fields: ID, method, status, and duration; no secrets,
  query strings, bodies, tokens, or user IDs.
- An atomic `Snapshot` is not a transaction: the observation may cover
  slightly different instants.
- Call `Publish` only once; a second registration is an error.
- Test concurrent requests under `-race`, like the recipe's test.

## Limits and extensions

No distributed traces, histograms, export, dashboards, alerts, or
per-route/per-user metrics. Add this level of observability via a dedicated
recipe, with a cardinality, cost, and exposure policy.

## Observable scenario and verification

```sh
go test -race ./recipes/recipe-observability-slog-expvar/...
go run ./probes/observability
```

The probe makes a request, verifies the ID and the `expvar` metric, then
prints `observability: PASS`.

## Primary sources

- [log/slog](https://pkg.go.dev/log/slog) — structured logs and `JSONHandler`.
- [expvar](https://pkg.go.dev/expvar) — global registry and `/debug/vars`.
- [sync/atomic](https://pkg.go.dev/sync/atomic) — concurrent counters.
