package snippet

import (
	"context"
	"errors"
	"testing"
)

func TestRunBoundedProcessesEveryJob(t *testing.T) {
	jobs := []func(context.Context) error{
		func(context.Context) error { return nil },
		func(context.Context) error { return nil },
		func(context.Context) error { return nil },
	}

	if err := RunBounded(context.Background(), jobs); err != nil {
		t.Fatalf("RunBounded() error = %v", err)
	}
}

func TestRunBoundedReturnsJobError(t *testing.T) {
	want := errors.New("stop")
	jobs := []func(context.Context) error{
		func(context.Context) error { return want },
	}

	if err := RunBounded(context.Background(), jobs); !errors.Is(err, want) {
		t.Fatalf("RunBounded() error = %v, want %v", err, want)
	}
}
