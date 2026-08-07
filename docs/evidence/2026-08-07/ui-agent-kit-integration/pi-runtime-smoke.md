# Pi runtime smoke — consumer copy (2026-08-07)

Setup: `rsync KitV2/ → /tmp/gak-consumer` (exact install.sh layout: KitV2
contents land at the consumer root). `pi -p -a --model deepseek/deepseek-v4-flash`
headless runs. All runs exit 0.

## 1. Extensions load; both routing tools registered

Prompt: "Which Pi tools do you have registered for finding kit resources?
List the tool names."

```
The kit-resource tools registered:

- **search_kit_resources** — routes Go/architecture/HTTP/DB/CLI/TUI tasks to Go Agent Kit resources (rules, recipes, catalogs, patterns, snippets)
- **search_ui_kit_resources** — routes UI tasks to the pinned ui-agent-kit SDK zone (Wails/React rules, patterns, skills)
```

No "Failed to load extension" errors. (Baseline before this wave reproduced
`Extension does not export a valid factory function` for the top-level
`kit-resource-router-scoring.ts` and aborted headless runs — fixed by
relocating shared modules to `.pi/extensions/shared/`, which Pi's loader
does not auto-discover: direct `*.ts` + one-level `index.ts` only.)

## 2. UI tool executes (runtime index build under jiti)

Prompt: call `search_ui_kit_resources` with query "wails login screen design".

```
1. [pattern] login (score 9.09) — ui-kit/patterns/login.md
2. [skill] ux-memory (score 4.26) — ui-kit/skills/ux-memory/SKILL.md
3. [doc] wails-constraints (score 3.62) — ui-kit/docs/wails-constraints.md
```

## 3. Non-pollution: Go corpus never returns UI paths

Prompt: call `search_kit_resources` with (1) "chi http router middleware"
(2) "wails login screen interface design"; report whether any path starts
with `ui-kit/`.

```
Query 1: [recipe] recipe-rest-chi -> recipes/recipe-rest-chi/SKILL.md (30.55)
         [catalog] chi -> knowledge/catalogs/libraries/chi/SKILL.md (27.79)
Query 2: [recipe] recipe-desktop-app -> recipes/recipe-desktop-app/SKILL.md (12.01)
         [anti-pattern] go-interface-everywhere -> ... (8.74)
ui-kit/ check: none of the returned paths start with ui-kit/
```

## 4. Regression baseline (pre-mission, HEAD~3 of this branch)

Consumer copy from `git archive HEAD~3 KitV2`: headless `pi -p -a` aborted
with the extension factory error — the defect was pre-existing; the shared/
relocation is a behavior-preserving fix that this wave's end-to-end smoke
requires.
