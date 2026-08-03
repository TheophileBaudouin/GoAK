# Technology documentation audit — 2026-08-03

## Scope

The audit used `.agent/sources/Go-dev-kit-sources-et-references.md` as the
technology registry and inspected the actual KitV2 module, imports, recipes,
rules, catalogs, offline bundle, and installed tools. The permanent directive
is stored only in metaproject agent memory; it is not present in KitV2.

## Inventory result

Direct module technologies are pinned in `KitV2/go.mod`:

- `charm.land/bubbletea/v2 v2.0.8`
- `github.com/go-chi/chi/v5 v5.3.1`
- `github.com/google/uuid v1.6.0`
- `golang.org/x/sync v0.22.0`
- `modernc.org/sqlite v1.55.0`
- Go standard library and local Go 1.26.5 toolchain

The repository also uses or references `slog`, `golangci-lint`, `gosec`,
`govulncheck`, and Wails v3 in its rules/recipes. Registry-only candidates such
as Viper, Gin, Fiber, Echo, Kafka, OpenTelemetry, OpenAI SDK, and Cookiecutter
were not expanded because they are not adopted by the product.

## Official source retrieval

Official package/API pages were fetched and indexed with bounded, queryable
source labels:

- `official:chi-v5.3.1`
- `official:bubbletea-v2.0.8`
- `official:x-sync-v0.22.0`
- `official:modernc-sqlite-v1.55.0`
- `official:google-uuid-v1.6.0`
- `official:log-slog-go1.26`

The raw pages remain in the context-mode cache. They are not copied into the
KitV2 product and are not injected wholesale into an agent context.

## Local coverage

- Go official sources: active and pinned in the existing offline bundle.
- chi, modernc-sqlite, sqlc, testify, validator: existing local decision
  catalogs remain canonical; metadata and official-source labels are now
  recorded in the metaproject registry.
- bubbletea and x/sync: recipes exist; official API cache units and exact
  versions are now registered.
- google/uuid and slog: official cache units and metadata are now registered;
  no duplicated rule or recipe was created.
- golangci-lint, gosec, govulncheck: existing validation rules remain
  canonical; installed version/provenance metadata is registered.
- Wails: remains partial because the product intentionally excludes host
  wiring from the pure-Go recipe and no stable version was pinned.

## Gaps retained intentionally

- No complete third-party documentation mirror was created.
- No documentation was added for unadopted registry candidates.
- No source was promoted into the standalone bundle without a product consumer,
  pin, attribution, checksum, and probe.
- Catalog decision artifacts were not replaced by copied upstream docs.
- `upstream_updated_at: unknown` remains explicit where the audit could not
  verify a reliable release signal.

## Validation

`python3 .agent/validators/validate-cognitive.py` passes and validates the
technology registry metadata, metaproject-only scope, and all registered source
unit IDs. Existing product validators and Go gates are run separately in the
current evidence workflow.
