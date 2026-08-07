# Evidence — ui-kit re-sync + single registration point (2026-08-08)

## Files

- `full-gate.log` — complete validation gate, UTC 2026-08-07T23:05:09Z,
  commit `f5bc710`: validators ×3 PASS, router index up to date, Go
  scenarios 22/22, UI scenarios 11/11, router unit tests OK, gofmt clean,
  go vet OK, golangci-lint 0 issues, `go test -race` OK, gosec 0 issues,
  govulncheck no vulnerabilities, probes PASS, GATE EXIT 0.
- `consumer-pi-smoke.txt` — headless consumer smoke
  (`pi -p -a --no-session`, trusted project, temp install of the KitV2
  tree via `git archive`):

  - **SKILLS**: the 7 ui-kit skills are discoverable through the fused
    root `.pi/settings.json` — `frontend-design, macos-design-guidelines,
    shadcn, ui-review, ux-memory, web-design-guidelines,
    web-platform-guidelines` — alongside the rules, recipes and `.pi/skills`
    (proof of registration, D-2026-08-08-02).
  - **GO** (`search_kit_resources`, Go-only query): top3
    `recipe-worker-pool, pattern:concurrency:worker-pool,
    pattern:antipattern:go-context-unused` — `ui-kit in paths: no`.
  - **UI** (`search_ui_kit_resources`, agent-chat query): top3
    `agent-chat, components-index, screens` — `outside ui-kit: no`.

## Verification performed

- Re-sync gate inside the helper: PASS (validators, Go 22/22, UI 9/9 at
  that point, 44 router tests, gofmt/vet/test-race, probes 16/16).
- npm 0.1.1 tarball `sdk/` vs pinned repo `sdk/` at `cd00eb5d`:
  `diff -rq` empty (byte-identical; npm never the source).
- After the routing fixes: Go gate 22/22, UI gate 11/11, router unit tests
  44 passed incl. the unreachable-expectation tripwire
  (`test_unreachable_expectation_fails`), `check_ui_kit_registration`
  4 unit tests, validators ×3 PASS.
- Product invariant: `git ls-files KitV2/.pi/memory` = 0 (no consumer
  memory shipped); the temp consumer smoke copy (which Pi initialized with
  memory stubs during the run) was deleted.

## Decision records

`../.pi/memory/Decisions.md` — D-2026-08-08-01 (re-pin to cd00eb5d),
D-2026-08-08-02 (single registration point), D-2026-08-08-03 (kit-audit
read-only ui-kit dimension).
