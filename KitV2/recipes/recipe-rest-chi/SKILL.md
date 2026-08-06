---
name: recipe-rest-chi
description: "Idiomatic REST API with the chi v5 router, composable middleware, route groups, bounded JSON decoding (MaxBytesReader), deterministic ordering, and safe logging. Use when building a reusable HTTP REST service."
category: recipe
tags: [rest, http, chi, router, middleware, json]
last-verified: 2026-08-05
---

# recipe-rest-chi — REST API service with chi v5

## Objective and use case

Build an HTTP REST web service in Go with `chi v5` providing composable middleware (`RequestID`, `Recoverer`), sub-routers/route groups, URL parameter extraction, strict size limiting of JSON requests, and event logging without exposing sensitive data.

Use `chi` when the project needs advanced middleware composition or sub-router decomposition while staying 100% compatible with the stdlib `net/http` signature.

## Prerequisites and architecture

- Go 1.25+
- Dependency: `github.com/go-chi/chi/v5 v5.3.1`
- Architecture:
  - `Store` encapsulates the state (in memory or DB) and the `*slog.Logger` logger.
  - The `(s *Store) Router() http.Handler` method instantiates the router and exposes the endpoints.
  - Strict bounding of HTTP request bodies with `http.MaxBytesReader(w, r.Body, 8KB)`.
  - JSON decoding with `decoder.DisallowUnknownFields()` and a check that no residual elements remain.
  - List responses sorted deterministically by ID.
  - Never log request bodies or sensitive client data.

## Components and choices

- `github.com/go-chi/chi/v5` — ultra-light router (~1000 lines of code, 0 external dependencies) purely compatible with `net/http`.
- `log/slog` — standard structured logging with logger injection.
- `middleware.RequestID` and `middleware.Recoverer` — base middleware stack.

## Rejected alternatives

- `net/http` 1.22+ `ServeMux`: suited to simple APIs without complex middleware. Prefer `chi` as soon as route chaining or grouping becomes heavy.
- Gin / Echo: not compatible with `net/http` (proprietary handler signatures `gin.Context` / `echo.Context`), strong framework coupling.
- chi's `middleware.RealIP`: deprecated and vulnerable to IP spoofing (GHSA-3fxj-6jh8-hvhx). Prefer `ClientIPFrom*` depending on the deployment environment.

## Complete example

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

## Best practices and pitfalls

- Always bound the maximum request body size with `http.MaxBytesReader` to avoid memory-exhaustion DoS attacks.
- Use `DisallowUnknownFields()` when decoding JSON to reject unexpected fields.
- Do not put confidential data or client identifiers in structured log attributes.

## Limits and extensions

For complex schema or OpenAPI validation, combine this router with `recipe-openapi-validation`.

## Observable scenario and verification

```sh
go test ./recipes/recipe-rest-chi/...
go run ./probes/rest-chi
```

The probe starts an `httptest` server, performs a `POST /items` request, checks the `201 Created` HTTP status and the returned JSON body, then prints `rest-chi: PASS`.

## Primary sources

- [go-chi/chi](https://github.com/go-chi/chi) — official chi repository.
- [pkg.go.dev/github.com/go-chi/chi/v5](https://pkg.go.dev/github.com/go-chi/chi/v5) — official chi v5 documentation.
