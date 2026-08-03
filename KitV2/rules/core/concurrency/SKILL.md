---
name: concurrency
description: "Universal Go concurrency rules: make goroutine lifetimes explicit, propagate cancellation, and choose channels or mutexes for their actual role. Load before writing concurrent code."
category: rule
tags: [concurrency, goroutines, channels, mutex, context]
last-verified: 2026-08-02
---

# concurrency — make lifetime and cancellation visible

- Every goroutine needs a clear exit condition. Do not leave work blocked on a
  channel or synchronization primitive after its result is no longer needed.
- Prefer synchronous functions unless concurrency is part of the API's required
  behavior; callers can add a goroutine, while removing hidden concurrency is
  difficult.
- Use channels to coordinate independent activities and mutexes to protect
  shared state. Do not use a channel merely because it is idiomatic-sounding.
- Thread the relevant `context.Context` into cancellable work. A worker must
  select on `ctx.Done()` or call context-aware operations where it can block.
- Bound fan-out when work competes for a finite resource. `errgroup.SetLimit` is
  a recipe-level option; do not build a general pool until measurements justify
  it.
- Test cancellation and completion, not only the successful result. Go 1.25's
  [`testing/synctest`](https://go.dev/doc/go1.25) can help test time-dependent
  concurrent behavior when the project declares Go 1.25 or newer.

Source: [Go Code Review Comments — Goroutine Lifetimes](https://go.dev/wiki/CodeReviewComments#goroutine-lifetimes),
[Go Code Review Comments — Synchronous Functions](https://go.dev/wiki/CodeReviewComments#synchronous-functions),
[testing/synctest](https://pkg.go.dev/testing/synctest), and
[Go Proverbs](https://go-proverbs.github.io/).
