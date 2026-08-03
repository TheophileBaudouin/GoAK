# Cognitive OS reconciliation — 2026-08-03

## Goal

Reconcile the requested Go Agent Kit cognitive-OS design with the existing
metaproject and standalone `KitV2` product without introducing parallel
knowledge surfaces. The existing architecture already provides the core
Retrieve → Reason → Generate → Validate → Remember protocol, typed graph
schema, source catalog, bounded offline resolver, toolchain mappings, product
bundle, Pi workflows, probes, and subagent contracts. This wave closes only
live integrity and validation gaps.

## Target architecture

- **Control plane:** root `.agent/` owns graph governance, source admission,
  retrieval policy, subagent contracts, evaluation governance, and validators.
- **Consumable runtime:** `KitV2/` owns self-contained product artifacts,
  native `.pi/` projections, product checks, probes, and the pinned offline
  source bundle. It never depends on root `.agent/` at runtime.
- **Knowledge graph:** stable IDs and explicit relationships are authoritative;
  directories are navigation only. Source bodies are stored once, addressed by
  pin/checksum, and transformed into narrow operational artifacts only when a
  repeated decision warrants promotion.
- **Retrieval:** metadata-first L0/L1 routing precedes bounded L2 content. The
  default is offline and deterministic; absent content returns miss/blocked,
  never fabrication. Embeddings, wall-clock values, and model ranking are not
  authorities.
- **Composition:** Rules constrain; Recipes order work; Patterns select
  designs; Snippets implement tested fragments; Templates assemble; Capabilities
  expose abilities; Evaluations measure behavior; Sources provide evidence;
  Memory stores durable project facts. No layer copies another layer's body.

## Source transformation policy

- `pkg.go.dev` remains a Source consulted by exact package/symbol unit. Its
  operational projection is the offline package-lookup Capability plus the
  offline retrieval Evaluation; complete generated HTML/API pages remain
  source-only and are never injected wholesale.
- Effective Go remains a pinned, content-addressed Source. Only stable,
  source-backed decisions become narrow Rules or Patterns with target Go
  version and provenance. Its complete prose remains retrievable source
  content, not a duplicated rulebook.
- Official toolchain documentation becomes native Capabilities and Evaluations
  selected by workflow: formatting, tests, vet, benchmarks, fuzzing, race,
  pprof, and trace. Tool implementation internals remain Source-only. The
  shipped product currently materializes only the offline lookup capability and
  offline-source evaluation; forward targets are explicitly proposed until a
  consumer and artifact exist.

## Context contract

- Always loaded: task/constraints, target Go version, graph router metadata,
  and applicable permanent Rules; hard ceiling 1,500 tokens.
- L0: IDs, pins, checksums, statuses, and routing metadata; ≤4 KiB.
- L1: sorted unit index and exact candidates; ≤16 KiB.
- L2: selected content-addressed source/artifact excerpt; default ≤2,000
  tokens, excerpt ≤512 tokens, explicit full retrieval ≤8,000 tokens.
- L3 is exploratory ranking only and never authoritative. Retrieval order is
  deterministic (exactness, then lexical unit ordering). Same query/cache gives
  byte-identical output.

## Subagent workflow

Planner orders dependencies and decision boundaries; Scout maps canonical owners
and duplicate risk; Web Research verifies primary sources and pins; Knowledge
Engineer transforms evidence into graph candidates; Context Engineer defines
budgets and query/result contracts; Go Architect chooses the smallest
stdlib-first implementation; Validation Engineer supplies executable gates and
observable scenarios; Documentation Engineer writes routing documentation only.
Each receives explicit inputs and returns structured outputs. One writer owns a
worktree; readers/reviewers do not edit.

## Live reconciliation

1. Re-verify the drift matrix before changes.
2. Canonicalize `race` vocabulary between catalog and product metadata.
3. Add status/materialization metadata for transformation targets: only the
   two shipped targets are active; unmaterialized capability/evaluation targets
   remain proposed.
4. Remove product relationships to proposed/undeclared evaluation IDs.
5. Extend the metaproject validator with target-status, materialization, and
   vocabulary checks.
6. Extend the standalone validator with self-contained knowledge metadata and
   relationship checks.
7. Keep the manifest capability-list duplication approval-gated; do not remove
   it in this wave without owner approval because it changes the manifest
   contract.
8. Document the cognitive validator in the metaproject validation gate.
9. Run deterministic validators, Go checks, and `GOPROXY=off` probes; record
   raw evidence and obtain fresh read-only review.

## Risks and mitigations

- Forward graph declarations may be mistaken for active artifacts: explicit
  `proposed` target status plus validator enforcement.
- Product and metaproject validators may drift: product checks remain
  structural/self-contained; cross-boundary integrity remains metaproject-only.
- Toolchain vocabulary can drift: compare product capability names to the
  catalog's canonical retrieval units.
- No Git repository exists: evidence is retained under `docs/evidence/`, but
  VCS-versioned evidence remains PARTIAL as required by memory.
- Scope creep into `gak`, multi-language generalization, new dependencies,
  frontmatter, or Pi settings is deferred.

## Definition of done for this wave

- All changed metadata parses and has only declared graph relationships.
- Pre-fix validator failure demonstrates new checks are active; post-fix checks
  pass.
- Product remains self-contained and its existing skill count is unchanged.
- Full applicable validation and offline probes pass, with raw evidence saved.
- Fresh-context reviewer confirms no duplicate surface, dangling target, or
  metaproject dependency was introduced.
