# Evidence — ui-agent-kit integration (2026-08-07)

Plan: docs/plans/2026-08-07-ui-agent-kit-integration.md
Phase 0: docs/research/2026-08-07-ui-agent-kit-phase0-investigation.md

## Final gate (2026-08-07, after step 5)

```
kitv2: PASS (73 product skills, 3 snippets, standalone, offline bundle, router index 280 resources)

--- router gates ---
router scenarios: 22/22 PASS (index v2.5.0, 280 resources)
ui router scenarios: 9/9 PASS (35 ui-kit resources)

--- metaproject unit tests ---
38 passed in 0.77s

--- Go gate ---

--- probes ---
16
```

--- Go gate (PATH exported) ---
gofmt: CLEAN
vet: OK
lint: 0 issues.
test -race ok packages: 19
gosec:   Issues : [1;32m0[0m
govulncheck: No vulnerabilities found.


## Final gate (post-review, b486fd9 + registry fix)

```
instruction-artifacts: PASS
cognitive: PASS (35 catalog objects)
kitv2: PASS (73 product skills, 3 snippets, standalone, offline bundle, router index 280 resources)
router index: up to date (280 resources)
router scenarios: 22/22 PASS (Go corpus, v2.5.0)
ui router scenarios: 9/9 PASS (35 ui-kit resources)
unit tests: 41 passed (.agent/router)
gofmt: CLEAN · go vet: OK · golangci-lint: 0 issues
go test -race: 19 packages ok
gosec: 0 issues · govulncheck: no vulnerabilities
probes: 16/16 PASS (incl. ui-kit-sync)
```

## Fresh-context review (R-2026-08-07)

Read-only reviewer (independent context) verdict: APPROVE-WITH-NITS after
fixes. Findings integrated:

- KitV2/AGENTS.md tail repaired (duplicated ## Limits + stray fragment from a
  lost multi-edit); the 'Wails projects (conditional)' section referenced by
  Z13 restored.
- Z13 §7.1 'validator cross-checks PIN.md' was claimed but unimplemented →
  check_ui_kit_pin() added (validate-kitv2.py) + 3 unit tests.
- UI ranking gate was local-only → run_ui_scenarios.mjs + router pytest wired
  into .github/workflows/ci.yml.
- New tool's MANDATORY lexeme registered in .agent/instructions.md (§16.1.4).
- NITs: Progress.md entry translated to English (D-2026-08-05-21).
- Reviewer spot-verified vendor fidelity (5 upstream files byte-identical to
  the zone) and corpus separation (Go index: 0 ui-kit/ paths; UI index: all
  paths under ui-kit/).
