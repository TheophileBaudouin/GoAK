// Package sqlcsqlite demonstrates the sqlc + SQLite workflow with a pure-Go
// (cgo-free) driver.
//
// sqlc is a code generator: you write plain SQL (see query.sql) and it emits
// type-safe Go query methods at build time. This package ships a hand-written
// stand-in for the generated *Queries type so the recipe is runnable and tested
// without requiring a live `sqlc generate` step — but its shape is exactly what
// `sqlc generate` produces, so it teaches the real pattern.
//
// Driver choice: modernc.org/sqlite is a pure-Go port of SQLite. It needs no C
// compiler, so the binary cross-compiles natively (CGO_ENABLED=0). That matters
// more for a universal kit than the marginal raw speed of the cgo driver.
package sqlcsqlite

import (
	"context"
	"database/sql"
	"fmt"

	_ "modernc.org/sqlite" // registers the "sqlite" driver (pure Go, no cgo)
)

// Foo mirrors the row sqlc would generate in models.go from schema.sql.
type Foo struct {
	ID        int64  `json:"id"`
	Name      string `json:"name"`
	CreatedAt string `json:"created_at"`
}

// DBTX is the minimal surface sqlc's generated *Queries depends on. Both
// *sql.DB and *sql.Tx satisfy it, so the same generated code works inside or
// outside a transaction without changes.
type DBTX interface {
	ExecContext(ctx context.Context, query string, args ...any) (sql.Result, error)
	QueryContext(ctx context.Context, query string, args ...any) (*sql.Rows, error)
	QueryRowContext(ctx context.Context, query string, args ...any) *sql.Row
}

// Queries is the type sqlc generates. Methods are thin wrappers around the SQL
// that give you compile-time type safety instead of manual rows.Scan plumbing.
type Queries struct {
	db DBTX
}

// New returns a Queries bound to db (a *sql.DB in the common case).
func New(db DBTX) *Queries {
	return &Queries{db: db}
}

// CreateFoo inserts a row and returns its generated id.
// (sqlc emits :execlastid / :execresult variants; last-insertID is the common need.)
func (q *Queries) CreateFoo(ctx context.Context, name string) (int64, error) {
	res, err := q.db.ExecContext(ctx, `INSERT INTO foos (name) VALUES (?)`, name)
	if err != nil {
		return 0, fmt.Errorf("insert foo: %w", err)
	}
	id, err := res.LastInsertId()
	if err != nil {
		return 0, fmt.Errorf("last insert id: %w", err)
	}
	return id, nil
}

// GetFoo fetches a single row by id. sqlc generates this for the `:one` query.
func (q *Queries) GetFoo(ctx context.Context, id int64) (Foo, error) {
	row := q.db.QueryRowContext(ctx, `SELECT id, name, created_at FROM foos WHERE id = ?`, id)
	var f Foo
	if err := row.Scan(&f.ID, &f.Name, &f.CreatedAt); err != nil {
		return Foo{}, fmt.Errorf("get foo %d: %w", id, err)
	}
	return f, nil
}

// ListFoos fetches all rows. sqlc generates this for the `:many` query.
func (q *Queries) ListFoos(ctx context.Context) ([]Foo, error) {
	rows, err := q.db.QueryContext(ctx, `SELECT id, name, created_at FROM foos ORDER BY id`)
	if err != nil {
		return nil, fmt.Errorf("list foos: %w", err)
	}
	defer func() { _ = rows.Close() }() // rows error is reported via rows.Err(); Close just releases the cursor

	var out []Foo
	for rows.Next() {
		var f Foo
		if err := rows.Scan(&f.ID, &f.Name, &f.CreatedAt); err != nil {
			return nil, fmt.Errorf("scan foo: %w", err)
		}
		out = append(out, f)
	}
	return out, rows.Err()
}

// schemaSQL is the DDL, kept in code so callers can spin up an in-memory DB in
// one call. It mirrors schema.sql verbatim.
const schemaSQL = `
CREATE TABLE IF NOT EXISTS foos (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    created_at TEXT    NOT NULL DEFAULT (datetime('now'))
);
`

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
	if _, err := db.Exec(schemaSQL); err != nil {
		_ = db.Close() // best-effort cleanup; the real error is schema application
		return nil, fmt.Errorf("apply schema: %w", err)
	}
	return db, nil
}
