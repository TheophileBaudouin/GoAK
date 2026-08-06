# Worker pool — reading map

This map explains how to navigate this project. The **Tree facts** section
below is machine-checked by the kit's drift gate (it cannot drift silently);
the role lines, reading path, and boundary explanations are human-reviewed
content and are not machine-verifiable by design.

## Tree facts (machine-checked; do not edit)

```text
top_dirs: .github
packages: (root) -> workerpool
entry_points: 
test_files: export_test.go; pool_test.go
internal_boundary: absent
```

## Directory roles

- (root) — `workerpool` package: a single flat package — the whole pool lives
  here, there is nothing to navigate.
- `.github/` and other dot-dirs — development tooling; not part of the
  application's reading path.

## Reading path

The package is a library, not an application: there is no entry point to
follow. To understand it, read `pool.go` first (the `WorkerPool` type:
configuration, submission, shutdown), then `job.go` and `handler.go` (the job
and `Handler` contracts), then `logger.go` and `errors.go` (the supporting
pieces). A consuming program implements `Handler.Handle(ctx, job)` and calls
`Submit`; `Stop` drains accepted jobs.

## Public vs internal boundary

There is no `internal/` directory: the package is entirely public API for its
consumers — `WorkerPool`, `Job`, `Handler`, `Logger`, `ErrorHandler`, and
`MetricsHook`. There is also no entry point: this is a library package, not a
binary. Test-only helpers live in `export_test.go`, which the Go toolchain
never ships outside the test build.

## Where the evidence lives

The behavior is proven by `pool_test.go` (submission, backpressure, graceful
draining, error handling) with `export_test.go` exposing internal seams to the
tests. Run them with `go test -race ./...`.
