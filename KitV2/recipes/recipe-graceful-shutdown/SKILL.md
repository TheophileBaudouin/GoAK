---
name: recipe-graceful-shutdown
description: "Testable graceful shutdown of an HTTP server in Go via signal.NotifyContext, http.Server.Shutdown and an expiration timeout. Use for any HTTP service that must drain requests on SIGINT/SIGTERM."
category: recipe
tags: [shutdown, http, signal, context, stdlib]
last-verified: 2026-08-05
---

# recipe-graceful-shutdown — Graceful HTTP server shutdown

## Objective and use case

Shut down a Go HTTP server cleanly when a system signal (SIGINT, SIGTERM) is received: refuse new connections, let in-flight requests run to completion within an expiration timeout, while keeping the orchestration fully testable at the unit level.

Use this recipe for all Web services exposed in production to avoid abruptly cutting client connections during redeployments or pod terminations (e.g., Kubernetes).

## Prerequisites and architecture

- Go 1.25+ (stdlib only: `net/http`, `os/signal`, `context`)
- Testable architecture:
  - Separate OS signal capture (which belongs to `main`) from the shutdown orchestrator `shutdown.Run(...)`.
  - `Run(ctx context.Context, srv *http.Server, ln net.Listener, timeout time.Duration) error`
  - `Run` listens for cancellation of the passed context. On cancellation, it triggers `srv.Shutdown(shutdownCtx)` with a new context with an expiration timeout (`timeout`).
  - The `http.ErrServerClosed` error returned by `Serve` during a normal shutdown is absorbed and does not make `Run` fail.

## Components and choices

- `signal.NotifyContext` (Go 1.16+) — clean stdlib API creating a context canceled on receipt of an OS signal.
- `http.Server.Shutdown` — stdlib method draining HTTP connections.

## Rejected alternatives

- Capturing signals directly in the orchestrator: prevents testing the shutdown at the unit level without sending real OS signals to the test process.
- `signal.Notify(chan os.Signal)` pre-1.16: verbose, reinvents context handling.
- Third-party packages (`appleboy/graceful`, etc.): over-engineering adding unnecessary dependencies for a stdlib-native feature.

## Complete example

```go
package shutdown

import (
	"context"
	"errors"
	"net"
	"net/http"
	"time"
)

func Run(ctx context.Context, srv *http.Server, ln net.Listener, timeout time.Duration) error {
	serveErr := make(chan error, 1)
	go func() {
		err := srv.Serve(ln)
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			serveErr <- err
			return
		}
		serveErr <- nil
	}()

	select {
	case err := <-serveErr:
		return err
	case <-ctx.Done():
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	return srv.Shutdown(shutdownCtx)
}
```

```go
// Dans main.go :
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
if err := shutdown.Run(ctx, srv, ln, 5*time.Second); err != nil {
	log.Fatal(err)
}
```

## Best practices and pitfalls

- Ensure the `timeout` is shorter than the orchestrator's grace period (e.g., `terminationGracePeriodSeconds` in Kubernetes).
- Long-running HTTP handlers must listen to `r.Context().Done()` to interrupt themselves if the shutdown timeout is exceeded.

## Limits and extensions

To shut down other components simultaneously (background workers, DB connection pools), combine this logic with `golang.org/x/sync/errgroup`.

## Observable scenario and verification

```sh
go test ./recipes/recipe-graceful-shutdown/...
go run ./probes/graceful-shutdown
```

The probe instantiates an HTTP server, triggers the shutdown via context cancellation, verifies the absorption of `http.ErrServerClosed` and the clean close, then prints `graceful-shutdown: PASS`.

## Primary sources

- [net/http Server.Shutdown](https://pkg.go.dev/net/http#Server.Shutdown) — stdlib documentation.
- [os/signal NotifyContext](https://pkg.go.dev/os/signal#NotifyContext) — stdlib documentation.
