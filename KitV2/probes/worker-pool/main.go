package main

import (
	"context"
	"errors"
	"fmt"
	"os"

	pool "go-agent-kit-v2/recipes/recipe-worker-pool"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// 1. Success case
	var processed int
	err := pool.Run(ctx, []int{10, 20, 30}, 2, func(_ context.Context, item int) error {
		processed++
		return nil
	})
	if err != nil || processed != 3 {
		fail(fmt.Errorf("worker-pool success run failed: err=%v processed=%d", err, processed))
	}

	// 2. Cancellation case
	sentinel := errors.New("worker-error")
	err = pool.Run(ctx, []int{1, 2, 3, 4, 5}, 2, func(_ context.Context, item int) error {
		if item == 3 {
			return sentinel
		}
		return nil
	})
	if !errors.Is(err, sentinel) {
		fail(fmt.Errorf("worker-pool cancellation run failed: err=%v, want %v", err, sentinel))
	}

	fmt.Println("worker-pool: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
