// Package tui shows a minimal, TESTABLE interactive terminal UI built on
// Bubble Tea v2 (The Elm Architecture: Model/Update/View).
//
// Testability hinge: the state-transition logic is a pure function of a key
// STRING (handleKey), decoupled from tea.KeyPressMsg internals (whose fields
// change across major versions). Update is just the wiring that derives the
// string from a KeyPressMsg; tests drive handleKey directly. View delegates to
// a string-returning render() for the same reason — the rendered text is
// asserted without depending on the tea.View wrapper.
package tui

import (
	"fmt"

	tea "charm.land/bubbletea/v2"
)

// model is the application state. Value receiver: Update returns a new model,
// not a mutated shared one (functional update).
type model struct {
	choices  []string
	cursor   int
	selected map[int]struct{}
}

// initialModel is the entry point a real program passes to tea.NewProgram.
func initialModel() model {
	return model{
		choices:  []string{"Buy carrots", "Buy celery", "Buy kohlrabi"},
		selected: make(map[int]struct{}),
	}
}

// Init satisfies tea.Model. No initial I/O, so no command.
func (m model) Init() tea.Cmd { return nil }

// Update is the framework wiring: turn a tea.KeyPressMsg into the key string
// and hand it to handleKey. All other messages are ignored.
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	if k, ok := msg.(tea.KeyPressMsg); ok {
		return m.handleKey(k.String())
	}
	return m, nil
}

// handleKey is the testable state machine: a pure transition driven by a key
// string. It does not import tea's key types, so tests are stable across
// bubbletea major versions.
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

// render produces the UI text. Pure function of the model — asserted in tests.
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

// View satisfies tea.Model; it wraps render() in a tea.View for the runtime.
func (m model) View() tea.View { return tea.NewView(m.render()) }
