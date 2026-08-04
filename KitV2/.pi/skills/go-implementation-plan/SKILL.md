---
name: go-implementation-plan
category: workflow
tags: [planning, implementation-plan, review, tasks]
last-verified: 2026-08-04
description: Create a reviewable, source-backed implementation plan for a non-trivial Go change. Use before writing code when the request spans multiple files, needs a recipe or architecture decision, or has meaningful testing, compatibility, or operational risk.
---

# Go implementation plan

Use this skill to plan; do not implement application code in the same pass.

## Procedure

1. Read the consumer project's local `.pi/memory/` and applicable `AGENTS.md`.
   If memory is absent, use the project's memory workflow before continuing.
2. Inspect the smallest relevant code surface end to end: entry points, callers,
   tests, configuration, and existing kit recipes. Search before inventing a
   helper, interface, package, or dependency.
3. Restate the requested behavior as observable acceptance scenarios. Separate
   confirmed requirements, assumptions, unknowns, and explicit non-goals.
4. Select the smallest matching registry recipe. If none fits, justify the
   smallest standard-library or existing-dependency design and name rejected
   alternatives.
5. Write a plan artifact with exact paths, symbols or interfaces, dependency
   order, focused checks, behavior checks, risks, rollback/stop conditions, and
   the final approval boundary. Use `references/plan-artifact.md`.
6. Cite primary documentation for Go APIs, security rules, public contracts, and
   library decisions. Record source and verification date using
   `references/source-ledger.md`.
7. Stop with a reviewable plan. Do not mark tasks complete and do not edit
   application code until the plan is approved.

## Decision rules

- Prefer the existing kit recipe over a new abstraction.
- Prefer the standard library over a new dependency when it covers the need.
- Keep public contracts and schemas unchanged unless the user approves a
  deliberate change.
- Keep one writer for a worktree; parallelize only independent research or
  read-only review.
- A plan is not evidence of behavior. Every acceptance criterion starts
  `PENDING` and becomes `PASS` only after the scenario runs.

## Output contract

End the artifact with:

- `Plan complete`;
- the exact artifact path;
- open questions or explicit assumptions;
- the approval needed before implementation.

Do not claim that a plan, test, or scenario passed merely because it was written.

## References

- [Plan artifact](references/plan-artifact.md)
- [Source ledger](references/source-ledger.md)
