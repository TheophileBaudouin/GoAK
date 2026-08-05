// Package pool shows a minimal bounded worker pool using errgroup.
//
// errgroup.WithContext returns a Group whose context is cancelled the moment
// any goroutine returns a non-nil error, so first-error-cancel is built in.
// g.SetLimit caps the number of concurrently running goroutines.
//
// This replaces the hand-rolled channel-semaphore + WaitGroup + error-collector
// pattern (~25 lines, easy to get wrong) with ~5 lines of proven code.
package pool

import (
	"context"
	"errors"

	"golang.org/x/sync/errgroup"
)

var (
	// ErrInvalidLimit reports a non-positive concurrency limit.
	ErrInvalidLimit = errors.New("worker-pool: limit must be positive")
	// ErrNilWorker reports a missing unit-of-work function.
	ErrNilWorker = errors.New("worker-pool: worker function must not be nil")
	// ErrNilContext reports an invalid nil context.
	ErrNilContext = errors.New("worker-pool: context must not be nil")
)

// Run processes items with at most limit goroutines in flight at once. The
// provided ctx is honoured: if it (or any worker's error) cancels the group,
// remaining queued workers are not started. Run returns the first non-nil
// error from fn, or nil if all succeeded.
//
// Note: since Go 1.22 the loop variable is fresh per iteration, so the old
// `item := item` capture trick is no longer needed.
func Run[T any](ctx context.Context, items []T, limit int, fn func(ctx context.Context, item T) error) error {
	if ctx == nil {
		return ErrNilContext
	}
	if limit < 1 {
		return ErrInvalidLimit
	}
	if fn == nil {
		return ErrNilWorker
	}
	if err := ctx.Err(); err != nil {
		return err
	}
	g, workerCtx := errgroup.WithContext(ctx)
	g.SetLimit(limit)
	for _, item := range items {
		if workerCtx.Err() != nil {
			break
		}
		g.Go(func() error {
			if err := workerCtx.Err(); err != nil {
				return nil
			}
			return fn(workerCtx, item)
		})
	}
	return g.Wait() // pi-lens-ignore: go-bare-error
}
