---
name: recipe-cli-interactive
description: "Interface TUI interactive testable avec Bubble Tea v2 (charm.land/bubbletea/v2), architecture MVU (Elm), façade NewModel et logique d'événements découplée du terminal réel. Utiliser pour toute application TUI interactive."
category: recipe
tags: [tui, cli, bubbletea, mvu, elm-architecture, interactive]
last-verified: 2026-08-05
---

# recipe-cli-interactive — Application TUI interactive avec Bubble Tea v2

## Objectif et cas d'utilisation

Construire une interface utilisateur interactive en terminal (TUI) en Go selon l'architecture MVU (Model-View-Update / The Elm Architecture) via Bubble Tea v2 (`charm.land/bubbletea/v2`), tout en conservant la logique de transition d'état et le rendu 100% testables sans dépendre d'un véritable émulateur de terminal.

Utiliser cette recette pour créer des menus interactifs, des sélecteurs, des formulaires CLI ou des dashboards terminal.

## Prérequis et architecture

- Go 1.25+
- Dépendance : `charm.land/bubbletea/v2 v2.0.8` (import de vanité charm.land/bubbletea/v2)
- Architecture testable :
  - Isoler la machine à états dans une méthode pure `(m model) handleKey(key string) (model, tea.Cmd)` qui prend des chaînes de caractères ("j", "k", "q", "enter", "space").
  - `Update(msg tea.Msg)` convertit simplement `tea.KeyPressMsg` en chaîne et délègue à `handleKey`.
  - Exposer la fonction façade `NewModel() tea.Model` pour permettre l'instanciation et le test du modèle sans terminal actif.
  - `render() string` génère le texte brut du composant ; `View()` l'encapsule dans `tea.NewView(m.render())`.

## Composants et choix

- `charm.land/bubbletea/v2` — framework TUI de référence en Go pour les interfaces réactives.
- `tea.NewView(string)` — constructeur de vue réquis par Bubble Tea v2.

## Alternatives rejetées

- `github.com/charmbracelet/bubbletea` v1 : ancienne version legacy. Préférer le nouvel import v2 `charm.land/bubbletea/v2`.
- `gdamore/tcell` ou `nsf/termbox-go` : API de bas niveau verbeuse nécessitant la gestion manuelle du tampon d'écran et des séquences d'échappement ANSI.
- Tester directement l'exécution de `tea.NewProgram().Run()` dans les tests unitaires : nécessite une TTY réelle et échoue dans les environnements CI/head-less.

## Exemple complet

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

## Bonnes pratiques et pièges

- Respecter le récepteur de valeur (`value receiver`) pour `model` : les méthodes d'update retournent une nouvelle copie modifiée du modèle.
- Tester les transitions d'état en appelant `handleKey` directement dans les tests unitaires.
- Éviter d'insérer de l'I/O bloquante dans `Update` ; utiliser `tea.Cmd` pour l'I/O asynchrone.

## Limites et extensions

Pour ajouter des styles riches (couleurs, bordures) ou des composants pré-faits, utiliser `charmbracelet/lipgloss` et `charmbracelet/bubbles`.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-cli-interactive/...
go run ./probes/cli-interactive
```

La probe instancie le modèle via `NewModel()`, vérifie l'état initial et la vue générée, puis affiche `cli-interactive: PASS`.

## Sources primaires

- [charm.land/bubbletea/v2](https://pkg.go.dev/charm.land/bubbletea/v2) — documentation API v2 de Bubble Tea.
- [Charm ecosystem](https://charm.sh/) — spécifications The Elm Architecture en Go.
