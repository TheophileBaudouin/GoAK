# Cognitive control plane

This directory is the metaproject's design-time cognitive layer. It is not a
consumer runtime and is never copied into `KitV2/`.

## Protocol

Agents follow:

```text
Retrieve -> Reason -> Generate -> Validate -> Remember
```

1. Classify the task and target Go/toolchain version.
2. Query graph metadata before reading any artifact body.
3. Load only the selected Rule, Capability, Recipe, Pattern, Snippet, or
   Evaluation and the smallest cited Source unit.
4. Generate by composition; never copy a source document or duplicate a
   canonical artifact body.
5. Run the selected executable Evaluation and observable scenario.
6. Record only durable decisions, progress, gotchas, and evidence pointers.

## Files

- `graph-schema.yaml` — stable IDs, required metadata, and graph relations.
- `source-catalog.yaml` — the two critical source-registry sections and their
  transformations into graph artifacts.
- `context-policy.yaml` — progressive disclosure, hard budgets, and the fixed
  offline retrieval ladder.
- `subagent-contracts.yaml` — atomic roles with explicit inputs and outputs.
- `../validators/validate-cognitive.py` — deterministic metadata, relationship,
  and standalone-product pointer checks.

The graph is authoritative. Directory names are navigation only. The shipped
product bundle is validated by `evaluation:go:offline-source-retrieval`; the
metaproject keeps governance and source admission, while KitV2 keeps the
standalone runtime data and resolver.

## Boundary

The metaproject owns source admission, pins, retrieval governance, evaluations,
and design history. `KitV2/` owns the standalone consumable product. Product
artifacts may reference a Source only when the complete source manifest and
resolver required to resolve it ship with the same product release. A dangling
pointer into this directory is invalid.
