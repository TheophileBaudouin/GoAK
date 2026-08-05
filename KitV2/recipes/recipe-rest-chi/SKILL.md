---
name: recipe-rest-chi
description: "API REST idiomatic avec le routeur chi v5, middleware composable, groupes de routes, décodage JSON borné (MaxBytesReader), tri déterministe et journalisation sécurisée. Utiliser pour concevoir un service HTTP REST réutilisable."
category: recipe
tags: [rest, http, chi, router, middleware, json]
last-verified: 2026-08-05
---

# recipe-rest-chi — Service API REST avec chi v5

## Objectif et cas d'utilisation

Construire un service Web HTTP REST en Go avec `chi v5` offrant des middlewares composables (`RequestID`, `Recoverer`), des sous-routeurs/groupes de routes, l'extraction de paramètres d'URL, la limitation stricte de la taille des requêtes JSON et la journalisation d'événements sans exposer de données sensibles.

Utiliser `chi` lorsque le projet nécessite une composition avancée de middlewares ou un découpage en sous-routeurs tout en restant 100% compatible avec la signature stdlib `net/http`.

## Prérequis et architecture

- Go 1.25+
- Dépendance : `github.com/go-chi/chi/v5 v5.3.1`
- Architecture :
  - `Store` encapsule l'état (en mémoire ou DB) et le logger `*slog.Logger`.
  - La méthode `(s *Store) Router() http.Handler` instancie le routeur et expose les endpoints.
  - Bornage strict des corps de requêtes HTTP avec `http.MaxBytesReader(w, r.Body, 8KB)`.
  - Décodage JSON avec `decoder.DisallowUnknownFields()` et contrôle d'absence d'éléments résiduels.
  - Réponses de liste triées de manière déterministe par ID.
  - Ne jamais journaliser les corps de requêtes ou données sensibles clients.

## Composants et choix

- `github.com/go-chi/chi/v5` — routeur ultra-léger (~1000 lignes de code, 0 dépendances externes) purement compatible `net/http`.
- `log/slog` — journalisation structurée standard avec injection de logger.
- `middleware.RequestID` et `middleware.Recoverer` — pile middleware de base.

## Alternatives rejetées

- `net/http` 1.22+ `ServeMux` : adapté aux APIs simples sans middleware complexe. Préférer `chi` dès que le chaînage ou le groupement de routes devient lourd.
- Gin / Echo : non compatibles avec `net/http` (signatures de handler propriétaires `gin.Context` / `echo.Context`), couplage fort au framework.
- `middleware.RealIP` de chi : déprécié et vulnérable à l'usurpation d'IP (GHSA-3fxj-6jh8-hvhx). Préférer `ClientIPFrom*` selon l'environnement de déploiement.

## Exemple complet

```go
package restchi

import (
	"encoding/json"
	"io"
	"log/slog"
	"net/http"
	"sort"
	"strconv"
	"strings"
	"sync"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
)

const maxRequestBodyBytes = 8 << 10

type Item struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type Store struct {
	mu     sync.RWMutex
	nextID int
	items  map[int]Item
	log    *slog.Logger
}

func NewStore() *Store {
	return NewStoreWithLogger(slog.Default())
}

func NewStoreWithLogger(logger *slog.Logger) *Store {
	if logger == nil {
		logger = slog.Default()
	}
	return &Store{nextID: 1, items: make(map[int]Item), log: logger}
}

func (s *Store) Router() http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.RequestID, middleware.Recoverer)

	r.Route("/items", func(r chi.Router) {
		r.Get("/", s.listItems)
		r.Post("/", s.createItem)
		r.Get("/{id}", s.getItem)
	})
	return r
}
```

## Bonnes pratiques et pièges

- Toujours borner la taille maximale du corps de requête avec `http.MaxBytesReader` pour éviter les attaques DoS par mémoire saturée.
- Utiliser `DisallowUnknownFields()` lors du décodage JSON pour rejeter les champs inattendus.
- Ne pas placer de données confidentielles ou d'identifiants clients dans les attributs de log structurés.

## Limites et extensions

Pour la validation de schémas complexes ou OpenAPI, combiner ce routeur avec `recipe-openapi-validation`.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-rest-chi/...
go run ./probes/rest-chi
```

La probe lance un serveur `httptest`, effectue une requête `POST /items`, vérifie le statut HTTP `201 Created` et le corps JSON de retour, puis affiche `rest-chi: PASS`.

## Sources primaires

- [go-chi/chi](https://github.com/go-chi/chi) — dépôt officiel chi.
- [pkg.go.dev/github.com/go-chi/chi/v5](https://pkg.go.dev/github.com/go-chi/chi/v5) — documentation officielle chi v5.
