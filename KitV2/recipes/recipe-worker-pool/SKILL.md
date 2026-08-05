---
name: recipe-worker-pool
description: "Worker pool avec goroutines bornées et annulation sur première erreur via errgroup.SetLimit. Validation stricte des entrées et respect des annulations de contexte. Utiliser pour le traitement concurrent avec limite de charge."
category: recipe
tags: [concurrency, errgroup, worker-pool, goroutine, context]
last-verified: 2026-08-05
---

# recipe-worker-pool — Worker Pool borné avec errgroup

## Objectif et cas d'utilisation

Exécuter $N$ tâches de manière concurrente tout en plafonnant le nombre maximum de goroutines simultanées (`limit`) et en annulant automatiquement l'ensemble du lot dès qu'un worker rencontre une erreur.

Utiliser ce pattern pour contrôler la concurrence sur les ressources (processeur, connexions DB, appels API distants) sans utiliser de bibliothèques de pool complexes.

## Prérequis et architecture

- Go 1.25+
- Dépendance : `golang.org/x/sync/errgroup`
- Architecture :
  - `Run[T any](ctx context.Context, items []T, limit int, fn func(ctx, item) error) error`
  - Validation stricte des entrées : rejeter `ctx == nil`, `limit < 1`, ou `fn == nil`.
  - Vérifier l'annulation initiale du contexte via `ctx.Err()` avant de démarrer le moindre worker.
  - Dériver `g, workerCtx := errgroup.WithContext(ctx)` et appliquer `g.SetLimit(limit)`.
  - Dans la boucle, vérifier `workerCtx.Err()` pour ne pas planifier de workers inutiles si une annulation a déjà eu lieu.

## Composants et choix

- `golang.org/x/sync/errgroup` — extension canonique maintenue par l'équipe Go.
- `g.SetLimit(n)` — fonctionnalité native Go 1.18+ remplaçant le pattern historique sémaphore/channel + WaitGroup.

## Alternatives rejetées

- Sémaphore manuelle par canal (`chan struct{}` + `sync.WaitGroup`) : ~25 lignes de boilerplate sujettes aux fuites de goroutines et erreurs de gestion du contexte.
- Pools de goroutines persistants (`panjf2000/ants`, `alitto/pond`) : sur-ingénierie inutile pour la plupart des charges applicatives. Justifié uniquement pour des millions de micro-tâches par seconde où l'allocation de goroutines devient le goulet d'étranglement.

## Exemple complet

```go
package pool

import (
	"context"
	"errors"

	"golang.org/x/sync/errgroup"
)

var (
	ErrInvalidLimit = errors.New("worker-pool: limit must be positive")
	ErrNilWorker    = errors.New("worker-pool: worker function must not be nil")
	ErrNilContext   = errors.New("worker-pool: context must not be nil")
)

func Run[T any](ctx context.Context, items []T, limit int, fn func(ctx context.Context, item T) error) error {
	if ctx == nil {
		return ErrNilContext
	}
	if limit < 1 {
		return ErrInvalidLimit
	}
	if fn == nil {
		return ErrNilWorker
	}
	if err := ctx.Err(); err != nil {
		return err
	}
	g, workerCtx := errgroup.WithContext(ctx)
	g.SetLimit(limit)
	for _, item := range items {
		if workerCtx.Err() != nil {
			break
		}
		g.Go(func() error {
			if err := workerCtx.Err(); err != nil {
				return nil
			}
			return fn(workerCtx, item)
		})
	}
	return g.Wait()
}
```

## Bonnes pratiques et pièges

- Depuis Go 1.22, les variables de boucle sont instanciées par itération (`fresh per iteration`) : la capture manuelle `item := item` n'est plus nécessaire.
- Les callbacks `fn` doivent respecter le contexte passe `workerCtx` et interrompre promptement leur traitement lorsque `workerCtx.Done()` est clos.

## Limites et extensions

Si les tâches sont produites en continu de manière indéfinie (stream) plutôt qu'un slice fixe $N$, utiliser une boucle canal/worker dédiée.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-worker-pool/...
go run ./probes/worker-pool
```

La probe exécute un lot valide, puis un lot interrompu par une erreur, vérifie l'arrêt du traitement et affiche `worker-pool: PASS`.

## Sources primaires

- [golang.org/x/sync/errgroup](https://pkg.go.dev/golang.org/x/sync/errgroup) — documentation officielle du package `errgroup`.
