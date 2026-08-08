# Plan — `workspace-init`: kernel-first project foundation (Z14)

**Date:** 2026-08-08
**Research:** `docs/research/2026-08-08-workspace-init-kernel-first.md`
**Status:** pending user arbitration on 4 open questions (§7), then
implementation + full gate.

## Goal

A new protocol, invoked **before any code** in a consumer project, that
interviews the user, frames the architecture as **one kernel + peripheral
modules** (Microkernel/Plugin architecture, Mark Richards), and materializes
the result in a `workspace/` folder referenced from the project's
`AGENTS.md` — so everything written afterwards (including
`spec-driven-dev`) starts from a stable foundation. The protocol sits
**before** spec-driven-dev Phase 0; it builds nothing.

## Context

- The kit already covers module boundaries, ports/adapters, `internal/`,
  constructor injection, testing seams/fakes/black-box/table-driven, the
  doc-comment contract, and resource routing (research §7). The protocol
  **points to** these; it adds only the kernel/modules *decision*, its
  capture, and the SDK production trigger.
- The product shape is a **workflow skill** (`.pi/skills/`, category
  `workflow`) per Z8 (procedures = skills; checklists = prompts) and the
  `setup-matt-pocock-skills` precedent (one-shot day-0 init).
- `workspace/` and its documents are **consumer project artifacts**, never
  shipped by the kit (like `structure.md` in Layer 5.1: produced, not
  prescribed). The kit ships only the *skill* + *document templates*
  (Z5: templates of *documents*, same status as
  `spec-driven-dev/references/templates/` — not code templates).

## Decisions to be taken (§7 asks the user)

1. Skill name: `workspace-init` (recommended) vs alternative.
2. Form factor: skill `.pi/skills/` (recommended) vs prompt `.pi/prompts/`.
3. Mandatory vs strongly recommended for new projects.
4. How spec-driven-dev Phase 0 reads `workspace/`: amend the "Before You
   Begin" continuity check (recommended, minimal) vs workflow-memory-only.

## 1. Zone contract Z14

New file `.agent/kit-governance/24-zone-workspace-init.md`, modeled exactly
on `22-zone-spec-driven-dev.md` (mission, format, rules, anti-patterns,
validation criteria C2, open questions), plus a row in
`.agent/kit-governance/README.md`.

## 2. Product tree (to create)

```text
KitV2/.pi/skills/workspace-init/
├── SKILL.md                    # category: workflow; ≤ 500 lines; English
└── references/
    ├── interview-framework.md  # adapted grilling: design tree over the
    │                           # kernel/modules decision; frontier rounds;
    │                           # facts vs decisions split
    └── templates/              # document templates (NOT code; Z5 §2 n/a —
                                # same status as spec-driven-dev templates)
        ├── constitution.md     # CONSTITUTION.md gabarit (adapted from
        │                       # spec-kit constitution-template.md)
        ├── architecture.md     # ARCHITECTURE.md gabarit (kernel/modules/
        │                       # SDK plan)
        └── domain.md           # DOMAIN.md gabarit (optional glossary,
                                # grill-with-docs CONTEXT.md pattern)
```

## 3. Skill phases (SKILL.md)

- **Phase 0 — Initial framing**: open questions (nature, users,
  constraints), no agent-imposed jargon.
- **Phase 1 — Kit scout**: a sub-agent (tiered dispatch per spec-driven-dev
  `references/parallel-protocol.md` — reuse, never a second mechanism)
  inventories relevant templates/recipes/catalogs/patterns via
  `search_kit_resources` + a targeted `knowledge/INDEX.md` read.
- **Phase 2 — External research**: web research sub-agents only where the
  user's framing + the kit catalog are insufficient (uncommon stack,
  platform constraint, pattern absent from the kit).
- **Phase 3 — Grilled interview** (adapted `grilling`): frontier rounds
  converging explicitly on (a) kernel/modules boundary for THIS project,
  (b) exact stack, (c) non-negotiable writing rules, (d) testing policy.
  Every question justified by what is still missing to decide (a)-(d).
  Facts looked up, never asked; decisions asked, never assumed.
- **Phase 4 — Restitution + write**: propose the synthesis, get explicit
  validation, then write `workspace/` (CONSTITUTION.md, ARCHITECTURE.md,
  optional DOMAIN.md, decisions/, research/) and insert/update the
  "Project Foundation" section in the consumer's AGENTS.md (marker
  mechanics §5). Idempotence: refuse to re-run when `workspace/` exists
  unless the user explicitly requests a revision.

## 4. Consumer `workspace/` layout (produced by the session)

```text
workspace/
├── CONSTITUTION.md   # mission, kernel-first mandate, non-negotiables
│                     # (test-first, documented SDK, no module→module direct
│                     # dependency), stack decisions — spec-kit pattern,
│                     # adapted: also an architecture decision + SDK plan
├── ARCHITECTURE.md   # kernel/modules boundary for this project; one-line
│                     # contract per module; SDK plan (packages, doc-comment
│                     # style; points to rules/registry/doc-comments)
├── DOMAIN.md         # shared vocabulary (optional, trivial domains skip)
├── decisions/        # D-YYYY-MM-DD-NN.md — same format as
│                     # .pi/memory/Decisions.md
└── research/         # dated, sourced notes from scout + web sub-agents
```

## 5. AGENTS.md placeholder mechanics (consumer side)

- `KitV2/AGENTS.md` gains a short **"Project Foundation"** section: pointer
  by default ("not initialized — run `workspace-init`"), describes the
  `workspace/` convention. Content is generic (kit-level), never
  project-specific.
- The init session writes a per-project "Project Foundation" section into
  the consumer's `AGENTS.md` with an identifiable marker
  (`<!-- workspace-init sha256: <hash of workspace/CONSTITUTION.md +
  ARCHITECTURE.md> -->`), mirroring the Z13 §4 mechanics **in reverse**:
  content is project-owned (written from the local session, never synced
  from the kit), never loses existing content, never touches projects that
  are not initialized.
- `spec-driven-dev` Phase 0 reads the workspace docs when present (see §6).

## 6. Articulation with spec-driven-dev Phase 0

Minimal amendment (composition, no duplication): in the "Before You Begin"
continuity check (which already inventories AGENTS.md + `.pi/memory/`),
add `workspace/` to the surfaces inventoried — if
`workspace/CONSTITUTION.md` + `ARCHITECTURE.md` exist, read them before
Phase 0 and make Phase 0's direction consistent with them. One bullet +
one line in Phase 0; no new logic duplicated.

## 7. Open questions (asked to the user before implementation)

1. **Name** — `workspace-init` (recommended) vs `project-foundation` vs
   another name.
2. **Form factor** — skill `.pi/skills/workspace-init/SKILL.md`
   (recommended: durable multi-phase procedure + references/templates;
   Z8 role boundary; setup-* precedent) vs prompt `.pi/prompts/workspace-init.md`
   (manual orchestrator, no sub-references).
3. **Mandatory vs recommended** — protocol blocking for new projects (no
   feature work until `workspace/` exists; requires a named control for the
   MANDATORY lexeme per Z8 rule 6 / charter §16.1.4) vs strongly recommended
   (the skill and AGENTS.md suggest it; a skipped init is recorded, not
   blocking).
4. **Phase 0 forcing** — amend spec-driven-dev "Before You Begin" to read
   `workspace/` (recommended) vs workflow-memory reminder only.

## 8. Implementation checklist

1. Z14 contract + governance README row.
2. Skill SKILL.md + `references/interview-framework.md` + 3 templates.
3. `KitV2/AGENTS.md` "Project Foundation" section (generic pointer).
4. spec-driven-dev "Before You Begin" amendment (+ last-verified bump).
5. Router: `python3 .agent/router/build_index.py` + optional scenario for
   `workspace-init` (realistic intent, able to fail).
6. Full gate: validate-instructions, validate-cognitive, validate-kitv2,
   router checks, gofmt/vet/lint/tests, probes. Evidence →
   `docs/evidence/2026-08-08/workspace-init/`.
7. `docs/plans/` = this file; Decisions D-2026-08-08-NN for: zone name,
   form factor, workspace/ layout, AGENTS.md marker mechanics, Phase 0
   articulation.

## 9. Risks / notes

- The skill itself must not become a second interview system: it adapts
  `grilling` (cited), it does not invent a new interview vocabulary.
- The templates are document gabarits, NOT Z5 code templates — the Z14
  contract must state this explicitly to avoid the MIT-fork policy being
  (wrongly) applied to them.
- `MANDATORY`/`always`/`never` lexemes inside the skill must name a control
  or be recorded in `.agent/instructions.md` enforcement gaps
  (validate-instructions.py gate).
- Prose id references inside the skill must resolve (validate-cognitive.py
  C12) — only reference existing indexed ids.
