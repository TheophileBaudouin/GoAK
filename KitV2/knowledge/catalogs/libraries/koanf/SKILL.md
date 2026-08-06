---
name: koanf
description: "github.com/knadh/koanf/v2 v2.3.6 — modular configuration cascade with explicit providers, parsers, and typed decoding. Use for defaults plus file/env/flag sources; not for a single flag, implicit global state, or unsynchronized reloads."
category: library
tags: [config, koanf, viper-alternative, env, flags]
last-verified: 2026-08-05
---

# koanf — explicit configuration cascade

## Selection

[`github.com/knadh/koanf/v2`](https://github.com/knadh/koanf) v2.3.6 is a modular
configuration library: providers supply data, parsers decode it, and the
application chooses load order and precedence. It is admitted for this
explicit multi-source boundary, active maintenance, tests, documentation, and
small focused design; stdlib remains preferable for trivial configuration.

## Admission checklist

- [x] Current v2.3.6 release and active upstream maintenance.
- [x] Single responsibility: provider/parser/configuration cascade.
- [x] Explicit modules avoid installing every possible source integration.
- [x] Tests, CI, documentation, and typed decoding APIs exist.
- [x] A stable v2 path and migration guidance are available.

## Minimal use

```go
func loadConfig(p koanf.Provider, parser koanf.Parser) (*Config, error) {
    k := koanf.New(".")
    if err := k.Load(p, parser); err != nil {
        return nil, fmt.Errorf("load configuration: %w", err)
    }
    var cfg Config
    if err := k.Unmarshal("", &cfg); err != nil {
        return nil, fmt.Errorf("decode configuration: %w", err)
    }
    return &cfg, nil
}
```

Load defaults before file, environment, and flags when later sources should
override earlier ones. Use `StrictMerge` when incompatible types must fail.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `flag`/`os.Getenv` | Prefer for a single source or a small flat command. |
| Viper | Existing Viper applications should follow their migration policy; new code should compare global state, case handling, and dependency cost explicitly. |
| envconfig | Env-only configuration; not a replacement for a multi-provider cascade. |
| Typed configuration package | Consider when strict compile-time schema and validation are more important than provider flexibility. |

## When to use this library
- Defaults, files, environment, and flags need a visible precedence cascade.
- Providers/parsers should be selected independently with typed decoding.
- A new Go service wants an alternative to Viper's broader/global model.

## When NOT to use this library
- A single value or small flag set is enough for stdlib.
- The project needs implicit case-insensitive keys or a global singleton.
- File watching will run concurrently with `Get`/`Load` without synchronization.
- The project is not prepared to pin and migrate the v2 module/provider paths.

## Advantages
- Provider/parser separation keeps dependencies deliberate.
- Load order and override semantics are explicit.
- Typed unmarshal and strict merge options expose configuration failures early.
- Modular integrations cover file, env, flags, cloud, and secret providers.

## Disadvantages
- Case-sensitive keys and no automatic load order require discipline.
- Providers/parsers add separate modules and their own operational behavior.
- Watching/reloading needs a synchronization policy owned by the application.
- v2.3.6 requires Go 1.23+ and has evolving provider integrations.

## Known pitfalls
- Establish and test one cascade order; later loads override earlier values.
- Synchronize reloads with concurrent readers; the library does not make the
  whole application configuration immutable for you.
- Use `StrictMerge` when incompatible types must be rejected instead of replaced.
- Treat experimental providers as separate admission decisions and pin their
  versions independently.
- Do not store secrets in logs or use unbounded environment/file inputs without
  validation at the configuration boundary.

## Verified sources
- [Official koanf repository](https://github.com/knadh/koanf) — maintenance,
  architecture, license, checked 2026-08-05.
- [koanf v2 on pkg.go.dev](https://pkg.go.dev/github.com/knadh/koanf/v2) — API,
  providers/parsers, and current module metadata, checked 2026-08-05.
- [koanf releases](https://github.com/knadh/koanf/releases) — v2.3.6 current
  version and changes, checked 2026-08-05.
- [v2.3.5 release](https://github.com/knadh/koanf/releases/tag/v2.3.5) —
  provider and merge changes, checked 2026-08-05.
- [Issue #402](https://github.com/knadh/koanf/issues/402) — flag-provider
  precedence limitation, checked 2026-08-05.
- [Issue #183](https://github.com/knadh/koanf/issues/183) — struct decoding
  limitation, checked 2026-08-05.
