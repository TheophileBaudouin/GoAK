# Go REST API template

Status: **sourced**.

This directory is a minimally adapted copy of
[`leeprovoost/go-rest-api-template`](https://github.com/leeprovoost/go-rest-api-template),
pinned to commit `4f2d17f700be3b355ff88986ca37c70ad2145cef`. Read
[`ATTRIBUTION.md`](ATTRIBUTION.md) before adapting it; the upstream MIT license
is retained in [`LICENSE`](LICENSE).

## What it provides

A standard-library-first HTTP REST service using `net/http`, `log/slog`, JSON,
small `http.Handler` middleware, an OpenAPI document, in-memory passport/user
services, health/status endpoints, rate limiting, tests, Docker packaging, and
CI. It is a foundation, not a complete product: replace the in-memory stores
and example passport domain before shipping.

## Adopt it

From a copy of this directory:

1. Change the module path in `go.mod` and all imports from
   `github.com/leeprovoost/go-rest-api-template` to your module path.
2. Replace `internal/passport/` with the application's domain and persistence
   boundary; keep handlers thin and preserve the test seams.
3. Update `api/openapi.yaml`, `cmd/api-service/VERSION`, and environment
   configuration for the service.
4. Run `go mod tidy`, then the checks below.

## Verify

```sh
go test -race ./...
go vet ./...
go run ./cmd/api-service
```

The observable smoke scenario is:

```sh
VERSION=./cmd/api-service/VERSION PORT=8080 ENV=LOCAL go run ./cmd/api-service
curl -i http://localhost:8080/healthcheck
curl -i http://localhost:8080/ready
```

The exact route names remain defined by `internal/passport/routes.go` and the
upstream OpenAPI document. Do not add authentication, a database, a cloud SDK,
or an observability backend without making that a separate, explicit design
choice.
