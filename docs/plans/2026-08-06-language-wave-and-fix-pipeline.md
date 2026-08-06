# 2026-08-06 — KitV2 audit remediation: language wave + fix pipeline

**Goal:** close the KVA-101…111 findings of the 2026-08-05 permanent audit so the
product can reach a clean `PASS` at the next audit.

**Context:** audit report (2026-08-05, this repository, root scope). The kit is
under the fundamental rule D-2026-08-05-21: English is the mandatory language
for every skill, instruction, and document. N1 §4 documents the migration wave;
the audit found the wave partially undocumented (recipes) and partly still
growing (new French admissions).

**Constraints:** faithful translations only (D-2026-08-05-21: preserve technical
terms and intent, never reformulate); one domain at a time (N1 §4); every
validator change ships with positive + negative tests (C2 §3); the fiche-header
conversion and the validator's French-heading requirement change together
(N1 §4a); router regenerated after any description change (Z11); full gate +
strict catalog at the end (C2 §4).

**Done =** all waves converted, gate green (validators, Go gate, probes,
strict catalog, router `--check`), N1 §4 updated to the actual residual state,
memory updated (Progress/Gotchas/Brief/Decisions).

## Findings to close

| ID | Fix |
| --- | --- |
| KVA-101 | 15 recipe SKILL.md bodies + 11 frontmatter descriptions → EN; N1 §4 wave list corrected to include recipes |
| KVA-102 | `knowledge/architecture/mcp-server-shape.yaml` → EN |
| KVA-103 | 40 catalog fiche headers → EN; `SOURCE_HEADING_RE` + strict-catalog messages → EN (same change) |
| KVA-104 | 39 patterns + 54 anti-patterns YAML bodies → EN; admission rule: new knowledge YAMLs are written in EN |
| KVA-105 | add `last_verified` to the 3 SNIPPET.yaml; implement the date-chain check (`snippet last_verified >= canonical last-verified`, missing dates ignored) + tests |
| KVA-106 | `.agent/instructions.md` §Enforcement: record the process absolutes found; rule-boundary "never/always" stays rule content (Z1) |
| KVA-107 | remove 10 untracked cache/junk files (`.DS_Store`, `.ruff_cache/`, `__pycache__/`) |
| KVA-108 | `probes/README.md` — drop the literal metaproject path from the boundary sentence |
| KVA-109 | `capabilities.yaml` `known_limits` → structured `id/impact/status`; open limits downgrade the capability to `partial` |
| KVA-110 | `templates/TEMPLATES.md` — add `desktop-app` roadmap line (planned, no conforming MIT source) |
| KVA-111 | `go_version` format: leave as-is, record the open question in Z10 (needs contract decision) — not part of this pass |
| KVA-112 (new) | `capabilities.yaml` pi-workflows criteria factual drift ("8 prompts, 6 skills" → actual 3 prompts, 8 skills) |

## Waves (sequential, one domain at a time)

1. **Mechanical pass** (parent): KVA-106/107/108/109/110/112 + SNIPPET `last_verified` + validator `check_snippet_chain` + tests.
2. **Wave 1 — recipes** (subagents, 15 files, disjoint): body + description → EN.
3. **Wave 2 — knowledge patterns + anti-patterns** (subagents, 93 files): body → EN.
4. **Wave 3 — catalog fiche headers** (parent, script): 6 headers × 40 files → EN; `SOURCE_HEADING_RE` → EN in the same pass.
5. **Wave 4 — mcp-server-shape.yaml** (parent): → EN.
6. **Gate**: `build_index.py`, both metaproject validators, `validate-kitv2.py` (+ strict), Go gate, probes, template builds/tests.
7. **Docs/memory**: N1 §4 residual-state update, Decisions.md entry, Progress/Brief/Gotchas refresh.

## Open questions (deferred, recorded only)

- `go_version` format (floor `1.22+` vs exact) — Z10 decision, next contract touch.
- Similarity tripwire between `snippets/*/example.go` and canonical blocks (annexe A, C2 §2) — warning-only, kept planned.
- `tools/generators/` (INDEX.md, registry) — separate workstream, not this pass.
