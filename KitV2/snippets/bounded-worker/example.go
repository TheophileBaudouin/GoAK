package snippet

import (
	"context"

	"golang.org/x/sync/errgroup"
)

// RunBounded executes jobs with a fixed concurrency limit.
func RunBounded(ctx context.Context, jobs []func(context.Context) error) error {
	group, groupCtx := errgroup.WithContext(ctx)
	group.SetLimit(4)
	for _, job := range jobs {
		group.Go(func() error { return job(groupCtx) })
	}
	return group.Wait()
}
