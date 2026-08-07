# Go Agent Development Kit (GoAK)

A Go development kit for code agents: sourced rules, runnable recipes,
verified snippets, MIT project templates, library catalogs, and executable
probes — organized as a typed knowledge graph (not a snippet folder, not a
framework). The consumable product is `KitV2/`; the repository root is the
metaproject that governs it (charter, source registry, plans, evidence).

## Installation — one command

```sh
curl -fsSL https://raw.githubusercontent.com/TheophileBaudouin/GoAK/v2.6.0/install.sh | sh -s -- go-agent-kit
```

Installs the product into `./go-agent-kit` (default pinned ref `v2.6.0`;
override with `GAK_REF=main` or `GAK_REF=<commit>` for another reference).
The install is verified by the product validator; a missing tool is reported
`PARTIAL`, never `PASS`.

## Getting started

```sh
cd go-agent-kit
pi                                  # loads AGENTS.md, .pi/prompts, .pi/skills
pi --approve                        # non-interactive: approve the trusted project
bash probes/run.sh                  # executable product probes (Go toolchain required)
```

Routing is built in: the `search_kit_resources` tool (`.pi/extensions/`)
routes any task to the relevant rules, recipes, patterns, and catalogs from a
read-only index — no tree scanning. The `kit-resource-routing` skill explains
when and how to call it. For large-scale transformations (rewrite, migration,
overhaul, refactor), the `spec-driven-dev` workflow skill runs a seven-phase
pipeline (intent, S.U.P.E.R analysis, decomposition, adaptive control,
archive) — local-only, no GitHub dependency. `deep-discuss` handles structured
problem analysis.

## Product validation gate

From `KitV2/` (or the installed directory), with
`PATH="$PATH:$(go env GOPATH)/bin"`:

```sh
python3 tools/validators/validate-kitv2.py
KITV2_STRICT_CATALOG=1 python3 tools/validators/validate-kitv2.py  # catalog changes
go mod tidy && go mod verify
test -z "$(gofmt -l .)"
go vet ./...
golangci-lint run ./...
go test -race ./...
gosec ./...
govulncheck ./...
bash probes/run.sh
```

The CI gate (metaproject + `templates/_kit-ci-workflow.yml`) additionally
enforces an aggregate coverage floor of 70% on the testable library surface;
the local gate does not.

## Repository structure

- `KitV2/` — the standalone consumable product: `rules/`, `recipes/`,
  `snippets/`, `templates/` (MIT-sourced projects, each with a machine-checked
  `structure.md` reading map), `knowledge/` (patterns, anti-patterns,
  security, performance, catalogs, stdlib pointers), `probes/` (15 executable
  observable scenarios), `tools/offline/` (offline resolver + pinned Effective
  Go bundle), `tools/generators/` (deterministic structure.md drift gate),
  `.pi/` (settings, prompts, workflow skills, routing extension), `router/`
  (generated read-only index + routing-quality contract).
- `.agent/`, `.pi/memory/`, `docs/` — metaproject governance only, never
  installed for a consumer.
- `install.sh` — bootstrap installer for the tree-based version.

## Status

**v2.6.0** — the ui-agent-kit integration release: the pinned `ui-kit/` SDK
zone re-pinned to ui-agent-kit 0.1.1 (agent chat + assistant-ui component
families), the UI skills registered through the root `.pi/settings.json`
(single registration point, inert by description for non-Wails projects),
the root `AGENTS.md` merged with the SDK instructions (checksum-enforced at
each re-sync), a separate UI routing corpus with 11 quality scenarios, the
hardened `sync-ui-kit-from-upstream.sh` re-sync helper, and zero pi-lens
blocking errors in the shipped extensions.

**v2.5.0** — the routing-guarantee release: 72 product skills, 15 runnable
recipes, 3 sourced MIT templates (REST, CLI, worker), 3 verified snippets,
278 indexed resources, 22 routing-quality scenarios verified under the real
runtime scoring, offline source retrieval, and the structure.md mechanism
(charter Layer 5.1). The canonical `gak` CLI (`init`, `update`, `doctor`,
`validate`, `remove`, `info`), the published Go module, and the formal
release pipeline remain on the roadmap; `install.sh` is the interim installer.
