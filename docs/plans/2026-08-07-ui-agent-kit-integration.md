# Plan — Native ui-agent-kit integration as a first-class KitV2 zone

Date: 2026-08-07
Status: approved by owner via Phase 1 questionnaire (2026-08-07)
Predecessor: `docs/research/2026-08-07-ui-agent-kit-phase0-investigation.md`

## Owner decisions (Phase 1)

1. **Architecture**: the SDK is integrated natively and completely as a new
   first-class `KitV2` zone (`ui-kit/`), on the same footing as `rules/`,
   `recipes/`, `knowledge/`, `router/`, with its own `AGENTS.md` (sourced
   verbatim from the SDK, pinned). Context non-pollution is the design bar:
   the zone is inert unless routed to.
2. **Routing**: a second read-only Pi tool `search_ui_kit_resources`,
   reusing the shared scoring module. The Go corpus (`router/index.json`)
   is never mixed with the UI corpus.
3. **Sourcing**: the zone content comes from the ui-agent-kit GitHub repo at a
   pinned commit SHA (never npm). A shipped sync tool materializes the SDK
   into a real Wails project's `frontend/`.
4. **Reports**: GoAK `docs/` conventions (this plan lives in `docs/plans/`).

## Reconciliation with mission rule 5 ("no trace for non-Wails")

The owner's Phase 1 answer explicitly supersedes a literal reading of rule 5:
full native integration is wanted, and non-pollution is achieved **behaviorally**
(no rules loaded into context, no Go-query contamination, no SDK materialized
into any `frontend/` unless a Wails project is detected) rather than by file
absence. Concretely: the zone ships with every install (like every other zone),
but (a) it is not declared in `.pi/settings.json`, so no UI skill is ever
auto-loaded into a Pi session; (b) `search_kit_resources` never reads it; and
(c) the sync tool refuses to materialize anything unless `wails.json` +
`frontend/` are present. Rule 5's operative constraints ("ni règle chargée,
ni entrée de routeur activée") are preserved; "ni fichier copié" is
interpreted as "no SDK files copied into a project's frontend".

## Target state

```
KitV2/
  ui-kit/                    # NEW first-class zone = mirror of ui-agent-kit sdk/ @ f9bdd9b
    AGENTS.md                # SDK's own AGENTS.md, shipped verbatim (autonomous)
    PIN.md                   # NEW: source, commit SHA, npm version, license, sync date, verification
    skills/                  # 7 Pi-native skills (name+description frontmatter)
    ui-rules/  patterns/  ux/  docs/  ui-sdk/   # knowledge + component code (mirrored)
    scenarios.json           # NEW: authored UI routing-quality contract
  .pi/extensions/
    kit-ui-router-core.ts    # NEW: shared UI index builder (single source ext+gate)
    kit-ui-router.ts         # NEW: registers search_ui_kit_resources (read-only tool)
  tools/sync-ui-kit.sh       # NEW: shipped, materializes ui-kit into a Wails frontend
  probes/ui-kit-sync/        # NEW: observable probe (fixture + sync + assertions)
  router/                    # UNCHANGED Go corpus (280 resources)
  .pi/settings.json          # UNCHANGED (["../rules","../recipes"]) — no UI skills loaded
.agent/
  kit-governance/23-zone-ui-kit.md   # NEW contract (Z13)
  kit-governance/README.md           # index row
  sync-ui-kit-from-upstream.sh       # NEW: metaproject re-sync helper (manual, gated)
  router/run_ui_scenarios.mjs        # NEW: UI ranking gate (reuses shared scoring + core)
  router/test_ui_router_*.py         # NEW: validator unit tests for the UI checks
```

Wails detection: `wails.json` at project root AND `frontend/` directory
(matching the ui-agent-kit CLI's own `findFrontendRoot` behavior).

## Files changed (product)

- `KitV2/ui-kit/**` (vendored, pinned) + `PIN.md` + `scenarios.json`
- `KitV2/.pi/extensions/kit-ui-router-core.ts`, `kit-ui-router.ts`
- `KitV2/tools/sync-ui-kit.sh`
- `KitV2/probes/ui-kit-sync/main.go`
- `KitV2/manifest.yaml` (capabilities + canonical entry `ui-kit: ui-kit/`)
- `KitV2/capabilities.yaml` (capability entry + `coverage.ui_kit_skills`)
- `KitV2/tools/validators/validate-kitv2.py` (additive: ui-kit frontmatter/
  scenario/disjointness checks; `coverage_counts()` gains `ui_kit_skills`)
- `KitV2/AGENTS.md` (Source-of-truth table row, Wails conditional section,
  Limits update)

## Files changed (metaproject)

- `.agent/kit-governance/23-zone-ui-kit.md` (Z13) + `README.md` index
- `.agent/router/run_ui_scenarios.mjs` + tests + negative tripwire
- `.agent/router/test_*.py` additions
- `.agent/sync-ui-kit-from-upstream.sh`
- `docs/plans/2026-08-07-ui-agent-kit-integration.md` (this file)
- `docs/evidence/2026-08-07/ui-agent-kit-integration/` (gate outputs)
- `.pi/memory/` (Decisions D-2026-08-07-XX, Gotchas, Progress, Brief)

## Execution steps (incremental; full gate after every step)

### Step 1 — Vendor the zone (content only)

- Copy `sdk/` from ui-agent-kit @ `f9bdd9b` (verified identical to npm
  `0.1.0` tarball's `sdk/`) into `KitV2/ui-kit/`; write `PIN.md`.
- Gate: `validate-kitv2.py` (must stay green — index globs do not touch
  `ui-kit/`), `build_index.py --check` (must stay up-to-date, proving the Go
  corpus is untouched), `go test ./...` unchanged.
- Verify: `find ui-kit -name "*.md" -size 0` empty; no `.agent/` strings;
  no accented-French content.

### Step 2 — Zone contract + metadata (first-class status)

- Write `Z13` contract: mission, format (mirror of pinned `sdk/`, never
  hand-edited, `AGENTS.md` verbatim, `PIN.md` mandatory), rules (UI corpus
  never indexed by the Go builder; UI skills never added to `.pi/settings.
  json`; re-sync = bump pin + full gate, never automatic), validation
  criteria (frontmatter, PIN, scenario linkage, disjointness).
- Extend `manifest.yaml`/`capabilities.yaml`; extend `coverage_counts()`
  with `ui_kit_skills`; add node-free checks (ui-kit SKILL.md frontmatter,
  `ui-kit/scenarios.json` schema+linkage, Go-index/UI-tree disjointness).
- Update `KitV2/AGENTS.md` (table row, Wails conditional section, Limits).
- Gate full + unit tests.

### Step 3 — UI routing runtime + ranking gate

- `kit-ui-router-core.ts`: `buildUiIndex(uiKitDir)` — walks `skills/`,
  `ui-rules/`, `patterns/`, `ux/`, `docs/`, `ui-sdk/docs/`,
  `ui-sdk/components-index.md`; tokenizes with the shipped stopwords
  (read from `router/meta.json`, single source); returns an `IndexFile`
  using the shared `Resource` type.
- `kit-ui-router.ts`: registers `search_ui_kit_resources` (typebox schema,
  same result formatting as the Go tool, explicit "no UI kit installed"
  message when the zone is missing); imports the shared scoring module.
- `ui-kit/scenarios.json`: ~6-8 realistic UI intents (Wails screen,
  login/settings dialog, macOS design, accessibility, spacing/typography,
  shadcn base) each with `expect` ids from the UI corpus + 1-2 offDomain
  (Go-only queries must be rejected).
- `.agent/router/run_ui_scenarios.mjs`: builds the UI index via the shared
  core, verifies ranking under the real scoring, asserts corpus disjointness
  (Go index ∩ ui-kit paths = ∅, UI index ⊆ ui-kit), negative tripwire tests
  (unreachable expectation → exit 1; stale id → exit 1).
- Extend `validate-kitv2.py` with the node-free UI scenario schema/linkage
  check (mirrors the two-layer rule for the Go contract).
- Re-run the 22 Go scenarios — must stay 22/22 (proof of zero
  cross-contamination).
- Update `router/README.md` and `.pi/README.md`.

### Step 4 — Sync tool + probe + re-sync process

- `tools/sync-ui-kit.sh`: detect Wails (`wails.json` + `frontend/`, or
  `--target`); materialize `ui-kit/` → `frontend/ui-kit/`; copy code pieces
  to `frontend/src/` per the SDK copy rules (mirror of the CLI's manifest);
  merge `frontend/.pi/settings.json` `skills: ["../ui-kit/skills"]`
  (create-if-missing, never destructive); refuse with exit 1 when no Wails
  frontend is detected (the "no trace" guarantee).
- `probes/ui-kit-sync/main.go`: fixture (`wails.json` + `frontend/`), run the
  sync tool, assert wiring + copies; assert refusal on a non-Wails fixture;
  PASS/FAIL verdicts.
- `.agent/sync-ui-kit-from-upstream.sh`: fetch ui-agent-kit @ new SHA, diff
  `sdk/` vs `KitV2/ui-kit/`, bump `PIN.md`, run the full gate. Documented in
  Z13 as the only update path (manual, revalidated, never automatic).
- Gate full (incl. `bash probes/run.sh`).

### Step 5 — Documentation, evidence, review, memory

- `docs/evidence/2026-08-07/ui-agent-kit-integration/` raw gate outputs.
- `.pi/memory/Decisions.md` (D-2026-08-07-04: integration decisions + rule 5
  reconciliation), `Gotchas.md` (npx ordering bug, no-tags pinning, identical
  npm tarball), `Progress.md`, `Brief.md`.
- Fresh-context review (read-only), integrate findings.
- End-to-end consumer verification: `install.sh` from the local tree into a
  temp dir → Wails fixture → sync tool → `pi -a` smoke (extension loads,
  both tools registered, Go vs UI queries non-polluted).

## Verification points

- [ ] `validate-kitv2.py` green before and after every step
- [ ] `build_index.py --check` up-to-date after every step (Go corpus
      byte-identical)
- [ ] Go scenarios 22/22 after every step
- [ ] UI scenarios green (new gate)
- [ ] Disjointness: Go index ∩ ui-kit = ∅, UI index ⊆ ui-kit
- [ ] `gofmt -l` empty · `go vet ./...` · `go test -race ./...` ·
      `golangci-lint run ./...` · `gosec` · `govulncheck` · `bash probes/run.sh`
      (full gate, end)
- [ ] Non-Wails Go project: no `.pi/settings.json` change, no skill loaded,
      `search_kit_resources` results identical
- [ ] Update propagation documented (manual re-sync + revalidation only)

## Open items for the owner

- None blocking. Notes: the npm CLI first-run bug is a ui-agent-kit repo
  proposal (separate), not part of this integration (mission rule 2).
