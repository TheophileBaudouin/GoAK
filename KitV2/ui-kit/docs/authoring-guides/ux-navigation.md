# Authoring guide — navigation.md

## What it's for

Document the app's navigation structure: what is always visible (sidebar, menu, toolbar),
what is contextual, and how one moves between zones.

## Format

One H2 title per navigation level (Global, Contextual), then a bullet list describing each
element: name, role, when visible.

Example:

```markdown
## Global navigation

- Sidebar (always visible): Dashboard, Projects, Settings
- File menu (menu bar): New, Open, Save — always visible
- Toolbar (contextual to the active screen): main actions of the screen

## Contextual navigation

- Tabs in the Project screen: Details, Records, History
```

## When to read

Before adding a screen, a menu entry, or a navigation element — to check where it fits
without duplicating an existing role.

## When and how to update

After any change to the navigation structure (added/removed screen, moved entries, new
zone). To analyze correctly: walk the app routes, list the real navigation entries (sidebar,
menus, tabs), compare with this file, and fix divergences — the documented order must
reflect the real on-screen order.
