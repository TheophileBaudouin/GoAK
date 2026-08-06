---
name: cobra
description: "spf13/cobra v1.10.2 — Go CLI framework with command trees, POSIX flags, generated help, aliases, and shell completion. Use for multi-command CLIs; use recipe-cli-minimal and stdlib flag for a flat single-command CLI."
category: library
tags: [cli, cobra, subcommands, completion, help]
last-verified: 2026-08-05
---

# cobra — multi-command CLI

## Selection

Use [`github.com/spf13/cobra`](https://github.com/spf13/cobra) v1.10.2 for a
CLI with subcommands, nested commands, persistent flags, aliases, generated
help, or shell completion. Cobra builds on `spf13/pflag` and keeps command
execution explicit through `RunE`/`ExecuteC`. It is admitted for this focused
multi-command responsibility and active maintenance, not for popularity.

## Admission checklist

- [x] Current tagged release v1.10.2 and active upstream commits.
- [x] Single responsibility: command trees, flags, help, and completion.
- [x] Tests, CI, documentation, and a formal security policy exist.
- [x] `RunE` and `ExecuteC` support explicit error propagation and tests.
- [x] The dependency is justified only when stdlib `flag` is too small.

## Minimal use

The canonical implementation and test live in `recipe-cli-cobra`; keep command
construction in a factory and inject arguments/output there. A command should
return failures through `RunE`, not terminate the process through `CheckErr`.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `flag` | Prefer for one command and a small flat flag set; see `recipe-cli-minimal`. |
| `urfave/cli` | A valid alternative when its API and command model match the project; compare maintenance and dependency policy directly. |
| Custom parsing | Avoid when help, completion, and command validation are required; it recreates Cobra's boundary. |

## When to use this library
- The CLI has multiple or nested commands, persistent/local flags, aliases,
  generated help, or shell completion.
- POSIX short/long flag behavior and command-level validation are required.
- A command factory and explicit execution boundary can be maintained in tests.

## When NOT to use this library
- A single command with a few flat flags is fully covered by stdlib `flag`.
- The binary must remain dependency-free and does not need generated help or
  completion.
- The code is a reusable library that must never own process exit behavior.

## Advantages
- Composable command tree with persistent and local flags.
- Generated help, aliases, validation hooks, and shell completion.
- `RunE` plus `ExecuteC` keeps application errors testable and injectable.

## Disadvantages
- Adds Cobra and pflag dependencies and a command model to learn.
- Mutable command options make package-global trees prone to order-dependent
  tests.
- Its feature set is unnecessary overhead for a flat command.

## Known pitfalls
- Use `RunE` and handle the returned error at the process boundary; avoid
  `CheckErr` in reusable command code.
- Build a fresh command tree per test and per execution when mutable state could
  leak between invocations.
- Validate arguments and flags at the command boundary.
- Never put secrets in flags: process listings and shell history can expose
  them. Use a protected configuration source.
- Pin Cobra and inspect pflag/transitive changes during upgrades.

## Verified sources
- [Official Cobra repository](https://github.com/spf13/cobra) — maintenance,
  API, and security policy, checked 2026-08-05.
- [Cobra v1.10.2 releases](https://github.com/spf13/cobra/releases) — current
  tagged version, checked 2026-08-05.
- [Cobra on pkg.go.dev](https://pkg.go.dev/github.com/spf13/cobra) — API and
  module metadata, checked 2026-08-05.
- [Cobra documentation](https://cobra.dev/docs/) — command and completion
  behavior, checked 2026-08-05.
- [Cobra security policy](https://github.com/spf13/cobra/blob/main/SECURITY.md)
  — supported security boundary, checked 2026-08-05.
- [Open issue #2358](https://github.com/spf13/cobra/issues/2358) — flag parsing
  limitation, checked 2026-08-05.
