# Go Agent Kit — User Guide

> The Go Agent Kit (GOAK) is a self-contained kit for building idiomatic Go
> software with a coding agent (Pi). It ships rules, recipes, knowledge,
> templates, probes, a semantic resource router, and a Pi runtime surface
> (prompts, skills, extensions). This guide is the shipped source of truth:
> it is installed with the kit and works with no other documentation.

This guide has two levels:

- **[Get Started](#2-get-started)** — the minimal path from "just installed"
  to "project ready" (read this first).
- **[Deep usage](#3-deep-usage)** — how the kit really works: commands,
  workflows, structure, capabilities, rules, troubleshooting.

## 1. What the kit brings

| Capability | Where | Use it for |
| --- | --- | --- |
| Rules | `rules/` | Go conventions: naming, errors, context, concurrency, validation |
| Recipes | `recipes/` | Runnable Go procedures with tests (CLI, REST, SQLite, worker pool, graceful shutdown, desktop service) |
| Knowledge | `knowledge/` | Patterns, anti-patterns, architecture, security, library fiches |
| Templates | `templates/` | Sourced project bases (REST, CLI, worker) and document templates |
| Probes | `probes/` | Executable scenarios that verify the kit's observable behavior |
| Resource router | `router/` + `search_kit_resources` | Find the kit resource that answers a task |
| UI SDK (Wails only) | `ui-kit/` + `search_ui_kit_resources` | UI rules/patterns for Wails desktop projects |
| Pi surface | `.pi/` | Prompts (`/goak-help`, `/checklist-*`), skills (`spec-driven-dev`, `workspace-init`, …), onboarding banner |

What it is **not**: a framework, a starter repo, or a replacement for Go's
standard library. It reduces the decisions an agent makes when building Go
software and keeps those decisions verifiable.

## 2. Get Started

Precondition: the kit is installed in your project root (installer:
`curl -fsSL https://raw.githubusercontent.com/TheophileBaudouin/GoAK/<ref>/install.sh | sh -s -- <dir>`,
where `<ref>` is a release tag such as `v2.7.1` and `<dir>` your project).

1. **Enter the project** — `cd <dir>`.
2. **Open Pi** — run `pi`. Approve project trust when asked (headless:
   `pi -a`). In interactive mode you will see the GOAK banner with three
   entries: Get Started, new large feature, new small feature (headless
   runs render no UI).
3. **Type `/goak-help`** — the agent reads this guide and explains the kit.
   Ask it anything ("what do I do now?", "how do I start a feature?").
4. **Verify the install** — run:

   ```sh
   python3 tools/validators/validate-kitv2.py   # product structure (needs python3 + PyYAML)
   bash probes/run.sh                           # observable scenarios (needs a Go toolchain)
   ```

   Both green means the kit works. If a tool is missing, the result is
   `PARTIAL`, not a failure of the kit.
5. **Initialize the project foundation** (recommended before the first
   feature) — run the `workspace-init` skill: one day-0 session that pins
   the stack, non-negotiables, and testing policy, and writes
   `workspace/` (CONSTITUTION.md, ARCHITECTURE.md) plus a "Project
   Foundation" section in your own `AGENTS.md`.
6. **Start a feature** — decide the path with the
   [workflow decision table](#33-workflow-decision-table), then follow it.

Done: your project is ready. The rest of this guide is reference — read the
sections you need, when you need them.

## 3. Deep usage

### 3.1 Commands

| Command | What it does | When |
| --- | --- | --- |
| `/goak-help` | Agent reads this guide (`.pi/docs/GOAK.md`) and explains the kit | First use, orientation, any "how do I…" question |
| `/checklist-api` | REST API review checklist with evidence verdicts | Before/while reviewing an API surface |
| `/checklist-release` | Release checklist separating mechanics and behavior | Before tagging/releasing |
| `/workflow-memory` | Initialize and maintain your project's `.pi/memory/` | Project start, after durable decisions/blockers |
| `search_kit_resources` (tool) | Top-K of kit resources for a task's technical terms | **Before any technical work** (routing is mandatory) |
| `search_ui_kit_resources` (tool) | Top-K of ui-kit resources for a UI task (Wails only) | Before any interface work in a Wails project |

Prompts and skills load after the project is trusted in Pi. If a command is
missing, run `/reload` or restart Pi.

### 3.2 Workflows

#### 3.3 Workflow decision table

| Situation | If… | Then… |
| --- | --- | --- |
| Large transformation | Rewrite, migration, overhaul, whole-project refactor, or a feature touching several components with an architecture decision | Use the **`spec-driven-dev` skill** — the seven-phase pipeline (intent → deep analysis → grounded refinement → decomposition with delivery batches → progress tracking → confirmed execution with adaptive control → archive). It replaces any ad-hoc "clarify → plan → tasks → implement → verify" chain. The discussion with you is built into the pipeline (Phase 2, grounded in the codebase analysis) — do not run a separate discussion workflow before it. |
| Problem analysis / design decision | A symptom, failure, or decision difficulty — "let's discuss", "help me analyze", "I'm torn between" — before any transformation is decided | Use the **`deep-discuss` skill** — a structured multi-phase discussion (receive → audit → deep analysis → solution design) that understands the problem before proposing anything. If the conclusion is a large transformation, then run `spec-driven-dev`. |
| Ordinary non-trivial change | One feature, one component, no architecture decision | Work directly: call `search_kit_resources`, follow the `kit-resource-routing` skill, use the native prompts/skills of `.pi/` (`/checklist-*`, `/workflow-memory`), read `AGENTS.md` sections that apply. |
| Project foundation | Before the first feature of a new project | Run **`workspace-init`** (kernel-first day-0 protocol; writes `workspace/` + a Project Foundation section in your `AGENTS.md`). Never invent a foundation per-feature. |
| UI work (desktop) | `wails.json` AND `frontend/` exist at the project root | Use the **ui-kit** corpus: call `search_ui_kit_resources` (never `search_kit_resources`), read `ui-kit/AGENTS.md` and `ui-kit/ui-sdk/docs/CONSUMPTION.md` before any interface code. For plain Go projects the UI corpus is inert. |
| Nothing matches | No kit resource covers the task | Say so, proceed with Go best practices (the kit's rules still apply), and note the gap. |

#### 3.4 The spec-driven-dev pipeline (large changes)

1. **Phase 0-1** — intent and deep analysis (with the S.U.P.E.R health lens;
   sourced kit rules win over doctrine).
2. **Phase 2** — grounded refinement of the plan.
3. **Phase 3** — decomposition into delivery batches.
4. **Phase 4** — progress tracking via `docs/progress/MASTER.md`.
5. **Phase 5** — confirmed execution with adaptive control (each batch
   verified; drift handled explicitly).
6. **Phase 6** — archive the run.

Run `spec-driven-dev` only after the project foundation exists
(`workspace/CONSTITUTION.md`/`ARCHITECTURE.md` when initialized); the skill
reads them in its continuity check.

### 3.5 Kit structure

| Zone | Mission | Pointer |
| --- | --- | --- |
| `rules/` | Agent rules and principles | `rules/core/`, `rules/registry/` |
| `knowledge/` | Sourced indexes and decision context | `knowledge/INDEX.md` |
| `recipes/` | Runnable Go recipes, tests, procedures | `recipes/README.md` |
| `snippets/` | Focused examples linked to a canonical recipe/rule | `snippets/README.md` |
| `templates/` | Runnable project bases or labelled partial contracts | `templates/README.md` |
| `probes/` | Runnable verification scenarios | `probes/README.md` |
| `tools/offline/` | Stdlib-only resolver, manifest, pinned source bundle | `tools/README.md` |
| `router/` | Generated read-only routing index | `router/README.md` |
| `ui-kit/` | Pinned UI SDK zone (Wails/React) | `ui-kit/AGENTS.md` |
| `.pi/` | Pi settings, prompts, skills, extensions, this guide | `.pi/README.md` |

If two files answer the same question, keep one canonical answer and point
the other to it — this is a kit-wide rule.

### 3.6 Finding capabilities

1. **Route first**: call `search_kit_resources` with 3–8 technical terms in
   English, one concern per query (example: "bounded worker pool with
   context cancellation"). Read the top matching resource (rule, recipe,
   pattern, or catalog) before writing code. The index only routes — the kit
   files stay the source of truth.
2. **Browse**: `knowledge/INDEX.md` lists every knowledge domain;
   `router/index.json` is the full generated index.
3. **Ask**: `/goak-help` for kit orientation; `/checklist-api` and
   `/checklist-release` for review procedures.

The router applies by default on every Go task: naming (rule `naming`),
error wrapping (pattern `error-wrapping-chain`), channel ownership (pattern
`concurrency-channel-ownership`), and zero-value design (pattern
`go-zero-value-valid`) govern ordinary code even when you do not name them.

### 3.7 Working rules

- **Routing is mandatory, not optional.** Call `search_kit_resources` before
  planning or implementing technical work. If it returns no match, say so
  and proceed with general Go knowledge.
- **Memory is local and verified.** Pi initializes `.pi/memory/` with a
  minimal default set — `Decisions.md` is NOT created by default. Always
  inventory which memory files actually exist before relying on them
  (`Brief`, `Progress`, `Gotchas`, `Agent`, `Decisions`); create the missing
  ones with `/workflow-memory`; never copy external history into them.
- **English only.** All kit content, docs, and project artifacts are written
  in English; ids stay ASCII kebab-case.
- **Validation gate.** From the kit root, with
  `PATH="$PATH:$(go env GOPATH)/bin"`:

  ```sh
  python3 tools/validators/validate-kitv2.py
  go mod tidy && go mod verify
  test -z "$(gofmt -l .)"
  go vet ./...
  golangci-lint run ./...
  go test -race ./...
  gosec ./...
  govulncheck ./...
  bash probes/run.sh
  ```

  A missing tool reports `PARTIAL`, never PASS. Never claim an unexecuted
  scenario passed.
- **Ask before**: adding dependencies, changing the manifest contract,
  changing a published metadata contract.

### 3.8 Limits

The kit does not claim to cover: Go-side desktop wiring beyond the
`recipe-desktop-app` recipe, TUI development beyond the interactive Bubble
Tea recipe, Pi discovery internals, or non-Go domains other than the
Wails/React surface governed by `ui-kit/`. Check the router before expecting
a kit resource for a technology.

## 4. Troubleshooting

| Symptom | Cause / fix |
| --- | --- |
| No GOAK banner at startup | The banner shows on session start/reload in interactive mode only. Run `/reload`; if it still does not show, the banner file `.pi/onboarding/banner.md` is missing (broken install) — reinstall the kit. |
| `/goak-help` or `/checklist-*` not found | Prompts load after project trust. Run `/reload` or restart Pi and approve trust (`pi -a` headless). |
| Verification reports `PARTIAL` | A tool is missing (python3/PyYAML for the validator, Go toolchain for probes). Install it, or run the commands that can run; never treat PARTIAL as PASS. |
| `probes/run.sh` fails on module download | Offline bundle pins may have drifted from `go.mod` — the validator's bundle check reports it; reinstall a release where manifest and `go.mod` agree. |
| `search_kit_resources` returns no match | The query is outside the kit's domain or badly phrased. Reformulate with Go-specific technical terms, or conclude that no kit resource applies. |
| UI tools return "no ui-kit SDK zone" | The project has no Wails layout (no `wails.json` + `frontend/`); the UI corpus is deliberately inert there. |
| A doc/command in this guide differs from the kit | This guide is the shipped contract; the kit's validator (`check_consumer_onboarding` inside `validate-kitv2.py`) fails when the guide, `/goak-help`, or the banner drift from the required structure — report the mismatch rather than working around it. |
