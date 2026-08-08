# Research — `workspace-init`: a kernel-first project foundation protocol

**Date:** 2026-08-08
**Scope:** external sources for the new protocol (kernel/modules decision,
`workspace/` capture, SDK documentation), plus a full inventory of what the
kit already covers so the protocol only adds what is genuinely missing.
**Status:** fresh research performed 2026-08-08 (web) — no reuse of agent
memory for cataloged content. Sub-agent research failed on OpenRouter key
limits (403); the web research was completed inline with `web_search` +
direct source fetches (raw.githubusercontent.com).

---

## 1. Microkernel / Plugin architecture (Mark Richards)

The academic name for "kernel + modules" is the **Microkernel Architecture
style** (also called plugin architecture). Authoritative sources:

- Mark Richards, *Fundamentals of Software Architecture*, ch. 13
  (O'Reilly, 2nd ed): <https://www.oreilly.com/library/view/fundamentals-of-software/9781098175504/ch13.html>
- Mark Richards, *Software Architecture Patterns*, ch. 3/4:
  <https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch03.html>
  and <https://www.oreilly.com/library/view/software-architecture-patterns/9781098134280/ch04.html>
- Mark Richards lesson 160 (2023-05): <https://www.developertoarchitect.com/lessons/lesson160.html>

Core facts to cite in kit artifacts (never as a home-made definition):

- A **minimal core kernel** (bootstrap, shared contracts, cross-cutting
  concerns) plus **peripheral modules** (plugins) that communicate only
  through the kernel's exposed interface, never directly with each other.
- A **module registry** (discovery + instantiation); kernel stays
  pluggable; failures are contained (an ecosystem where plugin bugs do not
  take down the core).
- The **main cost is the design of the kernel contract**: it must be small,
  stable, and sufficient for every module's needs. This maps exactly to the
  "SDK premium" Théo wants: the SDK *is* the kernel's public contract.

## 2. The pattern implemented in Go

Real, verifiable Go implementations of in-process microkernel/plugin
registries:

- **hansmi/staticplug** — build-time plugins, the canonical registry
  pattern: `var Registry = staticplug.NewRegistry()` + registration from
  `init()`: <https://github.com/hansmi/staticplug>
- **Go stdlib `plugin` package** — dynamic loading caveats (Linux-only,
  no close, version skew) that justify in-process registries instead:
  <https://pkg.go.dev/plugin>
- **dev.to — "Building a Plugin System in Go Without `plugin`: 3 Patterns
  That Actually Ship"** (compile-time registration: define the interface,
  each implementation in its own package, a tiny registry collected at
  process start via `init()`): <https://dev.to/gabrielanhaia/building-a-plugin-system-in-go-without-plugin-3-patterns-that-actually-ship-133d>
- **larksuite/cli extension/platform** — an in-process plugin SDK inside a
  CLI: blank import + `init()` registration, plugins share the binary's
  address space: <https://github.com/larksuite/cli/tree/main/extension/platform>
- **gavmor/wasm-microkernel** — guest/host facade split (plugin authors
  import only `guest`, hosts import only `host`):
  <https://github.com/gavmor/wasm-microkernel/blob/main/README.md>
- **Aleksei Aleinikov, "Scalable Micro-Kernel with Go, 2025 Edition"** —
  kernel keeps only lifecycle/event-routing/synchronization; business logic
  lives in detachable plugins; plugins depend on the core contract, not on
  each other: <https://levelup.gitconnected.com/scalable-micro-kernel-with-go-2025-edition-919a2b399dba>

Pattern synthesis (to point to, not to re-teach):
`interface` (contract) defined by the kernel → implementations in isolated
packages → `init()`-registered into a small registry → bootstrap composes.
This is exactly the kit's existing `go-constructor-injection` and
`architecture-ports-adapters` patterns applied at application level.

## 3. `spec-kit` constitution mechanics (direct template source)

- **Repo:** <https://github.com/github/spec-kit> (the kit's own
  `spec-driven-dev` skill already derives from this family). **License:
  MIT** (verified via the GitHub API on 2026-08-08) — adaptation is
  lawful; never copied verbatim.
- **`/speckit.constitution` command template:**
  <https://github.com/github/spec-kit/blob/main/templates/commands/constitution.md>
  — writes/updates `.specify/memory/constitution.md`; scope guard (only the
  constitution, never feature code); placeholder tokens `[ALL_CAPS]`;
  semver on the constitution (MAJOR = principle removal/redefinition, MINOR
  = new principle/section, PATCH = wording); Sync Impact Report prepended;
  validation (no unexplained brackets, ISO dates, declarative/testable
  principles, MUST/SHOULD over "should").
- **Constitution template structure:**
  <https://github.com/github/spec-kit/blob/main/templates/constitution-template.md>
  — `# [PROJECT_NAME] Constitution` → `## Core Principles` (name +
  description per principle) → free sections → `## Governance` (rules,
  guidance file, version, ratification date, last-amended date).
- **Re-read mechanics** — each later phase command re-loads the
  constitution "on demand for establishing context"; it is not pushed with
  every request (discussion #2476:
  <https://github.com/github/spec-kit/discussions/2476>; directory purposes
  #2660: <https://github.com/github/spec-kit/discussions/2660>).

This is the direct patron of `workspace/CONSTITUTION.md`, **adapted**: our
constitution carries not only principles but an architecture decision
(kernel + modules) and a stack/SDK plan.

## 4. `mattpocock/skills` primitives (to adapt, never copy verbatim)

**License: MIT** (verified via the GitHub API on 2026-08-08) — adaptation
is lawful; the skill text is never copied verbatim, only the mechanics
are adapted and re-expressed in the kit's own voice.

- **grilling** (the interview primitive):
  <https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md>
  — model the subject as a **design tree**; work it in **rounds**; each
  round asks the whole **frontier** (every decision whose prerequisites are
  settled); questions numbered `❓ Qn` with a recommended answer `➡️`;
  **facts are the agent's job** (dispatch sub-agents, never ask the user
  for what can be looked up), **decisions are the user's**; done when the
  frontier is empty AND the user confirms shared understanding; never act
  before that confirmation.
  Round-based rationale + limits (docs/productivity/grilling.md) — the
  frontier is the agent's judgment, not a computed graph.
- **grill-with-docs** (stateful variant):
  <https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md>
  — same interview, plus a `CONTEXT.md` **glossary** (terms resolved
  inline, lazily created, pure vocabulary) and **ADRs** under `docs/adr/`
  gated on three conditions (hard to reverse + surprising + real trade-off);
  assumes one writer. The glossary pattern is our optional `DOMAIN.md`.
- **codebase-design** (deep-module vocabulary):
  <https://github.com/mattpocock/skills/blob/main/skills/engineering/codebase-design/SKILL.md>
  — "a lot of behaviour behind a small interface, placed at a clean seam,
  testable through that interface"; vocabulary: module, interface, depth,
  seam, adapter, leverage, locality. Quotes Ousterhout.
- **setup-matt-pocock-skills** (one-shot day-0 init precedent):
  <https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md>
  — runs once before any other skill; explores the repo before prompting;
  walks guided decisions one at a time; **writes config, not behaviour**;
  `disable-model-invocation: true` (user-invoked only). This is the direct
  precedent for the "one-shot, day 0" mechanics Théo wants.

## 5. Deep modules (Ousterhout) — the SDK's theoretical justification

- John Ousterhout, *A Philosophy of Software Design* (2nd ed) — deep
  modules: the value of a module is the ratio between the behaviour it
  hides and the size of its interface ("The best modules are deep. They
  allow a lot of functionality to be accessed through a simple interface.").
  The kernel's SDK is exactly a deliberately small public interface over a
  kernel that does a lot of work behind it. (Quoted in mattpocock's
  codebase-design; the book itself is the primary source.)

## 6. Documenting an internal SDK for an AI agent (godoc as contract)

- **Go Doc Comments** (official, current): every exported name has a doc
  comment immediately preceding the declaration, starting with the name;
  package comments; doc comments are *the* API documentation:
  <https://go.dev/doc/comment>
- **Godoc: documenting Go code** (official blog): documentation should be
  coupled to the code so it evolves with it; runnable examples as first-class:
  <https://go.dev/blog/godoc>
- **Google Go Style Guide — doc comments**: first sentence = summary;
  doc preview during review; runnable examples are part of the contract:
  <https://google.github.io/styleguide/go/decisions.html>
- **godoc-lint**: a linter for doc practice, recommended for SDKs/API
  clients: <https://github.com/godoc-lint/godoc-lint>
- **godoc-mcp (mrjoshuak)**: structured Go docs for LLMs, "type signatures,
  error conditions, postconditions, thread safety, workflow patterns" —
  what an agent needs from docs, in token-efficient form:
  <https://github.com/mrjoshuak/godoc-mcp> ; AID-Docs spec:
  <https://github.com/dan-strohschein/AID-Docs>
- **Agent-Friendly Documentation Spec**: sites are increasingly consumed by
  coding agents; llms.txt-style discovery and truncation-aware structure:
  <https://agentdocsspec.com/>
- **Addy Osmani, "How to write a good spec for AI agents"**:
  <https://addyosmani.com/blog/good-spec/>

Synthesis for the skill: the SDK contract = doc-commented exported API
(kit rule `doc-comments` already enforces the convention) + executable
Example functions + a first-sentence summary per symbol; prose that
duplicates code is noise. The skill points to the kit rule and to these
sources; it does not re-teach them.

---

## 7. Kit inventory — what already exists (do not duplicate)

Scanned: `KIT_CHARTER.md`, `.agent/kit-governance/` (README, Z1/Z5/Z8/Z11/
Z12/Z13, A1), `KitV2/AGENTS.md`, `KitV2/.pi/settings.json`,
`KitV2/.pi/skills/spec-driven-dev/`, `kit-resource-routing/`,
`rules/registry/doc-comments/SKILL.md`, `rules/registry/testing/SKILL.md`,
the eight patterns listed in the request, `validate-kitv2.py`,
`validate-cognitive.py`, `validate-instructions.py`, router index.

**Already covered (the protocol must POINT, not re-explain):**

| Concern | Existing home |
| --- | --- |
| Module boundaries, strong internal boundaries | `knowledge/patterns/architecture-modular-monolith.yaml` (`pattern:architecture:modular-monolith`) |
| Domain decoupled from infrastructure | `knowledge/patterns/architecture-ports-adapters.yaml` |
| `internal/` public/private API boundary | `knowledge/patterns/go-internal-packages.yaml` |
| Explicit dependency wiring without a framework | `knowledge/patterns/go-constructor-injection.yaml` |
| Testable seams (logic vs effects) | `knowledge/patterns/testing-seam-injection.yaml` |
| Fakes over mocks | `knowledge/patterns/testing-fakes-over-mocks.yaml` |
| Black-box package tests through the exported API | `knowledge/patterns/testing-blackbox-package-tests.yaml` |
| Table-driven tests | `knowledge/patterns/testing-table-driven.yaml` |
| Doc-comment contract (exported API, revive-enforced) | `rules/registry/doc-comments/SKILL.md` |
| Testing rules | `rules/registry/testing/SKILL.md` |
| Kit resource discovery (mandatory search before technical work) | `kit-resource-routing` skill + `search_kit_resources` tool |
| Large-scale transformation workflow (7 phases, tiered dispatch) | `spec-driven-dev` skill (Z12) + `references/parallel-protocol.md` |
| Wails UI merge mechanics into `AGENTS.md` (checksum marker precedent) | `KitV2/AGENTS.md` "UI work" section + Z13 §4 |

**Genuinely missing (the protocol's scope):** the kernel-vs-modules
*decision itself*, its capture at project level (`workspace/`), the
production trigger for the SDK and its documentation, and the day-0
interview that produces them.

**Mechanics to reuse:**

- Z8 role boundary: prompts = short orchestrators; skills = durable
  procedures; `.pi/skills/*/SKILL.md` is auto-discovered by Pi (no
  `settings.json` entry needed — the settings file only registers
  `../rules`, `../recipes`, `../ui-kit/skills`).
- Router: `INDEXABLE_GLOBS` includes `.pi/skills/**/SKILL.md`; coverage
  check fails until `build_index.py` regenerates the index.
- Validators: `validate-cognitive.py` scans `.pi/skills/**/*.md` (prose-id
  C12); `validate-instructions.py` scans `.pi/skills/*/SKILL.md`
  (MANDATORY → named control); `validate-kitv2.py` checks router coverage,
  no-metaproject-paths, empty-markdown. `check_skill` (frontmatter +
  ≤500 lines) applies only to rules/recipes/catalogs — A1 §3 applies the
  ≤500-line budget to `.pi/skills/` by convention.
- `spec-driven-dev` "Before You Begin" continuity check already inventories
  instruction surfaces (AGENTS.md, `.pi/memory/`) — the natural, minimal
  anchor to read `workspace/` before Phase 0 without duplicating logic.
- AGENTS.md merge precedent (Z13 §4): identifiable HTML marker
  (`<!-- ui-kit/AGENTS.md sha256: … -->`), never lose existing content,
  conditional activation. Reversed flow here: the init session writes a
  per-project section into the consumer's AGENTS.md (project-owned, never
  synced from the kit).

## 8. Failure note

The `researcher` sub-agents (pi-subagents) hit an OpenRouter 403 key limit
(2026-08-08). Research was completed inline. If sub-agent research is
preferred for a later wave, the key limit must be resolved first.
