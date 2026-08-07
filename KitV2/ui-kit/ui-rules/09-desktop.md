# 09 — Desktop

## Rule

1. **Menu bar** (where the platform has one — macOS): standard menus at minimum **App,
   File, Edit, View, Window, Help** (omit File only if not document-based); every menu item
   has a keyboard shortcut; command names and locations are **stable** (Apple HIG §1,
   Rules 1.1, 1.2, 1.6). In Wails, expose menu actions as app-level commands that the React
   side handles.
2. **Windows**: resizable with sensible minimums, support fullscreen, remember state
   (size/position/last view), title bar shows the document/project name (Apple HIG §2).
3. **Toolbars**: unified title-bar-and-toolbar, search field in toolbar where relevant,
   segmented control for view switching, icons + labels (Apple HIG §3).
4. **Sidebar**: leading edge, collapsible, source-list style, badge counts for pending items
   (Apple HIG §4).
5. **System integration** (Wails): support the platform's standard shortcuts (Cmd+, for
   preferences, Cmd+Q quit, Cmd+W close window, Cmd+M minimize), spell-check/menu in text
   inputs, and respect Dark Mode/Reduce Motion/Reduce Transparency (Apple HIG §8, §11).
6. **Static-only (Wails hard constraint)**: the frontend must build to a static bundle
   (`frontend/dist/`, embedded via `//go:embed`) — no SSR, no server, no `next/*`;
   components never assume a backend beyond the declared interface (props/events).
7. **Navigation = hash routing**: screens use `HashRouter` (`#/page`), never history-mode
   full URLs (Wails runtime conflicts → `ERR_FILE_NOT_FOUND` on reload); Vite `base: "./"`
   for relative assets; dev server on `WAILS_VITE_PORT` (default 9245, `strictPort`).
8. **The Wails app shell is the integration boundary**: window management, native dialogs,
   menus, system info go through `@wailsio/runtime` + generated Go bindings
   (`frontend/bindings/`); SDK components receive data/actions via props — they never
   re-implement platform features.

## Source

- Apple HIG — Menu Bar, Windows, Toolbars, Sidebars, System Integration, via skill
  `macos-design-guidelines` §1, §2, §3, §4, §8.
- Wails v2/v3 official docs — verified constraints, see `docs/wails-constraints.md`
  (static build, HashRouter, `base: "./"`, `@wailsio/runtime`, bindings, dev port).
- Wails v2/v3 backend conventions (Go app menu, window config) — see the Go dev kit.

## Example

```tsx
// ✅ desktop toolbar with search + view switcher (macOS convention)
<header className="flex items-center justify-between border-b px-5 h-12">
  <div>
    <ToggleGroup type="single">
      <ToggleGroupItem value="list"><ListIcon /></ToggleGroupItem>
      <ToggleGroupItem value="grid"><GridIcon /></ToggleGroupItem>
    </ToggleGroup>
  </div>
  <CommandMenu />   {/* search in toolbar */}
</header>
```

```tsx
// ✅ preferences shortcut Cmd+, wired once (see ux/shortcuts.md)
// (registered at app level, not in a component)
```
