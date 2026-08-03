---
name: recipe-cli-cobra
description: "Testable multi-command Go CLI with Cobra subcommands, RunE errors, generated help, and completion boundaries. Use when a CLI has subcommands or needs Cobra's help and completion features; use recipe-cli-minimal for flat flags."
category: recipe
tags: [cli, cobra, subcommands, completion, help]
last-verified: 2026-08-03
---

# recipe-cli-cobra — multi-command CLI

## Selection

Use Cobra when the CLI has multiple subcommands, nested commands, persistent
flags, generated help, aliases, or shell completion. Keep the standard-library
`flag` recipe for one command with a small flat flag set.

## Canonical shape

Build a fresh command tree in a factory. Use `RunE` so failures are returned,
keep output injectable, and execute the command with explicit arguments in
 tests. Avoid `CheckErr` and package-global mutable command state because they
exit the process or make tests order-dependent.

The runnable example provides an `app greet` command with a local `--name`
flag. Consumers can add root persistent flags and additional subcommands while
keeping each command's argument validation and action small.

## Security and limits

- Validate command arguments and flags at the command boundary.
- Do not put secrets in flags when process listings or shell history can expose
  them; prefer environment or a protected configuration source.
- Pin Cobra and review its `pflag`/transitive dependency changes during updates.
- Cobra adds a dependency and POSIX flag semantics; it is not automatically
  better than the standard library.

## Verification

```sh
go test ./recipes/recipe-cli-cobra/...
```

## Sources

- <https://github.com/spf13/cobra>
- <https://pkg.go.dev/github.com/spf13/cobra>
- <https://cobra.dev/docs/>
- <https://cobra.dev/docs/how-to-guides/clis-for-llms/>
