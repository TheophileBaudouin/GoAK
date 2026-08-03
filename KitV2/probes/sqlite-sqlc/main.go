package main

import (
	"context"
	"fmt"
	"os"

	sqlcsqlite "go-agent-kit-v2/recipes/recipe-sqlite-sqlc"
)

func main() {
	db, err := sqlcsqlite.Open(":memory:")
	if err != nil {
		fail(err)
	}
	defer func() { _ = db.Close() }()

	queries := sqlcsqlite.New(db)
	id, err := queries.CreateFoo(context.Background(), "probe")
	if err != nil {
		fail(err)
	}
	foo, err := queries.GetFoo(context.Background(), id)
	if err != nil {
		fail(err)
	}
	if foo.ID != id || foo.Name != "probe" {
		fail(fmt.Errorf("unexpected row: %+v", foo))
	}
	fmt.Println("sqlite-sqlc: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
