---
name: spec-driven-dev
category: workflow
tags: [spec-driven, workflow, planning, analysis, s-u-p-e-r, adaptive-control, large-scale, migration, refactor]
last-verified: 2026-08-08
description: "Spec-driven development workflow for large-scale Go transformations (rewrite, migration, overhaul, whole-project refactor). Use when the user requests a large-scale project transformation that needs deep analysis, phased task decomposition, progress continuity across sessions, and execution within one session — not for ordinary single-task work. Runs the seven-phase pipeline: intent capture, deep analysis with S.U.P.E.R health scoring, grounded intent refinement, task decomposition with delivery batches, progress tracking (MASTER.md), confirmed execution with adaptive control, and archive. Local-only: no GitHub dependency. Composes the kit's existing prompts and skills (memory, planning, review, testing) instead of duplicating them."
---

# Spec-driven develop

You are executing the **Spec-Driven Development** workflow — a seven-phase pipeline (Phases 0-6) for large-scale complex tasks. Complete the preparation phases (analysis, planning, progress setup), then execute the plan — all within a single session.

**Behavioral rules**: `references/behavioral-rules.md` — read and follow them in every phase; they are non-negotiable.

## Configuration

| Path | Default Value | Purpose |
|:---|:---|:---|
| Analysis output | `docs/analysis/` | Phase 1 analysis documents |
| Plan output | `docs/plan/` | Phase 3 planning documents |
| Progress output | `docs/progress/` | Phase 4 tracking documents (incl. MASTER.md) |
| Instruction surfaces | Resolved per project | Project-level constraints for agents (see Phase 4) |
| Memory surface | `.pi/memory/` first | Durable facts via the agent's native memory; no silent file fallback |
| Archive output | `docs/archives/<project>/` | Phase 6 archived artifacts |
| Task tracking mode | `LOCAL_ONLY` | Pure local workflow (no GitHub dependency) |
| Delivery batching | Phase-first | Batches = local integration and validation units |
| Adaptive control | Enabled | Drift thresholds: annotate=20 %, replan=40 %, rescope=60 % of phase tasks |

**Canonical references** (each topic has exactly one home — cite it, never re-explain it):

| Reference | Owns |
|:---|:---|
| `references/behavioral-rules.md` | All behavioral rules (1-19) |
| `references/adaptive-control.md` | Telemetry collection, drift calculation, response actions, state storage, controller activation |
| `references/parallel-protocol.md` | Dispatch/review admission (tiers), lane/worktree protocol, review loop, merge risk, post-integration checks |
| `references/super-philosophy.md` | S.U.P.E.R principles + the 10-check review checklist |
| `references/templates/` | Schemas for every generated document (analysis, plan, progress, governance, archive) |

## Before You Begin: Cross-Conversation Continuity Check

**CRITICAL**: Before starting any phase, inventory and read any existing project-level instruction and memory surfaces (`AGENTS.md`, the native memory `.pi/memory/` — **verify which memory files actually exist; the native memory extension auto-bootstraps the five files (Brief, Progress, Gotchas, Decisions, Agent) when missing** — any existing platform rule files, and the project foundation `workspace/` when present: if `workspace/CONSTITUTION.md` and `workspace/ARCHITECTURE.md` exist — initialized by the `workspace-init` skill at day 0 — read them now and keep every phase consistent with them; the foundation is captured once, never re-derived per feature).

Then check if `docs/progress/MASTER.md` already exists:

- If it **exists**: Read it immediately. You are resuming an in-progress task. Identify the current phase and completed work; continue from the exact point where the previous conversation left off. Do NOT restart from Phase 0.
- If it **does not exist**: This is a fresh start. Proceed to Phase 0.

After loading your current state, populate the platform's native task tracking tool (e.g. todo) with the active phase's pending tasks: content = task description, status = in-progress for the active task, priority mapped P0=high, P1=medium, P2=low. If no native task tool is available, skip this step — MASTER.md alone is sufficient.

---

## Phase 0: Quick Intent Capture

**Goal**: Capture the user's high-level transformation direction in 1-2 sentences — just enough to give Phase 1 analysis a focus.

**Actions**:

1. Extract from the user's message: the transformation type, the rough target state, and any explicitly stated constraints.
2. Summarize the direction back in 1-2 sentences. Do NOT ask deep clarifying questions here — Phase 1 analysis will reveal what to ask. Confirm: "I understand you want to [direction]. Let me first analyze the current project so I can ask you the right questions." If a project foundation (`workspace/`) exists, the direction must be consistent with its CONSTITUTION.md and ARCHITECTURE.md (read in the continuity check).
3. If intent is completely unclear, ask ONE high-level question to determine the transformation type.

**Output**: A preliminary direction statement guiding Phase 1. NOT the final task definition — that comes in Phase 2.

---

## Phase 1: Deep Project Analysis

**Goal**: Build a comprehensive understanding of the current codebase, informed by the Phase 0 direction.

**Actions**:

1. Before analyzing, call `search_kit_resources` (skill `kit-resource-routing`) to route to the relevant rules, recipes, and catalogs — do not scan the kit tree manually.
2. Launch the analyses in parallel (`scout`/`researcher` sub-agents when available, otherwise sequentially yourself), split by focus area:
   - **Architecture & Stack**: structure, directory layout, tech stack, entry points, build/run commands.
   - **Module Inventory**: each module's responsibility, public API surface, size, dependencies — evaluated against all five S.U.P.E.R principles with a per-principle compliance rating.
   - **Risks, Tests & Governance**: transformation risks, complexity hotspots, coding conventions, test coverage, instruction/memory surfaces — plus a S.U.P.E.R Architecture Health Summary with violation hotspots (priority targets for the plan).
   Give each analysis the Phase 0 direction AND `references/super-philosophy.md`.
3. Consolidate outputs, resolve contradictions, and write the `docs/analysis/` documents from `references/templates/analysis.md`:
   `project-overview.md`, `module-inventory.md` (per-module S.U.P.E.R scores), `risk-assessment.md` (S.U.P.E.R health summary).

**Output**: Complete `docs/analysis/` (three documents). The S.U.P.E.R assessment is the architectural baseline for all subsequent phases.

---

## Phase 2: Intent Refinement & Confirmation

**Goal**: With the project analyzed, finalize the task definition through a grounded discussion.

**Actions**:

1. Present key Phase 1 findings: brief architecture summary, notable S.U.P.E.R health issues, and coupling/complexity highlights relevant to the transformation.
2. Ask **targeted questions grounded in the analysis** — specific and informed, not generic (e.g., about circular dependencies found, hardcoded environment assumptions, missing interface contracts). Use the platform's structured question tool (`ask_user_question` in Pi) — never plain text. At minimum confirm:
   - **Scope** — which modules from the inventory are in scope;
   - **Target** — target technology/architecture/state;
   - **Constraints** — timeline, backward compatibility, libraries, deployment targets;
   - **Priorities** — performance, maintainability, feature parity (use the risk assessment);
   - **S.U.P.E.R priorities** — which violations to fix now vs. defer;
   - **Testing policy** — which test layers protect changes; whether to establish a minimal test harness if none exists;
   - **Project governance** — canonical instruction surfaces; native memory surface or explicitly named fallback.
3. Summarize the refined understanding and get explicit confirmation.

**Output**: The authoritative, confirmed task definition guiding Phases 3-6.

---

## Phase 3: Task Decomposition

**Goal**: Break the transformation into manageable, trackable tasks organized in phases, with parallel lanes and coherent delivery batches.

**Actions**:

1. Launch the task architect (`planner` sub-agent when available, otherwise yourself) with the full Phase 1 analysis AND the confirmed Phase 2 definition. If multiple strategies are plausible, explore 2 different approaches (e.g., bottom-up vs. strangler fig) and keep the better result. Compose the kit's planning logic (`go-implementation-plan`, plan artifact, source ledger) — do not duplicate.
2. The decomposition must produce:
   - **Phases** ordered by dependency; early phases prioritize fixing S.U.P.E.R violation hotspots before new features.
   - **Tasks**, each with: description, priority (P0/P1/P2), effort (S/M/L/XL), dependencies, S.U.P.E.R design drivers, acceptance criteria, test expectation, and memory/governance impact. Every task's acceptance criteria implicitly include passing the S.U.P.E.R Quick Check for its listed principles.
     - **Testing is default**: tasks changing user-visible features, behavior, API contracts, schemas, migrations, parsing, routing, permissions, caching, or persistence MUST add or update automated tests; documentation/config tasks may mark tests N/A with an explicit reason.
     - **Governance is default**: tasks introducing a stable rule, gotcha, or convention must include updating the resolved memory surface (and instruction surfaces if the rule affects future agents).
   - **Parallel execution lanes** per phase: group mutually independent tasks; assess merge risk (file overlap).
   - **Delivery batches** (local units, no PRs): after reviewing the complete phase task set (dependencies, file overlap, shared validation, rollout risk, rollback boundary), assign every task to exactly one batch. Default to one coherent batch per phase; split only for a documented reviewability, release/rollback, ownership, risk-isolation, dependency, or policy reason. Record per batch: ID, goal, task IDs, execution waves, lanes, integration branch, combined validation, dependency order, split rationale.
   - **Dependency graph** as a Mermaid diagram (subgraphs for batch boundaries and lanes) and **milestones** at phase boundaries.
3. Write the `docs/plan/` documents from `references/templates/plan.md`: `task-breakdown.md`, `dependency-graph.md`, `milestones.md`.
4. **Initialize Adaptive Control State**: for each phase, compute the percentage-based drift thresholds and append the adaptive YAML block to MASTER.md (Phase 4) per `references/adaptive-control.md` § "Adaptive State Storage".

**Output**: Complete `docs/plan/` (three documents) with adaptive state initialized.

---

## Phase 4: Progress Tracking Documentation

**Goal**: Create a progress tracking and governance system that survives across conversations.

**Actions**:

Use `references/templates/progress.md` for progress documents and `references/templates/governance.md` for governance records.

### Project Governance Surface

1. **Inventory existing surfaces**: shared instruction files (`AGENTS.md` or equivalent), existing platform rule files, and the agent's native memory `.pi/memory/` — **verify which memory files actually exist** (the native memory extension auto-bootstraps the five files — Brief, Progress, Gotchas, Decisions, Agent — when missing); never assume the standard set is complete.
2. **Update instruction surfaces without overwriting**: shared rules → `AGENTS.md`; platform rule files only when they already exist or are requested. Preserve user-written sections, local commands, and security constraints. If an existing rule conflicts with the plan, do not silently replace it — record the conflict in MASTER.md and ask the user at the next checkpoint.
3. **Resolve the memory surface**: prefer native memory `.pi/memory/`; never silently create a Markdown memory file; use a repo-local fallback only on user confirmation or existing project declaration. Record the resolution in MASTER.md "Governance Status".

Do not create competing truth sources.

### Local tracking (`LOCAL_ONLY`)

1. Create `docs/progress/MASTER.md`: task name/description, `LOCAL_ONLY` mode, links to analysis/plan documents, phase summary table, links to phase files, "Current Status", "Next Steps".
2. Create one `docs/progress/phase-N-<short-name>.md` per phase: checkbox tasks with inline acceptance criteria plus a "Notes" section.
3. Add the "Adaptive Control State" section and a "Task Telemetry Log" table to MASTER.md per `references/adaptive-control.md` § "Adaptive State Storage".

### Common to all modes

- Phases use `- [ ] Phase N: <name> (0/X tasks)` linking to the phase file; `- [x] Phase N: <name> (X/X tasks)` when done.
- "Current Status" is updated at the start and end of each work session.

**Output**: Complete `docs/progress/` with MASTER.md and the phase files.

---

## Phase 5: Confirm & Execute

**Goal**: Present the preparation artifacts, get confirmation, then execute the plan.

**Actions**:

### 5a. Summary & Confirmation

1. Present: task definition (Phase 2), key findings (Phase 1), phased plan with task counts (Phase 3), delivery batch overview with split rationales (Phase 3), progress system description (Phase 4), and the execution model (tiered dispatch: orchestrator-direct by default; executor/reviewer sub-agents per `references/parallel-protocol.md` § "Dispatch Admission").
2. List all generated artifacts (analysis, plan, and progress documents; resolved instruction and memory surfaces).
3. Ask the user: "All preparation is complete. Ready to begin execution?" (structured question tool).

### 5b. Execution

1. **Process each phase sequentially.** Before editing, reread the phase's open tasks and revalidate the planned batches against current dependencies, affected files, review scope, and repository rules. If the mapping must change, update `task-breakdown.md`, MASTER.md, and the "Delivery Batch" field of every affected task; comment the regrouping reason so all execution surfaces agree.
2. **Choose the execution tier for each delivery batch** per the admission criteria in `references/parallel-protocol.md` § "Dispatch Admission (Tiered Execution)":
   - **Tier 0 — orchestrator-direct (default)**: S/M effort, ≤ 3 files, context already held, or machine-verifiable acceptance. Execute directly on the batch integration branch.
   - **Tier 1 — single coder**: L/XL bundles or context-heavy exploration. Delegate the complete batch to a `worker` sub-agent.
   - **Tier 2 — parallel lanes**: only when ALL hold — disjoint lane file sets, ≥ L effort per lane, independent verifiability, ≤ 4 lanes. Launch one `worker` per dependency-ready lane in isolated worktrees, in waves, each with the full batch context plus its task subset. Lane agents never create PRs or shared state.
   - Branch convention: repository's own; otherwise `batch/{batch_id}-{slug}` (integration) and `work/{batch_id}-{lane_id}-{slug}` (Tier 2 lanes only).
3. **Review before integrating** per `references/parallel-protocol.md` § "Review Admission (Tiered Review)":
   - **L1 — machine validation (always)**: every task's targeted checks plus the batch's combined validation.
   - **L2 — orchestrator diff review (default)**: personally read the diff against every task's acceptance criteria.
   - **L3 — independent reviewer (reserved)**: one reviewer per lane, mandatory for Tier 2 lanes and high-risk work (contract/port formats, logic code, cross-surface semantic invariants) — use the `go-code-review` skill. Verdict APPROVED | FIXED | ESCALATE; integrate only APPROVED or FIXED lanes; resolve ESCALATE yourself (with the user when needed). You remain the acceptance-verification authority and the single writer for all shared state.
4. **After each task completion** — follow `references/adaptive-control.md` § "Controller Activation": collect telemetry, update the cumulative `drift_score`, write telemetry to MASTER.md, and execute automatic threshold responses. For parallel lanes, lane agents return per-task telemetry and you record it once during batch integration.
5. **Integrate and validate each delivery batch**: consolidate reviewed lane branches onto the batch integration branch; reconcile overlaps; run per-task checks plus combined validation and post-integration architecture checks; verify every completed task's acceptance criteria yourself (L2). One batch = one validated integration (local commit or branch per repository convention); no PR.
6. **Progress updates**: check off tasks in the phase files; update MASTER.md counts; durable knowledge → resolved memory surface (`.pi/memory/`); agent-behavior changes → resolved instruction surfaces.
7. **When all tasks are complete** (all checkboxes checked): proceed to Phase 6.

**Output**: All planned tasks implemented and verified.

---

## Phase 6: Archive

**Trigger**: All tasks complete — all checkboxes `[x]`.

**Goal**: Archive all workflow artifacts for traceability, then clean up working directories.

**Actions**:

1. Announce completion to the user.
2. Determine the archive directory name from the Phase 2 task name (lowercase, hyphens, no special characters): `docs/archives/<project-name>/`. Target structure and index template: `references/templates/archive.md`.
3. Move `docs/analysis/`, `docs/plan/`, and `docs/progress/` into the archive; copy snapshots or export notes for the resolved instruction and memory surfaces into `docs/archives/<project-name>/governance/`; move any other temporary workflow files.
4. Create or update `docs/archives/README.md` with an entry: project name, one-line description, date range, link to the archived MASTER.md.
5. Remove the now-empty `docs/analysis/`, `docs/plan/`, `docs/progress/` directories. Keep active instruction and memory surfaces in place; only their snapshots live under the archive.
6. Suggest the user commit the archive to version control.

**Output**: All artifacts under `docs/archives/<project-name>/` with an updated `docs/archives/README.md` index.
