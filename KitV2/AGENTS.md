# Go Agent Development Kit

Standalone consumer kit for building idiomatic Go software: a typed corpus
of rules, recipes, knowledge, snippets, templates, probes, and a pinned UI
SDK zone. Go-generalist first; the UI domain activates only for Wails
projects (see "UI work — Wails projects").

This file is the agent's execution contract, not the kit's documentation
(the shipped user guide `.pi/docs/GOAK.md` is). When two files answer the
same question, keep one canonical answer and replace the other with a
pointer — never both.

## Normative levels

Every instruction uses exactly one level below; the level is the meaning.
Never introduce near-synonyms ("strongly recommended", "prefer") — they
blur the hierarchy.

| Level | Meaning |
| --- | --- |
| MUST | absolute obligation, no exception |
| MUST NOT | absolute prohibition, never |
| SHOULD | default rule; deviation only with a stated reason |
| MAY | authorized choice, no preference |

Vocabulary: a **tool** is an extension-provided function
(`search_kit_resources`), a **skill** is a loadable capability
(`.pi/skills/`), a **prompt** is a slash command (`.pi/prompts/`), a
**resource** is an indexed kit file.

<!-- user guide section: begin -->
## User guide — new to this kit?

The kit ships its own user guide at `.pi/docs/GOAK.md` — the source of
truth for how to use the kit, readable with no other documentation. A fresh
user (or an agent asked "how do I use this kit?") MUST start there, or run
the `/goak-help` prompt, which orders the agent to read the guide and
explain it. The onboarding banner shown at session start (Get Started / new
large feature / new small feature) points to the same three starting paths.
<!-- user guide section: end -->

## Non-Negotiable Rules

These invariants apply to every task, in every project state; a rule that
conflicts with an invariant is wrong.

- **Single source of truth.** One canonical answer per question; this file
  routes to rules, recipes, and knowledge — it never duplicates their
  bodies.
- **No invention.** When the project has an expected canonical source
  (foundation, memory, catalog, decision), never fabricate the missing truth
  from assumptions: find it, or state that it is absent. Never assume a file
  exists or a state holds — verify.
- **Evidence over claims.** Never claim an unexecuted scenario passed, and
  never treat static checks as proof of user intent. Report validation with
  exactly one status: PASS, PARTIAL, or FAIL (see "Validation").
- **Preservation.** Always preserve errors, cancellation, input validation,
  and observable evidence; nothing may drop them.
- **Contracts.** Ask before adding a dependency, changing the manifest
  contract, or altering a published metadata schema.
- **English only.** All files are written in English; code, commands, and
  identifiers are never translated.
- **Catalog integrity.** Catalog updates require fresh primary-source
  research and dated `Verified sources`; fenced Go examples must handle
  returned errors or be marked `illustrative`.

## Repository map

| Zone | Mission (one line) | Pointer |
| --- | --- | --- |
| `rules/` | Agent rules and principles (catalog freshness, single-source, example consistency) | `rules/core/`, `rules/registry/` |
| `knowledge/` | Sourced product indexes and decision context; must not duplicate rule/recipe bodies or decision history | `knowledge/INDEX.md` |
| `recipes/` | Runnable Go recipes, tests, and procedure documents | `recipes/README.md` |
| `snippets/` | Metadata-bearing, focused examples linked to a canonical recipe or rule | `snippets/README.md` |
| `templates/` | Runnable project bases or explicitly labelled partial contracts | `templates/README.md` |
| `probes/` | Product-facing runnable verification scenarios, including the offline retrieval probe | `probes/README.md` |
| `tools/offline/` | Stdlib-only resolver, manifest, pinned source bundle, and attribution files | `tools/README.md` |
| `router/` | Generated read-only routing index; `search_kit_resources` routes tasks to resources without loading the kit | `router/README.md` |
| `ui-kit/` | Pinned ui-agent-kit SDK zone (Wails/React UI rules, patterns, skills, docs); `search_ui_kit_resources` for UI tasks | `ui-kit/AGENTS.md` |
| `.pi/` | Native Pi settings, prompt templates, skills, and the `search_kit_resources` extension loaded after trust | `.pi/README.md` |

The source registry never overrides these rules; source-derived content
stays subject to evidence and validation gates.

## Task Routing

**Routing is mandatory, not optional.** Before planning or implementing any
technical work, call `search_kit_resources` with the task's technical terms
and read the top matching resource (rule, recipe, pattern, or catalog)
before writing code. Follow the `kit-resource-routing` skill for query
formulation and result interpretation. The index only routes; the kit files
stay the source of truth.

Workflow selection (task → skill):

- **Ordinary Go work** — route, then plan and implement directly. The
  tool's own guidelines name the rules and patterns that apply by default
  (naming, error wrapping, channel ownership, zero-value design); treat
  them as pre-loaded even when unnamed. Catalog fiches
  are routed on demand and are deliberately absent from the always-visible
  skill surface.
- **Large-scale transformation** (rewrite, migration, overhaul,
  whole-project refactor) — SHOULD use the `spec-driven-dev` skill: a
  seven-phase pipeline (intent, deep analysis with S.U.P.E.R health,
  grounded refinement, decomposition with delivery batches, progress
  tracking via `docs/progress/MASTER.md`, confirmed execution with adaptive
  control, archive) that composes the other kit resources.
- **Structured problem analysis and solution design** — use the
  `deep-discuss` skill.
- **Reviews** — use the `checklist-*` prompts of `.pi/`.
- **New project** — before the first feature, run `workspace-init` (see
  "Project Foundation").
- **"How do I use this kit?"** — run `/goak-help` or read
  `.pi/docs/GOAK.md`; never answer from general knowledge.
- **Memory** — follow the `workflow-memory` skill (see "Memory").

<!-- workspace-init section: begin -->
## Project Foundation — new consumer projects

Before the first feature of a new project (and before any `spec-driven-dev`
run), the kit recommends initializing the project foundation with the
`workspace-init` skill: one day-0 session that decides the
kernel/modules boundary, pins the stack, non-negotiables, and testing
policy, and writes `workspace/` (CONSTITUTION.md, ARCHITECTURE.md, optional
DOMAIN.md, decisions/, research/) plus a "Project Foundation" section in
the project's own `AGENTS.md`.

- **Initialized project**: `workspace/CONSTITUTION.md` and
  `workspace/ARCHITECTURE.md` are the foundation reference — read them
  before any feature work; `spec-driven-dev` reads them in its continuity
  check and makes Phase 0 consistent with them.
- **Not initialized**: run `workspace-init` (strongly recommended, never a
  hard gate). Do not invent a foundation on the fly per feature.
- The workspace docs are project-owned: written by the init session, never
  synced from the kit. Projects that are not initialized carry no
  project-specific section here — only this generic pointer.
<!-- workspace-init section: end -->

## UI work — Wails projects

<!-- ui-kit/AGENTS.md sha256: ae432ca832839f98ba80eea058f626880facd77ab6392152bf7d191a8f36f1ad — the UI domain's complete rule surface is ui-kit/AGENTS.md (single source); this section is its condensed pointer (activation guard, routing, cross-cutting invariants). The re-sync helper fails when the checksum drifts — re-verify this section against the new SDK instructions and refresh the marker. -->

**Activation guard.** The UI domain is active ONLY when `wails.json` exists
at the project root AND a `frontend/` directory is present. Otherwise none
of the rules below apply — no UI rule, skill, or router entry fires, and
the kit stays Go-generalist.

**When active, MUST:**

1. Read `ui-kit/AGENTS.md` before any UI work — it is the domain's complete
   instruction surface; this section only adds the guard and the
   cross-cutting invariants.
2. Call `search_ui_kit_resources` for UI tasks — never
   `search_kit_resources`.
3. Respect the invariants below (they mirror the SDK's absolute rules).

**Cross-cutting invariants (UI work):**

- The frozen base (shadcn/ui, Radix, Tailwind, Lucide) is provided by the
  consuming app via the shadcn CLI — never duplicated, never modified.
  Never "improve" an existing component: create a new, explicitly named one
  next to it, with a sourced justification and an index entry.
- Static-only, Wails-bound: a static bundle in `frontend/dist/` embedded
  via `//go:embed`; no SSR, no `next/*` imports; hash routing;
  `base: "./"`; platform features via `@wailsio/runtime` + generated Go
  bindings.
- No silent duplication: reuse what exists in `ui-sdk/components-index.md`
  before creating a new named piece.
- Any added rule or pattern cites its source (official design system or
  verified skill — see `docs/design-systems.md`).
- All files are written in English.
- The SDK folder is autonomous: it never references external project
  machinery; if content can only live outside the SDK, it does not belong in
  it.
- Every change is verified: run the diagnostics pass (typecheck, lint,
  build, markdownlint) and fix what it finds before reporting done.

All other UI rules — stack, consumption contract, constraints, UX,
skills — live in `ui-kit/AGENTS.md`; read it, not this section.

## Memory

Pi initializes `.pi/memory/` with a minimal default set — `Decisions.md` is
NOT created by the bootstrap.

- **Rule**: never assume a memory file exists; never write to a file that
  does not exist as if it did.
- **Procedure**: before relying on memory, inventory the real files under
  `.pi/memory/` (`Brief`, `Progress`, `Gotchas`, `Agent`, `Decisions`);
  create missing files in the host's expected format, without copying
  external history.
- **Reference**: follow the `workflow-memory` skill for initialization and
  updates. Durable rules, gotchas, and decisions discovered during a
  spec-driven run go into the resolved memory surface.

## Validation

**Scope.** The gate below validates the kit itself. Run it from the kit
root, with `PATH="$PATH:$(go env GOPATH)/bin"` for the lint/security tools.
A consumer project validates with its own project gate, not this list.

```sh
python3 tools/validators/validate-kitv2.py
KITV2_STRICT_CATALOG=1 python3 tools/validators/validate-kitv2.py  # required for catalog changes
go mod tidy && go mod verify
test -z "$(gofmt -l .)"
go vet ./...
golangci-lint run ./...
go test -race ./...
gosec ./...
govulncheck ./...
bash probes/run.sh
```

**Status semantics.** Report the gate with exactly one status:

| Status | Meaning |
| --- | --- |
| PASS | gate executed; every check succeeded |
| FAIL | gate executed; at least one check failed |
| PARTIAL | gate incomplete; one or more checks could not run (e.g. a required tool is missing) |

If a consumer environment lacks a required tool, report the gate as
`PARTIAL`, never as passing. The shipped CI workflow
(`templates/_kit-ci-workflow.yml`) additionally enforces an aggregate
coverage floor of 70%; the local gate does not.

## Limits

The kit does not claim to cover the following. Check the catalog and both
routers (`search_kit_resources`, `search_ui_kit_resources`) before expecting
a kit resource for a technology.

| Out of scope | Coverage |
| --- | --- |
| Go-side desktop-application wiring | beyond the `recipe-desktop-app` recipe |
| TUI development | beyond the kit's interactive Bubble Tea recipe |
| Pi discovery internals | none |
| Non-Go domains | none, except the Wails/React frontend surface governed by the pinned `ui-kit/` zone |

Always preserve errors, cancellation, input validation, and observable
evidence. Ask before adding dependencies or changing the manifest contract.
Never claim an unexecuted scenario passed or treat static checks as proof of
user intent.
