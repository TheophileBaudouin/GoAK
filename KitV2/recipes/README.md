---
name: recipes
description: Index of the runnable Go recipes shipped with this kit (procedures, tests, observable scenarios, limits, roadmap). Read it to browse recipes; each recipe loads on demand from its own SKILL.md.
disable-model-invocation: true
---

# Recipes

Recipes are ordered, runnable procedures for a repeatable Go task. Each recipe
has a `SKILL.md`, focused Go code, tests, an observable scenario, limits, and
primary sources. The canonical recipe contract is summarized in `AGENTS.md`.

## Roadmap

Planned recipes remain absent until their evidence, implementation, tests, and
observable scenario are ready. Empty directories are not placeholders.

| Recipe shape | Admission criterion |
| --- | --- |
| `create-grpc-service` | A focused, validated gRPC procedure with generated-code and transport constraints documented. |
| `create-rest-api` | A REST procedure whose central request/response behavior is exercised by a probe. |
| `deploy-container` | A deterministic container workflow with reproducible build and local acceptance evidence. |
| `testcontainers-integration` | Explicit authorization for Docker/Podman, an approved runtime, and a real successful container scenario before activation; no simulated substitute. |
