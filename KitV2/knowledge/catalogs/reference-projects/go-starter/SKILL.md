---
name: go-starter
description: "allaboutapps/go-starter — Go + Docker + Postgres scaffolding starter (621★). EXTRACT-ONLY and STAGNANT (issue-mined: 6 open automated/dependabot issues; no recent human-maintenance signal after 2025-05; last push 2025-10): layout inspiration only, do not rely on it. Candidate for removal at next review."
category: reference-project
tags: [starter, docker, postgres, extract-only]
last-verified: 2026-08-02
---

# go-starter (extract-only)

> **extract-only: true** — and flagged for maintenance recency.

## The project

`allaboutapps/go-starter` (621★, **last push 2025-10-16** — ~9 months ago, inside
the <12mo window but at its edge; not archived). A scaffolding starter for Go +
Docker + Postgres services.

## Verification outcome (the "verify-first" candidate)

This was the candidate requiring reinforced verification. Result:

- **Stars**: 621 — clears the ≥500 floor (narrowly).
- **Activity**: last push 2025-10-16 — clears the <12mo rule today, but it is the
  closest to the edge of all candidates. Re-verify at the next `last-verified`
  cycle; if it crosses 12 months, demote/reject.
- **CI/tests**: the repo's main README redirects to a generated project README,
  signalling a scaffold generator more than a maintained library — treat with
  caution.

## What you MAY extract

- **Project skeleton idea**: where config, migrations, handlers, and Docker
  wiring sit relative to each other — as a layout reference, not a copy.
- **Migration tooling placement** (adjacent to the DB layer).

## What you must NEVER copy

- **The scaffold itself** (Dockerfile chain, Postgres bootstrapping, generator
  scripts) — these encode one deployment opinion; the kit stays deployment-agnostic.
- **Generated boilerplate** — the kit generates nothing; consumers' needs differ.

## How an agent should use this

Glance at it for layout inspiration only. Prefer the kit's own recipes
(`recipe-rest-chi`, `recipe-sqlite-sqlc`) which give tested, minimal patterns
without imposing Docker/Postgres or a generator.

## Verification

- 621★ (≥500 ✓, narrow). Last push 2025-10-16 (inside <12mo but the only recent
  activity). **Issue-mined: 6 open automated/dependabot issues; no recent human-maintenance signal after 2025-05**
  (#269 was the last human-initiated issue), nothing since → effectively
  stagnant, not just borderline. Treat as
  reference-only; candidate for removal at the next `last-verified` cycle if
  still inactive.
