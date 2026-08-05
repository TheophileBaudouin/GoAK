---
name: recipe-worker-pool
description: "Bounded concurrent fan-out in Go with first-error-cancel via errgroup.SetLimit (~5 lines). Use when processing N items concurrently with a concurrency cap, error propagation, or context cancellation."
category: recipe
tags: [concurrency, errgroup, worker-pool, goroutine, context]
last-verified: 2026-08-05
---

# recipe-worker-pool — Bounded Worker Pool

## Problem

You have N items to process concurrently but must cap concurrency (CPU, DB
connections, rate limits) and you need errors to cancel the whole batch.

## Solution

`golang.org/x/sync/errgroup` with `SetLimit(n)`. It is the semi-official
extended-stdlib concurrency package, maintained by the Go team.

```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(limit) // ponytail: only goroutine-recycling workloads (millions of tiny tasks) need ants/pond
for _, item := range items {
    g.Go(func() error { return fn(ctx, item) })
}
return g.Wait() // returns the first non-nil error; group ctx auto-cancelled
```

Three things happen for free, with no boilerplate:

- **Bounding** — `SetLimit` caps concurrent goroutines; `Go` blocks until a slot frees.
- **First-error-cancel** — the first non-nil error cancels the group context, so
  queued/in-flight workers can abort early via `ctx.Done()`.
- **Context propagation** — `errgroup.WithContext` derives a child ctx handed to
  every worker.

Since Go 1.22 the loop variable is fresh per iteration, so the historical
`item := item` capture is no longer required.

## Why not the alternatives

| Approach | Verdict |
| --- | --- |
| Channel-semaphore (`chan struct{}` + `sync.WaitGroup` + manual error slice) | ~25 lines, easy to get cancellation wrong. Use only if you cannot take a dependency on `x/sync`. |
| `panjf2000/ants`, `alitto/pond` | Over-engineered for bounded fan-out — they recycle goroutines, which `errgroup.SetLimit` covers for every workload that is not millions of tiny tasks. Adds a dependency and a bigger API surface. |
| `gammazero/workerpool` | Redundant with errgroup **and** stalled maintenance. |

The boundary: `errgroup.SetLimit` is enough for embarrassingly parallel work where
the item count is known up front. A pool library is justified only when goroutine
*creation overhead* dominates (extreme scale of short-lived tasks) — a
micro-optimisation most services never need.

## Reference

- `golang.org/x/sync/errgroup` — canonical source, maintained by the Go team.
  `SetLimit` landed in Go 1.18.

## Verify the behavior (observable)

Run a command that calls `Run` on five numbers with `limit=2` and prints each
processed number, then prints the returned error. Observe every number exactly
once and `error=<nil>`. Run it again with one worker returning
`errors.New("stop")`; observe a non-nil `stop` result and that later work stops.
The output and cancellation are the behavior to verify, beyond unit tests.

## Run the tests

```sh
go test ./recipes/recipe-worker-pool/...
```

The test suite checks bounded execution and cancellation mechanics. It does
not replace running the command and inspecting its printed results.
