---
name: recipe-graceful-shutdown
description: "Minimal testable graceful shutdown of a Go HTTP server using signal.NotifyContext + http.Server.Shutdown + a drain timeout (stdlib only). Use when building an HTTP service that must drain in-flight requests on SIGINT/SIGTERM, and to make the shutdown logic unit-testable."
category: recipe
tags: [shutdown, http, signal, context, stdlib]
last-verified: 2026-08-05
---

# recipe-graceful-shutdown — Graceful HTTP server shutdown

## Problem

Stop an HTTP server cleanly on a termination signal: stop accepting new
connections, let in-flight requests finish, enforce a hard deadline — and keep
the logic **unit-testable**.

## Solution

Standard library only. `signal.NotifyContext` (Go 1.16+) derives a context that
is cancelled on SIGINT/SIGTERM; `http.Server.Shutdown(ctx)` drains in-flight
requests until they finish or the context expires. The testability trick:
**keep the signal wiring separate from the shutdown orchestration** — `Run`
takes a `context.Context`, so tests cancel it manually instead of sending OS
signals.

```go
// shutdown.Run — the orchestrator (this package)
func Run(ctx context.Context, srv *http.Server, ln net.Listener, timeout time.Duration) error

// main — the wiring (your application)
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
if err := shutdown.Run(ctx, srv, ln, 5*time.Second); err != nil {
    log.Fatal(err)
}
```

`http.Server.Serve` returns `http.ErrServerClosed` during a graceful shutdown;
`Run` absorbs that sentinel and returns `nil` on a clean drain, the serve error
if the server failed to start, or the Shutdown error if the drain exceeded the
timeout.

See [`shutdown.go`](shutdown.go) for the runnable, tested example.

## Why this shape (and not the common inline version)

The Go standard-library example (`net/http/example_test.go`,
`ExampleServer_Shutdown`) puts `signal.Notify` and `srv.Shutdown` in the same
goroutine — fine for a demo, but the signal call is impossible to unit-test (you
cannot send a real SIGINT deterministically inside a test). By taking a
`context.Context`, `Run` is pure orchestration: tests cancel the context and
assert the drain behaves. `signal.NotifyContext` belongs at the edge, in `main`,
exactly where the OS signal is a real input.

## The canonical pieces

| Piece | API | Role |
|---|---|---|
| Signal → context | `signal.NotifyContext(parent, os.Interrupt, syscall.SIGTERM)` | ctx is cancelled on signal |
| Drain | `http.Server.Shutdown(ctx)` | stops new conns; waits for in-flight (or ctx expiry) |
| Deadline | `context.WithTimeout(shutdownCtx, 5*time.Second)` | hard cap on drain time |
| Expected sentinel | `http.ErrServerClosed` from `Serve`/`ListenAndServe` | normal graceful-exit signal |

## Why not the alternatives

| Alternative | Verdict |
|---|---|
| `signal.Notify(chan os.Signal)` + `select` | The pre-1.16 pattern. Verbose; reinvents `NotifyContext`. Use `NotifyContext`. |
| `errgroup.WithContext` for multi-component shutdown | Good ADD-ON when you must also stop workers/DB together — but it is orchestration sugar on top of this pattern, not a replacement. |
| `appleboy/graceful`, `enrichman/httpgrace`, etc. | Wrap `http.Server` with signal handling the stdlib already provides. Reinvents `NotifyContext` + `Shutdown`; adds a dependency for nothing. |
| `http.Server.RegisterOnShutdown` callbacks | Useful for cleanup hooks (close a logger), orthogonal to the drain itself. |

## Notes

- Match `timeout` to your orchestrator's grace period (e.g. Kubernetes
  `terminationGracePeriodSeconds` — set it a bit below that so Shutdown returns
  before the kubelet hard-kills the pod).
- `Shutdown` does NOT cancel long-running handlers for you — your handlers must
  honour `r.Context()` and abort when it is cancelled. Wire that into handlers
  that do slow work.

## Verify the behavior (observable)

Run the finished HTTP service, start a request that intentionally sleeps, then
send `SIGTERM`. Observe that the request completes within the drain timeout and
the process exits cleanly. Send `SIGTERM` with a handler that exceeds the
 timeout and observe a timeout error and process exit. Use the service's actual
logs/output; tests alone do not prove signal wiring.

## Run the tests

```sh
go test ./recipes/recipe-graceful-shutdown/...
```
