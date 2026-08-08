# Debugging — knowledge domain

This directory is the "debugging" domain of the Kit's knowledge graph. It
answers one unique question:

> How to diagnose an observed Go failure (panic, deadlock, race, leak,
> slowness, corruption)?

It is an **observed-failure** domain (charter: "Observed production
failure"), not a general best-practices domain: a procedure enters here only
if it solves a concrete, reproducible symptom, verified against a source or
documented experience.

## Artifact format

- One artifact per failure: graph-YAML file `kind: Source` (or `Pattern` for
  a reusable diagnostic procedure), stable id
  (`source:go:debugging:<slug>` or `pattern:go:debugging:<slug>`), complete
  metadata (id, title, kind, version, status, owner, tags, go_version,
  dependencies, last_verified) and `relationships.references` pointing to the
  primary source (official docs, Go issue, verified article).
- Mandatory sections per the category schema (see `../patterns/` and
  `../anti-patterns/` for existing models).
- The body is **never** copied from a source: the YAML routes, explains the
  decision, and cites; the source lives outside the Kit (resolved via
  `tools/offline/` or the `references` link).

## Admission criteria

1. A precise, reproducible failure is described (symptom + detection).
2. A verified root cause is established (primary source or documented
   reproduction) — no unlabeled hypothesis.
3. The diagnostic procedure is actionable (commands, steps, expected outputs)
   and does not duplicate any existing rule or recipe.
4. `last_verified` ≤ 12 months (otherwise warning, 18 months → deprecated).

## Forbidden content

- General "debugging in Go" advice without a concrete failure (→ out of
  scope).
- Copied documentation bodies; raw evidence outputs are kept outside the
  product.
- Duplication of an existing pattern/anti-pattern (`../patterns/`,
  `../anti-patterns/`) or rule (`../../rules/`) — point, do not duplicate.
- Unverified hypothesis presented as fact.

## Roadmap

This directory is intentionally empty: it fills only on observed and verified
failure. Typical candidates (to admit one by one, with source):

- goroutine leak / `go test -race` — correlation with
  `anti-patterns/go-goroutine-leak.yaml`;
- race detected late (flaky CI);
- deadlock (pprof goroutine dump);
- measured slowness (pprof CPU) — correlation with `performance/`.

A domain directory lives only if it has ≥ 1 active artifact; as long as it is
empty, this README is the contract and the roadmap.
