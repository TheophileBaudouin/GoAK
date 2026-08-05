---
name: go-code-review
category: workflow
tags: [review, code-review, diff, evidence, verification]
last-verified: 2026-08-05
description: "Review a Go diff for correctness, regressions, maintainability, and evidence quality. Use before merging or handing off non-trivial Go changes, especially when a fresh-context reviewer should challenge the implementer's assumptions; do not use it as an automatic approval. Supports three targets: uncommitted changes (default), commits in a date range (default last 3 days), and a branch compared to the main branch or an explicit base."
---

# Go code review

Review the actual diff and repository behavior. Do not review a worker's summary
instead of the files.

## Target modes (mutually exclusive)

Three targets, resolved in this order of priority: `branch` specified → branch
mode; else `since`/`until` → commit-range mode; else uncommitted mode. `base`
applies only to branch mode. Vague requests ("review this") → uncommitted mode;
"recent commits" without dates → last 3 days.

1. **Uncommitted mode** (default) — working tree + staged changes.
2. **Commit-range mode** — commits in a date range; no explicit range → last 3 days.
3. **Branch / PR mode** — branch vs `origin/main`, `origin/master`, the remote
   default branch, or an explicit `base`.

Collect the diff context with git only (never judge from a summary):

```sh
git status --short
git diff --stat && git diff          # uncommitted
git log --since "3 days ago" --oneline && git diff HEAD~N  # commit-range
git diff origin/main...HEAD         # branch mode
```

If there are no changes, stop and say there is nothing to review. Do not invent
findings.

## Review planning by size

- **Small** (≤ 3 files, localized diff): cover Correctness + Tests.
- **Medium** (multiple files / behavior-affecting): add Regression/Compatibility.
- **Large or high-risk** (broad changes, auth/permissions, persistence,
  migrations, concurrency, caching, money, security, public APIs, generated
  code, config/deployment): add Security/Data Safety + Performance/Concurrency.

Prioritize behavior code, public contracts, data handling, error paths,
configuration, persistence, tests. Deprioritize docs, formatting-only changes,
generated files, lockfile churn unless they affect runtime behavior.

## Focused reviewer dimensions

When sub-agents are available (or sequentially otherwise), split the review
into focused reviewers — one focus per sub-agent :

- Correctness / Bug Risk
- Regression / Compatibility
- Tests / Verification
- Security / Data Safety
- Performance / Concurrency

Each reviewer returns only evidence-backed candidate findings for its own
focus. Full contract: `references/reviewer-focus.md`.

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
   Findings-first: present findings before any summary; never bury a bug
   under a summary. No findings → explicitly state `No findings` and list
   residual risks or testing gaps.
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
- [Focused reviewer dimensions](references/reviewer-focus.md)
