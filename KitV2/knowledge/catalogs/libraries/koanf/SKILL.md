---
name: koanf
description: "knadh/koanf v2.3.5 — modular multi-source configuration with separate providers and parsers. Use when loading defaults plus file, environment, or flag sources with an explicit cascade and typed decoding."
category: library
tags: [config, koanf, viper-alternative, env, flags]
last-verified: 2026-08-03
---

# koanf — explicit configuration cascade

## Selection

Use `github.com/knadh/koanf/v2` when configuration comes from multiple
sources and the application should choose providers, parsers, and precedence
explicitly. Koanf v2 separates provider/parser modules so applications install
only what they use.

For one value or a small flat flag set, use the standard library. For an
existing Viper application, do not migrate casually; use the Viper catalog and
its upgrade guidance.

## Canonical shape

Load defaults first, then file, environment, and flags in the desired order.
Later loads override earlier values. Unmarshal into a typed struct after the
cascade. Use `StrictMerge` when incompatible types must fail rather than be
silently replaced. Keep a configuration instance local or synchronize reloads
with concurrent readers.

## Official limits

- Koanf is case-sensitive and does not impose a load order.
- Providers and parsers are separate modules with their own dependencies.
- File/provider watching is not safe alongside concurrent `Get`/`Load` access
  without synchronization.
- v2 changes the module path to `/v2` and splits providers/parsers; consult
  the official v2 migration/release notes before upgrading.

## Sources

- <https://github.com/knadh/koanf>
- <https://pkg.go.dev/github.com/knadh/koanf/v2>
- <https://pkg.go.dev/github.com/knadh/koanf/providers/confmap>
