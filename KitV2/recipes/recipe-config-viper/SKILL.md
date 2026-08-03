---
name: recipe-config-viper
description: "Instance-scoped Viper configuration from a file with typed decoding. Use when an existing application standardizes on Viper or needs its broad format, environment, flag, or remote configuration integrations."
category: recipe
tags: [config, viper, files, env, flags]
last-verified: 2026-08-03
---

# recipe-config-viper — instance-scoped configuration

## Selection

Use `github.com/spf13/viper` when the project explicitly needs Viper's broad
configuration integrations or already uses Viper. Create an instance with
`viper.New()` and pass it through the application; do not use the package-level
singleton in testable or concurrent code.

For a new application that only needs a small explicit cascade, compare the
canonical `koanf` catalog and recipe first. For a flat flag set, use the
standard-library `flag` recipe.

## Canonical shape

Configure one Viper instance, set defaults, select a config file, read it, and
unmarshal into a typed struct. The example wraps errors and keeps file loading
out of package-global state.

Viper's precedence is explicit `Set`, flag, environment, config, key/value
store, then default. Its keys are case-insensitive. Viper instances are not
safe for concurrent read/write without external synchronization.

## Limits and migration

- Viper lowercases keys; preserve this behavior when integrating with existing
  configuration schemas.
- `ReadInConfig` returns a missing-file error that the application may handle
  explicitly; parsing errors must not be ignored.
- Viper v1.20+ changed encoding and mapstructure integration; consult the
  official `UPGRADE.md` before upgrading an existing application.
- Viper v2 is not yet a released compatibility target; pin v1.21.0 here.

## Verification

```sh
go test ./recipes/recipe-config-viper/...
```

## Sources

- <https://github.com/spf13/viper>
- <https://pkg.go.dev/github.com/spf13/viper>
- <https://github.com/spf13/viper/blob/master/UPGRADE.md>
