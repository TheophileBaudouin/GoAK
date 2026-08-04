---
name: go-code-review
category: workflow
tags: [review, code-review, diff, evidence, verification]
last-verified: 2026-08-04
description: Review a Go diff for correctness, regressions, maintainability, and evidence quality. Use before merging or handing off non-trivial Go changes, especially when a fresh-context reviewer should challenge the implementer's assumptions; do not use it as an automatic approval.
---

# Go code review

Review the actual diff and repository behavior. Do not review a worker's summary
instead of the files.

## Procedure

1. Read project rules, the approved plan or request, and the complete diff.
   Identify the intended behavior, public contracts, trust boundaries, and
   affected callers/tests.
2. Run the cheapest relevant mechanical checks first: formatting, `go vet`,
   focused tests, and the repository's configured lint/security checks.
3. Read changed files end to end and inspect each finding in context. Check
   error flow, cancellation, goroutine termination, resource cleanup, API
   compatibility, input validation, package ownership, tests, and documentation.
4. Report findings with severity, exact file/line, violated contract or source,
   impact, and the smallest safe fix. Use `references/finding-template.md`.
5. Reread every finding against the current source. Remove anything that cannot
   be justified by a concrete failure, contract, or primary source.
6. Separate blockers from optional suggestions. Do not edit the worktree unless
   the parent explicitly assigns a writer pass.

## Verdicts

- `PASS`: no blocking or worthwhile correctness findings and required evidence
  is present.
- `PARTIAL`: no known blocker, but required behavior or validation evidence is
  missing.
- `FAIL`: a concrete blocker or regression is present.
- `BLOCKED`: the review cannot run because required files/tools are unavailable.

## References

- [Review checklist](references/review-checklist.md)
- [Finding template](references/finding-template.md)
- [Review output template](assets/review-template.md)
