# Go Agent Development Kit

KitV2 is the standalone consumable Go agent kit.

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
| `.pi/` | Native Pi settings, prompt templates, skills, and the `search_kit_resources` extension loaded after trust | `.pi/README.md` |

If two files answer the same question, keep one canonical answer and replace the other with a pointer. Catalog updates require fresh primary-source research and dated `Verified sources`; fenced Go examples must handle returned errors or be marked `illustrative`. The source registry never overrides the kit charter or these rules; source-derived content remains subject to evidence and validation gates.

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

The kit does not claim to cover: full desktop-application wiring (Wails), TUI development beyond the kit's interactive Bubble Tea recipe, Pi discovery internals, or non-Go domains — check the catalog and the router before expecting a kit resource for a technology.

Always preserve errors, cancellation, input validation, and observable evidence. Ask before adding dependencies or changing the manifest contract. Never claim an unexecuted scenario passed or treat static checks as proof of user intent.
