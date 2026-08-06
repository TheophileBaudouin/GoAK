---
name: recipe-cli-minimal
description: "Minimal and testable CLI flag parsing in Go with the standard library flag package (flag.NewFlagSet + flag.ContinueOnError + io.Writer). Use for a single-command CLI without subcommands."
category: recipe
tags: [cli, flag, stdlib, config, args]
last-verified: 2026-08-05
---

# recipe-cli-minimal — minimal CLI with the stdlib flag package

## Goal and use case

Build a testable command-line flag parser for a single-command application using only the `flag` package of the Go standard library, without global state leaks or unrecoverable `os.Exit` calls.

Use this recipe for any simple flat-flag CLI that needs zero external dependencies.

## Prerequisites and architecture

- Go 1.25+ (stdlib only)
- The testability hinge:
  - `flag.Parse()` operates on the global `flag.CommandLine` singleton with `ExitOnError`, calling `os.Exit(2)` on error. That is not testable.
  - The solution is a `ParseTo(args []string, w io.Writer) (Config, error)` function.
  - Instantiate a dedicated `*flag.FlagSet` with `flag.ContinueOnError`.
  - Redirect output with `fs.SetOutput(w)` (pass `io.Discard` in tests).
  - Parse the explicit `args` slice instead of accessing `os.Args`.

## Components and choices

- `flag.NewFlagSet("app", flag.ContinueOnError)` — creates an isolated flag set that returns errors instead of killing the process.
- `fs.NArg()` — rejects unexpected positional arguments.

## Rejected alternatives

- Global `flag.Parse()`: uses `ExitOnError` and `os.Args`, making unit tests impossible.
- `spf13/cobra` / `urfave/cli`: unnecessary over-engineering for simple CLIs without subcommands.
- `spf13/pflag`: adds POSIX syntax (short/long flags), but introduces an external dependency not required for simple needs.

## Complete example

```go
package cli

import (
 "flag"
 "fmt"
 "io"
 "os"
)

type Config struct {
 Host    string
 Port    int
 Verbose bool
}

func Parse(args []string) (Config, error) {
 return ParseTo(args, os.Stderr)
}

func ParseTo(args []string, w io.Writer) (Config, error) {
 var c Config
 if w == nil {
  w = io.Discard
 }
 fs := flag.NewFlagSet("app", flag.ContinueOnError)
 fs.SetOutput(w)
 fs.StringVar(&c.Host, "host", "127.0.0.1", "listen host")
 fs.IntVar(&c.Port, "port", 8080, "listen port")
 fs.BoolVar(&c.Verbose, "verbose", false, "enable verbose logging")
 if err := fs.Parse(args); err != nil {
  return c, err
 }
 if fs.NArg() != 0 {
  return c, fmt.Errorf("unexpected positional arguments: %q", fs.Args())
 }
 return c, nil
}
```

## Best practices and pitfalls

- Distinguish help (`flag.ErrHelp`) from parsing errors: `ParseTo` returns `flag.ErrHelp` when `-h` or `-help` is used, letting `main` exit 0.
- Pass `io.Discard` in tests so the FlagSet help text does not pollute the test logs.

## Limits and extensions

If the application grows into a complex structure with subcommands (`app build`, `app deploy`), migrate to `recipe-cli-cobra`.

## Observable scenario and verification

```sh
go test ./recipes/recipe-cli-minimal/...
go run ./probes/cli-minimal
```

The probe executes `ParseTo` with explicit arguments, checks the resulting `Config` structure, and prints `cli-minimal: PASS`.

## Primary sources

- [Go flag package](https://pkg.go.dev/flag) — official documentation of the stdlib `flag` package.
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments#flag-packages) — flag package usage recommendations.
