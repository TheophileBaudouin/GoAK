# Go worker pool template

Status: **sourced**.

This directory is a minimally adapted copy of
[`sangianpatrick/go-workerpool`](https://github.com/sangianpatrick/go-workerpool),
pinned to commit `5d5c611c47489dda3b6e97cd277131d05c814bad`. Read
[`ATTRIBUTION.md`](./ATTRIBUTION.md) before adapting it. The upstream MIT license
is retained in [`LICENSE`](LICENSE).

## What it provides

A dependency-free bounded worker pool with context-aware submission, a small
`Handler` interface, queue backpressure, optional hooks, and graceful draining
on shutdown. It intentionally does not provide a broker, persistence, retries,
job scheduling, or delivery guarantees. Those choices belong to the consuming
application.

## Adopt it

1. Copy the package into the application or change the module path in `go.mod`.
2. Implement `Handler.Handle(ctx, job)` for the application's job type.
3. Select worker and queue sizes from measured workload limits.
4. Decide explicitly whether failed jobs are retried, persisted, or discarded;
   `Stop` only drains jobs already accepted by the pool.
5. Keep the race test and add an application-level test for the handler's side
   effects.

## Verify

```sh
go test -race ./...
go vet ./...
```

The observable scenario is to create a pool, submit jobs through a bounded
queue, assert that the handler receives them, and call `Stop` to verify a
clean drain. The package tests exercise this lifecycle and race behavior.
