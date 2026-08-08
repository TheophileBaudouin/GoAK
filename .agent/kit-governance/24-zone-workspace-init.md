# Z14 — Zone `workspace-init` (kernel-first project foundation protocol)

- **Metaproject Contract** — governs
  `KitV2/.pi/skills/workspace-init/` (workflow skill) and the project
  foundation convention it produces (`workspace/` + the "Project
  Foundation" section of a consumer project's `AGENTS.md`).
- **Origin**: owner directive 2026-08-08 — a protocol invoked **before any
  code** in a consumer project that interviews the user, frames the
  architecture as one kernel + peripheral modules, and materializes the
  result in `workspace/`. Research
  `docs/research/2026-08-08-workspace-init-kernel-first.md`, plan
  `docs/plans/2026-08-08-workspace-init-kernel-first.md`, decisions
  D-2026-08-08-06…10.

## 1. Mission

The kit's day-0 protocol for consumer projects: one session, run once,
**before any feature code and before `spec-driven-dev` Phase 0**, that (a)
interviews the user toward the **kernel/modules boundary** of this project
(Microkernel / Plugin architecture — cite Mark Richards, *Fundamentals of
Software Architecture*, never a home-made definition), (b) pins the stack,
the non-negotiable writing rules, and the testing policy, and (c)
materializes the result in a `workspace/` folder referenced from the
project's `AGENTS.md`. Everything written afterwards — including every
`spec-driven-dev` run — starts from that foundation instead of re-deriving
it per feature. The protocol **builds nothing**: it produces the decision
and its capture, never code, never a project scaffold.

## 2. Format

```text
KitV2/.pi/skills/workspace-init/
├── SKILL.md                    # phases 0-4, complete frontmatter
│                               # (category: workflow), English, ≤ 500 lines
└── references/
    ├── interview-framework.md  # adapted grilling: design tree over the
    │                           # kernel/modules decision; frontier rounds;
    │                           # facts vs decisions split
    └── templates/              # DOCUMENT templates (gabarits) — NOT code
        ├── constitution.md     # CONSTITUTION.md gabarit (adapted from the
        │                       # spec-kit constitution template)
        ├── architecture.md     # ARCHITECTURE.md gabarit (kernel/modules/SDK
        │                       # plan)
        └── domain.md           # DOMAIN.md gabarit (optional glossary)
```

Consumer-side output produced by the session (never shipped by the kit):

```text
workspace/
├── CONSTITUTION.md   # mission, kernel-first mandate, non-negotiables,
│                     # stack decisions — spec-kit constitution pattern,
│                     # adapted: carries an architecture decision too
├── ARCHITECTURE.md   # kernel/modules boundary, one-line contract per
│                     # module, SDK plan (packages + doc-comment style)
├── DOMAIN.md         # shared vocabulary (optional, trivial domains skip)
├── decisions/        # D-YYYY-MM-DD-NN.md — same format as
│                     # .pi/memory/Decisions.md
└── research/         # dated, sourced notes (kit scout + web research)
```

## 3. Rules

1. **One-shot, day 0, idempotent**: invoked once, before any feature work
   and before `spec-driven-dev` Phase 0. The skill refuses to re-run when
   `workspace/` already exists, unless the user explicitly requests a
   revision (which preserves the existing `decisions/` and `research/`
   history).
2. **Kernel-first mandate**: kernel = minimal core — shared
   contracts/types, bootstrap/lifecycle, cross-cutting concerns (config,
   logging, errors, optionally a command/event bus or an injection point) —
   **zero feature logic**. Modules = peripheral components that depend only
   on the SDK exposed by the kernel, never directly on each other (except
   via a contract carried by the kernel). Pattern name and definition cite
   Mark Richards (Microkernel/Plugin architecture); never a home-made
   definition. Align with the kit's cataloged patterns
   (`pattern:architecture:modular-monolith`,
   `pattern:architecture:ports-adapters`,
   `pattern:go:internal-packages`) rather than new vocabulary.
3. **SDK = deep module interface**: the SDK is the kernel's public
   interface, deliberately small, over a kernel doing much work behind it
   (John Ousterhout, *A Philosophy of Software Design* — deep modules;
   cite, never rephrase as doctrine). SDK documentation = doc-commented
   exported API + executable examples; the skill **points to**
   `rules/registry/doc-comments/SKILL.md`, it does not re-teach the rule.
   The SDK and its documentation grow in the same commit.
4. **Test-first, kernel and modules**: every module carries a black-box
   test suite at its public API, isolated from other modules — a regression
   in one module never fails another's tests. The skill points to
   `rules/registry/testing/SKILL.md` and the testing patterns
   (`pattern:testing:blackbox-package-tests`,
   `pattern:testing:seam-injection`, `pattern:testing:fakes-over-mocks`,
   `pattern:testing:table-driven`); it does not re-explain them.
5. **Composition, not duplication**: everything the kit already covers
   (module boundaries, injection, testing, doc-comments, routing) is
   referenced by tagged id or rule pointer. The protocol adds only the
   kernel-vs-modules **decision**, its **capture at project level**
   (`workspace/`), and the **trigger** for SDK production and
   documentation.
6. **Interview adapted from `grilling`** (mattpocock/skills — adapted, never
   copied verbatim): the session works a **design tree** in **rounds**; each
   round asks the whole **frontier** (decisions whose prerequisites are
   settled), numbered with a recommended answer; **facts are the agent's
   job** (looked up or dispatched), **decisions are the user's**; the
   session ends when the frontier is empty AND the user confirms shared
   understanding — the agent never acts before that confirmation and never
   answers its own questions. The interview must converge explicitly on (a)
   the kernel/modules boundary for this project, (b) the exact stack, (c)
   the non-negotiable writing rules, (d) the testing policy. A generic or
   unjustified question is a failure of the interview: each question must
   be motivated by what is still missing to decide (a)–(d).
7. **Kit scout + external research reuse the spec-driven-dev tiered
   dispatch** (Tier 0/1/2, `references/parallel-protocol.md`) — never a
   second dispatch mechanism. Phase 1 scoutes the kit via
   `search_kit_resources` + a targeted `knowledge/INDEX.md` read; Phase 2
   runs web research only where the user's framing or the kit catalog is
   insufficient. Research notes are dated and sourced into `workspace/research/`.
8. **Restitution before write**: the agent proposes the synthesis, the user
   explicitly validates it, then the session writes `workspace/` and the
   consumer `AGENTS.md` section. Never write before explicit validation.
9. **`AGENTS.md` mechanics** — two distinct markers, one per surface:
   - **Product pointer** (`KitV2/AGENTS.md`): the generic **"Project
     Foundation"** pointer section is delimited by explicit markers
     `<!-- workspace-init section: begin -->` … `<!-- workspace-init
     section: end -->` (N1 convention: every zone merging content into
     AGENTS.md delimits its section). The section is static kit content;
     `validate-kitv2.py` `check_workspace_init_placeholder()` verifies
     presence of both markers and the section title — a missing or altered
     section fails the gate.
   - **Consumer capture** (written by the init session into the consumer
     project's `AGENTS.md`): the per-project section under an identifiable
     marker (`<!-- workspace-init sha256: <hash of
     workspace/CONSTITUTION.md + ARCHITECTURE.md> -->`, recomputed when
     the workspace docs change). Content is project-owned, written from
     the local session, **never synced from the kit**; existing content is
     never lost; projects that are not initialized get no noise.
10. **`spec-driven-dev` articulation**: the skill's "Before You Begin"
    continuity check inventories `workspace/` alongside `AGENTS.md` and
    `.pi/memory/`; when `workspace/CONSTITUTION.md` + `ARCHITECTURE.md`
    exist, Phase 0 reads them and its direction must be consistent with
    them. One bullet + one line — composition, no duplicated logic.
11. **Strongly recommended, not blocking** (owner arbitration 2026-08-08):
    the skill and the AGENTS.md section suggest init for a new project; a
    skipped init is recorded in project memory, never silently assumed and
    never a hard gate. No `MANDATORY`/`always`/`never` lexeme on this
    subject without a named control.
12. **Templates are document gabarits, not Z5 code templates**: the
    `references/templates/*.md` files are document templates (same status
    as `spec-driven-dev/references/templates/`); the Z5 MIT-fork policy
    does not apply to them, and they must not be presented as project
    scaffolds.
13. **English only** (fundamental rule D-2026-08-05-21), including the
    frontmatter `description` (Pi discoverability); no metaproject path
    markers in shipped files (KVA-102 guard).
14. **Routing is the activation surface**: the skill is indexed by the
    router (`search_kit_resources`), and its frontmatter description is the
    routing contract — realistic activation terms ("project foundation",
    "new project", "kernel modules", "before feature work"), one concern.

## 4. Anti-patterns

- A second interview system: the session must adapt `grilling` (cited
  source), never invent a parallel interview vocabulary.
- A second dispatch mechanism: scout and research reuse the spec-driven-dev
  tiered dispatch; do not create a new sub-agent protocol.
- Re-explaining a kit rule/pattern (doc-comments, testing, injection,
  boundaries) — point by id, never re-teach.
- Shipping `workspace/` content or a consumer `AGENTS.md` section from the
  kit: the artifacts are produced at runtime in the consumer project, like
  `structure.md` (Layer 5.1) — never prescribed templates in the product.
- Treating the document gabarits as Z5 code templates (MIT-fork policy
  wrongly applied) or as project scaffolds.
- Re-running init over an existing `workspace/` without an explicit
  revision request (history loss).
- Writing to the consumer `AGENTS.md` without the marker, or overwriting
  existing content; touching projects that are not initialized.
- Generic interview questions (a failure of rule 6); the agent answering
  its own decisions or acting before explicit validation (grilling
  violations).
- A kernel that contains feature logic, or modules that depend directly on
  each other (microkernel violation).
- Making the protocol a hard blocking gate (contradicts rule 11).

## 5. Validation criteria (C2 / audit)

- [ ] Complete frontmatter (name == directory, category: workflow, English
      description ≤ 1024, tags, last-verified) for `workspace-init`.
- [ ] SKILL.md ≤ 500 lines; `references/**` present; relative links
      resolve; no metaproject path markers; English-only.
- [ ] Router indexed (skill: workspace-init) and `--check` green; the
      routing-quality scenario for workspace-init passes under the real
      scoring and can fail (Z11 admission bar).
- [ ] `validate-instructions.py` green: no unenforced MANDATORY lexeme
      (the protocol is "strongly recommended" — no blocking mandate).
- [ ] `validate-cognitive.py` green: every prose id reference resolves
      (C12), no unresolved `pattern:`/`rule:`/`knowledge:` tokens.
- [ ] No `workspace/`, `CONSTITUTION.md`, or `ARCHITECTURE.md` content
      shipped in `KitV2/` (produced at runtime only).
- [ ] `spec-driven-dev` "Before You Begin" inventories `workspace/` (one
      bullet, no duplicated logic) and `last-verified` is bumped.
- [ ] `KitV2/AGENTS.md` carries the generic "Project Foundation" pointer
      section, delimited by the `workspace-init section: begin/end`
      markers; `check_workspace_init_placeholder` is present in the
      validator and green (a missing or altered section fails the gate).
- [ ] The consumer-side marker mechanics are documented in the skill
      (marker format, no-content-loss rule, no-noise rule) and verified by
      review (no validator can check a runtime artifact).

## 6. Open questions

- Whether the future `gak` CLI should expose the init as `gak init` —
  deferred until the CLI exists.
- Whether a non-spec-driven consumer workflow should also be pointed to
  `workspace/` (today only the spec-driven-dev continuity check reads it;
  `workflow-memory` may carry a reminder).
- Whether the interview framework deserves its own scenario in
  `scenarios.json` beyond the activation scenario — revisit when the
  routing corpus grows.
