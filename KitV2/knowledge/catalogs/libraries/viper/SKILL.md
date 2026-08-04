---
name: viper
description: "spf13/viper v1.21.0 — broad Go configuration integration for existing applications that need files, environment, flags, or remote stores. Use when Viper is an established project choice; compare Koanf for new explicit cascades."
category: library
tags: [config, viper, env, flags, files]
last-verified: 2026-08-04
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

## Utiliser cette librairie quand

- Une application existante standardise déjà sur Viper (ne pas migrer au
  hasard).
- Des intégrations larges sont nécessaires : fichiers, environnement, flags,
  stores distants (remote key/value).

## Ne pas utiliser cette librairie quand

- Un projet neuf veut une cascade explicite et modulaire : préférer `koanf`
  (providers/parsers séparés).
- Une config plate et petite : stdlib `flag`/`os`/`encoding` suffisent.
- La testabilité et l'ownership des dépendances priment : l'instance
  `viper.New()` reste requise (jamais le singleton package).

## Avantages

- Intégrations très larges (fichiers, env, flags, remote stores) et
  prévalence de fait dans l'écosystème.
- Précédence explicite documentée (Set > flag > env > config > KV > défaut).
- Clés case-insensitives.

## Inconvénients

- Singleton package-level par défaut : état global mutable à éviter
  (`viper.New()`).
- Non sûr en lecture/écriture concurrente sans synchronisation.
- v1.20 a changé encoding et l'intégration mapstructure — upgrade guide
  obligatoire avant toute montée.
- Plus lourd que koanf pour une cascade explicite neuve.

## Pièges connus

- Toujours `viper.New()` pour la testabilité, jamais le singleton global.
- Synchroniser les accès concurrents (lecture/écriture) à l'instance.
- Lire UPGRADE.md avant de monter depuis v1.19 (changements encoding/
  mapstructure).
- Pinner v1.21.0 pour la cible kit actuelle.

## Sources vérifiées

- [spf13/viper (repo officiel, v1.21.0)](https://github.com/spf13/viper) —
  vérifié 2026-08-03
- [pkg.go.dev/github.com/spf13/viper](https://pkg.go.dev/github.com/spf13/viper)
  — vérifié 2026-08-03
- [UPGRADE.md](https://github.com/spf13/viper/blob/master/UPGRADE.md) —
  vérifié 2026-08-03
- Artefacts internes : `recipe-config-viper`, catalog `koanf` (alternative
  modulaire), `pattern:config:twelve-factor-config`
