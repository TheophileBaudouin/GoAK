---
name: cobra
description: "spf13/cobra v1.10.2 — subcommand-based Go CLI framework with POSIX flags, generated help, aliases, and shell completion. Use when a CLI has multiple commands or needs generated help/completion; use recipe-cli-minimal for flat flags."
category: library
tags: [cli, cobra, subcommands, completion, help]
last-verified: 2026-08-03
---

# cobra — multi-command CLI

## Selection

Use `github.com/spf13/cobra` v1.10.2 when a CLI needs subcommands, nested
commands, persistent flags, generated help, aliases, or shell completion. The
standard-library `flag` recipe remains the correct choice for one command with
a small flat flag set.

## Official decision facts

- Commands form a tree; use `AddCommand` to compose subcommands.
- Use `RunE` and `ExecuteC()` so application errors return to the caller and
  remain testable; avoid `CheckErr` in reusable command code because it exits.
- Cobra uses `spf13/pflag` for POSIX-compatible short and long flags.
- `MarkFlagRequired`, mutually-exclusive flag validation, command groups, and
  generated shell completion are optional features, not reasons to use Cobra
  for every CLI.
- The official Cobra documentation includes an LLM-ready CLI documentation
  guide; no repository `llms.txt` file is required or copied into the kit.

## Limits and security

- Cobra and pflag add dependencies and mutable package-level options; keep
  command construction in a factory and avoid shared command trees in tests.
- Validate arguments and flags at the command boundary.
- Do not pass secrets through flags when process listings or shell history can
  expose them; use a protected configuration source instead.
- Pin versions and inspect pflag changes during upgrades.

## Sources

- <https://github.com/spf13/cobra>
- <https://pkg.go.dev/github.com/spf13/cobra>
- <https://cobra.dev/docs/>
- <https://cobra.dev/docs/how-to-guides/clis-for-llms/>
