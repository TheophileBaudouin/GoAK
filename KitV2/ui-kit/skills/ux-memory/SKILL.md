---
name: ux-memory
description: Guard for reading and updating the design memory (ux/) before and after any interface change. Use systematically for any task touching a screen, a flow, navigation, a shortcut, a persona or a design decision.
---

# ux-memory — product memory guard

The `ux/` folder is the **living design memory** of the project. It contains only real
product facts, never invention. Any interface change must go through it.

## Golden rule: read before, write after

1. **BEFORE** modifying an interface (creating a screen, changing a flow, adding a shortcut,
   changing navigation): read the relevant `ux/` files.
2. **AFTER** the change: update the relevant `ux/` files, **in the same change as the code**
   — never later.

## File ↔ domain mapping

| `ux/` file | When it is concerned |
| --- | --- |
| `user-personas.md` | The user target changes (new persona, dropped) |
| `user-flows.md` | A journey changes: steps, order, destination screen |
| `navigation.md` | Navigation structure: entries, zones, tabs, menus |
| `screens.md` | A screen is created, changed in content or actions, deleted |
| `shortcuts.md` | A keyboard shortcut is added, modified or removed |
| `design-decisions.md` | A design decision (or a constitution deviation) is made |

## How to proceed

1. Determine which `ux/` files your task touches (table above).
2. Read them fully (they are short).
3. Make your code change.
4. Update the concerned `ux/` files following **exactly** the format of their authoring
   guide in `docs/authoring-guides/`:
   - `ux-user-personas.md`, `ux-user-flows.md`, `ux-navigation.md`, `ux-screens.md`,
     `ux-shortcuts.md`, `ux-design-decisions.md`.
5. Never document something that does not yet exist in the product (no "planned", no
   hypothetical flow).

## Forbidden

- Filling an empty `ux/` file with invented content "to make it pretty".
- Modifying an interface without reading the relevant `ux/` files.
- Changing a screen name in `ux/screens.md` without propagating it to `ux/user-flows.md`
  (both files share the screen names).
