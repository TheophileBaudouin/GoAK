---
name: viper
description: "github.com/spf13/viper v1.21.0 — broad Go configuration integration for files, environment, flags, and remote stores. Use when an existing application already chose Viper; prefer Koanf for a new explicit modular cascade and stdlib for small config."
category: library
tags: [config, viper, env, flags, files]
last-verified: 2026-08-05
---

# viper — integrated configuration

## Selection

[`github.com/spf13/viper`](https://github.com/spf13/viper) v1.21.0 is a broad
configuration integration library covering files, environment, flags, remote
stores, decoding, and watching. It is kept as a conditional catalog choice for
existing Viper applications and broad integrations; a new explicit cascade
should first compare Koanf and stdlib.

## Admission checklist

- [x] Current v1.21.0 and active upstream maintenance/CI.
- [x] Single responsibility: configuration sources, precedence, and decoding.
- [x] Supports files, env, flags, remote stores, and typed unmarshal.
- [x] Tests, documentation, upgrade guide, and large ecosystem use exist.
- [x] Global singleton, case-insensitive keys, and concurrency limits are explicit
      adoption costs.

## Minimal use

```go
func readConfig(path string) (Config, error) {
    v := viper.New()
    v.SetConfigFile(path)
    if err := v.ReadInConfig(); err != nil {
        return Config{}, fmt.Errorf("read config: %w", err)
    }
    var cfg Config
    if err := v.Unmarshal(&cfg); err != nil {
        return Config{}, fmt.Errorf("decode config: %w", err)
    }
    return cfg, nil
}
```

Use `viper.New()` and inject the instance; do not build shared service code on
the package-level singleton. Synchronize reload/read access yourself.

## Alternatives considered

| Need | Choice |
|---|---|
| One command or a few values | stdlib `flag`, `os`, and explicit decoding. |
| New modular provider/parser cascade | Koanf, with explicit source order and smaller boundaries. |
| Existing Viper application | Viper, pinned and instance-scoped; avoid a casual migration. |
| Strict schema/config contract | A typed configuration package or explicit constructor validation. |

## When to use this library
- An existing application already depends on Viper and migration cost exceeds
  the benefit of changing configuration libraries.
- Broad file/env/flag/remote integration and Viper's precedence model are needed.
- The project can own instance lifecycle, synchronization, and upgrade testing.

## When NOT to use this library
- A new service needs a small explicit cascade: prefer Koanf or stdlib.
- The project cannot tolerate case-insensitive keys or package-global legacy
  behavior.
- Concurrent reads/writes or watch callbacks cannot be synchronized.
- A typed schema and strict validation boundary are the actual requirement.

## Advantages
- Broad integrations for files, env, flags, remote stores, and decoding.
- Familiar precedence model and compatibility with Cobra/pflag ecosystems.
- `viper.New()` supports explicit ownership despite the legacy singleton API.

## Disadvantages
- Package-level singleton makes hidden mutable state easy to introduce.
- Instances are not safe for concurrent read/write without synchronization.
- Case-insensitive keys can hide configuration collisions.
- Upgrade and decoding changes require reading the official guide and testing
  existing configurations.

## Known pitfalls
- Prefer `viper.New()`; never let package-global Viper state cross tests or
  service boundaries.
- Synchronize reads/writes and watch/reload callbacks explicitly.
- Treat environment/config values as untrusted input: validate typed results
  and secret handling after decoding.
- Read the official upgrade guide before moving across v1.19/v1.20 behavior and
  pin v1.21.0 for reproducible builds.

## Verified sources
- [Official Viper repository](https://github.com/spf13/viper) — API,
  maintenance, license, checked 2026-08-05.
- [Viper releases](https://github.com/spf13/viper/releases) — v1.21.0 current
  version, checked 2026-08-05.
- [Viper on pkg.go.dev](https://pkg.go.dev/github.com/spf13/viper) — sources,
  precedence, and API, checked 2026-08-05.
- [Viper upgrade guide](https://github.com/spf13/viper/blob/v1.21.0/UPGRADE.md)
  — decoding/encoding migration, checked 2026-08-05.
- [Viper README concurrency guidance](https://github.com/spf13/viper/blob/v1.21.0/README.md)
  — synchronization boundary, checked 2026-08-05.
