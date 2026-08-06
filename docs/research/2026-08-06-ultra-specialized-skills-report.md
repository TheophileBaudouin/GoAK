# Report — Ultra-specialized Go skill expansion (2026-08-06)

Mission: extend the KitV2 kit with a collection of ultra-specialized Go
micro-expertises an orchestrator can route to precisely, using only
recognized practices with identifiable sources, and zero duplication.

## 1. New skills added — 25

| Kind | Count | Artifacts |
| --- | --- | --- |
| stdlib pointers | 11 | `source:go:encoding-json`, `source:go:crypto`, `source:go:io`, `source:go:io-fs`, `source:go:regexp`, `source:go:time`, `source:go:slices`, `source:go:net-url`, `source:go:sync-atomic`, `source:go:go-generate`, `source:go:cross-compilation` |
| patterns | 7 | `pattern:go:zero-value-valid`, `pattern:go:value-vs-pointer-receivers`, `pattern:go:generics-when-worth`, `pattern:go:internal-packages`, `pattern:concurrency:channel-ownership`, `pattern:go:semantic-import-versioning`, `pattern:testing:blackbox-package-tests` |
| anti-patterns | 4 | `pattern:antipattern:go-reflection-overuse`, `pattern:antipattern:sec-weak-randomness`, `pattern:antipattern:sec-timing-unsafe-comparison`, `pattern:antipattern:concurrency-close-from-receiver` |
| sources | 2 | `source:performance:benchmarking`, `source:go:gc-guide` |
| registry rule | 1 | `rules/registry/naming/SKILL.md` |

Router index: 253 → 278 resources. Product skills: 71 → 72.

**Naming mapping note.** The mission's `go-{domain}-{subdomain}` convention
is implemented through the kit's own uniform id scheme (N1, the authority):
`pattern:go:<slug>`, `pattern:antipattern:<slug>`, `source:<domain>:<slug>`,
and the `naming` rule directory — same uniformity, kit-native format. No
`GoNamingExpert`-style ids were created.

## 2. Sources used

All 39 URLs verified live (HTTP 200, 2026-08-06), raw evidence in
`docs/evidence/2026-08-06/ultra-specialized-skills/sources.md`.

- **Official Go** (blog/wiki/docs/FAQ/spec): When To Use Generics
  (Ian Lance Taylor), An Introduction To Generics, Effective Go, Go FAQ,
  Code Review Comments, Organizing a Go module, Keeping Your Modules
  Compatible, Go Modules: v2 and Beyond, Go Modules Reference, Go
  Concurrency Patterns: Pipelines and cancellation, The Laws of Reflection,
  Secure Randomness in Go 1.22, A Guide to the Go Garbage Collector, More
  predictable benchmarking with testing.B.Loop, Package names, testing /
  math/rand / math/rand/v2 / crypto/subtle / cmd/go / cmd/cgo / io / io/fs /
  regexp / time / slices / net/url / sync/atomic / encoding/json / crypto
  pkg docs.
- **Recognized community authors** (allowed by the mission's source rules):
  Dave Cheney (zero value, internal packages), rakyll (Go package style
  guide), golang/go#18936 (official issue, constant-time length leak).
- SEO/generic/auto-generated content: none used.

## 3. Skills merged / strengthened

**Zero merges were needed** — this is the honest outcome of the
anti-duplication phase, not an omission. The mission's own example list is
already covered by the existing graph:

| Mission example | Existing artifact (unchanged) |
| --- | --- |
| Go error wrapping | `pattern:go:error-wrapping-chain`, `pattern:go:sentinel-errors`, `pattern:antipattern:go-error-string-matching`, `rules/core/errors` |
| Go context propagation / cancellation | `pattern:go:contextual-worker`, `pattern:go:private-context-keys`, `pattern:resilience:timeout-deadlines`, `rules/core/concurrency` |
| Go goroutine lifecycle | `pattern:go:contextual-worker`, `pattern:antipattern:go-goroutine-leak` |
| Go graceful shutdown | `recipe-graceful-shutdown` (+ probe) |
| Go database transactions | `pattern:database:transaction-boundary`, `pattern:antipattern:db-raw-transactions` |
| Go HTTP middleware design | `pattern:http:middleware-chain` |
| Go logging / observability | `pattern:observability:structured-logging`, `rules/registry/logging`, `source:go:slog` |
| Go interface design | `pattern:go:concrete-returns`, `pattern:antipattern:go-interface-everywhere`, `pattern:go:constructor-injection` |
| Go memory allocation optimization | `source:go:profiling`, `pattern:go:string-builder`, `pattern:antipattern:go-string-concat-loop` |
| Go security review | `source:go:security-best-practices`, 8 security sources, 10 security patterns/anti-patterns |
| Go naming conventions | **new** `rules/registry/naming` (elaborates, does not restate `rules/core/universal` — fresh-context review fixed one near-verbatim duplication) |

Five candidates were evaluated for strengthening (`middleware-chain`,
`concrete-returns`, `contextual-worker`, `goroutine-leak`,
`transaction-boundary`) and each was found already complete and specific to
its question — patching them would have added churn without content. One
existing artifact **was** modified for routing clarity:
`source:go:command`'s selection was narrowed to point cross-compilation and
code-generation intents at the new dedicated pointers (`last_verified`
bumped).

## 4. Skills refused, and why

| Refused | Reason |
| --- | --- |
| Go repository pattern, Clean Architecture, DDD | OOP/Clean-Code/GoF doctrine — the charter's decision order explicitly forbids importing it as a default; Go-native equivalents already exist (`ports-adapters`, `modular-monolith`, consumer-owned interfaces, database patterns) |
| Go programming / Go development / Go best practices | Too broad — violates Z2 "one question, one artifact" and the mission's own granularity rule |
| Generic struct-design / API-boundary / compiler-behavior skills | No single recognized primary source or distinct question (subsumed by existing artifacts) |
| unsafe, memory layout, zero-copy | No verifiable single-question practice with an authoritative source; kept in the under-covered list below instead of invented |
| Metric collection (Prometheus client) | Library not yet vetted in the catalog (9-criteria gate) — a source pointer would outrun the admission process |

## 5. Domains still under-covered

- **Escape analysis / allocation behavior**: no single authoritative primary
  source; the workflow is served by `source:go:profiling` +
  `source:performance:benchmarking` + the GC guide. A dedicated artifact
  waits for a stable primary (e.g. an official wiki page) or an approved
  recognized-author reference.
- **Deadlock / goroutine-leak debugging procedures**: `knowledge/debugging/`
  stays empty by contract (Z2 §7) until an observed, verified failure with an
  actionable procedure is admitted.
- **Metrics (Prometheus/OTel)**: `source:go:opentelemetry` exists; the
  prometheus client has no vetted fiche.
- **Go unsafe / reflect internals**: pointer-only routing exists via
  `source:go:language-specification`; deeper guidance requires a recognized
  source to be vetted.
- **Testing**: integration-test strategy (testcontainers) is a roadmap
  recipe, not yet admitted.

## 6. Future recommendations

1. **Back-references** (fresh-context review, minor): when
   `pattern:concurrency:pipeline` and `pattern:go:minimal-layout` are next
   touched, add references back to the new artifacts so pair/related links
   are bidirectional.
2. **Escape-analysis artifact** when a stable primary appears — until then
   the profiling/benchmarking/GC-guide trio covers the decision path.
3. **Prometheus client + OTel metric fiche** once the 9-criteria library
   admission gate is run (survey 2026-08-05 candidates pending integration).
4. **Catalog-promoted pointers**: the new stdlib pointers give precise
   routing; the next natural wave is `os`, `flag`, `sort`, `embed`, `net`,
   `unicode` if distinct questions justify them — do not pad.
5. **Routing regression check**: rerun the end-to-end router scenarios
   (obvious/vague/empty/near-multiple) after the next indexable change, per
   Z11 §4.

## Verification (gate)

- `validate-kitv2.py` PASS (72 product skills, router 278 resources)
- `validate-instructions.py` PASS · `validate-cognitive.py` PASS
- `build_index.py --check` PASS (deterministic rebuild)
- Probes 15/15 PASS · gofmt clean · `go vet` OK · `go test ./...` OK
- `golangci-lint` 0 issues (no Go source changed)
- Fresh-context review: REQUEST-CHANGES → both moderate findings fixed
  (naming rule duplication, go-command routing overlap) → re-verified PASS
