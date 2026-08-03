# Technology documentation audit — 2026-08-03

## Directive boundary

The permanent rule governing this audit is stored only in the metaproject
agent memory. It is not added to KitV2, Go code, packages, examples, or
shipped documentation.

The authoritative inventory is:

`.agent/sources/Go-dev-kit-sources-et-references.md`

This audit distinguishes technologies **present in the product** from
technologies merely listed as future candidates. Full documentation is not
copied into the LLM context or product artifacts; official sources are stored
or referenced through bounded, content-addressed retrieval.

## Present technology inventory

| Technology | Evidence of presence | Local coverage | Status / action |
|---|---|---|---|
| Go toolchain (`go 1.25.6`, local Go 1.26.5) | `KitV2/go.mod`, `tools/offline/`, probes | `knowledge/stdlib/toolchain-offline.yaml`, pinned resolver metadata | Complete for current offline retrieval; refresh when toolchain changes |
| pkg.go.dev / Go standard library | offline resolver and probe | `knowledge/stdlib/pkg-doc-offline.yaml`, capability/evaluation metadata | Complete for bounded package/symbol lookup; not a copied HTML corpus |
| Effective Go | content-addressed bundle blob + index | `knowledge/stdlib/effective-go-offline.yaml`, attribution, resolver | Complete for current pinned source; historical-source limitation documented |
| gofmt, go test, go vet | toolchain resolver and validation gate | toolchain metadata, rules, probes | Complete |
| benchmarks, fuzzing, race, pprof, trace | catalog/toolchain mappings and validation rules | `toolchain-offline.yaml`, source catalog | Represented; targeted recipes/evaluations remain proposed until consumed |
| chi v5 | direct dependency, REST recipe, probe | `knowledge/catalogs/libraries/chi/SKILL.md`, `recipe-rest-chi` | Partial: local decision record exists; official docs/API/migration snapshot is not separately indexed |
| bubbletea v2 | direct dependency, interactive CLI recipe | recipe and source code | Partial: no dedicated local technology catalog/reference metadata |
| x/sync errgroup | direct dependency, worker-pool recipe | recipe and source code | Partial: no dedicated local official API snapshot |
| modernc.org/sqlite | direct dependency, SQLite recipe/probe | `knowledge/catalogs/libraries/modernc-sqlite/SKILL.md` | Partial: decision catalog exists; current upstream version provenance/docs not fully local |
| sqlc | recipe and catalog | catalog + recipe + SQL configuration | Partial/decision-covered; official docs are represented by selected citations, not a complete local source bundle |
| testify | catalog and tests | `knowledge/catalogs/libraries/testify/SKILL.md` | Catalog coverage exists; official reference/migration metadata is incomplete |
| slog | direct standard-library usage | `rules/registry/logging/SKILL.md` and source pointers | Partial: no dedicated local source metadata record |
| google/uuid | transitive dependency and code usage | no dedicated catalog | Missing dedicated local documentation |
| net/http, database/sql, context, testing, flag, os/exec, runtime/pprof, runtime/trace | direct standard library usage | pkg-doc/toolchain resolver and rules | Covered through official Go source routing; no duplicate per-package corpus required |
| golangci-lint | validation configuration and rule | `rules/core/validation/golangci-lint/SKILL.md`, `.golangci.yml` | Partial: tool guidance exists; exact installed version/update date not captured in a technology metadata record |
| gosec | validation gate and rule | `rules/core/validation/gosec/SKILL.md` | Partial: tool guidance exists; exact installed version/update date not captured |
| govulncheck | validation gate and rule | `rules/core/validation/govulncheck/SKILL.md`, Gotchas | Partial: tool guidance exists; exact installed version/update date not captured |
| Wails v3 | desktop recipe reference, no Go import in product | `recipe-desktop-app/SKILL.md` | Partial and intentionally host-wiring limited; upstream snapshot absent |
| Bubble Tea host behavior | recipe reference | recipe + probe limitation | Partial; host behavior explicitly outside probe coverage |

## Registry technologies not currently present

The source registry also lists Viper, Koanf, Cobra, Zap, Zerolog, Validator,
Resty, Gin, Fiber, Echo, sqlx, GORM, golang-migrate, GoMock, go-redis,
Kafka/RabbitMQ/NATS clients, OpenTelemetry, Prometheus, Air, Mockery, JWT,
OpenAI SDK, Ollama, go-blueprint, Cookiecutter, Awesome Go, Go by Example,
Go Cookbook, GitHub Code Search, and Sourcegraph. These remain source-registry
candidates or catalog references unless direct product evidence adopts them.
They should not receive speculative product documentation or dependencies.

## Findings

### Real documentation gaps

1. Several technologies used directly by KitV2 lack a dedicated local metadata
   record with exact version, retrieval date, upstream update date, official URL,
   and licence/redistribution note: bubbletea v2, x/sync, slog, google/uuid,
   golangci-lint, gosec, govulncheck, and Wails v3.
2. Existing library catalogs are decision records, not complete official
   documentation. They are useful and must remain canonical for selection
   decisions, but they need explicit provenance/update metadata and bounded
   official-source references before being called complete.
3. The current source bundle is complete for the three critical Go sources but
   deliberately not a general-purpose mirror of every third-party website.

### Non-gaps / intentional boundaries

- Do not copy complete third-party documentation into the context.
- Do not document every transitive module independently when Go module sums and
  the parent technology's official docs are sufficient.
- Do not add docs for registry candidates not adopted by the product.
- Do not create duplicate Rules/Recipes from library documentation; catalog
  entries remain selection/limits/alternatives records and link to official
  source units.
- Do not promote community sources over official sources.
- Do not change the permanent rule into a KitV2 artifact.

## Minimal next correction

Create one metaproject-only documentation coverage manifest/index for the
technologies actually present. It contains metadata and bounded source
pointers, not copied documentation, in `.agent/cognitive/technology-documentation.yaml`.
Official API pages for the six direct dependency/tool technologies were fetched
into the context-mode cache under the labels declared in
`.agent/cognitive/technology-source-units.yaml`; only metadata and bounded
section retrieval are used by the agent.

Existing catalogs remain the canonical selection artifacts. The new registry
records exact versions, dates, URLs, licenses, local units, and coverage status
without duplicating catalog bodies. The cognitive validator checks required
metadata, metaproject-only scope, and source-unit references.

This remains staged: targeted official fetch/pin comes before any promotion to
the standalone bundle; no bulk scrape or KitV2 documentation corpus is
justified by the audit.
