---
name: bubbletea
description: "charm.land/bubbletea/v2 v2.0.8 — Go TUI framework implementing Model/Update/View with commands and subscriptions. Use for interactive terminal applications whose state machine should be testable without a real terminal; not for static output or web/desktop UIs."
category: library
tags: [tui, cli, mvu, elm-architecture, terminal]
last-verified: 2026-08-05
---

# bubbletea — MVU TUI framework

## Selection

[`charm.land/bubbletea/v2`](https://github.com/charmbracelet/bubbletea) v2.0.8
is the current v2 module. It implements the Elm-style Model/Update/View loop,
commands, and subscriptions for interactive terminal programs. It is admitted
for its focused TUI responsibility, active maintenance, tests, documentation,
and broad production use, not for popularity.

## Admission checklist

- [x] Active v2 maintenance with current patch release v2.0.8.
- [x] Single responsibility: interactive terminal event loop and rendering.
- [x] Explicit model lifecycle: `Init`, `Update`, and `View`.
- [x] Tests, CI, documentation, and examples are maintained upstream.
- [x] The state-machine shape gives consumers a test seam without a live
      terminal.

## Minimal use

```go
func run(model tea.Model) error {
    _, err := tea.NewProgram(model).Run()
    if err != nil {
        return fmt.Errorf("run TUI: %w", err)
    }
    return nil
}
```

In v2, `View` returns a declarative `tea.View`, and key messages use the v2
message types. Keep application logic in pure state transitions where possible;
the kit's `recipe-cli-interactive` tests a `handleKey(string)` seam rather than
constructing framework message structs.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| tview | Choose for an imperative widget tree; it is the main Go alternative to MVU. |
| tcell | Choose when low-level terminal control is required and the application accepts owning the event loop and layout. |
| lipgloss | Companion styling library, not an interactive framework. |
| Ratatui | Rust alternative; not a Go dependency choice. |

## When to use this library
- Building an interactive Go CLI, wizard, dashboard, or agent-facing TUI.
- The state transitions should be unit-testable without a real terminal.
- Commands and subscriptions are useful for asynchronous work or terminal
  events.

## When NOT to use this library
- The program only formats or prints terminal output.
- The interface belongs in a browser or desktop webview.
- An imperative widget tree is a better fit than MVU.
- The project cannot accept the breaking import/API migration from v1 to v2.

## Advantages
- A clear Model/Update/View architecture with explicit asynchronous commands.
- The application state can be tested independently from terminal rendering.
- The v2 API exposes terminal capabilities and keyboard enhancements through a
  structured `tea.View`.
- It composes with Bubbles widgets, Lip Gloss styling, and Huh forms.

## Disadvantages
- MVU adds ceremony for a one-screen or non-interactive command.
- v2 is a breaking migration: vanity import path, key message names, and View
  return type differ from v1.
- Terminal capabilities such as clipboard or keyboard enhancements depend on
  the user's terminal.

## Known pitfalls
- Pin `charm.land/bubbletea/v2`; do not copy v1 examples using the old import
  path or `tea.KeyMsg`.
- Keep the framework message at the adapter seam and test pure transitions
  instead of constructing unstable framework structs.
- Treat `Run` as a boundary error: return or handle it once; do not hide it in
  a library or service layer.
- Add Bubbles separately when standard widgets are needed; Bubble Tea itself is
  the framework, not the widget catalog.

## Verified sources
- [Official Bubble Tea repository](https://github.com/charmbracelet/bubbletea) —
  maintenance, license, architecture, checked 2026-08-05.
- [Bubble Tea v2.0.8 release](https://github.com/charmbracelet/bubbletea/releases/tag/v2.0.8)
  — exact current release, checked 2026-08-05.
- [Bubble Tea v2 on pkg.go.dev](https://pkg.go.dev/charm.land/bubbletea/v2) —
  API and module path, checked 2026-08-05.
- [v2 upgrade guide](https://github.com/charmbracelet/bubbletea/blob/v2.0.0/UPGRADE_GUIDE_V2.md)
  — breaking changes, checked 2026-08-05.
