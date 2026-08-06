---
name: recipe-config-koanf
description: "Explicit, typed configuration cascade with Koanf v2, merging sources (defaults, map, environment, file, flags) with strict validation. Use for any Go service combining multiple configuration sources."
category: recipe
tags: [config, koanf, cascade, env, flags, yaml]
last-verified: 2026-08-05
---

# recipe-config-koanf — explicit configuration cascade with Koanf v2

## Purpose and use cases

Load and merge a Go application's configuration from multiple sources in an explicit precedence order (for example: defaults < config file < environment variables < CLI flags) and unmarshal the result into a typed, validated structure.

Use Koanf for new applications that need a modular architecture and full control over the provider merge order.

## Prerequisites and architecture

- Go 1.25+
- Dependencies:
  - `github.com/knadh/koanf/v2 v2.3.6`
  - `github.com/knadh/koanf/providers/confmap v1.0.0`
- Architecture:
  - Instantiate `koanf.New(".")` locally inside a `Load(overrides map[string]any) (Config, error)` function.
  - Avoid any mutable global instance.
  - Load defaults first via `confmap.Provider`.
  - Load overrides sequentially (files, env, map); each successive `Load` overwrites previous keys.
  - Decode via `k.Unmarshal("", &config)`, then run an explicit business validation step.

## Components and choices

- `github.com/knadh/koanf/v2` — modern, lightweight, modular library (~15x lighter than Viper with no unneeded dependencies).
- `confmap.Provider` — in-memory object provider, ideal for injecting defaults and test overrides.

## Rejected alternatives

- Standard library `os.Getenv` / `flag` alone: sufficient for 1 or 2 variables, but quickly becomes verbose and error-prone for complex cascades.
- `spf13/viper`: popular but monolithic, uses global singletons by default, and lowercases keys irreversibly.
- `kelseyhightower/envconfig`: limited to environment variables only; does not allow multi-source merging.

## Complete example

```go
package koanfconfig

import (
 "fmt"
 "strings"

 "github.com/knadh/koanf/providers/confmap"
 "github.com/knadh/koanf/v2"
)

type Config struct {
 Host string `koanf:"host"`
 Port int    `koanf:"port"`
}

func Load(overrides map[string]any) (Config, error) {
 k := koanf.New(".")
 if err := k.Load(confmap.Provider(map[string]any{
  "host": "127.0.0.1",
  "port": 8080,
 }, "."), nil); err != nil {
  return Config{}, fmt.Errorf("load defaults: %w", err)
 }
 if len(overrides) > 0 {
  if err := k.Load(confmap.Provider(overrides, "."), nil); err != nil {
   return Config{}, fmt.Errorf("load overrides: %w", err)
  }
 }
 var config Config
 if err := k.Unmarshal("", &config); err != nil {
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

> The `validate` function is deliberately shared with
> `recipe-config-viper` (separate packages that must compile independently;
> an independent Go copy is kept in each recipe, decision
> D-2026-08-05-09). Both recipes answer the same input-validation question:
> consult the other library's fiche for the koanf ↔ viper comparison.

## Best practices and pitfalls

- Always validate the `Config` struct after `Unmarshal` to detect out-of-range or missing values.
- For dynamic runtime reloading, protect the `*koanf.Koanf` instance with a `sync.RWMutex`.
- Do not keep plaintext secrets in configuration files under version control.

## Limits and extensions

Koanf defines no default cascade order: the developer must orchestrate the order of `k.Load(...)` calls. Parsers (YAML, JSON, TOML) must be imported separately.

## Observable scenario and verification

```sh
go test ./recipes/recipe-config-koanf/...
go run ./probes/config-koanf
```

The probe loads the configuration with overrides, verifies that defaults and overrides are applied, then prints `config-koanf: PASS`.

## Primary sources

- [knadh/koanf](https://github.com/knadh/koanf) — official Koanf repository and documentation.
- [pkg.go.dev/github.com/knadh/koanf/v2](https://pkg.go.dev/github.com/knadh/koanf/v2) — v2 API reference.
