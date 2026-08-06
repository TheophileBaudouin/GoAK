---
name: recipe-worker-pool
description: "Bounded worker pool with first-error cancellation via errgroup.SetLimit. Strict input validation and context-cancellation awareness. Use for concurrent processing with a load limit."
category: recipe
tags: [concurrency, errgroup, worker-pool, goroutine, context]
last-verified: 2026-08-05
---

# recipe-worker-pool — bounded worker pool with errgroup

## Goal and use case

Run $N$ tasks concurrently while capping the maximum number of simultaneous goroutines (`limit`) and automatically cancelling the whole batch as soon as a worker hits an error.

Use this pattern to control concurrency over resources (CPU, DB connections, remote API calls) without relying on complex pool libraries.

## Prerequisites and architecture

- Go 1.25+
- Dependency: `golang.org/x/sync/errgroup`
- Architecture:
  - `Run[T any](ctx context.Context, items []T, limit int, fn func(ctx, item) error) error`
  - Strict input validation: reject `ctx == nil`, `limit < 1`, or `fn == nil`.
  - Check the initial context cancellation via `ctx.Err()` before starting any worker.
  - Derive `g, workerCtx := errgroup.WithContext(ctx)` and apply `g.SetLimit(limit)`.
  - In the loop, check `workerCtx.Err()` so no useless workers are scheduled once a cancellation has already happened.

## Components and choices

- `golang.org/x/sync/errgroup` — canonical extension maintained by the Go team.
- `g.SetLimit(n)` — native Go 1.18+ feature replacing the historical semaphore/channel + WaitGroup pattern.

## Rejected alternatives

- Hand-rolled channel semaphore (`chan struct{}` + `sync.WaitGroup`): ~25 lines of boilerplate prone to goroutine leaks and context-handling errors.
- Persistent goroutine pools (`panjf2000/ants`, `alitto/pond`): unnecessary over-engineering for most application workloads. Justified only for millions of micro-tasks per second where goroutine allocation becomes the bottleneck.

## Complete example

```go
package pool

import (
	"context"
	"errors"

	"golang.org/x/sync/errgroup"
)

var (
	ErrInvalidLimit = errors.New("worker-pool: limit must be positive")
	ErrNilWorker    = errors.New("worker-pool: worker function must not be nil")
	ErrNilContext   = errors.New("worker-pool: context must not be nil")
)

func Run[T any](ctx context.Context, items []T, limit int, fn func(ctx context.Context, item T) error) error {
	if ctx == nil {
		return ErrNilContext
	}
	if limit < 1 {
		return ErrInvalidLimit
	}
	if fn == nil {
		return ErrNilWorker
	}
	if err := ctx.Err(); err != nil {
		return err
	}
	g, workerCtx := errgroup.WithContext(ctx)
	g.SetLimit(limit)
	for _, item := range items {
		if workerCtx.Err() != nil {
			break
		}
		g.Go(func() error {
			if err := workerCtx.Err(); err != nil {
				return nil
			}
			return fn(workerCtx, item)
		})
	}
	return g.Wait()
}
```

## Good practices and pitfalls

- Since Go 1.22, loop variables are instantiated per iteration (`fresh per iteration`): the manual `item := item` capture is no longer needed.
- The `fn` callbacks must honor the passed `workerCtx` context and promptly interrupt their work when `workerCtx.Done()` is closed.

## Limits and extensions

If tasks are produced continuously and indefinitely (stream) rather than as a fixed slice of $N$, use a dedicated channel/worker loop.

## Observable scenario and verification

```sh
go test ./recipes/recipe-worker-pool/...
go run ./probes/worker-pool
```

The probe runs a valid batch, then a batch interrupted by an error, verifies that processing stops, and prints `worker-pool: PASS`.

## Primary sources

- [golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup) — official documentation of the `errgroup` package.
