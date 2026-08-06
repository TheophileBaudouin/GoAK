---
name: bubbles
description: "charm.land/bubbles/v2 v2.1.1 — reusable Bubble Tea TUI components such as lists, tables, inputs, progress, and viewport. Use when a Bubble Tea application needs standard widgets; not for non-interactive terminal output or a different TUI framework."
category: library
tags: [tui, components, widgets, bubbletea, terminal]
last-verified: 2026-08-05
---

# bubbles — TUI components for Bubble Tea

## Selection

[`charm.land/bubbles/v2`](https://github.com/charmbracelet/bubbles) v2.1.1,
released 2026-07-04, is a collection of standalone `tea.Model` components for
Bubble Tea v2. It is admitted for its focused widget responsibility, active
maintenance, tests, documentation, and production use in Charm applications,
not for star count.

## Admission checklist

- [x] Active v2 maintenance; current release v2.1.1.
- [x] Single responsibility: composable terminal widgets.
- [x] Components expose the Bubble Tea model lifecycle and remain independently
      composable.
- [x] Tests, CI, documentation, and examples are present.
- [x] The module is useful when hand-written keyboard, viewport, or input state
      would be a larger risk than the dependency.

## Minimal use

```go
func newTaskList(items []list.Item) list.Model {
    delegate := list.NewDefaultDelegate()
    return list.New(items, delegate, 20, 14)
}
```

`list.Item` is an interface implemented by the consumer's item type; this
example deliberately constructs the widget but does not pretend to be a full
Bubble Tea program. Use a `tea.Model` wrapper to forward `Update` and `View`.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Hand-written widgets | Avoid unless the widget is trivial or the dependency is not justified; otherwise it recreates keyboard and viewport edge cases. |
| tview | A separate imperative TUI model; choose it when that model is preferred instead of Bubble Tea MVU. |
| lipgloss | Companion styling library, not a replacement for widgets. |

## When to use this library
- A Bubble Tea v2 TUI needs a list, table, text input, textarea, spinner,
  progress bar, paginator, viewport, timer, or help component.
- The application wants standard widget state and rendering while retaining its
  own top-level model and event flow.
- Keyboard, scrolling, or input-state edge cases should be delegated to a
  maintained component.

## When NOT to use this library
- The program only prints formatted terminal output.
- The application does not use Bubble Tea v2.
- The required widget is simpler to implement than the dependency boundary.
- The application needs an imperative widget tree and has selected tview.

## Advantages
- Components fit the `tea.Model` lifecycle and compose with Bubble Tea.
- The v2 module has a clear vanity import path and active upstream maintenance.
- Standard widgets reduce repeated keyboard, pagination, and viewport code.
- The package family covers both basic controls and asynchronous progress/timer
  views.

## Disadvantages
- Components inherit Bubble Tea's MVU model and v2 migration cost.
- Generic widgets still require consumer delegates, styles, and composition.
- The v2 API is not source-compatible with the old GitHub import path.

## Known pitfalls
- Forward the child component's `Update` and `View`; constructing a widget alone
  does not wire it into the parent model.
- Pin and import `charm.land/bubbles/v2`; do not mix v1 examples with v2 code.
- Test the pure model seam rather than requiring a real terminal in unit tests.
- Review viewport dimensions and timer lifecycle at boundaries; upstream tracks
  edge-case issues for zero dimensions and repeated starts.

## Verified sources
- [Official Bubbles repository](https://github.com/charmbracelet/bubbles) —
  maintenance, license, components, checked 2026-08-05.
- [Bubbles v2.1.1 release](https://github.com/charmbracelet/bubbles/releases/tag/v2.1.1)
  — exact version and release date, checked 2026-08-05.
- [Bubbles v2 on pkg.go.dev](https://pkg.go.dev/charm.land/bubbles/v2) — API and
  module path, checked 2026-08-05.
- [Viewport issue #879](https://github.com/charmbracelet/bubbles/issues/879) —
  tracked edge-case limitation, checked 2026-08-05.
