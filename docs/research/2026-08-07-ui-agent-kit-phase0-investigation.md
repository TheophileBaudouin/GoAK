# Phase 0 — Investigation: integrating ui-agent-kit into GoAK

Date: 2026-08-07
Author: agent session (Pi)
Status: complete — feeds the Phase 1 architecture decision

> Mission note on location: the mission brief asked for this report "in
> `references/` of GoAK". GoAK has no `references/` directory — that convention
> belongs to the ui-agent-kit repository. GoAK's governance (KIT_CHARTER, root
> AGENTS.md) homes research output under `docs/research/`, so this report lives
> there instead. Creating a top-level `references/` in GoAK would be a
> structural change requiring explicit approval (root AGENTS.md Modification
> Policy). Flagged for the owner in the Phase 1 presentation.

## 1. How Pi resolves `AGENTS.md` and `.pi/settings.json`

Verified against the installed Pi source (`@earendil-works/pi-coding-agent`
v0.84.1, `dist/core/*.js`), cross-checked with the shipped docs
(`README.md` §Context Files, `docs/usage.md`, `docs/settings.md`).

### `AGENTS.md` — layered walk-up, all files concatenated

`dist/core/resource-loader.js` → `loadProjectContextFiles(cwd)`:

- Loads the global `~/.pi/agent/AGENTS.md` (or `AGENTS.override.md` /
  `CLAUDE.md` variants), then walks **up** from the current working directory
  to the filesystem root, loading **one** context file per directory
  (`AGENTS.override.md` > `AGENTS.md` > `CLAUDE.md`).
- All matching files are **concatenated** — there is no "nearest wins"
  shadowing between levels (unlike Claude Code's override semantics). Every
  ancestor context applies, in root→cwd order.
- Directories **below** the cwd are never scanned.

**Consequence for the mission:** a nested `frontend/ui-kit/AGENTS.md` is only
loaded when Pi's session cwd is at or below `frontend/ui-kit/`. From a Wails
project root it is invisible to context loading. When it IS active it layers on
top of the GoAK root AGENTS.md (no suppression), unless an
`AGENTS.override.md` is introduced.

### `.pi/settings.json` and `.pi/skills|prompts|extensions|themes` — exactly cwd, no walk-up

- `dist/core/settings-manager.js` → `FileSettingsStorage`:
  `projectSettingsPath = <cwd>/.pi/settings.json`. The project settings file is
  resolved against the **exact** cwd only; there is no ancestor walk and no
  nested-project discovery.
- `dist/core/skills.js` → `loadSkills`: default skill dirs are
  `~/.pi/agent/skills` (user) + `<cwd>/.pi/skills` (project). Same exact-cwd
  rule for prompts, extensions, themes (`resource-loader.js`).
- Paths inside `.pi/settings.json` resolve relative to `.pi`
  (`docs/settings.md`): GoAK ships `{"skills": ["../rules", "../recipes"]}`,
  ui-agent-kit writes `{"skills": ["../ui-kit/skills"]}` — both land in the
  sibling folder next to `.pi`.
- Project trust gates `<cwd>/.pi` resources (settings, extensions, skills);
  trust decisions are stored per-directory path in `~/.pi/agent/trust.json`
  with parent fallback (`dist/core/trust-manager.js`).

**Consequence for the mission:** `frontend/.pi/settings.json` and
`frontend/ui-kit/skills` (written by the ui-agent-kit installer) are active
**only when Pi's cwd is `frontend/`** (or below). From the Wails project root,
Pi does not discover them natively.

**Bottom line for architecture selection:** a "scoped pointer" architecture is
viable, but the scoping is **not automatic Pi discovery** from the project
root. It requires an explicit pointer in the root GoAK surface (AGENTS.md
and/or router guidance) that tells the agent: "if this is a Wails project, the
UI rules/skills live at `frontend/ui-kit/…`, read `ui-kit/AGENTS.md`, and
either `cd frontend` for native skill activation or read the SKILL.md files
directly". Both variants keep the two corpora textually separate.

## 2. What breaks in `npx ui-agent-kit`

Reproduced end-to-end on a disposable Wails-shaped project
(`/tmp/wails-test/` with `wails.json` + `frontend/package.json` Vite+React).

- The package **exists on npm**: `ui-agent-kit@0.1.0` (latest, published
  2026-08-06, 1.0 MB unpacked, `bin: ui-agent-kit`). Not a registry/package
  problem.
- **First run on a fresh frontend fails the frozen-base step:**
  `npx shadcn@latest add --all --yes` errors with
  `Failed to load tsconfig.json. Couldn't find tsconfig.json`.
  Root cause is an **ordering bug** in `cli/index.js`:
  `ensureBase()` (step 3) runs shadcn **before** `applyConfigs()` (step 5)
  creates `tsconfig.json` / `vite.config.ts`.
- **The failure is silent**: `cli/lib/base.js` catches the non-zero exit,
  logs "shadcn add failed — the kit needs the frozen base to compile", and
  returns `{installed: false}`; the install continues and prints
  "Done ✔ … (base failed — see error above)"; **the process exits 0**. An
  agent or script cannot detect the failure from the exit code.
- **Second run succeeds**: tsconfig.json now exists, shadcn adds 62
  components, `doctor` reports all green. So the breakage is first-run-only
  but misreported as success — structurally unreliable, not a missing
  dependency.
- The repo's own test suite (`npm test`, 11 tests) **passes** — it stubs the
  base step, so the first-run e2e failure is not covered.

Verdict: the breakage is a fixable CLI ordering + error-handling defect
(proposal for the ui-agent-kit repository, NOT part of the GoAK integration —
mission rule 2). The GitHub-source fallback (clone / sparse-checkout /
`git archive` at a pinned ref) is not needed to bypass the npm packaging —
the npm tarball contains `cli/`, `sdk/`, `README.md` — but it remains the
mandated sourcing path for the SDK content.

## 3. GoAK's routing mechanism (as built today)

- **Builder** (metaproject tool): `.agent/router/build_index.py` (Python,
  PyYAML) walks fixed zones of `KitV2/` — `rules/**/SKILL.md`,
  `recipes/**/SKILL.md`, `knowledge/catalogs/**/SKILL.md`,
  `knowledge/**/*.yaml`, `snippets/*/SNIPPET.yaml`, `templates/*/template.yaml`,
  `.pi/prompts/*.md`, `.pi/skills/**/SKILL.md` — and emits a deterministic
  `KitV2/router/index.json` (`{schema:1, resources:[{id,kind,path,description,
  tags,terms}]}`) plus `meta.json` (version, `index_sha256`, per-kind counts,
  stopwords). `--check` re-derives the index and fails on drift.
- **Runtime**: `.pi/extensions/kit-resource-router.ts` registers the
  `search_kit_resources` tool. It loads `../../router/index.json` relative to
  the extension file — in a consumer install that is `<project>/router/`.
  Scoring lives in `kit-resource-router-scoring.ts` (single shared
  implementation, imported by the metaproject gate `.agent/router/
  run_scenarios.mjs` — 22 scenarios, 22/22 PASS at baseline).
- **Registration of new content**: add files under an indexable zone →
  rebuild the index → the drift gate and the scenario gate must stay green.
  Product validator (`validate-kitv2.py`) also checks the router index and
  scenario id linkage (node-free).
- **Baseline captured 2026-08-07**: index up to date, 280 resources; scenarios
  22/22; `validate-kitv2.py` PASS (73 product skills).

**Constraints for the integration:** the index is a single merged Go corpus
today; the mission requires a **separate** UI corpus (no shared index, no
cross-contamination). Any extension/scoring change must preserve the
"single scoring implementation" rule (D-2026-08-06-11) and the two-layer gate.
The extension's `dir` resolution (`../../router/`) is product-scoped; a second
corpus needs its own index location + loader, or a second tool.

## 4. What the ui-agent-kit installer writes to `.pi/settings.json`

Read from the cloned repo (`cli/index.js`, `cli/lib/configs.js`,
`cli/lib/copy.js`, `cli/manifest.json`, `sdk/`).

- `mergePiSettings(frontendRoot)` creates/merges `<frontend>/.pi/settings.json`
  to exactly:

  ```json
  { "skills": ["../ui-kit/skills"] }
  ```

  Paths resolve relative to `.pi` → `<frontend>/ui-kit/skills` (7 Pi-native
  skills: frontend-design, macos-design-guidelines, shadcn, ui-review,
  ux-memory, web-design-guidelines, web-platform-guidelines). Merge is
  conservative (existing entries preserved, invalid JSON backed up).
- The entire `sdk/` folder is mirrored to `<frontend>/ui-kit/` (copy rule
  `{from:"sdk", to:"ui-kit"}`), including `sdk/AGENTS.md` →
  `ui-kit/AGENTS.md` (an **autonomous** instruction file that explicitly never
  references the metaproject), `ui-rules/`, `patterns/`, `ux/`, `docs/`,
  `skills/`, `ui-sdk/` code.
- Code pieces are additionally copied to `src/components` (+ example),
  `vite.config.ts` / `tsconfig.json` created when missing, `components.json`
  (radix-nova harvest registries) + shadcn base, npm deps (echarts, recharts,
  motion, @tabler/icons-react, react-medium-image-zoom), and
  `ui-kit/.ui-agent-kit.json` installed manifest.
- **The `.pi/settings.json` format is identical to GoAK's** (native Pi
  `skills` array, paths relative to `.pi`) — no conversion layer is needed for
  Pi discovery. The only gating factor is Pi's exact-cwd scoping (point 1):
  the wiring is effective only when the agent works with cwd = `frontend/`.
- **Pinning:** the ui-agent-kit repository has **no git tags**; npm version is
  0.1.0. A "pinned ref" for vendorization must therefore be a **commit SHA**
  (e.g. the current `main` HEAD), matching how GoAK pins its own refs.

## Other facts relevant to the decision

- GoAK explicitly declares Wails frontend **out of scope** in
  `KitV2/AGENTS.md` §Limits ("full desktop-application wiring (Wails)…
  or non-Go domains"). Integrating the SDK as a separate, conditionally-active
  corpus is consistent with that boundary; merging UI rules into GoAK rules/
  would violate it.
- Skill-name collision check between the two corpora: GoAK ships 8 Pi skills,
  ui-agent-kit ships 7 — no name overlap (verified by listing both
  `sdk/skills/*/SKILL.md` and `KitV2/.pi/skills/*/SKILL.md`).
- Wails detection signals available at project root: `wails.json` + `frontend/`
  directory (+ `frontend/package.json` with Vite+React). The ui-agent-kit CLI
  itself auto-detects `frontend/` via `findFrontendRoot`.

## Sources consulted

- Pi v0.84.1 source: `dist/core/resource-loader.js`, `dist/core/settings-manager.js`,
  `dist/core/skills.js`, `dist/core/trust-manager.js`, `dist/main.js`;
  `README.md` §Context Files; `docs/usage.md`; `docs/settings.md`.
- ui-agent-kit repo (cloned at HEAD, no tags): `cli/index.js`,
  `cli/lib/{base,configs,copy}.js`, `cli/generate-manifest.js`,
  `cli/manifest.json`, `sdk/AGENTS.md`, `sdk/.pi/settings.json`,
  `governance/{constitution,phases}.md`, root `AGENTS.md`.
- GoAK repo: `KitV2/AGENTS.md`, `.agent/router/build_index.py`,
  `KitV2/.pi/extensions/kit-resource-router.ts`,
  `KitV2/.pi/extensions/kit-resource-router-scoring.ts`,
  `KitV2/router/{index,meta,scenarios}.json`, `install.sh`.
- npm registry: `npm view ui-agent-kit`.
- Reproduction artifacts: `/tmp/ui-agent-kit/` (clone), `/tmp/wails-test/`
  (disposable Wails-shaped project, install logs).
