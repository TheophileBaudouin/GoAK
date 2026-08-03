---
name: viper
description: "spf13/viper v1.21.0 — broad Go configuration integration for existing applications that need files, environment, flags, or remote stores. Use when Viper is an established project choice; compare Koanf for new explicit cascades."
category: library
tags: [config, viper, env, flags, files]
last-verified: 2026-08-03
---

# viper — configuration alternative

## Selection

Use Viper when an existing application already standardizes on it or needs its
broad configuration integrations. For a new application with explicit,
modular providers and parsers, prefer the canonical `koanf` catalog and recipe.
For a small flat configuration, use the standard library.

## Official decision facts

- Pin `github.com/spf13/viper` v1.21.0 for the current kit target.
- Prefer `viper.New()` over the package-level singleton for testability and
  dependency ownership.
- Viper's precedence is explicit `Set`, flag, environment, config, key/value
  store, then default.
- Keys are case-insensitive and Viper instances are not safe for concurrent
  read/write without synchronization.
- Viper v1.20 changed encoding and mapstructure integration; read the official
  upgrade guide before upgrading an existing application.

## Alternatives

| Need | Choice |
| --- | --- |
| One command or a few values | Standard library `flag`, `os`, or `encoding` |
| New modular cascade | `koanf` |
| Existing Viper application | Viper, pinned and instance-scoped |

## Sources

- <https://github.com/spf13/viper>
- <https://pkg.go.dev/github.com/spf13/viper>
- <https://github.com/spf13/viper/blob/master/UPGRADE.md>
