# Authoring guide — user-personas.md

## What it's for

Document, for each important user type of the app, their goals, constraints and interface
expectations — so that any screen decision refers to a real person, not an abstract user.

## Format

One persona = one H2 title, then a block of bullet-list fields. Keep under ~15 lines per
persona.

Example:

```markdown
## Claire — project manager (advanced)

- Goals: enter data fast, export reports, not be interrupted
- Constraints: works on keyboard 90% of the time, 14" screen, fullscreen app
- UI expectations: full keyboard shortcuts, dense table, few clicks per action
- What she dislikes: animations, needless multi-step forms
- Product priority: high — daily user
```

## When to read

Before designing or modifying a screen aimed at a persona, and before writing an interface
rule that assumes a user type (in `ui-rules/`).

## When and how to update

After any product decision that changes who uses the app (new target, dropped target), or
when user feedback contradicts an existing persona. To analyze correctly: re-read existing
flows and screens (`ux/user-flows.md`, `ux/screens.md`), ask the product owner about the real target, and
correct only what is contradicted — do not add personas to fill the file.
