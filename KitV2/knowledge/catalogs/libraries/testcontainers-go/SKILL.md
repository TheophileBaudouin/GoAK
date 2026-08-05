---
name: testcontainers-go
description: "github.com/testcontainers/testcontainers-go v0.43.0 — Go integration-test containers with wait strategies, lifecycle cleanup, and Docker/Podman support. Use for real dependency integration tests; requires a container runtime and never belongs in production runtime code."
category: library
tags: [testing, integration, containers, docker, testcontainers]
last-verified: 2026-08-05
---

# testcontainers-go — dépendances réelles en test

## Selection

[`github.com/testcontainers/testcontainers-go`](https://github.com/testcontainers/testcontainers-go)
v0.43.0 is a Go integration-testing library that provisions real containers,
waits for readiness, and cleans them up. It is admitted for a test-only
infrastructure boundary, active maintenance, CI, documentation, and broad
module support; it is not a runtime dependency or a replacement for unit tests.

## Admission checklist

- [x] Current v0.43.0 and active upstream maintenance.
- [x] Single responsibility: container lifecycle for integration tests.
- [x] Docker/Podman provider, wait strategies, modules, and cleanup are explicit.
- [x] Tests, CI matrices, documentation, and examples exist.
- [x] Security fixes and credential handling are maintained upstream.

## Minimal use

```go
func startRedis(ctx context.Context) (testcontainers.Container, error) {
    container, err := testcontainers.Run(ctx, "redis:7-alpine")
    if err != nil {
        return nil, fmt.Errorf("start redis container: %w", err)
    }
    return container, nil
}
```

Call `TerminateContainer`/the current cleanup helper with a test cleanup hook,
pin image tags/digests, and verify readiness with a wait strategy before using a
service. Docker/Podman must be available when the test runs.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `ory/dockertest` | Consider only after a fresh maintenance review; testcontainers-go has the broader maintained module/wait ecosystem. |
| In-memory fake | Prefer for unit tests when a real dependency is not part of the behavior under test. |
| Docker CLI scripts | Avoid when typed lifecycle, wait, cleanup, and test ownership are required. |
| Testcontainers Cloud | Operational alternative when local Docker is unavailable, not a code replacement. |

## Utiliser cette librairie quand

- Integration tests must exercise a real PostgreSQL, Redis, Kafka, or other
  dependency with reproducible lifecycle control.
- The test environment provides Docker, Podman, or Testcontainers Cloud.
- Readiness, cleanup, image pinning, and failure diagnostics can be owned by CI.

## Ne pas utiliser cette librairie quand

- Unit tests can use a deterministic in-memory fake.
- The production binary would import container lifecycle code.
- CI cannot provide a container runtime or the test must run offline.
- An unpinned latest image would make the test result non-reproducible.

## Avantages

- Real dependency behavior without hand-written container lifecycle scripts.
- Typed wait strategies, modules, cleanup, and compose integration.
- Supports rootless/remote/container-cloud testing configurations.

## Inconvénients

- Slow, environment-dependent tests require Docker/Podman and image pulls.
- Ryuk cleanup uses a privileged helper container by default; review that trust
  boundary and configure it deliberately.
- Dependency and image versions form a larger supply-chain surface.
- A container passing readiness does not prove application-level correctness.

## Pièges connus

- Pin images by digest or explicit compatible tag; never use `latest` in a gate.
- Always register cleanup and set bounded startup/test contexts.
- Treat Docker credentials, socket access, Ryuk, and privileged containers as
  CI trust boundaries.
- Use wait strategies for application readiness, not merely container start.
- Keep integration tests tagged/isolated when a local runtime is unavailable;
  report `PARTIAL` rather than silently skipping them.

## Sources vérifiées

- [Official testcontainers-go repository](https://github.com/testcontainers/testcontainers-go)
  — API, maintenance, license, checked 2026-08-05.
- [v0.43.0 releases](https://github.com/testcontainers/testcontainers-go/releases)
  — current version and breaking changes, checked 2026-08-05.
- [testcontainers-go on pkg.go.dev](https://pkg.go.dev/github.com/testcontainers/testcontainers-go)
  — API and providers, checked 2026-08-05.
- [Configuration documentation](https://github.com/testcontainers/testcontainers-go/blob/main/docs/features/configuration.md)
  — Docker/Ryuk/runtime behavior, checked 2026-08-05.
- [Docker auth documentation](https://github.com/testcontainers/testcontainers-go/blob/main/docs/features/docker_auth.md)
  — credential boundary, checked 2026-08-05.
- [Docker Compose documentation](https://github.com/testcontainers/testcontainers-go/blob/main/docs/features/docker_compose.md)
  — compose/runtime constraints, checked 2026-08-05.
- [Credential leak fix PR #3721](https://github.com/testcontainers/testcontainers-go/pull/3721)
  — security remediation, checked 2026-08-05.
