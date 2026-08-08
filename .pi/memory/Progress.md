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

- [~] Reconstruction 2.4.0 des dix recipes historiques — contrats publics à
      préserver, probes dédiées, génération sqlc réelle et sources fraîches ;
      worktree 2.3.0 conservé sans reset.

- [x] `recipe-auth-session-scs`, `recipe-auth-jwt`,
      `recipe-observability-slog-expvar`, `recipe-openapi-validation` — lot
      2.3.0 livré avec tests, probes et gate complète PASS.
- [!] `recipe-postgres-pgx` — code, migrations et test réel tagué livrés ;
      scénario PostgreSQL observé BLOCKED tant qu'une `DATABASE_URL` jetable
      autorisée n'est pas fournie. Revue fresh-context également BLOCKED par la
      limite de service du réviseur, sans validation fictive.

- [x] `recipe-cli-minimal` — testable stdlib flag (NewFlagSet + ContinueOnError + explicit args); boundary vs cobra documented. Suite green.
- [x] `recipe-rest-chi` — chi v5 REST API (skill + test, suite green)
- [x] `recipe-sqlite-sqlc` — sqlc + modernc.org/sqlite (skill + test, suite green)
- [x] `recipe-worker-pool` — errgroup.SetLimit (skill + test, suite green)
- [x] `recipe-graceful-shutdown` — signal.NotifyContext + http.Server.Shutdown, signal wiring separated from orchestration for testability. Suite green.
- [x] `recipe-cli-interactive` — bubbletea v2 MVU, testable via handleKey(string) seam (skill + test, suite green)
- [x] `recipe-desktop-app` — wails v3 service logic, testable pure Go (no wails import; wiring documented) (skill + test, suite green)

## KitV2 rules

- [x] `testing` — idiomatic Go testing (from quii/learn-go-with-tests)
- [x] logging (slog default, explicit-injection request-scoped pattern, Error=failure) + doc-comments (Go doc-comment convention, enforced via revive exported)

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
- [ ] Placement analysis of the 26-technology catalog on the existing architecture (research only, no product change)
- [ ] Admit catalog wave from technology KB: 5 libraries (fyne, go-git, mcp-go-sdk, ristretto, bleve) + 4 pre-1.0 pointers (eino, playwright-go, sqlite-vec, tree-sitter) + go/ast stdlib; registry sections 24-28; gate PASS

## Blocked

- (none)

## Completed (this session)

## Completed maintenance

- [x] [2026-08-08] Onboarding fixes (D-2026-08-08-18, user-reported): (1)
      `/goak` renamed to `/goak-help` everywhere (prompt file, guide, banner,
      AGENTS.md, validator, tests, Z8 naming exception, kit-audit C18,
      instructions.md, Agent.md, router entry `goak-help`); (2) banner is
      NO LONGER a persistent widget — `kit-onboarding.ts` now appends one
      chat-transcript entry per session (`pi.appendEntry` +
      `registerEntryRenderer`, content from `.pi/onboarding/banner.md`),
      startup|reload only, idempotent (same session never duplicated),
      silent headless/missing-file — verified by a behavioral mock test
      (startup append / reload no-dup / headless no-op / renderer / missing
      file); banner content simplified to user-facing one-liners;
      (3) skill-conflict fix: `pi` from the kit root reported
      "[Skill conflicts] recipes/README.md — description is required" (Pi
      loads root-level .md of declared skill dirs without a root SKILL.md as
      skills) — fixed with frontmatter (name + description +
      disable-model-invocation: true) + new validator gate
      `check_declared_skill_dirs` (+2 tests); verified with Pi's own skills
      loader: diagnostics NONE, `recipes` skill loads, 15 recipe skills
      intact. Gate PASS (validators ×3, 29 unit tests, scenarios 23/23 +
      UI 11/11), consumer smoke: `/goak-help` expands → agent reads the
      guide.
- [x] [2026-08-08] Consumer onboarding & knowledge system (D-2026-08-08-14..17):
      shipped user guide `KitV2/.pi/docs/GOAK.md` (Get Started + deep usage,
      LLM-native, decision tables, verified commands) + `/goak-help` prompt
      (`.pi/prompts/goak-help.md`, orders the agent to read the local guide) +
      onboarding banner (`.pi/extensions/kit-onboarding.ts` renders
      `.pi/onboarding/banner.md` as a session-start widget on
      startup/reload) + marker-delimited "User guide" section in
      KitV2/AGENTS.md; validator `check_consumer_onboarding` (+5 unit
      tests), kit-audit dimension C18 + Phase E row, Z8 roles table
      (docs/onboarding/extensions) + /goak-help naming exception, Z9 §3.5
      markers rule, .agent/instructions.md row, root AGENTS.md +
      Agent.md maintenance rules, router regenerated (prompt 3→4, index
      287, version 2.6.0). Gate PASS (validators ×3, unit tests 27,
      scenarios 23/23 + UI 11/11, go gate, lint/gosec). Consumer Pi smoke
      verified end-to-end: `/goak-help` expands → agent reads
      .pi/docs/GOAK.md → faithful explanation. Incident: an external
      git-driven process truncated ~909 tracked files to 0 bytes (mode 000)
      at 14:18:46 — recovered via `git restore --source=HEAD`; untracked
      deliverables survived. Plan:
      docs/plans/2026-08-08-consumer-onboarding-system.md.
- [x] [2026-08-08] Merged root AGENTS.md + release v2.6.0 (owner mission): KitV2/AGENTS.md rewritten as the single agent file — merges the pinned ui-kit/AGENTS.md instructions into a 'UI work — Wails projects' section (agent-instructions skill discipline; EVERY instruction from both files preserved, adapted not deformed) with a sha256 checksum marker; the re-sync helper now refuses to finish when the marker drifts (merged prose + marker must be updated at every SDK update — Z13 §4, update-ui-kit prompt, idempotent re-sync + stale-marker tripwire tested); pi-lens autofix normalized bullets, Stack line fixed. Release v2.6.0: version bumped across manifest/capabilities/install.sh/README (router meta regenerated), full gate PASS (validators, Go 22/22, UI 11/11, 44 router tests, lint/gosec/govulncheck 0, probes), installer simulated (extraction + validator + probes + ui-kit + settings fused + no .agent leak) and verified end-to-end after push. Decisions D-2026-08-08-04/05.

- [x] [2026-08-07] ui-agent-kit native integration (D-2026-08-07-04..06, owner decision): first-class `KitV2/ui-kit/` zone (pinned `sdk/` mirror @ f9bdd9b = npm 0.1.0 tarball, AGENTS.md verbatim, PIN.md), Z13 contract + governance index, manifest/capabilities (capability `ui-kit`, coverage.ui_kit_skills=7, probes 16), validator (Pi-compat frontmatter, disjointness, node-free UI scenarios) + 8 tests, `search_ui_kit_resources` tool (separate corpus, shared scoring, on-the-fly index from `shared/kit-ui-router-core.ts`), `ui-kit/scenarios.json` 9/9 under the real scoring (gate `run_ui_scenarios.mjs` + negative tripwire), shared modules relocated to `.pi/extensions/shared/` (pre-existing Pi loader fix, headless smoke OK), `tools/sync-ui-kit.sh` Wails-only + probe 16/16, manual gated metaproject re-sync; full gate PASS (validators, Go 22/22, UI 9/9, 38 tests, gofmt/vet/lint/gosec 0, govulncheck 0, probes 16/16), consumer Pi smoke: 2 tools registered, UI query → UI corpus, Go queries → Go corpus with no ui-kit/ paths; plan docs/plans/2026-08-07-ui-agent-kit-integration.md, evidence docs/evidence/2026-08-07/ui-agent-kit-integration/.
- [x] [2026-08-07] macOS Computer Use resources (pattern + fiche, D-2026-08-07-01..03) : prémisse « règle anti-CGO/Objective-C » vérifiée fausse (zéro-CGO = préférence de sélection, pas une règle) → guidance positive dans le pattern knowledge/architecture/macos-computer-use.yaml (AXUIElement primaire, RobotGo exécution, ScreenCaptureKit perception, caveat darwinkit stale 2024-07) ; RobotGo admis en fiche vétée catalogs/libraries/robotgo/SKILL.md (v1.0.2 stable 2026-03, macOS cgo par défaut / purego via -tags purego, 9 critères réels) ; router régénéré 280, capabilities 73/44, gate complet PASS (validators, 22/22 scénarios, gofmt/vet/lint 0, test race, gosec 0, govulncheck 0, probes 15/15) ; revue fresh-context APPROVE-WITH-NITS ; plan docs/plans/2026-08-07-computer-use-macos.md, évidence docs/evidence/2026-08-07/computer-use-macos/.

- [x] Pi-native skill layer: four reusable skills added under `KitV2/.pi/skills/`.
- [x] KIT_CHARTER correction wave: clarified the universal rules boundary,
      added the approved four probes under `KitV2/probes/`, corrected root AGENTS.md
      drift and duplication, added deterministic instruction validation, and captured
      evidence. Remaining PARTIAL: no Git repository for VCS versioning and no
      real non-probe consumer-project maturity evidence.
- [x] Audit-fix wave KVA-001…KVA-011 (2026-08-05, produit 2.4.1)
- [ ] [2026-08-05] Passe méta-projet « durcissement gouvernance » (5 findings Rodin fermés sans toucher KitV2) : C2/Z4/Z3/Z1 (déclenchement revue inter-fichiers par dates + tripwire, D-11), roadmap snippets déclarée saine (D-12), philosophie → Option 3 « naviguer par la raison » réponse Marie (D-13), dossier desktop-app aucun candidat Wails conforme + précision Z5 (D-14), principe instructions absolues étendu + registre + spec porte Pi (D-15) ; kit-audit phases B/C4/C9/§5-E évolué ; gates méta-projet PASS ; revue fresh-context APPROVE-WITH-NITS intégrée ; actions KitV2 en attente documentées (plan 2026-08-05-metaproject-governance-hardening.md).
- [ ] [2026-08-05] Intégration spec-driven-dev (mise à jour majeure, D-16…20) : skill spec-driven-dev (phases 0-6 + 4 références + 5 templates, FR/EN, LOCAL_ONLY), skill deep-discuss, go-code-review augmenté (findings-first), ancienne chaîne workflow-clarify/plan/tasks/implement/verify supprimée (router régénéré prompt 8→3, skill 6→8), règle mémoire kit (vérifier les fichiers .pi/memory, Decisions.md absent au bootstrap), contrat Z12 + kit-audit C10, frontière S.U.P.E.R vs doctrine Go encodée ; analyse docs/research/2026-08-05-spec-driven-dev-analysis.md.
- [x] [2026-08-06] Permanent-audit remediation (KVA-101..110 closed): language wave EN executed (15 recipes, 93 pattern/anti-pattern YAML, 43 fiche files, mcp-server-shape — 0 French residual, accent-scan verified), validator snippet date-chain check implemented + 11/11 unit tests, known_limits structured (pi-workflows → partial), TEMPLATES.md desktop-app roadmap, .agent/instructions.md registry expanded + interpretation decided, router regenerated (253), full gate green (validators, strict catalog, Go gate, 15/15 probes, 3 templates), N1 §4 updated, plan docs/plans/2026-08-06-language-wave-and-fix-pipeline.md.
- [x] [2026-08-06] structure.md contract + governance hardening (RDN-003, metaproject only): structure.md defined as Layer 5.1 (reading map, generation-first, drift gate), 4 verifiable governance constraints added to charter §16.1 (relation resolvability, router sole entry, category justification, absolute-instruction validation), kit-audit dimensions C11-C15 + Phase E rows added, decisions D-2026-08-06-07..09 recorded, gotchas on Go dir role metadata + generated-docs-truth scope recorded, fresh-context review APPROVE-WITH-NITS (nits applied), plan docs/plans/2026-08-06-structure-contract-governance.md, research docs/research/2026-08-06-structure-md-generation.md, KitV2 untouched; KitV2 implementation deferred to next kit-audit pass.
- [x] [2026-08-06] KitV2 AGENTS.md Z9-conformity correction: Source-of-truth list → Z9 §2.1 table (zone → mission → pointer, all pointers verified), Limits states uncovered domains (Z9 §2.5, aligned example), §Limits absolutes registered guidance-only in .agent/instructions.md (§16.1.4), stale critical-report proposals rejected (deleted workflow chain, stale skill inventory, metaproject cognitive imports); validators PASS, fresh review REQUEST-CHANGES → fixed → APPROVE, D-2026-08-06-10 recorded.
- [ ] [2026-08-06] Ultra-specialized Go skills wave (25 artifacts): 11 stdlib pointers (json/crypto/io/io-fs/regexp/time/slices/net-url/sync-atomic/go-generate/cross-compilation), 7 patterns (zero-value, receivers, generics, internal/, channel ownership, semantic import versioning, black-box tests), 4 anti-patterns (reflection overuse, weak randomness, timing-unsafe comparison, receiver closes channel), 2 sources (benchmarking, gc-guide), 1 registry rule (naming) — all sourced & URL-verified; naming rule elaborates universal (no dup); go-command selection narrowed; router 253→278, product skills 71→72; gate PASS (validators, cognitive, probes 15/15, gofmt/vet/test/lint); fresh review REQUEST-CHANGES→fixed; plan docs/plans/2026-08-06-ultra-specialized-go-skills.md, report docs/research/2026-08-06-ultra-specialized-skills-report.md.
- [ ] [2026-08-06] Routing guarantee wave (product 2.5.0, owner decisions 2026-08-06): routing-quality gate (scenarios.json 22 scénarios, scoring runtime partagé kit-resource-router-scoring.ts importé par l'extension ET le gate node .agent/router/run_scenarios.mjs — zéro divergence, 22/22 PASS), surface prompt réduite (catalogs retirés de .pi/settings.json → règles+recipes visibles, fiches routables), mandat renforcé (AGENTS.md « routing is mandatory » + promptGuidelines du tool nommant les patterns par défaut), validate-kitv2 check_router_scenarios (schéma+linkage, node-free), tests 25 passed, gate complet PASS (validators, probes 15/15, gofmt/vet/lint), revue fresh-context APPROVE (3 nits corrigés), plan docs/plans/2026-08-06-routing-guarantee.md.
- [ ] [2026-08-06] Router maintainability hardening (metaproject rules): Z11 contract updated with the routing-quality system (roles table: scenarios.json authored contract, shared scoring core, two-layer gate; rules: single scoring implementation, two-layer verification, scenario admission "must be able to fail", scoring evolution protocol, node ≥ 23.6; anti-patterns: decorative scenarios, second scoring copy), negative gate tests added proving the tripwire fires (unreachable expectation → exit 1, stale id → exit 1 — run_scenarios.mjs gains optional scenarios path arg), Decisions.md D-2026-08-06-11 recorded, Agent.md new section "Router & scoring maintenance", gate 22/22 PASS, metaproject tests 27 passed, validators PASS.
- [ ] [2026-08-06] Audit-fix wave + release v2.5.0 (KVA-101..110) : structure.md mechanism (Layer 5.1) implémenté (tools/generators/structure_md.py + 3 structure.md + hook validateur + champs template.yaml), registry instructions.md complété (2 carriers routage), scan .agent/ dans le produit (KVA-102), lexeme MANDATORY ↔ registry (KVA-103), PyYAML épinglé (requirements.txt + CI), CI = gate local complet (validators + build_index + run_scenarios + probes, coverage hors probes 81.5% ≥ 70%), tests coverage sqlite/offline/postgres, README anglais v2.5.0 + install.sh ref, commits 8757f6d/ced6285/685e74b, tag v2.5.0 poussé, install vérifiée de bout en bout (validateur PASS, probes 15/15, zéro fuite .agent/), revue fresh-context APPROVE après fixes.
- [ ] [2026-08-07] CI offline fix + audit wave KVA-101..105 + CI pytest fix : manifest offline aligné sur go.mod + gate de dérive manifest↔go.mod (check_bundle), prose-id gate C12 dans validate-cognitive.py, inventaire probes README 16 (ui-kit-sync) + cross-check check_probe_runner, PIN.md rewording, .pytest_cache gitignoré, décision KVA-105 (D-2026-08-07-09), tests stale 72→73 ; CI "router gate tests" passe à unittest stdlib (pytest jamais installé en CI) + suites validateurs produit et structure.md câblées dans ci.yml. Gate complet PASS, commits 3294a8e/9381dce/a2a060f/521968e/20089b7 poussés.
- [x]  [2026-08-08] ui-agent-kit re-sync + single registration point (owner mission): re-pinned zone to cd00eb5d (0.1.1, agent chat + assistant-ui wave, +5392 lines, copy-rules 4th rule, npm byte-identity verified); root KitV2/.pi/settings.json fused (../ui-kit/skills additive) — nested ui-kit/.pi/settings.json dead (deleted + excluded from re-syncs); Z13 updated (rules 1-9, single registration point, §9 past-mistake reminder, catalog-table pattern), capabilities.yaml + AGENTS.md reworded, Decisions.md D-2026-08-08-01..03; kit-audit C16 read-only ui-kit dimension + Phase E row; check_ui_kit_registration validator gate + 4 unit tests; routing fixes (Z11 protocol): off-domain rejection on raw vocabulary + components-index catalog table indexed → UI gate 11/11 (2 new scenarios), Go 22/22, 44 router tests incl. tripwire; consumer Pi smoke (pi -p -a): 7 UI skills discovered, Go router no ui-kit path, UI router agent-chat first no outside path; full gate PASS (validators ×3, lint/gosec/govulncheck 0, probes 16/16); plan docs/plans/2026-08-08-ui-kit-resync-and-registration.md, evidence docs/evidence/2026-08-08/ui-kit-resync-and-registration/; commits d15574f, edc52c1, e4bf4fd, f5bc710.
- [x]  [2026-08-08] ui-kit sync script hardening + pi-lens clean (owner request): .agent/sync-ui-kit-from-upstream.sh corrected — pytest→stdlib unittest (CI parity, gotcha 2026-08-07), FULL GATE now actually runs golangci-lint/gosec/govulncheck + exports GOPATH/bin PATH, dead .pi dir excluded from BOTH diff and rsync (diff --exclude matches basenames only — .pi/settings.json pattern never matched, real bug caught by idempotent re-sync test), rollback guards on copy-rules gen + PIN update, PIN contains new SHA check, --check now reports upstream HEAD drift (git ls-remote, graceful offline), shellcheck-clean (SC1007/2155/2016/2086). Pi-lens blocking errors eliminated: triple-slash `/// <reference lib=es2022 />` + `/// <reference path=types/pi-env.d.ts />` in all 4 extension .ts files (LSP inferred project couldn't see the tsconfig; tsc already passed, now LSP 0 errors). Full idempotent re-sync cd00eb5d → FULL GATE PASS; consumer Pi smoke (pi -p -a): UI router agent-chat/components-index/screens. Memory: Agent.md rule "Sub-agent delegation goes through pi-subagents ONLY" (never intercom/supervisor for delegation; pi -p smoke tests are environment tests, not delegation); gotcha: memory_update rule_add silently no-ops when the agent_section title doesn't exist ("Absolute Rules" absent from Agent.md) — verify on disk after every memory_update.
- [ ] [2026-08-08] Protocole workspace-init (Z14) : skill kernel-first day-0 avant spec-driven-dev — contrats/validators/probes/evidences en place
- [ ] [2026-08-08] Nettoyage autonomie produit : ~30 références métaprojet retirées de KitV2/, gate check_no_metaproject_paths étendu (9 marqueurs), fix unittest.main() dormant (7 tests réactivés), Z9 §3.2 généralisé

## KitV2 reference projects

- [x] `ardanlabs-service` — extract-only layer/observability reference.
- [x] `pagoda` — extract-only SSR structure reference.
- [x] `go-starter` — extract-only, stagnant; re-verify before relying on it.
- [x] Remplacer les 7 scaffolds legacy de templates par 3 templates MIT sourcés (REST, CLI, worker), retirer les shapes sans source conforme, mettre à jour le validateur, router et evidence (2026-08-05).

## KitV2 Pi prompt-templates (.pi/prompts/ — slash commands)

- [x] `/checklist-api` — REST API review checklist with evidence verdicts
- [x] `/checklist-release` — release checklist separating mechanics and behavior
- [x] `/workflow-memory` — initialize local consumer memory without inherited history
- [x] `/workflow-clarify` → `/workflow-plan` → `/workflow-tasks` →
      `/workflow-implement` → `/workflow-verify` — spec-driven workflow
- [x] [2026-08-05] Add metaproject-only /kit-audit prompt: read-only complete KitV2 inventory, charter/type/source/duplication/language/validation checks, and meta-project-versus-Kit pollution classification; prompt not shipped by install.sh.

- [x] Terminer l'audit d'intégration des 6 ressources Niveau B (GORM, Fiber, Kafka, RabbitMQ, Resty, Cookiecutter) + audit global du registre : 21 entrées Source conditionnelles ajoutées (6 Niveau B + 15 entrées non classées du corps), matrice de couverture 59/59, gate complète PASS, evidence docs/evidence/2026-08-03/b-resource-integration-audit.md, registre non modifié.
- [x] Corriger les skill conflicts Pi du benchmark : suppression des 5 placeholders .md vides de rules/ (architecture, go-style, performance, security, testing), check validateur « aucun .md vide » dans validate-kitv2.py (test négatif vérifié), ruff I001 sur le validateur, gate PASS, push main 0399cdd, tag v2.1.0 déplacé sur le commit corrigé, tarball v2.1.0 vérifié sans .md vide.
- [x] Ajouter l'écosystème Charm au registre des sources : 12 libs Go retenues (bubbletea, bubbles, lipgloss, glamour, huh, log, wish, ssh, harmonica, sequin, colorprofile, keygen), section #21 + Niveau A/B, apps humaines et libs pré-1.0/expérimentales exclues (crush, gum, glow, vhs, fantasy, catwalk, ultraviolet, x…), modules vérifiés via go.mod (vanity charm.land), evidence docs/evidence/2026-08-04/charm-ecosystem-registry/evidence.md.
- [x] Audit de gouvernance complet du Kit (phase 1) : rapport docs/research/2026-08-04-kit-audit-governance.md — audit des 12 zones + racine, 17 sources externes vérifiées (agentskills spec, Anthropic skill best-practices, Google Agent Skills governance, Red Hat ACE pitfalls, obra/superpowers, write-gate kkrlstrm, SemVer skills), vision globale, architecture cible, plan de 14 contrats MetaProjet (C0-C2, Z1-Z10, A1, N1) et 10 décisions requises. Aucun fichier d'instruction final créé (phase 2).
- [x] Phase 2 gouvernance exécutée : 15 contrats MetaProjet créés (.agent/kit-governance/ : C0, C1, C2, Z1-Z10, A1, N1 + README index), nettoyages approuvés exécutés (suppression embeddings/, tools/analyzers/, templates/api-service/ ; renommage rules/core/rules/universal → rules/core/universal ; README knowledge/debugging/ ; squelettes templates marqués legacy), politique templates MIT documentée (jamais agent-écrit), frontmatter des 5 skills .pi/skills/ complété (category: workflow), gate complète PASS (validateur 45 skills, gofmt, vet, go test -race, lint 0, gosec 0, govulncheck, probes 5/5), revue fresh-context REQUEST-CHANGES → 2 blocages corrigés (fermetures Markdown 7 contrats, évidence+mémoire) + nits intégrés, evidence docs/evidence/2026-08-04/kit-governance-phase2/, plan docs/plans/2026-08-04-kit-governance-phase2.md.
- [ ] Compléter le graphe de connaissance pour les 29 bibliothèques du catalogue (manques réels uniquement) : 14 artefacts YAML sourcés ajoutés (anti-patterns sec-ip-trust, sec-cswsh, db-codegen-dynamic-queries, sec-ssh-host-key-reuse ; security ssh-server-security, ssh-key-generation, websocket-security, mcp-tool-security, input-validation ; performance search-index-merge, template-compiled-rendering ; observability ssh-metrics ; architecture mcp-server-shape ; stdlib go-html-template), INDEX.md corrigé (domaine cloud fantôme retiré, observability ajouté), router régénéré (231 ressources), gate complète PASS (validators, gofmt, vet, lint 0, tests, gosec 0, govulncheck préexistant non appelé, probes 5/5), evidence docs/evidence/2026-08-04/knowledge-completion/.
- [ ] Durabiliser la pipeline d'analyse de bibliothèques : contrat Z2 §9 (pipeline 9 étapes, admission manques réels, contrôles de sortie vérifiables) + N1 §3 (conventions YAML : URLs canoniques/échappement, langue, post-écriture) mis à jour, mémoire synchronisée (Agent.md « Library knowledge pipeline », Decisions.md, Brief.md, Gotchas.md), revue fresh-context APPROVE-WITH-NITS intégrée, gate PASS.
- [ ] Fiches de référence des 28 bibliothèques du catalogue : 6 sections décisionnelles ajoutées à chaque SKILL.md (Utiliser/Ne pas utiliser quand, Avantages, Inconvénients, Pièges connus, Sources vérifiées), placement contraint par la gouvernance (knowledge/catalogs = répertoire de skills Pi déclaré → fiche dans le SKILL.md), critiques multi-sources, revue fresh-context APPROVE-WITH-NITS intégrée (5 nits : Sources legacy supprimées cobra/koanf/viper, citation CVE validator, last-verified bumpés, N1 §4 reformulé, cross-refs A1+template), standard encodé N1 §4 + Z2 §9.2, gate PASS, évidence docs/evidence/2026-08-04/catalog-fiches/.
- [ ] Admettre google/adk-go en pointeur « à considérer » (décision utilisateur) : échoue 2 critères durs du portail (528 fichiers .go / ~129k LOC, couplage Google Cloud — précédent temporalio), pointeur YAML pointers/adk-go.yaml créé, registre sources §18 + Niveau B mis à jour, router régénéré (232), gate PASS.
- [ ] Survey bibliothèques Go multi-domain (recherche seule, aucune admission) : 31 découvertes, 18 analysées (GitHub API/OSV/Scorecard/proxy.golang), 8 approuvées + 1 avec WARNING (age, bbolt, compress, goldmark, pgx, minio-go, kin-openapi, testcontainers, certmagic), 7 refusées (maintenance : xxhash, msgpack, r3labs/sse, projets <12 mois), 6 à surveiller (otel, miekg/dns, oapi-codegen, goccy/yaml, joshuafuller/sse, promotions legacy). Rapport : docs/research/2026-08-05-go-library-survey.md. Intégration = décision à approuver (charte).
- [ ] Intégration des 9 bibliothèques approuvées du survey 2026-08-05 : fiches SKILL.md (age, bbolt, compress, goldmark, pgx, kin-openapi, minio-go, testcontainers-go, certmagic) au format N1 §4/A1 (minimal use compilés hors kit), 5 artefacts YAML knowledge (file-encryption, embedded-kv, compression-selection, sec-unsanitized-rendering, db-placeholder-cache-injection), EXPECTED_PRODUCT_SKILLS 51→60, capabilities 45→60/31→40, router 232→246, bump x/text (fix GO-2026-5970), gate complète verte (5 probes PASS, govulncheck 0), revue fresh-context APPROVE-WITH-NITS (6 nits corrigés), évidence docs/evidence/2026-08-05/library-integration/.
- [ ] Intégration auth 2026-08-05 : évaluation critique de 6 candidats + bonus (données GitHub/OSV/Scorecard), 2 fiches vétées (golang-jwt promotion + scs remplaçant gorilla/sessions), 2 pointeurs stdlib (x-crypto, x-oauth2), 2 artefacts (auth-session-vs-jwt pattern, sec-missing-csrf anti-pattern), 5 rejets loggés (gorilla/sessions, alice, authboss, gorilla/csrf, nosurf), legacy golang-jwt.yaml supprimé, EXPECTED_PRODUCT_SKILLS 60→62, router 246→251, gate verte (5 probes, govulncheck 0), revue fresh-context APPROVE-WITH-NITS (F1-F4+F6 corrigés), évidence docs/evidence/2026-08-05/auth-libraries/.

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
- [x] Admettre 5 pointeurs LLM/ML de référence (llama.cpp, MLX family, Outlines, DSPy, Langfuse)

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
