# Decisions — Go Engineering Kit

## Sourcing policy

Rules in `KitV2/rules/` and `KitV2/knowledge/` are added only when a real source supports them. A source is recorded here with its scope and limits; unsupported ideas remain hypotheses, not product doctrine.

- `.agent/sources/Go-dev-kit-sources-et-references.md` is the strict, ordered source registry supplied by the owner for creating and evolving KitV2. Its contents, priorities, and categories are indispensable for metaproject source selection. All use remains subordinate to `KIT_CHARTER.md` and the kit rules; the registry does not override them.
- `.agent/sources/awesome-llm-apps.yaml` and `.agent/sources/addyosmani-agent-skills.yaml` are additional explicitly requested metaproject sources for prompts, skills, and agent workflows, even though they are not part of the supplied exhaustive registry. Their content is not automatically KitV2 content.

## Go style and structure

- [Effective Go](https://go.dev/doc/effective_go) is a baseline for idiomatic Go, but its page notes that it is not actively updated for newer language and library changes.
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) supplies review guidance for contexts, errors, goroutine lifetimes, interfaces, examples, and tests. It is a supplement, not an exhaustive style guide.
- [Go Proverbs](https://go-proverbs.github.io/) supports small interfaces, concrete clarity, explicit error handling, and simple concurrency design.
- [Go package names](https://go.dev/blog/package-names) supports short, clear, lower-case package names and warns against generic packages such as `util`, `common`, `api`, and `types`.
- [Google Go Style Guide](https://google.github.io/styleguide/go/) is a Google-specific canonical style reference, not a universal Go specification.
- [Uber Go Style Guide](https://github.com/uber-go/guide) is a practical community/company guide; use it as supporting evidence, not as Go authority.
- [Organizing a Go module](https://go.dev/doc/modules/layout) demonstrates that Go supports layouts from one root package through `internal/` and optional `cmd/`; it does not mandate one universal tree.
- `golang-standards/project-layout` is not treated as authority. The kit prefers the smallest structure justified by a concrete recipe or project need.

## Compatibility

- [Go module reference — `tool` directive](https://go.dev/ref/mod#go-mod-file-tool) documents the `tool` directive, which adds a tool package to the module and makes it available through `go tool`; the kit currently documents this as a later modernization, not a required migration.
- [Go 1.25 release notes](https://go.dev/doc/go1.25) establish that `testing/synctest` became generally available in Go 1.25 and that Go 1.25 has no language changes affecting existing programs.
- [Go 1.26 release notes](https://go.dev/doc/go1.26) establish the new `go fix` modernizers. The local Go 1.26.5 observation is recorded in Gotchas: `go mod init` wrote `go 1.26.5`; the kit must not claim a compatibility matrix without testing target toolchains.

## Agent workflow

- [AGENTS.md](https://agents.md/) is a plain Markdown convention for agent-facing project context, with no required fields and support for nested files.
- [Awesome LLM Apps](https://github.com/Shubhamsaboo/awesome-llm-apps) is recorded as a research source for prompts, agent skills, agent applications, and workflow examples. Observed source surfaces include `agent_skills/`, repository README guidance, and deterministic skill-evaluation/security workflows. It is a source for future review, not copied operational doctrine.
- [Addy Osmani Agent Skills](https://github.com/addyosmani/agent-skills/tree/main/skills) is recorded as a research source for prompt and skill organization, workflow phases, progressive disclosure, and agent-skill discovery. Observed source surfaces include `skills/`, lifecycle slash commands, and skill references/docs. It is a source for future review, not copied operational doctrine.
- [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) supports minimal high-signal context, progressive disclosure, just-in-time retrieval, and persistent notes.
- [Anthropic long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) supports an initializer/coding-agent split, incremental work, progress artifacts, and end-to-end human-like verification. It is evidence for the workflow design, not a guarantee across all runtimes.
- [GitHub Spec Kit](https://github.com/github/spec-kit) provides the relevant sequence: specify/clarify, plan, tasks, implement, analyze/converge. The kit adds a mandatory observable verification phase.
- [Agent Skills specification](https://agentskills.io/specification) supports load-on-demand `SKILL.md` packages with metadata and optional resources. The kit keeps its existing Pi-specific frontmatter contract.

## Architecture decisions

- 2026-08-03 — The official future distribution mechanism is a dedicated `gak`
  CLI, not manual file copying. The CLI is the canonical entry point for
  `init`, `update`, `doctor`, `validate`, `remove`, and `info`; it must provide
  a package-manager-style UX while preserving explicit versions, checksums,
  ownership, atomic installation, deterministic output, and reproducible
  recreation. Deployment is intentionally postponed until a public repository,
  published module, installer, and release process exist. The future bootstrap
  targets are documented only as `go install <future-published-module>/cmd/gak@latest`
  and `go run <future-published-module>/cmd/gak@latest init`; no placeholder
  repository path is valid.
- 2026-08-03 — The canonical consumer agent runtime is `.pi/`, not a new
  `.agent/` runtime. Pi's primary documentation and local runtime evidence show
  that project `.pi/settings.json`, `.pi/prompts/`, and `.pi/skills/` are native
  project surfaces; the existing boundary decision also proves `KitV2/.agent/`
  must remain absent. Root `.agent/` remains metaproject-only governance and
  cognitive control-plane material. Future non-Pi integrations are adapters or
  projections of the canonical runtime, not competing runtimes, and must install
  only the selected adapter.
- 2026-08-03 — Future distribution is modular: `gak` selects versioned knowledge
  modules such as postgres, grpc, auth, kafka, docker, kubernetes, and otel.
  Each module composes Rules, Recipes, Patterns, Snippets, Templates, and
  Evaluations through the existing graph and explicit relationships. The CLI
  materializes selected modules into the canonical runtime while preserving
  provenance and ownership; it must not duplicate canonical artifact bodies.

- 2025-07-31 — The repository needs testable Go examples, so the kit module
  exists to compile recipe examples; the repo is a kit, not an application.
- 2025-07-31 — Recipes are importable packages rather than throwaway `main`
  programs; runnable demos use a separate example package when needed.
- 2025-07-31 — Universal rules are loaded every session, so project-specific
  guidance belongs in load-on-demand product content; the permanent context
  budget is non-negotiable.
- 2025-07-31 — The stray directory with a space in its name was removed; root
  directories must use shell-safe names.

## Confidence and behavior

- Mechanical checks are not behavioral proof. The kit therefore requires each recipe to include a concrete, user-observable scenario and an actual execution check. The distinction is a product requirement from the kit owner; sources above support the need for explicit end-to-end verification but do not prove every generated app correct.
- The requested LLM reliability studies and Pearce et al. security study were not fully verified in this session due to web-tool limits. No numerical claim from those studies is added to kit doctrine until primary papers are retrieved and checked.

## Reliability evidence

- [Pearce et al., Asleep at the Keyboard?](https://arxiv.org/abs/2108.09293) generated 1,689 programs across 89 security-relevant scenarios and reported approximately 40% vulnerable in that study's prompts and conditions. This is evidence against treating generated code as automatically secure, not a universal rate for all models or projects.
- [Sandoval et al., Lost at C](https://arxiv.org/abs/2208.09727) studied 58 student programmers implementing a C data structure and reported critical security bugs no greater than 10% above control in that setting. This result is narrower and does not negate the need for behavioral verification.
- No primary source was found in this session sufficient to support a numeric claim that same-model tests generally create a specific false-confidence rate. The kit therefore makes the weaker, defensible rule: tests are mechanical evidence and must be paired with observable behavior.
- [OpenSSF Scorecard](https://scorecard.dev/) and [Best Practices Badge](https://bestpractices.coreinfrastructure.org/) cover supply-chain/project-health signals; they are intentionally deferred for this local-only kit.

## Memory ownership and consumer bootstrap

- The root `.pi/memory/` is the only authoritative memory for this metaproject.
- KitV2 must not ship `.pi/memory/`; consumers initialize their own memory
  locally.
- Reusable memory behavior belongs in `KitV2/AGENTS.md` and
  `KitV2/.pi/prompts/workflow-memory.md`: initialize first, read before acting,
  record only durable context/progress/gotchas/rules/evidence, and never store
  transcripts, temporary reasoning, raw output, generic kit guidance, or secrets.

## Kit v1 deletion approval

- 2026-08-03 — Owner approved the plan to delete the obsolete v1 product only
  after an external archive, checksum, restore drill, self-contained KitV2
  validator, rewritten root harness/CI/dependabot, complete KitV2 gate, and
  a final active-reference scan all pass. The root metaproject and KitV2 are
  retained. No Git repository exists, so archive integrity replaces VCS
  rollback evidence; any failed checkpoint leaves the source product intact.
  Historical evidence may retain old paths, but active instructions and runtime
  tools may not reference the deleted product. This checkpoint passed on
  2026-08-03; the former product now exists only in the external archive.

## KitV2 migration history

- 2026-08-02 — Owner approved the additive KitV2 migration. Rules, knowledge,
  recipes, snippets, templates, probes, manifest, scripts, and migrated Go
  examples were created beside the former source product. The source product
  was retained until the later archive-backed deletion approval.

- 2026-08-03 — Boundary correction approved after Pi-native research: root `.pi/memory/`, root `.pi/` project resources, and metaproject decision/evaluation/governance artifacts belong to the metaproject; they must not be shipped inside KitV2. Pi natively loads `AGENTS.md`, `.pi/settings.json`, `.pi/prompts/*.md`, and recursively discovered `.pi/skills/**/SKILL.md`; Pi does not natively load singular `.agent/`. KitV2 therefore keeps a kit-facing `AGENTS.md` plus native `.pi/` resources and removes metaproject-only `.agent/decisions/`, `.agent/memory/`, `.agent/evaluations/`, `.agent/capabilities.yaml`, and duplicate `.agent/skills/`/prompts. Non-goals: no change to v1, no new dependency, no V2 deletion, no claim of Pi runtime discovery until executed. No-VCS deletion risk is accepted as PARTIAL by the owner.

## Offline official-Go retrieval

- 2026-08-03 — Offline official-Go retrieval uses a metadata-first,
  `goretrieval/1` protocol with fixed resolution order: local content store,
  GOROOT/GOMODCACHE, explicit online refresh, then `blocked`; it never
  fabricates missing API or guidance. `pkg.go.dev` is represented by
  `go doc`/local module data rather than copied HTML. Effective Go is pinned
  and labelled historical. Toolchain capabilities are mapped to `go help`,
  `go doc`, and GOROOT command sources.
- 2026-08-03 — Phase 1-4 bundle approval completed: KitV2 now ships a
  self-contained manifest, SHA-256 content-addressed Effective Go source,
  license/attribution, stdlib-only resolver, product validator, offline probe,
  and Pi load-on-demand retrieval/memory workflows. Product source metadata is
  active only because the resolver and bundle ship together; the metaproject
  catalog mirrors the same active sources. No Git repository exists, so commit
  authenticity and rollback history remain PARTIAL.
- 2026-08-03 — The metaproject `.agent/cognitive/` owns retrieval governance,
  graph schema, source admission, and subagent contracts. KitV2 now contains a
  complete standalone runtime bundle and must not point into metaproject files.
- 2026-08-03 — Cognitive source transformation targets are status-honest:
  only materialized targets are `active`; forward capability, evaluation, rule,
  and pattern targets remain `proposed` until a consumer and artifact exist.
  The catalog uses `race` as the canonical toolchain retrieval unit, and the
  validators enforce target materialization, product relationship status, and
  product knowledge metadata without importing metaproject files.
- 2026-08-03 — The standalone product graph declares metadata objects for its
  shipped offline lookup capability and retrieval evaluation. Its validator
  resolves stable relationship IDs within `knowledge/**/*.yaml` and allows
  external URLs only for `references`; product documentation must not depend on
  metaproject paths. The universal Go rule remains the canonical source for
  context/errors/interfaces, while implementation references point to it rather
  than repeating its body.
- 2026-08-03 — Technology documentation is maintained in the metaproject only:
  `.agent/cognitive/technology-documentation.yaml` records adopted technology
  versions, retrieval/update dates, official URLs, licenses, local units, and
  coverage status; `.agent/cognitive/technology-source-units.yaml` routes to
  bounded official source-cache sections. Unadopted registry candidates are
  not bulk-documented, and no directive or third-party documentation corpus is
  shipped in KitV2.
- 2026-08-03 — Owner authorized real dependencies for source points 3–4.
  KitV2 pins Viper v1.21.0, Koanf v2.3.5 plus its confmap provider v1.0.0, and
  Cobra v1.10.2. Koanf is the explicit-cascade default for new configuration;
  Viper is retained for existing/broad integrations; Cobra is reserved for
  multi-command CLIs while stdlib `flag` remains the flat-CLI default. The
  dependencies, module allowlist, recipes, catalogs, and offline probes are
  updated atomically and validated offline.

## Charter compliance

- 2026-08-02 — The initial correction wave established deterministic probes, raw evidence, and instruction validation. Its historical v1 paths are preserved only in the external archive/evidence record; active KitV2 tooling uses the standalone product paths.
- 2026-08-02 — `KIT_CHARTER.md` is process authority. Structural approvals are recorded in this file before implementation. The current product probe runner is `KitV2/probes/run.sh`; Pi discovery remains a separate runtime check.

## Deferred by reconciliation

- Secret scanning, SARIF publication, SLSA provenance, and release/versioning infrastructure are deferred because this is a personal, local kit and the deliverable is not currently a public/shared release pipeline. Revisit if the kit or generated apps are distributed outside the machine.
- Dedicated Claude/Codex/Gemini generators are deferred until the core, recipes, and spec-driven workflow are solid. A root `AGENTS.md` plus the existing Pi skills covers the current need without adding parallel output surfaces.
- Fuzzing, `go fix`, `testing/synctest` adoption in recipes, and modern `tool` dependencies remain secondary; adopt only where a concrete recipe gains verified value.
