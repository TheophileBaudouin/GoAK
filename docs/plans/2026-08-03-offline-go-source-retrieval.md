# Offline Go Source Retrieval and Cognitive Architecture Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make the Go Agent Kit an offline-first cognitive system that retrieves only the official Go knowledge required for a task and validates generated code deterministically.

**Architecture:** The metaproject `.agent/` owns the cognitive protocol, source admission, graph governance, and evaluation methods. `KitV2/` remains the standalone consumable product and exposes only product-safe native `.pi/` resources plus pointer-only source metadata. Official Go documentation is represented by local toolchain/module capabilities and pinned source records, never by wholesale copied documents.

**Tech Stack:** Go standard library, `go doc`, `go help`, GOROOT/GOMODCACHE, content-addressed files, YAML/JSON manifests, existing Python validators, Pi-native `.pi/` prompts and skills.

---

## 1. Scope and authority

This plan implements the design task recorded in `.pi/memory/Progress.md` and is subordinate to `KIT_CHARTER.md`.

The strict source registry entries being integrated are:

1. **Cœur du langage Go**: `pkg.go.dev` and Effective Go.
2. **Outils officiels Go**: gofmt, go test, go vet, benchmarks, fuzzing, race detector, pprof, and trace.

The registry is an admission list, not a license to copy source content. The charter remains the process authority. No new artifact kind, dependency, public metadata contract, or product capability counter is introduced by this design.

### Boundary decision

- Root `.agent/` is the metaproject cognitive control plane. It is the canonical home for source pins, retrieval protocol, graph governance, subagent contracts, and evaluation governance.
- `KitV2/` is the standalone consumable product. It must not depend on root `.agent/` files at runtime and must not ship metaproject memory, decisions, or evaluation governance.
- Product-side content uses pointer-only source metadata and native `.pi/` workflows. A future distributable offline bundle must copy a **complete, self-contained** source manifest and index into the product in one atomic release; dangling pointers are forbidden.
- The first implementation wave is therefore design plus source-routing metadata. The fetcher/query engine is a dependent Phase 2 change, not silently added to the current product contract.

This resolves the hidden-dependency risk identified during review: `KitV2/tools/offline/` may not read `.agent/sources/offline/`.

---

## 2. Target architecture

```text
User task
   |
   v
Intent + constraints + target Go version
   |
   v
L0 graph router (metadata only; always small)
   |
   +--> select Rules (permanent constraints)
   +--> select Capability (stdlib/tooling ability)
   +--> select Recipe (ordered procedure)
   +--> select Pattern (design choice)
   +--> select Evaluation (acceptance evidence)
   |
   v
L1 deterministic index: source/unit/pin/checksum
   |
   +--> L2 local source store (content-addressed, immutable)
   +--> GOROOT: go doc / cmd source / go help
   +--> GOMODCACHE: module docs already downloaded
   |
   v
Bounded evidence excerpts
   |
   v
Reason -> Generate -> Validate -> durable Memory update
```

The graph is authoritative. Directories are navigation and packaging only. Every object has one responsibility and explicit relationships.

### Cognitive loop

1. **Retrieve**: classify the task, query the graph by exact identifiers/tags, then retrieve the smallest source unit needed.
2. **Reason**: compare the retrieved evidence with applicable Rules, selected Pattern, and project constraints. Record unresolved choices as a Decision Record, not as hidden context.
3. **Generate**: compose a Recipe from Rules/Patterns/Snippets/Templates; do not copy source documents or duplicate a canonical body.
4. **Validate**: execute the selected Evaluation and observable scenario; static checks are evidence, not proof of behavior.
5. **Remember**: persist only durable decisions, progress, gotchas, and evidence pointers. Never persist transcripts or raw command output in product content.

Equivalent input, pinned sources, same toolchain, and same cache state must yield the same retrieval ordering and generated artifact inputs.

---

## 3. Knowledge graph contract

### 3.1 Stable identity

Use a namespace and semantic unit, never a path-only identity:

```text
rule:go:errors-explicit
recipe:go:validate-package
pattern:go:bounded-concurrency
snippet:go:testing-table-driven
capability:go:toolchain-test
source:go:pkg-doc:net/http
source:go:effective-go
source:go:toolchain:gofmt
 evaluation:go:package-gate
memory:consumer:<project>:decision:<id>
```

`source` identities are distinct from retrieved blobs. A blob is addressed by SHA-256; `(source_id, unit, pin)` identifies the cited source unit.

### 3.2 Required metadata

Every graph object carries:

```yaml
id: stable-namespace-id
title: human-readable title
kind: Rule | Recipe | Pattern | Snippet | Template | Capability | Evaluation | DecisionRecord | Source | Memory
version: semver-or-schema-version
status: proposed | active | deprecated | rejected
owner: kit-or-metaproject-owner
tags: [go, ...]
go_version: "1.25+"
dependencies: []
last_verified: YYYY-MM-DD
relationships:
  depends_on: []
  uses: []
  implements: []
  references: []
  requires: []
  supersedes: []
  validated_by: []
  generated_from: []
```

Missing relationships are validation failures, not implicit folder relationships.

### 3.3 Composition

```text
Template -> assembles Recipe -> selects Pattern -> uses Snippet
Rule -> constrains all applicable layers
Capability -> exposes a tool/source ability
Source -> supplies evidence
Evaluation -> validates generated behavior
Memory/DecisionRecord -> records durable project history only
```

A source can be referenced by many artifacts, but its content has one canonical storage location. A Rule may summarize a source-derived constraint; it must cite the Source and must not reproduce the source chapter.

---

## 4. Transformation of official sources

| Registry source | Becomes operationally | Remains source-only | Required relation |
| --- | --- | --- | --- |
| `pkg.go.dev` | `Capability` for offline package/symbol lookup; focused `Snippet`/`Recipe` only when a repeated decision is proven; `Evaluation` that runs `go doc`/compilation against the pinned Go version | Full package pages, exhaustive API indexes, generated HTML | Source -> Capability; Recipe/Snippet `references` exact package unit |
| Effective Go | Small, stable `Rule` records for idioms actually used by the kit; focused Patterns such as error handling or package naming; examples may become tested Snippets | Full guide, historical prose, broad style catalogue | Rule/Pattern `generated_from` or `references` Effective Go Source |
| gofmt | `Capability`; mandatory validation step in the formatting Rule/Evaluation | `gofmt` implementation source | Evaluation `uses` capability |
| go test | `Capability`; test Recipe and package quality Evaluation | Full `testing` package docs | Recipe `uses` capability; Evaluation `validated_by` tool output |
| benchmark | `Capability`; performance Evaluation and benchmark Recipe | Full benchmark documentation | Evaluation `requires` benchmark capability |
| fuzzing | `Capability`; opt-in fuzz Recipe and Evaluation with bounded time | Full fuzzing guide | Recipe `uses` capability |
| race detector | `Capability`; concurrency Evaluation and required race command where applicable | Full detector internals | Rule/Evaluation `requires` capability |
| go vet | `Capability`; static-analysis Evaluation | Full analyzer implementation docs | Evaluation `uses` capability |
| pprof | `Capability`; profiling Recipe/Evaluation triggered by measured need | Full pprof implementation/docs | Recipe `requires` capability |
| trace | `Capability`; tracing Recipe/Evaluation triggered by measured need | Full trace implementation/docs | Recipe `requires` capability |

The two critical documentation sources are not treated alike: `pkg.go.dev` is an API lookup surface, while Effective Go is a bounded source of idiomatic decisions. Neither is loaded wholesale.

### pkg.go.dev offline strategy

`pkg.go.dev` has no required offline HTML mirror in the kit. The deterministic equivalent for installed Go APIs is:

- `go doc -short <package>` and `go doc -short <package>.<Symbol>` from the pinned local GOROOT;
- module documentation from the already available GOMODCACHE, verified by `go.sum`/module checksums;
- an optional content-addressed cache populated only by an explicit online refresh command.

If the requested package is unavailable locally and network is disabled, return `blocked` with the exact prerequisite. Never fabricate an API from model memory.

### Effective Go offline strategy

Store one pinned, checksum-verified source unit and a small deterministic unit index. Retrieve headings/sections or bounded excerpts only. Because Effective Go is historical and not actively updated for every current Go release, every derived Rule states its Go version and freshness limitation. Newer official references can supersede a Rule without rewriting the historical Source.

---

## 5. Offline retrieval protocol

Protocol name: `goretrieval/1`.

### Levels

- **L0 manifest**: source IDs, pins, Go version, schema, checksums; target <= 4 KB.
- **L1 indexes**: sorted `unit<TAB>store_reference<TAB>sha256` records; one index per Source; target <= 16 KB per source.
- **L2 store**: immutable raw official content addressed by SHA-256. No edited or generated prose is stored beside raw content.
- **L3 optional ranking**: embeddings may exist for exploratory UX but never control deterministic retrieval or validation.

### Fixed resolution ladder

1. Exact L2 hit.
2. Exact L1 record with missing blob -> `miss`.
3. Local GOROOT/GOMODCACHE resolution (`go doc`, `go help`, source files) with `GOPROXY=off`.
4. Explicit online refresh only when the caller sets `online: true`; verify pin/checksum before install.
5. `blocked` result with prerequisite command.

No automatic network fallback exists. Offline mode is a process contract, not a suggestion.

### Query contract

```json
{
  "protocol": "goretrieval/1",
  "source": "stdlib",
  "unit": "net/http",
  "mode": "exact",
  "limit": 4,
  "budget_tokens": 2000,
  "go_version": "1.26.5",
  "online": false
}
```

Allowed modes are `exact`, `prefix`, and explicit `contains`. Results are ordered by exactness, then lexical unit ID. No timestamps, elapsed time, model scores, or nondeterministic ranking fields affect content.

```json
{
  "protocol": "goretrieval/1",
  "status": "hit | miss | stale | blocked",
  "source": "stdlib",
  "unit": "net/http",
  "matches": [],
  "provenance": {
    "pin": "toolchain-version-or-commit",
    "sha256": "verified-checksum",
    "verifier": "toolchain-local | git-commit | module-sum | dl-json"
  }
}
```

### Context limits

| Item | Default hard limit |
| --- | ---: |
| Always-loaded project context | 1,500 tokens |
| L0 manifest | 4 KB |
| One L1 index | 16 KB |
| One default retrieval response | 2,000 tokens |
| One excerpt | 512 tokens |
| Explicit full response | 8,000 tokens |
| Raw stored document | 512 KB, with a truncation marker |

The agent must load metadata first, then one artifact body, then one referenced source excerpt. It must not load an entire source family, all rules, or all recipes for a task.

### Duplicate prevention

- One `(source, unit)` canonical record.
- Identical content hashes deduplicate physically.
- Product knowledge stores pointers and selection guidance, not source bodies.
- A source-derived Rule must answer a narrower operational question than the Source.
- Any second artifact answering the same question blocks admission until one becomes a pointer.
- Embeddings cannot become the authority for source selection.

---

## 6. Pi-native cognitive layer

The current repository boundary means the metaproject `.agent/` layer is canonical governance, while `KitV2/.pi/` carries the consumable runtime workflow.

### Metaproject `.agent/`

- `instructions.md`: permanent control-plane behavior.
- `sources/`: ordered source registry and future pinned offline manifest/index.
- `cognitive/`: this protocol, graph schema, context budget, and subagent contracts.
- `evaluations/`: evaluation governance and independent review checklists.
- `validators/`: deterministic structural checks.

### Product `.pi/`

- `.pi/settings.json`: native skill discovery only.
- `.pi/prompts/`: task workflows that call retrieval by metadata and preserve the retrieve/reason/generate/validate order.
- `.pi/skills/`: load-on-demand capabilities; each skill points to references rather than embedding large docs.
- `AGENTS.md`: compact permanent product contract; never a second source registry.

Rules that must happen without model discretion belong in validators/scripts. Repeated procedures belong in prompts/skills. API details belong in the offline source index. This prevents a large permanent instruction file.

---

## 7. Subagent workflow contracts

Subagents are readers/reviewers by default. One writer owns a worktree.

| Role | Input | Output | Forbidden |
| --- | --- | --- | --- |
| Planner | user goal, charter, current graph | dependency-ordered plan and decision boundaries | editing product files |
| Scout | repository tree, manifests, validators | canonical-owner map and duplicate risks | inventing architecture |
| Web Research | source IDs and unresolved claims | cited primary-source matrix with freshness/pin facts | promoting doctrine |
| Knowledge Engineer | source matrix, graph schema | candidate artifacts with IDs, relations, provenance, admission status | copying source bodies |
| Context Engineer | artifact inventory, token limits | retrieval tiers, budgets, query/result contract | relevance model as authority |
| Go Architect | approved plan, capabilities | minimal Go interfaces/commands and compatibility notes | new dependency without approval |
| Validation Engineer | artifact contracts | executable checks, observable scenarios, PASS/PARTIAL/BLOCKED evidence | treating compile as behavior proof |
| Documentation Engineer | accepted graph objects | concise routing docs and changelog | duplicating canonical bodies |

Each output is a bounded artifact with source references, unresolved risks, and a deterministic status. Failed subagent work is recorded as unavailable evidence, never silently treated as completion.

---

## 8. Validation workflow

### Per generated Go change

```sh
go mod tidy
go mod verify
test -z "$(gofmt -l .)"
go vet ./...
golangci-lint run ./...
go test -race ./...
gosec ./...
govulncheck ./...
```

Run benchmarks, fuzzing, pprof, and trace only when the selected Evaluation requires them; use bounded durations and record raw output under `docs/evidence/`. `gofmt` must be checked by output, not only by exit status.

### Retrieval-specific checks

- Manifest schema and source IDs parse.
- Every pinned source has a full checksum and verifier.
- L1 units are sorted and unique.
- Every L1 blob exists and hashes correctly.
- Query output is byte-stable for identical inputs/cache state.
- Offline mode performs no network request.
- Missing knowledge returns `miss`/`blocked`, never invented prose.
- Product pointers resolve to a declared Source ID.
- No product knowledge file embeds a whole official source.

### Observable probes

At minimum, an offline probe must demonstrate:

- `go doc -short fmt` succeeds without network;
- `go help testflag` exposes benchmark and fuzz flags; `go help build` documents `-race`;
- the gofmt documentation mapping resolves to `GOROOT/src/cmd/gofmt/doc.go` because `go help gofmt` is not a valid topic on the verified toolchain;
- a missing module returns `blocked` with a prerequisite;
- a toolchain mismatch returns `stale` or `blocked`, never a falsely attributed result.

A product release is `PASS` only when structural checks, mechanical checks, and the observable probe are all green. Missing network, VCS, or toolchain evidence is explicitly `PARTIAL`/`BLOCKED`.

---

## 9. Implementation phases and dependencies

### Phase 0 — Design and admission (this change)

- Record this plan and boundary decision.
- Add the cognitive protocol and graph contracts under root `.agent/cognitive/`.
- Add pointer-only product Source metadata for the three critical registry entries.
- Do not change manifest/capability counters, `.pi/settings.json`, dependencies, or public frontmatter.

Depends on: charter/source inspection and fresh review.

### Phase 1 — Self-contained source manifest

- Choose either a metaproject-only retrieval tool or a fully copied product bundle.
- Define exact pinned Go version, Effective Go commit/path/checksum, and any toolchain-source pins.
- Add deterministic L0/L1 indexes and provenance records.
- Add a finite module-doc allowlist (initially direct KitV2 dependencies only).

Depends on: Phase 0 and owner approval of the boundary/public surface.

### Phase 2 — Stdlib-only retrieval/query tool

- Implement fetch, checksum verification, local resolution, query, and `blocked`/`stale` status.
- Keep it stdlib-only (`encoding/json`, `crypto/sha256`, `archive/tar`, `net/http`, filesystem APIs).
- Add unit tests for ordering, checksum failure, offline refusal, and budget truncation.

Depends on: Phase 1 manifest and Go Architect review.

### Phase 3 — Product integration

- Wire a self-contained product bundle or a product-local GOROOT-only mode.
- Add the offline probe and validator checks.
- Update `manifest.yaml`, `capabilities.yaml`, and `.pi/settings.json` only through the required approval boundary.

Depends on: Phase 2, approval, and no dangling product pointers.

### Phase 4 — Workflow and learning

- Add native prompts/skills that invoke metadata-first retrieval.
- Add evaluations for generated applications and toolchain-specific capabilities.
- Persist only durable consumer Memory; refresh sources explicitly and atomically.

Depends on: Phase 3 green and fresh-context review.

### Phase 5 — Extension to other languages

Generalize the protocol, not the Go rules: `language`, `toolchain_pin`, `source_units`, `resolver`, `validator`, and `artifact_namespace` become adapter fields. The Go adapter remains authoritative for Go and is not rewritten into a generic framework prematurely.

Depends on: measured reuse evidence from at least one additional language.

---

## 10. Risks and mitigations

- **Hidden metaproject dependency**: keep product bundles self-contained; validator rejects unresolved pointers.
- **Context saturation**: enforce metadata-first hard caps and explicit full retrieval.
- **Stale Effective Go guidance**: pin and label historical freshness; prefer newer official sources when available.
- **Toolchain drift via `GOTOOLCHAIN=auto`**: verify `go version` and record the actual toolchain pin before answering.
- **No Git repository at root**: checksums provide integrity, but VCS versioning remains PARTIAL until an approved VCS exists.
- **Non-deterministic embeddings**: keep them optional and outside authority.
- **Unbounded GOMODCACHE**: document no automatic eviction initially; add measured retention only after evidence.
- **Unbounded module index**: use an explicit allowlist, never index every possible module.
- **pprof/trace availability**: retrieve documentation from GOROOT source and treat first on-demand tool build as environment-dependent.
- **Source duplication**: run graph duplicate checks before admission and keep product entries pointer-only.

---

## 11. Definition of done for this design wave

Phase 0 review corrections applied on 2026-08-03:

- Product source pointers are `proposed` until a self-contained resolver and
  pinned bundle ship; Effective Go has no implicit local blob.
- Product routing states its minimum offline/blocked contract without pointing
  at metaproject files.
- Existing `errors` and `universal` rules are reused rather than duplicated.
- Race documentation resolves through `go help build`; benchmark/fuzz remain
  under `go help testflag`.
- `.agent/validators/validate-cognitive.py` checks YAML metadata, graph target
  resolution, and forbidden metaproject paths in product pointers.

- [x] The two critical source-registry sections have an explicit transformation strategy.
- [x] The graph identity, metadata, and relationships are explicit.
- [x] Retrieve -> Reason -> Generate -> Validate -> Memory is operationally specified.
- [x] Offline resolution, network refusal, pinning, provenance, and context caps are specified.
- [x] Toolchain capabilities and when to run each validation are specified.
- [x] `.agent/` and product `.pi/` ownership boundaries are explicit.
- [x] Subagent roles have single responsibilities and structured I/O.
- [x] Implementation phases, dependencies, risks, and approval boundaries are explicit.
- [ ] Executable retrieval tooling and offline probes are implemented (Phase 2/3, intentionally not part of this design-only wave).
- [ ] VCS-versioned raw evidence is available (blocked by current workspace state).
