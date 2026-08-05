package snippet

import (
	"errors"
	"testing"
)

func TestWrapBoundary(t *testing.T) {
	if WrapBoundary(nil) != nil {
		t.Fatal("WrapBoundary(nil) must return nil")
	}

	want := errors.New("not found")
	got := WrapBoundary(want)
	if !errors.Is(got, want) {
		t.Fatalf("WrapBoundary() = %v, want wrapped %v", got, want)
	}
}
