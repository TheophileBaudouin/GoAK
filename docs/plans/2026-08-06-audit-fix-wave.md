# Plan — 2026-08-06 audit-fix wave (KVA-101..110) + release v2.5.0

## Goal

Close every finding of the 2026-08-06 permanent KitV2 audit, restore the CI
coverage floor to green, ship the pending 2.5.0 waves, and release v2.5.0
(README + install.sh ref + tag + push). One writer; fresh-context review
before committing; full gate after each phase.

## Context

- HEAD `8843477`; 182 modified + 34 untracked files pending (language wave,
  ultra-specialized skills wave, routing guarantee wave, router hardening).
- Audit verdict: PARTIAL — coverage closed, all mechanical gates PASS, but
  C11/C5/C9-C15 NON CONFORM (KVA-101/102/103) + 7 more findings.
- CI coverage floor (70%) is red: `go test -coverprofile ./...` counts the 15
  probe `main.go` files at 0% (59.9%); library surface alone is 79.6%.
- Root README is French, references v2.1.0, and still cites the removed
  `workflow-clarify` chain — violates D-2026-08-05-21 and D-2026-08-05-16.

## Constraints

- Non-destructive policy ends here: this is the correction pass (audit said
  "never fix during the audit"; the audit is closed).
- English is the mandatory language for every document (D-2026-08-05-21).
- Any template.yaml schema change = contract change (Z5 §3) → written
  decision in `.pi/memory/Decisions.md` + contract update in the same change.
- The validator must stay node-free; the ranking gate stays metaproject-owned.

## Done criteria

- KVA-101..110 fixed (or explicitly closed as no-action with reason).
- structure.md mechanism implemented and validated (Layer 5.1).
- Coverage floor green in the CI-equivalent computation; CI runs the full
  gate (validators, build_index --check, probes, Go gate).
- Full gate PASS (validators, router 22/22, gofmt/vet/lint/race/gosec/
  govulncheck, probes 15/15, snippets 3/3).
- Fresh-context review APPROVE.
- Commit A (preexisting waves), Commit B (audit fixes + release polish).
- README (English) + install.sh ref at v2.5.0; tag v2.5.0 pushed.

## Execution order

1. Decisions D-2026-08-06-12..14 (template.yaml schema fields; CI coverage
   scope; stopwords policy) + this plan.
2. Commit A: snapshot the 216 pending files (gate re-verified).
3. KVA-101 structure.md mechanism (generator module + 3 structure.md +
   validator hook + template.yaml field + TEMPLATES.md/template-contract.md/
   tools README + Z5 §3).
4. KVA-102..110 fixes (router README, .agent scan, registry rows,
   validate-instructions MANDATORY check, rule reword, usage-evidence,
   `_kit-*` declaration, capabilities note, stopwords prune, kind paragraph).
5. Coverage tests (sqlite WithTx/Open, offline setters/rank, postgres Close)
   - CI completion (coverage scope, validators, probes, build_index).
6. Full gate.
7. Fresh-context review (read-only subagent).
8. Commit B; README + install.sh; Commit C; tag v2.5.0; push.
9. Memory updates (Decisions, Progress, Brief, Gotchas).

## Evidence

- Audit report (this session, 2026-08-06): KVA-101..110 tables, coverage
  analysis (59.9% aggregate vs 79.6% library-only), gate outputs.
- `docs/evidence/2026-08-06/audit-fix-wave/` raw gate outputs.
