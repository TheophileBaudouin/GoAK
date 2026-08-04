---
name: example-rule-consistency
description: "Consistency rules for executable Go examples in GoAK catalog and recipe Markdown. Load when writing or reviewing a fenced Go example; require explicit error/resource handling and a runnable verification path."
category: rule
tags: [examples, errors, validation, documentation, testing]
last-verified: 2026-08-05
---

# example-rule-consistency — examples must not teach violations

## Rule

A fenced Go block presented as `Minimal use`, `Example`, or runnable usage must
be a correct example, not pseudocode that silently discards failures. Handle
returned errors and resource cleanup according to the loaded `errors`,
`universal`, `concurrency`, `logging`, and `testing` rules.

An intentionally abbreviated block must say `illustrative` and must not claim to
compile, run, or prove behavior. Prefer a complete `ExampleXxx` in Go test code
for behavior that needs executable proof; Markdown remains a concise pointer.

## Required checks

Before commit:

1. run the Markdown example scanner in `validate-kitv2.py`;
2. compile/run the canonical example or its linked recipe test;
3. run `gofmt`, `go vet`, `golangci-lint`, `gosec`, and the relevant tests;
4. review the block against the applicable rules, recording any justified
   boundary-level discard such as a documented best-effort cleanup.

The scanner is a tripwire, not a semantic proof. It reports suspicious blank
identifier returns and unchecked calls so the author must fix or justify them.

## Boundary

This rule does not require a full application in every catalog entry. It does
require that a short example be honest about its scope and never teach an
unchecked error, leaked resource, unbounded goroutine, or hidden globalside effect as the canonical path.

## Sources

- [Go testable examples](https://go.dev/blog/examples) — `Example` functions
  and `go test`; verified 2026-08-05.
- [golangci-lint errcheck](https://golangci-lint.run/docs/linters/configuration/)
  — unchecked error detection; verified 2026-08-05.
- [Go Code Review Comments: Errors](https://go.dev/wiki/CodeReviewComments#handle-errors)
  — handling returned errors; verified 2026-08-05.
