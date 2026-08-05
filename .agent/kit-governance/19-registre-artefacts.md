# Z10 — Artifact registry (cross-cutting graph)

- **Metaproject Contract** — cross-cutting schema applied to **every** kit artifact, whatever its zone.
- **Audit report:** §2 (graph), charter §2/§5.

## 1. Mission

Define the **metadata template and relations** that `validate-kitv2.py` applies to every artifact: an artifact is accepted if, and only if, its template and relations are complete and resolved.

## 2. The 10 kinds (charter §2)

`Rule`, `Recipe`, `Pattern`, `Snippet`, `Template`, `Capability`, `Evaluation`, `DecisionRecord`, `Source`, `Memory`.

| Kind | Mainly lives in | Format |
| --- | --- | --- |
| Rule | `rules/` | SKILL.md |
| Recipe | `recipes/` | SKILL.md + code |
| Pattern | `knowledge/patterns/` (positive); `knowledge/anti-patterns/` (negative) | graph-YAML |
| Snippet | `snippets/` | SNIPPET.yaml + code |
| Template | `templates/` | MIT project directory (Z5) |
| Capability | `capabilities.yaml` (+ `manifest.yaml`) | YAML |
| Evaluation | `probes/` | main.go |
| DecisionRecord | **metaproject** (`.pi/memory/Decisions.md`, `docs/`) | Markdown — never in the Kit |
| Source | `knowledge/**` (pointers) + `tools/offline/` (bundle) | graph-YAML / bundle |
| Memory | **metaproject** (`.pi/memory/`) | Markdown — never in the Kit |

## 3. Mandatory metadata (all product kinds)

```text
id:            <kind>:<domain>:<slug>     (C2 regex: ^(rule|recipe|pattern|snippet|
                                             template|capability|evaluation|decision-record|
                                             source|memory):[^:]+:.+$)
title:         one sentence
kind:          one of the 10
version:       semver (from v2; existing integer accepted)
status:        proposed | active | deprecated | rejected
owner:         go-agent-kit (or declared team/maintainer)
tags:          [kebab-case]
go_version:    minimum tested version (never future)
dependencies:  []
last_verified: YYYY-MM-DD
```

## 4. Allowed relations (graph)

`depends_on`, `uses`, `implements`, `extends`, `references`, `requires`, `supersedes`, `validated_by`, `generated_from`.

Coherence note (2026-08-04): this list matches exactly `GRAPH_RELATIONS` in `validate-kitv2.py`. `extends` is declared but currently **unused** in the Kit — it stays in the published schema (no schema removal without written decision); the metaproject Brief omits `extends` from its list — to fix at next touch.

Resolution rules (C2):

1. Every stable-id target must exist in the registry (known ids).
2. Every target must be `active` (relations to `proposed`/`rejected`/`deprecated` are a failure, except explicit `supersedes`/`references`).
3. `references` accepts URLs (primary sources); the other relations only stable ids.
4. The graph is the truth; the directory is only navigation (charter §13).

## 5. Quality rules (actionable)

1. An artifact = **one responsibility, one question**; two artifacts answering the same question = at least one is wrong (C0).
2. No body duplication: relations replace copying.
3. A `proposed` artifact is invisible to consumers and carries no incoming relations from `active`, **except** the Source pointers explicitly shipped for discoverability: the entries of `knowledge/catalogs/libraries/pointers/` and the proposed architecture artifacts whose shipping is recorded in `Decisions.md`. These exceptions stay marked `proposed` and must be filterable by path and status in the router.
4. `last_verified` ≤ 12 months (warning) / 18 (deprecated) — C0/C2.
5. Every `active` artifact with observable behavior is `validated_by` an evaluation (probe) or an executed scenario.

## 6. The generated registry (Z7)

The complete registry (id, kind, status, zone, relations) is **generated** by `tools/generators/` and verified by C2 — it replaces any manual index and makes relation resolution verifiable without a database.

## 7. Validation criteria

- [ ] C2: complete template (§3 metadata) for every graph-YAML and product SKILL.md module.
- [ ] C2: relations resolved and §4 rules applied.
- [ ] C2: freshness and question uniqueness (duplicates detected by title).

## 8. Open questions

- Version: normalize `version:` to semver string (e.g. `1.0.0`) for all new artifacts while accepting the existing integer — migration by generation?
