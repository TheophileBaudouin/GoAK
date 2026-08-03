# Plan artifact

Use this structure for `docs/plans/YYYY-MM-DD-<change>.md` or the project's
established plan path. Adapt headings when the repository already has a
contract; do not create duplicate ledgers.

```markdown
# <Change> Implementation Plan

**Goal:** <observable outcome>

**Context:** <relevant current flow and chosen recipe>

**Constraints:** <compatibility, trust boundaries, dependencies, limits>

**Done when:** <mechanical and behavioral acceptance>

## Non-goals

- <explicitly excluded behavior>

## Acceptance scenarios

- [ ] Given <starting state>, when <user action>, then <observable result>.

## Task 1: <one outcome>

**Files:**
- Modify: `<exact/path>`
- Test: `<exact/path>`

**Depends on:** <task IDs or none>

**Check:** `<exact command>` — expected `<result>`.

**Behavior evidence:** `<exact command or user action>` — expected `<result>`.

## Risks and stop conditions

- <risk, mitigation, and condition that requires returning to the user>

## Sources

- <primary URL or local documentation path>

Plan complete: `<artifact path>`
Approval required before implementation.
```

## Task granularity

One task should produce one verifiable outcome. Split implementation, focused
test, check, and behavior probe when each needs an independent result. Do not
force artificial two-minute tasks when a single small change is already
independently verifiable.

## Quality gate

Reject the plan as incomplete when it has vague paths, hidden dependencies,
missing failure behavior, unbounded input, an unapproved public-contract change,
or an acceptance criterion that cannot be observed. Return to clarification
instead of guessing.
