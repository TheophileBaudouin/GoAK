---
name: koanf
description: "knadh/koanf v2.3.5 — modular multi-source configuration with separate providers and parsers. Use when loading defaults plus file, environment, or flag sources with an explicit cascade and typed decoding."
category: library
tags: [config, koanf, viper-alternative, env, flags]
last-verified: 2026-08-04
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

## Utiliser cette librairie quand

- La config provient de plusieurs sources (défauts + fichier + env + flags)
  avec une cascade de précédence explicite et un décodage typé.
- Chaque source veut son provider/parser choisi explicitement, sans
  dépendances inutiles.
- Un projet neuf cherche une alternative structurée à Viper.

## Ne pas utiliser cette librairie quand

- Une seule valeur ou un petit jeu de flags plats : stdlib `flag` suffit.
- Une application Viper existante : ne pas migrer au hasard (catalog viper +
  guidance de migration).
- Le watching de fichiers est requis SANS synchronisation avec les
  `Get`/`Load` concurrents (koanf ne synchronise pas pour vous).

## Avantages

- Providers/parsers séparés : on installe seulement ce qu'on utilise.
- Cascade explicite (dernier chargé écrase), décodage typé, `StrictMerge`
  pour échouer sur types incompatibles.
- Cas-sensitive assumé, pas de magie implicite d'ordre.

## Inconvénients

- Cas-sensitive et sans ordre imposé : la discipline de cascade est à la
  charge de l'appelant.
- Watching de fichiers non sûr avec accès concurrent sans synchronisation.
- v2 a changé le chemin de module (/v2) et éclaté providers/parsers —
  migration à faire consciencieusement.

## Pièges connus

- Toujours charger les défauts AVANT fichier/env/flags (ordre = précédence).
- Garder l'instance de config locale ou synchroniser les rechargements avec
  les lecteurs concurrents.
- Consulter les notes de migration v2 avant une montée de version.
- Utiliser `StrictMerge` quand des types incompatibles doivent échouer plutôt
  que d'être silencieusement remplacés.

## Sources vérifiées

- [knadh/koanf (repo officiel, v2.3.5)](https://github.com/knadh/koanf) —
  vérifié 2026-08-03
- [pkg.go.dev/github.com/knadh/koanf/v2](https://pkg.go.dev/github.com/knadh/koanf/v2)
  — vérifié 2026-08-03
- Artefacts internes : `recipe-config-koanf`, catalog `viper` (comparaison),
  `pattern:config:twelve-factor-config`, `pattern:antipattern:cfg-hardcoded-values`
