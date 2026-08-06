---
name: pagoda
description: "mikestefanello/pagoda v0.27.0 — Go full-stack SSR starter using Echo, Ent, Gomponents, HTMX, and SQLite. EXTRACT-ONLY: borrow routes/services/templates layering; never copy its stack, admin panel, or deployment assumptions."
category: reference-project
tags: [ssr, web, starter, extract-only, echo, ent]
last-verified: 2026-08-05
---

# pagoda (extract-only)

> **extract-only: true** — Pagoda is a template/starter, not a library or the
> default architecture for every Go web project.

## The project

[`mikestefanello/pagoda`](https://github.com/mikestefanello/pagoda) v0.27.0 is a
full-stack SSR starter with Echo, Ent, Gomponents, HTMX/Alpine/DaisyUI, and
SQLite defaults. It includes a service container and a beta admin panel. The
repository is consumed by cloning/forking, not importing as a reusable kit
module.

## What you MAY extract

- The routes → services → templates request shape.
- Page/layout/partial composition and a service-container composition boundary.
- The conceptual placement of session/auth wiring, after choosing an
  independently vetted implementation.
- Task/admin concerns only when the consumer actually needs them and accepts
  their beta/product scope.

## What you must NEVER copy

- Echo, Ent, HTMX, Alpine, DaisyUI, or SQLite as an imposed stack.
- The admin-panel surface or its beta assumptions as a universal feature.
- The full scaffold, generated Ent code, or deployment defaults.
- A library choice from Pagoda without evaluating that component independently
  against the kit's admission rules.

## How an agent should use this

Read it for one SSR layering question, then re-express the shape with the
consumer's approved router, templates, database, and auth choices. Prefer the
kit's own recipes for implementation and validation. Do not clone the complete
project when only one structural idea is required.

## Verification

- Current tagged release verified: v0.27.0, published 2025-08-04.
- Recent release history includes v0.26.0 and v0.25.0; current activity must be
  rechecked before relying on it as a maintained base.
- MIT template; Go 1.24-era metadata; admin panel explicitly beta.

## Verified sources
- [Official Pagoda repository](https://github.com/mikestefanello/pagoda) — stack,
  template identity, and architecture, checked 2026-08-05.
- [Pagoda releases](https://github.com/mikestefanello/pagoda/releases) — current
  v0.27.0 and release history, checked 2026-08-05.
- [Pagoda issues](https://github.com/mikestefanello/pagoda/issues) — current
  maintenance/limits, checked 2026-08-05.
- [Pagoda package metadata](https://pkg.go.dev/github.com/mikestefanello/pagoda)
  — module/Go metadata, checked 2026-08-05.
- [Pagoda README](https://github.com/mikestefanello/pagoda/blob/main/README.md)
  — template workflow and service stack, checked 2026-08-05.
