// Package shutdown shows a minimal, TESTABLE graceful-shutdown orchestration
// for an *http.Server using only the standard library.
//
// Testability hinge: the signal wiring (signal.NotifyContext, which catches
// SIGINT/SIGTERM) is kept OUT of this package — the caller passes a
// context.Context. Run waits on that context, then calls http.Server.Shutdown
// with a timeout so in-flight requests drain. Tests cancel the context manually
// instead of sending real OS signals.
package shutdown

import (
	"context"
	"errors"
	"net"
	"net/http"
	"time"
)

// Run serves srv on ln until ctx is cancelled, then shuts srv down gracefully:
// it stops accepting new connections and waits up to timeout for in-flight
// handlers to finish.
//
// Signal wiring belongs to the CALLER (see the example in SKILL.md):
//
//	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
//	defer stop()
//	if err := shutdown.Run(ctx, srv, ln, 5*time.Second); err != nil { log.Fatal(err) }
//
// Run returns nil on a clean drain, a non-nil error if the server failed to
// serve (e.g. listener closed), or the Shutdown error if draining exceeded the
// timeout. http.ErrServerClosed (the expected return from Serve during shutdown)
// is absorbed, not surfaced.
func Run(ctx context.Context, srv *http.Server, ln net.Listener, timeout time.Duration) error {
	serveErr := make(chan error, 1)
	go func() {
		err := srv.Serve(ln)
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			serveErr <- err
			return
		}
		serveErr <- nil
	}()

	select {
	case err := <-serveErr:
		// Server failed to serve before shutdown was requested.
		return err
	case <-ctx.Done():
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	return srv.Shutdown(shutdownCtx)
}
