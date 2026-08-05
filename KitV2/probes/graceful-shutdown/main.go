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
)

func main() {
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		fail(err)
	}

	server := &http.Server{
		Handler:           http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {}),
		ReadHeaderTimeout: time.Second,
	}

	shutdownCtx, cancel := context.WithCancel(context.Background())
	result := make(chan error, 1)

	go func() {
		result <- shutdown.Run(shutdownCtx, server, listener, time.Second)
	}()

	// Trigger graceful shutdown
	cancel()

	if err := <-result; err != nil && !errors.Is(err, http.ErrServerClosed) {
		fail(fmt.Errorf("graceful shutdown failed: %w", err))
	}

	fmt.Println("graceful-shutdown: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
