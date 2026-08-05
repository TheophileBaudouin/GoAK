package main

import (
	"bytes"
	"fmt"
	"os"

	cobracli "go-agent-kit-v2/recipes/recipe-cli-cobra"
)

func main() {
	var buf bytes.Buffer
	cmd := cobracli.NewCommand(&buf)
	cmd.SetArgs([]string{"greet", "--name", "Ada"})

	if _, err := cmd.ExecuteC(); err != nil {
		fail(fmt.Errorf("cobra execute failed: %w", err))
	}

	if got := buf.String(); got != "hello Ada\n" {
		fail(fmt.Errorf("cobra output mismatch: got %q, want %q", got, "hello Ada\n"))
	}

	fmt.Println("cli-cobra: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
