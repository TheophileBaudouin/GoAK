---
name: recipe-cli-cobra
description: "CLI multi-commandes testable avec sous-commandes Cobra, validation d'arguments, gestion explicite des sorties io.Writer, aide générée et limites d'autocomplétion. Utiliser pour une CLI Go à sous-commandes ou flags persistants."
category: recipe
tags: [cli, cobra, subcommands, flags, validation]
last-verified: 2026-08-05
---

# recipe-cli-cobra — CLI multi-commandes avec Cobra

## Objectif et cas d'utilisation

Construire une CLI Go multi-commandes testable (ex. `app greet --name Ada`) avec des sous-commandes, des drapeaux locaux et globaux, une validation stricte des arguments et des erreurs de sortie capturables sans quitter prématurément le processus via `os.Exit`.

Utiliser Cobra uniquement lorsque l'application requiert une arborescence de sous-commandes (`git clone`, `git commit`), des alias, de l'aide automatique ou de l'autocomplétion. Pour un outil à commande unique et drapeaux plats, utiliser `recipe-cli-minimal`.

## Prérequis et architecture

- Go 1.25+
- Dépendance externe : `github.com/spf13/cobra v1.10.2`
- Architecture testable :
  - Encapsuler la création de la commande dans une fabrique `NewCommand(out io.Writer) *cobra.Command`.
  - Utiliser `RunE` pour retourner les erreurs au lieu d'appeler `os.Exit`.
  - Configurer `SilenceUsage: true` et `SilenceErrors: true` pour laisser le point d'entrée `main` contrôler le formatage d'erreur.
  - Injecter un `io.Writer` pour capturer la sortie standard dans les tests (ex. `bytes.Buffer`).

## Composants et choix

- `github.com/spf13/cobra` — standard de fait pour les CLI Go complexes (utilisé par Kubernetes, Hugo, GitHub CLI).
- `ExecuteC()` — permet d'exécuter l'arbre de commande en retournant la commande active et l'erreur.
- `Args: cobra.NoArgs` — validation stricte rejetant les arguments positionnels inattendus.

## Alternatives rejetées

- `flag` (stdlib) : limité aux drapeaux plats sans sous-commandes. Idéal pour les petits outils, insuffisant pour les arborescences.
- `spf13/pflag` seul : ajoute les drapeaux style POSIX (long/short), mais ne gère pas l'arborescence de sous-commandes.
- `urfave/cli` : API alternative valide, mais introduit une dépendance supplémentaire concurrente sans avantage décisif sur Cobra.
- États globaux mutables (`cobra.Command` global) : rend les tests dépendants de l'ordre d'exécution et non isolés.

## Exemple complet

```go
package cobracli

import (
	"fmt"
	"io"
	"strings"

	"github.com/spf13/cobra"
)

func NewCommand(out io.Writer) *cobra.Command {
	if out == nil {
		out = io.Discard
	}
	var name string
	root := &cobra.Command{
		Use:           "app",
		Short:         "Application multi-commandes",
		SilenceUsage:  true,
		SilenceErrors: true,
	}
	greet := &cobra.Command{
		Use:   "greet",
		Short: "Saluer une personne",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, args []string) error {
			if strings.TrimSpace(name) == "" {
				return fmt.Errorf("name must not be empty")
			}
			_, err := fmt.Fprintf(out, "hello %s\n", name)
			return err
		},
	}
	greet.Flags().StringVar(&name, "name", "", "nom de la personne")
	root.AddCommand(greet)
	return root
}
```

## Bonnes pratiques et pièges

- Éviter `cobra.CheckErr()` dans les handlers de sous-commandes : il appelle `os.Exit(1)` et empêche tout nettoyage ou test.
- Réinitialiser ou réinstancier l'arbre de commande pour chaque test via `NewCommand(&buf)`.
- Valider systématiquement les arguments positionnels et les options obligatoire au début de `RunE`.
- Ne jamais passer de secrets par les drapeaux de ligne de commande : ils sont visibles dans la liste des processus (`ps aux`) et l'historique shell.

## Limites et extensions

Cobra ajoute une dépendance transitive importante (`pflag`, etc.). Ne pas l'utiliser par réflexe pour des scripts ou des micro-services nécessitant uniquement 2-3 drapeaux de configuration.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-cli-cobra/...
go run ./probes/cli-cobra
```

La probe instancie la commande, exécute `greet --name Ada` et vérifie la sortie exacte `hello Ada\n`, puis affiche `cli-cobra: PASS`.

## Sources primaires

- [spf13/cobra](https://github.com/spf13/cobra) — dépôt officiel Cobra.
- [Cobra Documentation](https://cobra.dev/docs/) — guides d'architecture et recommandations pour les CLI LLM.
- [pkg.go.dev/github.com/spf13/cobra](https://pkg.go.dev/github.com/spf13/cobra) — référence API.
