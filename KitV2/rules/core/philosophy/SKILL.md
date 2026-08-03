---
name: philosophy
description: "Universal decision rules for Go projects: smallest justified structure, standard library first, and mechanical checks separate from observable behavior. Load before choosing architecture or dependencies."
category: rule
tags: [philosophy, minimalism, architecture, behavior]
last-verified: 2026-08-02
---

# philosophy — choose the smallest justified solution

## Decision order

1. Confirm the requested behavior and unresolved questions.
2. Reuse an existing recipe or package when it fits.
3. Prefer the standard library or platform capability.
4. Add a dependency only when it removes real complexity; record the rejected
   simpler option.
5. Use the smallest project layout that the selected behavior needs.

Go's official module-layout guidance demonstrates several valid shapes—from one
root package to `internal/` and optional `cmd/`—rather than prescribing one
universal tree. See [Organizing a Go module](https://go.dev/doc/modules/layout).

## Evidence has two layers

- **Mechanical:** formatting, compilation, tests, race checks, lint, and security
  scanners establish properties of the code and dependency graph.
- **Behavioral:** a real command, HTTP request, UI action, or other user-visible
  scenario demonstrates that the application does what was requested.

Never report the mechanical gate as proof of the behavioral result. Every recipe
must provide an observable scenario with concrete actions and expected output.

## Sources

- [Effective Go](https://go.dev/doc/effective_go) — idiomatic Go baseline.
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) — review guidance and runnable examples.
- [Go Proverbs](https://go-proverbs.github.io/) — clarity, errors, interfaces,
  and concurrency principles.
- [Organizing a Go module](https://go.dev/doc/modules/layout) — examples of
  minimal layouts without a universal prescription.
