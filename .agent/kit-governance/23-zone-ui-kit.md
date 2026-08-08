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
without polluting the context of a non-Wails Go project. The UI skills are
**registered** in the root `KitV2/.pi/settings.json` (single registration
point) so a Wails-project agent can discover them, but they are **inert by
description**: their frontmatter scopes them to UI work and the product
AGENTS.md "Wails projects" section tells the agent to ignore them for plain
Go projects. The Go routing corpus never contains UI entries, and nothing is
materialized into a project's `frontend/` unless a Wails layout
(`wails.json` + `frontend/`) is detected.

## 2. Roles and boundaries (inviolable)

| Element | Role | Owner |
| --- | --- | --- |
| `ui-kit/**` | Pinned mirror of upstream `sdk/` (AGENTS.md, skills/, ui-rules/, patterns/, ux/, docs/, ui-sdk/) | upstream ui-agent-kit (content); metaproject (pin) |
| `ui-kit/PIN.md` | Pin record: source repo, commit SHA, npm equivalence, license, sync verification, update path | metaproject (written at sync) |
| `ui-kit/copy-rules.json` | **Local-owned** copy rules (zone-relative src -> frontend-relative dst), regenerated at every re-sync from the upstream `cli/manifest.json` — the consumer sync tool reads it instead of hardcoding paths | metaproject (written at sync) |
| `ui-kit/scenarios.json` | **Authored** UI routing-quality contract (intent → expected top-K UI resources) | product; maintained under metaproject gate |
| `KitV2/.pi/settings.json` | **Single Pi skill registration point**: declares `../rules`, `../recipes`, `../ui-kit/skills`. The nested `ui-kit/.pi/settings.json` is dead by design (excluded from re-syncs) — no second registration source | kit (product) |
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
4. **Registered once, inert by description (activation is conditional).** `ui-kit/skills` ARE declared in the root `KitV2/.pi/settings.json` (single registration point, owner decision 2026-08-08). The SDK's own nested `ui-kit/.pi/settings.json` is dead: deleted from the zone and excluded from re-syncs, so it can never be mistaken for a registration source. Discoverability is unconditional; ACTIVATION is conditional — skill descriptions scope them to Wails/UI work, the Go builder and `search_kit_resources` never index `ui-kit/`, and nothing is materialized into a project's `frontend/` unless the sync tool detects a Wails layout.
5. **Two routing domains, one scoring.** UI routing reuses the shared
   scoring implementation (`kit-resource-router-scoring.ts`) and the shipped
   stopwords (read from `router/meta.json`). Re-implementing scoring or
   tokenization for the UI corpus is release-blocking. Query-time synonyms
   may be extended only in the shared module, and every extension re-runs the
   22 Go scenarios (tripwire).
6. **Two-layer UI verification.** The product validator checks
   `ui-kit/scenarios.json` schema + expected-id linkage (node-free) and
   corpus disjointness; the metaproject gate verifies ranking under the real
   scoring. A UI scenario change must pass both.
7. **Wails-only materialization.** `tools/sync-ui-kit.sh` refuses (exit 1)
   unless a Wails frontend is detected (`wails.json` present and `frontend/`
   with a package.json) or an explicit `--target` points at one. It never
   deletes consumer files; it only adds/overwrites SDK-owned paths and merges
   `.pi/settings.json` conservatively.
8. **English only** (fundamental rule D-2026-08-05-21) and **no metaproject
   path markers** in shipped files (KVA-102 guard), including `PIN.md`.
9. **Update propagation is manual and gated** — see §4. Silent or automatic
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
files excluded (`PIN.md`, `scenarios.json`, `copy-rules.json`) plus the dead
`.pi` dir (D-2026-08-08-02). Nothing outside the zone is touched; nothing is
committed automatically.

**Root AGENTS.md UI section (delegation, owner rule 2026-08-08, revised
2026-08-08, D-2026-08-08-19)**: `KitV2/AGENTS.md` carries a condensed "UI
work" section that declares the activation guard, the routing obligation,
and the cross-cutting invariants, and delegates every other UI instruction
to `ui-kit/AGENTS.md` — the single canonical source; the root never mirrors
the SDK. The section carries a checksum marker (hash of the pinned
`ui-kit/AGENTS.md`) in its HTML comment. The helper's post-sync guardrails
FAIL when `ui-kit/AGENTS.md` changed but the marker was not refreshed — the
maintainer must re-verify the condensed section against the new SDK
instructions before the sync can finish. Instructions are never lost: they
live in `ui-kit/AGENTS.md`, which the root obliges the agent to read.

**Post-sync guardrails** (helper): upstream `sdk/` vs `ui-kit/` must differ
only in local-owned files; the UI-section checksum marker matches the synced
`ui-kit/AGENTS.md`; no `.go` file may enter the zone (the Go gate would
compile it); no metaproject path markers; no zero-byte `.md`; English-only.
Then the FULL gate runs inside the helper: validators (instruction-artifacts,
cognitive, kitv2), router index check, Go scenarios 22/22, UI scenarios,
router unit tests (stdlib unittest), gofmt, go vet, golangci-lint,
go test -race, gosec, govulncheck, probes. Any failure exits 1 with
rollback instructions — the maintainer never commits a red gate.

**After a green gate** (manual): review `git diff` (including
`KitV2/AGENTS.md` — the condensed UI section), commit with the new SHA in the
message (include `KitV2/AGENTS.md` when its section changed), record a dated
decision in `.pi/memory/Decisions.md` and raw evidence in
`docs/evidence/YYYY-MM-DD/ui-kit-update/`, add Gotchas for any upstream
surprise. A fresh-context review is required for any non-trivial jump.

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
- The component catalog table (`ui-sdk/components-index.md`) is the routing
  surface for component NAMES: the builder indexes the table rows into the
  single `components-index` resource so newly added families (agent/,
  assistant-ui/) are discoverable by name without per-component resources
  (D-2026-08-08).

## 6. Anti-patterns

- Duplicating skill registration (a nested `ui-kit/.pi/settings.json` that
  re-declares the skills, or any second settings file that claims to be the
  registration source) — the root `KitV2/.pi/settings.json` is the single
  registration point; the nested SDK file stays dead (deleted + excluded
  from re-syncs).
- Letting the UI corpus into the Go builder globs (`INDEXABLE_GLOBS`) or the
  Go corpus into the UI index — the corpora never mix.
- Editing SDK files in place, or re-syncing automatically/silently.
- Shipping a UI index.json as a generated artifact (two artifacts to drift).
- The sync tool overwriting consumer-owned files or skipping the Wails check.
- Copying the SDK into `KitV2/` and stopping there — a folder with its own
  AGENTS.md/.pi is invisible to Pi until registered (see §9).

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
9. Registration integrity: the root `KitV2/.pi/settings.json` declares
   `../ui-kit/skills` and the zone contains NO nested `ui-kit/.pi/settings.json`
   (single registration point; the re-sync helper excludes `.pi/settings.json`
   so upstream's copy is never resurrected).

## 9. Past mistake — do not repeat

In a first attempt (2026-08-07, pre-native-integration) the ui-agent-kit
SDK was copied into `KitV2/ui-kit/` with its own `AGENTS.md` and its own
`.pi/` but **registered nowhere**. Pi performs NO automatic discovery by
directory: a folder of skills is only loaded when an already-loaded
`.pi/settings.json` references it (`{ "skills": ["../skills"] }`). The
result was content that was invisible to the agent — the copy existed, but
nothing could route to it. The native integration fixed this by registering
the zone (router tool, AGENTS.md pointer section, and — since 2026-08-08 —
the root `settings.json` fusion).

**Rule: copying a folder that carries its own AGENTS.md and its own `.pi/`
does NOT integrate it. Any integration of external content must include an
explicit registration step (skills config, AGENTS.md entry, router entry)
verified concretely afterwards — never assumed.**

## 8. Open questions

- Whether the future `gak` CLI should expose the sync as `gak ui-kit sync`
  — deferred until the CLI exists (same as the rest of the distribution
  work).
