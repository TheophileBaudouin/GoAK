// Package sqlcsqlite demonstrates sqlc-generated SQLite query methods with a
// pure-Go (cgo-free) driver. The generated files are derived only from
// schema.sql, query.sql, and sqlc.yaml by sqlc v1.31.1.
package sqlcsqlite

import (
	"context"
	"database/sql"
	_ "embed"
	"fmt"

	_ "modernc.org/sqlite" // registers the "sqlite" driver (pure Go, no cgo)
)

// schemaSQL is the schema source used by sqlc; embedding avoids a second DDL
// copy in Go while allowing Open to initialise an in-memory example database.
//
//go:embed schema.sql
var schemaSQL string

// Open returns a *sql.DB backed by an in-memory SQLite database with the schema
// applied. Pass a file path (e.g. "file:app.db") for a persistent database.
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
		_ = db.Close() // best-effort cleanup; the real error is schema application
		return nil, fmt.Errorf("apply schema: %w", err)
	}
	return db, nil
}
