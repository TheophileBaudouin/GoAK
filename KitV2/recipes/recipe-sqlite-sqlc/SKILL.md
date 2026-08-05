---
name: recipe-sqlite-sqlc
description: "Accès SQLite fortement typé en Go via la génération de code sqlc v1.31.1 et le pilote pure-Go modernc.org/sqlite v1.56.0 (sans cgo). Utiliser pour tout service Go nécessitant une persistance SQLite robuste et testable."
category: recipe
tags: [sqlite, sqlc, database, sql, codegen, cgo-free]
last-verified: 2026-08-05
---

# recipe-sqlite-sqlc — SQLite sans CGO avec sqlc

## Objectif et cas d'utilisation

Interagir avec une base SQLite de manière fortement typée et portable (sans compilateur C ni CGO), en générant le code d'accès aux données à partir de schémas DDL et de requêtes SQL brutes via `sqlc v1.31.1`.

Utiliser cette recette pour éliminer le code verbeux `rows.Scan()` et attraper les erreurs SQL lors de la génération de code plutôt qu'à l'exécution.

## Prérequis et architecture

- Go 1.25+
- Dépendances :
  - `modernc.org/sqlite v1.56.0` (pilote SQLite pure-Go, zéro CGO)
  - `sqlc v1.31.1` (outil de génération de code CLI)
- Architecture :
  - `schema.sql` définit la structure des tables.
  - `query.sql` contient les requêtes annotées (`-- name: GetFoo :one`, etc.).
  - `sqlc.yaml` configure le générateur (engine: sqlite, emit_json_tags: true).
  - Les fichiers générés (`db.go`, `models.go`, `query.sql.go`) fournissent l'interface `DBTX` et la structure `*Queries`.
  - `Open(dsn string) (*sql.DB, error)` initialise la connexion et applique le schéma via SQL embarqué (`//go:embed schema.sql`).

## Composants et choix

- `modernc.org/sqlite` — pilote 100% pure Go compilé depuis C vers Go (transpilation). Permet le cross-compiling universel avec `CGO_ENABLED=0`.
- `sqlc v1.31.1` — générateur de code SQL de référence qui préserve le SQL comme source de vérité.

## Alternatives rejetées

- `mattn/go-sqlite3` : nécessite `CGO_ENABLED=1` et une chaîne d'outils C complète sur chaque cible de build. Compromet la portabilité.
- `database/sql` sans sqlc : requiert du `Scan()` manuel, sensible aux erreurs d'alignement de types et sans vérification à la compilation.
- GORM / ORM lourd : abstractions complexes qui masquent les requêtes SQL réelles, ralentissent les exécutions et génèrent un SQL imprévisible.

## Exemple complet

```go
package sqlcsqlite

import (
	"context"
	"database/sql"
	_ "embed"
	"fmt"

	_ "modernc.org/sqlite"
)

//go:embed schema.sql
var schemaSQL string

func Open(dsn string) (*sql.DB, error) {
	if dsn == "" {
		dsn = ":memory:"
	}
	db, err := sql.Open("sqlite", dsn)
	if err != nil {
		return nil, fmt.Errorf("open sqlite: %w", err)
	}
	if err := db.PingContext(context.Background()); err != nil {
		_ = db.Close()
		return nil, fmt.Errorf("ping sqlite: %w", err)
	}
	if _, err := db.ExecContext(context.Background(), schemaSQL); err != nil {
		_ = db.Close()
		return nil, fmt.Errorf("apply schema: %w", err)
	}
	return db, nil
}
```

## Bonnes pratiques et pièges

- Exécuter `sqlc generate` à chaque modification de `schema.sql` ou `query.sql` pour maintenir le code Go aligné.
- L'interface `DBTX` générée permet d'exécuter les requêtes aussi bien sur une connexion `*sql.DB` que dans une transaction `*sql.Tx` via `q.WithTx(tx)`.
- Éviter d'insérer des commentaires arbitraires en haut de `query.sql` s'ils ne sont pas directement liés aux requêtes annotées.

## Limites et extensions

Pour les besoins de très fortes performances en écriture concurrente (milliers de requêtes/s), évaluer si WAL mode ou PostgreSQL (`recipe-postgres-pgx`) est nécessaire.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-sqlite-sqlc/...
go run ./probes/sqlite-sqlc
```

La probe ouvre une base de données SQLite en mémoire, insère une entrée via `CreateFoo`, la relit via `GetFoo` et valide les données obtenues avant d'afficher `sqlite-sqlc: PASS`.

## Sources primaires

- [sqlc Documentation](https://docs.sqlc.dev) — guide officiel et tutoriel SQLite.
- [modernc.org/sqlite](https://gitlab.com/cznic/sqlite) — dépôt officiel GitLab du pilote pure-Go.
