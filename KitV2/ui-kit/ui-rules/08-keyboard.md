# 08 — Keyboard

## Rule

1. **Every mouse-reachable action has a keyboard equivalent.** Modifier conventions
   (Apple HIG Rule 5.1):

   | Pattern | Usage |
   | --- | --- |
   | Cmd+letter | Primary actions (New, Open, Save) |
   | Cmd+Shift+letter | Variant of primary (Save As) |
   | Cmd+Option+letter | Alternative mode (Paste and Match Style) |
   | Cmd+Ctrl+letter | Window/view controls (Fullscreen, Toggle Sidebar) |
   | Ctrl+letter | Emacs-style text navigation (acceptable) |

   Register shortcuts in the app's shortcut registry (`ux/shortcuts.md`), not scattered in
   components.

2. **Esc cancels/closes**: popovers, sheets, dialogs, and in-progress operations; in modal
   dialogs Esc = Cancel (Rule 5.3). **Return** activates the default button (visually
   emphasized, safest action) (Rule 5.4).
3. **Delete** removes the selection (lists/tables); Cmd+Delete for destructive removal;
   always support Cmd+Z undo (Rule 5.5).
4. **Arrows navigate** within lists/grids/tables; Space previews (Quick Look) when items
   support it (Rule 5.6–5.7).
5. Full keyboard navigation: Tab between controls, Shift+Tab reverse, focus is always
   visible (see `05-accessibility.md`).

## Source

- Apple HIG — Keyboard, via skill `macos-design-guidelines` §5 (Rules 5.1–5.7).
- WCAG 2.2 — 2.1.1 Keyboard, via skill `web-platform-guidelines` §1.
- Recording convention: `ux/shortcuts.md` + its authoring guide.

## Example

```tsx
// ✅ global shortcut, registered once
useEffect(() => {
  const onKey = (e: KeyboardEvent) => {
    if (e.metaKey && e.key.toLowerCase() === "n") { e.preventDefault(); createRecord(); }
  };
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}, []);

// ❌ Esc swallowed by a component that doesn't close
<Dialog open={open} onOpenChange={setOpen}>  {/* Esc handled by the base Dialog */}
  …
</Dialog>
```
