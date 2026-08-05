# Z12 — Zone `spec-driven-dev` (large-scale transformation workflow)

- **Metaproject Contract** — governs `KitV2/.pi/skills/spec-driven-dev/` and
  `KitV2/.pi/skills/deep-discuss/` (workflow skills), plus the findings-first
  review discipline merged into `KitV2/.pi/skills/go-code-review/`.
- **Origin**: integration of the logic of the MIT repository
  `zhu1090093659/spec_driven_develop` (v1.15.0) adapted to the kit and the Pi
  harness — decisions D-2026-08-05-16…21, analysis
  `docs/research/2026-08-05-spec-driven-dev-analysis.md`, plan
  `docs/plans/2026-08-05-spec-driven-dev-integration.md`.

## 1. Mission

The kit's reference workflow for **large-scale transformations** (rewrite,
migration, overhaul, whole-project refactor): a seven-phase pipeline (0-6) —
intent capture, deep analysis with S.U.P.E.R health, grounded refinement,
decomposition with delivery batches, cross-session tracking (MASTER.md),
confirmed execution with adaptive control, archive. It replaces the former
`workflow-clarify → plan → tasks → implement → verify` prompt chain (removed
2026-08-05) and composes the remaining kit resources (`workflow-memory`,
`go-*`, `kit-resource-routing`, `go-code-review`) by cross-references — never
by duplication.

## 2. Format

```text
KitV2/.pi/skills/spec-driven-dev/
├── SKILL.md                    # phases 0-6, complete frontmatter (category: workflow)
└── references/
    ├── behavioral-rules.md     # 19 non-negotiable rules
    ├── super-philosophy.md     # S.U.P.E.R + boundary with the kit rules
    ├── adaptive-control.md     # telemetry, drift, thresholds, responses
    ├── parallel-protocol.md    # tiered dispatch/review, writer model
    └── templates/              # analysis, plan, progress, governance, archive
```

`KitV2/.pi/skills/deep-discuss/SKILL.md`: structured 7-phase discussion.

## 3. Rules

1. **Local mode only**: no GitHub (Issues/Milestones/PRs/gh CLI) — user
   decision D-2026-08-05-18. Tracking lives in `docs/progress/` (MASTER.md +
   phase files); delivery batches are local integration/validation units,
   never PRs.
2. **S.U.P.E.R boundary**: S.U.P.E.R is a health evaluation lens and a review
   checklist, not a Go design doctrine. In case of conflict, the kit's sourced
   rules win (`rules/core/philosophy`, `rules/core/universal`) — encoded in
   `references/super-philosophy.md` § "Boundary with the kit rules".
3. **Adaptive control mandatory**: post-task telemetry (effort, S.U.P.E.R
   delta, unplanned dependencies), cumulative `drift_score`, 20/40/60 %
   thresholds, automatic annotate/replan/rescope responses. The adaptive
   state persists in MASTER.md (never only in conversation memory).
4. **Archive mandatory**: Phase 6 always executed; all artifacts under
   `docs/archives/<project>/` with an index.
5. **Memory rule** (kit, NOT metaproject): every agent using the kit verifies
   which `.pi/memory/` files actually exist — the Pi bootstrap does not create
   `Decisions.md` by default. Never assume the standard set; create the
   missing files without copying external history. Encoded in
   `KitV2/AGENTS.md` and `workflow-memory.md`.
6. **Composition, not duplication**: the skill composes the existing
   prompts/skills (`workflow-memory`, `go-implementation-plan`,
   `go-code-review`, `go-testing-verification`, `kit-resource-routing`); it
   does not introduce a second workflow answering the same question.
7. **Language**: bodies in English (fundamental rule D-2026-08-05-21,
   superseding D-2026-08-05-17); frontmatter `description` in English (Pi
   discoverability).
8. **Sub-agents = economic decision**: tiered dispatch (Tier 0 default,
   Tier 1 one coder, Tier 2 lanes ≤ 4 disjoint) mapped onto the native Pi
   mechanism; without sub-agents, sequential execution. The spec-driven roles
   (project-analyzer, task-architect, task-executor, code-reviewer) are
   documented as a mapping, never shipped as files.

## 4. Anti-patterns

- Spec-driven skill without S.U.P.E.R, without adaptive control, or without
  archive.
- Reintroducing GitHub/PR into the local workflow.
- Duplicating the former workflow-* chain (prompts removed; do not recreate
  them).
- S.U.P.E.R imposed as a Go design doctrine against the sourced rules.
- `Decisions.md` assumed present without verification.
- Prompt or skill that re-explains a canonical reference (single-sourcing).

## 5. Validation criteria (C2 / audit)

- [ ] Complete frontmatter (name == directory, category: workflow, English
      description ≤ 1024, tags, last-verified) for spec-driven-dev and
      deep-discuss.
- [ ] SKILL.md ≤ 500 lines; `references/**` present and relative links
      resolved.
- [ ] The three Phase-1 document templates (project-overview,
      module-inventory, risk-assessment) are covered by
      `references/templates/analysis.md`.
- [ ] Absence of `github-integration.md` or gh/PR references in the skill.
- [ ] `go-code-review` carries the findings-first discipline (targets, focus,
      format) without exceeding 500 lines.
- [ ] Router indexed (skills: spec-driven-dev, deep-discuss) and
      `--check` green.
- [ ] No residual `workflow-{clarify,plan,tasks,implement,verify}` prompt
      (verified by the audit, named finding category).

## 6. Open questions

- GitHub integration (GITHUB_FULL/STANDARD) remains excluded by user decision;
  re-evaluate only if a consumer explicitly requests it.
- The source repository's scripts (export-progress.py, install-*.sh,
  review-context.py) are not ported: no multi-agent installation surface and
  no external export need in the kit. Re-evaluate with the future `gak` CLI.
