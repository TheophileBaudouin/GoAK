# Attribution

## Source

- Repository: <https://github.com/leeprovoost/go-rest-api-template>
- Pinned commit: `4f2d17f700be3b355ff88986ca37c70ad2145cef`
- License: MIT; the complete upstream `LICENSE` file is retained unchanged.
- Verified: 2026-08-05

## Technical scope

This is a single-purpose Go HTTP REST service foundation. It uses the Go
standard library for routing, JSON, middleware, structured logging, and HTTP
server lifecycle, with only `golang.org/x/time/rate` for per-IP rate limiting
and `stretchr/testify` for tests. It does not include an ORM, authentication
framework, message broker, cloud SDK, Kubernetes deployment, or telemetry
backend. The source is 18 Go files and 1,877 Go lines at the pinned commit;
there is no vendored or generated source tree.

## Adaptations

- Added this attribution file, `template.yaml`, and the Kit catalog metadata.
- Kept the upstream source tree, tests, CI configuration, and OpenAPI document;
  the Dockerfile gains a non-root runtime user for container hardening.
- Replaced the upstream golangci-lint configuration with the Kit's v2 opt-in
  configuration and exported-documentation rule.
- The JSON response helper now returns after an encoding failure, and the
  in-memory service receives the precise lint suppression required for its
  established domain name.
- Replaced the upstream README with a Kit adaptation that explains adoption,
  boundaries, and the executed smoke scenario.
- The upstream module path remains in `go.mod` so the copied tree can be
  validated without rewriting source imports. When adopting it, replace the
  module path and run `go mod tidy`.

No application behavior was authored for the Kit.
