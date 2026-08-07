# ui-agent-kit — desktop UI SDK for Wails apps

Premium desktop UI kit: components, blocks, interface rules, screen patterns and the AI
skills that guide building and reviewing frontends for **Wails** apps (Go + React).

This folder is the **SDK** — copy it into your project (or consume piece by piece per
`ui-sdk/docs/CONSUMPTION.md`). It works with the frozen base installed by the shadcn CLI.

## What's inside

| Folder | Role |
| --- | --- |
| `ui-sdk/` | 40 license-verified components & blocks (charts, settings, upload, sections, page blocks) + index + consumption guide |
| `ui-rules/` | Interface rules: spacing, colors, typography, animations, accessibility, layout, icons, keyboard, desktop, dialogs |
| `patterns/` | How to organize recurring screens: settings-page, dashboard, wizard, login, file-explorer, preferences, search, table |
| `ux/` | Product memory: personas, flows, navigation, screens, shortcuts, design decisions (filled with real product decisions) |
| `skills/` | AI skills: `ux-memory` (read/write the design memory), `ui-review` (review guard), shadcn + design-system references |
| `docs/` | Wails constraints (static build), design-systems sourcing, authoring guides, consumption contract |

## Quick start

1. Read `AGENTS.md` (the rules for working with this kit).
2. Read `ui-sdk/docs/CONSUMPTION.md` (how to consume pieces).
3. Read `docs/wails-constraints.md` (the platform contract).

## Licensing

All pieces are MIT or Apache-2.0 (per-piece provenance in each README and in
`ui-sdk/components-index.md`). The frozen base (shadcn/ui) is MIT.
