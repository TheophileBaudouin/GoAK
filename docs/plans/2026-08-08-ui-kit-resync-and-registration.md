# Plan — ui-agent-kit re-sync + single registration point (2026-08-08)

## Goal

Integrate the updated ui-agent-kit SDK into GoAK (KitV2) the way the owner
mission defines: re-sync the pinned `ui-kit/` zone from upstream, register
the UI skills through the root `.pi/settings.json` (single registration
point — the previous state relied on a nested SDK settings file and router
entries only), keep activation strictly conditional for non-Wails Go
projects, prove Go/UI router separation, and leave a reusable, gated sync
procedure plus governance.

## Context

- The upstream ui-agent-kit repo jumped `f9bdd9b` → `cd00eb5d` (+5392 lines:
  agent chat + assistant-ui component families, agent-chat pattern + example,
  CONSUMPTION/design-decisions/screens updates; npm 0.1.1).
- A first attempt (2026-08-07) had copied the SDK into `KitV2/ui-kit/` with
  its own AGENTS.md and `.pi/` but without root registration — Pi does NO
  automatic discovery by directory; a skills folder is only loaded when an
  already-loaded `.pi/settings.json` references it. The native integration
  session fixed most of this (Z13, router tool, AGENTS.md section, probes);
  this mission completes the registration (settings.json fusion) and
  re-syncs the new content.
- `npx ui-agent-kit` is broken (documented gotcha) — sourcing is
  GitHub-direct at a pinned SHA only, never npm. No git tags upstream → pin
  by commit SHA (HEAD `cd00eb5d`, npm 0.1.1 tarball `sdk/` verified
  byte-identical, `diff -rq` empty).

## Constraints

- Never modify upstream ui-agent-kit source.
- The GoAK validation gate must never regress.
- Commit and document after each step.
- The audit prompt stays non-destructive (it detects drift, never syncs).

## Decisions

- **D-2026-08-08-01**: re-pin zone to `cd00eb5d` (ui-agent-kit 0.1.1).
- **D-2026-08-08-02**: single registration point — root
  `KitV2/.pi/settings.json` declares `../ui-kit/skills` (additive); the
  nested `ui-kit/.pi/settings.json` is dead (deleted + excluded from
  re-syncs). Supersedes the earlier inert-by-default stance (Z13 §3.3/§6,
  capabilities.yaml updated).
- **D-2026-08-08-03**: kit-audit gains a read-only ui-kit dimension (C16) +
  Phase E row; registration integrity becomes a mechanical validator gate
  (`check_ui_kit_registration` + 4 unit tests).

## Steps executed

1. **Re-sync** via the sanctioned helper
   `.agent/sync-ui-kit-from-upstream.sh cd00eb5d…` — full gate PASS inside
   the helper (validators, Go 22/22, UI 9/9, 44 router tests,
   gofmt/vet/test-race, probes 16/16). commit `d15574f`.
2. **Registration fusion**: root settings.json += `../ui-kit/skills`;
   `ui-kit/.pi/settings.json` deleted; helper `EXCLUDES` +=
   `.pi/settings.json` (never resurrected); PIN.md, Z13, capabilities.yaml,
   AGENTS.md reworded; update-ui-kit prompt notes the single registration
   point; Decisions.md D-2026-08-08-01..03. commit `edc52c1`.
3. **Kit-audit dimension** C16 (read-only pin/drift/registration checks) +
   Phase E row + `check_ui_kit_registration` validator gate (4 tests).
   commit `e4bf4fd`.
4. **Routing fixes surfaced by the new content** (shared scoring, Z11
   protocol): off-domain rejection now uses raw query vocabulary (synonym
   expansions can no longer flip an in-domain query off-domain); the
   components-index resource now indexes the catalog TABLE names, so the
   new agent/assistant-ui families are routable. scenarios.json +2
   (agent-chat, assistant-ui) — both would have failed before the fixes.
   UI gate 11/11, Go gate 22/22, 44 router tests incl. tripwire. commit
   `f5bc710`.
5. **Memory + evidence**: Agent.md durable rule (registration is mandatory,
   never assumed), Gotchas entry (off-domain/synonym + truncated-catalog
   indexing), consumer Pi smoke test with `pi -p -a` (trust): all 7 UI
   skills discovered, Go router returns no ui-kit path, UI router returns
   agent-chat + components-index with no path outside ui-kit/.

## Done

- `KitV2/ui-kit/` pinned at `cd00eb5d` with the new content.
- Root `.pi/settings.json` fused (additive); nested SDK settings file dead
  and excluded from re-syncs.
- AGENTS.md pointer section (conditional, Wails-only) in place.
- Router proof: Go query → Go corpus (no ui-kit path), UI query → UI corpus
  (agent-chat first, no path outside ui-kit).
- Reusable gated sync: `.agent/sync-ui-kit-from-upstream.sh` (manual +
  kit-audit C16 drift detection routing to the `update-ui-kit` workflow).
- Governance: Z13 updated (rules 1-9, roles, §9 past-mistake reminder,
  catalog-table pattern), Decisions.md D-2026-08-08-01..03.
- Full gate PASS (2026-08-08): validators ×3, router index check, Go 22/22,
  UI 11/11, 44 router tests, gofmt/vet/lint 0, test-race, gosec 0,
  govulncheck 0, probes 16/16.

## Evidence

- `docs/evidence/2026-08-08/ui-kit-resync-and-registration/`
  (`full-gate.log`, `consumer-pi-smoke.txt`).
