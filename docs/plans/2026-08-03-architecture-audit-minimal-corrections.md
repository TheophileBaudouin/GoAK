# Architecture audit and minimal corrections — 2026-08-03

## Goal

Audit the existing Go Agent Kit against the requested cognitive-OS target and
apply only corrections that close verified architectural defects. Preserve the
existing `.agent/` control plane, `.pi/` runtime, offline resolver, source
bundle, graph schema, and validation contracts.

## Audit result

| Requirement | Canonical owner | Status | Decision |
| --- | --- | --- |---|
| Offline pkg.go.dev / Effective Go / toolchain retrieval | `KitV2/tools/offline/`, bundle, `knowledge/stdlib/` | Implemented | No redesign |
| Deterministic retrieval | `tools/offline/search.go`, `context-policy.yaml` | Implemented and tested | No change |
| Lazy loading and hierarchical L0/L1/L2 retrieval | resolver, bundle manifest/index/blob store, retrieval skill | Implemented | No change |
| Content-addressed storage | `tools/offline/bundle/blobs/` | Implemented for bundled content | No change |
| Typed graph and explicit relationships | `.agent/cognitive/`, product knowledge metadata | Implemented, with product-local target gap | Add missing product graph objects |
| `.agent/` control plane / `.pi/` runtime separation | root `.agent/`, `KitV2/.pi/` | Implemented and validator-enforced | No change |
| Source transformation statuses | `.agent/cognitive/source-catalog.yaml` | Implemented; proposed targets honest | No speculative materialization |
| Go toolchain capabilities | `knowledge/stdlib/toolchain-offline.yaml` | Represented and validated by offline probe/gate | No change |
| Progressive disclosure | Pi skills + resolver budgets | Implemented | No rolling-summary engine; not required by current contract |
| Atomic retrieval | resolver result per query | Implemented | Atomic refresh remains procedural and `gak` is deferred |
| Context budget | L0/L1/L2 and retrieval budgets enforced; always-loaded 1,500-token target is policy-only | Partial by design | Do not pretend to meter external agent context |
| Subagent contracts | `.agent/cognitive/subagent-contracts.yaml` | Implemented | No change |
| Validation and memory | validators, probes, evidence, `.pi/memory/` | Implemented | Update audit record only |

## Verified deviations

1. Product knowledge relationships referenced active capability/evaluation IDs
   that were resolvable only through the metaproject catalog. A standalone
   product graph should declare its own materialized IDs.
2. The product validator checked relationship syntax but did not resolve stable
   relationship targets within the standalone product graph.
3. A shipped authoring template referenced a nonexistent metaproject research
   file, and product probe documentation referenced metaproject-only paths.
4. `rules/*.md` contains empty navigation stubs while canonical rule bodies are
   under `rules/**/SKILL.md`. They are a navigation hazard, but deletion is
   deferred because product-content deletion requires an explicit archive/
   checkpoint decision; no replacement knowledge is needed.
5. The idiomatic implementation reference repeated universal rule content.
   The repeated constraints are removed from the reference; the universal core
   rule remains canonical.

## Minimal correction set

- Add two product graph metadata objects for the already-shipped capability and
  evaluation; do not add new implementation or duplicate source bodies.
- Make the standalone validator resolve graph relationship IDs against the
  product's YAML object set while permitting external URLs for `references`.
- Replace broken product documentation links with self-contained wording.
- Replace duplicated universal-rule prose in the on-demand reference with a
  canonical-rule pointer and retain only decisions unique to that reference.
- Leave empty stubs, manifest capability deduplication, proposed toolchain
  artifacts, progressive summary tooling, and `gak` CLI unchanged.

## Dependencies

1. Add product graph objects.
2. Add product-local relationship resolution.
3. Correct documentation/reference duplication.
4. Run validators, tests, probes, and fresh review.

## Risks

- Activating existing materialized IDs could be mistaken for adding new
  capabilities; the records are metadata for already-shipped resolver/probe
  behavior and contain no duplicated body.
- Product-local relationship checking could reject URL references; URLs are
  explicitly allowed only for `references`.
- Removing duplicated prose could lose useful guidance; the universal rule is
  still loaded from its canonical core skill, while the reference retains its
  distinct boundaries and measurement guidance.
- No VCS exists at repository root; evidence remains checksum-backed and VCS
  status stays PARTIAL.

## Done

- No existing correct architecture replaced.
- No new dependency, manifest contract, Pi setting, or frontmatter schema.
- Product graph is internally resolvable for stable IDs.
- Product documentation has no broken metaproject-only references.
- Full validation and offline probes remain green.
