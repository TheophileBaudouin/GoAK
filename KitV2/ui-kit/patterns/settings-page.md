# Pattern — Settings Page

## When to use

For any screen grouping the settings of an app section (account, appearance, notifications,
security…). Desktop apps expose a top-level Preferences window (`Cmd+,`) with categories in a
sidebar (macOS convention, Apple HIG §4).

## How to organize the information

1. **Sidebar of categories** (left) + **settings panel** (right): categories = account,
   appearance, notifications, security, advanced. Use the base `Sidebar` or a simple nav list.
2. One line per setting: **label left, control right** (`Field` + control in a row).
3. Group related settings under section titles; keep each category to one scrolling panel.
4. Saving: either instant-apply (toggles, selects) or a single "Save" button per panel —
   never both mixed in the same panel.

## Common mistakes

- Stacking more than 8 settings without a group.
- Mixing instant-apply and "must save" settings in the same panel.
- Deep nesting (3+ levels of categories) — flatten to 1–2 levels.
- No way back / no visible state saved indicator.

## Best practices

- **Read the settings screen's real content from `ux/screens.md`** before writing it.
- Reuse the harvested screens: `ui-sdk/components/hextaui/settings-*` (preferences,
  notifications, security, team-members, activity-log…) as the starting point.
- Respect `ui-rules/01-spacing.md` (8px related / 20px groups), `02-colors.md` (tokens,
  dark mode), `05-accessibility.md` (labels, focus), `08-keyboard.md` (Cmd+, Esc).
- Keep destructive/advanced settings at the bottom of their category (Apple HIG §7).

## Components/blocks recommended

- `ui-sdk/components/hextaui/settings-account.tsx`, `settings-preferences.tsx`,
  `settings-notifications.tsx`, `settings-security.tsx`, `settings-team-members.tsx`,
  `settings-activity-log.tsx`, `settings-api-keys.tsx` (+ `auth-session-manager.tsx`).
- Frozen base: `Sidebar`, `Field`, `Switch`, `Select`, `Input`, `Separator`, `Card`.
- If a category is missing, create a new named component (`PremiumXxxSettings`) next to the
  base per constitution §Naming.
