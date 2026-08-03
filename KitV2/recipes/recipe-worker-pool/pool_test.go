package pool

import (
	"context"
	"errors"
	"sync/atomic"
	"testing"
	"time"
)

// TestRun_processesAll verifies every item is processed when all succeed.
func TestRun_processesAll(t *testing.T) {
	items := []int{1, 2, 3, 4, 5}
	var got int32

	err := Run(context.Background(), items, 2, func(_ context.Context, n int) error {
		atomic.AddInt32(&got, 1)
		return nil
	})

	if err != nil {
		t.Fatalf("expected nil error, got %v", err)
	}
	if got != int32(len(items)) {
		t.Fatalf("processed %d items, want %d", got, len(items))
	}
}

// TestRun_respectsLimit verifies at most `limit` goroutines run concurrently.
// Each worker holds a slot for long enough that, without bounding, the peak
// concurrency would exceed the limit.
func TestRun_respectsLimit(t *testing.T) {
	const limit = 3
	var current, max int32
	items := make([]int, 20)
	for i := range items {
		items[i] = i
	}

	_ = Run(context.Background(), items, limit, func(_ context.Context, _ int) error {
		c := atomic.AddInt32(&current, 1)
		// Track the high-water mark of concurrent goroutines.
		for {
			m := atomic.LoadInt32(&max)
			if c <= m || atomic.CompareAndSwapInt32(&max, m, c) {
				break
			}
		}
		time.Sleep(5 * time.Millisecond) // hold the slot
		atomic.AddInt32(&current, -1)
		return nil
	})

	if max > limit {
		t.Fatalf("peak concurrency %d exceeded limit %d", max, limit)
	}
}

// TestRun_firstErrorCancels verifies Run returns the first error and that
// group cancellation aborts the remaining work.
//
// The error-triggering worker returns the sentinel with no delay so the group
// is cancelled immediately; the others observe ctx.Done() and abort returning
// nil (NOT ctx.Err()) so the sentinel is the sole non-nil error — no race over
// which error errgroup records first.
func TestRun_firstErrorCancels(t *testing.T) {
	sentinel := errors.New("boom")
	var completed int32
	items := make([]int, 100)
	for i := range items {
		items[i] = i
	}

	err := Run(context.Background(), items, 4, func(ctx context.Context, n int) error {
		if n == 5 {
			return sentinel // cancels the group context immediately
		}
		select {
		case <-ctx.Done():
			return nil // cancelled before doing real work — no error (sentinel already wins)
		case <-time.After(20 * time.Millisecond):
			atomic.AddInt32(&completed, 1)
			return nil
		}
	})

	if !errors.Is(err, sentinel) {
		t.Fatalf("expected sentinel error, got %v", err)
	}
	// Cancellation should have prevented most of the 99 non-error items.
	if completed > 10 {
		t.Fatalf("expected cancellation to abort work, but %d/99 completed", completed)
	}
}
