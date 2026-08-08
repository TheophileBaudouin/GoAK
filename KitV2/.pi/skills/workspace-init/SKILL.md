---
name: workspace-init
category: workflow
tags: [project-foundation, kernel, modules, architecture, interview, day-0, sdk, microkernel, workspace]
last-verified: 2026-08-08
description: "Day-0 project foundation protocol for a new or pre-feature consumer project: interview the user (adapted grilling), decide the kernel/modules boundary (Microkernel/Plugin architecture), and pin stack, non-negotiables, and testing policy, then write workspace/ (CONSTITUTION.md, ARCHITECTURE.md, optional DOMAIN.md, decisions/, research/) plus the project's AGENTS.md 'Project Foundation' section. Use once at the very start of a project, before any feature code and before spec-driven-dev Phase 0. Not for projects that already have a workspace/ (revision only on explicit request). Builds nothing — produces the decision and its capture only."
---

# Workspace init — kernel-first project foundation

You are executing the **day-0 foundation protocol** for a consumer Go
project: a single session that frames the architecture as **one kernel +
peripheral modules** and captures the decision in `workspace/`, so every
later step (including every `spec-driven-dev` run) starts from a stable
foundation instead of re-deriving it per feature.

This protocol **builds nothing**: no code, no project scaffold, no feature.
It produces the decision and its capture. It runs **before any feature
code** and **before `spec-driven-dev` Phase 0**.

**Interview discipline**: `references/interview-framework.md` — read and
follow it in Phase 3; it is the non-negotiable interview contract.

## Configuration

| Item | Default | Purpose |
| :--- | :--- | :--- |
| Foundation output | `workspace/` | CONSTITUTION.md, ARCHITECTURE.md, optional DOMAIN.md, decisions/, research/ |
| AGENTS.md section | `## Project Foundation` | Consumer-side pointer to workspace/ (marker mechanics §8) |
| Decisions format | `decisions/D-YYYY-MM-DD-NN.md` | Same format as `.pi/memory/Decisions.md` |
| Research notes | `workspace/research/` | Dated, sourced notes (kit scout + web research) |
| Kit discovery | `search_kit_resources` | Phase 1 only — never a manual kit tree scan |

**Canonical references** (each topic has exactly one home — cite it, never
re-explain it):

| Reference | Owns |
| :--- | :--- |
| `references/interview-framework.md` | The design-tree interview, frontier rounds, facts-vs-decisions split |
| `references/templates/` | Document gabarits for CONSTITUTION.md, ARCHITECTURE.md, DOMAIN.md (consumer output) |
| `rules/registry/doc-comments/SKILL.md` | The doc-comment contract the SDK must follow |
| `rules/registry/testing/SKILL.md` | The testing rules every module's suite must follow |
| `spec-driven-dev` skill | The downstream workflow; reads workspace/ via its continuity check |
| `workflow-memory` prompt | Memory surface conventions for the consumer project |

## Before you begin

1. **Idempotence check**: if `workspace/` already exists at the consumer
   project root, the protocol is done. Do NOT re-run — unless the user
   explicitly asks for a **revision** (which preserves `decisions/` and
   `research/` history and amends CONSTITUTION.md/ARCHITECTURE.md with a
   version bump and an amendment entry in `decisions/`).
2. **Surface inventory** (same discipline as spec-driven-dev): read the
   consumer's `AGENTS.md` (including any existing `## Project Foundation`
   section), and verify which `.pi/memory/` files exist (the native memory
   extension auto-bootstraps the five files when missing — create any
   missing one without copying external history).
3. **Existing constraints**: note any user-provided or repository-level
   constraints (license, toolchain, existing README intent) before the
   interview — they become facts, not questions.

---

## Phase 0: Initial framing

Open, jargon-free questions to locate the project. Do NOT use kit or
architecture vocabulary (no "kernel", "module", "SDK" yet). Ask only what
is needed to know the territory:

- What is the project? What problem does it solve, for whom?
- Who are the users / operators, and what are the hard constraints
  (platform, deployment, performance, team size, timeline)?
- What already exists (repository, docs, prior decisions), if anything?

**Output**: a one-paragraph project statement in plain language. If the
user volunteers constraints, record them as facts.

## Phase 1: Kit scout

A sub-agent (tiered dispatch per `spec-driven-dev` `references/parallel-protocol.md` —
reuse, never a second mechanism) inventories what the kit already offers
for this type of project:

1. Call `search_kit_resources` with the project's concrete terms (stack,
   domain, shape) — never a manual tree scan.
2. Read the relevant `knowledge/INDEX.md` sections and the routed
   resources (templates, recipes, catalogs, patterns).
3. Record findings as **dated, sourced notes** in `workspace/research/`
   (pending Phase 4 write) — what the kit covers, what it does not.

**Output**: a kit-coverage note: reusable pieces (by id/path) and the real
gaps the interview must resolve.

## Phase 2: External research

Only where the user's framing or the kit catalog is insufficient — uncommon
stack, platform constraint, pattern absent from the kit:

1. Delegate web research to a researcher sub-agent (same tiered dispatch),
   primary sources only, URLs verified.
2. Keep research bounded: one question per sub-agent, dated and sourced
   notes in `workspace/research/`.

**Output**: focused, sourced research notes. If the kit + user framing
suffices, this phase is empty — do not manufacture research.

## Phase 3: Grilled interview

Run the interview exactly as specified in
`references/interview-framework.md`. The design tree converges on four
decision clusters — everything else hangs off them:

1. **Kernel/modules boundary** (the core decision): what is cross-cutting
   and belongs in the kernel (shared contracts/types, bootstrap/lifecycle,
   config, logging, errors, optional command/event bus or injection point);
   what is a feature and becomes a module. One-line contract per module.
2. **Exact stack**: language level, libraries, persistence, transports,
   tooling — pinned by name/version, justified against kit recipes and
   catalogs.
3. **Non-negotiable writing rules**: error handling, naming, boundaries,
   zero-value design, doc-comments — point to the kit rules; record only
   what is project-specific on top.
4. **Testing policy**: test-first by default; every module black-box at its
   public API, isolated from other modules; which test layers protect what.

Facts are looked up (files, kit, web), never asked. Decisions are the
user's, each put to them with a recommendation. A question must be
motivated by what is still missing to decide (1)–(4); a generic question is
a failure of this phase.

**Output**: the settled decision tree (boundary, stack, rules, testing) —
recorded in the conversation and, once validated, in `workspace/`.

## Phase 4: Restitution & write

1. **Restitution**: present the full synthesis — the kernel/modules
   boundary with the one-line module contracts, the pinned stack, the
   non-negotiables, the testing policy, and the proposed `workspace/`
   layout.
2. **Explicit validation**: ask the user to confirm the synthesis (the
   platform's structured question tool). The frontier is empty only when
   the user says the understanding is shared. **Never write before this
   confirmation.**
3. **Write**:
   - `workspace/CONSTITUTION.md` from `references/templates/constitution.md`
     — mission, kernel-first mandate, non-negotiables, stack decisions.
   - `workspace/ARCHITECTURE.md` from `references/templates/architecture.md`
     — the boundary, per-module contracts, the SDK plan.
   - `workspace/DOMAIN.md` from `references/templates/domain.md` — only if
     the interview surfaced non-trivial shared vocabulary; trivial domains
     skip it (no placeholder file).
   - `workspace/decisions/D-<date>-NN.md` — every structuring arbitration
     of this session (zone name, boundary cases, stack pins), same format
     as `.pi/memory/Decisions.md`.
   - `workspace/research/` — the dated, sourced scout + research notes.
   - The `## Project Foundation` section in the consumer's `AGENTS.md`
     (§8 mechanics).
4. **Memory**: record the initialization in the consumer's `.pi/memory/`
     (Progress: foundation initialized; Gotchas: any trap found).

**Output**: `workspace/` + the consumer AGENTS.md section, explicitly
validated.

---

## The kernel-first mandate (what CONSTITUTION.md must say)

- **Kernel** = the minimal core: shared contracts/types, bootstrap and
  lifecycle, cross-cutting concerns (config, logging, errors, optionally a
  command/event bus or an injection point). **Zero feature logic.**
- **Modules** = peripheral components that depend only on the SDK exposed
  by the kernel — never directly on each other (except via a contract
  carried by the kernel). Align vocabulary with
  `pattern:architecture:modular-monolith`,
  `pattern:architecture:ports-adapters`, `pattern:go:internal-packages`;
  wiring via `pattern:go:constructor-injection`.
- **SDK** = the kernel's public interface: deliberately small (deep module —
  John Ousterhout, *A Philosophy of Software Design*), documented as
  doc-commented exported API + executable examples per
  `rules/registry/doc-comments/SKILL.md`. The SDK and its documentation
  grow in the same commit.
- **Test-first, kernel and modules**: every module tested black-box at its
  public API, isolated from the others (`pattern:testing:blackbox-package-tests`,
  `pattern:testing:seam-injection`, `pattern:testing:fakes-over-mocks`,
  `pattern:testing:table-driven`); a regression in one module never fails
  another's tests.

The pattern name and definition cite Mark Richards, *Fundamentals of
Software Architecture* (Microkernel/Plugin architecture) — never a
home-made definition.

## The AGENTS.md section mechanics

The session writes (or updates) a `## Project Foundation` section in the
consumer project's `AGENTS.md`:

```markdown
## Project Foundation

<!-- workspace-init sha256: <sha256 of workspace/CONSTITUTION.md + workspace/ARCHITECTURE.md> -->

Before any feature work, read `workspace/CONSTITUTION.md` and
`workspace/ARCHITECTURE.md`. This project is framed as one kernel + modules
(kernel-first mandate); modules depend only on the kernel SDK, never on
each other. Stack, non-negotiables, and testing policy live in the
workspace docs — do not re-derive them per feature.
```

Rules (same spirit as the kit's UI-section merge, reversed flow):

- The marker is an identifiable placeholder; when the workspace docs
  change, the session recomputes the sha256 and updates the marker.
- **Never lose existing content**: insert the section at the end (or after
  the memory section), never rewrite the file.
- **No noise**: projects that are not initialized get no section. The kit's
  own `AGENTS.md` carries only the generic pointer ("Project Foundation —
  not initialized; run `workspace-init`").
- The section content is **project-owned**: written from this session,
  never synced from the kit.

## Handoff to spec-driven-dev

For the next large-scale transformation in this project, `spec-driven-dev`
reads `workspace/CONSTITUTION.md` + `ARCHITECTURE.md` in its "Before You
Begin" continuity check and makes Phase 0 consistent with them. Ordinary
feature work: read the workspace docs before planning — the AGENTS.md
section above already points there.

## Strongly recommended, not blocking

Initializing the foundation is strongly recommended for any new consumer
project, never a hard gate: if the user declines, record the decision in
`.pi/memory/` and proceed — the kit does not block feature work on an
uninitialized project.

## Anti-patterns

- Re-running init over an existing `workspace/` without an explicit
  revision request.
- A kernel containing feature logic, or modules depending directly on each
  other.
- The agent answering its own interview questions, or writing before
  explicit validation.
- Generic interview questions; a second interview vocabulary; a second
  dispatch mechanism.
- Re-explaining kit rules (doc-comments, testing, boundaries, injection) —
  point by id.
- Shipping `workspace/` content from the kit, or touching a project that is
  not being initialized.
