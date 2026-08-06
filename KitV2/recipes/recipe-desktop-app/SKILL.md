---
name: recipe-desktop-app
description: "Testable Go service layer for a Wails v3 desktop application without a direct runtime dependency. Typed bound methods isolated from the Webview. Use to design the Go business logic of a Wails desktop application."
category: recipe
tags: [desktop, wails, gui, bindings, frontend, Go]
last-verified: 2026-08-05
---

# recipe-desktop-app — Go service adapter for Wails v3

## Objective and use cases

Design the Go business service layer of a Wails v3 desktop application so that the methods exposed to the web frontend are 100% testable in pure Go, without requiring CGO compilation of the webview or the Wails runtime in the test suite.

Use this recipe to create hybrid desktop applications (Go + HTML/TS frontend) while keeping the Go unit tests portable and fast.

## Prerequisites and architecture

- Go 1.25+
- Wails v3 (Beta-to-GA transition) — documented for the client application, not imported in this Go package.
- Testable architecture:
  - The `App` object holds the application state and the synchronization (`sync.Mutex`).
  - The public methods (`AddNote`, `Notes`, `DeleteNote`) take and return typed Go types with JSON tags (`json:"id"`).
  - Contain no import of `github.com/wailsapp/wails/v3/pkg/application` in the business service package, to avoid pulling the CGO/GTK/Webview2 dependency into the Go gate.

## Components and choices

- Pure Go business struct with Mutex — guarantees concurrent access safety between the main Go thread and the frontend's asynchronous JS calls.
- Transparent interface contract — the exported methods are automatically exposed to the frontend by the Wails bindings generators (`wails3 generate bindings`).

## Rejected alternatives

- Importing the Wails `application` package directly into the service package: imposes the presence of CGO/GUI system libraries (WebKitGTK on Linux, Webview2 on Windows), breaking cross-platform unit tests on CI without a GUI.
- Tauri (Rust): another major framework, but written in Rust and not Go.
- Fyne / Gio: pure-Go GUI frameworks without a webview (different architecture paradigm).

## Complete example

```go
package desktop

import (
	"errors"
	"sync"
	"time"
)

type Note struct {
	ID        int       `json:"id"`
	Text      string    `json:"text"`
	CreatedAt time.Time `json:"created_at"`
}

type App struct {
	mu     sync.Mutex
	nextID int
	notes  map[int]Note
}

func NewApp() *App {
	return &App{nextID: 1, notes: make(map[int]Note)}
}

var errEmptyNote = errors.New("note text must not be empty")

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

func (a *App) Notes() []Note {
	a.mu.Lock()
	defer a.mu.Unlock()

	out := make([]Note, 0, len(a.notes))
	for i := 1; i < a.nextID; i++ {
		if n, ok := a.notes[i]; ok {
			out = append(out, n)
		}
	}
	return out
}

func (a *App) DeleteNote(id int) bool {
	a.mu.Lock()
	defer a.mu.Unlock()
	_, ok := a.notes[id]
	delete(a.notes, id)
	return ok
}
```

## Best practices and pitfalls

- Protect all shared state with `sync.Mutex`: the Wails frontend can execute method calls in parallel.
- Always validate arguments on the Go side: Go is the trust boundary, the frontend can pass invalid inputs.
- Note that Wails v3 is currently in Beta-to-GA status: check the issue tracker before going to production.

## Limits and extensions

This recipe covers the testable Go adapter. The Wails `main.go` wiring with the webview window and static asset embedding (`embed.FS`) lives in the final client application binary.

## Observable scenario and verification

```sh
go test ./recipes/recipe-desktop-app/...
go run ./probes/desktop-app
```

The probe instantiates `NewApp()`, adds a note, lists it, deletes it and verifies the result, then prints `desktop-app: PASS`.

## Primary sources

- [Wails Documentation](https://wails.io/) — official Wails v2 / v3 site and documentation.
- [Wails v3 Beta Repository](https://github.com/wailsapp/wails) — official Wails repository.
