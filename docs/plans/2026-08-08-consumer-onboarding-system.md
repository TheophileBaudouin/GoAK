# Plan — Consumer onboarding & knowledge system (docs + /goak + banner)

- **Date:** 2026-08-08
- **Type:** kit structuring feature (consumer-facing), metaproject rules + audits
- **Goal / Context / Constraints / Done** framing per work protocol.

## Goal

A fresh consumer who installs the Go Agent Kit and opens Pi must be able,
without any knowledge of the build repository, to:

1. see a small onboarding banner at session start (`/reload`) that says what
   to do now (Get Started / large feature / small feature);
2. type `/goak` and get the agent to read the kit's **local** user guide and
   explain it;
3. find all deep usage info in a shipped, LLM-native micro-documentation.

And durably: any future kit change must naturally trigger a documentation /
banner / audit review (`kit audit` verifies the whole surface).

## Context (verified facts)

- The consumable product is the `KitV2/` tree (install.sh extracts exactly
  `KitV2/` with prefix stripped; consumer root = KitV2 content). Anything
  under `KitV2/` ships; anything outside is metaproject.
- Consumer `.pi` = `KitV2/.pi/`: `settings.json` (skills only), `prompts/*.md`
  (auto-discovered by Pi, filename = command), `skills/*/SKILL.md`,
  `extensions/*.ts` (auto-discovered by Pi after trust; top-level `*.ts`
  only, `shared/` subdir for non-extensions), `README.md`.
- Pi prompt templates: `.pi/prompts/goak.md` → `/goak`; frontmatter
  `description` (+ optional `argument-hint`); loading is non-recursive.
- Pi extension events: `session_start` with `reason: "startup" | "reload" |
  "new" | "resume" | "fork"`; TUI widget via `ctx.ui.setWidget(key, lines[])`
  (persistent banner, idempotent per key); `ctx.hasUI` false in print mode.
- Real workflows to document (from KitV2/AGENTS.md, .pi/README, prompts):
  - large-scale transformations → `spec-driven-dev` skill (7 phases);
  - ordinary non-trivial work → native skills/prompts of `.pi/`
    (`checklist-*`, `workflow-memory`);
  - day-0 foundation → `workspace-init` (before first feature);
  - UI work (Wails only) → `search_ui_kit_resources` + `ui-kit/` zone;
  - routing is mandatory → `search_kit_resources` before technical work;
  - memory: verify which `.pi/memory/` files exist (Decisions.md may be
    missing); validation gate from AGENTS.md.
- `kit audit` = metaproject prompt `.pi/prompts/kit-audit.md` (not shipped).
  Dimensions C1–C17; C13 requires every `.pi/prompts/*.md` to be router
  indexed; C9/C15 require absolute instructions on consumer process surfaces
  to be registered in `.agent/instructions.md`.
- Mechanical gates that touch the new surface:
  - `validate-kitv2.py`: `check_router` (index regen needed for a new
    prompt), `check_no_metaproject_paths` (9 markers, IGNORECASE, scans all
    shipped files incl. `.md`/`.ts`), `check_empty_markdown`,
    `check_workspace_init_placeholder` (marker-section pattern);
  - `validate-instructions.py`: prompts need a `description`; forward
    absolute check scans only the lexeme "mandatory" on process surfaces
    (AGENTS.md, prompts, skills, extensions).
- Consumer AGENTS.md merge-sections convention (N1 §5.1, gotcha 2026-08-08):
  any injected AGENTS.md section MUST be marker-delimited AND covered by a
  dedicated mechanical check.

## External research (sources)

- Diátaxis (diataxis.fr): task-oriented docs; how-to = goal-oriented
  directions, one job at a time, least prose.
- llms.txt convention (llmstxt.org / llmtxt.info): fixed predictable
  structure — H1 + short summary + H2 sections; curated reading list for a
  small context window; parseable by regex.
- llmbestpractices.com (technical-writing-standards, documentation-for-ai):
  docs have two readers (human + LLM); task-first, one job per page, exact
  runnable examples, precise consistent terms, versioned and tested like
  code; honest capability limits; dated facts.
- Google developer style (prescriptive docs, timeless docs): "must"/"can"/
  "might" instead of "should"; avoid time-sensitive words ("now", "new").
- Anti-patterns (docmd avoiding-anti-patterns, ninadpathak): vague
  instructions, bloated examples, content debt, stale docs, undocumented
  commands.

### Principles applied

1. Task-first, numbered steps, exact commands/paths, preconditions.
2. Decision tables ("if X then Y") for workflow selection.
3. No marketing, no "should" — use must/can/might and plain imperative.
4. Timeless wording (no versions, no "now"), every named command/path
   verified against the current tree.
5. Local source of truth: `/goak` forces reading `.pi/docs/GOAK.md`;
   the banner only points; `kit audit` + validator make it an invariant.

## Design decisions (recorded in .pi/memory/Decisions.md as D-2026-08-08-14..17)

- **D-14 — Docs location: `.pi/docs/GOAK.md`** (single file). NOT a root
  `docs/` folder: consumer workflows (spec-driven-dev) create the consumer's
  own `docs/` at the project root; the installer merges kit files into that
  same root, so a shipped `docs/` would collide with consumer-owned docs.
  `.pi/` is the shipped Pi surface whose README already documents path
  contracts, and both consumers of the guide (`/goak`, banner) live there.
  Z8 amended: `.pi/` gains a docs role (user guide) besides
  settings/prompts/skills/extensions.
- **D-15 — `/goak` is a prompt template** (`.pi/prompts/goak.md`), not an
  extension command: Pi-native, zero code, filename = command; it does not
  inline the docs — it orders the agent to read the local file, then answer,
  then invite follow-up questions. Z8 naming rule amended: entry-point
  commands may use non `workflow-*`/`checklist-*` names.
- **D-16 — Banner = tiny project-local extension + data file**:
  `KitV2/.pi/extensions/kit-onboarding.ts` renders
  `KitV2/.pi/onboarding/banner.md` as a TUI widget on `session_start` with
  `reason: startup | reload` only, guarded by `ctx.hasUI`; silent no-op when
  the file is missing. Content stays out of code (single source for the
  displayed text; mechanically auditable). No network, no background
  process, no state.
- **D-17 — AGENTS.md "User guide" pointer section** delimited by
  `<!-- user guide section: begin/end -->` + title, enforced by a new
  validator check `check_consumer_onboarding` (same pattern as
  `check_workspace_init_placeholder`, N1 §5.1). No version bump / no release
  in this change (not requested); router meta stays at manifest 2.6.0.

## Files

### Created (consumer — shipped)

1. `KitV2/.pi/docs/GOAK.md` — user guide: summary, Get Started (numbered
   steps + verification), commands table, workflow decision table (small /
   large / foundation / UI), structure map, finding capabilities, working
   rules, troubleshooting. LLM-native, compact (~150 lines), English, no
   metaproject markers.
2. `KitV2/.pi/prompts/goak.md` — `/goak`: read `.pi/docs/GOAK.md` first,
   explain from it, point to sections, answer, invite follow-up. No
   "mandatory" lexeme (registry-avoidant); description required.
3. `KitV2/.pi/onboarding/banner.md` — 3 entries (GET STARTED / NEW FEATURE
   large / NEW FEATURE small) + `/goak` pointer; plain short lines.
4. `KitV2/.pi/extensions/kit-onboarding.ts` — session_start widget renderer
   (startup/reload, hasUI guard, silent fallback).

### Modified (consumer)

1. `KitV2/.pi/README.md` — document docs/ + onboarding/ roles.
2. `KitV2/AGENTS.md` — "User guide" marker section + one line in Workflow
   about `/goak`.
3. `KitV2/.pi/extensions/types/pi-env.d.ts` — add editor-only stubs for
   `pi.on` / `ctx.ui.setWidget` / minimal ExtensionContext (types/ is never
   loaded by Pi).
4. `KitV2/tools/validators/validate-kitv2.py` — `check_consumer_onboarding()`
   wired into `main()`: guide exists + has Get Started + deep sections;
   goak.md exists + references `.pi/docs/GOAK.md` (no stale path); extension
   exists + `session_start`/`setWidget` markers; banner exists + 3 entry
   markers + `/goak` pointer; AGENTS.md marker section present.
5. `KitV2/tools/validators/test_validate_kitv2.py` — positive + negative
   tests for the new check.
6. `KitV2/router/index.json` + `meta.json` — regenerated (prompt 3→4) via
    `.agent/router/build_index.py`.

### Modified (metaproject — not shipped)

1. `.agent/kit-governance/17-zone-pi.md` (Z8) — .pi surface table gains
    extensions/docs/onboarding; prompt naming rule amended (entry-point
    commands allowed); docs-maintenance rule.
2. `.agent/kit-governance/18-zone-agents.md` (Z9) — note the new marker
    section + its check in §3/§4.
3. `.pi/prompts/kit-audit.md` — new dimension C18 "Consumer onboarding
    system" + Phase E gaps row.
4. `.agent/instructions.md` — register the guide's key absolutes
    (guidance-only row naming `KitV2/.pi/docs/GOAK.md`).
5. Root `AGENTS.md` — "Consumer documentation" rule (docs are shipped
    source of truth; every kit change must check docs//goak/banner/audit).
6. `.pi/memory/Agent.md` — new section "Consumer documentation &
    onboarding maintenance" (before/during/after workflow).
7. `.pi/memory/Decisions.md` — D-2026-08-08-14..17 (+ no-release note).
8. `.pi/memory/Progress.md` + `Brief.md` — task + architecture line.

### Not changed (explicit)

- `KitV2/.pi/settings.json` — extensions and prompts auto-discover; no
  registration needed (single-registration-point rule untouched).
- `install.sh` — installer "next steps" stays; the guide is the Get Started.
- Manifest/capabilities version — no release in this change.
- Router scenarios — existing 22+9 stay green; no new scenario (the guide
  is not a routing resource; out of scope).

## Validation

From `KitV2/`:

- `python3 ../.agent/validators/validate-instructions.py`
- `python3 tools/validators/validate-kitv2.py`
- `python3 ../.agent/router/build_index.py` (regenerate) then
  `.agent/router/run_scenarios.mjs` (Go 22) + `run_ui_scenarios.mjs` (UI 9)
- `python3 -m unittest discover -q` in `KitV2/tools/validators`
- go gate (gofmt/vet/lint/test) — untouched Go, but run to be safe
- Consumer Pi smoke: temp consumer copy → `pi -p -a` registers no new tool,
  `/goak` prompt discoverable; interactive widget cannot be asserted
  headless — verified by reading the extension + validator markers
  (documented limitation).

## Done when

- Checklist of mission §18 all checked; validator + gates green; fresh
  read-only review APPROVE; memory + decisions recorded.
