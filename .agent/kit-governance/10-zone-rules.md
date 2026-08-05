# Z1 — Zone `rules/` (rules)

- **Metaproject Contract** — governs `KitV2/rules/`.
- **Audit report:** §2.1. **Decision:** core budget ≤ 6 modules / ≤ 300 lines approved (2026-08-04).

## 1. Mission

The "must always be true" layer of the Kit (charter Layer 1). Rules answer "what must stay true for any generated or reviewed Go code?" — they never contain implementation.

## 2. Structure

- `rules/core/` — **universal rules, loaded every session** (permanent cost): `philosophy`, `concurrency`, `errors`, `universal`, `validation/{golangci-lint,gosec,govulncheck}`.
- `rules/registry/` — **domain rules loaded on demand**: `doc-comments`, `logging`, `testing` (examples).

## 3. Boundary rules (inviolable)

1. **core ≠ registry**: a core rule never references a registry module (universals do not depend on load-on-demand content).
2. A rule does not contain production code (charter §3) — at most a minimal demonstration excerpt linked to its imperative.
3. A rule does not duplicate a pattern/anti-pattern of `knowledge/` — it references it (explicit relation).
4. Nothing but rules in this directory: no recipes, no memory, no contracts.

## 4. Core compactness budget (decision 2026-08-04)

- **≤ 6 modules** in `rules/core/`; **≤ 300 lines** per SKILL.md.
- **Counting unit: "module" = top-level directory of `rules/core/` containing at least one SKILL.md** (5 on 2026-08-04: concurrency, errors, philosophy, universal, validation — `validation/` counts as 1 module even with 3 SKILL.md).
- Any core addition above the budget is **blocked**: it requires a written decision (Decisions.md) and the removal/merging of an existing module.
- C2 check: module count (top-level directories) + max size per file.

## 5. Rule schema (semantic elements — cf. A1 §2 and §1.9)

Each rule carries the following semantic elements, whatever the form (free headers; A1 §1.9: a section exists only if it has content — a statement in the body counts as a header):

1. **Imperative**: the rule, in one actionable sentence (mandatory).
2. **When to apply**: scope of application (mandatory).
3. **Boundary**: what the rule does NOT cover (mandatory; dedicated section or identifiable statement).
4. **Counter-examples**: cases where the rule seems to apply but does not (when they exist).
5. **Verification**: how to check conformity (command, grep, review) (mandatory).
6. **Sources**: primary, verified (mandatory).

Decision 2026-08-05: the old fixed-headers schema of the former §5 was implemented by no rule and contradicted A1 §1.9; it is replaced by the semantic form above (free headers). The corresponding C2 check remains a review (see §9).

## 6. Maintenance

- **Core addition**: written decision + budget re-verified (C2 blocks beyond).
- **Registry addition**: admission = primary source + boundary + actionable verification + no contradiction with existing rules.
- **Modification**: bump `version` (major if stricter) + `last_verified` + verification of the artifacts that reference the rule (trigger for dependent re-verification — cross-file C2 check, D-2026-08-05-11).

## 7. Patterns

- A rule = a verifiable imperative + a "does NOT cover" boundary.
- Core rules cite official sources (Effective Go, Code Review Comments, Go Proverbs) and only other core rules.

## 8. Anti-patterns

- Vague rule ("use idiomatic Go") without boundary or verification.
- "Just this once" addition in core (permanent budget drift).
- Rule containing a pattern body (knowledge/ duplication).
- Empty `.md` (regression already fixed — C2 detects it).

## 9. Validation criteria

- [ ] C2: core budget (≤ 6 modules, ≤ 300 lines) verified.
- [ ] Rule schema (imperative, boundary, verification, sources): review control (free headers, A1 §1.9) — source freshness verified by C2.
- [ ] C2: no core → registry reference.
- [ ] Freshness 12/18 months (C0).

## 10. Open questions

- `universal` (renamed 2026-08-04): verify its content is really core and not registry (review at next audit).
- Should there be a quantified "session budget" core rule other than the module count?
