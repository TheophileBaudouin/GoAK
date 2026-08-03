# Bootstrap CLI and Agent Runtime Architecture Plan

**Goal:** Define the future Go Agent Kit distribution CLI, installed runtime, adapter model, and modular knowledge packaging without implementing deployment.

**Architecture:** The future `gak` CLI is the canonical distribution boundary. It will install a versioned, self-contained kit runtime into a target project through an atomic, manifest-driven operation; the installed project uses one canonical runtime directory, `.pi/`, with agent-specific adapters selected explicitly. The current metaproject `.agent/` remains governance/control-plane material and is not a second consumer runtime.

**Tech Stack:** Go CLI delivered through the Go module ecosystem; versioned manifests and checksums; existing KitV2 knowledge graph and native Pi resources; future adapter contracts for PI, Claude Code, Codex, Cursor, and Gemini CLI.

---

## Scope and decision boundary

This is an architecture-only change. It records the future distribution contract and roadmap. It does not create `cmd/gak`, an installer, an update script, a repository URL, a release workflow, or a placeholder deployment mechanism.

The workspace currently has no GitHub repository, published module, installer, or release pipeline. The commands below are therefore future deployment targets, not executable instructions today.

## Evidence used

- Pi's official local documentation states that project `.pi/settings.json`, `.pi/prompts/`, and `.pi/skills/` are project-local resources loaded after trust; it also documents package installation and project-local package scope.
- Pi's official skills documentation states that skills are load-on-demand `SKILL.md` packages and can be discovered from `.pi/skills/` or packages.
- Pi's official package documentation states that packages bundle skills, prompts, extensions, and themes, and can be selected or filtered.
- The Go toolchain's local `go help install` and `go help run` state that version suffixes such as `@latest` use module-aware mode independent of the current module; this is the basis for the future bootstrap target.
- Existing boundary evidence proves that `KitV2/.pi/` is the trusted, native Pi surface and that `KitV2/.agent/` is intentionally absent. Existing plans and memory state that singular `.agent/` is not a Pi-native discovery path.

## Future CLI contract

The future `gak` command is the official entry point for distribution and project runtime management:

| Command | Responsibility | Determinism requirement |
| --- | --- | --- |
| `gak init` | Select an agent and modules, then install a complete runtime into a target project. | Same kit version, agent, module set, and target state produce the same manifest and file set. |
| `gak update` | Reconcile an installed runtime to a selected kit release, preserving local ownership boundaries and applying migrations. | Resolve only declared versions; verify checksums before replacement; use an atomic update boundary. |
| `gak doctor` | Inspect manifest integrity, runtime ownership, adapter compatibility, tool availability, and drift. | Report facts and stable diagnostic codes; do not silently repair. |
| `gak validate` | Run the kit's structural, metadata, and selected observable checks against the installed runtime. | Use versioned evaluations and return a reproducible pass/fail result. |
| `gak remove` | Remove only files owned by the kit according to the project manifest. | Never delete unowned or modified files without an explicit policy and confirmation. |
| `gak info` | Display kit, runtime, adapter, module, and manifest metadata. | Read local metadata; do not infer state from folder names. |

The CLI owns orchestration and lifecycle. Canonical rules, recipes, patterns,
snippets, templates, evaluations, and module metadata remain in the knowledge
graph; the CLI must not become a second authoring surface for their bodies.

## Distribution and bootstrap

The preferred future user experience is package-manager-like: a short, discoverable command that selects a versioned release, performs a reproducible installation, and leaves an inspectable project manifest. This is the same usability category as `cargo`, `uv`, `npm create`, `npx`, and `create-next-app`, without claiming implementation parity.

The future deployment targets are:

```text
go install <future-published-module>/cmd/gak@latest

go run <future-published-module>/cmd/gak@latest init
```

No repository or module path exists yet. Do not replace the angle-bracket marker with a fake URL or name. `@latest` is a convenience selector, not a reproducibility pin; reproducible project setup must record the resolved kit version and content checksums in the project manifest.

Deployment is not based on manually copying files. Any future archive extraction, embedded asset materialization, or package-manager integration is an implementation detail behind the CLI contract and must preserve the same manifest, ownership, checksum, atomicity, and migration guarantees.

## Reproducible and deterministic installation

`gak init` must eventually:

1. resolve an explicit kit release and selected module versions;
2. resolve the selected agent adapter from the supported adapter registry;
3. load the corresponding canonical artifact graph entries;
4. materialize only the requested runtime and modules;
5. write a project manifest containing kit version, adapter, module IDs/versions, ownership, source/checksum metadata, and schema version;
6. validate the generated file set before committing it;
7. install through an atomic staging-and-commit procedure with a defined conflict policy.

Reproducible means a project can be recreated from recorded versions and checksums without relying on mutable branch state, ambient metaproject files, or undocumented machine state. Deterministic means equivalent inputs yield the same selected artifacts, paths, ordering, metadata, and validation result. Network access may retrieve a release, but it must not change the selected content after resolution.

## Canonical runtime: `.pi`, not `.agent`

The research conclusion is that the installed consumer runtime is `.pi/`.

Pi's documented native project surfaces are `.pi/settings.json`,
`.pi/prompts/`, `.pi/skills/`, and related `.pi` resources. Existing evidence
also confirms the current product's trusted runtime surface and validates the
absence of `KitV2/.agent/`. Creating a second `.agent` consumer runtime would
not be native to Pi, would duplicate ownership, and would conflict with the
existing boundary decision.

Therefore:

- `.pi/` is the canonical installed runtime directory for the current product.
- Root `.agent/` remains metaproject-only governance and cognitive control-plane material: source admission, graph governance, evaluation methods, and design-time contracts.
- The future CLI must never install root `.agent/` into a consumer project as a competing runtime.
- A future non-Pi adapter may use native files required by its host, but those files are adapter projections owned by the single `.pi` runtime model, not a second canonical runtime. This adapter projection rule requires a future contract and validation before implementation.
- Consumer `.pi/memory/` is project-local state and must not be populated from metaproject memory. The kit may install memory initialization workflows, but not this repository's history.

## Adapter model

The runtime will support agent adapters for:

- PI
- Claude Code
- Codex
- Cursor
- Gemini CLI

An adapter translates the canonical runtime model into the selected agent's
native loading and invocation surfaces. `gak init` installs only the selected
adapter and its required projection; it does not install every agent's files.
Adapters must be independently versioned, capability-declared, deterministic,
and validated against the target agent's documented behavior. Core knowledge
artifacts remain agent-neutral; adapter-specific formatting and entrypoints
must not fork canonical rule, recipe, pattern, snippet, template, or evaluation
bodies.

The adapter registry and compatibility matrix are future implementation work.
The current kit only has native Pi resources and deferred Claude/Codex/Gemini
adapter work; Cursor is an architectural target, not a current capability.

## Module system

The future CLI will install modular knowledge packages selected by project need.
Initial module examples are `postgres`, `grpc`, `auth`, `kafka`, `docker`,
`kubernetes`, and `otel`.

Each module is a graph-scoped package composed from these artifact kinds:

- Rules
- Recipes
- Patterns
- Snippets
- Templates
- Evaluations

A module has a stable ID, version, metadata, declared dependencies, source
references, compatibility constraints, and explicit relationships. Modules are
selected by ID and version, not by directory copying. The module manifest is
the installation contract; the existing KitV2 directories remain navigation
and canonical artifact storage, consistent with the charter.

Modules must be independently consumable and must not duplicate core rules or
other module bodies. Shared artifacts are referenced through graph relations.
The CLI may compose modules into one installed runtime, but it must preserve
artifact provenance and ownership so update and remove can act safely.

## Roadmap milestone: deployment foundation

Deployment is a first-class future milestone, intentionally blocked until a
published repository/module exists:

1. publish the canonical repository and establish its public module identity;
2. define release/version policy and immutable release artifacts;
3. implement the `gak` CLI packaging and command contract;
4. define embedded asset packaging and content-addressed asset verification;
5. implement the deterministic installer and atomic conflict policy;
6. define the project manifest schema and ownership model;
7. implement version resolution and update reconciliation;
8. define and implement migration support for manifest/runtime schema changes;
9. define agent adapter contracts and compatibility checks;
10. implement selected-agent runtime projections without duplicate runtimes;
11. define module packaging, dependency resolution, and evaluation selection;
12. add release automation, provenance, checksums, and observable installation probes;
13. validate fresh-project bootstrap, update, doctor, validate, remove, and migration scenarios.

No item above is implemented by this architecture task.

## Remaining risks and open decisions

- The future public module path is unknown until a repository is published.
- Release signing/provenance policy is not selected; it must be decided before public distribution.
- The project manifest schema is only an architectural requirement, not yet a published contract.
- Native projection details for Claude Code, Codex, Cursor, and Gemini CLI require fresh primary-source research when each adapter is implemented.
- Conflict, preservation, rollback, and migration semantics require executable evaluations before the CLI can be considered complete.
