package shutdown

import (
	"context"
	"io"
	"net"
	"net/http"
	"testing"
	"time"
)

// TestRun_drainsInFlightRequest proves graceful shutdown: a request that is
// already in flight when shutdown is triggered still completes, and Run returns
// nil. The context is cancelled manually (no real OS signal), which is exactly
// why Run takes a context rather than doing its own signal handling.
func TestRun_drainsInFlightRequest(t *testing.T) {
	started := make(chan struct{})
	release := make(chan struct{})

	srv := &http.Server{Handler: http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		close(started) // tell the test the handler is in-flight
		<-release      // block until the test lets us finish
		w.WriteHeader(http.StatusOK)
	})}

	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("net.Listen: %v", err)
	}
	addr := "http://" + ln.Addr().String()

	ctx, cancel := context.WithCancel(context.Background())
	t.Cleanup(cancel)

	runDone := make(chan error, 1)
	go func() { runDone <- Run(ctx, srv, ln, 2*time.Second) }()

	// Fire a request; it will block in the handler until released.
	go func() {
		resp, err := http.Get(addr)
		if err != nil {
			return
		}
		_, _ = io.Copy(io.Discard, resp.Body)
		_ = resp.Body.Close()
	}()

	select {
	case <-started:
	case <-time.After(time.Second):
		t.Fatal("handler never started; request did not reach the server")
	}

	// Handler is now in-flight → request graceful shutdown.
	cancel()

	// Release the in-flight handler so Shutdown's drain can complete.
	close(release)

	select {
	case err := <-runDone:
		if err != nil {
			t.Fatalf("Run returned %v, want nil", err)
		}
	case <-time.After(3 * time.Second):
		t.Fatal("Run did not return; shutdown hung")
	}
}

// TestRun_serveError verifies that if the server cannot serve (here: a listener
// already closed), Run surfaces that error instead of blocking forever.
func TestRun_serveError(t *testing.T) {
	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("net.Listen: %v", err)
	}
	_ = ln.Close() // Serve will return "use of closed network connection" immediately.

	srv := &http.Server{}
	err = Run(context.Background(), srv, ln, time.Second)
	if err == nil {
		t.Fatal("expected a serve error for a closed listener, got nil")
	}
}

// TestRun_shutdownTimeout verifies that if in-flight requests exceed the drain
// timeout, Run surfaces context.DeadlineExceeded error from Shutdown.
func TestRun_shutdownTimeout(t *testing.T) {
	block := make(chan struct{})
	srv := &http.Server{Handler: http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		<-block // never releases during the short timeout
	})}

	ln, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatalf("net.Listen: %v", err)
	}
	addr := "http://" + ln.Addr().String()

	ctx, cancel := context.WithCancel(context.Background())
	t.Cleanup(func() {
		cancel()
		close(block)
	})

	runDone := make(chan error, 1)
	go func() { runDone <- Run(ctx, srv, ln, 50*time.Millisecond) }()

	// Send a request to block the handler
	go func() {
		resp, _ := http.Get(addr)
		if resp != nil {
			_ = resp.Body.Close()
		}
	}()

	// Give request time to hit handler
	time.Sleep(20 * time.Millisecond)

	// Trigger shutdown
	cancel()

	select {
	case err := <-runDone:
		if err == nil {
			t.Fatal("expected timeout error, got nil")
		}
	case <-time.After(2 * time.Second):
		t.Fatal("Run timed out without returning error")
	}
}
