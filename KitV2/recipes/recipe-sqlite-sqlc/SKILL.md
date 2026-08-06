---
name: recipe-sqlite-sqlc
description: "Typed SQLite access in Go via sqlc v1.31.1 code generation and the pure-Go driver modernc.org/sqlite v1.56.0 (cgo-free). Use for any Go service needing robust, testable SQLite persistence."
category: recipe
tags: [sqlite, sqlc, database, sql, codegen, cgo-free]
last-verified: 2026-08-05
---

# recipe-sqlite-sqlc — CGO-free SQLite with sqlc

## Goal and use case

Interact with a SQLite database in a strongly typed and portable way (no C compiler, no CGO), by generating data-access code from DDL schemas and raw SQL queries via `sqlc v1.31.1`.

Use this recipe to eliminate verbose `rows.Scan()` code and to catch SQL errors at code-generation time rather than at runtime.

## Prerequisites and architecture

- Go 1.25+
- Dependencies:
  - `modernc.org/sqlite v1.56.0` (pure-Go SQLite driver, zero CGO)
  - `sqlc v1.31.1` (CLI code-generation tool)
- Architecture:
  - `schema.sql` defines the table structure.
  - `query.sql` contains the annotated queries (`-- name: GetFoo :one`, etc.).
  - `sqlc.yaml` configures the generator (engine: sqlite, emit_json_tags: true).
  - The generated files (`db.go`, `models.go`, `query.sql.go`) provide the `DBTX` interface and the `*Queries` struct.
  - `Open(dsn string) (*sql.DB, error)` initializes the connection and applies the schema via embedded SQL (`//go:embed schema.sql`).

## Components and choices

- `modernc.org/sqlite` — 100% pure Go driver compiled from C to Go (transpilation). Enables universal cross-compiling with `CGO_ENABLED=0`.
- `sqlc v1.31.1` — reference SQL code generator that keeps SQL as the source of truth.

## Rejected alternatives

- `mattn/go-sqlite3`: requires `CGO_ENABLED=1` and a full C toolchain on every build target. Compromises portability.
- `database/sql` without sqlc: requires manual `Scan()`, prone to type-alignment errors, and without compile-time checking.
- GORM / heavy ORM: complex abstractions that hide the real SQL queries, slow down execution, and generate unpredictable SQL.

## Complete example

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

## Best practices and pitfalls

- Run `sqlc generate` after every change to `schema.sql` or `query.sql` to keep the Go code in sync.
- The generated `DBTX` interface allows running queries on either a `*sql.DB` connection or inside a `*sql.Tx` transaction via `q.WithTx(tx)`.
- Avoid inserting arbitrary comments at the top of `query.sql` when they are not directly related to the annotated queries.

## Limits and extensions

For very high concurrent write performance needs (thousands of queries/s), evaluate whether WAL mode or PostgreSQL (`recipe-postgres-pgx`) is required.

## Observable scenario and verification

```sh
go test ./recipes/recipe-sqlite-sqlc/...
go run ./probes/sqlite-sqlc
```

The probe opens an in-memory SQLite database, inserts an entry via `CreateFoo`, reads it back via `GetFoo`, and validates the retrieved data before printing `sqlite-sqlc: PASS`.

## Primary sources

- [sqlc Documentation](https://docs.sqlc.dev) — official guide and SQLite tutorial.
- [modernc.org/sqlite](https://gitlab.com/cznic/sqlite) — official GitLab repository of the pure-Go driver.
