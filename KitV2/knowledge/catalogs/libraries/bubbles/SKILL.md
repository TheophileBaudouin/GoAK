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

## Utiliser cette librairie quand

- Construire une TUI Bubble Tea et avoir besoin de widgets standards
  (list, table, textinput, textarea, spinner, progress, paginator, viewport,
  help) plutôt que de les coder à la main.
- Composer des composants `tea.Model` self-contained dans son propre modèle.
- La gestion clavier, le calcul de viewport et l'état d'entrée doivent être
  fiables (source principale de bugs des TUI faites main).

## Ne pas utiliser cette librairie quand

- Le widget est trivial (une ligne de style) : pas de dépendance pour rien.
- La TUI n'est pas basée sur Bubble Tea : bubbles dépend de bubbletea et n'est
  pas utilisable sans.
- Le modèle impératif de tview est préféré (incompatible avec Bubble Tea).

## Avantages

- Composants `tea.Model` autonomes, composition simple (embed + forward
  Update/View).
- Même équipe que Bubble Tea, module unique, v2.1.x actif (2026).
- Élimine les bugs récurrents des widgets fait main (key handling, viewport
  math, input state).
- README par composant + exemples dédiés.

## Inconvénients

- Dépend de bubbletea : pas de composant isolé sans le framework.
- Widgets génériques : les besoins très spécifiques exigent une customisation
  (delegates, styles) — un widget fait main peut être plus simple.
- v2 = import vanity `charm.land/bubbles/v2` à respecter.

## Pièges connus

- Un composant non forwardé (Update/View) ne réagit pas : toujours forwarder
  vers le composant embed.
- `viewport` pour le contenu scrollable ; `spinner`+`progress` pour les états
  async — à piloter avec `tea.Tick`/commands, pas avec des boucles.
- Styler avec `lipgloss`, jamais en ANSI brut.

## Sources vérifiées

- [charmbracelet/bubbles (repo officiel, v2.1.x)](https://github.com/charmbracelet/bubbles)
  — vérifié 2026-08-04
- [charm.land/bubbles/v2 (pkg.go.dev)](https://pkg.go.dev/charm.land/bubbles/v2)
  — vérifié 2026-08-04
- Artefacts internes : `recipe-cli-interactif`, catalog `lipgloss`
