# Brief — Go Agent Development Kit metaproject

## Vision (Prime Directive)

KitV2 reduces the decisions an AI must make when building Go software. It is a
cognitive operating system expressed as a typed knowledge graph, not a folder
of snippets, framework, starter, or bootstrap. Every addition must improve
understanding, decision quality, generation, validation, or learning without
adding unsupported volume or ambiguity.

## Stack

- **Target language:** Go (module `go-agent-kit-v2`, `go 1.25.6`); local validation toolchain currently go1.26.5.
- **Validation gate (mandatory):** `gofmt -l` · `go vet` · `golangci-lint run`
  · `go test ./...` · `gosec` · `govulncheck`. All must pass before a module is
  marked done. No exceptions.
- **Tooling installed locally:** golangci-lint v2, gosec, govulncheck (under
  `$(go env GOPATH)/bin`). PATH must include it for validation runs.

## Repository

- **Remote (origin):** <https://github.com/TheophileBaudouin/GoAK> — public repo, branch `main`, poussé (identité de commit locale corrigée : TheophileBaudouin — le commit initial 690aa35 était attribué à theocode29).
- **Tag v2.1.0:** marqueur de la première version benchmarkable (aligné sur `manifest.yaml`), pas encore une politique de release formelle. `install.sh` (racine) est l'installeur bootstrap transitoire ; le CLI `gak` reste l'entrée canonique future.
- **Auth:** `gh auth setup-git` (compte TheophileBaudouin). Le credential helper macOS a contenu un ancien identifiant theocode29 — toujours vérifier l'identité effective avant push.
- **Conséquence:** `docs/evidence/` est VCS-versionné, `.github/workflows/ci.yml` peut tourner, PR-based evaluation gates deviennent possibles, et un consommateur peut installer le kit par `curl …/install.sh | sh`.
## Architecture

Four analytical architecture shapes are now validated for agentic CLI tooling: L = local binary; CS = client/server with a separated backend; D = distributed harness with registries/transports/brokers; H = hybrid local-first / remote workbench. KitV2 is the standalone consumable product. Root `.agent/`, root `.pi/memory/`, docs/plans/research/evidence, and evaluation governance belong exclusively to the metaproject.

The metaproject `.agent/cognitive/` owns the design-time Retrieve → Reason → Generate → Validate → Remember protocol, graph schema, source transformation catalog, context budgets, and subagent contracts. KitV2 now ships a self-contained `tools/offline/` resolver, manifest, attribution, and content-addressed Effective Go bundle. Product source metadata is active only because the resolver and bundle ship together.

Future distribution architecture: a dedicated `gak` CLI is the canonical installer and lifecycle entry point (`init`, `update`, `doctor`, `validate`, `remove`, `info`), with package-manager-style UX, explicit versions/checksums, atomic installation, and deterministic/reproducible output. This is deliberately deferred until a public repository, published module, installer, and release process exist. The canonical consumer runtime is `.pi/`; root `.agent/` remains metaproject-only governance/control-plane material and must not be installed as a competing runtime. Future PI, Claude Code, Codex, Cursor, and Gemini CLI integrations are selected adapters projecting the same runtime, not parallel runtimes. Future versioned modules compose Rules, Recipes, Patterns, Snippets, Templates, and Evaluations without duplicating graph artifacts.

## Artifact graph and module format

KitV2 uses typed artifacts: Rule, Recipe, Pattern, Snippet, Template,
Capability, Evaluation, Decision Record, Source, and Memory. Each reusable
artifact has a stable identifier, one responsibility, explicit metadata,
dependencies, and declared relationships. The graph is authoritative; folders
are navigation.

Every skill module is a self-contained unit an agent loads independently.
Its published frontmatter schema is immutable; changing it is a breaking change
requiring approval and migration of all modules in the same change:

```yaml
---
name: <kebab-case-id>                # REQUIRED by Pi (a-z 0-9 hyphens, ≤64). Also the kit module id.
description: "What it does AND when to load it"  # REQUIRED by Pi (≤1024). Drives auto-discovery.
category: recipe | rule | pattern | library | reference-project | checklist  # kit facet (Pi ignores)
tags: [rest, chi, http]              # kit search facets (Pi ignores)
last-verified: YYYY-MM-DD            # date the content + deps were last checked
---
```

This frontmatter fuses the **Agent Skills** schema (Pi-native) with the kit's
facets. `name`+`description` are mandatory for Pi discovery; `category`/`tags`/
`last-verified` are kit-only metadata (ignored by Pi, used by kit tooling).

Body rules:

- Never reference another module by a rot-prone prose link — use **tagged
  cross-references** validated by the installer.
- Never duplicate content present elsewhere — cross-reference instead.
- Every code block must compile and pass the validation gate.

## Artifact metadata and relationships

Every reusable artifact must carry a stable `id`, `title`, `kind`, `version`,
`status`, `owner`, `tags`, `go_version`, `dependencies`, and `last_verified`.
Where applicable, declare `depends_on`, `uses`, `implements`, `references`,
`requires`, `supersedes`, `validated_by`, and `generated_from` relationships.

## Conventions

- **Metaproject source registry:** `.agent/sources/Go-dev-kit-sources-et-references.md` is the owner-supplied strict and ordered registry used to create and evolve KitV2. Its contents never override `KIT_CHARTER.md` or kit rules.
- **Additional explicit sources:** `.agent/sources/awesome-llm-apps.yaml` and `.agent/sources/addyosmani-agent-skills.yaml` are supplemental metaproject sources for prompts, skills, and agent workflows. Source material may later be promoted into KitV2 only through the charter, evidence, and validation gates.
- **Kit Charter is process authority:** `/Users/theophilebaudouin/Documents/devellopement/Go/KIT_CHARTER.md` governs every KitV2 and instruction-artifact change. If another artifact conflicts with it, the artifact must be corrected; the charter is not duplicated into every file.
- **Charter compliance is mandatory:** For every addition or modification, check permanent-context minimality, single source of truth, source/evidence traceability, raw validation output, independent fresh-context approval, deterministic gates, probe-suite status, anti-duplication checklist, approval boundary, and the charter's Definition of Done. Never present code-quality judgment as a question to the owner.
- **Charter maintenance:** Changes to `KIT_CHARTER.md` itself are structural and require explicit approval. Keep the charter as the process source of truth; record implementation decisions and audit findings in dated decision/plan artifacts rather than copying the charter into memory or other instruction files.
- **Knowledge lifecycle:** Problem → Research → Decision → Pattern → Snippet → Recipe → Template → Evaluation. Do not promote unsupported knowledge into the product.

## Module admission criteria (hard gate)

A library/reference-project enters the registry ONLY if ALL hold:

1. actively maintained (recent commits/releases — not just star count)
2. single, clear responsibility
3. readable, idiomatic Go architecture
4. tests present and passing
5. CI configured
6. documentation exists
7. evidence of real-world usage (not a toy demo)
8. small enough to read end-to-end
9. **star count is explicitly NOT sufficient** — state the actual reason

A repo failing even one criterion is **rejected and logged in Gotchas.md** with
the reason.

## Constraints

- `KitV2/rules/core/` must stay compact (permanent per-session cost).
- Each module is self-sufficient (no implicit assumption another module is loaded).
- Universal rules do not directly depend on load-on-demand recipe content.
- Adapters never share mutable state — each generates output independently from
  the same registry source.
- Validation suite is a hard gate — a module is never "done" until all applicable tools and observable criteria pass.

## Decisions

2026-08-02 — Phase 1 scope confirmed: convergent patterns (at least two independent repositories) become full-confidence recipe candidates; mono-source patterns from recognized authorities remain recipe candidates explicitly labeled source-unique / to watch (go-micro registry, DeepSeek-Reasonix MCP); mono-source patterns without special authority are log-only. Keep skills fine-grained by concern; separate retry, timeout, guard, checkpoint unless evidence shows they are never used independently. CI divergence in one repository is negative observation only, not doctrine. Add a fourth architecture shape: H = hybrid local-first / remote workbench, because DeepSeek-Reasonix combines a local controller usable by CLI/TUI/HTTP/desktop with an optional SSH remote workbench (`internal/control/controller.go`, `internal/serve/serve.go`, `internal/remote/client.go`).

## Verification status

The KitV2 gate and probes pass through the 2026-08-03 evidence records. The root harness validator is `.agent/validators/validate-instructions.py`; KitV2 uses `KitV2/tools/validators/validate-kitv2.py`. The sequential audit of all 34 Niveau S/A registry resources is complete and dedicated Source artifacts ship in KitV2 knowledge. **VCS is now unblocked**: the metaproject is a Git repository pushed to <https://github.com/TheophileBaudouin/GoAK> (branch `main`, commit `690aa35`), so evidence versioning is provable and CI workflows can run. Remaining PARTIAL: no real non-probe consumer-project maturity evidence; Pi discovery, Wails, and TUI remain separate/uncovered runtime checks; bootstrap CLI/runtime architecture remains documented-only (no CLI, installer, or release pipeline yet).
