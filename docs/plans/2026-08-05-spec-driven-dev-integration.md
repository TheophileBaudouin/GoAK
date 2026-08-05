# Plan — spec-driven-dev integration into the Go Agent Kit (major update)

## Goal

Integrate all the logic of the `zhu1090093659/spec_driven_develop` repository
(MIT, v1.15.0) into the kit: the 7-phase spec-driven workflow (0-6), the
S.U.P.E.R philosophy, adaptive control (drift/telemetry), the tiered
execution protocol, the document templates, deep-discuss, and the
findings-first review discipline — **adapted to the Pi harness and the kit's
existing rules, translated faithfully (English mandatory, D-2026-08-05-21),
without denaturing the logic**, then bounded in the metaproject governance
(contract Z12 + kit audit) so this major asset is always taken into account.

## Context

### Source repository analysis (verified by read-only clone, commit 14f8c0f)

- **Core**: `plugins/spec-driven-develop/skills/spec-driven-develop/SKILL.md`
  (7 phases: 0 intent, 1 deep analysis, 2 refinement, 3 decomposition, 4
  progress/governance, 5 confirm+execution, 6 archive) + 6 references
  (behavioral-rules 19 rules, super-philosophy S.U.P.E.R, adaptive-control,
  parallel-protocol, github-integration, templates analysis/plan/progress/
  governance/archive).
- **Companion skills**: `deep-discuss` (structured 7-phase discussion,
  originally in Chinese) and `review-spd` (findings-first review, 3 targets:
  uncommitted / date-range / branch-PR, 5 review focuses).
- **Agents**: project-analyzer, task-architect, task-executor, code-reviewer
  (Claude Code sub-agent prompts).
- **Scripts**: review-context.py (git collector), export-progress.py,
  validate.sh (consistency guard), install-*.sh.
- Detailed analysis: `docs/research/2026-08-05-spec-driven-dev-analysis.md`.

### Kit state (verified)

- Existing workflow chain: `.pi/prompts/workflow-{clarify,plan,tasks,
  implement,verify}.md` (5 prompts, indexed in the router: prompt=8) +
  `workflow-memory.md`, `checklist-api.md`, `checklist-release.md`.
- Skills `.pi/skills/`: go-code-review, go-idiomatic-implementation,
  go-implementation-plan, go-source-retrieval, go-testing-verification,
  kit-resource-routing (6, indexed in the router: skill=6).
- `KitV2/AGENTS.md` said "Use the native `.pi/prompts/` workflow templates in
  order" — replaced.
- Contract Z8 (17-zone-pi.md) cited `workflow-clarify`, `workflow-plan`, … as
  an example of the "prompts = orchestrators" role — updated.
- `workflow-memory.md` initialized consumer memory without mentioning that the
  Pi bootstrap may not create `Decisions.md`.

### User decisions (2026-08-05, questions asked)

1. **Strategy: replace the existing chain.** Phases 0-6 become THE kit
   workflow; the 5 workflow-*prompts are removed (documented migration). The
   spec-driven-dev skill composes the remaining prompts/skills
   (workflow-memory, go-*, kit-resource-routing) by cross-references.
2. **Language: English mandatory** (fundamental rule D-2026-08-05-21,
   superseding the earlier FR-body decision D-2026-08-05-17). Bodies and
   frontmatter descriptions in English.
3. **Scope: LOCAL_ONLY only.** No GitHub (Issues/Milestones/PRs/gh CLI): pure
   local workflow (docs/analysis, plan, progress, archives); delivery batches
   = local integration/validation units (no PRs). Sub-agents: the tiered
   protocol is kept but mapped onto the native Pi mechanism and remains an
   economic decision; without sub-agents, orchestrator-sequential execution.
4. **Governance: contract Z12 + audit, without the charter.** New contract
   `.agent/kit-governance/22-zone-spec-driven-dev.md`, new kit-audit dimension
   and finding category, decisions D-2026-08-05-16…, Brief/Progress.
   `KIT_CHARTER.md` unchanged.

### Identified conflicts to resolve (adaptation, not copy)

- **S.U.P.E.R vs sourced Go doctrine**: S.U.P.E.R draws on Clean/Hexagonal
  Architecture (U, P); the kit refuses Clean Code/OOP doctrine as default
  (root AGENTS.md) and `rules/core/philosophy` prescribes the smallest
  justified design, stdlib-first, no universal structure. **Resolution**:
  S.U.P.E.R is kept as the workflow's **health evaluation lens** (scoring,
  hotspots) and as a **review checklist**, with an explicit boundary: in
  conflict with a sourced kit rule (philosophy, universal), the kit rule
  wins; P reads "consumer interfaces + explicit contracts" (kit doctrine), E
  reads "environment-driven config, zero hardcoded path" (already kit), R =
  replaceability (already kit), U = consumer-owned dependency direction
  (already kit). Encoded in the adapted super-philosophy reference + Z12.
- **Memory progress vs MASTER.md**: consumer memory `.pi/memory/` (durable)
  and `docs/progress/MASTER.md` (run state) are two distinct, non-competing
  surfaces — the adapted governance template states it explicitly ("no
  competing truth sources" kept).
- **review-spd vs go-code-review**: two code reviews = forbidden duplication
  (charter §4). **Resolution**: review-spd's findings-first discipline (3
  targets, severities, 5 focuses, output format) is **merged into
  go-code-review** (a single review skill), not a parallel skill.
- **deep-discuss vs workflow-clarify**: clarify ≈ Phase 2; deep-discuss is an
  analysis discussion (not a spec) — complementary, no duplication.

## Constraints

- One writer per worktree; parallelize only read-only research (source
  analysis already done).
- Kit rules win over S.U.P.E.R in case of conflict (explicit boundary above).
- Language: English (fundamental rule D-2026-08-05-21).
- No GitHub in the adaptation (LOCAL_ONLY); no shipped agent files (mapping to
  Pi roles documented in the skill).
- Each new SKILL.md ≤ 500 lines, name == directory, English description ≤
  1024.
- The replaced chain is removed AFTER reference verification (router, Z8,
  docs); no residual dead reference.
- Full product gate mandatory (KitV2 is touched) + metaproject validators +
  fresh-context review.
- Three identical failures → stop and report.

## Done when

- Skill `spec-driven-dev` (SKILL.md + references/behavioral-rules.md,
  super-philosophy.md, adaptive-control.md, parallel-protocol.md,
  templates/{analysis,plan,progress,governance,archive}.md) shipped, EN,
  LOCAL_ONLY, S.U.P.E.R boundary encoded.
- Skill `deep-discuss` shipped (EN, adapted).
- `go-code-review` augmented with the findings-first discipline
  (references/reviewer-focus.md + 3 targets + size planning), without
  exceeding 500 lines.
- Prompts workflow-{clarify,plan,tasks,implement,verify} removed; router
  regenerated (prompt 8→3, skill 6→8); Z8 updated; product AGENTS.md updated
  (workflow = spec-driven-dev).
- `workflow-memory.md` adapted: "verify which memory files exist, Decisions.md
  may be missing from the Pi bootstrap" rule; rule added in `KitV2/AGENTS.md`
  (kit rule, NOT metaproject).
- Contract Z12 (`22-zone-spec-driven-dev.md`) + kit-governance README indexed;
  kit-audit: dimension + finding category + §5-E row; decisions
  D-2026-08-05-16…; Brief/Progress/Gotchas updated.
- Source analysis: `docs/research/2026-08-05-spec-driven-dev-analysis.md`.
- Full gate green (strict+normal validators, gofmt, vet, lint, test -race,
  gosec, govulncheck, probes) + metaproject validators + fresh-context review
  APPROVE before declaring completion.

## Steps / micro-tasks

### A. Analysis (done)

1. (done) Read-only clone + 57-file inventory.
2. (done) Read core SKILL.md + 6 references + deep-discuss + review-spd +
   agents + scripts + templates.
3. (done) Kit overlap mapping (workflow-* ≈ phases 2-5).
4. (done) User questions (4 answers: replace, EN, LOCAL_ONLY, Z12 without
   charter).
5. Write `docs/research/2026-08-05-spec-driven-dev-analysis.md` (evidence).

### B. spec-driven-dev skill (KitV2/.pi/skills/spec-driven-dev/)

6. `SKILL.md` — phases 0-6 adapted: Phase 0 intent; Phase 1 deep analysis (3
   docs, S.U.P.E.R health, kit search via search_kit_resources); Phase 2
   refinement (structured questions, composes go-implementation-plan); Phase 3
   decomposition (composes workflow-tasks logic → tasks + local batches);
   Phase 4 progress (MASTER.md + phase files, .pi/memory resolution +
   governance); Phase 5 execution (tiered local dispatch + tiered review,
   adaptive telemetry); Phase 6 archive. English description, English body,
   ≤ 500 lines.
2. `references/behavioral-rules.md` (EN) — 19 rules translated 1:1, adapted:
   questions via the Pi structured tool (ask_user_question), dual-write
   progress (Pi todo + MASTER.md), durable memory → .pi/memory.
3. `references/super-philosophy.md` (EN) — S.U.P.E.R + 10-point checklist,
   with the "Boundary with the kit rules" section (sourced rules win).
4. `references/adaptive-control.md` (EN) — telemetry (effort, SUPER delta,
   unplanned deps), drift_score, 20/40/60 thresholds, annotate/replan/rescope
   responses, LOCAL_ONLY storage (MASTER.md), session/post-task/post-batch
   activation.
5. `references/parallel-protocol.md` (EN) — tiered dispatch (Tier 0 default,
    Tier 1 one coder, Tier 2 lanes ≤ 4 disjoint) mapped onto the native Pi
    mechanism; tiered review L1 machine / L2 orchestrator / L3 independent
    reviewer (→ go-code-review skill); writer model (orchestrator = single
    writer of shared state).
6. `references/templates/analysis.md` (EN) — 3 templates (project-overview,
    module-inventory with S.U.P.E.R scores, risk-assessment with S.U.P.E.R
    health).
7. `references/templates/plan.md` (EN) — task-breakdown (phases, lanes, local
    delivery batches), dependency-graph (Mermaid), milestones.
8. `references/templates/progress.md` (EN) — MASTER.md + phase files +
    adaptive state + telemetry journal.
9. `references/templates/governance.md` (EN) — surface resolution
    (project AGENTS.md, .pi/memory), "verify which memory files exist" rule,
    no competing truth source.
10. `references/templates/archive.md` (EN) — archive docs/archives + index.
11. Static validation: complete frontmatter, ≤ 500 lines, resolved relative
    links, English description.

### C. Companion skills

17. `KitV2/.pi/skills/deep-discuss/SKILL.md` (EN) — 7 phases adapted (receive,
    problem audit, deep analysis, design, self-review, final review, optional
    execution); FR/EN triggers in description.
2. `KitV2/.pi/skills/go-code-review/` — review-spd discipline merge: new
    `references/reviewer-focus.md` (EN: 5 reviewer focuses, findings-first
    output contract, severity mapping); SKILL.md augmented (3 targets:
    uncommitted / commits / branch; size-based review planning; findings-first
    discipline) without exceeding 500 lines.

### D. Chain replacement (migration)

19. Verify references (router index.json, Z8, product AGENTS.md, historical
    metaproject docs = untouched).
2. `git rm` the 5 prompts workflow-{clarify,plan,tasks,implement,verify}.md.
3. Regenerate the router (`.agent/router/build_index.py`, expected prompt
    8→3, skill 6→8) + verify `--check`.
4. Update `KitV2/AGENTS.md`: Workflow section → spec-driven-dev (skill); add
    the kit memory rule (verify the actual .pi/memory files, Decisions.md may
    be missing; never assume the standard set).
5. Adapt `KitV2/.pi/prompts/workflow-memory.md`: real memory-file inventory +
    creation of missing files (incl. Decisions.md) + no metaproject-history
    copy.

### E. Metaproject governance (bounding)

24. `.agent/kit-governance/22-zone-spec-driven-dev.md` (Z12): mission, format
    (SKILL.md + references + templates), rules (LOCAL_ONLY, S.U.P.E.R
    boundary, archive mandatory, adaptive control mandatory, memory verified,
    composition of existing prompts/skills, no duplication), anti-patterns,
    C2 validation criteria (complete frontmatter, ≤ 500 lines, resolved
    references, 3 analysis templates present, no github-integration.md),
    open questions.
2. `.agent/kit-governance/README.md`: Z12 line in the index.
3. `.agent/kit-governance/17-zone-pi.md` (Z8): roles table updated
    (examples = spec-driven-dev, workflow-memory, checklist-*); rule
    "workflow = spec-driven-dev skill".
4. `.pi/prompts/kit-audit.md`: new C10 dimension "spec-driven-dev workflow"
    (skill + references inventory + S.U.P.E.R + adaptive control + archive +
    no GitHub leakage + no residual workflow-* prompts); named finding
    category; §5-E row.
5. `.pi/memory/Decisions.md`: D-2026-08-05-16 (chain replacement), -17
    (language — superseded by -21), -18 (LOCAL_ONLY), -19 (Z12 without
    charter), -20 (kit memory rule), -21 (English mandatory).
6. `.pi/memory/Brief.md`: Workflow section updated.
7. `.pi/memory/Progress.md`: pass task.
8. `.pi/memory/Gotchas.md`: lessons (Pi bootstrap without Decisions.md;
    S.U.P.E.R vs Go doctrine; review-spd → go-code-review merge).

### F. Validation

32. Full product gate (strict + normal validators, gofmt, vet, lint,
    test -race, gosec, govulncheck, probes) + metaproject validators.
2. Fresh-context review (read-only sub-agent, C0 §6.3) — integrate or settle.
3. Commit + final report (touched files, future-audit checklist, confidence).

## Pending actions (out of scope of this pass)

- No deferred KitV2 implementation (this pass is the implementation).
- Voluntarily out of scope: GitHub integration (LOCAL_ONLY decision);
  install-*/export-progress.py scripts (no multi-agent installation surface
  in the kit); shipped agent files (Pi mapping documented).

## Annexes

### Annex A — S.U.P.E.R boundary vs kit rules (text to encode in super-philosophy.md and Z12)

S.U.P.E.R is the workflow's health evaluation lens and a review checklist. It
is NOT a Go design doctrine replacing the kit's sourced rules. In case of
conflict, `rules/core/philosophy`, `rules/core/universal`, and the applicable
rules win. Compatible readings: S ≈ single responsibility (already kit), U ≈
consumer-owned dependencies and import direction (already kit), P ≈ consumer
interfaces + explicit serializable contracts (already kit), E ≈ environment-
driven config, zero hardcoded path (already kit), R ≈ replaceability without
side effects (already kit). What S.U.P.E.R ADDS: per-principle scoring
(🟢🟡🔴) in the analysis, the 10-point review checklist, and violation hotspots
as plan priorities.

### Annex B — spec-driven agent roles mapped to the Pi harness

| Spec-driven role | Pi / kit role | Notes |
| --- | --- | --- |
| project-analyzer | scout / researcher (sub-agent) | focus-based analysis, structured output |
| task-architect | planner (sub-agent) | decomposition + batches |
| task-executor | worker (sub-agent) | executes a batch/lane, never touches shared state |
| code-reviewer | reviewer (sub-agent) + go-code-review skill | verdict APPROVED/FIXED/ESCALATE, `fix:` commits on the lane branch |

Agents are not shipped as files: the skill documents the mapping; without Pi
sub-agents, sequential execution (Tier 0).
