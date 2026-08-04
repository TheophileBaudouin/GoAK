---
name: bubbletea
description: "charm.land/bubbletea/v2 — the standard TUI framework for Go, implementing The Elm Architecture (Model/Update/View) with commands and subscriptions. Use when building an interactive terminal UI in Go, including agent-facing CLIs, and you want the MVU logic unit-testable without a real terminal."
category: library
tags: [tui, cli, mvu, elm-architecture, terminal]
last-verified: 2026-08-04
---

# bubbletea — TUI framework (MVU)

## Selection

[`charm.land/bubbletea/v2`](https://github.com/charmbracelet/bubbletea) (v2, Go 1.22+).

**Why it passes the gate** (actual reason, not stars): it is a compact (~10k LOC)
framework implementing **The Elm Architecture** — pure `Model` state, `Update`
(state transitions from messages), `View` (render). That model is intrinsically
testable: the state machine is a pure function of messages, so recipes in this
kit test `handleKey(string)` seams without driving a real terminal (see
`recipe-cli-interactif`). It is the de-facto Go TUI standard (Azure, Cockroach
Labs, NVIDIA, MinIO use it), actively maintained with a stable v2 API and a
vanity import.

## Admission checklist

- [x] Actively maintained — v2.0.x releases, very active (2026)
- [x] Single responsibility — terminal UI framework
- [x] Idiomatic Go — plain structs + methods, no globals, no magic
- [x] Tests present + CI — yes, extensive
- [x] Documentation — README, examples, charm.sh docs
- [x] Real-world usage — Azure, Cockroach Labs, NVIDIA, MinIO, Charm's own CLI suite
- [x] Readable end-to-end — yes, small core
- [x] Justified by need — interactive CLIs/agents need a testable UI layer

## Minimal use

```go
p := tea.NewProgram(model{})
if _, err := p.Run(); err != nil { os.Exit(1) }
```

```go
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    if k, ok := msg.(tea.KeyPressMsg); ok {
        return m.handleKey(k.String()) // pure, testable seam
    }
    return m, nil
}
```

See `recipe-cli-interactif` for a runnable, tested example with the
`handleKey(string)` testability pattern.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| tview | Widget/imperative style; couples logic to a global app; weaker pure-logic story. Fine for quick dashboards, not for testable agent TUIs. |
| tcell / termbox-go | Low-level cell buffers; you build the event loop, cursor and layout yourself. termbox-go is unmaintained. |
| gocui | Simplest widget-ish layer, but less maintained and smaller ecosystem. |
| pterm | Output formatting only, not an interactive framework — complementary, not an alternative. |

## Ecosystem notes

The Charm family composes: `lipgloss` (styling), `bubbles` (ready components:
list, table, textinput…), `huh` (forms). Prefer those over hand-rolling.

## Version note

v1 moved to the vanity import `charm.land/bubbletea/v2`. Never import the old
`github.com/charmbracelet/bubbletea` v1 path for new code; `tea.KeyMsg` was
renamed `tea.KeyPressMsg` in v2 — drive messages through `k.String()` in tests,
never construct framework key structs.
