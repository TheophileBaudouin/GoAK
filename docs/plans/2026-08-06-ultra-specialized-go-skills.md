# Plan — Ultra-specialized Go skill expansion (2026-08-06)

## Goal

Expand the KitV2 knowledge surface with a batch of ultra-specialized Go
micro-expertises that a Pi orchestrator can route to precisely. Every new
artifact answers **one distinct, recognized question** and cites a verifiable
primary or recognized source. Nothing is invented.

## Context

- KitV2 is a compact, typed knowledge graph. "Skills" in the mission sense map
  to the kit's native artifact kinds:
  - **knowledge YAML** (patterns / anti-patterns / sources) — decision
    micro-expertises, routed through `router/index.json` by intention.
  - **registry rules** (SKILL.md) — must-always-be-true imperatives, loaded on
    demand.
  - **strengthening** of an existing, more specific artifact — when research
    fills a real gap, the existing artifact is updated, never duplicated.
- The mission's own example list (naming, interface design, error wrapping,
  context, goroutines, graceful shutdown, transactions, logging…) is **already
  covered** by the existing graph (39 patterns, 54 anti-patterns, 41 sources,
  13 rules, 15 recipes). The added value is the *uncovered* remainder, plus
  the mission-listed stdlib domains that have no pointer yet.
- Naming: the kit's id conventions (N1) are the authority over the mission's
  `go-{domain}-{subdomain}` suggestion — `pattern:go:<slug>`,
  `anti-pattern:<domain>:<slug>`, `source:<domain>:<slug>`, registry rule
  `<slug>` already implement the same uniform scheme.

## Constraints

- English only (D-2026-08-05-21). One question per artifact. Primary sources
  (official Go docs/blog/wiki/FAQ first; recognized authors second).
- No duplication: each candidate is checked against the existing graph
  (id/title/question grep) and against `rules/core/universal` before creation;
  overlapping material strengthens the most specific existing artifact.
- No core budget change (`rules/core/` stays ≤ 6 modules — no core edit).
- Gate: `validate-kitv2.py` (metadata schema, resolved relations, router
  coverage), `build_index.py --check`, probes. New YAML must pass the
  metadata + freshness + relation-resolution checks.
- Refused domains (documented in report): Go repository pattern, Clean
  Architecture, DDD — OOP doctrine vs the charter's Go-native decision order.

## Done

- New artifacts: 11 stdlib pointers, ~10-12 patterns/anti-patterns/sources,
  1 registry rule (`naming`), all with verified sources.
- 2-4 existing artifacts strengthened where research found real gaps
  (bumped `last_verified`, no duplicated bodies).
- Router regenerated, `--check` PASS, validators PASS, probes PASS.
- Plan report: new count, sources, merged, refused + reasons, under-covered
  domains, future recommendations.

## Candidate artifacts (verify sources during research)

### stdlib pointers (official pkg.go.dev / go.dev)

`source:go:encoding-json`, `source:go:crypto`, `source:go:io`,
`source:go:io-fs`, `source:go:regexp`, `source:go:time`, `source:go:slices`,
`source:go:net-url`, `source:go:sync-atomic`, `source:go:go-generate`,
`source:go:cross-compilation`.

### patterns

- `pattern:go:zero-value-valid` — zero value immediately usable
  (Go FAQ / Effective Go / CodeReviewComments).
- `pattern:go:value-vs-pointer-receivers` — receiver kind decision
  (Go FAQ / CodeReviewComments / Go wiki).
- `pattern:go:generics-when-worth` — when generics pay off
  (Ian Lance Taylor "When to use generics"; official generics tutorial).
- `pattern:go:internal-packages` — `internal/` API boundary (official docs).
- `pattern:concurrency:channel-ownership` — sender closes; explicit ownership
  (official pipelines & cancellation post).
- `pattern:go:semantic-import-versioning` — major-version module paths for
  API compatibility (Go blog "Keeping Your Modules Compatible").
- `pattern:testing:blackbox-package-tests` — external `package foo_test`
  (official testing docs).

### anti-patterns

- `anti-pattern:go-reflection-overuse` — reflection where concrete code or
  generics suffice (Laws of Reflection, official).
- `anti-pattern:sec-weak-randomness` — math/rand for security-sensitive uses
  (crypto/rand docs, Go 1.22 math/rand/v2, OWASP).
- `anti-pattern:sec-timing-unsafe-comparison` — non-constant-time secret
  comparison (crypto/subtle, OWASP).
- `anti-pattern:concurrency:close-from-receiver` — receiver closes a channel.

### sources

- `source:performance:benchmarking` — testing.B, -benchmem, benchstat.
- `source:go:gc-guide` — Go GC tuning guide (go.dev/doc/gc-guide).

### registry rule

- `rules/registry/naming` — deepens universal's package-naming bullet
  (precedent: doc-comments registry rule); sources: Go blog package names,
  CodeReviewComments naming, rakyll style guide.

### strengthen (after gap check)

- Candidates: `pattern:http:middleware-chain`, `pattern:go:concrete-returns`,
  `pattern:go:contextual-worker`, `anti-pattern:go-goroutine-leak`,
  `pattern:database:transaction-boundary`.

## Evidence

Raw research output in `docs/evidence/2026-08-06/ultra-specialized-skills/`
(source URLs verified, dates).
