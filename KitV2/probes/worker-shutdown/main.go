package main

import (
	"context"
	"errors"
	"fmt"
	"net"
	"net/http"
	"os"
	"time"

	shutdown "go-agent-kit-v2/recipes/recipe-graceful-shutdown"
	pool "go-agent-kit-v2/recipes/recipe-worker-pool"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	if err := pool.Run(ctx, []int{1, 2, 3}, 2, func(context.Context, int) error { return nil }); err != nil {
		fail(err)
	}

	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		fail(err)
	}
	server := &http.Server{
		Handler:           http.HandlerFunc(func(http.ResponseWriter, *http.Request) {}),
		ReadHeaderTimeout: time.Second,
	}
	shutdownCtx, shutdownCancel := context.WithCancel(context.Background())
	result := make(chan error, 1)
	go func() { result <- shutdown.Run(shutdownCtx, server, listener, time.Second) }()
	shutdownCancel()
	if err := <-result; err != nil && !errors.Is(err, http.ErrServerClosed) {
		fail(err)
	}
	fmt.Println("worker-shutdown: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
