# Router — semantic routing index (read-only)

`router/` ships the kit's routing index: a **generated artifact** that lets an
agent get directions to the relevant resources (rules, recipes, catalogs,
patterns, anti-patterns, sources, snippets, prompts, skills) without loading
the kit into context.

## What it is

- `index.json` — the indexed resources: `id`, `kind`, `path` (kit-relative
  path), `description` (short, hand-written in the frontmatter), `tags`,
  `terms` (precomputed search tokens).
- `meta.json` — provenance: kit version, `index_sha256` (integrity), per-type
  counts, stopword list (single source shared with the runtime).

The index is a **router only**: it does not contain the kit file content. The
source of truth always stays the files themselves — every entry points to a
real path to read.

## Rules

- **Never edit `index.json` or `meta.json` by hand.** They are generated
  artifacts; any modification is detected by the validator
  (`validate-kitv2.py` verifies the hash and the complete coverage) and
  blocks the release.
- **Read-only at runtime**: the `search_kit_resources` tool
  (`.pi/extensions/kit-resource-router.ts`) reads the index, never writes it,
  never modifies the kit.
- **Never rebuild on the consumer side**: the index is regenerated before
  each kit release; you have nothing to do.

## Routing-quality contract (`scenarios.json`)

`scenarios.json` is an **authored** contract (not generated): a list of
realistic task intents (`query`) mapped to the kit resources that MUST
surface in the top-K (`expect`, default top-5, `top` overrides) plus
off-domain queries that must be rejected (`offDomain: true`, empty-over-noise
rule). Every expected id must exist in the index — `validate-kitv2.py`
enforces this schema and linkage check on every gate.

The ranking verification itself runs in the **metaproject gate** with the
REAL runtime scoring: the gate runner imports `kit-resource-router-scoring.ts`
(the exact module the tool uses), so the gate and the agent cannot diverge.
The runner, its sources, and the Node runtime requirement (≥ 23.6) are
metaproject-only and are **not shipped** with this product — the installed
kit is verified by `validate-kitv2.py` (schema + id linkage) and ships the
index read-only. Metaproject maintainers run the ranking gate from the
repository root with the metaproject runner (`run_scenarios.mjs`); exit 0
means the routing contract holds.

The gate verifies the scoring layer: for off-domain scenarios it asserts
the `offDomain` guard fires (the tool then renders the empty-result
message); the message rendering itself stays a runtime behavior.

A skill with weak terms, a duplicate question, or a misleading description
degrades this gate — that is the tripwire that keeps routing precise as the
kit grows.

## Usage

The agent calls the native `search_kit_resources` tool with a technical query
(e.g. "bounded worker pool with context cancellation"). The tool returns a
compact top-K: `kind`, `id`, path, matched terms (the match reason), and a
short description. The `kit-resource-routing` skill (`.pi/skills/`) explains
when and how to use it.

> `kind` is the **routing resource class**, not the charter artifact kind.
> The index groups resources by the surface an agent routes to (recipe,
> rule, pattern, anti-pattern, catalog, source, snippet, prompt, skill,
> template); a catalog-layer YAML pointer declares `kind: Source` in its own
> metadata yet routes as class `catalog`. The artifact file itself stays the
> authority for its charter kind.

## Schema

```json
{
  "schema": 1,
  "resources": [
    {
      "id": "recipe-worker-pool",
      "kind": "recipe",
      "path": "recipes/recipe-worker-pool/SKILL.md",
      "description": "Bounded concurrent fan-out in Go…",
      "tags": ["concurrency", "errgroup"],
      "terms": ["bounded", "concurrent", "errgroup"]
    }
  ]
}
```
