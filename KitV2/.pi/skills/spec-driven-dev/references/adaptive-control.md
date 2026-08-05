# Adaptive Control Protocol

Closed-loop feedback control for the Spec-Driven Develop workflow: how execution telemetry is collected, how plan-vs-reality drift is measured, and what automatic corrective actions fire when drift exceeds thresholds.

---

## Core Concepts

| Control Theory Concept | Workflow Mapping |
|:---|:---|
| **Plant** | The codebase under transformation |
| **Set point** | Phase 2 confirmed task definition + S.U.P.E.R principles |
| **Controller** | The SKILL workflow (Phases 0-6) + this protocol |
| **Actuator** | Delivery batch executors and lane workers |
| **Sensor** | Post-task telemetry collection |
| **Error signal** | `drift_score` — cumulative plan-vs-reality deviation |

---

## Telemetry Collection

After completing every task and BEFORE marking it as done, collect three signals.

### Actual Effort

Compare estimated effort (from `task-breakdown.md`) against actual:

| Level | Criteria |
|:---|:---|
| S | Completed in < 30 minutes, no unexpected issues |
| M | 30 min – 2 hours, minor surprises |
| L | 2 – 4 hours, or significant unexpected complexity |
| XL | > 4 hours, or required fundamental re-thinking |

Record the **effort delta** as levels between estimated and actual (estimated M / actual M → 0; S → L → +2; L → M → -1).

### S.U.P.E.R Score Delta

Run the 10-check checklist in `super-philosophy.md` § "S.U.P.E.R Code Review Checklist (10 checks)". Record `super_score` (passes out of 10) and `super_delta` (change vs. pre-task state). No improvement where the task's S.U.P.E.R drivers promised improvement → delta = 0 (counts as deviation); regression → negative.

### Unplanned Dependencies

Count dependencies discovered during execution that were NOT in the task's "Dependencies" field: unlisted files modified, unidentified prerequisite tasks, external libraries/APIs that needed changes.

---

## Drift Score Calculation

### Per-Task Drift Contribution

```text
task_drift = max(0, effort_delta) + (1 if super_delta <= 0 AND task had SUPER drivers else 0) + min(unplanned_deps, 2)
```

Only positive effort deltas count. Unplanned deps are capped at 2 per task.

### Cumulative Drift Score

```text
drift_score = sum of all task_drift values for completed tasks
```

### Percentage-Based Thresholds

Relative to the **total task count of the current phase**, computed once at phase start:

```text
threshold_annotate = ceil(total_tasks * 0.20)
threshold_replan   = ceil(total_tasks * 0.40)
threshold_rescope  = ceil(total_tasks * 0.60)
```

---

## Automatic Response Actions

### Annotate (drift ≥ threshold_annotate)

Mild deviation; plan still viable. Automatically:

1. Add a warning line to the next task's entry in the phase file (LOCAL_ONLY).
2. Update the adaptive state (§ "Adaptive State Storage").

### Replan (drift ≥ threshold_replan)

Significant deviation; remaining decomposition is likely inaccurate. Automatically:

1. **HALT** — do not start the next task.
2. Annotate MASTER.md:

   ```text
   🔄 Adaptive Control: Replanning triggered (drift_score={n}).
   Remaining tasks will be re-decomposed based on execution learnings.
   ```

3. **Re-enter Phase 3** for the remaining scope only, using completed-task telemetry as estimation input; preserve completed tasks; create new tasks under the same phase.
4. Reset `drift_score` to 0 for the re-planned segment.
5. LOCAL_ONLY: archive old phase file entries and create new ones.

### Rescope (drift ≥ threshold_rescope)

Severe deviation; scope or strategy may be fundamentally wrong. Automatically:

1. **HALT**.
2. Add the scope re-evaluation annotation to MASTER.md:

   ```text
   ## Adaptive Control: Scope Re-evaluation

   drift_score has reached {n}, exceeding the rescope threshold of {threshold}.

   ### Execution Summary
   | Metric | Value |
   |--------|-------|
   | Tasks completed | X/Y |
   | Average effort delta | +Z levels |
   | SUPER improvement rate | N% |
   | Unplanned dependencies | W total |

   ### Recommendation
   The current scope/strategy appears misaligned with project reality.
   Returning to Phase 2 for scope confirmation with the user.
   ```

3. **Re-enter Phase 2** with accumulated execution data as context.
4. After user re-confirms scope, re-enter Phase 3 for all remaining work.
5. LOCAL_ONLY: same flow using MASTER.md annotations.

---

## Adaptive State Storage (LOCAL_ONLY)

**Primary storage**: `docs/progress/MASTER.md` — "Adaptive Control State" section:

```markdown
## Adaptive Control State

| Field | Value |
|-------|-------|
| drift_score | 0 |
| strategy | bottom-up |
| threshold_annotate | 2 |
| threshold_replan | 4 |
| threshold_rescope | 6 |
| total_tasks | 10 |
| completed_tasks | 0 |
| last_updated | 2026-05-17 |

### Task Telemetry Log

| Task ID | Est. | Actual | Δ Effort | SUPER Score | SUPER Δ | Unplanned Deps | Task Drift |
|---------|------|--------|----------|-------------|---------|----------------|------------|
```

---

## Controller Activation

### Session Start

At the start of every conversation, AFTER reading MASTER.md:

1. Read the "Adaptive Control State" section of MASTER.md.
2. Parse `drift_score` and thresholds.
3. If `drift_score` already exceeds a threshold (from a previous session), trigger the response BEFORE executing any new task.
4. Report the adaptive state in the session's opening status.

### Post-Task

For sequential execution, after every task completion:

1. Collect telemetry (§ "Telemetry Collection").
2. Calculate task drift contribution and new cumulative `drift_score` (§ "Drift Score Calculation").
3. Persist the updated adaptive state (§ "Adaptive State Storage").
4. Write telemetry to MASTER.md using the updated cumulative score.
5. If a threshold is exceeded → execute the response BEFORE the next task; otherwise proceed.

For parallel lanes, lane executors perform steps 1-2 and return per-task telemetry, but never steps 3-5 — the orchestrator records and applies contributions once per batch, preventing duplicate increments and concurrent state writes.

### Post-Delivery-Batch Integration

After consolidating all work in a delivery batch:

1. Collect any lane telemetry not yet recorded.
2. Add the sum of only those unrecorded contributions to `drift_score` once; persist.
3. Write each unrecorded task's telemetry to MASTER.md using the post-batch cumulative score.
4. Verify telemetry exists for every task in the batch.
5. If a threshold is exceeded → trigger the response BEFORE the next delivery batch.

---

## Workflow Integration

| Workflow Phase | Adaptive Control Integration |
|:---|:---|
| Phase 3 (Decomposition) | Initialize adaptive state; compute thresholds. |
| Phase 4 (Progress Tracking) | MASTER.md includes the telemetry section and adaptive state. |
| Phase 5 (Confirm & Execute) | Every task completion triggers "Post-Task"; every batch integration triggers "Post-Delivery-Batch Integration". |
| Phase 6 (Archive) | Archive includes the final telemetry summary and drift history as retrospective. |
