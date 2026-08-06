---
name: catalog-freshness
description: "Freshness and evidence rules for GoAK catalog modules. Load when creating or updating a library or reference-project catalog; require a fresh primary-source check, exact verification dates, and a review before commit."
category: rule
tags: [catalog, freshness, sources, governance]
last-verified: 2026-08-05
---

# catalog-freshness — write from fresh evidence

## Principle

A catalog decision is a snapshot, not memory. Before creating or updating a
catalog module, perform a fresh web check of the official repository or
maintainer documentation and a version/API source such as `pkg.go.dev`, a
release page, changelog, specification, or official issue/advisory.

Record each source URL and the real verification date in `Verified sources`.
`last-verified` is the date of the complete recheck, not the date the prose was
edited.

## Cadence

- `library`: reverify at least every 90 days; the product validator blocks an
  older catalog entry.
- `reference-project`: reverify at least every 180 days; the validator blocks an
  older entry.
- A living project may require earlier review when a release, advisory, or
  maintenance event changes the decision.

## Required review

Before commit, confirm the current version, maintenance signal, important
limitations, alternatives, and every negative security or compatibility claim.
A live URL is not evidence that the claim on the page is still correct.

## Boundary

This rule does not prescribe a library choice, replace admission criteria, or
prove that a web search occurred. The validator checks dated source evidence
and age; the author and reviewer must verify that the sources were actually
consulted.

## Sources

- [Agent Skills specification](https://agentskills.io/specification) —
  progressive disclosure and bounded skill bodies; verified 2026-08-05.
- [Go testable examples](https://go.dev/blog/examples) — executable examples;
  verified 2026-08-05.
- [GitHub content model](https://github.com/github/docs/blob/main/.github/instructions/content.instructions.md)
  — reusable content and single-source guidance; verified 2026-08-05.
