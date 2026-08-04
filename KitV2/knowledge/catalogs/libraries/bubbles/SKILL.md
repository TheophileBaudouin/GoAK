---
name: bubbles
description: "charm.land/bubbles/v2 — reusable TUI components for Bubble Tea (list, table, textinput, textarea, spinner, progress, paginator, viewport, help). Use when building a Bubble Tea TUI and you need standard widgets instead of hand-rolling them."
category: library
tags: [tui, components, widgets, bubbletea, terminal]
last-verified: 2026-08-04
---

# bubbles — TUI components for Bubble Tea

## Selection

[`charm.land/bubbles/v2`](https://github.com/charmbracelet/bubbles) (v2).

**Why it passes the gate** (actual reason, not stars): each component is a
self-contained `tea.Model` (state + Update + View) you compose into your own
model — selection lists, tables, text input/textarea, spinner, progress bars,
pagination, viewport scrolling, help bar. They are maintained by the same team
as Bubble Tea, ship as a single module, and eliminate the largest source of
hand-rolled TUI bugs (key handling, viewport math, input state).

## Admission checklist

- [x] Actively maintained — v2.1.x, active alongside bubbletea (2026)
- [x] Single responsibility — one module of composable TUI widgets
- [x] Idiomatic Go — every component is a plain tea.Model
- [x] Tests present + CI — yes
- [x] Documentation — README per component + examples
- [x] Real-world usage — everywhere Bubble Tea is used
- [x] Readable end-to-end — yes, small per-component
- [x] Justified by need — standard widgets, not a widget framework

## Minimal use

```go
items := []list.Item{task("one"), task("two")}
m := list.New(items, list.NewDefaultDelegate(), 20, 14) // implements tea.Model
p := tea.NewProgram(m)
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Hand-rolled widgets | Reintroduces key-handling and viewport bugs the components already solved. Use bubbles unless the widget is trivial. |
| tview widgets | Belong to tview's imperative model; not composable with Bubble Tea. |

## Notes

- Components are `tea.Model`s: embed them in your model and forward Update/View.
- `viewport` handles scrollable content; `spinner`+`progress` cover async states —
  pair with `tea.Tick`/commands.
- Pair with `lipgloss` for styling the widgets.
