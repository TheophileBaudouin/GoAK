# Consumption guide — ui-agent-kit

> How to use `ui-sdk/` in a real Wails app (or any React + Vite + TS project). This is the
> contract every consumer must follow. Verified 2026-08-06.

## Single-command install (recommended)

```bash
npx ui-agent-kit          # install: copy SDK, install base + deps, wire configs
npx ui-agent-kit update   # refresh when a newer version is published
npx ui-agent-kit doctor   # check prerequisites
```

The installer is the source of truth for the copy rules below. It is idempotent (re-running
never deletes consumer files), detects your package manager and Wails `frontend/` layout,
and verifies every `@/` import after copying. Flags: `--skip-base`, `--skip-deps`,
`--target <dir>`, `--force`.

**Install layout** — the **entire `sdk/` folder is mirrored to `ui-kit/`** (reference copy:
components, blocks, rules, patterns, ux, skills, docs, configs — nothing is left out).
On top of that, the code pieces are copied into `src/` so the `@/` imports resolve:

```text
frontend/
├── ui-kit/               # full SDK mirror (ui-sdk/, ui-rules/, patterns/, ux/, skills/, docs/, configs)
└── src/
    └── components/
        ├── evilcharts/   # kit pieces, per origin (usable copy)
        ├── hextaui/
        ├── retab/
        ├── shadcncraft/
        ├── command-menu-02.tsx   # blocks-so (flat)
        └── example/      # the Preferences example screen
```

The `ui-kit/` copy is the reference you read and keep; the `src/` copy is the code you
build and own. Both come from the same `sdk/` folder — they are never edited in place by
the installer (it only adds/overwrites its own files).

## Model: copy-paste source library (like shadcn/ui)

`ui-sdk/` is **not** an npm package. It is a source library: you copy the files you need into
your app, keep them, and own them. This matches the frozen base (shadcn/ui) model and keeps
the kit dependency-free.

## Prerequisites in the target app

1. A React + Vite + TypeScript project with the **frozen base installed** (shadcn/ui on the
   Radix base, `components.json` present) — i.e. `npx shadcn@latest init` + `npx shadcn@latest add --all`.
2. The `@/` path alias resolves to your `src/` folder (set by `tsconfig.json` + `vite.config.ts`).

## Copy rules (must all hold)

| Rule | Why |
| --- | --- |
| Copy a whole folder, keep the relative path under `src/` | Internal imports between kit files are relative (`@/components/…` or `./…`) and break if the path changes |
| `components/<origin>/` → `src/components/<origin>/` | Origin folders (evilcharts, hextaui, retab, shadcncraft) keep their internal `@/components/<origin>/…` imports valid |
| `blocks/blocks-so/*.tsx` → `src/components/` (flat) | blocks-so files are self-contained single files, imported as `@/components/<name>` |
| `examples/preferences-screen/` → `src/components/example/` | The example screen imports the kit as a consumer would |
| `@/components/ui/*` imports point to **your** frozen base | The kit components are built on top of the base; never copy the base itself from `ui-sdk/` |
| Install the npm deps listed in the piece's README | e.g. `echarts` for evilcharts, `motion` for shadcncraft — they are declared per piece |
| Keep `ThemeProvider` + `TooltipProvider` wrappers where the piece requires them | Documented per piece (tooltip-based pieces need the provider) |
| Do not modify frozen-base files to make a piece work | Constitution, principle 1 — create a new named component instead |

## Example (adding the settings-preferences screen to an app)

```bash
# 1. copy the folder
cp -r ui-sdk/components/hextaui src/components/hextaui
# 2. install missing npm deps (see components/hextaui/settings-preferences.md)
bun add <deps>
# 3. use it
```

```tsx
import { SettingsPreferences } from "@/components/hextaui/settings-preferences"

export function SettingsScreen() {
  return <SettingsPreferences />
}
```

## Category map

| ui-sdk path | What lives there |
| --- | --- |
| `components/evilcharts/` | Chart components (ECharts + Recharts) |
| `components/hextaui/` | Settings / auth / billing screens |
| `components/retab/` | File upload primitives (dropzone, size format) + hook |
| `components/shadcncraft/` | Marketing sections (hero, marquee, rating…) |
| `blocks/blocks-so/` | Full page blocks (command menu, login, onboarding, stats…) |
| `layouts/`, `templates/`, `examples/` | Reserved — populated in later phases |

## Origin & licenses

Every piece traces its registry, license and source in its README and in
`components-index.md`. Current licenses: MIT (blocks-so, hextaui, evilcharts, retab) and
Apache-2.0 (shadcncraft). The frozen base itself is installed by the consumer via the shadcn
CLI (MIT).

## Wails integration contract (static build)

This kit builds **Wails desktop apps** (Go backend, webview frontend). Verified constraints
in `docs/wails-constraints.md`. The contract:

1. **Static build only.** The frontend must build to a static bundle at `frontend/dist/`
   (embedded via `//go:embed all:frontend/dist`). No SSR, no server, no `next/*` imports.
   Every piece in this kit already complies (Next-specific pieces were excluded at integration).
2. **Hash routing.** App navigation uses `HashRouter` (`#/page`) — never history-mode full
   URLs (Wails runtime conflicts → `ERR_FILE_NOT_FOUND` on reload).
3. **Vite config** (consumer):

   ```ts
   // vite.config.ts
   export default defineConfig({
     base: "./",                       // relative assets for the embedded context
     plugins: [react(), tailwindcss()],
     server: {
       host: "127.0.0.1",
       port: Number(process.env.WAILS_VITE_PORT) ?? 9245,  // wails3 dev proxy
       strictPort: true,
     },
   })
   ```

4. **Runtime & bindings.** Install `@wailsio/runtime`; import generated Go bindings from
   `frontend/bindings/`. Platform features (windows, dialogs, menus, system info) go through
   the runtime/bindings — SDK components receive data via props and never re-implement them.
5. **Dev parity.** `wails3 dev` runs the frontend's `dev` script and proxies Vite on the
   fixed port; `wails3 build` runs `build` and embeds `frontend/dist/`.

## Note for agents (LSP diagnostics)

`ui-sdk/` is a **source library**: it has no `package.json`, `tsconfig.json` or
`node_modules`, so LSP/type-checkers report "cannot resolve `react`, `lucide-react`,
`@/components/ui/*`" on its files. That is expected — the imports resolve only inside a
consumer app (or the `ui-workspace/` mirror, which is the buildable verification channel).
Do not "fix" these diagnostics by adding project files to `ui-sdk/`; verify changes through
`ui-workspace/` (copy the piece, build) instead.
