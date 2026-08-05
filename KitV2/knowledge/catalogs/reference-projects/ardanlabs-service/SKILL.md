---
name: ardanlabs-service
description: "ardanlabs/service at commit 75942ce (2026-06-22) — Go service starter using business/app/foundation layering. EXTRACT-ONLY: borrow layer and observability shapes; never clone its Kubernetes/RBAC/deployment assumptions."
category: reference-project
tags: [service, ddd, observability, extract-only, kubernetes]
last-verified: 2026-08-05
---

# ardanlabs-service (extract-only)

> **extract-only: true** — this is a starter/template reference, not a Go
> dependency or a universal architecture.

## The project

[`ardanlabs/service`](https://github.com/ardanlabs/service) is a maintained Go
service starter using Domain-Driven/Data-Oriented ideas and a
business/app/foundation separation. The documented workflow uses `gonew` to
fork a project; it is not an importable library.

## What you MAY extract

- `business/` for domain logic and strong domain types.
- `app/` for composition and transport edges.
- `foundation/` for cross-cutting logging, shutdown, web errors, and
  observability wiring.
- Conversion boundaries between API primitives, business types, and database
  models.
- Coordinated server/worker shutdown and readiness concepts when the consumer
  actually has those processes.

## What you must NEVER copy

- Kubernetes-first readiness, RBAC, cluster authentication, or deployment
  assumptions into a CLI, desktop app, or small service.
- The full tree, vendor/build pipeline, or course-specific conventions without
  evaluating the consumer's actual requirements.
- Its architecture as a universal Go standard; it is one maintained reference
  shape.

## How an agent should use this

Read the relevant layer or conversion example, compare it with the consumer's
service shape, and re-express only the justified boundary using the kit's own
rules/recipes. Prefer the smallest number of layers that preserves the required
behavior. Do not clone the repository wholesale.

## Verification

- Latest verified commit: `75942ce8de8c8ba012e55507fb9c4f0c5912086f`, pushed
  2026-06-22.
- Starter/template workflow and project structure verified in the official
  README/wiki; Apache-2.0; not an imported library.
- Treat Go/toolchain and deployment choices as versioned source facts, not as
  universal kit defaults.

## Sources vérifiées

- [Official ardanlabs/service repository](https://github.com/ardanlabs/service) —
  project identity and README, checked 2026-08-05.
- [Repository activity](https://github.com/ardanlabs/service/activity) —
  verified commit/activity, checked 2026-08-05.
- [Package metadata](https://pkg.go.dev/github.com/ardanlabs/service) — module,
  license, and Go metadata, checked 2026-08-05.
- [Project structure wiki](https://github.com/ardanlabs/service/wiki/Project-Structure)
  — layer responsibilities, checked 2026-08-05.
