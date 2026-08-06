# Plan & decision — Routing guarantee wave (2026-08-06)

## Goal

Make the kit's skill usage **verifiable and salient** instead of relying on
agent discipline alone. Three owner-approved changes (asked 2026-08-06,
decisions recorded here):

1. **Routing-quality gate** — the router's ranking becomes contract-tested
   against the REAL runtime scoring (zero divergence by construction).
2. **Reduced always-visible surface** — library fiches leave the Pi prompt
   surface (settings.json); rules and recipes stay visible; fiches stay
   routable.
3. **Strengthened routing mandate** — KitV2/AGENTS.md + the tool's
   promptGuidelines make the `search_kit_resources` call mandatory and name
   the default-applicable patterns.

## Why (evidence)

- Pi loads only SKILL.md **descriptions** into the system prompt; skill
  bodies load on demand and Pi documents that models don't always load them.
- The knowledge graph YAML (patterns/anti-patterns/sources) is invisible
  natively — reachable only through `search_kit_resources`.
- The index was verified **complete and intact** but its **ranking quality**
  was never tested: a skill with weak terms could silently degrade routing.
- ~80 always-visible descriptions diluted per-skill salience (the naming
  rule was buried).

## What changed

| File | Change |
| --- | --- |
| `.pi/extensions/kit-resource-router-scoring.ts` (new) | Pure BM25 scoring core, no Pi imports — single source shared by runtime and gate |
| `.pi/extensions/kit-resource-router.ts` | Imports the scoring core (`./…scoring.js`, jiti maps to `.ts`); behavior byte-identical; promptGuidelines strengthened (mandatory call + default patterns: naming, error wrapping, channel ownership, zero value) |
| `.pi/settings.json` | `skills: ["../rules", "../recipes"]` (catalogs removed) |
| `.pi/README.md` | Documents the surface decision |
| `router/scenarios.json` (new) | 22-scenario routing contract: 20 intent→resource mappings (new wave + core), 1 explicit-library fiche check, 1 off-domain rejection |
| `router/README.md` | Documents the contract + gate (Node ≥ 23.6) |
| `.agent/router/run_scenarios.mjs` (new) | Gate runner importing the real scoring module; exit 0/1 |
| `.agent/router/test_router_scenarios.py` (new) | unittest; skips without node (PARTIAL); 1 test |
| `.agent/router/test_validate_kitv2_router.py` | +6 unit tests for the validator's scenarios check |
| `tools/validators/validate-kitv2.py` | `check_router_scenarios()`: schema + expected-id linkage, pure Python, node-free; wired into main() |
| `AGENTS.md` | "Routing is mandatory, not optional" — call before technical work, read the top matching resource, default patterns named by the tool's guidelines |
| `manifest.yaml`, `capabilities.yaml` | Version 2.5.0; resource-routing criteria mention the gate |
| `router/index.json` + `meta.json` | Regenerated (v2.5.0, 278 resources) |

## Verification (gate)

- `run_scenarios.mjs`: **22/22 PASS** under the real scoring (naming → rule
  #1, channel ownership → pattern #1, chi fiche in top-3, quantum →
  off-domain).
- Metaproject router tests: **25 passed** (12 existing + 6 scenarios-check +
  1 gate + 6 build tests).
- `validate-kitv2.py` PASS (72 product skills, router 278) ·
  `validate-instructions.py` PASS · `validate-cognitive.py` PASS ·
  `build_index.py --check` PASS.
- Probes 15/15 PASS · gofmt clean · `go vet` OK · golangci-lint 0 issues.
- Fresh-context review: **APPROVE** — scoring extraction byte-identical
  (verified against `git show HEAD`), gate design sound (no scoring
  duplication), 3 minor nits fixed (dead `limit` param, Node-version doc,
  off-domain rendering note).

## Boundaries kept

- Z11: `index.json`/`meta.json` stay generated; `scenarios.json` is
  documented as an authored contract in router/README.md.
- Runtime zone: scoring module lives in `.pi/extensions/` with zero Pi
  dependency (jiti/plain-node compatible).
- Product validator stays node-free (schema/linkage only); the ranking gate
  is metaproject-owned, mirroring the builder ownership.
- Catalog fiches remain indexed and routable; only the prompt surface
  changed.
