# Parallel Execution Protocol

This protocol defines when and how the orchestrator dispatches sub-agents during development work, and how reviewed results are integrated. Tasks are work units; delivery batches are integration and validation units. It applies throughout the implementation, not to a specific phase.

---

## Dispatch Admission (Tiered Execution)

Sub-agent dispatch is an economic decision, not a default. A sub-agent pays a cold-start tax (it re-reads tasks, files, and rules you already hold) and an orchestration overhead (worktrees, handoffs, integration). Dispatch only when parallelism gain and context-isolation value exceed that cost.

Choose per delivery batch:

- **Tier 0 — orchestrator-direct (default)**: tasks are S/M effort, touch ≤ 3 files, you already hold the context, or acceptance is machine-verifiable. Execute directly on the batch integration branch. No sub-agents, no worktrees.
- **Tier 1 — single coder**: L/XL task bundles, heavy exploratory reading, or outputs long enough to pollute your context. Delegate the complete batch to a `worker` sub-agent.
- **Tier 2 — parallel lanes**: only when ALL hold — lane file sets are disjoint, each lane is ≥ L effort, each lane is independently verifiable, and there are ≤ 4 lanes. Launch one `worker` per dependency-ready lane in isolated worktrees.

If the platform does not support sub-agents, execute all tasks sequentially yourself (Tier 0).

---

## Review Admission (Tiered Review)

Apply the cheapest review level that matches the risk:

- **L1 — machine validation (always)**: targeted acceptance checks plus the batch's combined validation.
- **L2 — orchestrator diff review (default)**: you read the integrated diff against every task's acceptance criteria.
- **L3 — independent reviewer (reserved)**: one reviewer per lane (skill `go-code-review`). Mandatory for every Tier 2 lane and for any high-risk work: contract/port format changes, logic code, or cross-surface semantic invariants.

Writer model (see `behavioral-rules.md` rules 18-19):

- Each Tier 2 lane gets exactly one `worker` (coder), then exactly one reviewer, in the same worktree on the same lane branch.
- The reviewer verifies the lane's diff against the per-task acceptance criteria and commits fixes directly to the lane branch — append-only `fix:` commits that reference but never close tasks.
- Reviewers never write MASTER.md, nor drift/adaptive state, nor instruction or memory surfaces; their Review Reports return to you.
- You integrate only lanes whose verdict is APPROVED or FIXED; ESCALATE is resolved by you (with the user when needed). You remain the acceptance-verification authority and the single writer for all shared state.

---

## When to Parallelize

At the start of each development phase, read every open task in that phase and consult `docs/plan/task-breakdown.md` for delivery batches and parallel lane assignments. Revalidate the planned grouping against current dependencies, file overlap, shared tests, review scope, rollback boundaries, and the dispatch admission criteria above before editing.

- Process delivery batches in dependency order; do not consider a batch done as soon as one task is implemented.
- A batch qualifies for Tier 2 only via the admission criteria. If it qualifies, derive dependency-ready execution waves, integrate each wave, then branch the next wave from the updated integration base. Each lane receives the complete batch context plus its assigned task subset.
- Otherwise execute at Tier 0 or Tier 1 — do not force parallelism.

---

## How to Launch Parallel Task Executors

For each parallel lane in the current dependency-ready wave:

1. Prepare the input for each `worker`:
   - Delivery Batch ID, batch goal, rationale, combined validation, and complete ordered task set;
   - Assigned lane ID plus its task IDs and descriptions from the plan;
   - Per-task acceptance criteria, test expectations, and explicit no-test rationales, if any;
   - Per-task memory/governance impact and expected surface updates, if any;
   - Relevant source file paths (from `docs/analysis/module-inventory.md`);
   - Coding standards and resolved project governance context.
2. Launch all ready lane agents **in a single message** (this is how platforms achieve true parallelism). Each agent works in an isolated worktree to prevent file conflicts. Do not launch a downstream lane until its prerequisite commits are integrated.
   - Follow the repository branch convention; otherwise each lane uses `work/{batch_id}-{lane_id}-{slug}`. Lane agents commit their work and return branch/commit references, but do not create shared state.
3. When a coder returns DONE, dispatch one reviewer for the lane (L3 review) with: the lane ID, its assigned task subset, and the per-task acceptance criteria (the reviewer's checklist), the coder's handoff report, the lane branch + worktree path and the lane-level validation commands. The reviewer verifies the diff, commits fixes to the lane branch, and returns a Review Report (verdict APPROVED | FIXED | ESCALATE). Resolve ESCALATE before integrating that lane.
4. When all lanes carry verdict APPROVED or FIXED, consolidate their results:
   - Verify each lane's Review Report and re-verify the acceptance criteria yourself (L2);
   - Consolidate lane commits onto the batch integration branch (`batch/{batch_id}-{slug}` unless the repository requires another convention); resolve conflicts there;
   - Run every task's targeted checks plus the batch's combined validation to verify the integrated changes are coherent;
   - Verify each completed task's acceptance criteria and post its per-task telemetry (including reviewer telemetry, recorded once here). In parallel runs, the orchestrator is the single writer for cumulative drift, MASTER.md, and adaptive state;
   - Verify any reported instruction or memory surface updates are consistent and do not create competing sources of truth.

---

## Progress Synchronization

After the orchestrator consolidates a delivery batch:

- Apply lane completion reports to the phase progress file once; lane agents do not write shared progress state.
- Update MASTER.md with the final accurate completion counts.
- Update the platform's native task tool to reflect all completed tasks.
- Reconcile memory surface updates from parallel agents before moving on.
- Keep resolved instruction surfaces aligned if any lane changed project-level agent instructions.

---

## Merge Risk Mitigation

The `task-breakdown.md` includes merge risk ratings for parallel lanes. Apply these safeguards:

- **Low risk**: Merge freely — lanes touch different files.
- **Medium risk**: Merge sequentially, run tests between each merge.
- **High risk**: Consider running these tasks sequentially instead of in parallel, or use worktree isolation with careful conflict resolution.

---

## Post-Integration Architecture Validation

After the test suite passes on integrated parallel results, perform these architecture-level checks. They go beyond functional correctness to verify structural integrity across lane boundaries.

### Cross-Lane S.U.P.E.R Compliance

Verify that parallel execution did not introduce cross-lane violations:

- **S (Single Purpose)**: No module gained responsibilities from multiple lanes.
- **U (Unidirectional Flow)**: No circular dependencies introduced between code touched by different lanes.
- **P (Ports)**: Interface contracts at lane boundaries remain intact — if Lane A changed a module's API, Lane B's usage still conforms.
- **R (Replaceable)**: No lane created implicit coupling that makes another lane's modules harder to replace.

### Aggregate Telemetry

After consolidating a delivery batch's parallel results, aggregate the adaptive control telemetry:

1. Sum only the `task_drift` contributions returned by lane agents and not already recorded.
2. Add that sum to cumulative `drift_score` once in MASTER.md.
3. Evaluate thresholds against the new cumulative score.
4. If any threshold is exceeded → trigger the appropriate response (see `references/adaptive-control.md` § "Automatic Response Actions") BEFORE starting the next delivery batch.
