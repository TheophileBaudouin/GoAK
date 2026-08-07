# Authoring guide — shortcuts.md

## What it's for

Document all keyboard shortcuts of the app (reference device: macOS), to guarantee
consistency, discoverability and no conflicts.

## Format

A 3-column table: Shortcut, Action, Screen(s) involved. Group by zone (Global, List,
Editing). Convention: `Cmd` = ⌘, `Shift` = ⇧, `Alt` = ⌥, `Ctrl` = ⌃.

Example:

```markdown
| Shortcut | Action | Screens |
| --- | --- | --- |
| Cmd+N | New record | All (global) |
| Cmd+S | Save | Form |
| Cmd+Shift+F | Search | All (global) |
| Esc | Close the modal window | Modal windows |
```

## When to read

Before adding or modifying a shortcut, and before writing the keyboard rules in
`ui-rules/08-keyboard.md`.

## When and how to update

After any addition, removal or change of a shortcut in the code (search for
`addEventListener('keydown')`, key handlers and `Cmd`/`Ctrl` mentions in the source code).
Check conflicts: two actions on the same shortcut must be flagged. Document only shortcuts
that are actually implemented — not "planned" ones.
