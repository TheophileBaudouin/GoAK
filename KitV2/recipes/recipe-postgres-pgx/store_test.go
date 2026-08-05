package postgrespgx

import (
	"context"
	"errors"
	"testing"
)

func TestOpenRequiresURL(t *testing.T) {
	t.Parallel()
	if _, err := Open(context.Background(), " "); err == nil {
		t.Fatal("Open accepted an empty database URL")
	}
}

func TestOpenReturnsPingErrorForCanceledContext(t *testing.T) {
	t.Parallel()
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	_, err := Open(ctx, "postgres://localhost:5432/kit")
	if err == nil {
		t.Fatal("Open succeeded with a canceled context")
	}
	if !errors.Is(err, context.Canceled) {
		t.Fatalf("Open error = %v, want context.Canceled", err)
	}
}

func TestStoreValidatesBeforeQuery(t *testing.T) {
	t.Parallel()
	store := &Store{}
	if _, err := store.CreateWidget(context.Background(), " "); err == nil {
		t.Fatal("CreateWidget accepted an empty name")
	}
	if _, err := store.CreateWidget(context.Background(), "widget"); err == nil {
		t.Fatal("CreateWidget accepted a closed store")
	}
	if _, err := store.Widget(context.Background(), 0); err == nil {
		t.Fatal("Widget accepted a non-positive ID")
	}
	if _, err := store.Widget(context.Background(), 1); err == nil {
		t.Fatal("Widget accepted a closed store")
	}
}
