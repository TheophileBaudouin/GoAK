---
name: cobra
description: "spf13/cobra v1.10.2 — subcommand-based Go CLI framework with POSIX flags, generated help, aliases, and shell completion. Use when a CLI has multiple commands or needs generated help/completion; use recipe-cli-minimal for flat flags."
category: library
tags: [cli, cobra, subcommands, completion, help]
last-verified: 2026-08-04
---

# cobra — multi-command CLI

## Selection

Use `github.com/spf13/cobra` v1.10.2 when a CLI needs subcommands, nested
commands, persistent flags, generated help, aliases, or shell completion. The
standard-library `flag` recipe remains the correct choice for one command with
a small flat flag set.

## Official decision facts

- Commands form a tree; use `AddCommand` to compose subcommands.
- Use `RunE` and `ExecuteC()` so application errors return to the caller and
  remain testable; avoid `CheckErr` in reusable command code because it exits.
- Cobra uses `spf13/pflag` for POSIX-compatible short and long flags.
- `MarkFlagRequired`, mutually-exclusive flag validation, command groups, and
  generated shell completion are optional features, not reasons to use Cobra
  for every CLI.
- The official Cobra documentation includes an LLM-ready CLI documentation
  guide; no repository `llms.txt` file is required or copied into the kit.

## Limits and security

- Cobra and pflag add dependencies and mutable package-level options; keep
  command construction in a factory and avoid shared command trees in tests.
- Validate arguments and flags at the command boundary.
- Do not pass secrets through flags when process listings or shell history can
  expose them; use a protected configuration source instead.
- Pin versions and inspect pflag changes during upgrades.

## Utiliser cette librairie quand

- La CLI a plusieurs commandes ou commandes imbriquées (arbre de commandes),
  des flags persistants, du help généré, des alias ou de la completion shell.
- Des conventions POSIX de flags (short/long via pflag) sont attendues.

## Ne pas utiliser cette librairie quand

- Une seule commande avec un petit jeu de flags plats : stdlib `flag` suffit
  (`recipe-cli-minimal`).
- Le help généré et la completion shell ne sont pas nécessaires.
- L'objectif est une librairie réutilisable qui ne doit pas appeler `os.Exit`.

## Avantages

- Standard de facto des CLIs Go (docker, kubectl, gh, hugo).
- Commandes composables (`AddCommand`), flags persistants/locaux, help +
  completion générés.
- `RunE` + `ExecuteC()` rendent les erreurs applicatives testables.

## Inconvénients

- Ajoute des dépendances (cobra + pflag) et des options package-level
  mutables.
- Modèle à apprendre (arbre de commandes, binding de flags) — coût réel pour
  un CLI plat.
- Sur-dimensionné quand `flag` couvre le besoin.

## Pièges connus

- Éviter `CheckErr` dans le code réutilisable (il exit) : utiliser `RunE` et
  `ExecuteC()` pour que les erreurs remontent à l'appelant.
- Ne pas partager un arbre de commandes global dans les tests (état mutable) —
  garder la construction dans une factory.
- Valider arguments et flags à la frontière de commande.
- Ne pas passer de secrets par flags (exposés dans le process listing et
  l'historique shell) : source de configuration protégée.
- Pinner les versions et inspecter pflag lors des montées de version.

## Sources vérifiées

- [spf13/cobra (repo officiel, v1.10.2)](https://github.com/spf13/cobra) —
  vérifié 2026-08-03
- [pkg.go.dev/github.com/spf13/cobra](https://pkg.go.dev/github.com/spf13/cobra)
  — vérifié 2026-08-03
- [cobra.dev/docs](https://cobra.dev/docs/) — vérifié 2026-08-03
- [cobra.dev — CLIs for LLMs](https://cobra.dev/docs/how-to-guides/clis-for-llms/)
  — vérifié 2026-08-03
- Artefacts internes : `recipe-cli-minimal` (frontière flag),
  `pattern:cli:subcommands-conventions`
