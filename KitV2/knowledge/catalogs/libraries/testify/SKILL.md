---
name: testify
description: "github.com/stretchr/testify v1.11.1 — Go assertions, requirements, mocks, and test suites. Use when stdlib testing is too verbose or mock/suite support earns the dependency; prefer stdlib for simple checks and behavior tests."
category: library
tags: [testing, assertions, mocks, suites, go]
last-verified: 2026-08-05
---

# testify — assertions et mocks

## Selection

[`github.com/stretchr/testify`](https://github.com/stretchr/testify) v1.11.1
is a maintained v1 testing helper with `assert`, `require`, `mock`, and `suite`.
It is admitted for focused assertion/mock ergonomics, tests, documentation, and
stable v1 maintenance; stdlib `testing` remains the default when it is clearer.

## Admission checklist

- [x] Current v1.11.1; maintainers state v1 remains the compatibility line.
- [x] Single responsibility: test assertions, mocks, and suite helpers.
- [x] Go 1.17+ module with tests, CI, documentation, and broad use.
- [x] `require`/`assert` semantics and mock caveats are documented.
- [x] Dependency is optional and justified by readability or mock/suite needs.

## Minimal use

```go
func TestParse(t *testing.T) {
    got, err := Parse("value")
    require.NoError(t, err)
    assert.Equal(t, "value", got)
}
```

Use `require` when continuing would make the test invalid; use `assert` for
independent checks. Table-driven stdlib tests remain the canonical shape for
simple behavior.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `testing` | Prefer for one or two assertions, table-driven cases, and tests that do not need mocks/suites. |
| Hand-written fakes | Prefer when a small consumer-owned fake is clearer and less coupled than a mock expectation tree. |
| `gomock` | Consider when generated strict mocks and call contracts justify its separate tooling. |
| `suite` | Use only when suite lifecycle adds value; ordinary subtests are often simpler. |

## Utiliser cette librairie quand

- Repeated assertions are clearer with `assert`/`require`.
- The test needs testify's mock object or suite helpers.
- The project accepts a test-only dependency and keeps behavior assertions
  independent from implementation details.

## Ne pas utiliser cette librairie quand

- Stdlib `testing` expresses the test with a few direct checks.
- A fake or pure function test is simpler than mock expectations.
- The project would use suites with parallel tests or over-specify incidental
  call order.

## Avantages

- Readable fatal/non-fatal assertion distinction.
- Mock and suite packages cover common test seams without production imports.
- Stable v1 line with broad documentation and ecosystem familiarity.

## Inconvénients

- Assertion helpers can hide the exact failure context if messages are vague.
- Mocks couple tests to calls and argument matching rather than behavior.
- `suite` and mock semantics have concurrency/pointer caveats.
- Dependency is unnecessary when stdlib checks are already concise.

## Pièges connus

- Use `require.NoError` before dereferencing a value that an error may invalidate.
- Do not mutate pointer arguments after a mock call when using call assertions;
  matching may observe changed values.
- `suite` does not support parallel tests; use ordinary subtests when race-safe
  parallelism matters.
- Prefer exact failure messages and table-driven behavior over a large mock
  expectation graph.
- Testify has no published security advisory at verification time; still scan
  its transitive dependencies in the normal gate.

## Sources vérifiées

- [Official testify repository](https://github.com/stretchr/testify) — API,
  maintenance, license, checked 2026-08-05.
- [v1.11.1 release](https://github.com/stretchr/testify/releases/tag/v1.11.1)
  — current version and mock fix, checked 2026-08-05.
- [testify on pkg.go.dev](https://pkg.go.dev/github.com/stretchr/testify) —
  package boundaries, checked 2026-08-05.
- [mock package documentation](https://pkg.go.dev/github.com/stretchr/testify/mock)
  — argument matching caveats, checked 2026-08-05.
- [Suite issue #934](https://github.com/stretchr/testify/issues/934) — parallel
  test limitation, checked 2026-08-05.
- [Security advisories](https://github.com/stretchr/testify/security/advisories)
  — package-specific advisory status, checked 2026-08-05.
