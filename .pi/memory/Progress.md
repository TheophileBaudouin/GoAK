# Progress — Go Engineering Kit

Module ledger. State of every registry unit. Kept accurate at all times —
AGENTS.md forbids marking a module done before the validation suite passes.

Legend: `[x]` done (validation green) · `[ ]` planned · `[~]` in progress · `[!]` blocked · `[—]` explicitly out of scope

## KitV2 rules (loaded by concern)

- [x] `rules/core/philosophy/` — smallest justified design and mechanics vs behavior.
- [x] `rules/core/rules/universal/` — package names, contexts, errors, interfaces, docs.
- [x] `rules/core/errors/` — sentinel/typed/opaque decisions and handle-once rule.
- [x] `rules/core/concurrency/` — goroutine lifetimes, cancellation, bounded fan-out.
- [x] `rules/core/validation/` — golangci-lint, gosec, govulncheck.
- [ ] Semantic Resource Router — système de routage par index (2026-08-05)

## KitV2 recipes (Pi skills: SKILL.md + code)

- [x] `recipe-cli-minimal` — testable stdlib flag (NewFlagSet + ContinueOnError + explicit args); boundary vs cobra documented. Suite green.
- [x] `recipe-rest-chi` — chi v5 REST API (skill + test, suite green)
- [x] `recipe-sqlite-sqlc` — sqlc + modernc.org/sqlite (skill + test, suite green)
- [x] `recipe-worker-pool` — errgroup.SetLimit (skill + test, suite green)
- [x] `recipe-graceful-shutdown` — signal.NotifyContext + http.Server.Shutdown, signal wiring separated from orchestration for testability. Suite green.
- [x] `recipe-cli-interactif` — bubbletea v2 MVU, testable via handleKey(string) seam (skill + test, suite green)
- [x] `recipe-desktop-app` — wails v3 service logic, testable pure Go (no wails import; wiring documented) (skill + test, suite green)

## KitV2 reference projects

- [x] `ardanlabs-service` — extract-only layer/observability reference.
- [x] `pagoda` — extract-only SSR structure reference.
- [x] `go-starter` — extract-only, stagnant; re-verify before relying on it.

## KitV2 rules

- [x] `testing` — idiomatic Go testing (from quii/learn-go-with-tests)
- [x] logging (slog default, explicit-injection request-scoped pattern, Error=failure) + doc-comments (Go doc-comment convention, enforced via revive exported)

## KitV2 Pi prompt-templates (.pi/prompts/ — slash commands)

- [x] `/checklist-api` — REST API review checklist with evidence verdicts
- [x] `/checklist-release` — release checklist separating mechanics and behavior
- [x] `/workflow-memory` — initialize local consumer memory without inherited history
- [x] `/workflow-clarify` → `/workflow-plan` → `/workflow-tasks` →
      `/workflow-implement` → `/workflow-verify` — spec-driven workflow

## Deferred adapters (not implemented)

- [ ] Claude Code output adapter.
- [ ] Codex output adapter.
- [ ] Gemini CLI output adapter.

## Future deployment foundation (repository public ; module, CLI et pipeline de release toujours à venir)

- [ ] Publish the canonical repository and public Go module.
- [ ] Define release, versioning, checksums, and provenance policy.
- [ ] Package the future `gak` CLI and document its command contract.
- [ ] Define embedded asset packaging and content verification.
- [ ] Implement the deterministic installer and project manifest.
- [ ] Implement atomic update reconciliation and migration support.
- [ ] Define selected-agent adapter contracts and compatibility checks.
- [ ] Implement selected-agent runtime projections without a second runtime.
- [ ] Define modular knowledge packaging and dependency resolution.
- [ ] Add installer, update, migration, and removal evaluations/probes.

## KitV2 boundary correction (2026-08-03)

- [x] Research Pi-native loading: `AGENTS.md`, `.pi/settings.json`, direct
      `.pi/prompts/*.md`, recursive `.pi/skills/**/SKILL.md`; singular `.agent/`
      is not native.
- [x] Keep KitV2 as consumable product with `AGENTS.md` and `.pi/` resources.
- [x] Move metaproject evaluation methods to root `.agent/evaluations/`;
      KitV2 ships only product probes/checks, not evaluation governance.
- [x] Remove KitV2 `.agent/`, `tools.yaml`, and shipped evaluation governance.
- [x] Trusted Pi discovery runtime smoke returned the exact sentinel from a
      temporary consumer copy; individual skill invocation remains separate.

## Kit v1 deletion (2026-08-03)

- [x] Read-only inventory and independent risk review completed.
- [x] Obsolete v1-only plans, research, and evidence retired; current KitV2
      synthesis is `docs/research/2026-08-03-final-kitv2-synthesis.md`.
- [x] Atomic deletion plan recorded in `docs/plans/2026-08-03-kitv1-deletion.md`.
- [x] Deletion approval recorded in `.pi/memory/Decisions.md`.
- [x] External archive, checksum, and restore drill passed.
- [x] KitV2 validator and metaproject harness are self-contained.
- [x] CI/dependabot point to KitV2 and the pre-deletion KitV2 gate passes.
- [x] Active references and KitV2 module identity reconciled.
- [x] Delete the archived former product only after the final pre-delete scan and archive checksum.
- [x] Post-deletion KitV2 validation and active-reference scan.
- [x] Memory synchronized with the current KIT_CHARTER.md: artifact graph,
      metadata, relationships, lifecycle, ownership, and gates verified.

## Current phase

- [x] Phase 1: structure + memory + toolchain
- [x] Phase 2: deep research and admission gate
- [x] Phase 3: initial recipes, libraries, and checklists
- [x] Phase 4: full validation suite green
- [x] Phase 5: Pi-native skills, prompts, and settings
- [x] Phase 6: separated metaproject root from the consumable product
- [x] Phase 7: added stdlib CLI/shutdown recipes
- [x] Phase 8: candidate admission, core validation skills, libraries, and reference extracts
- [x] Phase 9: interactive CLI and desktop service recipes
- [x] Phase 10: sourced agent prompting/skills/spec-driven rewrite, exact skill-name migration, and consumer-memory separation
- [x] Fresh consumer-runtime check: invoke prompts/skills from a new project and execute recipe scenarios
- [x] Deferred public-distribution infrastructure: secret scanning, SARIF/SLSA, release/versioning, dedicated adapters
- [x] Bootstrap CLI and agent-runtime architecture — research `.pi`/`.agent`, record canonical CLI distribution, runtime, adapter, module, and deterministic-installation design; no implementation
- [ ] Relaunch external research on Pi-native skills, workflows, and kit maintenance
- [ ] Re-run blocked recipe and Pi prompt/template reference audits with fresh specialized sub-agents before claiming full instruction audit completion
- [ ] Produce the missing synthesis plan after all component-family research reports are available
- [x] Design cognitive architecture for offline official Go source retrieval and toolchain capabilities — graph, context policy, source transformations, and subagent contracts validated
- [x] Implement self-contained pinned official-source bundle and deterministic offline resolver (Phase 1-2) — manifest, checksums, bounded lookup, local toolchain/module resolution, tests, and probe green
- [x] Integrate offline resolver into standalone KitV2 (Phase 3) — product capability, validators, metadata, bundle, and five probes green
- [x] Integrate Pi retrieval workflows and consumer memory refresh rules (Phase 4) — load-on-demand skill and metadata-first prompts shipped
- [x] Reconcile cognitive-OS graph integrity and validator coverage — source target statuses, canonical toolchain vocabulary, self-contained knowledge metadata checks, and offline evidence in `docs/evidence/2026-08-03/cognitive-osi-reconciliation/`
- [x] Audit architecture and apply minimal corrections — product graph IDs, standalone relationship resolution, documentation boundary cleanup, and canonical universal-rule reference; evidence in `docs/evidence/2026-08-03/architecture-audit-minimal-corrections/`
- [x] Audit referenced technology documentation — metaproject-only coverage registry, official source cache units, exact versions/dates/licenses, and validator enforcement in `.agent/cognitive/technology-documentation.yaml`
- [x] Integrate source points 3–4 — Viper v1.21.0, Koanf v2.3.5, and Cobra v1.10.2 recipes/catalogs, pinned dependencies, offline module allowlist, and five green probes; evidence in `docs/evidence/2026-08-03/config-cli-integration/`

## Completed maintenance

- [x] Pi-native skill layer: four reusable skills added under `KitV2/.pi/skills/`.
- [x] KIT_CHARTER correction wave: clarified the universal rules boundary,
      added the approved four probes under `KitV2/probes/`, corrected root AGENTS.md
      drift and duplication, added deterministic instruction validation, and captured
      evidence. Remaining PARTIAL: no Git repository for VCS versioning and no
      real non-probe consumer-project maturity evidence.

## Blocked

- (none)

## Completed (this session)

- [x] Terminer l'audit d'intégration des 6 ressources Niveau B (GORM, Fiber, Kafka, RabbitMQ, Resty, Cookiecutter) + audit global du registre : 21 entrées Source conditionnelles ajoutées (6 Niveau B + 15 entrées non classées du corps), matrice de couverture 59/59, gate complète PASS, evidence docs/evidence/2026-08-03/b-resource-integration-audit.md, registre non modifié.
- [x] Corriger les skill conflicts Pi du benchmark : suppression des 5 placeholders .md vides de rules/ (architecture, go-style, performance, security, testing), check validateur « aucun .md vide » dans validate-kitv2.py (test négatif vérifié), ruff I001 sur le validateur, gate PASS, push main 0399cdd, tag v2.1.0 déplacé sur le commit corrigé, tarball v2.1.0 vérifié sans .md vide.
- [x] Ajouter l'écosystème Charm au registre des sources : 12 libs Go retenues (bubbletea, bubbles, lipgloss, glamour, huh, log, wish, ssh, harmonica, sequin, colorprofile, keygen), section #21 + Niveau A/B, apps humaines et libs pré-1.0/expérimentales exclues (crush, gum, glow, vhs, fantasy, catwalk, ultraviolet, x…), modules vérifiés via go.mod (vanity charm.land), evidence docs/evidence/2026-08-04/charm-ecosystem-registry/evidence.md.
- [x] Audit de gouvernance complet du Kit (phase 1) : rapport docs/research/2026-08-04-kit-audit-governance.md — audit des 12 zones + racine, 17 sources externes vérifiées (agentskills spec, Anthropic skill best-practices, Google Agent Skills governance, Red Hat ACE pitfalls, obra/superpowers, write-gate kkrlstrm, SemVer skills), vision globale, architecture cible, plan de 14 contrats MetaProjet (C0-C2, Z1-Z10, A1, N1) et 10 décisions requises. Aucun fichier d'instruction final créé (phase 2).
- [x] Phase 2 gouvernance exécutée : 15 contrats MetaProjet créés (.agent/kit-governance/ : C0, C1, C2, Z1-Z10, A1, N1 + README index), nettoyages approuvés exécutés (suppression embeddings/, tools/analyzers/, templates/api-service/ ; renommage rules/core/rules/universal → rules/core/universal ; README knowledge/debugging/ ; squelettes templates marqués legacy), politique templates MIT documentée (jamais agent-écrit), frontmatter des 5 skills .pi/skills/ complété (category: workflow), gate complète PASS (validateur 45 skills, gofmt, vet, go test -race, lint 0, gosec 0, govulncheck, probes 5/5), revue fresh-context REQUEST-CHANGES → 2 blocages corrigés (fermetures Markdown 7 contrats, évidence+mémoire) + nits intégrés, evidence docs/evidence/2026-08-04/kit-governance-phase2/, plan docs/plans/2026-08-04-kit-governance-phase2.md.

## KitV2 knowledge catalogs

- [x] `chi` — go-chi/chi v5
- [x] `sqlc` — SQL→Go code generation
- [x] `modernc-sqlite` — pure-Go SQLite driver
- [x] `testify` — assert/require/mock (stdlib-first)
- [x] `validator` — go-playground/validator (⚠ maintainer-call watch)
- [x] `koanf` — config, viper alternative
- [x] `templ` — type-safe HTML templates
- [x] `req` — imroc/req (**extract-only**: global-state API)
- [x] Enrichir le registre des sources critiques avec les références officielles Go, modules/toolchains, tests, sécurité et outils de validation; revue indépendante PARTIAL et VCS BLOCKED.
- [x] Terminer l’audit séquentiel des 34 ressources Niveau S/A du registre; toutes vérifiées, intégrations dédiées ajoutées, validation KitV2/tests/format/probes PASS; VCS evidence BLOCKED.
- [x] Promouvoir l'écosystème Charm en knowledge catalogs : 12 SKILL.md sous knowledge/catalogs/libraries/ (bubbletea, bubbles, lipgloss Niveau A ; glamour, huh, log, wish, ssh, harmonica, sequin, colorprofile, keygen Niveau B), EXPECTED_PRODUCT_SKILLS 33→45, gate complète PASS (validators, gofmt, vet, lint, tests, gosec, 4 probes), evidence docs/evidence/2026-08-04/charm-ecosystem-registry/evidence.md.
- [x] Remplir knowledge/anti-patterns/ : 47 anti-patterns YAML (go 14, database 6, http 4, architecture 6, testing 4, security 4, observability 2, cli 1, messaging 3, config-cache 3) avec contrat de graphe + symptom/detect/problem/fix/when_ok + sources primaires vérifiées, rapport docs/research/2026-08-04-anti-patterns-research.md, plan docs/plans/2026-08-04-anti-patterns.md, gate complète PASS, revue fraîche-contexte APPROVE-WITH-NITS intégrée, evidence docs/evidence/2026-08-04/anti-patterns/evidence.md.
- [x] Remplir knowledge/patterns/ : 38 patterns positifs YAML (go 8, concurrency 3, resilience 3, http/api 4, database 4, architecture 2, testing 4, observability 2, cli 1, messaging 3, config-cache 2, security 2) avec schéma positif problem/context/solution/benefits/costs/related, ids pattern:<domaine>:<slug> (séparés de pattern:antipattern:*), homologues anti-patterns référencés, 50 URLs vérifiées 200, rapport docs/research/2026-08-04-patterns-research.md, plan docs/plans/2026-08-04-patterns.md, gate complète PASS, revue fraîche-contexte intégrée (2 URL mortes corrigées), evidence docs/evidence/2026-08-04/patterns/evidence.md.

## Meta-project / KitV2 separation

- [x] KitV2 is the only consumable product; the root is the metaproject.
- [x] Root `.pi/memory/` is the only authoritative metaproject memory.
- [x] `KitV2/.pi/` ships reusable settings, prompts, and Pi-native skills; no
      pre-populated consumer memory is committed.
- [x] `KitV2/.pi/prompts/workflow-memory.md` instructs fresh consumer projects to initialize local memory without copying metaproject history.
- [x] Move source registry and prompt/skill source records to root .agent/sources/; keep source inputs out of KitV2 unless separately admitted.

## Infrastructure

- [x] KitV2 product tree, module `go-agent-kit-v2`, and native `.pi/` resources.
- [x] Validation toolchain installed: gofmt, go vet, golangci-lint v2, gosec, govulncheck.
- [x] Metaproject memory: root `.pi/memory/` Brief / Progress / Gotchas / Agent / Decisions.
- [x] Publier le dépôt Git public du metaprojet — remote <https://github.com/TheophileBaudouin/GoAK>, branche main, commit initial 690aa35 (295 fichiers, 17 334 insertions), push OK après gh auth setup-git.
s/workflow-memory.md` instructs fresh consumer projects to initialize local memory without copying metaproject history.
- [x] Move source registry and prompt/skill source records to root .agent/sources/; keep source inputs out of KitV2 unless separately admitted.

## Infrastructure

- [x] KitV2 product tree, module `go-agent-kit-v2`, and native `.pi/` resources.
- [x] Validation toolchain installed: gofmt, go vet, golangci-lint v2, gosec, govulncheck.
- [x] Metaproject memory: root `.pi/memory/` Brief / Progress / Gotchas / Agent / Decisions.
- [x] Publier le dépôt Git public du metaprojet — remote <https://github.com/TheophileBaudouin/GoAK>, branche main, commit initial 690aa35 (295 fichiers, 17 334 insertions), push OK après gh auth setup-git.
