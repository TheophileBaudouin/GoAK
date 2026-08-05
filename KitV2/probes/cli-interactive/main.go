package main

import (
	"fmt"
	"os"

	tui "go-agent-kit-v2/recipes/recipe-cli-interactive"
)

func main() {
	m := tui.NewModel()
	if m == nil {
		fail(fmt.Errorf("tui.NewModel returned nil"))
	}

	v := m.View()
	if v.Content == "" {
		fail(fmt.Errorf("tui View content is empty"))
	}

	fmt.Println("cli-interactive: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
