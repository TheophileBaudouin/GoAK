---
name: go-testing-verification
description: Design focused Go tests and verify a finished change through mechanical checks and a real user-observable scenario. Use after planning or implementation when behavior, concurrency, persistence, APIs, CLIs, or release readiness must be evidenced; do not treat a green unit test as proof of user intent.
---

# Go testing and verification

Close the loop with the smallest checks that can falsify the requested behavior.

## Procedure

1. Read the acceptance scenarios and changed flow. Identify the smallest
   success, meaningful failure, boundary, cancellation, persistence, and
   concurrency cases that matter.
2. Prefer the standard `testing` package and the repository's existing test
   style. Use subtests or table-driven cases when they improve coverage and
   failure readability; do not force them when distinct tests are clearer.
3. Add or update a focused test at the behavior seam. Avoid testing private
   implementation details when a public function, HTTP request, CLI action, or
   persisted state can prove the result.
4. Run the focused test, then the race-sensitive check when shared state or
   goroutines are involved. Record the exact command and output.
5. Run the repository mechanical gate separately. A lint, race, or security
   result is mechanical evidence, not a behavior verdict.
6. Execute the finished command or application as a user would. Record the
   starting state, action, observed output/state, and verdict using
   `references/evidence-record.md`.
7. Mark missing tools, skipped scenarios, or environment mismatches `PARTIAL`
   or `BLOCKED`; add the precise next task instead of downgrading silently.

## Evidence rules

- `PASS` requires the criterion's check and expected observation.
- `PARTIAL` means no known failure but required evidence is missing.
- `FAIL` means the observed result contradicts the criterion.
- `BLOCKED` means the check could not run for a stated reason.
- One passing run proves that run. Repeat only when the plan requires reliability
  evidence; report the number of runs.

## References

- [Test strategy](references/test-strategy.md)
- [Evidence record](references/evidence-record.md)
