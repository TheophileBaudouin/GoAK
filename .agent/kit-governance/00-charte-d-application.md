# C0 — Application charter (artifact lifecycle)

- **Metaproject Contract** — governs `KitV2/` (the product). Status: phase-2 contracts (2026-08-04), referenced by C1, C2, Z1–Z10, A1, N1.
- **Authority**: `KIT_CHARTER.md` (root) remains the process authority. This contract **operationalizes** the charter: it neither replaces nor contradicts it.

## 1. Mission

Define the lifecycle of every kit artifact (addition, modification, deprecation, removal) and the cross-cutting work rules — so that an agent or developer can enrich the Kit in 3–5 years without drift.

## 2. Artifact lifecycle

```text
proposed → active → deprecated → (removal, after migration)
```

| Transition | Trigger | Exit conditions |
| --- | --- | --- |
| proposed → active | Admission passed (source + distinct question + category validation) | Complete metadata, primary source, resolved relations, green gate, executed observable scenario (`PASS`/`PARTIAL`/`BLOCKED` documented) |
| active → deprecated | Source obsolete, duplicate detected, ecosystem changed, `last_verified` > 18 months not renewed | Written decision (metaproject Decision Record), `status: deprecated`, replacement note, consumers identified |
| deprecated → removal | No active consumer, migration done | Deletion **with** Decision Record and reference updates in the same commit |

Rule: a `proposed` artifact **cannot** be referenced by an `active` artifact (the validator rejects relations to proposed/nonexistent targets).

## 3. Versioning (semver per artifact)

Each artifact carries `version:` (integer in existing graph-YAML, to keep; semver from v2 of artifacts):

- **major**: breaking change of the output contract (schema, observed behavior, signature, frontmatter);
- **minor**: compatible addition (new section, new optional field);
- **patch**: correction (typo, source, rewording without behavior change).

Any **major** upgrade requires: written decision, documented migration, and `supersedes`/`validated_by` relation updates in the same commit.

## 4. Write-gate (evidence before inclusion)

1. The contributor **proposes** (plan or issue) — never direct writing for new content.
2. Admission requires a **verified primary source** (official docs, RFC, maintained reference implementation, observed production failure, proven community standard) — not "seems useful".
3. The artifact answers a **distinct question**: if an existing rule/recipe/pattern already answers it, the contributor points instead of writing (duplication = admission failure).
4. Category validation is executed (see A1) and the gate passes.

## 5. Freshness (`last_verified`)

- Every factual datum carries `last_verified: YYYY-MM-DD`.
- **12 months** → validator warning; **18 months** → proposed deprecation status.
- Verification is not bumping the date: it re-verifies sources, versions, APIs, and cited behaviors, and updates content if needed.

## 6. Cross-cutting work rules (metaproject)

1. One writer per worktree; parallelize only read-only research.
2. Plan in `docs/plans/` for any non-trivial work; decision in `.pi/memory/Decisions.md`; raw evidence in `docs/evidence/<date>/`.
3. Fresh-context review (read-only sub-agent) before declaring completion; remarks are integrated or settled with reason.
4. Three identical failures in a row → stop and report, no loop.
5. The gate is the only mechanical proof; the observable scenario is the only behavioral proof; never one for the other.

## 7. Forbidden content everywhere in the Kit

- Metaproject memory/decisions/evidence/history.
- Secrets, hardcoded paths, raw command output.
- Body duplication (each truth lives once; the rest points).
- Empty placeholders (`.gitkeep` directories without contract): planned zones live in the zone README roadmap, not ghost directories.

## 8. Validation criteria (enforceable by C2)

- [ ] C2 validator passes (including freshness and manifest/capabilities coherence).
- [ ] Green Go gate (gofmt, vet, lint, tests, race, gosec, govulncheck — or documented PARTIAL if a tool is missing).
- [ ] Affected probes pass (observable scenario).
- [ ] No duplication introduced (C2 check).
- [ ] Relations resolved (no reference to `proposed`/nonexistent).
- [ ] Written decision for any status transition.

## 9. Open questions

- Integer semver (`1`) vs string semver (`1.2.0`) for artifacts: align on the schema validated in Z10.
- "Capabilities" policy (manifest): see C1.
