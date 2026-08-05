---
name: recipe-cli-minimal
description: "Analyse minimale et testable des drapeaux CLI en Go via le package flag de la bibliothèque standard (flag.NewFlagSet + flag.ContinueOnError + io.Writer). Utiliser pour une CLI à commande unique sans sous-commandes."
category: recipe
tags: [cli, flag, stdlib, config, args]
last-verified: 2026-08-05
---

# recipe-cli-minimal — CLI minimale avec le package stdlib flag

## Objectif et cas d'utilisation

Construire un parseur de drapeaux de ligne de commande testable pour une application à commande unique en utilisant uniquement le package `flag` de la bibliothèque standard Go, sans fuite d'état global ni appels irrécupérables à `os.Exit`.

Utiliser cette recette pour toute CLI simple à drapeaux plats nécessitant zéro dépendance externe.

## Prérequis et architecture

- Go 1.25+ (stdlib uniquement)
- Le pivot de testabilité (hinge) :
  - `flag.Parse()` opère sur le singleton global `flag.CommandLine` avec `ExitOnError`, appelant `os.Exit(2)` en cas d'erreur. C'est non testable.
  - La solution consiste à créer une fonction `ParseTo(args []string, w io.Writer) (Config, error)`.
  - Instancier un `*flag.FlagSet` dédié avec `flag.ContinueOnError`.
  - Rediriger la sortie avec `fs.SetOutput(w)` (passer `io.Discard` dans les tests).
  - Parser le slice d'arguments explicite `args` au lieu d'accéder à `os.Args`.

## Composants et choix

- `flag.NewFlagSet("app", flag.ContinueOnError)` — crée un jeu de drapeaux isolé qui renvoie les erreurs au lieu de tuer le processus.
- `fs.NArg()` — permet d'interdire les arguments positionnels inattendus.

## Alternatives rejetées

- `flag.Parse()` global : utilise `ExitOnError` et `os.Args`, rendant les tests unitaires impossibles.
- `spf13/cobra` / `urfave/cli` : sur-ingénierie inutile pour les CLI simples sans sous-commandes.
- `spf13/pflag` : ajoute la syntaxe POSIX (drapeaux courts/longs), mais introduit une dépendance externe non requise pour les besoins simples.

## Exemple complet

```go
package cli

import (
	"flag"
	"fmt"
	"io"
	"os"
)

type Config struct {
	Host    string
	Port    int
	Verbose bool
}

func Parse(args []string) (Config, error) {
	return ParseTo(args, os.Stderr)
}

func ParseTo(args []string, w io.Writer) (Config, error) {
	var c Config
	if w == nil {
		w = io.Discard
	}
	fs := flag.NewFlagSet("app", flag.ContinueOnError)
	fs.SetOutput(w)
	fs.StringVar(&c.Host, "host", "127.0.0.1", "listen host")
	fs.IntVar(&c.Port, "port", 8080, "listen port")
	fs.BoolVar(&c.Verbose, "verbose", false, "enable verbose logging")
	if err := fs.Parse(args); err != nil {
		return c, err
	}
	if fs.NArg() != 0 {
		return c, fmt.Errorf("unexpected positional arguments: %q", fs.Args())
	}
	return c, nil
}
```

## Bonnes pratiques et pièges

- Distinguer l'aide (`flag.ErrHelp`) des erreurs de parsing : `ParseTo` renvoie `flag.ErrHelp` quand `-h` ou `-help` est utilisé, permettant au `main` d'avoir un exit 0.
- Transmettre `io.Discard` dans les tests pour ne pas polluer les journaux de test avec le texte d'aide du FlagSet.

## Limites et extensions

Si l'application évolue vers une structure complexe avec sous-commandes (`app build`, `app deploy`), migrer vers `recipe-cli-cobra`.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-cli-minimal/...
go run ./probes/cli-minimal
```

La probe exécute `ParseTo` avec des arguments explicites, vérifie la structure `Config` résultante et affiche `cli-minimal: PASS`.

## Sources primaires

- [Go flag package](https://pkg.go.dev/flag) — documentation officielle du package stdlib `flag`.
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments#flag-packages) — recommandations d'utilisation du package flag.
