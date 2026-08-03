# KitV2 migration plan

> **SUPERSEDED (2026-08-03):** The ownership and Pi-native layout in this
> historical plan were corrected by `docs/plans/2026-08-02-kitv2-boundary-correction.md`.
> Retain this file as the original migration record; do not execute its old
> `.agent/` or `evaluations/` layout.

## Goal

Create a complete, additive `KitV2/` beside the untouched `kit/` v1. KitV2
organizes the kit as an agent-native development system with explicit rules,
knowledge indexes, recipes, metadata-bearing snippets, project templates, and
native Pi resources. This original goal is retained for history; the boundary
correction removed metaproject governance from the product.

## Context

The current `kit/` already contains the authoritative v1 registry, Pi prompts,
skills, probes, validation script, and Go examples. The workspace has no Git
repository. Therefore v1 remains untouched as the rollback/archive source; no
claim of VCS-backed rollback is made.

## Constraints

- Do not delete, move, or rewrite `kit/`.
- Preserve all v1 modules and map every one into KitV2.
- Keep one canonical copy inside KitV2; indexes link to canonical modules rather
  than duplicating their bodies.
- Preserve the published v1 frontmatter contract in migrated SKILL.md files.
- Add no third-party dependency.
- Mark templates honestly when they are catalogs/checklists rather than
  runnable application projects.
- Provide deterministic validation and an observable migration audit.

## Target layout

```text
KitV2/
├── AGENTS.md
├── manifest.yaml
├── rules/                 # canonical rules migrated from core/rules and registry/rules
├── knowledge/             # indexes and sourced explanations; no duplicate rule bodies
├── recipes/               # canonical recipe modules and tests
├── snippets/              # metadata + small canonical examples, linked to recipes
├── templates/             # template contracts and status-bearing project templates
├── probes/                # copied consumer probes and runner
├── scripts/               # deterministic V2 validator and migration audit
└── go.mod                 # testable migrated Go examples
```

## Migration map

- `kit/core/**` and `kit/registry/rules/**` → `KitV2/rules/**`.
- `kit/registry/recipes/**` → `KitV2/recipes/**`.
- `kit/registry/libraries/**` and `kit/registry/reference-projects/**` →
  `KitV2/knowledge/catalogs/**`, retaining their original SKILL.md contracts.
- `kit/.pi/prompts/**` and `kit/.pi/skills/**` → `KitV2/.pi/prompts/**` and
  `KitV2/.pi/skills/**`; V2 keeps native Pi settings pointing at its
  rule/recipe/knowledge roots.
- `kit/templates/**` → `KitV2/templates/_kit/**`.
- `kit/probes/**` → `KitV2/probes/**`.
- `docs/evidence/**` is not copied into the product; V2 records evidence paths
  and writes new evidence under the metaproject docs tree.

## Canonical-source rules

- Rule and recipe bodies live only in `rules/` and `recipes/` inside V2.
- Knowledge catalogs contain links, rationale, admission status, and source
  pointers; they do not restate module bodies.
- Snippet records contain a stable id, purpose, context, dependencies,
  Go-version floor, tags, complexity, source module, example, and check.
- Templates contain a contract and a status. A template is not called
  production-ready until its own runnable scenario and validation evidence exist.
- Metaproject decisions, memory, and evaluation governance remain at the root;
  KitV2 ships product content and native Pi resources only.

## Validation

1. `python3 KitV2/tools/validators/validate-kitv2.py` validates structure, manifest,
   metadata, migrated-module coverage, memory hygiene, and template shape.
2. `bash KitV2/probes/run.sh` runs all four consumer probes.
3. From `KitV2/`, run `go mod tidy`, `go mod verify`, output-gated `gofmt`,
   `go vet`, `go test -race`, and available security/lint tools.
4. Run a fresh-context review of the V2 tree before claiming completion.

## Non-goals

- Deleting v1.
- Implementing Claude/Codex/Gemini adapters.
- Claiming all seven project templates are complete applications in this first
  migration wave.
- Adding a runtime workflow engine, external dependencies, or auto-trust.
- Treating static checks as proof of product behavior.

## Done when

- Every v1 module is present in the migration map and represented in V2.
- The V2 validator passes and reports the migration counts.
- All four probes pass.
- The V2 Go gate passes as far as the local toolchain permits, with unavailable
  tools reported explicitly.
- A fresh review reports no blockers; remaining gaps are labelled PARTIAL.
