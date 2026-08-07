# Authoring guide — user-flows.md

## What it's for

Document, for each important task the user accomplishes in the app, the exact path they
follow screen by screen.

## Format

One flow = one H2 title, a numbered list of steps, each step naming the screen and the
action. Add a "Variants" line if a shortcut or alternative path exists.

Example:

```markdown
## Create a new record

1. Dashboard screen → click "New"
2. Form screen → fill in → click "Save"
3. Back to Dashboard, the record appears at the top of the list

Variants: Cmd+N shortcut from any screen → opens the Form directly.
```

## When to read

Before modifying a screen that appears in at least one existing flow.

## When and how to update

After any change that alters the number of steps, the order, or the destination screen of an
existing flow. To analyze correctly: re-read the code of the screens involved
(routes/navigation), compare with the documented flow, fix divergences, do not add a flow
that does not yet actually exist in the product.
