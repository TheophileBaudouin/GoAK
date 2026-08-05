package tui

import (
	"strings"
	"testing"

	tea "charm.land/bubbletea/v2"
)

// quitMsg unwraps a tea.Cmd into its produced message, or returns nil.
func quitMsg(cmd tea.Cmd) tea.Msg {
	if cmd == nil {
		return nil
	}
	return cmd()
}

func TestHandleKey_navigateDownThenUp(t *testing.T) {
	m := initialModel()
	if m.cursor != 0 {
		t.Fatalf("start cursor = %d, want 0", m.cursor)
	}

	m, _ = m.handleKey("j") // down
	if m.cursor != 1 {
		t.Fatalf("after j: cursor = %d, want 1", m.cursor)
	}

	m, _ = m.handleKey("k") // up
	if m.cursor != 0 {
		t.Fatalf("after k: cursor = %d, want 0", m.cursor)
	}
}

func TestHandleKey_cursorClampsAtBounds(t *testing.T) {
	m := initialModel()

	// cursor already at top: "up" must not underflow.
	m, _ = m.handleKey("up")
	if m.cursor != 0 {
		t.Fatalf("up at top: cursor = %d, want 0", m.cursor)
	}

	// go to the bottom and try to go past the last item.
	last := len(m.choices) - 1
	for i := 0; i < len(m.choices)+2; i++ {
		m, _ = m.handleKey("down")
	}
	if m.cursor != last {
		t.Fatalf("past-bottom: cursor = %d, want %d", m.cursor, last)
	}
}

func TestHandleKey_toggleSelection(t *testing.T) {
	m := initialModel()

	m, _ = m.handleKey("space") // toggle item 0
	if _, ok := m.selected[0]; !ok {
		t.Fatal("space did not select item 0")
	}

	m, _ = m.handleKey("enter") // toggle again → deselected
	if _, ok := m.selected[0]; ok {
		t.Fatal("enter did not deselect item 0")
	}
}

func TestHandleKey_quitEmitsQuitCmd(t *testing.T) {
	m := initialModel()
	_, cmd := m.handleKey("q")
	if quitMsg(cmd) == nil {
		t.Fatal("q should emit a command")
	}
	if _, ok := quitMsg(cmd).(tea.QuitMsg); !ok {
		t.Fatalf("q command produced %T, want tea.QuitMsg", quitMsg(cmd))
	}
}

func TestHandleKey_unknownKeyIsNoOp(t *testing.T) {
	before := initialModel()
	after, cmd := before.handleKey("x")
	if after.cursor != before.cursor || len(after.selected) != len(before.selected) {
		t.Fatal("unknown key mutated state")
	}
	if cmd != nil {
		t.Fatal("unknown key should emit no command")
	}
}

func TestRender_containsChoicesCursorAndFooter(t *testing.T) {
	m := initialModel()
	out := m.render()

	for _, c := range m.choices {
		if !strings.Contains(out, c) {
			t.Errorf("render missing choice %q", c)
		}
	}
	if !strings.Contains(out, ">") {
		t.Error("render missing cursor marker '>' at item 0")
	}
	if !strings.Contains(out, "Press q to quit") {
		t.Error("render missing footer")
	}

	// Selecting an item should surface a checked marker.
	m, _ = m.handleKey("space")
	if !strings.Contains(m.render(), "[x]") {
		t.Error("selected item not rendered with [x]")
	}
}

func TestNewModel(t *testing.T) {
	tm := NewModel()
	if tm == nil {
		t.Fatal("NewModel() returned nil")
	}
	if tm.Init() != nil {
		t.Fatal("Init() should return nil")
	}
	v := tm.View()
	if v.Content == "" {
		t.Fatal("View() returned empty content")
	}
}
