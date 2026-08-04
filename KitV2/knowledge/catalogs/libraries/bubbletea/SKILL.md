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

## Utiliser cette librairie quand

- Construire une CLI interactive (wizards, menus, dashboards, TUIs
  agent-facing) avec une vraie boucle d'événements.
- La logique MVU doit être testable unitairement sans terminal réel (seam
  `handleKey(string)`).
- Composer l'écosystème Charm : `lipgloss` (style), `bubbles` (widgets),
  `huh` (formulaires).

## Ne pas utiliser cette librairie quand

- Le besoin est seulement de la sortie terminale formatée (lipgloss/pterm
  suffisent — pterm n'est pas un framework interactif).
- Un dashboard rapide non testable est acceptable (tview peut suffire).
- Le contrôle bas niveau de la cellule terminal est requis (tcell).
- L'interface est web ou desktop (hors périmètre — wails/fyne).

## Avantages

- MVU pur : l'état est une fonction pure des messages → testable sans
  terminal, exactement le besoin des recettes du kit (`recipe-cli-interactif`).
- Standard de facto du TUI Go : Azure, Cockroach Labs, NVIDIA, MinIO,
  suite CLI de Charm.
- Maintenance très active, API v2 stable, import vanity.
- Écosystème complet (bubbles, lipgloss, huh, glamour…).

## Inconvénients

- Discipline MVU obligatoire : tout passe par Update/commands/subscriptions —
  le code impératif « classique » doit être restructuré.
- v2 a cassé l'import path et renommé `tea.KeyMsg` → `tea.KeyPressMsg` :
  migration nécessaire depuis v1.
- Framework opiné : les cas exotiques (multiplexage avancé, protocoles
  custom) demandent un travail d'intégration.

## Pièges connus

- Ne jamais importer l'ancien chemin v1 `github.com/charmbracelet/bubbletea`
  pour du nouveau code.
- En v2, `tea.KeyPressMsg` et `k.String()` pour les tests ; ne jamais
  construire les structs de messages clavier (instables entre majors).
- La vue se construit via `tea.NewView(s)` (v2) — vérifier la doc de la
  version épinglée.
- Tester la seam pure, jamais le terminal réel (cf. Gotcha recipe
  cli-interactif).

## Sources vérifiées

- [charmbracelet/bubbletea (repo officiel, v2)](https://github.com/charmbracelet/bubbletea)
  — vérifié 2026-08-04
- [charm.land/bubbletea/v2 (pkg.go.dev)](https://pkg.go.dev/charm.land/bubbletea/v2)
  — vérifié 2026-08-04
- Artefact interne : `recipe-cli-interactif` (seam `handleKey` testé)
