# Z13 — Zone `ui-kit/` (pinned ui-agent-kit SDK)

- **Metaproject Contract** — governs `KitV2/ui-kit/`: a pinned, verbatim
  mirror of the consumable SDK of the ui-agent-kit repository, its own
  `AGENTS.md`, the UI routing corpus and its quality contract, and the
  consumer-side sync tool.
- **Origin:** owner decision 2026-08-07 (native integration, first-class
  zone) — plan `docs/plans/2026-08-07-ui-agent-kit-integration.md`;
  investigation `docs/research/2026-08-07-ui-agent-kit-phase0-investigation.md`.

## 1. Mission

Give a Pi agent working on a **Wails desktop project** (Go + React frontend)
direct, complete access to the ui-agent-kit rules, components, and skills —
without ever polluting the context of a non-Wails Go project. The zone ships
with every install but is **inert until routed to**: no UI skill is loaded
into a Pi session by default, the Go routing corpus never contains UI
entries, and nothing is materialized into a project's `frontend/` unless a
Wails layout (`wails.json` + `frontend/`) is detected.

## 2. Roles and boundaries (inviolable)

| Element | Role | Owner |
| --- | --- | --- |
| `ui-kit/**` | Pinned mirror of upstream `sdk/` (AGENTS.md, skills/, ui-rules/, patterns/, ux/, docs/, ui-sdk/) | upstream ui-agent-kit (content); metaproject (pin) |
| `ui-kit/PIN.md` | Pin record: source repo, commit SHA, npm equivalence, license, sync verification, update path | metaproject (written at sync) |
| `ui-kit/copy-rules.json` | **Local-owned** copy rules (zone-relative src -> frontend-relative dst), regenerated at every re-sync from the upstream `cli/manifest.json` — the consumer sync tool reads it instead of hardcoding paths | metaproject (written at sync) |
| `ui-kit/scenarios.json` | **Authored** UI routing-quality contract (intent → expected top-K UI resources) | product; maintained under metaproject gate |
| `.pi/extensions/shared/kit-ui-router-core.ts` | **Single source of the UI index construction** (walk ui-kit tree → IndexFile); lives in `shared/` (not auto-discovered by the Pi extension loader) | kit (runtime) |
| `.pi/extensions/kit-ui-router.ts` | Native Pi tool `search_ui_kit_resources`, read-only; reuses the shared scoring module | kit (runtime) |
| `tools/sync-ui-kit.sh` | Shipped consumer helper: materialize the zone into a Wails project's `frontend/` (detect, copy, wire, never destructive) | kit (product) |
| `probes/ui-kit-sync/` | Observable probe: fixture → sync → assertions (PASS/FAIL) | kit (product) |
| metaproject re-sync helper + `run_ui_scenarios.mjs` + tests | Pin refresh and UI ranking gate (Node ≥ 23.6, reuses the shared scoring + UI core) | metaproject |

The UI corpus is a **separate routing domain**: the Go index
(`router/index.json`) never contains a `ui-kit/` path, and the UI index never
contains a path outside `ui-kit/`. The two tools never read each other's
corpus.

## 3. Rules

1. **Verbatim mirror, never hand-edited.** Every file under `ui-kit/` except
   `PIN.md` and `scenarios.json` is byte-copied from the pinned upstream
   `sdk/`. Local edits to SDK content are forbidden; needed changes are
   proposed to the ui-agent-kit repository (separate change) and arrive here
   through re-sync.
2. **Pinned source, never npm.** Content is sourced from the GitHub
   repository at a pinned commit SHA (git archive / clone of `sdk/`). The npm
   package is never used as a source. `PIN.md` records the SHA and the sync
   verification; a missing or inconsistent PIN is a validation error.
3. **Structure evolution is a re-sync concern, not a tooling concern.** The shipped `tools/sync-ui-kit.sh` reads `ui-kit/copy-rules.json` (local-owned, generated at re-sync from the upstream SDK's own `cli/manifest.json`): new folders, renames, or a different `sdk/` layout are covered by the next re-sync — the tool itself never hardcodes a source path. Its ownership manifest (`<frontend>/ui-kit/.owned.json`, path + sha256) guarantees nothing is destroyed: owned+unmodified files are refreshed, owned files dropped upstream are removed cleanly, and ANY consumer-modified or unowned file at a destination path is preserved and reported (refused). A zone missing its required shape (`AGENTS.md`, `skills/`, `ui-sdk/`) aborts the sync.
3. **Inert by default (context protection).** `ui-kit/skills` are NOT added
   to `.pi/settings.json`; the Go builder and `search_kit_resources` never
   index `ui-kit/`; the UI skills activate only when an agent works inside a
   Wails `frontend/` where the sync tool wired them, or when routed there by
   `search_ui_kit_resources` / the Wails section of the product AGENTS.md.
4. **Two routing domains, one scoring.** UI routing reuses the shared
   scoring implementation (`kit-resource-router-scoring.ts`) and the shipped
   stopwords (read from `router/meta.json`). Re-implementing scoring or
   tokenization for the UI corpus is release-blocking. Query-time synonyms
   may be extended only in the shared module, and every extension re-runs the
   22 Go scenarios (tripwire).
5. **Two-layer UI verification.** The product validator checks
   `ui-kit/scenarios.json` schema + expected-id linkage (node-free) and
   corpus disjointness; the metaproject gate verifies ranking under the real
   scoring. A UI scenario change must pass both.
6. **Wails-only materialization.** `tools/sync-ui-kit.sh` refuses (exit 1)
   unless a Wails frontend is detected (`wails.json` present and `frontend/`
   with a package.json) or an explicit `--target` points at one. It never
   deletes consumer files; it only adds/overwrites SDK-owned paths and merges
   `.pi/settings.json` conservatively.
7. **English only** (fundamental rule D-2026-08-05-21) and **no metaproject
   path markers** in shipped files (KVA-102 guard), including `PIN.md`.
8. **Update propagation is manual and gated** — see §4. Silent or automatic
   re-sync is forbidden.

## 4. Maintenance

The update path is **one workflow**: the metaproject prompt
`.pi/prompts/update-ui-kit.md` (run it when the user asks to update ui-kit)
drives the mechanical helper `.agent/sync-ui-kit-from-upstream.sh`, which
enforces the guardrails below. The workflow is manual (the maintainer
invokes it), gated (the helper RUNS the full gate), and reversible (a failed
gate rolls back with `git restore`). Never automatic, never silent.

**Pre-flight guardrails** (helper, before any write): the target SHA is a
well-formed 40-hex commit; `KitV2/ui-kit/` is clean in the working tree (a
dirty zone would be clobbered — abort); upstream resolves the SHA and
exposes `sdk/`.

**Sync scope**: only `KitV2/ui-kit/` is written (rsync), with the local-owned
files excluded (`PIN.md`, `scenarios.json`). Nothing outside the zone is
touched; nothing is committed automatically.

**Post-sync guardrails** (helper): upstream `sdk/` vs `ui-kit/` must differ
only in local-owned files; no `.go` file may enter the zone (the Go gate
would compile it); no metaproject path markers; no zero-byte `.md`;
English-only. Then the FULL gate runs inside the helper: validators
(instruction-artifacts, cognitive, kitv2), router index check, Go scenarios
22/22, UI scenarios, router unit tests, gofmt, go vet, go test -race,
probes. Any failure exits 1 with rollback instructions — the maintainer
never commits a red gate.

**After a green gate** (manual): review `git diff`, commit with the new SHA
in the message, record a dated decision in `.pi/memory/Decisions.md` and raw
evidence in `docs/evidence/YYYY-MM-DD/ui-kit-update/`, add Gotchas for any
upstream surprise. A fresh-context review is required for any non-trivial
jump.

- **Add or change a UI scenario**: must be a realistic UI agent intent
  (3–8 technical terms, one concern), target an id produced by the UI index
  builder, and be able to fail (padding is not admitted — same bar as Z11).
  Verify it under the metaproject gate AND the validator linkage check.
- **SDK content change needed** (rule in the SDK itself, a skill fix, a new
  component): open the change on the ui-agent-kit repository; after upstream
  acceptance, refresh the pin. Do not edit `ui-kit/` in place.

## 5. Patterns

- Zone = self-contained mirror with its own AGENTS.md (SDK autonomy clause
  preserved); GoAK never merges UI text into Go rules (single source stays
  upstream).
- Shared index-builder module imported by both the runtime tool and the gate
  (same "cannot drift" pattern as the scoring core).
- On-the-fly UI index (no committed generated artifact): the UI tree is the
  source of truth; nothing to regenerate, nothing to drift.

## 6. Anti-patterns

- Adding `ui-kit/skills` to `.pi/settings.json` (loads UI skills into every
  Go session — context pollution).
- Adding `ui-kit/**` to the Go builder globs (`INDEXABLE_GLOBS`) — merges the
  corpora.
- Editing SDK files in place, or re-syncing automatically/silently.
- Shipping a UI index.json as a generated artifact (two artifacts to drift).
- The sync tool overwriting consumer-owned files or skipping the Wails check.

## 7. Validation criteria (verifiable)

1. `PIN.md` exists with a well-formed pinned SHA and a sync date; validator
   cross-checks it against the zone's `AGENTS.md` presence.
2. Every `ui-kit/skills/*/SKILL.md` has `name` + `description` frontmatter
   (Pi-compat check; the kit facet fields are NOT required — the upstream SDK
   owns its frontmatter schema).
3. `ui-kit/scenarios.json` validates (schema + every expected id is produced
   by the UI index builder; node-free in the product validator).
4. Disjointness: no `router/index.json` entry has a path under `ui-kit/`; the
   UI index (as built by the shared core) contains only paths under `ui-kit/`.
5. Metaproject gate: UI scenarios rank correctly under the real scoring;
   negative tripwire tests (unreachable expectation → exit 1, stale id →
   exit 1) pass.
6. `tools/sync-ui-kit.sh` exits 1 on a non-Wails target and wires a Wails
   `frontend/` correctly (probe `ui-kit-sync`).
7. `ui-kit/copy-rules.json` exists, is a list of `{src,dst}` with every `src`
   present in the zone (node-free validator check), and is regenerated by the
   re-sync helper from the upstream `cli/manifest.json` — so a new upstream
   folder is copied by the consumer tool without a code change (probe).
8. The sync tool's ownership contract is probe-verified: idempotent refresh,
   clean removal of upstream-dropped SDK files, and preservation (refusal) of
   consumer-modified or unowned files at destination paths.

## 8. Open questions

- Whether the future `gak` CLI should expose the sync as `gak ui-kit sync`
  — deferred until the CLI exists (same as the rest of the distribution
  work).
