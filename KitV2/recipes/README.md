# Recipes

Recipes are ordered, runnable procedures for a repeatable Go task. Each recipe
has a `SKILL.md`, focused Go code, tests, an observable scenario, limits, and
primary sources. The canonical recipe contract is summarized in `AGENTS.md`.

## Roadmap

Planned recipes remain absent until their evidence, implementation, tests, and
observable scenario are ready. Empty directories are not placeholders.

| Recipe shape | Admission criterion |
| --- | --- |
| `add-authentication` | A sourced authentication boundary with explicit session/token, CSRF, and failure behavior. |
| `add-database` | A runnable database boundary with migration, error, cleanup, and observable persistence checks. |
| `add-observability` | A minimal observability boundary with injected dependencies and a local verification scenario. |
| `create-grpc-service` | A focused, validated gRPC procedure with generated-code and transport constraints documented. |
| `create-rest-api` | A REST procedure whose central request/response behavior is exercised by a probe. |
| `deploy-container` | A deterministic container workflow with reproducible build and local acceptance evidence. |
