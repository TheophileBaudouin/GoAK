---
name: recipe-cli-interactif
description: "Minimal testable interactive terminal UI with Bubble Tea v2 (The Elm Architecture: Model/Update/View). Use when building a TUI in Go and you want the MVU logic unit-testable without a real terminal."
category: recipe
tags: [tui, cli, bubbletea, mvu, elm-architecture]
last-verified: 2025-07-31
---

# recipe-cli-interactif — Interactive TUI (Bubble Tea v2)

## Problem

Build an interactive terminal UI (keys, cursor, state) — but keep the logic
**unit-testable** without driving a real terminal.

## Solution

Bubble Tea v2 (`charm.land/bubbletea/v2`, 44k★, in production at Azure, Cockroach
Labs, NVIDIA, MinIO). It implements The Elm Architecture: **Model** (state),
**Update** (state transitions from messages), **View** (render).

The testability hinge: keep the state-transition logic in a pure function of a
key **string** (`handleKey`), not a `tea.KeyPressMsg`. `Update` is just the wiring
that derives the string; tests drive `handleKey` directly.

```go
// the testable state machine — no tea key types, stable across versions
func (m model) handleKey(key string) (model, tea.Cmd) {
    switch key {
    case "q", "ctrl+c": return m, tea.Quit
    case "up", "k":     if m.cursor > 0 { m.cursor-- }
    case "down", "j":   if m.cursor < len(m.choices)-1 { m.cursor++ }
    case "enter","space": /* toggle selected */
    }
    return m, nil
}

// framework wiring — turns a KeyPressMsg into the string handleKey wants
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    if k, ok := msg.(tea.KeyPressMsg); ok { return m.handleKey(k.String()) }
    return m, nil
}
```

See [`tui.go`](tui.go) for the runnable, tested model.

## Run it (wiring, not compiled in the test suite)

```go
func main() {
    p := tea.NewProgram(initialModel())
    if _, err := p.Run(); err != nil { fmt.Println(err); os.Exit(1) }
}
```

## v2 migration notes (gotchas)

- **Import path changed**: `charm.land/bubbletea/v2` (vanity import), NOT
  `github.com/charmbracelet/bubbletea`. v1 code uses the github path.
- **`View()` returns `tea.View`** (not `string`); build it with `tea.NewView(s)`.
- **`tea.KeyMsg` → `tea.KeyPressMsg`**; `msg.String()` still returns "j", "down",
  "space", "ctrl+c", … so a `switch msg.String()` survives the rename.
- Quit: `return m, tea.Quit`. To assert in tests, call the cmd and type-assert
  `tea.QuitMsg`.

## Why this shape (testability)

A TUI that puts `tea.KeyPressMsg` field access inside `Update` is untestable —
those fields change across majors, and you can't send real keypresses in a unit
test. By routing through a key **string**, the entire state machine is pure and
version-stable. This is the same seam as `recipe-graceful-shutdown` (signal
wiring kept out of the orchestrator).

## Companions (not required for the minimal case)

- **Bubbles** (`charmbracelet/bubbles`) — ready components: lists, text inputs,
  spinners, viewports. Pull when you need them; the minimal recipe uses none.
- **Lip Gloss** (`charmbracelet/lipgloss`) — styling/layout.

## Verify the behavior (observable)

Run the finished TUI in a terminal. Press `j` twice, press `space`, and observe
that the third item is selected with `[x]`; press `q` and observe a clean exit.
This terminal interaction is mandatory evidence in addition to unit tests.

## Run the tests

```sh
go test ./recipes/recipe-cli-interactif/...
```
