# Z11 — Zone `router/` (semantic routing index)

- **Metaproject Contract** — governs `KitV2/router/` (index, routing-quality
  contract, runtime tool). The builder and the quality gate live in the
  metaproject (`.agent/router/`).
- **Origin:** user decisions 2026-08-05 (BM25, versioned JSON, mandatory
  search, native Pi extension) — plan `docs/plans/2026-08-05-resource-router.md`; routing-quality wave 2026-08-06 (product 2.5.0) — plan
  `docs/plans/2026-08-06-routing-guarantee.md`.

## 1. Mission

The kit's embedded routing system: a **generated index** that lets a Pi agent
find relevant resources without loading the kit into context, a **read-only
runtime tool** that scores queries, and a **routing-quality contract** that
keeps the ranking verifiable as the kit grows. The index routes to source
files; it never replaces them.

## 2. Roles and boundaries (inviolable)

| Element | Role | Owner |
| --- | --- | --- |
| `router/index.json` | Generated artifact: resources (id, kind, path, description, tags, terms) | metaproject (builder) |
| `router/meta.json` | Version, index sha256, counts, stopwords | metaproject (builder) |
| `router/scenarios.json` | **Authored** routing-quality contract (intent → expected top-K resources) | product; maintained under metaproject gate |
| `router/README.md` | Consumption doc: read-only, never hand-edited | metaproject (review) |
| `.agent/router/build_index.py` | Builder (build / --check) — outside the kit | metaproject |
| `.agent/router/run_scenarios.mjs` | Quality-gate runner — imports the REAL runtime scoring (Node ≥ 23.6) | metaproject |
| `.agent/router/test_router_scenarios.py` (+ router validator tests) | Gate + contract tests | metaproject |
| `.pi/extensions/shared/kit-resource-router-scoring.ts` | **Single source of the ranking logic**: pure BM25 core, zero Pi/typebox imports; lives in `shared/` so Pi's extension loader (direct `*.ts` + one-level `index.ts` only) never mistakes it for an extension | kit (runtime) |
| `.pi/extensions/kit-resource-router.ts` | Native Pi tool `search_kit_resources`, read-only; imports the scoring core | kit (runtime) |
| `.pi/skills/kit-resource-routing/SKILL.md` | Usage skill (when/how) | kit (runtime) |
| `validate-kitv2.py` `check_router_scenarios()` | Node-free schema + expected-id linkage check on scenarios.json | kit (product validator) |

## 3. Rules

1. **Generated artifact**: `index.json` and `meta.json` are NEVER hand-edited.
   Any modification of an indexable resource (rules/, recipes/, knowledge/,
   snippets/, .pi/prompts/, .pi/skills/) requires a builder regeneration then
   the full gate.
2. **Read-only at runtime**: the extension tool only reads the index. It
   modifies neither the index, nor the kit, nor the environment.
3. **Index = router only**: every entry points to a real file; the truth
   content stays the source file.
4. **Determinism**: stdlib Python builder, no network, stable output (sorted
   by id); `--check` compares and exits non-zero on drift.
5. **Bounded volume**: short descriptions (source: frontmatter), precomputed
   terms, index ~< 200 KB. The runtime never loads kit file content, only the
   index.
6. **Context protection**: top-K ≤ 5 (max 8), score threshold, clean zero
   result rather than noise ("empty > noise" rule).
7. **Scoring has exactly one implementation**: the ranking logic lives ONLY
   in `kit-resource-router-scoring.ts`. The extension imports it; the gate
   runner imports it. Re-implementing the scoring anywhere else (a Python
   copy, a duplicate TS module) is a release-blocking defect — the gate must
   verify exactly what the agent sees, by construction.
8. **Two-layer verification (never one)**: the product validator checks the
   contract file's schema and id linkage (node-free, runs anywhere); the
   metaproject gate checks the actual ranking under the real scoring (Node ≥
   23.6). A scenario change must pass BOTH; if node is missing the gate is
   skipped as PARTIAL, never PASS.

## 4. Maintenance

- **Add an indexable resource**: the gate (coverage) will fail until the
  index is regenerated → run `python3 .agent/router/build_index.py` from the
  metaproject root, verify `git diff` on router/.
- **Add or change a scenario** (routing-quality contract): the scenario must
  be a realistic agent intent (3–8 technical terms, one concern), target an
  existing indexed id, and be **able to fail** — an expectation that cannot
  break under any realistic change is padding and is not admitted. Verify the
  expectation against the real scoring before committing (run the gate).
- **Evolve the scoring** (synonyms, KIND_WEIGHT, BM25 constants, off-domain
  threshold): runtime-side change — edit `kit-resource-router-scoring.ts`
  only, re-run the full gate (all scenarios) and the four e2e scenario types
  (obvious, vague, empty, near-multiple), and re-check every scenario
  expectation that shifts. Never edit a duplicate copy.
- **Modify the system**: builder (metaproject, tests + README) OR runtime
  (kit, end-to-end scenario); never both in the same responsibility.
- **Test**: builder fixtures + scenario gate (positive AND negative cases —
  a gate with no demonstrated failure mode proves nothing) + end-to-end pi
  scenarios + full gate.
- **Do not degrade routing**: every new resource must have a real frontmatter
  description (1..1024 characters, technical vocabulary); no generic
  description ("useful for Go"). The scenarios that exist must keep passing
  after the addition.

## 5. Patterns

- Deterministic builder + verifying gate (same schema as tools/offline).
- Stopwords in meta.json (single source, no builder/runtime duplication).
- Synonyms only on the runtime side (query expansion), never on the build
  side.
- Shared scoring core: one pure module imported by runtime and gate — the
  only way to make "the test verifies what the agent sees" true by
  construction (gotcha 2026-08-06: jiti resolves `.js` → `.ts`; Node ≥ 23.6
  runs `.ts` natively).

## 6. Anti-patterns

- Hand-edited index; runtime that writes; index containing file content
  (instead of descriptions); unfiltered results injected into context;
  network dependencies in the builder.
- A second scoring implementation (Python port, duplicated TS) "for test
  convenience".
- Decorative scenarios: expectations that can never fail, or queries so
  broad every resource matches.
- The product validator depending on node (it must stay node-free; the
  ranking gate is metaproject-owned).

## 7. Validation criteria

- [ ] `validate-kitv2.py`: valid index.json, conforming meta.sha256, complete
      coverage of indexable resources, existing paths, scenarios contract
      schema + expected-id linkage.
- [ ] `python3 .agent/router/build_index.py --check`: clean output.
- [ ] `node --no-warnings .agent/router/run_scenarios.mjs`: 22/22 scenarios
      PASS under the real runtime scoring (or more, as the contract grows).
- [ ] Gate tests include negative cases proving the tripwire fires (unreachable
      expectation → exit 1; expected id missing from index → exit 1).
- [ ] End-to-end scenarios: 4 types, no false positive in the assertions.

## 8. Open questions

- None: the scope was arbitrated with the user (2026-08-05); the
  routing-quality wave extended it with the scenarios contract and the
  two-layer gate (2026-08-06).
