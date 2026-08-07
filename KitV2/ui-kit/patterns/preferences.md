# Pattern — Preferences

## When to use

For the app-level preferences window (macOS: `Cmd+,`), distinct from per-section settings
pages: behavior that applies to the whole app (appearance, keyboard shortcuts, updates,
storage, integrations).

## How to organize the information

1. One window, **categories in the sidebar** (general, appearance, keyboard, advanced) —
   reuse the settings-page layout (`patterns/settings-page.md`).
2. Appearance: theme (light/dark/system) + accent, via the frozen-base tokens
   (`ui-rules/02-colors.md`); instant apply with live preview.
3. Keyboard: shortcut list with search and reset-to-defaults (record in
   `ux/shortcuts.md` — see its authoring guide).
4. Advanced/experimental settings behind a clearly labeled section, never in the first view.

## Common mistakes

- Preferences window that can't be opened from the menu (missing `Cmd+,`).
- Changing preferences that don't take effect until restart without saying so.
- Hardcoded theme choices that ignore the system (no "system" option, no dark mode).
- Duplicating per-section settings into app preferences (one source of truth).

## Best practices

- Persist preferences immediately; show "Restart required" only when genuinely needed.
- Reset-to-defaults per category (macOS convention) with confirm
  (`ui-rules/10-dialogs.md`).
- Respect `ui-rules/01-spacing.md` and `05-accessibility.md` (keyboard reachable, labels).

## Components/blocks recommended

- `ui-sdk/components/hextaui/settings-preferences.tsx`,
  `settings-notifications.tsx`, `settings-security.tsx` — starting points.
- Frozen base: `Sidebar`, `Switch`, `Select`, `Field`, `Separator`, `Button`.
- Theme switching: base `ThemeProvider` (next-themes based, installed in the frozen base).
