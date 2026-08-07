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

- **Tag v2.2.0:** livré avec le semantic resource router (commit e38c068, 2026-08-05) — manifest v2.2.0, index 206 ressources, install.sh amélioré (ANSI minimaliste, étapes, spinner TTY, résumé, retry). Tag v2.2.1 (2026-08-05) : installeur spinner livré par défaut. Install vérifiée de bout en bout : `curl -fsSL https://raw.githubusercontent.com/TheophileBaudouin/GoAK/v2.2.1/install.sh | sh -s -- <dir>` → validation PASS (45 skills + router 206) puis pi -a fonctionnel. `install.sh` (racine) reste l'installeur bootstrap transitoire ; le CLI `gak` reste l'entrée canonique future. **CI gate rouge préexistante résolue (D-2026-08-06-13) : le floor de couverture mesure la surface testable — probes exclues (scénarios exécutables vérifiés par probes/run.sh), library surface 81.5% ≥ 70%.**

## Architecture

KitV2 is the standalone consumable product. Root `.agent/`, root `.pi/memory/`, docs/plans/research/evidence, and evaluation governance belong exclusively to the metaproject. Since 2026-08-04, `.agent/kit-governance/` holds the 15 construction contracts (C0, C1, C2, Z1–Z10, A1, N1) that govern each KitV2 zone: mission, format, actionable rules, patterns, anti-patterns, validation criteria. Every rule a contract states must be verifiable by the product validator or an explicit review control. Templates policy (owner directive 2026-08-04): templates are NEVER agent-authored — each is a minimally-adapted fork of a real, reliable, functional, single-responsibility open-source project under MIT license; existing agent scaffolds are marked `legacy` and candidates for replacement.

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
category: recipe | rule | pattern | library | reference-project | checklist | workflow  # kit facet (Pi ignores); `workflow` = .pi/skills only (2026-08-04)
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
Where applicable, declare `depends_on`, `uses`, `implements`, `extends`,
`references`, `requires`, `supersedes`, `validated_by`, and `generated_from`
relationships (`extends` is declared but unused as of 2026-08-04).

## Conventions

- **Metaproject source registry:** `.agent/sources/Go-dev-kit-sources-et-references.md` is the owner-supplied strict and ordered registry used to create and evolve KitV2. Its contents never override `KIT_CHARTER.md` or kit rules.
- **Additional explicit sources:** `.agent/sources/awesome-llm-apps.yaml` and `.agent/sources/addyosmani-agent-skills.yaml` are supplemental metaproject sources for prompts, skills, and agent workflows. Source material may later be promoted into KitV2 only through the charter, evidence, and validation gates.
- **Kit Charter is process authority:** `/Users/theophilebaudouin/Documents/devellopement/Go/KIT_CHARTER.md` governs every KitV2 and instruction-artifact change. If another artifact conflicts with it, the artifact must be corrected; the charter is not duplicated into every file.
- **Charter compliance is mandatory:** For every addition or modification, check permanent-context minimality, single source of truth, source/evidence traceability, raw validation output, independent fresh-context approval, deterministic gates, probe-suite status, anti-duplication checklist, approval boundary, and the charter's Definition of Done. Never present code-quality judgment as a question to the owner.
- **Charter maintenance:** Changes to `KIT_CHARTER.md` itself are structural and require explicit approval. Keep the charter as the process source of truth; record implementation decisions and audit findings in dated decision/plan artifacts rather than copying the charter into memory or other instruction files.
- **Knowledge lifecycle:** Problem → Research → Decision → Pattern → Snippet → Recipe → Template → Evaluation. Do not promote unsupported knowledge into the product.
- **Language (fundamental rule, 2026-08-05):** English is the mandatory language for every skill, instruction, and document in this repository — one unique language across the whole project (D-2026-08-05-21, supersedes D-2026-08-05-17). Translations preserve technical terms and intent, and stay as close to the original as possible.

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

2026-08-05 — **Metaprojet-only KitV2 audit workflow** : le prompt `.pi/prompts/kit-audit.md` vit à la racine du méta-projet et audite `KitV2/` sans modification. Il impose un inventaire complet daté et réconcilié fichier par fichier, des verdicts par dimension contre `KIT_CHARTER.md`, et une décision explicite `KIT` vs `META-PROJET` pour détecter la pollution du produit. `install.sh` n'extrait que `KitV2/`, donc ce prompt n'est pas livré au consommateur par construction.

2026-08-05 — **Intégration spec-driven-dev (mise à jour majeure, D-16…20)** :
le workflow de référence des transformations à grande échelle est la skill
`spec-driven-dev` (phases 0-6, LOCAL_ONLY, FR/EN) + `deep-discuss` ; la
chaîne `workflow-clarify → plan → tasks → implement → verify` est supprimée.
`go-code-review` intègre la discipline findings-first (review-spd). Règle
mémoire kit : vérifier les fichiers `.pi/memory/` présents (`Decisions.md`
absent au bootstrap Pi). Bornage : contrat Z12, kit-audit dimension C10,
S.U.P.E.R borné (les règles sourcées priment). Voir Decisions.md et le plan
`docs/plans/2026-08-05-spec-driven-dev-integration.md`.

## Verification status

2026-08-07 — CI offline-probe fix + kit audit wave + CI pytest fix: (1) offline bundle manifest drift (koanf/v2 v2.3.5→v2.3.6, x/text v0.28.0→v0.40.0) fixed + manifest↔go.mod drift gate added to validate-kitv2.py check_bundle (probe runs `go mod download <path>@<manifest-version>` with GOPROXY=off; local cache masked the stale pins); (2) kit audit KVA-101..105: broken prose id in go-contextual-worker.yaml, probes/README inventory 15→16 (ui-kit-sync missing) + probe-inventory cross-check in check_probe_runner, ui-kit/PIN.md update-path reworded (no metaproject-only surfaces), KitV2/.gitignore + .pytest_cache/, KVA-105 decision D-2026-08-07-09 (_kit-* files stay as declared kit machinery); new C12 prose-id gate in validate-cognitive.py (kind:domain:slug tokens must resolve; zero false positives, negative-tested, D-2026-08-07-10/11); stale test product_skills 72→73 fixed; (3) CI "router gate tests" failed (pytest never installed — stdlib-only requirements contract): switched to `python3 -m unittest discover` (all suites are unittest.TestCase) and wired the product-validator + structure.md-generator test suites into .github/workflows/ci.yml. Gate PASS before push (validators ×3, 60/60 pytest suites locally, router 22/22 + UI 9/9, gofmt/vet/lint 0, test -race, gosec 0, govulncheck 0, probes 16/16). Commits 3294a8e, 9381dce, a2a060f, 521968e, 20089b7 pushed to origin/main. Gotchas: offline manifest drift + CI pytest availability recorded.