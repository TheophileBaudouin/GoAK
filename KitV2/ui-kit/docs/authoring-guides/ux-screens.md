# Authoring guide — screens.md

## What it's for

Describe every screen of the app: its purpose, content, actions — the shared reference
between product, design and code.

## Format

One screen = one H2 title (screen name as used in `user-flows.md`), then 4 bullet fields:
Purpose, Content, Main actions, Notes. One line per content element or action, named as in
the UI.

Example:

```markdown
## Dashboard

- Purpose: give an overview of active projects and recent activity
- Content: project list, activity counters, "recent" zone
- Actions: New project (→ Form), Open a project, Search
- Notes: it is the landing screen after login; first screen of the "Create a record" flow
```

## When to read

Before creating, modifying or deleting a screen — and before writing a pattern that involves
it.

## When and how to update

After any screen change that alters its purpose, content or actions (including changes
introduced by a new pattern). To analyze correctly: look at the screen code (components,
forms, buttons), compare with this file, update missing elements, and make sure screen names
stay identical to those in `user-flows.md` (a naming gap breaks the links between files).
