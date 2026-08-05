# Z7 — Zone `tools/` (build and gate mechanics)

- **Metaproject Contract** — governs `KitV2/tools/`.
- **Audit report:** §2.8. **Decision:** `analyzers/` removed (2026-08-04).

## 1. Mission

The Kit's **mechanics** — never knowledge content. Tools build (generation), verify (validators), resolve (offline). A tool is tested, documented, and executed by a gate or in CI.

## 2. Structure and roles

| Sub-zone | Role | State on 2026-08-04 |
| --- | --- | --- |
| `tools/validators/` | Executable governance portal (C2) | active — to extend |
| `tools/generators/` | Deterministic generation of indexes/counts (INDEX.md, registry, C1 counts) | to create (first: index generator) |
| `tools/offline/` | Offline resolution: manifest + pinned bundle + attribution | active, reference model |

`analyzers/` was removed on 2026-08-04 (empty, without contract): duplication analysis is absorbed by the extended validator; reintroducible later only on written decision.

## 3. Rules

1. **Every tool = directory + README** (mission, inputs/outputs, gate that runs it) + test. A tool without README or test does not exist.
2. **Deterministic and offline in CI**: no network dependency for generators/validators.
3. **A generator replaces every manual index/count** (C1): INDEX.md, coverage counts, artifact registry are generated then verified by the validator — never hand-written.
4. The validator remains the **only** artifact that can fail the product gate; a tool that mutates without test is an error.
5. No Kit business logic in a tool; a tool does not invent knowledge, it verifies or generates it.

## 4. Maintenance

- **Addition**: mission + test + CI integration (or documented exclusion) + zone README update.
- **Validator modification**: each new check = positive case + negative case (tests); output stays `PASS`/error list + exit code.

## 5. Patterns

- One validator per responsibility (structure / freshness / manifest coherence) — composable.
- Output aligned on probes: `PASS` line or actionable errors (path + reason).

## 6. Anti-patterns

- "See later" tool without contract (the analyzers case — fixed);
- hardcoded coverage constants; counts are derived and verified by C2;
- hand-generated indexes; untested tool; network in CI.

## 7. Validation criteria

- [ ] Every tool has README + test.
- [ ] Kit indexes/counts are generated (C2 verifies the absence of drift).
- [ ] Full gate green (or documented PARTIAL).

## 8. Open questions

- First generator: knowledge index or complete artifact registry? (proposal: complete registry — it feeds INDEX.md, C1 counts, and relation verification.)
