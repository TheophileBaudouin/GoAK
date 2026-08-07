# Authoring guide — components-index.md

## What it's for

The single index of all SDK components, blocks and layouts (`ui-sdk/components-index.md`):
what each one is for, where it lives, in what state. It is the entry point to avoid
reinventing a component that already exists.

## Format

A 4-column table: **Component** (exact name, e.g. `PremiumButton`), **Category**
(component / block / layout), **Short description** (one sentence, usage), **Status**
(Planned / Installed frozen base / Created / Under review / Stable). One row per entry,
sorted by category then name. The name must exactly match the folder/file name in `ui-sdk/`.

Example:

```markdown
| Component | Category | Short description | Status |
| --- | --- | --- | --- |
| PremiumButton | component | Desktop primary-action button (Button variant) | Created |
| Button | component | Frozen-base button (shadcn) | Installed frozen base |
| SettingsPage | block | Complete settings page (settings-page pattern) | Planned |
```

## When to read

Before creating a component, block or layout — to check it does not exist yet. During any
review (the `ui-review` skill: "reuse of existing components").

## When and how to update

At every addition, removal or status change of a component/block/layout, **in the same
change as the code involved** (never later). To analyze correctly: list the files of
`ui-sdk/components/`, `blocks/`, `layouts/` (the code is the source of truth), compare with
the index, fix divergences. A component removed from the code must leave the index the same
day.
