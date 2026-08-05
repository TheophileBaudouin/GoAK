// Package cli shows a minimal, TESTABLE command-line flag parser built on the
// standard library "flag" package.
//
// The testability hinge: use a dedicated *flag.FlagSet with
// flag.ContinueOnError (NOT the global flag.CommandLine, whose default is
// ExitOnError and which reads os.Args). Parse an explicit []string so the same
// code runs in main(os.Args[1:]) and in tests without touching global state.
package cli

import (
	"flag"
	"io"
	"os"
)

// Config holds the parsed command-line options.
type Config struct {
	Host    string
	Port    int
	Verbose bool
}

// Parse parses an argument slice (typically os.Args[1:]) into a Config,
// writing usage/error text to os.Stderr. It returns the parse error (nil on
// success; flag.ErrHelp when -h is requested).
func Parse(args []string) (Config, error) {
	return ParseTo(args, os.Stderr) // pi-lens-ignore: go-bare-error
}

// ParseTo is Parse with an explicit output writer — the testable seam used to
// silence usage noise during tests (pass io.Discard). It builds a fresh
// *flag.FlagSet bound to a Config struct so the parsing logic is isolated from
// os.Args and from global flag state.
func ParseTo(args []string, w io.Writer) (Config, error) {
	var c Config
	fs := flag.NewFlagSet("app", flag.ContinueOnError)
	fs.SetOutput(w)
	fs.StringVar(&c.Host, "host", "127.0.0.1", "listen host")
	fs.IntVar(&c.Port, "port", 8080, "listen port")
	fs.BoolVar(&c.Verbose, "verbose", false, "enable verbose logging")
	return c, fs.Parse(args) // pi-lens-ignore: go-bare-error
}
