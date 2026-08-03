---
description: Review a Go HTTP API against routing, trust-boundary, error, concurrency, security, and behavior evidence before declaring the endpoint complete.
argument-hint: "[path or endpoint]"
---

# API review — evidence before approval

Review the requested API change${1:+ at $1}. Mark each item `PASS`, `FAIL`, or
`NOT APPLICABLE` with a file/line or command-output reference. Do not approve
based on code reading alone when a behavior scenario can be run.

## Contract and routing

- [ ] Method and path are explicit; route parameters reject malformed input.
- [ ] Request/response schema and status codes match the approved specification.
- [ ] Errors use a stable public shape without internal details.
- [ ] Public contract changes are documented.

## Trust boundaries and failures

- [ ] Request bodies, query values, flags, and config are bounded and validated.
- [ ] Context is propagated to I/O and cancellable work.
- [ ] Errors are handled once at the boundary and wrapped with `%w` below it.
- [ ] Authentication and authorization are enforced where required.

## State and concurrency

- [ ] Shared state is protected or avoided; goroutine lifetimes have exit paths.
- [ ] Database rows, files, and response bodies are closed with errors handled.
- [ ] Cancellation, timeout, not-found, conflict, and dependency failures have
      deliberate behavior.

## Checks and behavior

- [ ] Focused tests cover success and meaningful failure cases.
- [ ] Mechanical gate passes: formatting, vet, lint, race tests, gosec, and
      govulncheck.
- [ ] A real request was sent to the finished service and its status, headers,
      body, and persisted effect were recorded.
- [ ] If the scenario was not run, verdict is `PARTIAL` or `BLOCKED`, not `PASS`.

## Verdict

Report failed items first, then evidence paths, then one of:

- `PASS`: all applicable checks and the observable scenario passed.
- `PARTIAL`: some evidence is missing, but no known failure is present.
- `BLOCKED`: a required check or scenario could not run.
