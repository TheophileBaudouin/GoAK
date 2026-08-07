# AGENTS.md — ui-agent-kit (SDK)

## This project

**Premium desktop UI kit** for Wails apps (Go + Wails v2/v3, frontend React + TypeScript +
Vite + Tailwind CSS + shadcn/ui + Radix UI + Lucide React). This folder is the **SDK** —
the consumable, installable kit: components and blocks (`ui-sdk/`), interface rules
(`ui-rules/`), screen patterns (`patterns/`), design memory (`ux/`), and the skills that
guide building and reviewing frontends (`skills/`). The frozen base (shadcn/ui, Radix,
Tailwind, Lucide) is provided by the consuming app via the shadcn CLI — it is never
duplicated or modified here.

## Before doing anything

1. Read `ui-sdk/docs/CONSUMPTION.md` — the copy-paste contract for using pieces in an app.
2. Read `docs/wails-constraints.md` — the hard static-build constraints of the target
   platform (Wails). They are non-negotiable.
3. If you touch an interface, read the relevant files in `ux/` first, update them after
   (see `skills/ux-memory/SKILL.md`).
4. Any design rule you write must cite a source (`docs/design-systems.md`).

## Absolute rules

- The frozen base is **never** modified here. We never "improve" an existing component: we
  create a new one next to it, explicitly named (`PremiumButton`, `DesktopButton`…) with a
  sourced justification in `ui-rules/` or `patterns/` and an entry in
  `ui-sdk/components-index.md`.
- **Static-only, Wails-bound**: the frontend must build to a static bundle
  (`frontend/dist/`, embedded via `//go:embed`). No SSR, no `next/*` imports. Navigation
  uses hash routing (`HashRouter`); Vite uses `base: "./"`; platform features (windows,
  dialogs, menus, system info) go through `@wailsio/runtime` + generated Go bindings —
  never re-implemented in components (see `docs/wails-constraints.md`).
- Any added rule/pattern cites its source (official design system or verified skill — see
  `docs/design-systems.md`).
- No silent duplication: if a piece already exists in `ui-sdk/components-index.md`, reuse
  it; otherwise create a new named piece.
- **This folder is autonomous**: it never references the meta-project (`governance/`,
  `references/`, meta skills) — everything it needs is inside (`docs/`, `skills/`,
  `ui-sdk/docs/`). If a piece of content or a reference can only exist outside this folder,
  it does not belong in the SDK: either bring its source in or drop it.
- **All files are written in English** — the ecosystem standard.
- **Every change is verified**: after any implementation, run the diagnostics pass
  (typecheck, lint, build, markdownlint) and fix what it finds before reporting done.

## Where to find what

| Need | Where |
| --- | --- |
| Copy-paste consumption contract | `ui-sdk/docs/CONSUMPTION.md` |
| Wails static constraints | `docs/wails-constraints.md` |
| Reference design systems & sourcing | `docs/design-systems.md` |
| Authoring guides (format of every living file) | `docs/authoring-guides/` |
| Interface rules (spacing, colors, typography…) | `ui-rules/` |
| How to organize a screen | `patterns/` |
| Components / blocks / layouts index | `ui-sdk/components-index.md` |
| Product memory (personas, flows, screens) | `ux/` (see `skills/ux-memory/`) |
| Interface review guard | `skills/ui-review/SKILL.md` |
| Reference skills (shadcn, design systems) | `skills/` |

## Useful commands (verified 2026-08-06)

```bash
# Install all shadcn components in a consumer app (the frozen base)
npx shadcn@latest add --all

# Search / get docs for a shadcn component
npx shadcn@latest search <query>
npx shadcn@latest docs <component>

# Install a skill for Pi
npx skills add <owner>/<repo> -a pi
```

The skills of this folder live in `skills/` and are declared to Pi via `.pi/settings.json`
→ `{ "skills": ["../skills"] }` (a root `skills/` folder is not auto-discovered by Pi).

## Reminder

This file stays **short**: durable information goes into `docs/` or the authoring guides,
never here. Do not duplicate information present elsewhere — link to it.
