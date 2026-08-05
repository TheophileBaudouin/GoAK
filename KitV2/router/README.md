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

## Usage

The agent calls the native `search_kit_resources` tool with a technical query
(e.g. "bounded worker pool with context cancellation"). The tool returns a
compact top-K: `kind`, `id`, path, matched terms (the match reason), and a
short description. The `kit-resource-routing` skill (`.pi/skills/`) explains
when and how to use it.

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
