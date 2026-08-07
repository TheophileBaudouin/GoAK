# Authoring guide — a patterns/ file

## What it's for

Document, for a recurring screen type (settings, table, search…), how to organize it: when
to use it, how to structure the information, which mistakes to avoid, which SDK
components/blocks to recommend.

## Format

One pattern = one H1 "Pattern — Name", then 5 sections: **When to use**,
**How to organize the information**, **Common mistakes**, **Best practices**,
**Recommended components/blocks** (links to `ui-sdk/components|blocks`, empty until
populated). Maximum 2 pages.

Example (format; real content would cite verified sources):

```markdown
# Pattern — Settings page

## When to use
For any page grouping the settings of an app section (preferences, accounts…).

## How to organize the information
1. Groups by theme (general, appearance, accounts), separated by section titles.
2. One line per setting: label on the left, control on the right.

## Common mistakes
- Stacking more than 8 settings without a group.
- Mixing instant-apply and "must save" settings in the same section.

## Best practices
- Auto-save or a single "Save" button at the bottom — never both.
- Settings search if more than 3 groups.

## Recommended components/blocks
- (to complete when pieces are added — ui-sdk/components/…, ui-sdk/blocks/…)
```

## When to read

Before creating a screen matching an existing pattern, and before modifying a screen that
uses one.

## When and how to update

After building a screen that reveals a better organization than the pattern, or when an SDK
component/block changes the recommendation. To analyze correctly: re-read the real screens
matching the pattern (`ux/screens.md` + code), extract what repeats, verify the sources
(design systems / skills), and update the pattern to reflect validated practice — a pattern
never documents untested practice.
