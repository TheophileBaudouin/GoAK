---
name: recipe-config-viper
description: "Typed and isolated configuration with instance-scoped Viper (no global singleton), YAML loading, defaults, and validation. Use when integrating or maintaining projects built on the Viper ecosystem."
category: recipe
tags: [config, viper, yaml, files, env, instance-scoped]
last-verified: 2026-08-05
---

# recipe-config-viper — instance-scoped configuration with Viper

## Objective and use cases

Load a configuration file (YAML/JSON/TOML) and apply defaults in an isolated
Viper instance via `viper.New()`, without using the package's global
singleton.

Use this recipe in existing projects standardized on Viper or requiring its
advanced integrations (remote config, etcd/consul, pflag binding).

## Prerequisites and architecture

- Go 1.25+
- Dependency: `github.com/spf13/viper v1.21.0`
- Architecture:
  - Create a local instance `v := viper.New()` for each load in a
    `Load(path string) (Config, error)` function.
  - Configure `v.SetConfigFile(path)` explicitly and set defaults via
    `v.SetDefault()`.
  - Read the file with `v.ReadInConfig()` then unmarshal with
    `v.Unmarshal(&config)`.
  - Never share the `viper.CommandLine` instance or the global singleton in
    unit tests.

## Components and choices

- `github.com/spf13/viper v1.21.0` — pinned stable version for application
  configuration.
- `mapstructure` tags (`mapstructure:"host"`) — struct tags required by
  Viper for typed unmarshaling.

## Rejected alternatives

- Global singleton `viper.Get()` / `viper.SetConfigFile()`: makes tests
  dependent on global state and prevents parallel test execution
  (`t.Parallel()`).
- `recipe-config-koanf`: recommended for new lightweight projects without a
  dependency on the Viper ecosystem.
- Standard library `flag` / `os`: too limited for reading structured YAML
  files.

## Complete example

```go
package viperconfig

import (
 "fmt"
 "strings"

 "github.com/spf13/viper"
)

type Config struct {
 Host string `mapstructure:"host"`
 Port int    `mapstructure:"port"`
}

func Load(path string) (Config, error) {
 if strings.TrimSpace(path) == "" {
  return Config{}, fmt.Errorf("read config: path must not be empty")
 }
 v := viper.New()
 v.SetConfigFile(path)
 v.SetDefault("host", "127.0.0.1")
 v.SetDefault("port", 8080)
 if err := v.ReadInConfig(); err != nil {
  return Config{}, fmt.Errorf("read config: %w", err)
 }
 var config Config
 if err := v.Unmarshal(&config); err != nil {
  return Config{}, fmt.Errorf("unmarshal config: %w", err)
 }
 if err := validate(config); err != nil {
  return Config{}, err
 }
 return config, nil
}

func validate(config Config) error {
 if strings.TrimSpace(config.Host) == "" {
  return fmt.Errorf("validate config: host must not be empty")
 }
 if config.Port < 1 || config.Port > 65535 {
  return fmt.Errorf("validate config: port must be between 1 and 65535")
 }
 return nil
}
```

> The `validate` function is deliberately shared with `recipe-config-koanf`
> (separate packages that must compile independently; an independent Go copy
> is kept in each recipe, decision D-2026-08-05-09). Both recipes answer the
> same input-validation question: consult the other library's fiche for the
> koanf ↔ viper comparison.

## Best practices and pitfalls

- Mind the keys: Viper automatically converts all keys to lowercase.
- Check `ReadInConfig()`: distinguish missing-file errors from YAML syntax
  errors.
- Always use `viper.New()` instead of the package singleton.

## Limits and extensions

Viper v2 is not yet released as a stable target; keep version `v1.21.0`.
Viper instances are not safe for concurrent access without an external lock
(`sync.RWMutex`).

## Observable scenario and verification

```sh
go test ./recipes/recipe-config-viper/...
go run ./probes/config-viper
```

The probe creates a temporary `config.yaml` file, loads it via `Load`,
verifies the read values, and prints `config-viper: PASS`.

## Primary sources

- [spf13/viper](https://github.com/spf13/viper) — official Viper repository.
- [Viper UPGRADE.md](https://github.com/spf13/viper/blob/master/UPGRADE.md) —
  migration guide and breaking changes.
