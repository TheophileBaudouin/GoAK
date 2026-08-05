---
name: recipe-graceful-shutdown
description: "Arrêt propre (graceful shutdown) testable d'un serveur HTTP en Go via signal.NotifyContext, http.Server.Shutdown et délai d'expiration (timeout). Utiliser pour tout service HTTP devant drainer les requêtes sur SIGINT/SIGTERM."
category: recipe
tags: [shutdown, http, signal, context, stdlib]
last-verified: 2026-08-05
---

# recipe-graceful-shutdown — Arrêt propre de serveur HTTP (Graceful Shutdown)

## Objectif et cas d'utilisation

Arrêter un serveur HTTP Go de manière propre lors de la réception d'un signal système (SIGINT, SIGTERM) : refuser les nouvelles connexions, laisser les requêtes en cours s'exécuter jusqu'à leur terme dans la limite d'un délai d'expiration (timeout), tout en gardant l'orchestration totalement testable au niveau unitaire.

Utiliser cette recette pour tous les services Web exposés en production afin d'éviter la coupure abrupte des connexions clients lors de redéploiements ou d'arrêts de pods (ex. Kubernetes).

## Prérequis et architecture

- Go 1.25+ (stdlib uniquement : `net/http`, `os/signal`, `context`)
- Architecture testable :
  - Séparer la capture des signaux OS (qui appartient au `main`) de l'orchestrateur d'arrêt `shutdown.Run(...)`.
  - `Run(ctx context.Context, srv *http.Server, ln net.Listener, timeout time.Duration) error`
  - `Run` écoute l'annulation du contexte transmis. En cas d'annulation, il déclenche `srv.Shutdown(shutdownCtx)` avec un nouveau contexte à délai d'expiration (`timeout`).
  - L'erreur `http.ErrServerClosed` renvoyée par `Serve` lors d'un arrêt normal est absorbée et ne fait pas échouer `Run`.

## Composants et choix

- `signal.NotifyContext` (Go 1.16+) — API stdlib propre créant un contexte annulé lors de la réception d'un signal OS.
- `http.Server.Shutdown` — méthode stdlib drainant les connexions HTTP.

## Alternatives rejetées

- Capturer les signaux directement dans l'orchestrateur : empêche de tester l'arrêt en mode unitaire sans envoyer de véritables signaux OS au processus de test.
- `signal.Notify(chan os.Signal)` pré-1.16 : verbeux, réinvente la gestion du contexte.
- Paquets tiers (`appleboy/graceful`, etc.) : sur-ingénierie apportant des dépendances inutiles pour une fonctionnalité native de la stdlib.

## Exemple complet

```go
package shutdown

import (
	"context"
	"errors"
	"net"
	"net/http"
	"time"
)

func Run(ctx context.Context, srv *http.Server, ln net.Listener, timeout time.Duration) error {
	serveErr := make(chan error, 1)
	go func() {
		err := srv.Serve(ln)
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			serveErr <- err
			return
		}
		serveErr <- nil
	}()

	select {
	case err := <-serveErr:
		return err
	case <-ctx.Done():
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	return srv.Shutdown(shutdownCtx)
}
```

```go
// Dans main.go :
ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
defer stop()
if err := shutdown.Run(ctx, srv, ln, 5*time.Second); err != nil {
	log.Fatal(err)
}
```

## Bonnes pratiques et pièges

- Assurer que le délai `timeout` est inférieur au délai de grâce de l'orchestrateur (ex. `terminationGracePeriodSeconds` dans Kubernetes).
- Les handlers HTTP de longue durée doivent écouter `r.Context().Done()` pour s'interrompre si le timeout d'arrêt est dépassé.

## Limites et extensions

Pour éteindre simultanément d'autres composants (workers en arrière-plan, pools de connexions DB), combiner cette logique avec `golang.org/x/sync/errgroup`.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-graceful-shutdown/...
go run ./probes/graceful-shutdown
```

La probe instancie un serveur HTTP, déclenche l'arrêt via l'annulation du contexte, vérifie l'absorption de `http.ErrServerClosed` et la fermeture propre, puis affiche `graceful-shutdown: PASS`.

## Sources primaires

- [net/http Server.Shutdown](https://pkg.go.dev/net/http#Server.Shutdown) — documentation stdlib.
- [os/signal NotifyContext](https://pkg.go.dev/os/signal#NotifyContext) — documentation stdlib.
