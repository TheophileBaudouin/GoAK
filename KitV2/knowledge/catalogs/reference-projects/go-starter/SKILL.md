---
name: go-starter
description: "allaboutapps/go-starter tag go-starter-2025-10-16 (25.10.0) — opinionated Go/Docker/PostgreSQL template. EXTRACT-ONLY and effectively stagnant: use only for layout inspiration, never as a maintained dependency or current default."
category: reference-project
tags: [starter, docker, postgres, extract-only, stale]
last-verified: 2026-08-05
---

# go-starter (extract-only, stagnant)

> **extract-only: true** — this GitHub template is not an importable library and
> its current maintenance status limits how much trust an agent should place in
> it.

## The project

[`allaboutapps/go-starter`](https://github.com/allaboutapps/go-starter) is an
opinionated Go REST service template around Docker, PostgreSQL, SQLBoiler,
Swagger, and development containers. It is consumed as a GitHub template/fork,
not as a Go module dependency.

## Verification outcome

- Latest known tag/release convention: `go-starter-2025-10-16` / `25.10.0`.
- Last code commit verified: 2025-10-16.
- Open queue verified as dependency-bump work that has remained unresolved.
- The repository is not archived, but absence of code activity since the last
  release makes it a stale reference rather than an actively maintained base.

## What you MAY extract

- Relative placement ideas for config, migrations, handlers, Docker wiring, and
  generated SQL code.
- A deployment concern to compare against the consumer's actual requirements.

## What you must NEVER copy

- The Docker/PostgreSQL/SQLBoiler/Swagger stack as a bundle.
- Generated boilerplate, CI assumptions, or a generator as if it were a kit
  contract.
- A dependency/version choice from this repository without fresh independent
  verification.

## How an agent should use this

Use it only to inspect one layout question. Prefer the kit's tested recipes and
current library catalogs for implementation choices. If a proposed design
relies on this template's current behavior, stop and re-verify the specific
source or reject the reference.

## Sources vérifiées

- [Official go-starter repository](https://github.com/allaboutapps/go-starter) —
  template identity, license, and stack, checked 2026-08-05.
- [Repository API metadata](https://github.com/allaboutapps/go-starter)
  — activity/status, checked 2026-08-05.
- [Commit history](https://github.com/allaboutapps/go-starter/commits/master)
  — last code commit, checked 2026-08-05.
- [Open issues](https://github.com/allaboutapps/go-starter/issues)
  — maintenance signal, checked 2026-08-05.
- [Changelog](https://raw.githubusercontent.com/allaboutapps/go-starter/master/CHANGELOG-go-starter.md)
  — release/tag convention, checked 2026-08-05.
