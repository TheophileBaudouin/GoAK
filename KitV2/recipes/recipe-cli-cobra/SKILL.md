---
name: recipe-cli-cobra
description: "Testable multi-command CLI with Cobra subcommands, argument validation, explicit io.Writer output handling, generated help, and autocompletion limits. Use for a Go CLI with subcommands or persistent flags."
category: recipe
tags: [cli, cobra, subcommands, flags, validation]
last-verified: 2026-08-05
---

# recipe-cli-cobra — multi-command CLI with Cobra

## Goal and use case

Build a testable multi-command Go CLI (e.g. `app greet --name Ada`) with subcommands, local and global flags, strict argument validation, and output errors that can be captured without exiting the process prematurely via `os.Exit`.

Use Cobra only when the application requires a subcommand tree (`git clone`, `git commit`), aliases, automatic help, or autocompletion. For a single-command tool with flat flags, use `recipe-cli-minimal`.

## Prerequisites and architecture

- Go 1.25+
- External dependency: `github.com/spf13/cobra v1.10.2`
- Testable architecture:
  - Encapsulate command creation in a factory `NewCommand(out io.Writer) *cobra.Command`.
  - Use `RunE` to return errors instead of calling `os.Exit`.
  - Set `SilenceUsage: true` and `SilenceErrors: true` so the `main` entry point controls error formatting.
  - Inject an `io.Writer` to capture standard output in tests (e.g. `bytes.Buffer`).

## Components and choices

- `github.com/spf13/cobra` — the de facto standard for complex Go CLIs (used by Kubernetes, Hugo, GitHub CLI).
- `ExecuteC()` — runs the command tree while returning the active command and the error.
- `Args: cobra.NoArgs` — strict validation rejecting unexpected positional arguments.

## Rejected alternatives

- `flag` (stdlib): limited to flat flags without subcommands. Ideal for small tools, insufficient for command trees.
- `spf13/pflag` alone: adds POSIX-style flags (long/short), but does not handle the subcommand tree.
- `urfave/cli`: a valid alternative API, but introduces an additional competing dependency without a decisive advantage over Cobra.
- Mutable global state (global `cobra.Command`): makes tests dependent on execution order and not isolated.

## Complete example

```go
package cobracli

import (
	"fmt"
	"io"
	"strings"

	"github.com/spf13/cobra"
)

func NewCommand(out io.Writer) *cobra.Command {
	if out == nil {
		out = io.Discard
	}
	var name string
	root := &cobra.Command{
		Use:           "app",
		Short:         "Application multi-commandes",
		SilenceUsage:  true,
		SilenceErrors: true,
	}
	greet := &cobra.Command{
		Use:   "greet",
		Short: "Saluer une personne",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, args []string) error {
			if strings.TrimSpace(name) == "" {
				return fmt.Errorf("name must not be empty")
			}
			_, err := fmt.Fprintf(out, "hello %s\n", name)
			return err
		},
	}
	greet.Flags().StringVar(&name, "name", "", "nom de la personne")
	root.AddCommand(greet)
	return root
}
```

## Best practices and pitfalls

- Avoid `cobra.CheckErr()` in subcommand handlers: it calls `os.Exit(1)` and prevents any cleanup or testing.
- Reset or re-instantiate the command tree for each test via `NewCommand(&buf)`.
- Always validate positional arguments and required options at the start of `RunE`.
- Never pass secrets through command-line flags: they are visible in the process list (`ps aux`) and the shell history.

## Limits and extensions

Cobra adds a significant transitive dependency (`pflag`, etc.). Do not use it out of habit for scripts or micro-services that need only 2-3 configuration flags.

## Observable scenario and verification

```sh
go test ./recipes/recipe-cli-cobra/...
go run ./probes/cli-cobra
```

The probe instantiates the command, runs `greet --name Ada`, verifies the exact output `hello Ada\n`, then prints `cli-cobra: PASS`.

## Primary sources

- [spf13/cobra](https://github.com/spf13/cobra) — official Cobra repository.
- [Cobra Documentation](https://cobra.dev/docs/) — architecture guides and recommendations for LLM CLIs.
- [pkg.go.dev/github.com/spf13/cobra](https://pkg.go.dev/github.com/spf13/cobra) — API reference.
