# Go Agent Development Kit (GoAK)

A self-contained knowledge kit that makes a code agent reliably build idiomatic
Go software. GoAK is a **typed knowledge graph** — sourced rules, runnable
recipes, verified snippets, MIT project templates, library catalogs, executable
probes, a semantic resource router, and a native Pi runtime surface. It is not
a folder of snippets and not a framework: every reusable artifact has stable
metadata, declared relationships, and a single responsibility, and every claim
is backed by a primary source or an executable scenario.

The consumable product is **`KitV2/`**: it installs standalone into any project
directory and works with no other documentation. The repository root is the
**metaproject** that builds and governs it — charter, construction contracts,
source registry, plans, evidence — none of which ships to consumers.

## What the kit gives you

| Zone | Content | Use it for |
| --- | --- | --- |
| `rules/` | Universal, sourced Go rules: naming, errors, context, concurrency, validation, doc comments, logging, testing | Every Go implementation — loaded on demand |
| `recipes/` | 15 runnable procedures with tests and observable scenarios: REST API (chi), CLI (cobra / minimal / interactive), SQLite (sqlc), PostgreSQL (pgx), worker pool, graceful shutdown, JWT + session auth, config (koanf/viper), slog+expvar observability, desktop service | Copy the shape, adapt, verify with the probe |
| `knowledge/` | 195+ sourced patterns, anti-patterns, security/performance/observability guidance, stdlib pointers, architecture decisions, 44 library fiches with decision sections | Choosing libraries, avoiding pitfalls, understanding Go design |
| `snippets/` | Focused, executable views (bounded worker, error wrapping, JSON HTTP) linked to their canonical source | A small, tested fragment instead of a full recipe |
| `templates/` | 3 real MIT-sourced project bases (REST API, CLI, worker pool), each with a machine-checked `structure.md` reading map | Starting a new project from a proven, pinned base |
| `probes/` | 16 executable product evaluations with explicit PASS verdicts and exit codes | Verifying the kit actually behaves as claimed |
| `router/` | Generated read-only semantic index + routing-quality contract | Routing any task to the right resource without scanning the tree |
| `ui-kit/` | Pinned desktop UI SDK for **Wails** projects: shadcn/ui components, interface rules, screen patterns, review skills — inert for plain Go projects | Wails/React interface work only |
| `.pi/` | Prompts (`/goak-help`, `/checklist-api`, `/checklist-release`, `/workflow-memory`), workflow skills (`spec-driven-dev`, `deep-discuss`, `workspace-init`, `go-code-review`, …), routing extensions, onboarding banner, and the shipped **user guide** | Everything the agent does in a project |

## Installation — one command

```sh
curl -fsSL https://raw.githubusercontent.com/TheophileBaudouin/GoAK/v2.7.4/install.sh | sh -s -- go-agent-kit
```

Installs the complete product into `./go-agent-kit` (default pinned ref
`v2.7.4`). The installer downloads the release tarball, extracts only the
consumable `KitV2/` tree (never the metaproject), and verifies the install
with the product validator — a missing toolchain is reported `PARTIAL`, never
`PASS`.

Options:

- `GAK_REF=main` — install the latest branch head instead of the pinned tag;
- `GAK_REF=<tag|commit>` — any pinned install;
- `GAK_SKIP_VERIFY=1` — skip the post-install verification step.

## Get started

```sh
cd go-agent-kit
pi                          # loads AGENTS.md, .pi/prompts, .pi/skills, the router
/goak-help                  # the agent reads the shipped user guide and explains the kit
```

1. **Verify the install** — `python3 tools/validators/validate-kitv2.py`
   (product structure) and `bash probes/run.sh` (observable scenarios, needs a
   Go toolchain). Both green means the kit works.
2. **Initialize the project foundation** (recommended for a new project,
   before the first feature) — run the `workspace-init` skill: one day-0
   session that decides the kernel/modules boundary, pins the stack, and
   writes `workspace/` (CONSTITUTION.md, ARCHITECTURE.md) plus a "Project
   Foundation" section in your `AGENTS.md`.
3. **Start a feature** — routing is mandatory: call `search_kit_resources`
   with the task's technical terms and read the top matching resource (rule,
   recipe, pattern, or catalog) **before writing code**. Follow the
   `kit-resource-routing` skill for query formulation.

### Workflow selection

| Task | Use |
| --- | --- |
| Ordinary Go work | Route, then plan and implement directly |
| Large-scale transformation (rewrite, migration, overhaul, whole-project refactor) | **`spec-driven-dev`** — seven-phase pipeline (intent, S.U.P.E.R deep analysis, grounded refinement, delivery batches, MASTER.md progress, adaptive control, archive), local-only |
| Structured problem analysis / design decision | **`deep-discuss`** — multi-round discussion before proposing anything |
| Code review | **`go-code-review`** (findings-first) + `/checklist-api`, `/checklist-release` |
| New project, before the first feature | **`workspace-init`** — kernel-first day-0 foundation |
| Wails/React interface work | `search_ui_kit_resources` + `ui-kit/AGENTS.md` (never `search_kit_resources`) |
| "How do I use this kit?" | `/goak-help` — the agent reads `.pi/docs/GOAK.md` |

## What the kit guarantees

- **Sourced, evidence-based knowledge.** Every rule and pattern cites primary
  sources (official docs, RFCs, maintained reference implementations). Every
  catalog fiche records verified sources with dates; negative claims are
  confirmed by at least two sources.
- **Composition over duplication.** One canonical answer per question; layers
  point to each other, never copy. A recipe composes patterns and snippets;
  a template assembles recipes — each truth lives once.
- **Deterministic validation.** The product gate (validators, Go toolchain,
  probes, routing scenarios) is the only mechanical proof; observable probes
  are the only behavioral proof. Never claim an unexecuted scenario passed.
- **Routing quality you can trust.** The ranking of `search_kit_resources` is
  contract-tested under the **real runtime scoring** — the gate verifies
  exactly what the agent sees, and quality scenarios must be able to fail.
- **Self-contained.** The consumer kit ships its own user guide, onboarding
  banner, offline source bundle (Effective Go), and validation tools. It works
  with no external documentation and no network.
- **Stable contracts.** The published frontmatter schema and the product
  manifest are immutable; breaking changes require a version increment, a
  migration, and updated evaluations.

## Repository structure

| Path | What it is |
| --- | --- |
| `KitV2/` | The standalone consumable product — the only part that is installed |
| `.agent/` | Metaproject control plane: governance contracts (`.agent/kit-governance/`), validators, router builder, source registry — **never installed** |
| `.pi/memory/` | Metaproject memory — **never installed** |
| `docs/` | Metaproject plans, research, raw evidence — **never installed** |
| `install.sh` | The one-command bootstrap installer (tree-based, pinned to the latest release) |

## Validation

From the installed kit root, with `PATH="$PATH:$(go env GOPATH)/bin"`:

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

Report the gate with exactly one status: **PASS** (all checks succeeded),
**FAIL** (at least one failed), or **PARTIAL** (a required tool is missing —
never present PARTIAL as PASS). The shipped CI workflow
(`templates/_kit-ci-workflow.yml`) additionally enforces an aggregate coverage
floor of 70% on the testable library surface; the local gate does not.

## Current release — v2.7.4

- **Project-memory v2**: all consumer memory surfaces now match the
  platform's project-memory extension v2 — five files (`Brief`, `Progress`,
  `Gotchas`, `Decisions`, `Agent`) auto-bootstrapped when missing, the
  `memory_read` tool (omit `file` = all memory) as the only memory tool,
  direct edits under the `memory-writing` skill, and refactoring only via
  the `memory-refactor` skill. The stale "Decisions.md is not created by
  the bootstrap" premise is gone from every instruction surface, and the
  product validator now enforces the contract with `check_memory_contract`
  (no removed-tool residue in shipped files, v2 facts required in the
  memory instruction surfaces). Kit-audit gained dimension C19
  (memory-system consistency). Migration plan and decision:
  `docs/plans/2026-08-08-project-memory-v2-migration.md`, D-2026-08-08-22.

## Version history

- **v2.7.3** — installer default-ref alignment (re-pinned after the v2.7.2
  withdrawal), consumer `AGENTS.md` mandatory top blocks with mechanical
  enforcement, kit-audit fixes (KVA-001…005), clean diagnostics, full
  README.
- **v2.7.2** — withdrawn tag: shipped without the installer default-ref bump
  (would install v2.7.1); replaced by v2.7.3.
- **v2.7.1** — installer default-ref fix (the initial v2.7.0 tag shipped an
  installer still pulling v2.6.0); onboarding banner Get Started also points
  to `/workflow-memory`.
- **v2.7.0** — first cut of the release (superseded by v2.7.1 for the
  installer default-ref fix).
- **v2.6.0** — ui-agent-kit integration: pinned `ui-kit/` SDK zone
  (ui-agent-kit 0.1.1, agent chat + assistant-ui component families), single
  skill registration point in `.pi/settings.json`, separate UI routing corpus
  (11 quality scenarios), hardened re-sync helper with checksum-enforced
  AGENTS.md section.
- **v2.5.0** — routing-guarantee release: 72 product skills, 15 runnable
  recipes, 3 sourced MIT templates (REST, CLI, worker), 3 verified snippets,
  278 indexed resources, 22 routing-quality scenarios under the real runtime
  scoring, offline source retrieval, and the structure.md reading-map
  mechanism (charter Layer 5.1).
- **v2.2.x** — semantic resource router release: 206 indexed resources, the
  native `search_kit_resources` tool, and the improved installer with a
  TTY spinner, retry, and a verified install summary.

## Roadmap

The canonical **`gak` CLI** (`init`, `update`, `doctor`, `validate`, `remove`,
`info`), the published Go module, and the formal release pipeline (checksums,
provenance, atomic updates) remain on the roadmap; `install.sh` is the interim
installer for the tree-based version.

## License

The sourced templates each carry their own **MIT** LICENSE + ATTRIBUTION.md
(source, pinned version, adaptations, technical scope); the pinned `ui-kit/`
zone is MIT (see `ui-kit/PIN.md`). Kit-authored content is provided under the
repository's terms — see each artifact's metadata for provenance.
