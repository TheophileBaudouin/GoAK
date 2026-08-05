# Deep analysis — zhu1090093659/spec_driven_develop

Date: 2026-08-05. Method: read-only clone outside the repository (commit
`14f8c0f`, 57 files, 724K), full file reading, overlap mapping with the kit.
License: MIT (LICENSE verified). This document is the evidence of the
integration plan `docs/plans/2026-08-05-spec-driven-dev-integration.md`; it
does not copy the bodies (translation/adaptation in the kit).

## 1. Repository structure

```text
spec_driven_develop/
├── AGENTS.md / CLAUDE.md              # project instructions (agents)
├── README.md / README.zh-CN.md        # bilingual documentation
├── plugins/spec-driven-develop/       # self-contained plugin
│   ├── .claude-plugin/plugin.json     # Claude Code manifest
│   ├── .codex-plugin/plugin.json      # Codex manifest
│   ├── opencode-plugin.js             # opencode entrypoint
│   ├── skills/
│   │   ├── spec-driven-develop/       # WORKFLOW CORE
│   │   │   ├── SKILL.md               # 7 phases (0-6), v1.15.0
│   │   │   └── references/
│   │   │       ├── behavioral-rules.md    # 19 non-negotiable rules
│   │   │       ├── super-philosophy.md    # S.U.P.E.R
│   │   │       ├── parallel-protocol.md   # tiered dispatch/review
│   │   │       ├── adaptive-control.md    # closed loop (drift)
│   │   │       ├── github-integration.md  # Issues/Milestones/PRs
│   │   │       └── templates/             # analysis, plan, progress,
│   │   │                                  # governance, archive
│   │   ├── deep-discuss/SKILL.md      # structured 7-phase discussion (zh)
│   │   └── review-spd/
│   │       ├── SKILL.md               # findings-first review
│   │       ├── references/ (output-format, reviewer-template)
│   │       └── scripts/review-context.py
│   └── agents/ (project-analyzer, task-architect, task-executor,
│                code-reviewer)
├── scripts/ (install-*, validate.sh, export-progress.py, review-context.py)
└── docs/archives/ (2 archived runs: adaptive-control-layer,
                    orchestrator-centric-execution-model)
```

## 2. The core: 7 phases (SKILL.md spec-driven-develop)

| Phase | Name | Output |
| --- | --- | --- |
| 0 | Quick Intent Capture | 1-2 sentence direction statement |
| 1 | Deep Project Analysis | `docs/analysis/` (project-overview, module-inventory with S.U.P.E.R scores, risk-assessment with S.U.P.E.R health) + GitHub pre-flight |
| 2 | Intent Refinement | confirmed task definition (targeted questions) |
| 3 | Task Decomposition | `docs/plan/` (task-breakdown, Mermaid dependency-graph, milestones) + delivery batches + adaptive states |
| 4 | Progress Tracking | `docs/progress/MASTER.md` + phase files + governance/memory resolution |
| 5 | Confirm & Execute | tiered execution + tiered review + batch PR (GitHub) + adaptive telemetry |
| 6 | Archive | `docs/archives/<project>/` + index |

Structuring concepts: **S.U.P.E.R** (S single purpose, U unidirectional flow,
P ports over implementation, E environment-agnostic, R replaceable parts +
10-point review checklist, 🟢🟡🔴 scoring); **adaptive control** (telemetry
effort/SUPER/unplanned deps, cumulative drift_score, 20/40/60 % thresholds →
annotate/replan/rescope); **tiered dispatch** (Tier 0 orchestrator-direct,
Tier 1 one coder, Tier 2 parallel lanes ≤ 4 disjoint); **tiered review** (L1
machine, L2 orchestrator diff, L3 independent reviewer, verdicts
APPROVED/FIXED/ESCALATE); **writer model** (orchestrator = single writer of
shared state; reviewers commit `fix:` on the lane branch only); **behavioral
rules** (19, incl.: never skip phases, confirmation at every boundary,
dual-write progress, MASTER.md first each session, mandatory post-task
telemetry, mandatory governance resolution, no competing truth sources, tests
by default, durable learnings → memory, sub-agents = economic decision).

## 3. Companion skills

- **deep-discuss** (Chinese): 7 structured discussion phases (receive,
  problem audit = quality gate, deep multi-angle analysis with confidence
  levels, 2-3 option design, self-review, final review, optional "go"
  execution). Philosophy: "don't rush to answers — think the problem through
  first."
- **review-spd**: findings-first review; 3 mutually exclusive targets
  (uncommitted by default, date-range with 3-day default, branch vs main or
  explicit base); size-based planning (small = Correctness+Tests, medium = +
  Regression, large/risky = + Security/Performance); 5 reviewer focuses
  (correctness, regression, tests, security, performance); findings-first
  output by severity with Impact/Evidence/Trigger/Fix/Test gap; "No findings"
  preferred over weak findings.

## 4. Agents (Claude Code sub-agent prompts)

- **project-analyzer**: focus-based analysis (architecture & stack, module
  inventory with S.U.P.E.R, risks/tests/governance); output aligned on the
  analysis templates.
- **task-architect**: strategy (bottom-up/top-down/strangler/big-bang),
  phases, tasks (independently verifiable checkbox acceptance criteria),
  lanes, delivery batches, milestones, Mermaid graph, critical path.
- **task-executor**: executes a complete batch or one lane; input contract
  (batch, tasks, criteria, telemetry); isolation (no PR, no closing keywords,
  no shared state); structured handoff report; explicit BLOCKED.
- **code-reviewer**: independent lane reviewer; verifies acceptance criteria
  by running the checks itself; append-only `fix:` commits; verdicts
  APPROVED/FIXED/ESCALATE; prohibitions (no Issues/PRs, no MASTER.md/drift/
  governance).

## 5. Scripts

- `validate.sh`: consistency guard (resolved references, manifest/files
  parity, 4-site version, JSON, ESM, py_compile, exporter smoke) — the C2-role
  equivalent in the source repository.
- `review-context.py`: git context collector (uncommitted / --since/--until /
  --branch --base) — review-spd utility script.
- `export-progress.py`: progress JSON export (Linear/Jira/Notion).
- `install-*.sh`: multi-agent installation (Claude/Codex/opencode/Cursor).

## 6. Lessons and pitfalls of the repository (useful for the adaptation)

- **Skills-only**: workflows are invoked through skills, not slash commands —
  the kit must follow (skill auto-triggered by the description).
- **Single-sourcing**: each topic has exactly one canonical home (one
  reference per topic); prompts never re-explain, they cite.
- **Dual-write progress**: no single point of failure for state.
- **Tests by default**: every feature task requires tests, otherwise an
  explicit reason + the closest validation.
- **Governance by default**: every stable rule → resolved memory surface;
  never a competing truth source; file fallback only if chosen.
- **Sub-agents = economic decision**: cold-start tax vs parallelism gain.
- **S.U.P.E.R is architecture doctrine**: Clean/Hexagonal/12-Factor — in
  potential conflict with the kit's sourced Go doctrine (to bound).

## 7. Overlap mapping with the kit (before integration)

| spec-driven | Kit existing | Verdict |
| --- | --- | --- |
| Phase 0 intent | none | missing → add |
| Phase 1 deep analysis | scout/researcher (sub-agents) | missing as a phase → add |
| Phase 2 refinement | workflow-clarify | overlap → replace |
| Phase 3 decomposition | workflow-plan + workflow-tasks | overlap → replace |
| Phase 4 progress/governance | workflow-memory | partial overlap → adapt |
| Phase 5 execution | workflow-implement + workflow-verify | overlap → replace |
| Phase 6 archive | none | missing → add |
| S.U.P.E.R | rules/core/philosophy, universal | doctrinal conflict → bound |
| adaptive control | "3 failures → stop" | complementary → add |
| review-spd | go-code-review | duplicate → merge |
| deep-discuss | none | complementary → add |
| github-integration | none (LOCAL_ONLY decided) | excluded (decision) |
| 4 agents | Pi sub-agent contracts (scout/planner/worker/reviewer) | documented mapping |

Integration decisions (user, 2026-08-05): replace the workflow-* chain with
phases 0-6; English mandatory (D-2026-08-05-21); LOCAL_ONLY only; bounded by
contract Z12 + audit, without touching KIT_CHARTER.md.

## Confidence

Facts verified by direct file reading (paths, phase numbers, rules 1-19,
10-point checklist, 20/40/60 thresholds). Interpretations (the "S.U.P.E.R =
doctrine in potential conflict" lesson, role mapping) are labeled as such.
