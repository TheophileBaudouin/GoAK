# Authoring guide — a ui-rules/ file

## What it's for

Define the actionable, sourced interface rules of a precise domain (spacing, colors,
typography…), that every agent must apply when building or reviewing an interface.

## Format

One file = one H1 "NN — Title", then three sections: **Rule** (2 to 5 concrete, numbered,
actionable rules), **Source** (official design system or verified skill, with link),
**Example** (a correct example; an incorrect one if useful). Maximum 1 to 2 pages.

Example (format; real content would cite verified sources):

```markdown
# 01 — Spacing

## Rule
1. Use only the 4px scale (4, 8, 12, 16, 24, 32, 48) for inner margins.
2. The space between two related elements is smaller than the space between two groups.

## Source
Apple HIG — Layout (https://developer.apple.com/design/human-interface-guidelines/layout) ;
macos-design-guidelines skill (skills/macos-design-guidelines/).

## Example
✅ p-4, gap-4 between fields of the same group, gap-8 between groups.
❌ px-5 (off-scale), arbitrary margins "to balance".
```

## When to read

Before writing or modifying a component/screen touching this domain, and during any
interface review (the `ui-review` skill refers to it).

## When and how to update

At initial writing, then after each discovery that changes an existing rule (e.g. a
new spacing token validated in `ux/design-decisions.md`). To analyze correctly: collect the
values actually used in the code (`ui-sdk/`), compare with the frozen-base tokens
(Tailwind/shadcn), verify the rule against the cited source, and never write a rule without
a source. Each modified rule records its justification in the file history.
