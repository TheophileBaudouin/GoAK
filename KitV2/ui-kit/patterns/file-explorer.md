# Pattern — File Explorer

## When to use

For browsing/opening files and folders inside the app (project files, attachments,
documents, local or remote). Desktop apps make file handling feel native.

## How to organize the information

1. **Three-zone layout** (macOS Finder convention, Apple HIG §4): sidebar (locations /
   folders, collapsible) + list/table of the current folder + optional preview pane.
2. List rows: name (primary), size, modified date (`tabular-nums`); sortable columns;
   selection state visible (hover + selected + keyboard focus).
3. **Keyboard is first-class** (`ui-rules/08-keyboard.md`): arrows move selection, Return
   opens, Delete removes, Space previews, Cmd+Up goes to parent.
4. Dropzone for imports/uploads (`ui-sdk/components/retab/dropzone.tsx`): drag & drop files
   in, with progress and status per file.

## Common mistakes

- Rebuilding the OS file dialog when the platform one exists (Wails can open native dialogs).
- No keyboard navigation in a file list (mouse-only = broken desktop app).
- Unclear empty state (no "this folder is empty" + action).
- Sizes/dates formatted inconsistently (use `ui-sdk/components/retab/file-size-format.ts`).

## Best practices

- Virtualize long lists (base `Table` or a virtualized list for 1000+ rows).
- Remember last location/selection per session (`ui-rules/09-desktop.md` Rule 2.5).
- Errors (permission, missing file) as inline states, not silent failures.
- Path breadcrumb in the toolbar (base `Breadcrumb`).

## Components/blocks recommended

- `ui-sdk/components/retab/dropzone.tsx`, `dropzone-core.ts`, `file-size-format.ts`.
- Frozen base: `Sidebar`, `Table`, `Breadcrumb`, `ScrollArea`, `Skeleton`, `Empty`,
  `ContextMenu` (right-click actions), `Progress`.
- Full document previews (PDF/PPTX/…): deferred — see `ui-sdk/docs/CONSUMPTION.md`
  (§retab cluster) before re-integrating.
