---
name: recipe-cli-minimal
description: "Minimal testable Go CLI flag parsing using the standard library flag package (NewFlagSet + ContinueOnError + explicit args). Use when building a single-command CLI or parsing flags into a config struct, and to decide stdlib flag vs cobra."
category: recipe
tags: [cli, flag, stdlib, config, args]
last-verified: 2025-07-31
---

# recipe-cli-minimal — Minimal CLI (stdlib flag)

## Problem

Parse command-line flags into a config — but keep it **testable** and dependency-free.

## Solution

The standard library `flag` package, used the *testable* way: a dedicated
`*flag.FlagSet` with `flag.ContinueOnError`, parsing an explicit `[]string`.

```go
func ParseTo(args []string, w io.Writer) (Config, error) {
    var c Config
    fs := flag.NewFlagSet("app", flag.ContinueOnError) // ContinueOnError = returns error, never os.Exit
    fs.SetOutput(w)                                     // redirect usage (io.Discard in tests)
    fs.IntVar(&c.Port, "port", 8080, "listen port")
    fs.StringVar(&c.Host, "host", "127.0.0.1", "listen host")
    fs.BoolVar(&c.Verbose, "verbose", false, "verbose logging")
    return c, fs.Parse(args)                            // explicit args, NOT the global flag.Parse()
}
// main:    c, err := Parse(os.Args[1:])   // writes usage to os.Stderr
// test:    c, err := ParseTo([]string{...}, io.Discard)
```

See [`cli.go`](cli.go) for the runnable, tested example.

## The testability hinge (why not just `flag.Parse()`)

`flag.Parse()` operates on the **global** `flag.CommandLine`, whose default
`ErrorHandling` is `ExitOnError` — it calls `os.Exit(2)` on a bad flag and reads
`os.Args` directly. That is untestable. The fix is always:

1. `flag.NewFlagSet(name, flag.ContinueOnError)` — returns the error instead of exiting.
2. `fs.Parse(args)` on an explicit slice — never touches `os.Args`.
3. `fs.SetOutput(io.Discard)` in tests — silences usage noise.

This is the pattern used by the standard library's own tests
(`flag.TestFlagSetParse`, `log/slog/level_test.go`).

## Decision boundary: stdlib `flag` vs cobra

| When | Use |
|---|---|
| Single command, a few flags, no subcommands | **stdlib `flag`** (this recipe) |
| Multiple subcommands (`git clone`/`git commit`), nested commands, auto-generated help, shell completion | **cobra** (`spf13/cobra`) |

cobra is a fine, maintained library (used by Kubernetes, Hugo, GitHub CLI) — but
it is over-engineering for a flat flag set. Reaching for it "to be modern" adds a
dependency and a framework for what `flag` does natively. *Per gofaq.org: "Use
the standard flag package when your tool has a single command and fewer than
five flags."*

## Why not the alternatives

| Alternative | Verdict |
|---|---|
| `spf13/cobra` | Justified only for subcommands + auto-help/completion. Over-engineered for the minimal case. |
| `spf13/pflag` | Adds POSIX (short+long) flags; only worth it if you need GNU-style flags — otherwise stdlib suffices. |
| `urfave/cli` | Functional API + built-in version handling; a valid choice but a dependency you don't need for flat flags. |
| `jnovack/flag` (env/file flag) | Only if you specifically need env+file binding (12-factor). Not for plain flag parsing. |

## Error contract

`fs.Parse` returns:

- `nil` on success,
- `flag.ErrHelp` when `-h`/`-help` is passed (main should exit 0),
- a non-nil error on unknown flags / invalid values (main should exit non-zero).

## Verify the behavior (observable)

Run the finished command with `--host 0.0.0.0 --port 9090 --verbose` and observe
that it prints or uses host `0.0.0.0`, port `9090`, and verbose mode. Run it with
`--unknown` and observe a non-zero exit plus a useful error, not a process panic.
This is separate from the parser unit tests.

## Run the tests

```sh
go test ./recipes/recipe-cli-minimal/...
```
