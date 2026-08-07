# Authoring guide — design-decisions.md

## What it's for

Record every significant design decision with its context and justification — the journal
that explains WHY the interface is the way it is (including deviations from the
constitution).

## Format

One decision = one dated, numbered H2 title, then 4 fields: Context, Decision,
Alternative(s) rejected, Source/Justification. Always end with a status line
(Frozen / Under review).

Example:

```markdown
## D-004 — 2026-09-15: per-screen toolbar instead of a global ribbon

- Context: the global ribbon became unreadable with 3 modules
- Decision: each screen has its own contextual toolbar
- Alternatives rejected: tabbed ribbon (too complex for 2 active screens)
- Source: consistent with the navigation pattern (ux/navigation.md), rule ui-rules/06-layout
- Status: Frozen
```

## When to read

Before making a design decision that could contradict a previous one — and before any
deviation from the constitution.

## When and how to update

As soon as a decision is made (record immediately, not at project end), and when a frozen
decision is challenged (change the status, document why). To analyze correctly: ask
"why is this screen the way it is?", "what changed since?", re-read the relevant `ux/` files
and the code. A decision without status or date is not a recorded decision.
