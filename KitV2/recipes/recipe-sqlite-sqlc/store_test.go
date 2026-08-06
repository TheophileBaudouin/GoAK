package sqlcsqlite

import (
	"context"
	"database/sql"
	"errors"
	"sort"
	"testing"
)

func newQueries(t *testing.T) *Queries {
	t.Helper()
	db, err := Open(":memory:")
	if err != nil {
		t.Fatalf("Open: %v", err)
	}
	t.Cleanup(func() { _ = db.Close() })
	return New(db)
}

func TestCreateAndGetFoo(t *testing.T) {
	q := newQueries(t)
	ctx := context.Background()

	id, err := q.CreateFoo(ctx, "alpha")
	if err != nil {
		t.Fatalf("CreateFoo: %v", err)
	}
	if id != 1 {
		t.Fatalf("first id = %d, want 1", id)
	}

	foo, err := q.GetFoo(ctx, id)
	if err != nil {
		t.Fatalf("GetFoo: %v", err)
	}
	if foo.Name != "alpha" {
		t.Fatalf("name = %q, want alpha", foo.Name)
	}
	if foo.CreatedAt == "" {
		t.Fatal("CreatedAt empty, want default datetime value")
	}
}

func TestGetFoo_notFound(t *testing.T) {
	q := newQueries(t)
	ctx := context.Background()

	_, err := q.GetFoo(ctx, 999)
	if !errors.Is(err, sql.ErrNoRows) {
		t.Fatalf("err = %v, want sql.ErrNoRows", err)
	}
}

func TestListFoos(t *testing.T) {
	q := newQueries(t)
	ctx := context.Background()

	for _, name := range []string{"a", "b", "c"} {
		if _, err := q.CreateFoo(ctx, name); err != nil {
			t.Fatalf("CreateFoo %q: %v", name, err)
		}
	}

	foos, err := q.ListFoos(ctx)
	if err != nil {
		t.Fatalf("ListFoos: %v", err)
	}
	if len(foos) != 3 {
		t.Fatalf("len = %d, want 3", len(foos))
	}

	got := []string{foos[0].Name, foos[1].Name, foos[2].Name}
	want := []string{"a", "b", "c"}
	sort.Strings(got)
	// ListFoos orders by id (insertion order), so names are already a,b,c.
	for i := range want {
		if got[i] != want[i] {
			t.Fatalf("names = %v, want %v", got, want)
		}
	}
}

func TestOpenDefaultsAndErrors(t *testing.T) {
	if _, err := Open(""); err != nil {
		t.Fatalf("Open with empty DSN (default :memory:) failed: %v", err)
	}
	if _, err := Open("file:/no/such/directory-xyz/db.sqlite"); err == nil {
		t.Fatal("Open accepted an unreachable file DSN")
	}
}

func TestWithTxCommitAndRollback(t *testing.T) {
	db, err := Open(":memory:")
	if err != nil {
		t.Fatalf("Open: %v", err)
	}
	defer func() { _ = db.Close() }()
	ctx := context.Background()
	q := New(db)

	// Committed transaction: the row is visible after Commit.
	tx, err := db.Begin()
	if err != nil {
		t.Fatalf("Begin: %v", err)
	}
	tq := q.WithTx(tx)
	if _, err := tq.CreateFoo(ctx, "in-tx"); err != nil {
		t.Fatalf("CreateFoo in tx: %v", err)
	}
	if err := tx.Commit(); err != nil {
		t.Fatalf("Commit: %v", err)
	}
	rows, err := q.ListFoos(ctx)
	if err != nil {
		t.Fatalf("ListFoos: %v", err)
	}
	if len(rows) != 1 || rows[0].Name != "in-tx" {
		t.Fatalf("after commit: %+v, want one in-tx row", rows)
	}

	// Rolled-back transaction: the row must not be visible.
	tx, err = db.Begin()
	if err != nil {
		t.Fatalf("Begin: %v", err)
	}
	tq = q.WithTx(tx)
	if _, err := tq.CreateFoo(ctx, "rolled-back"); err != nil {
		t.Fatalf("CreateFoo in tx: %v", err)
	}
	if err := tx.Rollback(); err != nil {
		t.Fatalf("Rollback: %v", err)
	}
	rows, err = q.ListFoos(ctx)
	if err != nil {
		t.Fatalf("ListFoos: %v", err)
	}
	if len(rows) != 1 || rows[0].Name == "rolled-back" {
		t.Fatalf("after rollback: %+v, want only the committed row", rows)
	}
}
