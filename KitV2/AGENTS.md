# Go Agent Development Kit (KitV2)

KitV2 is the standalone consumable Go agent kit: rules, recipes, knowledge,
snippets, templates, probes, and a pinned UI SDK zone — everything an agent
needs to build idiomatic Go software, Go-generalist first.

## Source of truth

| Zone | Mission (one line) | Pointer |
| --- | --- | --- |
| `rules/` | Agent rules and principles (catalog freshness, single-source, example consistency) | `rules/core/`, `rules/registry/` |
| `knowledge/` | Sourced product indexes and decision context; must not duplicate rule/recipe bodies or metaproject history | `knowledge/INDEX.md` |
| `recipes/` | Runnable Go recipes, tests, and procedure documents | `recipes/README.md` |
| `snippets/` | Metadata-bearing, focused examples linked to a canonical recipe or rule | `snippets/README.md` |
| `templates/` | Runnable project bases or explicitly labelled partial contracts | `templates/README.md` |
| `probes/` | Product-facing runnable verification scenarios, including the offline retrieval probe | `probes/README.md` |
| `tools/offline/` | Stdlib-only resolver, manifest, pinned source bundle, and attribution files | `tools/README.md` |
| `router/` | Generated read-only routing index; `search_kit_resources` routes tasks to resources without loading the kit | `router/README.md` |
| `ui-kit/` | Pinned ui-agent-kit SDK zone (Wails/React UI rules, patterns, skills, docs); merged instructions in the "UI work" section; `search_ui_kit_resources` for UI tasks | `ui-kit/AGENTS.md` |
| `.pi/` | Native Pi settings, prompt templates, skills, and the `search_kit_resources` extension loaded after trust | `.pi/README.md` |

If two files answer the same question, keep one canonical answer and replace
the other with a pointer. Catalog updates require fresh primary-source
research and dated `Verified sources`; fenced Go examples must handle
returned errors or be marked `illustrative`. The source registry never
overrides the kit charter or these rules; source-derived content remains
subject to evidence and validation gates.

## Workflow

For ordinary non-trivial work, use the native skills and prompts of `.pi/`
(checklist-* for reviews, `workflow-memory` for memory). For large-scale
transformations (rewrite, migration, overhaul, whole-project refactor), use
the `spec-driven-dev` skill: it runs the seven-phase pipeline (intent,
deep analysis with S.U.P.E.R health, grounded refinement, decomposition with
delivery batches, progress tracking via `docs/progress/MASTER.md`, confirmed
execution with adaptive control, archive) and composes the other kit
resources — it replaces the former `workflow-clarify → plan → tasks →
implement → verify` prompt chain (removed 2026-08-05). The `deep-discuss`
skill handles structured problem analysis and solution design.

**Routing is mandatory, not optional.** Before planning or implementing any
technical work, call `search_kit_resources` with the task's technical terms
and read the top matching resource (rule, recipe, pattern, or catalog) before
writing code — the index only routes, the kit files stay the source of truth.
See the `kit-resource-routing` skill for query formulation and result
interpretation. The tool's own guidelines name the rules and patterns that
apply by default to ordinary Go code (naming, error wrapping, channel
ownership, zero-value design); treat those as pre-loaded even when the user
does not name them. Catalog fiches are routed on demand and are deliberately
absent from the always-visible skill surface.

## UI work — Wails projects (merged ui-agent-kit SDK instructions)

<!-- ui-kit/AGENTS.md sha256: ae432ca832839f98ba80eea058f626880facd77ab6392152bf7d191a8f36f1ad — this section mirrors the pinned SDK AGENTS.md; the re-sync helper (metaproject) fails when the checksum drifts. Update the prose at every ui-kit update, never lose an instruction from either file. -->

The kit stays Go-generalist, but a real subset of projects are **Wails
desktop apps** (Go backend + React frontend in `frontend/`). Detect: a
`wails.json` at the project root AND a `frontend/` directory. Only when both
are present do the instructions below apply — for plain Go projects none of
this is active: no UI rule, skill, or router entry fires.

The UI domain is governed by the **ui-agent-kit SDK**: the pinned `ui-kit/`
zone in this kit, and — once `tools/sync-ui-kit.sh` materialized it into a
Wails project — also `<frontend>/ui-kit/`. All paths below are relative to
that folder (the zone in the kit, or `frontend/ui-kit/` in a synced consumer
project). For UI work call `search_ui_kit_resources` (never
`search_kit_resources`) and read `ui-kit/AGENTS.md`. The zone is a pinned,
separate corpus: it never mixes with the Go index, its skills are registered
in `.pi/settings.json` but inert by description, and nothing is copied into
a project's `frontend/` unless the Wails layout is detected.

**Stack**: Wails v2/v3 · React + TypeScript + Vite · Tailwind CSS · shadcn/ui + Radix UI · Lucide React. The frozen base (shadcn/ui, Radix, Tailwind,
Lucide) is provided by the consuming app via the shadcn CLI — it is never
duplicated or modified in the SDK.

**Before any UI task**:

1. Read `ui-sdk/docs/CONSUMPTION.md` — the copy-paste contract for using
   pieces in an app.
2. Read `docs/wails-constraints.md` — the hard static-build constraints of
   the target platform. They are non-negotiable.
3. If you touch an interface, read the relevant `ux/` files first and update
   them after (see `skills/ux-memory/SKILL.md`).
4. Any design rule you write must cite a source (`docs/design-systems.md`).

**Absolute rules (UI work)**:

- The frozen base is **never** modified. We never "improve" an existing
  component: we create a new one next to it, explicitly named
  (`PremiumButton`, `DesktopButton`…) with a sourced justification in
  `ui-rules/` or `patterns/` and an entry in `ui-sdk/components-index.md`.
- **Static-only, Wails-bound**: the frontend must build to a static bundle
  (`frontend/dist/`, embedded via `//go:embed`). No SSR, no `next/*`
  imports. Navigation uses hash routing (`HashRouter`); Vite uses
  `base: "./"`; platform features (windows, dialogs, menus, system info) go
  through `@wailsio/runtime` + generated Go bindings — never re-implemented
  in components (see `docs/wails-constraints.md`).
- Any added rule/pattern cites its source (official design system or verified
  skill — see `docs/design-systems.md`).
- No silent duplication: if a piece already exists in
  `ui-sdk/components-index.md`, reuse it; otherwise create a new named piece.
- **The SDK folder is autonomous**: it never references the metaproject
  (governance, references, meta skills) — everything it needs is inside
  (`docs/`, `skills/`, `ui-sdk/docs/`). If a piece of content can only exist
  outside, it does not belong in the SDK: bring its source in or drop it.
- **All files are written in English** — the ecosystem standard.
- **Every change is verified**: after any implementation, run the diagnostics
  pass (typecheck, lint, build, markdownlint) and fix what it finds before
  reporting done.

**Where to find what** (relative to the ui-kit folder):

| Need | Where |
| --- | --- |
| Copy-paste consumption contract | `ui-sdk/docs/CONSUMPTION.md` |
| Wails static constraints | `docs/wails-constraints.md` |
| Reference design systems & sourcing | `docs/design-systems.md` |
| Authoring guides (format of every living file) | `docs/authoring-guides/` |
| Interface rules (spacing, colors, typography…) | `ui-rules/` |
| How to organize a screen | `patterns/` |
| Components / blocks / layouts index | `ui-sdk/components-index.md` |
| Product memory (personas, flows, screens) | `ux/` (see `skills/ux-memory/`) |
| Interface review guard | `skills/ui-review/SKILL.md` |
| Reference skills (shadcn, design systems) | `skills/` |

**Commands** (verified 2026-08-06):

```bash
npx shadcn@latest add --all          # install the frozen base in a consumer app
npx shadcn@latest search <query>     # search shadcn components
npx shadcn@latest docs <component>   # docs for a shadcn component
npx skills add <owner>/<repo> -a pi  # install a skill for Pi
```

**Skills registration**: the SDK skills are declared to Pi through the root
`.pi/settings.json` (`"skills": ["../ui-kit/skills"]` — the single
registration point; the SDK's nested `.pi/settings.json` is dead by design,
D-2026-08-08-02). A root `skills/` folder is never auto-discovered by Pi.

## Memory (consumer projects)

Pi initializes `.pi/memory/` with a minimal default set — `Decisions.md` is
**not** created by the bootstrap. Any agent using this kit MUST verify which
memory files actually exist before relying on them:

- inventory the real files under `.pi/memory/` (`Brief`, `Progress`,
  `Gotchas`, `Agent`, `Decisions`);
- create the missing files in the host's expected format, without copying kit
  or metaproject history;
- never assume the standard set is present; never write to a file that does
  not exist as if it did.

Follow `workflow-memory` for initialization and updates. Durable rules,
gotchas, and decisions discovered during a spec-driven run go into the
resolved memory surface.

## Validation

From `KitV2/`, with `PATH="$PATH:$(go env GOPATH)/bin"` for the lint/security
tools:

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

If a consumer environment lacks a required tool, report the gate as `PARTIAL`,
never as passing. The CI workflows (metaproject gate and
`templates/_kit-ci-workflow.yml`) additionally enforce an aggregate coverage
floor of 70%; the local gate does not.

## Limits

The kit does not claim to cover: Go-side desktop-application wiring beyond
the `recipe-desktop-app` recipe, TUI development beyond the kit's interactive
Bubble Tea recipe, Pi discovery internals, or non-Go domains other than the
Wails/React frontend surface that the pinned `ui-kit/` zone governs — check
the catalog, the Go router (`search_kit_resources`) and the UI router
(`search_ui_kit_resources`) before expecting a kit resource for a technology.

Always preserve errors, cancellation, input validation, and observable
evidence. Ask before adding dependencies or changing the manifest contract.
Never claim an unexecuted scenario passed or treat static checks as proof of
user intent.
