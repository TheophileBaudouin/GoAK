# C2 — Validation gate (executable governance portal)

- **Metaproject Contract** — governs `KitV2/tools/validators/validate-kitv2.py` and the product gate.
- **Audit report:** §2.8, §1.3 (problem 6).
- **Decisions:** 12/18-month freshness threshold approved (2026-08-04).

## 1. Mission

`validate-kitv2.py` is the **governance portal**: it turns the contract rules (C0, C1, Z1–Z10, A1, N1) into executable checks. Content that violates a contract must fail the gate. The charter stops being declarative: it becomes verifiable.

## 2. Required checks (to be implemented progressively; each addition has its test)

### Structure (existing, to extend)

- Mandatory root files (manifest, capabilities, AGENTS.md, .pi/settings).
- Absence of forbidden directories (`.agent/`, `.pi/memory/`, `evaluations/`).
- SKILL.md frontmatter (name/description/category/tags/last-verified; name == parent directory; ≤ 500 lines) — existing.
- Snippets (SNIPPET.yaml + example.go + check.sh) — existing.
- Templates (expected shape form) — existing.
- Offline bundle (manifest, checksums, sizes, licenses) — existing.
- No empty `.md` — existing.

### Coherence (new)

- `canonical`/`source` paths of manifest+capabilities exist.
- Identical manifest↔capabilities vocabulary.
- Recomputed counts == displayed counts (zero hardcoded count) — see C1.
- `run.sh` discovers probes (glob `probes/*/main.go`) — a hardcoded list is a failure.
- Generated INDEX up to date (knowledge/INDEX.md == real tree; no phantom domain).
- Graph-YAML relations resolved and never to `proposed`/nonexistent (existing, extend to status).

### Freshness (new — decision 2026-08-04)

- `last_verified` > 12 months → warning; > 18 months → error (proposed deprecated status) for every dated artifact (SKILL.md, graph-YAML, SNIPPET.yaml).
- Strict catalog opt-in: `KITV2_STRICT_CATALOG=1 python3 tools/validators/validate-kitv2.py` verifies catalogs: dated `Sources vérifiées` section, age (90 days for libraries, 180 days for reference-projects), suspicious returns in Go blocks and exactly duplicated paragraphs. Semantic duplication remains a human review.
- **Cross-file freshness (new — decision 2026-08-05, D-2026-08-05-11)**: the semantic cross-file review stays human (cf. the preexisting sentence of this contract, Freshness block above), but its triggering becomes mechanical: any modification of a canonical artifact (recipe, rule, pattern) with declared dependents requires each dependent to be re-verified in the same change. Verifiable form (check to implement, exact contract: plan 2026-08-05-metaproject, annexe A): `last_verified(dependent) >= last_verified(canonical)` for declared chains — snippet `source:` → target SKILL.md, and graph-YAML relations (`references`/`uses`/`depends_on`) to dated artifacts; `last_verified` field recommended in SNIPPET.yaml (Z4 §3). In addition, a similarity tripwire (warning, never error) between `snippets/*/example.go` and the canonical Go block of `source:` — detects literal drift, does not replace semantic review.

### Description quality (new)

- `description` of each SKILL.md: contains the activation ("Use when" / "Load when" / equivalent) — a description without activation condition is a failure (discoverability bottleneck, cf. Red Hat/Anthropic).
- Description > 1024 characters → failure (already checked).

### Absolute instructions (MANDATORY) — new, decision D-2026-08-05-15

Assumed extension of `.agent/instructions.md`: any absolute instruction (`MANDATORY`, "always", "never") added in a consumer artifact (skills, prompts, AGENTS.md, recipes) must either be accompanied by a named mechanical control (validator C2 or Pi gate), or be explicitly recorded as "guidance only, not enforced" in the automation-gaps registry (`.agent/instructions.md` §Enforcement). The audit (dimension "absolute instructions", kit-audit phase C9) inventories every occurrence and its enforcement status; a deterministic C2 check (lexeme grep + registry attachment) is planned (annexe C of the 2026-08-05-metaproject plan).

### Per category (new — aligned on A1)

- Recipe: presence of an observable scenario section and a test; the scenario carries an explicit verdict (`PASS`/`PARTIAL`/`BLOCKED`) — no recipe without a scenario.
- Library (module SKILL.md): admission criteria stated (admission checklist); considered alternatives present.
- Template: MIT `LICENSE` + `ATTRIBUTION.md` (source, version, adaptations) for every non-legacy template.
- Rule: imperative + boundary ("does NOT cover") + sources present.

## 3. Operation

- Output: error list on stderr + exit code 1 on error; otherwise one line `kitv2: PASS (…)`.
- Each check is an isolated, testable function with a positive and a negative case (tests `test_validate_*.py` — the ruff suite is part of the metaproject gate).
- Warnings (12-month freshness, notes) do not fail but are printed with `warning:` prefix.
- CI (`.github/workflows/ci.yml`) runs the validator + the Go gate on the product.

## 4. Full Go gate (from `KitV2/`)

```sh
python3 tools/validators/validate-kitv2.py
go mod tidy && go mod verify
test -z "$(gofmt -l .)"
go vet ./...
golangci-lint run ./...
go test -race ./...
gosec ./...
govulncheck ./...
bash probes/run.sh
```

Rules:

- `PATH="$PATH:$(go env GOPATH)/bin"` before the tools (golangci-lint, gosec, govulncheck).
- Missing tool → documented **PARTIAL** gate, never PASS.
- Mechanical checks prove code properties; the observable scenario (probe/recipe) proves behavior; never one for the other.

## 5. Anti-patterns

- Validator that mutates without test; check without negative case.
- Hardcoded count in the validator: coverage counts are now derived from the tree and verified against `capabilities.yaml`.
- Green gate despite a violated contract.
- Unreadable output (errors without path or actionable reason).

## 6. Contract validation criteria

- [ ] Every check listed in §2 exists (or is planned with an issue).
- [ ] A negative test set covers each check.
- [ ] The full gate (structure + Go + probes) runs in CI.
- [ ] Derived counts replace hardcoded constants.
- [ ] 12/18-month freshness implemented.

## 7. Open questions

- The decision applies since 2026-08-05: derivation from the tree, comparison with `capabilities.yaml`, positive and negative tests in `tools/validators/test_validate_kitv2.py`.
- Should there be a `--strict` mode (warnings = errors) for CI?
