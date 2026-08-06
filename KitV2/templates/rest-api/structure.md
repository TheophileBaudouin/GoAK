# REST API — reading map

This map explains how to navigate this project. The **Tree facts** section
below is machine-checked by the kit's drift gate (it cannot drift silently);
the role lines, reading path, and boundary explanations are human-reviewed
content and are not machine-verifiable by design.

## Tree facts (machine-checked; do not edit)

```text
top_dirs: .github; api; cmd; internal; pkg
packages: cmd/api-service -> main; internal/passport -> passport; internal/passport/models -> models; pkg/health -> health; pkg/status -> status; pkg/version -> version
entry_points: cmd/api-service
test_files: internal/passport/db_passport_test.go; internal/passport/db_user_test.go; internal/passport/handlers_test.go; internal/passport/middleware_test.go; internal/passport/server_test.go; pkg/version/parser_test.go
internal_boundary: present
```

## Directory roles

- `cmd/` — the runnable service: `cmd/api-service` wires configuration,
  middleware, routes, and the HTTP server lifecycle.
- `internal/` — the private application: the passport/user domain, handlers,
  and middleware no external module may import.
- `pkg/` — small reusable helpers (health, status, version endpoints) that are
  safe to publish outside the application.
- `api/` — the API contract: the OpenAPI document describing the service.
- `.github/` and other dot-dirs — development tooling; not part of the
  application's reading path.

## Reading path

Send a request to a protected endpoint, for example `POST /api/v1/passports`.
The server starts in `cmd/api-service` (configuration, rate limiting,
middleware stack); the request reaches a handler in `internal/passport/`,
which validates the body, applies the domain rules in `internal/passport/models`,
and stores the result through the repository boundary. Error responses and
status codes follow `api/openapi.yaml`. Health and version probes come from
`pkg/health`, `pkg/status`, and `pkg/version`.

## Public vs internal boundary

`internal/` is private implementation — the Go compiler prevents external
imports, so the passport domain, handlers, and middleware can evolve freely.
`pkg/` is the public helper surface (health/status/version endpoints). The
entry point is `cmd/api-service`; everything a client sees is the HTTP API
described in `api/openapi.yaml`.

## Where the evidence lives

The service behavior is proven by tests under `internal/passport/`
(`handlers_test.go`, `middleware_test.go`, `db_passport_test.go`,
`db_user_test.go`, `server_test.go`) and `pkg/version/parser_test.go`. Run
them with `go test -race ./...`; a smoke scenario starts the server
in-process and checks the status and body of real requests.
