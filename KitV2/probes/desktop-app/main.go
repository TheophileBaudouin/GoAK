package main

import (
	"fmt"
	"os"

	desktop "go-agent-kit-v2/recipes/recipe-desktop-app"
)

func main() {
	app := desktop.NewApp()
	note, err := app.AddNote("probe note")
	if err != nil {
		fail(fmt.Errorf("desktop AddNote failed: %w", err))
	}

	notes := app.Notes()
	if len(notes) != 1 || notes[0].ID != note.ID || notes[0].Text != "probe note" {
		fail(fmt.Errorf("desktop Notes mismatch: got %+v", notes))
	}

	if !app.DeleteNote(note.ID) {
		fail(fmt.Errorf("desktop DeleteNote reported false for existing note"))
	}

	if len(app.Notes()) != 0 {
		fail(fmt.Errorf("desktop note was not removed"))
	}

	fmt.Println("desktop-app: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
