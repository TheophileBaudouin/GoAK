---
description: Prepare a Go application for release by running the mechanical gate, checking supply-chain and operational risks, and recording a real behavior result. Use before publishing or handing off a build.
argument-hint: "[release target]"
---

# Release review — do not confuse green code with working software

Run every applicable item. Record the exact command and result. A missing tool
or unexecuted scenario is `BLOCKED`, not silently skipped. Use `N/A` only with a
reason. This checklist is a release review, not a promise that production
traffic has been simulated.

## Mechanical gate

- [ ] `go mod tidy` produces no unexpected diff.
- [ ] `go mod verify` reports `all modules verified`.
- [ ] `test -z "$(gofmt -l .)"` passes.
- [ ] `go vet ./...` is clean.
- [ ] `golangci-lint run ./...` is clean.
- [ ] `go test -race -count=1 ./...` passes.
- [ ] `gosec ./...` has no unexplained finding.
- [ ] `govulncheck ./...` has no unresolved vulnerability.

## Build and delivery

- [ ] `go build ./...` succeeds from a clean dependency state.
- [ ] Target OS/architecture and cgo requirements are explicit and tested when
      relevant.
- [ ] Version, configuration, migration, and rollback behavior are documented.
- [ ] Secrets are absent from source, defaults, artifacts, and logs.
- [ ] Public contract and run instructions match the delivered build.

## Operational behavior

- [ ] Startup, normal operation, error path, and shutdown have an observable
      scenario or an explicit reason they are not applicable.
- [ ] Timeouts, cancellation, resource cleanup, and signal handling are tested.
- [ ] Logs are structured and do not expose credentials or private data.
- [ ] Input validation and authorization are checked at every trust boundary.

## Final evidence

- [ ] The exact finished artifact was executed in the target-like environment.
- [ ] The approved user scenario was run and its output/state recorded.
- [ ] A fresh reviewer or deterministic challenge checked high-risk behavior.
- [ ] Remaining uncertainty is listed with a follow-up task.

Verdict: `PASS` only when every applicable item has evidence. Otherwise report
`PARTIAL`, `FAIL`, or `BLOCKED` and state the precise next action.
