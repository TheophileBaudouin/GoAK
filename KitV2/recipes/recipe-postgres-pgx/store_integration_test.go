//go:build postgres

package postgrespgx

import (
	"context"
	"errors"
	"os"
	"os/exec"
	"path/filepath"
	"testing"

	"github.com/jackc/pgx/v5"
)

func TestPostgreSQLMigrationAndStore(t *testing.T) {
	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		t.Fatal("DATABASE_URL is required for the PostgreSQL integration scenario")
	}
	migrate, err := exec.LookPath("migrate")
	if err != nil {
		t.Fatal("golang-migrate CLI is required; install github.com/golang-migrate/migrate/v4/cmd/migrate@v4.19.1")
	}
	migrations, err := filepath.Abs("migrations")
	if err != nil {
		t.Fatalf("resolve migrations path: %v", err)
	}
	runMigrate(t, migrate, migrations, databaseURL, "up")
	t.Cleanup(func() { runMigrate(t, migrate, migrations, databaseURL, "down", "-all") })

	ctx := context.Background()
	store, err := Open(ctx, databaseURL)
	if err != nil {
		t.Fatalf("Open: %v", err)
	}
	t.Cleanup(store.Close)

	created, err := store.CreateWidget(ctx, "integration-widget")
	if err != nil {
		t.Fatalf("CreateWidget: %v", err)
	}
	loaded, err := store.Widget(ctx, created.ID)
	if err != nil {
		t.Fatalf("Widget: %v", err)
	}
	if loaded != created {
		t.Fatalf("loaded widget = %#v, want %#v", loaded, created)
	}
	if _, err := store.Widget(ctx, created.ID+1_000_000); !errors.Is(err, pgx.ErrNoRows) {
		t.Fatalf("missing widget error = %v, want pgx.ErrNoRows", err)
	}
}

func runMigrate(t *testing.T, migrate, path, databaseURL string, args ...string) {
	t.Helper()
	commandArgs := []string{"-path", path, "-database", databaseURL}
	commandArgs = append(commandArgs, args...)
	if output, err := exec.Command(migrate, commandArgs...).CombinedOutput(); err != nil { // #nosec G204 -- binary and arguments are controlled by the test environment.
		t.Fatalf("migrate %s failed: %v (%s)", args[0], err, output)
	}
}
