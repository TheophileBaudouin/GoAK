// Package desktop shows how to structure the Go side of a Wails v3 desktop app
// so the bound methods (the ones the web frontend calls) are plain, testable Go.
//
// Testability hinge: the App's exported methods are pure Go with no dependency
// on the Wails runtime. The Wails wiring (application.New + Services binding +
// the webview) is intentionally NOT imported here — it needs GUI/webview/CGO and
// is not portable into the kit's test suite. That wiring lives in SKILL.md as a
// reference snippet; see it for how NewApp() is registered as a service.
package desktop

import (
	"errors"
	"sync"
	"time"
)

// Note is a stored item; its fields travel to the frontend via the binding.
type Note struct {
	ID        int       `json:"id"`
	Text      string    `json:"text"`
	CreatedAt time.Time `json:"created_at"`
}

// App holds the bound methods a Wails frontend calls. It is plain Go: the exact
// same type a web client would call through generated TS bindings.
//
// ponytail: a single mutex guards the store; per-note locks if throughput ever matters.
type App struct {
	mu     sync.Mutex
	nextID int
	notes  map[int]Note
}

// NewApp returns an empty App ready to be registered as a Wails service.
func NewApp() *App {
	return &App{nextID: 1, notes: make(map[int]Note)}
}

var errEmptyNote = errors.New("note text must not be empty")

// AddNote validates and stores a note, returning it with its generated id.
// This is the method Wails exposes to the frontend (bound via NewService).
func (a *App) AddNote(text string) (Note, error) {
	if text == "" {
		return Note{}, errEmptyNote
	}

	a.mu.Lock()
	defer a.mu.Unlock()

	n := Note{ID: a.nextID, Text: text, CreatedAt: time.Now().UTC()}
	a.notes[n.ID] = n
	a.nextID++
	return n, nil
}

// Notes returns all stored notes, oldest first.
func (a *App) Notes() []Note {
	a.mu.Lock()
	defer a.mu.Unlock()

	out := make([]Note, 0, len(a.notes))
	for i := 1; i < a.nextID; i++ { // stable insertion order
		if n, ok := a.notes[i]; ok {
			out = append(out, n)
		}
	}
	return out
}

// DeleteNote removes a note by id. Missing id is a no-op (idempotent delete).
func (a *App) DeleteNote(id int) bool {
	a.mu.Lock()
	defer a.mu.Unlock()
	_, ok := a.notes[id]
	delete(a.notes, id)
	return ok
}
