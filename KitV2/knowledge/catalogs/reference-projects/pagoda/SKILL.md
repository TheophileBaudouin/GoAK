---
name: pagoda
description: "mikestefanello/pagoda — full-stack SSR web starter (Echo+Ent+HTMX, ~2.9k★). EXTRACT-ONLY: extract the SSR service structure (routes/services/templates); NEVER copy the imposed stack (Ent/Echo/Tailwind)."
category: reference-project
tags: [ssr, web, starter, extract-only, echo, ent]
last-verified: 2026-08-02
---

# pagoda (extract-only)

> **extract-only: true** — extract the structure, not the stack.

## The project

`mikestefanello/pagoda` (2.9k★, pushed 2026-07, CI functional). Self-described as
a "starter kit and admin panel" full-stack web app built on Echo + Ent + HTMX +
Tailwind.

## What you MAY extract

- **SSR service structure**: the separation of routes → services → templates, and
  how a request flows from router through a service to a rendered page. This shape
  is stack-agnostic and transfers to any SSR app (chi, net/http, …).
- **Page/component composition**: how page-level layout and partials are organised
  under a templates layer.
- **Session/auth wiring** as a concept (where it lives in the layering) — not the
  specific implementation.

## What you must NEVER copy

- **The imposed stack**: Ent (ORM), Echo (router), HTMX, Tailwind. These must be
  evaluated and chosen INDEPENDENTLY — Echo is not in this kit's admitted set, and
  the kit's REST default is chi (see `recipe-rest-chi`).
- **The admin-panel surface** — it is product scope, not a universal pattern.
- **The full scaffold** — again, the kit is not a starter.

## How an agent should use this

Borrow the *layering idea* (routes/services/templates) and re-express it over the
consumer's chosen stack. If the consumer genuinely wants Ent or Echo, vet EACH
component against the admission criteria as its own library sheet — do not pull
the whole stack on pagoda's authority.

## Verification

- 2.9k★ (≥500 floor ✓), pushed 2026-07 (<12mo ✓), not archived.
- Open issues: 2 — no recurring-issue mass to log.
