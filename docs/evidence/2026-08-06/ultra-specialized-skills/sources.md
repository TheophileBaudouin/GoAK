# Research evidence — Ultra-specialized Go skills (2026-08-06)

Verified primary sources (HTTP 200, checked 2026-08-06, `curl -sL -A Mozilla`).
Used for the new knowledge artifacts and the `naming` registry rule.

## Official Go blog / wiki / docs

| Artifact target | Source | URL |
| --- | --- | --- |
| `pattern:go:generics-when-worth` | When To Use Generics (Ian Lance Taylor) | <https://go.dev/blog/when-generics> |
| `pattern:go:generics-when-worth` | An Introduction To Generics | <https://go.dev/blog/intro-generics> |
| `pattern:go:zero-value-valid` | Effective Go — The zero value | <https://go.dev/doc/effective_go> |
| `pattern:go:zero-value-valid` | Dave Cheney — What is the zero value | <https://dave.cheney.net/2013/01/19/what-is-the-zero-value-and-why-is-it-useful> |
| `pattern:go:value-vs-pointer-receivers` | Code Review Comments — Receiver Type | <https://go.dev/wiki/CodeReviewComments> |
| `pattern:go:value-vs-pointer-receivers` | Go FAQ — Pointers and Allocation | <https://go.dev/doc/faq> |
| `pattern:go:internal-packages` | Organizing a Go module (official) | <https://go.dev/doc/modules/layout> |
| `pattern:go:internal-packages` | Dave Cheney — internal packages | <https://dave.cheney.net/2019/10/06/use-internal-packages-to-reduce-your-public-api-surface> |
| `pattern:go:semantic-import-versioning` | Keeping Your Modules Compatible | <https://go.dev/blog/module-compatibility> |
| `pattern:go:semantic-import-versioning` | Go Modules: v2 and Beyond | <https://go.dev/blog/v2-go-modules> |
| `pattern:go:semantic-import-versioning` | Go Modules Reference / major versions | <https://go.dev/ref/mod> |
| `pattern:concurrency:channel-ownership` | Go Concurrency Patterns: Pipelines and cancellation | <https://go.dev/blog/pipelines> |
| `pattern:testing:blackbox-package-tests` | testing package docs (black-box) | <https://pkg.go.dev/testing> |
| `anti-pattern:go-reflection-overuse` | The Laws of Reflection | <https://go.dev/blog/laws-of-reflection> |
| `anti-pattern:sec-weak-randomness` | math/rand docs ("not for security-sensitive") | <https://pkg.go.dev/math/rand> |
| `anti-pattern:sec-weak-randomness` | math/rand/v2 docs | <https://pkg.go.dev/math/rand/v2> |
| `anti-pattern:sec-weak-randomness` | Secure Randomness in Go 1.22 (chacha8rand) | <https://go.dev/blog/chacha8rand> |
| `anti-pattern:sec-timing-unsafe-comparison` | crypto/subtle docs | <https://pkg.go.dev/crypto/subtle> |
| `anti-pattern:sec-timing-unsafe-comparison` | golang/go#18936 (length leak) | <https://github.com/golang/go/issues/18936> |
| `source:performance:benchmarking` | testing docs (benchmarks) | <https://pkg.go.dev/testing> |
| `source:performance:benchmarking` | benchstat | <https://pkg.go.dev/golang.org/x/perf/cmd/benchstat> |
| `source:performance:benchmarking` | More predictable benchmarking with testing.B.Loop | <https://go.dev/blog/testing-b-loop> |
| `source:go:gc-guide` | A Guide to the Go Garbage Collector | <https://go.dev/doc/gc-guide> |
| `source:go:go-generate` | go command — generate | <https://pkg.go.dev/cmd/go> |
| `source:go:cross-compilation` | go command env (GOOS/GOARCH/CGO_ENABLED) | <https://pkg.go.dev/cmd/go> |
| `source:go:cross-compilation` | cgo command (CGO_ENABLED default) | <https://pkg.go.dev/cmd/cgo> |
| `rules/registry/naming` | Package names (blog) | <https://go.dev/blog/package-names> |
| `rules/registry/naming` | Code Review Comments — naming | <https://go.dev/wiki/CodeReviewComments> |
| `rules/registry/naming` | Style guideline for Go packages (rakyll) | <https://rakyll.org/style-packages/> |
| `rules/registry/naming` | Effective Go — names | <https://go.dev/doc/effective_go> |

## Stdlib pointers (official pkg.go.dev)

encoding/json, crypto, io, io/fs, regexp, time, slices, net/url, sync/atomic — all live (200).

## Negative / refusal evidence

- Repository pattern, Clean Architecture, DDD: OOP/Clean Code doctrine — charter decision order forbids importing it as default (KitV2/AGENTS.md, Go Engineering Kit metaproject contract; `KIT_CHARTER.md` § decision order, sources registry Niveau S/A guidance).
- "Go best practices"/"Go programming": too broad, no single question — would violate Z2 "one question one artifact".
