---
description: Verify a finished Go feature through its real user-observable scenario and report evidence separately from mechanical checks. Use after implementation and never skip it.
argument-hint: "[task artifact and acceptance scenario]"
---

# Verify — close the loop with evidence

Read the approved acceptance criteria and run the exact scenario as a user would:
start the command or app, provide realistic input, perform the actions, and
inspect the visible output, HTTP response, persisted state, or UI result.

## Evidence record

For every criterion record:

- starting state and environment;
- exact command or user actions;
- observed output/state and expected output/state;
- logs, screenshots, or response bodies when useful;
- verdict: `PASS`, `PARTIAL`, `FAIL`, or `BLOCKED`.

A single passing run proves only that run. For stochastic or unattended systems,
repeat the scenario when the plan requires reliability evidence and state the
number of runs. A green unit-test/lint/security gate cannot replace this check. Verify toolchain
claims against the pinned local toolchain: benchmark/fuzz flags via
`go help testflag`, `-race` via `go help build`, and gofmt via `go help fmt` or
`GOROOT/src/cmd/gofmt/doc.go` (`go help gofmt` is not a valid topic).
For high-risk work, request a fresh-context reviewer or deterministic challenge
to try to falsify the result; the implementer must not be the only evidence.

Run the mechanical gate separately and report its first failure verbatim. Never
silently downgrade a missing tool, skipped scenario, or environment mismatch.

End with:

- `Behavior: PASS`, `PARTIAL`, `FAIL`, or `BLOCKED` with evidence paths;
- `Mechanical gate: PASS` or the first failing command;
- remaining uncertainty and the precise next task.
