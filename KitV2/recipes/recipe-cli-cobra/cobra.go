// Package cobracli contains the testable command behavior used by a Cobra CLI.
// The Cobra wiring is kept in NewCommand and remains thin: application logic
// stays independent from command-global state.
package cobracli

import (
	"fmt"
	"io"
	"strings"

	"github.com/spf13/cobra"
)

// NewCommand builds a small multi-command CLI with an explicit output writer.
func NewCommand(out io.Writer) *cobra.Command {
	if out == nil {
		out = io.Discard
	}
	var name string
	root := &cobra.Command{
		Use:           "app",
		Short:         "Example multi-command application",
		SilenceUsage:  true,
		SilenceErrors: true,
	}
	greet := &cobra.Command{
		Use:   "greet",
		Short: "Greet a name",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, args []string) error {
			if strings.TrimSpace(name) == "" {
				return fmt.Errorf("name must not be empty")
			}
			_, err := fmt.Fprintf(out, "hello %s\n", name)
			return err
		},
	}
	greet.Flags().StringVar(&name, "name", "", "name used by the command")
	root.AddCommand(greet)
	return root
}
