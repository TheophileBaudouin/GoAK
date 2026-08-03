---
name: recipe-config-koanf
description: "Explicit layered configuration with Koanf v2 providers and parsers. Use when an application combines defaults with file, environment, or flag sources and needs an explicit merge order."
category: recipe
tags: [config, koanf, env, files, flags]
last-verified: 2026-08-03
---

# recipe-config-koanf — explicit configuration cascade

## Selection

Use `github.com/knadh/koanf/v2` when configuration comes from multiple
sources and the application should choose providers, parsers, and precedence
explicitly. Koanf v2 keeps providers and parsers in separate modules; import
only the modules the application needs.

For one value or a flat flag set, use the standard library instead. The
canonical decision record is the `koanf` library catalog.

## Canonical shape

Load defaults first, then later sources override them. Keep the `*koanf.Koanf`
instance local to the loading operation or protect it when reloading while
other goroutines read it. Use `StrictMerge` when incompatible value types must
fail instead of being replaced.

The runnable example uses the official `confmap` provider and typed
`Unmarshal`. File, environment, and flag providers are added by a consuming
application as required.

## Limits

- Koanf does not impose a source order; the recipe must define one.
- Provider and parser modules add their own dependencies.
- A provider watcher is not safe to combine with concurrent reads without
  synchronization.
- Do not switch an existing project from Viper to Koanf without a migration
  decision; this recipe is for new configuration boundaries.

## Verification

```sh
go test ./recipes/recipe-config-koanf/...
```

## Sources

- <https://github.com/knadh/koanf>
- <https://pkg.go.dev/github.com/knadh/koanf/v2>
- <https://pkg.go.dev/github.com/knadh/koanf/providers/confmap>
