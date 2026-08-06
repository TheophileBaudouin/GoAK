---
name: recipe-cli-interactive
description: "Testable interactive TUI built with Bubble Tea v2 (charm.land/bubbletea/v2), MVU (Elm) architecture, NewModel facade, and event logic decoupled from the real terminal. Use for any interactive TUI application."
category: recipe
tags: [tui, cli, bubbletea, mvu, elm-architecture, interactive]
last-verified: 2026-08-05
---

# recipe-cli-interactive — Interactive TUI application with Bubble Tea v2

## Goal and use case

Build an interactive terminal user interface (TUI) in Go following the MVU architecture (Model-View-Update / The Elm Architecture) with Bubble Tea v2 (`charm.land/bubbletea/v2`), while keeping the state-transition logic and the rendering 100% testable without depending on a real terminal emulator.

Use this recipe to build interactive menus, selectors, CLI forms, or terminal dashboards.

## Prerequisites and architecture

- Go 1.25+
- Dependency: `charm.land/bubbletea/v2 v2.0.8` (vanity import charm.land/bubbletea/v2)
- Testable architecture:
  - Isolate the state machine in a pure `(m model) handleKey(key string) (model, tea.Cmd)` method that takes strings ("j", "k", "q", "enter", "space").
  - `Update(msg tea.Msg)` simply converts `tea.KeyPressMsg` to a string and delegates to `handleKey`.
  - Expose the facade function `NewModel() tea.Model` to allow instantiating and testing the model without an active terminal.
  - `render() string` generates the component's raw text; `View()` wraps it in `tea.NewView(m.render())`.

## Components and choices

- `charm.land/bubbletea/v2` — the reference TUI framework in Go for reactive interfaces.
- `tea.NewView(string)` — view constructor required by Bubble Tea v2.

## Rejected alternatives

- `github.com/charmbracelet/bubbletea` v1: old legacy version. Prefer the new v2 import `charm.land/bubbletea/v2`.
- `gdamore/tcell` or `nsf/termbox-go`: verbose low-level APIs requiring manual management of the screen buffer and ANSI escape sequences.
- Testing `tea.NewProgram().Run()` directly in unit tests: requires a real TTY and fails in CI/headless environments.

## Complete example

```go
package tui

import (
 "fmt"

 tea "charm.land/bubbletea/v2"
)

type model struct {
 choices  []string
 cursor   int
 selected map[int]struct{}
}

func initialModel() model {
 return model{
  choices:  []string{"Buy carrots", "Buy celery", "Buy kohlrabi"},
  selected: make(map[int]struct{}),
 }
}

func NewModel() tea.Model {
 return initialModel()
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
 if k, ok := msg.(tea.KeyPressMsg); ok {
  return m.handleKey(k.String())
 }
 return m, nil
}

func (m model) handleKey(key string) (model, tea.Cmd) {
 switch key {
 case "q", "ctrl+c":
  return m, tea.Quit
 case "up", "k":
  if m.cursor > 0 {
   m.cursor--
  }
 case "down", "j":
  if m.cursor < len(m.choices)-1 {
   m.cursor++
  }
 case "enter", "space":
  if _, ok := m.selected[m.cursor]; ok {
   delete(m.selected, m.cursor)
  } else {
   m.selected[m.cursor] = struct{}{}
  }
 }
 return m, nil
}

func (m model) render() string {
 s := "What should we buy at the market?\n\n"
 for i, choice := range m.choices {
  cursor := " "
  if m.cursor == i {
   cursor = ">"
  }
  checked := " "
  if _, ok := m.selected[i]; ok {
   checked = "x"
  }
  s += fmt.Sprintf("%s [%s] %s\n", cursor, checked, choice)
 }
 s += "\nPress q to quit.\n"
 return s
}

func (m model) View() tea.View { return tea.NewView(m.render()) }
```

## Best practices and pitfalls

- Keep a value receiver for `model`: the update methods return a new modified copy of the model.
- Test state transitions by calling `handleKey` directly in unit tests.
- Avoid blocking I/O in `Update`; use `tea.Cmd` for asynchronous I/O.

## Limits and extensions

To add rich styles (colors, borders) or pre-built components, use `charmbracelet/lipgloss` and `charmbracelet/bubbles`.

## Observable scenario and verification

```sh
go test ./recipes/recipe-cli-interactive/...
go run ./probes/cli-interactive
```

The probe instantiates the model via `NewModel()`, checks the initial state and the generated view, then prints `cli-interactive: PASS`.

## Primary sources

- [charm.land/bubbletea/v2](https://pkg.go.dev/charm.land/bubbletea/v2) — Bubble Tea v2 API documentation.
- [Charm ecosystem](https://charm.sh/) — The Elm Architecture specifications in Go.
