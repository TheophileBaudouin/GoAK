---
name: ardanlabs-service
description: "ardanlabs/service — Go service starter (DDD/data-oriented, ~4.1k★). EXTRACT-ONLY: extract layer separation (business/app/foundation) + observability wiring; NEVER copy its Kubernetes-first architecture or integrated RBAC."
category: reference-project
tags: [service, ddd, observability, extract-only, kubernetes]
last-verified: 2026-08-02
---

# ardanlabs-service (extract-only)

> **extract-only: true** — the kit is NOT a starter. Extract patterns; never clone
> the tree or adopt its imposed architecture.

## The project

`ardanlabs/service` (4.1k★, last verified commit 2026-06). It self-describes as a starter kit
for writing services in Go on Kubernetes, using a Domain-Driven / Data-Oriented
design.

## What you MAY extract

- **Layer separation**: `business/` (domain logic), `app/` (composition /
  transport), `foundation/` (cross-cutting: logging, shutdown, web errors). This
  three-layer split is a sound mental model for any non-trivial service.
- **Observability wiring**: how logging/tracing/metrics are centralised in
  `foundation/` and threaded via context, not scattered through handlers.
- **Graceful shutdown + readiness**: the pattern of coordinating server + workers
  - probes on a single context (compare `recipe-graceful-shutdown`).

## What you must NEVER copy

- **The Kubernetes-first assumption** — readiness/liveness probes, RBAC, and
  cluster-oriented defaults are NOT universal. A CLI tool or a desktop app does
  not have them.
- **Integrated RBAC / cluster auth** — imposes a security model on consumers who
  may use a completely different one.
- **The full tree / build pipeline** — it is a starter; cloning it turns the kit
  into exactly the starter-kit the Prime Directive forbids.

## How an agent should use this

Read it to internalise the layer split and observability threading, then express
those as the kit's own patterns in `rules/` (when the universal rules are authored), instantiated
MINIMALLY for the consumer's actual project type. Do not reproduce the K8s shape.

## Verification

- 4.1k★ (≥500 floor ✓), last verified commit 2026-06 (<12mo ✓), not archived.
- Open issues: 1 — no recurring-issue mass to log as a Gotcha.
