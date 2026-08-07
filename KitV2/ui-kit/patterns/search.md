# Pattern — Search

## When to use

For any search surface: command palette (global, `Cmd+K`), in-screen search box, or filter
within a table/list. Desktop power users expect global search to be a keyboard-first
surface (`ui-rules/08-keyboard.md`).

## How to organize the information

1. **Command palette** (global): trigger `Cmd+K` (registered once in `ux/shortcuts.md`);
   open a `Command` dialog with grouped results (actions, recent items, navigation); arrows
   move, Enter runs, Esc closes. Empty query = recent items.
2. **In-screen search**: a single `Input`/`Command` in the toolbar (Apple HIG §3.4: search
   field in toolbar) filtering the current list/table live.
3. Result rows: name + secondary line (context/meta); selected row highlighted with visible
   focus (`ui-rules/05-accessibility.md`); keyboard on every result.
4. **No-results state** is informative: "No results for X" + a hint (check spelling,
   clear filters) — never a blank area.

## Common mistakes

- Search that requires the mouse (no arrow navigation in results).
- Results without context (which screen/file does this hit?).
- Debounce/stale results: cancel in-flight requests when the query changes.
- Global palette that can't be closed with Esc.

## Best practices

- Keep results grouped and capped (5–10 per group) with "see all" actions.
- Respect `prefers-reduced-motion` for result animations
  (`ui-rules/04-animations.md`).
- For large datasets, debounce input (150–300ms) and show a subtle loading state.
- Highlight the matched fragment in result text.

## Components/blocks recommended

- `ui-sdk/blocks/blocks-so/command-menu-01.tsx` (groups),
  `command-menu-02.tsx` (keyboard shortcuts) — starting points.
- Frozen base: `Command` (cmdk-based), `Dialog`, `Input`, `Kbd`, `ScrollArea`,
  `Separator`.
