package desktop

import (
	"errors"
	"sync"
	"testing"
)

func TestAddNote_assignsIncreasingIDs(t *testing.T) {
	app := NewApp()
	n1, err := app.AddNote("first")
	if err != nil {
		t.Fatalf("AddNote first: %v", err)
	}
	n2, err := app.AddNote("second")
	if err != nil {
		t.Fatalf("AddNote second: %v", err)
	}
	if n1.ID != 1 || n2.ID != 2 {
		t.Fatalf("ids = %d,%d, want 1,2", n1.ID, n2.ID)
	}
	if n2.CreatedAt.IsZero() {
		t.Error("CreatedAt not set")
	}
}

func TestAddNote_rejectsEmpty(t *testing.T) {
	app := NewApp()
	_, err := app.AddNote("")
	if !errors.Is(err, errEmptyNote) {
		t.Fatalf("err = %v, want errEmptyNote", err)
	}
	if len(app.Notes()) != 0 {
		t.Error("empty note was stored")
	}
}

func TestNotes_returnsInsertionOrder(t *testing.T) {
	app := NewApp()
	for _, txt := range []string{"a", "b", "c"} {
		if _, err := app.AddNote(txt); err != nil {
			t.Fatalf("AddNote %q: %v", txt, err)
		}
	}
	got := app.Notes()
	if len(got) != 3 {
		t.Fatalf("len = %d, want 3", len(got))
	}
	for i, want := range []string{"a", "b", "c"} {
		if got[i].Text != want {
			t.Errorf("Notes[%d].Text = %q, want %q", i, got[i].Text, want)
		}
	}
}

func TestDeleteNote_idempotent(t *testing.T) {
	app := NewApp()
	n, _ := app.AddNote("x")

	if !app.DeleteNote(n.ID) {
		t.Error("first delete of existing id should report true")
	}
	if app.DeleteNote(n.ID) { // already gone
		t.Error("second delete should report false (idempotent)")
	}
	if len(app.Notes()) != 0 {
		t.Error("note not removed")
	}
}

// TestAddNote_concurrentSafety proves the mutex keeps the id generator and map
// consistent under concurrent writers (run with -race).
func TestAddNote_concurrentSafety(t *testing.T) {
	app := NewApp()
	const writers, each = 8, 50

	var wg sync.WaitGroup
	wg.Add(writers)
	for w := 0; w < writers; w++ {
		go func() {
			defer wg.Done()
			for i := 0; i < each; i++ {
				_, _ = app.AddNote("concurrent")
			}
		}()
	}
	wg.Wait()

	want := writers * each
	if got := len(app.Notes()); got != want {
		t.Fatalf("after concurrent adds: %d notes, want %d (lost updates → missing mutex)", got, want)
	}
}
