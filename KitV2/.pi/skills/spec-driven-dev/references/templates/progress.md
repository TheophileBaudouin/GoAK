# Progress Document Templates

Templates for the tracking documents generated in Phase 4 (Progress Tracking Documentation). Output to `docs/progress/`.

---

## MASTER.md (LOCAL_ONLY mode)

```markdown
# MASTER — Spec-Driven Develop Run

## Task

**Name**: <task name (Phase 2)>
**Tracking mode**: `LOCAL_ONLY`
**Confirmed task definition**: <link or short summary>

## Documents

- Analysis: [project-overview.md](../analysis/project-overview.md) ·
  [module-inventory.md](../analysis/module-inventory.md) ·
  [risk-assessment.md](../analysis/risk-assessment.md)
- Plan: [task-breakdown.md](../plan/task-breakdown.md) ·
  [dependency-graph.md](../plan/dependency-graph.md) ·
  [milestones.md](../plan/milestones.md)

## Phases

- [ ] Phase 1: <name> (0/N tasks) — [phase file](phase-1-<name>.md)
- [ ] Phase 2: <name> (0/N tasks) — [phase file](phase-2-<name>.md)

## Governance Status

| Surface | Status | Notes |
|:--------|:-------|:------|
| `AGENTS.md` | existing / created / unused | shared agent rules |
| `.pi/memory/` | verified — files present: | **verify which files actually exist (Decisions.md may be missing from the Pi bootstrap)** |
| Memory fallback | approved / not | never created silently |

## Current Status

<current state, updated at the start and end of each work session>

## Next Steps

<exact next action>

---

## Adaptive Control State

| Field | Value |
|-------|-------|
| drift_score | 0 |
| strategy | <strategy> |
| threshold_annotate | <computed> |
| threshold_replan | <computed> |
| threshold_rescope | <computed> |
| total_tasks | <count> |
| completed_tasks | 0 |
| last_updated | <ISO-8601> |

### Task Telemetry Log

| Task ID | Est. | Actual | Δ Effort | SUPER Score | SUPER Δ | Unplanned Deps | Task Drift |
|---------|------|--------|----------|-------------|---------|----------------|------------|
```

---

## Phase file (LOCAL_ONLY mode)

One `docs/progress/phase-N-<short-name>.md` per phase.

```markdown
# Phase N : <phase name>

**Goal**: <phase goal>
**Prerequisite**: <what must be done before>

## Tasks

- [ ] **T1.1** — <description>
  - **Priority**: P0/P1/P2 | **Effort**: S/M/L/XL
  - **Depends on**: <IDs or "None">
  - **Lane**: A/B/—
  - **S.U.P.E.R**: <principles>
  - **Acceptance criteria**:
    - [ ] <verifiable criterion>
    - [ ] Passes the S.U.P.E.R Quick Check for: <principles>
    - [ ] Satisfies the test expectation: <tests or no-test reason>
    - [ ] Updates the resolved memory/instruction surfaces if durable knowledge
          or agent instructions changed

## Notes

<!-- Decisions, conflicts, context — behavioral rule 3 -->
```
