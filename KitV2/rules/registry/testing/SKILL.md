---
name: testing
description: "Idiomatic Go testing rules — table-driven tests, TDD red/green, naming, and when stdlib testing suffices over testify. Distilled from quii/learn-go-with-tests (an educational source, NOT a reference project)."
category: rule
tags: [testing, tdd, table-driven, stdlib]
last-verified: 2026-08-02
---

# testing — idiomatic Go testing

## Source

Distilled from `quii/learn-go-with-tests` (~24k★) — a free book/tutorial on TDD
in Go. It is an **educational source**, explicitly NOT a reference project (it
has no single production responsibility). These are the durable rules, not a copy
of its examples.

## Rules

### 1. Table-driven is the default shape

One test function, a slice of cases, a `t.Run(tc.name, ...)` loop. Keeps
inputs/expected/want-error side by side and makes adding a case trivial.

```go
func TestParse(t *testing.T) {
    tests := []struct {
        name    string
        in      []string
        want    Config
        wantErr bool
    }{
        {"defaults", nil, Config{Port: 8080}, false},
        {"bad flag", []string{"-bogus"}, Config{}, true},
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            got, err := ParseTo(tc.in, io.Discard)
            if (err != nil) != tc.wantErr { t.Fatalf("err=%v", err) }
            // assert got == tc.want
        })
    }
}
```

### 2. TDD red → green → refactor

Write the smallest failing test first. Make it pass with the least code. Then
refactor. The test pins behaviour before the implementation exists — this is the
discipline that prevents "tests that just encode the current bug".

### 3. Fail loudly, fail locally

`t.Fatal`/`require` when subsequent lines depend on the assertion; `t.Error`/
`assert` to collect independent failures. Always include a message that names
what failed (`got %v want %v`).

### 4. Prefer stdlib until a helper earns its keep

`if err != nil { t.Errorf(...) }` for one or two checks. Reach for testify only
when assertions multiply and readability suffers (see `testify`).

### 5. Naming + isolation

`TestSubject_scenario` (`TestRun_firstErrorCancels`). Subtests via `t.Run`.
Never share mutable state across cases — a leaked global makes tests
order-dependent and flaky.

### 6. Race-clean by default

`go test -race` is part of the gate. If a test spawns goroutines, it must close
its channels / wait its WaitGroup / honour its context.

## Anti-patterns (reject on sight)

- A test that depends on execution order.
- `time.Sleep` to "wait" for a goroutine — use a channel/WaitGroup/`Eventually`.
- Ignoring the `_ = resp.Body.Close()` / `_ = rows.Close()` returns (errcheck
  fails the gate — see `rules/core/validation/golangci-lint`).

## 7. Coverage floor — 70%, enforced in CI

The CI workflows (metaproject gate and the shipped `templates/_kit-ci-workflow.yml`)
run `go test -race -coverprofile=coverage.out ./...` and fail when the aggregate
drops below a **70%** floor. The local gate (`AGENTS.md`) checks `-race` without
a coverage floor. A 70% floor catches a wholly-untested package without
pressuring anyone to write hollow tests that touch a line without asserting
anything meaningful. It is a floor, not a target — 100% is not the goal.

CI fails when the aggregate total drops below 70%:

```sh
go test -race -coverprofile=coverage.out ./...
go tool cover -func=coverage.out | tail -1        # -> "total: ... 90.8%"
# CI step compares the percentage against 70 and fails below it.
```

Per-package coverage prints inline (`coverage: 81.5% of statements`). A package
below 70% is a smell to investigate, not an automatic failure — the aggregate
floor is what blocks.

## 8. Test fixtures live in testdata/

Go's tooling reserves the `testdata/` directory: `go build` ignores it, so it is
the canonical home for fixture files (golden output, sample JSON, SQL seeds).

```text
recipe-sqlite-sqlc/
├── store.go
├── store_test.go
└── testdata/
    └── seed.sql          # loaded in the test with os.ReadFile("testdata/seed.sql")
```

`testdata/` paths are relative to the test file's package directory, and
`go test` always runs with that as the working directory — no path stitching.

## 9. Unit vs. integration — the `//go:build integration` tag

Unit tests (stdlib, in-memory, no external process) are the default and run on
every `go test ./...`. Integration tests (a real database, a network server, a
slow dependency) carry a build tag so they are **opt-in**:

```go
//go:build integration

package restchi

func TestStore_RealPostgres(t *testing.T) { /* ... */ }
```

- Run unit tests only: `go test ./...` (default — integration files are skipped).
- Run integration too: `go test -tags=integration ./...`.
- Name the file `*_integration_test.go` as well, so integration tests are
  greppable without parsing build tags.

Why a build tag over `_integration_test.go` naming alone: the tag guarantees the
file is excluded from the default build, so a missing external dependency never
breaks a routine `go test`. The suffix is readability; the tag is the gate.

## Optional, not in the gate: mutation testing (gremlins)

Coverage measures **which lines ran**, not whether the test **asserted anything
correct about them** — a test that calls a function and checks nothing can still
produce 100% coverage. Mutation testing (`go-gremlins`) flips operators and
constants in the source and reports which mutants survive (i.e. tests that
should have failed didn't). It is a stronger signal than coverage.

This is a **human opt-in**, not part of the blocking gate — it is slower than
the unit suite and choosing to block on it is an infrastructure decision. TODO:
evaluate gremlins in CI as a non-blocking report before promoting it. Do not
enable it silently.

## Boundary — what this rule does not cover

- Benchmark methodology and micro-benchmark hygiene (see the `go-profiling`
  source pointer for measured guidance).
- Fuzzing setup and corpus management (see the `go-fuzzing` stdlib pointer).
- Coverage tooling policy beyond the CI aggregate floor described in §7.
