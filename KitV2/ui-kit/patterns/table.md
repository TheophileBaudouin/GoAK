# Pattern — Table

## When to use

For structured, row-based data that the user scans, sorts, selects and acts on. Tables are
the workhorse of desktop apps (projects, records, files, history). Not for simple lists
(<10 rows, no columns needed).

## How to organize the information

1. **Toolbar above the table** (left: primary actions, right: search/filters/export)
   (Apple HIG §3 Toolbars). Bulk actions apply to the selection.
2. Columns: minimal set, sensible default order; numeric columns right-aligned with
   `tabular-nums`; sortable headers with visible sort state; row count/status clearly
   labeled.
3. **Selection + keyboard** (`ui-rules/08-keyboard.md`): arrows move, Return opens,
   Delete removes (with undo), Space selects/toggles; selection state visible in all modes
   (hover, selected, focus).
4. Row actions on hover or via `ContextMenu` (right-click); the most important action per
   row can be an inline icon button.
5. **Empty and loading states**: `Empty` (with primary action) and `Skeleton` rows while
   loading; errors as inline states with retry.

## Common mistakes

- 12 columns of everything (cut to what the user actually needs; detail goes to a panel/dialog).
- No keyboard navigation in the table (mouse-only).
- Selecting rows with checkboxes only and no bulk-action bar.
- Pagination hidden inside a dropdown — desktop tables can scroll; paginate only when the
  dataset is truly large, with count + page info visible.

## Best practices

- Virtualize for 1000+ rows (base `Table` + `ScrollArea`, or a virtualized list).
- Keep column order/width stable across screens for the same data.
- Sorting, filtering and search state should survive navigation back to the screen
  (`ui-rules/09-desktop.md` window-state rule).
- Row height ≥40px, readable density (spacing per `ui-rules/01-spacing.md`).

## Components/blocks recommended

- `ui-sdk/blocks/blocks-so/stats-12.tsx` (usage table dashboard) — not a table block per se;
  see `ui-sdk/components-index.md` — `table-05` was not kept (built against a different
  Table API; re-integrate if the newer `@tanstack/react-table` is adopted).
- Frozen base: `Table`, `DropdownMenu`, `ContextMenu`, `Checkbox`, `Input`,
  `Pagination`, `Skeleton`, `Empty`, `Badge` (status), `Tooltip`.
