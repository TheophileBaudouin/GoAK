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

## Recipes prioritaires KitV2 (2026-08-05)

- Le lot 2.3.0 comporte exactement cinq recipes : sessions navigateur `scs`,
  JWT Bearer HS256, PostgreSQL `pgx` avec migrations externes, observabilité
  `slog`/`expvar`, et validation OpenAPI de requête et de réponse. Il privilégie
  deux frontières d'authentification explicites plutôt qu'une abstraction
  commune ou un framework.
- Les versions autorisées sont `scs/v2 v2.9.0`, `golang-jwt/jwt/v5 v5.3.1`,
  `pgx/v5 v5.10.0` et `kin-openapi v0.146.0`. `golang-migrate/migrate/v4
  v4.19.1` est admis comme CLI de déploiement après sa fiche dédiée, pas comme
  dépendance runtime ni mécanisme de migration au démarrage.
- Les métriques restent atomiques et exposées par `expvar` sur un listener
  d'administration privé. Aucun logger ne passe par `context.Context`, et
  OpenTelemetry/Prometheus ne sont pas ajoutés.
- La validation OpenAPI utilise un adaptateur explicite afin de borner et
  valider les réponses ; une fonction d'authentification non nulle est exigée.
  Aucun fail-open ni `NoopAuthenticationFunc` n'est admis.
- Testcontainers est différé : Docker/Podman est à la fois non autorisé et
  indisponible dans cet environnement. Son admission future exige une
  autorisation explicite, un runtime approuvé et l'exécution réelle du scénario
  avant activation ; aucun substitut simulé ne peut le déclarer couvert.
- Le compteur `product_skills` 2.3.0 est `71`, non `70` : le validateur dérive
  `13 rules + 15 recipes + 43 catalogues`. La gouvernance C1/C2 (compteurs
  dérivés et validés) prévaut sur le total incohérent de la demande.

## Reconstruction recipes historiques 2.4.0 (2026-08-05)

- Les dix recipes historiques sont reconstruites sans rupture de leurs chemins
  ni API Go publiques. Les ajouts de façades restent non cassants ; la TUI peut
  exposer `NewModel` car aucun symbole public précédent n'est retiré.
- Chaque recipe cœur possède sa probe locale dédiée. La probe combinée
  `worker-shutdown` est remplacée par `worker-pool` et `graceful-shutdown` :
  une réussite ne doit plus masquer l'échec d'une frontière distincte.
- Les seuls changements de dépendances autorisés sont l'alignement de versions
  déjà admises (`koanf v2.3.6`, `modernc.org/sqlite v1.56.0`) après recherche
  primaire et gate complète. `sqlc v1.31.1` est utilisé comme CLI ponctuelle,
  sans ajout au module runtime.
- Wails v3 reste une intégration alpha documentée et non compilée. Le package
  Go de service, sans import runtime Wails, est le périmètre testable du kit ;
  GUI, CGO et build Wails réel restent hors périmètre.

- 2026-08-02 — The initial correction wave established deterministic probes, raw evidence, and instruction validation. Its historical v1 paths are preserved only in the external archive/evidence record; active KitV2 tooling uses the standalone product paths.
- 2026-08-02 — `KIT_CHARTER.md` is process authority. Structural approvals are recorded in this file before implementation. The current product probe runner is `KitV2/probes/run.sh`; Pi discovery remains a separate runtime check.

## Kit governance audit — phase 1 decisions (2026-08-04)

Owner decisions recorded from the governance audit
(`docs/research/2026-08-04-kit-audit-governance.md`, §4.7), taken before the
phase-2 contract drafting:

1. **Bibliothèques — format unique.** `knowledge/catalogs/libraries/` : les
   bibliothèques admises (admission 9 critères passée) sont des modules
   SKILL.md ; les simples pointeurs « à considérer » restent des artefacts
   YAML Source dans un sous-dossier distinct (ex. `pointers/`). La distinction
   actuelle devient explicite et vérifiable par le validateur.
2. **Module Go unique.** Le Kit conserve un go.mod racine unique
   (`go-agent-kit-v2`) pour recettes, templates, probes et tools. Pas de
   modules isolés par recette ; les exceptions éventuelles (dépendance lourde)
   nécessitent une décision dédiée.
3. **Skills de workflow dans le produit.** Les 5 skills `KitV2/.pi/skills/`
   (go-code-review, go-implementation-plan, go-source-retrieval,
   go-testing-verification, go-idiomatic-implementation) restent dans le
   produit comme skills de workflow du processus de dev. Le contrat Z8
   délimite les trois rôles (prompts = orchestrateurs, skills = procédures,
   modules = contenu) et complète leur frontmatter (description,
   last-verified).
4. **Nettoyages actés (phase 2, avant rédaction des contrats) :**
   - supprimer `KitV2/embeddings/` (héritage vide ; graphe + index généré le
     remplacent ; Decision Record note le rejet) ;
   - supprimer `KitV2/tools/analyzers/` (vide, sans contrat ; la vérification
     de duplication est absorbée par le validateur étendu) ;
   - renommer `rules/core/rules/universal` → `rules/core/universal`
     (anomalie d'imbrication, migration du chemin dans settings et
     références) ;
   - remplir `knowledge/debugging/` (procédures d'échec observé, promis par
     l'INDEX) comme objectif de phase 2.

En attente (défauts proposés dans les contrats, à confirmer à la revue) :
seuil de fraîcheur `last_verified` (12 mois → warning, 18 → déprécié), budget
de compacité core (≤ 6 modules, ≤ 300 lignes), nouvelles shapes de templates
(library, desktop/wails) listées en roadmap.

## Kit governance audit — décisions phase 2 (2026-08-04)

1. **Seuil de fraîcheur approuvé.** `last_verified` : 12 mois → warning,
   18 mois → statut déprécié. Applicable à tous les artefacts datés du Kit
   (modules SKILL.md, YAML-graphe, recettes).
2. **Budget de compacité core approuvé.** `rules/core/` ≤ 6 modules, chacun
   ≤ 300 lignes ; dépassement = admission bloquée (coût permanent de session).
   Unité de compte : dossier top-level de `rules/core/` contenant une SKILL.md
   (5 au 2026-08-04).
3. **Politique templates — directive propriétaire (majeure).** Les templates
   du Kit ne sont **jamais écrits par un agent**. Chaque template est une
   copie (fork léger, adaptations minimales documentées) d'un **projet open
   source réel, fiable, fonctionnel, à responsabilité unique**, qui respecte
   les règles du Kit, et sous **licence MIT** (totalement ouverte). Les
   templates doivent être directement réutilisables avec très peu de
   modifications, simples et documentées. Un template non fonctionnel est
   interdit. Il peut y avoir **moins de templates mais très qualitatifs**,
   améliorés par la communauté au fil du temps. Les squelettes agent-générés
   existants dans `templates/` sont marqués `legacy` et candidats au
   remplacement par des templates sourcés MIT.
   **Précision 2026-08-04 (complément propriétaire)** : le critère de
   sélection est élevé — le projet source doit être **ultra-spécifique et
   minimal** : presque exclusivement la/les technologie(s) du template, une
   seule stack, aucune technologie annexe hors périmètre, codebase petit et
   parcourable de bout en bout, structure claire, bien organisée et
   **modulaire** (composants isolés et remplaçables, intégration dans un
   projet quelconque par copie de modules bien délimités, modification
   simple). Le périmètre technique est attesté dans `ATTRIBUTION.md` et
   contrôlé (C2 + revue) — voir contrat Z5.
4. **Extension de schéma `category: workflow`.** Les 5 skills de
   `KitV2/.pi/skills/` portent `category: workflow` (hors jeu validé des
   modules : recipe|rule|pattern|library|reference-project|checklist). Cette
   valeur kit-only ne s'applique qu'aux skills de workflow ; le validateur
   produit ne la contrôle pas (hors de ses chemins). Enregistrée le
   2026-08-04 avec le frontmatter complété (category, tags, last-verified).

## Deferred by reconciliation

- Secret scanning, SARIF publication, SLSA provenance, and release/versioning infrastructure were deferred while the kit was local-only. Since the repository is public (2026-08-03), the reason is obsolete: release/versioning infrastructure is now a planned future task (see Progress — Future deployment foundation); secret scanning, SARIF, and SLSA remain deferred until the kit or generated apps are distributed outside the machine.
- Dedicated Claude/Codex/Gemini generators are deferred until the core, recipes, and spec-driven workflow are solid. A root `AGENTS.md` plus the existing Pi skills covers the current need without adding parallel output surfaces.
- Fuzzing, `go fix`, `testing/synctest` adoption in recipes, and modern `tool` dependencies remain secondary; adopt only where a concrete recipe gains verified value.

## Semantic Resource Router (2026-08-05)

- **Index de routage, pas RAG** : le kit embarque un index généré
  (`KitV2/router/index.json` + `meta.json`) utilisé en lecture seule par
  l'outil Pi natif `search_kit_resources`. L'index ne contient que des
  descriptions ; la vérité reste les fichiers du kit.
- **Pas d'embeddings (décision utilisateur 2026-08-05)** : recherche BM25
  (k1=1.2, b=0.75) + synonymes bilingues (runtime-only) sur les descriptions
  frontmatter curées ; l'agent LLM fait le tri final sur le top-K compact.
  API externe (coût, réseau, requête à encoder côté consommateur) et modèle
  local Ollama (service chez l'utilisateur) rejetées — sources web vérifiées
  (BM25 ≥ embeddings sur petit corpus).
- **Stockage JSON versionné** : index.json + meta.json (sha256, compteurs,
  stopwords source unique). SQLite rejeté (surdimensionné à ~206 ressources).
- **Déclenchement : recherche obligatoire avant tout travail technique**
  (décision utilisateur) — encodée dans la skill `kit-resource-routing`.
- **Outil = extension Pi native** (`registerTool`, zéro dépendance npm —
  typebox fourni par Pi). CLI python3 rejeté (dépendance d'exécution).
- **Séparation stricte** : builder dans le méta-projet
  (`.agent/router/build_index.py`, déterministe, --check) ; kit en lecture
  seule. Gate étendue (couverture + hash) → toute dérive bloque la release.

## Knowledge completion pipeline (2026-08-04)

- **Pipeline obligatoire pour toute bibliothèque du catalogue** (décision
  utilisateur, suite au lot de complétion des 29 bibliothèques) : Analyse →
  Audit de couverture → Recherche (sources primaires) → Question (si décision
  éditoriale) → Plan → Découpage → Exécution (une bibliothèque à la fois) →
  Validation → Rapport. Encodé dans le contrat Z2 §9 et la règle Agent.md
  « Library knowledge pipeline ».
- **Manques réels uniquement** (réponse utilisateur à la question éditoriale) :
  un artefact par question distincte non couverte ; le volume non justifié est
  un échec d'admission (write-gate C0 §4).
- **Les Notes des catalogs couvrent souvent les limites** d'une bibliothèque
  (ex. TTL de ristretto, v6 alpha de go-git) : les vérifier avant d'écrire un
  artefact de connaissance, sous peine de duplication.
- **Conventions d'écriture** : URLs canoniques jamais réécrites pour un lint
  (échappement YAML `"...\<LF>  suite"` sur `source:` si nécessaire, vérifié
  par yaml.safe_load) ; français pour patterns/anti-patterns, anglais pour les
  pointeurs Source ; lignes > 80 non bloquantes (convention corpus).
- **Contrôles de sortie** : gate C0 §8 + router régénéré après tout ajout YAML
  knowledge + INDEX.md à jour (générateur d'index toujours en attente — Z2 §4).

## Catalog fiche format (2026-08-04)

- **28 bibliothèques enrichies** : chaque SKILL.md de `catalogs/libraries/`
  porte les 6 sections décisionnelles du « format fiche » (Utiliser cette
  librairie quand / Ne pas utiliser cette librairie quand / Avantages /
  Inconvénients / Pièges connus / Sources vérifiées), ajoutées après les
  sections vétées, en-têtes FR (spécification utilisateur), contenu libre.
- **Placement contraint** : `knowledge/catalogs` est déclaré répertoire de
  skills Pi dans `.pi/settings.json` → la fiche vit DANS le SKILL.md ; un
  fichier compagnon (.md non-SKILL.md) casserait la découverte Pi (Gotcha
  2026-08-03). Frontmatter des entrées vétées inchangé.
- **Exigence multi-source** : toute critique négative d'une fiche est
  confirmée par ≥ 2 sources ou issues officielles (jamais une source isolée) ;
  chaque entrée de « Sources vérifiées » porte URL + date + type.
- **Standard encodé** : N1 §4 (format fiche canonique du corps des catalog
  SKILL.md) + Z2 §9.2 (admission = fiche complète). Le router est inchangé
  (édition de corps uniquement, descriptions frontmatter intactes).

## Correction post-audit KitV2 (2026-08-05, cycle KVA-001→017)

Journal de décision du cycle de correction post-audit
(`docs/plans/2026-08-05-kitv2-correction-plan.md`, rapport d'audit
`docs/research/2026-08-05-kitv2-audit-report.md`). Chaque décision est
enregistrée AVANT l'édition correspondante ; les items AMBIGU/À VÉRIFIER de
l'audit sont retraités, jamais recopiés.

- **D-2026-08-05-01 (KVA-005, placement 21 YAML Niveau B)** : contractualiser
  le format au lieu de déplacer. `catalogs/libraries/*.yaml` devient un format
  documenté de `knowledge/` : pointeurs Source actifs « Niveau B » (source
  conditionnelle, non vétée, admission allégée : source primaire + question
  distincte), distincts des SKILL.md vétées et des pointeurs `pointers/`
  (`status: proposed`, « à considérer »). Justification : la pratique des kits
  comparables sépare candidats/admis (recherche 05-placement-kits, 2026-08-05),
  mais les 21 fichiers sont des artefacts actifs dont le déplacement casserait
  la sémantique de statut et le graphe ; le contrat est la surface minimale qui
  élimine le défaut « format non contractualisé ». Mise à jour : Z2 §2 (contrat
  méta-projet, sortie de périmètre documentée). Aucun déplacement de fichier.
- **D-2026-08-05-02 (KVA-006, statut templates)** : appliquer le vocabulaire
  Z5 §4 (planned/sourced/legacy/deprecated) : les 7 `template.yaml` passent de
  `status: partial` à `status: legacy`, les README des 7 shapes alignent leur
  ligne de statut sur `LEGACY`, `capabilities.yaml` passe le statut de la
  capacité templates à `legacy-scaffolds`. Justification : Z5 §4 définit 4
  statuts ; TEMPLATES.md dit déjà `legacy` ; `partial` n'existe pas au
  vocabulaire et crée une triple source de vérité contradictoire.
- **D-2026-08-05-03 (KVA-011, pointeurs proposed livrés et indexés)** : les
  pointeurs `status: proposed` (`catalogs/libraries/pointers/*.yaml` ×5 et
  `knowledge/architecture/bootstrap-cli-runtime.yaml`) restent livrés et
  indexés par le router PAR DÉCISION (découvrabilité « à considérer », pratique
  B1 observée dans 05-placement-kits) ; Z10 §5.3 est amendé avec l'exception
  documentée. Aucun changement de code ni de router.
- **D-2026-08-05-04 (KVA-001, gate validate-cognitive)** : résoudre la gate
  depuis la base de résolution contractée (le catalogue) : ajouter
  `source:security:owasp-session-jwt-cheatsheets` à
  `.agent/cognitive/source-catalog.yaml` avec `transformations.patterns` =
  [pattern:security:auth-session-vs-jwt, pattern:security:secrets-management]
  et `target_status` = active + materialized_by vers les 2 fichiers produits.
  Justification : validate-cognitive résout CONTRE le catalogue par design
  (Gotchas 2026-08-03 : « product Source entries remain pointer-only ») ;
  l'arbre produit reste la vérité de validate-kitv2. Sortie de périmètre
  `.agent/cognitive/` documentée (le finding l'exige).
- **D-2026-08-05-05 (KVA-015, id français)** : renommer
  `recipe-cli-interactif` → `recipe-cli-interactive` (N1 §1 interdit le
  français dans les ids ; Z3 §4.2 acte le renommage) : git mv du dossier,
  frontmatter `name`, titre et ligne `go test` du SKILL.md, références produit
  (knowledge/patterns/testing-seam-injection ×2, cli-subcommands-conventions
  ×1, anti-patterns/test-implementation-details ×1,
  catalogs/libraries/bubbletea ×1), `.agent/cognitive/technology-documentation.yaml`
  ×1 ; router régénéré ; documents historiques de docs/ NON modifiés.
- **D-2026-08-05-06 (KVA-016, contrat Z2 stale)** : mettre à jour Z2 §2 —
  `pointers/` existe depuis 2026-08-05 (5 pointeurs proposed « à considérer »).
- **D-2026-08-05-07 (KVA-007/008, validateur)** : étendre validate-kitv2.py
  avec (a) une suite de tests unittest `test_validate_kitv2.py` couvrant les
  contrôles existants et nouveaux (cas +/−), (b) la dérivation des comptes
  coverage depuis l'arbre (suppression de EXPECTED_PRODUCT_SKILLS en dur,
  vérification de capabilities.coverage), (c) contrôles ajoutés : fraîcheur
  12/18 mois (warning/erreur), vocabulaire Z5 des template.yaml, découverte
  probes par glob (rejet liste en dur), check.sh réel (rejet gofmt-only).
- **D-2026-08-05-08 (KVA-004, schéma de règle)** : aligner `10-zone-rules.md`
  §5 sur A1 §1.9/§2 — les éléments sémantiques (impératif, quand appliquer,
  frontière, contre-exemples, vérification, sources) restent obligatoires mais
  les en-têtes sont libres (une section n'existe que si elle a du contenu).
  L'ancien schéma en-têtes-fixes n'était implémenté par aucune des 13 règles et
  contredisait A1 §1.9. Frontières manquantes ajoutées aux règles
  (concurrency, philosophy, golangci-lint, gosec, govulncheck, doc-comments,
  testing) ; universal avait déjà un énoncé de frontière. Z1 §9 passe le
  schéma en contrôle de revue. Décision utilisateur : Option A.
- **D-2026-08-05-09 (KVA-007, parallélisme config)** : les recettes
  `recipe-config-koanf` et `recipe-config-viper` partagent une fonction
  `validate()` de 6 lignes (byte-identique dans les packages séparés koanf.go /
  viper.go et dans les deux SKILL.md). Décision : conserver la duplication Go
  (packages distincts devant compiler séparément, module unique sans couplage
  croisé inutile) mais la déclarer par cross-référence mutuelle dans les deux
  fiches au lieu d'un doublon silencieux. Aucun nouvel artefact (une fonction
  de 6 lignes ne justifie pas un snippet canonique).
- **D-2026-08-05-10 (vague de correction d'audit KVA-001…011, produit 2.4.1)** :
  (a) vocabulaire manifest↔capabilities unifié en kebab (11 capacités, clés
  `knowledge`/`templates`/`product-verification`/`resource-routing` au lieu de
  `knowledge-catalog`/`project-templates`/snake), chaque capacité porte
  `criteria:` (C1 §6) ; (b) `golang.org/x/sync` admis comme pointeur stdlib
  (`knowledge/stdlib/x-sync.yaml`) — Z3 §8 rendu vérifiable par
  `check_recipe_dependencies` ; (c) gate : `check_template_build` (Z5 §8) et
  `check_manifest_capabilities_coherence` (C1 §3.2) ajoutés à
  validate-kitv2.py avec tests +/− ; (d) `rules/core/errors` ne référence plus
  le registry ; (e) probes/README.md = contrat de zone Z6 à jour. Router
  régénéré (256 ressources, meta version 2.4.1). Revue fresh-context :
  APPROVE-WITH-NITS, nits intégrés.

## Durcissement gouvernance méta-projet (2026-08-05, findings Rodin)

Passe méta-projet uniquement (aucune édition KitV2) fermant 5 findings de la
critique « Rodin » — plan `docs/plans/2026-08-05-metaproject-governance-
hardening.md`, revue fresh-context APPROVE-WITH-NITS (nits intégrés). Les
5 décisions suivantes sont enregistrées AVANT la clôture de la passe ; les
éditions produit correspondantes sont des actions en attente du plan (passe
suivante).

- **D-2026-08-05-11 (Chantier A, dérive inter-fichiers)** : la revue sémantique
  inter-fichiers reste humaine (C2, bloc Fraîcheur), mais son déclenchement
  devient mécanique — combinaison de (b) mécanisée et (a) tripwire. Règle
  vérifiable : toute modification d'un artefact canonique (recette, règle,
  pattern) avec dépendants déclarés exige leur re-vérification dans le même
  changement, contrôlable par dates `last_verified(dépendant) >=
  last_verified(canonique)` pour les chaînes déclarées (snippet `source:` →
  SKILL.md cible ; relations YAML-graphe `references`/`uses`/`depends_on`).
  Champ `last_verified` recommandé dans SNIPPET.yaml (Z4 §3). En complément,
  tripwire de similarité (warning, jamais erreur) entre `example.go` et le bloc
  Go canonique de `source:` (vue focalisée ≠ copie → faux positifs possibles,
  d'où warning). Statu quo seul (c) écarté : n'ajoute aucun déclencheur.
  Contrats : C2 §2, Z4 §3/§5/§8, Z3 §5, Z1 §6 ; kit-audit phase C4 + §5-E.
  Contrôle C2 exact (entrées/sortie/faux positifs/tests) : plan, annexe A —
  à implémenter dans validate-kitv2.py à la passe suivante (KitV2).
- **D-2026-08-05-12 (Chantier B, roadmap snippets)** : le design est sain,
  fermé sans travail fabriqué. Comparaison : les 7 lignes roadmap de
  `snippets/README.md` portent chacune un critère d'admission actionnable
  (plus précis par ligne que le statut `planned` des templates « décision +
  ligne ») ; le patron roadmap-pas-de-dossier-fantôme est mandaté par Z4 §3
  règle 3 + C0 §7 et déjà en usage pour templates/TEMPLATES.md. Aucune
  faiblesse réelle à corriger ; aucun changement de contrat.
- **D-2026-08-05-13 (Chantier C, philosophie)** : tension vérifiée à 2 niveaux
  (AGENTS.md racine « Go does not prescribe a universal project tree » ;
  rules/core/philosophy « prescribes no universal project layout ») vs objectif
  personnel de navigation identique. **Réponse Marie (question posée) :
  Option 3 — « naviguer par la raison »** : liberté de structure conservée,
  mais toute recette qui produit/recommande une disposition de projet doit
  l'expliquer au même endroit (section Structure), et le README de tout
  template sourcé justifie sa structure. Appliqué (méta-projet) : Z3 §3.8 +
  §8 (contrôle de revue audit C1), Z5 §3. KitV2 en attente : section Structure
  dans les recettes concernées + justification dans les README des 3
  templates. Aucune modification d'AGENTS.md racine ni de rules/core
  nécessaire (l'Option 3 est compatible avec la doctrine sourcée). Note :
  `docs/research/2026-08-05-philosophy-tension.md`.
- **D-2026-08-05-14 (Chantier D, template desktop-app)** : aucun candidat Wails
  ne satisfait la politique Z5 §2 au 2026-08-05 (Wails v3 en beta, écosystème
  immature ; v2 stable mais aucun projet réel MIT mono-techno testé ;
  `wailsapp/examples` = démos, exclus). On n'assouplit pas les critères.
  Précision Z5 §2 appliquée : la source d'un template doit être une application
  réelle à responsabilité unique, pas un starter/template tiers ni un recueil
  de démos (leçon transférable). Ligne roadmap desktop-app = `planned` avec
  note « aucune source conforme au 2026-08-05, ré-évaluer à la GA » (texte prêt
  : plan, annexe D — non appliquée, KitV2). kit-audit phase B : toute capacité
  couverte par recette + probe sans reconnaissance roadmap de template est une
  catégorie de finding nommée. Dossier :
  `docs/research/2026-08-05-desktop-app-template-candidates.md`.
- **D-2026-08-05-15 (Chantier E, instructions MANDATORY)** : Pi expose une
  vraie porte mécanique (vérifié dans `docs/extensions.md` : l'événement
  `tool_call` peut bloquer `{ block: true }`, `pi.setActiveTools()` active/
  désactive des outils, `before_agent_start` injecte des messages,
  `pi.appendEntry()` persiste l'état de session). Principe étendu aux artefacts
  consommateurs (extension assumée d'.agent/instructions.md) : toute absolue
  doit avoir un contrôle mécanique nommé OU être consignée « guidance seule »
  dans le registre des lacunes d'automatisation (`.agent/instructions.md`
  §Enforcement — première ligne : kit-resource-routing, statut guidance seule).
  Contrats : C2 §2 (bloc instructions absolues), Z8 §3.6 ; kit-audit nouvelle
  dimension C9 + §5-E. Spec de la porte (reminder doux, dégradation sans UI,
  hard-block optionnel, confiance medium : présence-session ≠ bonne recherche) :
  plan, annexe B — implémentation en passe suivante (KitV2/.pi/extensions/).
  Pas de scan validateur dur : risque de faux positifs sur des absolus
  légitimement appliqués par revue.

## Intégration spec-driven-dev (2026-08-05, mise à jour majeure)

Intégration de toute la logique du dépôt MIT `zhu1090093659/spec_driven_develop`
(v1.15.0) dans le kit, adaptée au harnais Pi et bornée par le contrat Z12.
Analyse : `docs/research/2026-08-05-spec-driven-dev-analysis.md` ; plan :
`docs/plans/2026-08-05-spec-driven-dev-integration.md`. Décisions prises APRÈS
questions utilisateur.

- **D-2026-08-05-16 (stratégie : remplacer la chaîne workflow-*)** : le
  workflow de référence des transformations à grande échelle devient la skill
  `spec-driven-dev` (phases 0-6) ; les prompts
  `workflow-{clarify,plan,tasks,implement,verify}` sont supprimés
  (2026-08-05) et ne doivent pas être recréés. La skill compose les ressources
  restantes (workflow-memory, go-*, kit-resource-routing, go-code-review) par
  cross-références. Raison : la chaîne existante ≈ phases 2-5 ; spec-driven
  apporte les phases 0-1, S.U.P.E.R, le contrôle adaptatif et l'archive —
  deux workflows parallèles auraient été un doublon (charte §4).
- **D-2026-08-05-17 (langue : FR + frontmatter EN)** : corps des
  skills/références en français (style kit-audit), `description:` frontmatter
  en anglais (découvrabilité Pi, format validate-instructions.py).
- **D-2026-08-05-18 (périmètre : LOCAL_ONLY uniquement)** : pas de GitHub
  (Issues/Milestones/PRs/gh CLI). Le suivi vit dans `docs/progress/` ;
  les lots de livraison sont des unités locales d'intégration/validation.
  Sous-agents : dispatch tiercé conservé, mappé sur le mécanisme natif Pi,
  décision économique ; rôles spec-driven documentés en mapping (jamais
  livrés comme fichiers).
- **D-2026-08-05-19 (bornage : contrat Z12, sans toucher la charte)** :
  nouveau contrat `.agent/kit-governance/22-zone-spec-driven-dev.md` + index
  README, Z8 mis à jour (table des rôles), kit-audit dimension C10 + catégorie
  de finding + §5-E. `KIT_CHARTER.md` inchangé : le workflow est un artefact
  de zone (Z8/Z12), la charte reste l'autorité de processus.
- **D-2026-08-05-20 (règle mémoire kit)** : règle AJOUTÉE DANS LE KIT (pas le
  méta-projet) — tout agent utilisant le kit vérifie quels fichiers
  `.pi/memory/` existent réellement : le bootstrap Pi ne crée pas
  `Decisions.md` par défaut. Ne jamais supposer l'ensemble standard ; créer
  les fichiers manquants sans copier d'historique externe. Encodé dans
  `KitV2/AGENTS.md` + `workflow-memory.md` + templates governance.
- **Fusion review-spd → go-code-review** : la discipline findings-first de
  review-spd (3 cibles, planning par taille, 5 focus de reviewers, format de
  sortie) est fusionnée dans la skill existante `go-code-review`
  (references/reviewer-focus.md + SKILL.md augmenté) — une seule skill de
  review (anti-doublon charte §4). Sévérités du kit conservées comme référence
  de sortie.
- **Frontière S.U.P.E.R** : S.U.P.E.R = lentille d'évaluation de santé +
  checklist de revue, PAS une doctrine de conception Go. En conflit avec
  rules/core/philosophy (Clean/Hexagonal vs « plus petit design justifié,
  stdlib-first »), les règles sourcées du kit priment. Encodé dans
  `references/super-philosophy.md` + Z12 §3.2.

## Mandatory language: English (2026-08-05, fundamental rule)

- **D-2026-08-05-21 (mandatory language: English only)** : owner directive
  (fundamental project rule) — English is the mandatory language for EVERY
  skill, instruction, and document in this repository (kit and metaproject):
  skills, prompts, contracts, plans, research, decisions, written artifacts.
  The whole project lives on one single language. **SUPERSEDES
  D-2026-08-05-17** ("FR bodies + EN frontmatter"): French bodies written
  under D-17 (spec-driven-dev zone, contracts, kit-audit, plans/research)
  must be translated to English. Any translation preserves technical terms
  and intent; it is faithful to the original meaning and as close to it as
  possible, without reformulation. Ids stay ASCII kebab-case; code, commands,
  and technical identifiers are never translated. Governance impact: N1
  (30-conventions.md) — the "French for patterns/anti-patterns, English for
  Source pointers" convention is replaced by "English everywhere";
  kit-audit C7 (language) — explicit repository policy: English mandatory.
  Priority (owner clarification): the kit must respect the rule absolutely
  (mandatory for standardization and unification); the metaproject is
  secondary but the selected scope (active instruction surfaces) is
  translated in the same pass.

## Language wave + audit remediation (2026-08-06)

- **D-2026-08-06-01 (language wave executed, KVA-101…110 closed)**: the
  residual-French wave documented in N1 §4 was converted to English in one
  pass: 15 recipe SKILL.md (bodies + descriptions), 93 pattern/anti-pattern
  graph-YAML, 43 catalog fiche files (6 headers, 37 H1s, bleve +
  golang-migrate bodies), `mcp-server-shape.yaml`, and the `AGENTS.md` /
  `rules/registry/` references to the old French section names. Zero French
  remains on the kit instruction surface (accent-scan, 2026-08-06). New
  content must be written in English at admission.
- **D-2026-08-06-02 (fiche source heading English)**: `validate-kitv2.py`
  strict-catalog check now accepts/requires the English `Verified sources`
  heading (French tolerated for one migration cycle); the 43 files were
  converted in the same change (N1 §4a coupling). Plan:
  `docs/plans/2026-08-06-language-wave-and-fix-pipeline.md`.
- **D-2026-08-06-03 (snippet date-chain check)**: `validate-kitv2.py`
  implements the D-2026-08-05-11 cross-file freshness check
  (`last_verified(snippet) >= last_verified(canonical)`; missing dates
  ignored) with positive + negative tests (11/11); the 3 `SNIPPET.yaml` now
  carry `last_verified`.
- **D-2026-08-06-04 (known_limits structured)**: `capabilities.yaml`
  `known_limits` migrated to `id`/`impact`/`status` (C1 §3.4 target state);
  the open pi-discovery limit downgrades `pi-workflows` to `partial`;
  criteria text corrected to the real counts (3 prompts, 8 workflow skills).
- **D-2026-08-06-05 (absolute-instruction interpretation)**: rule-content
  boundaries (Z1 semantic elements with their own "Verification" section)
  are NOT "process absolutes" for the `.agent/instructions.md` §Enforcement
  registry; only process instructions in skills/prompts/AGENTS.md/recipes are
  recorded (4 new rows added, KVA-106).
- **D-2026-08-06-06 (template roadmap recognition)**: `templates/TEMPLATES.md`
  now records `desktop-app` as `planned` (recipe + probe exist; no conforming
  real single-responsibility MIT Wails source, research 2026-08-05).

## structure.md contract + governance hardening (2026-08-06)

- **RDN-003 (structure.md reading map, as ruled)**: no forced identical
  project structure across project types; every project generated by the kit
  embeds a `structure.md` at its root — a reading map for a non-developer, not
  a file inventory. It complements (does not replace) the philosophy universal
  rule "no imposed universal project layout"; the philosophy rule was NOT
  modified. The implementation (generator, rule, template integration) is
  specified in the charter (Layer 5.1) but NOT implemented in KitV2 in this
  session; the next kit-audit pass detects and drives it.
- **D-2026-08-06-07 (placement: Layer 5.1 subsection, not a new layer)**:
  `structure.md` lives as a subsection of Layer 5 — Templates ("Layer 5.1"),
  not as a new cognitive layer. Rationale: layers type knowledge artifacts;
  structure.md is a produced document of generated projects; a new layer would
  inflate the type system and break §4 single-source-of-truth.
- **D-2026-08-06-08 (generation vs validation policy)**: default is
  deterministic generation — drift gate (`git diff --exit-code` in CI), Go
  "// Code generated ... DO NOT EDIT" convention; semantic exception: reading
  paths/explanations are human enrichment over the generated skeleton;
  validation-only exception allowed only under three objective conditions
  (non-standard layout; mechanical drift check in CI; semantic content
  reviewed with tree-touching changes). Evidence:
  `docs/research/2026-08-06-structure-md-generation.md` (fresh researcher, no
  blocking technical obstacle found → no owner question needed).
- **D-2026-08-06-09 (governance hardening, charter §16.1)**: four verifiable
  governance constraints added to the charter — relation resolvability; router
  as sole entry; category justification; absolute-instruction validation.
  Each constraint names its enforcement control: validate-cognitive.py,
  validate-kitv2.py date-chain check, `build_index --check`,
  `.agent/instructions.md` §Enforcement + kit-audit C9/C15. Kit-audit gained
  dimensions C11–C15.

## KitV2 AGENTS.md Z9-conformity correction (2026-08-06)

- **D-2026-08-06-10 (AGENTS.md zone map + Limits brought to Z9)**: a
  critical report proposed rewriting `KitV2/AGENTS.md`; verification showed
  most premises stale (the `workflow-clarify → plan → tasks → implement →
  verify` chain was removed 2026-08-05, D-16..20; the skill inventory is 8,
  not 5; the "MANDATORY search_kit_resources" rule already lives in
  `kit-resource-routing` and is registered guidance-only). Applied only the
  contract-required parts: Source-of-truth converted from a bullet list to
  the Z9 §2.1 table (zone → one-line mission → pointer), Limits now states
  uncovered domains (Z9 §2.5): full Wails desktop wiring, TUI beyond the
  interactive Bubble Tea recipe, Pi discovery internals, non-Go domains.
  `rules/` repointed to `rules/core/` + `rules/registry/` (no zone README may
  be created: rules/ is a declared Pi skill dir, gotcha 2026-08-03). The
  AGENTS.md §Limits absolutes were registered guidance-only in
  `.agent/instructions.md` (charter §16.1.4). Z9 §2.5 example aligned with
  actual coverage (rewording, not a scope change). Validators PASS,
  fresh-context review REQUEST-CHANGES → 1 dangling pointer + 1 TUI wording
  tension fixed, then APPROVE.

## Routing guarantee wave (2026-08-06, product 2.5.0)

- **D-2026-08-06-11 (routing quality is contract-tested, owner decisions)**: three
  owner decisions (asked 2026-08-06): (1) implement the routing-quality gate —
  `router/scenarios.json` (22 scenarios) verified by the metaproject runner
  `.agent/router/run_scenarios.mjs` under the REAL runtime scoring
  (`kit-resource-router-scoring.ts`, the exact module the tool imports — zero
  divergence by construction); (2) reduce the always-visible Pi skill surface —
  `.pi/settings.json` now loads only `../rules` + `../recipes`, catalog fiches
  stay indexed and routable on demand; (3) strengthen the routing mandate —
  KitV2/AGENTS.md "Routing is mandatory, not optional" + the tool's
  promptGuidelines name the default-applicable patterns (naming, error
  wrapping, channel ownership, zero value). Product validator stays node-free
  (`check_router_scenarios`: schema + id linkage); the ranking gate is
  metaproject-owned. Z11 updated with the full maintenance protocol; the gate
  has demonstrated failure modes (2 negative tests: unreachable expectation →
  exit 1, stale id → exit 1) — a gate that cannot fail proves nothing.
  Evidence: plan `docs/plans/2026-08-06-routing-guarantee.md`, gate
  `run_scenarios.mjs` 22/22 PASS, metaproject tests 27 passed, review APPROVE.

## Audit-fix wave (2026-08-06, KVA-101..110, release v2.5.0)

- **D-2026-08-06-12 (template.yaml schema gains two mandatory fields)**: per
  charter §16.1.3 (usage-evidence at admission) and Layer 5.1 (structure.md
  mechanism), every sourced template's `template.yaml` must carry
  `usage-evidence` (real, documented usage — never theoretical utility) and
  `structure.md` (generation/validation declaration). This changes Z5 §3's
  documented schema; the Z5 contract and the product validator are updated in
  the same change. The three existing sourced templates are backfilled with
  honest evidence (worker template notes its young repo and thin popularity
  evidence explicitly).
- **D-2026-08-06-13 (CI coverage floor measures the testable surface)**:
  the 15 probe `main.go` files are executable observable scenarios verified
  by `bash probes/run.sh` in the same CI run — not unit-testable library
  code. The coverage aggregate excludes `probes/` (library surface alone is
  79.6% ≥ 70%); this is scope definition, not metric gaming. The CI gate is
  completed with the product validators, `build_index.py --check`, and
  `probes/run.sh` so the machine gate equals the local gate.
- **D-2026-08-06-14 (English-only stopwords)**: the router stopword list is
  pruned of the residual French tokens (pre-2026-08-05 bilingual era);
  queries and descriptions are English-only (D-2026-08-05-21). The routing
  skill's "French terms have partial synonym coverage" note is reworded
  accordingly. Index regenerated; routing gate must stay 22/22.

## macOS Computer Use resources (2026-08-07)

- **D-2026-08-07-01 (premise check: no general anti-CGO/Objective-C rule exists)**: the request asked for an "exception" to a supposed kit rule avoiding CGO/Objective-C/native bindings. Verified against the tree: no such rule exists — zero-CGO appears only as a library-selection preference in catalog fiche decision sections and as factual cross-compilation guidance (`stdlib/go-cross-compilation.yaml`); `rules/core/philosophy` says "Prefer the standard library or platform capability". The "exception" would qualify a rule that does not exist. The intent (agents must not refuse native Apple APIs for computer use) is served by explicit positive guidance in the new artifacts, with no existing artifact modified.
- **D-2026-08-07-02 (RobotGo admitted as vetted fiche)**: github.com/go-vgo/robotgo passes the 9-criteria admission gate with actual reasons — v1.0.0 (2025-12-04), v1.0.2 (2026-03-30), v2.0.0-beta2 (2026-07-29), CI `.github/workflows/go.yml`, 9 `_test.go`, 10.7k stars, Apache-2.0. macOS: cgo by default (`robotgo_mac.go`, CoreGraphics), purego opt-in via `-tags purego` ("no Xcode required", CGO_ENABLED=0 compatible). Fiche: `knowledge/catalogs/libraries/robotgo/SKILL.md`.
- **D-2026-08-07-03 (Computer Use macOS scope: pattern + fiche, no recipe)**: user decision (2026-08-07). One architecture pattern `knowledge/architecture/macos-computer-use.yaml` (AXUIElement primary semantic layer, RobotGo execution layer, ScreenCaptureKit visual complement; native-API guidance; darwinkit mentioned with stale-maintenance caveat only — not admitted, last release 2024-07) + the RobotGo vetted fiche. No runnable recipe (no cgo code in the gate), no new category (pattern lives in the existing `architecture/` domain). Router regenerated (280 resources), capabilities 73/44, gate PASS (validators, 22/22 scenarios, gofmt/vet/lint/test/gosec/govulncheck, probes 15/15), fresh-context review APPROVE-WITH-NITS (nits: router classifies architecture YAMLs as kind "source" — pre-existing builder behavior; memory update). Plan `docs/plans/2026-08-07-computer-use-macos.md`; evidence `docs/evidence/2026-08-07/computer-use-macos/sources.md`.

## ui-agent-kit integration (2026-08-07)

- **D-2026-08-07-04 (native first-class zone, owner decision)**: the ui-agent-kit
  SDK is integrated as a first-class KitV2 zone (`ui-kit/`), mirror of upstream
  `sdk/` at pinned commit `f9bdd9b` (byte-identical to npm `ui-agent-kit@0.1.0`
  tarball `sdk/`), with its own AGENTS.md shipped verbatim. The owner explicitly
  superseded mission rule 5's literal "no trace" reading: non-pollution is
  achieved behaviorally — no UI skill in `.pi/settings.json`, Go router never
  reads the zone, the sync tool refuses without `wails.json` + `frontend/`,
  and the two routing corpora are gate-checked disjoint. UI queries route via
  the second read-only tool `search_ui_kit_resources`; the shared scoring
  module is reused (single scoring implementation), stopwords come from the
  shipped `router/meta.json`. Reports follow GoAK `docs/` conventions.
- **D-2026-08-07-05 (shared modules relocate to `.pi/extensions/shared/`)**: the
  Pi extension loader auto-discovers direct `*.ts` files and one-level
  `index.ts` only; top-level shared modules (`kit-resource-router-scoring.ts`)
  were mis-discovered as extensions and aborted headless `pi -p` runs
  (reproduced on the pre-mission baseline). The scoring core and the new UI
  index core now live in `shared/` (not discovered), imported by the two
  extension files (jiti `.js` specifier) and the metaproject gates (plain
  node `.ts` specifier). Behavior-preserving; the 22 Go scenarios and 9 UI
  scenarios pass identically.
- **D-2026-08-07-06 (Wails-only sync tool + manual gated updates)**: consumer
  materialization is a shipped `tools/sync-ui-kit.sh` (detects `wails.json` +
  `frontend/`, copies the zone + code pieces per the SDK copy rules, merges
  `.pi/settings.json`, refuses with exit 1 otherwise) verified by probe
  `ui-kit-sync`. Zone updates are manual and gated via
  `.agent/sync-ui-kit-from-upstream.sh <sha>` (Z13 §4) — never automatic.
  The ui-agent-kit CLI first-run ordering bug (`shadcn` before `tsconfig.json`,
  exit 0 on failure) is a separate upstream proposal (mission rule 2).

## ui-agent-kit maintenance workflow (2026-08-07)

- **D-2026-08-07-07 (update workflow: one prompt + one gated helper)**: the
  ui-kit update path is now a complete maintenance system. The metaproject
  prompt `.pi/prompts/update-ui-kit.md` (phases 0-3: pre-flight, sync,
  review/commit, record) drives the mechanical helper
  `.agent/sync-ui-kit-from-upstream.sh`, which enforces guardrails instead of
  printing a checklist: pre-flight (40-hex SHA, clean zone, upstream
  reachable, sdk/ present), sync scope (only KitV2/ui-kit/, local-owned
  files excluded), post-sync structural checks (diff clean beyond
  local-owned, no .go, no metaproject markers, no empty .md, English), then
  the FULL gate runs INSIDE the helper (validators, router Go+UI gates,
  router tests, gofmt/vet/lint/test-race/gosec/govulncheck, probes). Any
  failure exits 1 with `git restore` rollback instructions; nothing is
  committed automatically. Verified end-to-end (same-pin re-sync → no-op
  tree + FULL GATE PASS). Z13 §4 documents the protocol; the GitHub source
  stays pinned in PIN.md (repo + SHA + npm equivalence). The npm CLI remains
  unused as a source, per the integration mandate.

## ui-kit structure-evolution safety (2026-08-07)

- **D-2026-08-07-08 (dynamic copy rules + ownership manifest)**: the sync
  scripts no longer hardcode the ui-kit layout. `copy-rules.json`
  (local-owned in the zone, regenerated at every re-sync from the upstream
  `cli/manifest.json`) drives the consumer tool's code copies — a new
  upstream folder is covered by the next re-sync with zero tooling change.
  The consumer tool keeps an ownership manifest
  (`<frontend>/ui-kit/.owned.json`, path + sha256): owned+unmodified files
  are refreshed, upstream-dropped files are removed cleanly, and ANY
  consumer-modified or unowned file at a destination path is preserved and
  the run exits 1 (conflicts are never clobbered; first-run adoption records
  without overwriting). The re-sync helper validates the required zone shape
  (`AGENTS.md`, `skills/`, `ui-sdk/`) and every copy-rule source, and its
  pre-flight now detects untracked zone files (`git status --porcelain`, not
  `git diff`). Probe `ui-kit-sync` verifies all four behaviors (materialize/
  idempotence, Wails-only refusal, structure evolution, ownership contract);
  gosec 0. User requirement: the ui-kit may evolve and nothing in a project
  may be destroyed by the scripts.

## Kit audit fixes (2026-08-07, KVA-101..105 + C12/README drift gates)

- **D-2026-08-07-09 (KVA-105 — `_kit-*` files stay in the product, declared
  kit machinery)**: `templates/_kit-ci-workflow.yml` and
  `templates/_kit-skill-authoring.md` remain shipped inside `KitV2/templates/`
  as explicitly declared "kit machinery" (TEMPLATES.md §Kit machinery +
  templates/README.md). `_kit-ci-workflow.yml` is a consumer drop-in CI gate
  (referenced by `rules/registry/testing` and `KitV2/AGENTS.md`);
  `_kit-skill-authoring.md` is a self-contained contributor aid whose
  authority remains the metaproject contract A1 (20-auteur-modules.md),
  never shipped. No move to the metaproject; both files stay, documented.
- **D-2026-08-07-10 (C12 prose-id gate)**: validate-cognitive.py now scans
  product knowledge YAMLs and instruction surfaces for
  `kind:domain:slug` prose tokens and fails on any token that does not
  resolve to a known artifact id (audit finding KVA-101:
  `go-contextual-worker.yaml` referenced the non-existent
  `pattern:go:concurrency-worker-pool`; fixed to
  `pattern:concurrency:worker-pool`). Zero false positives across 280 known
  ids at implementation time.
- **D-2026-08-07-11 (probe inventory gate)**: validate-kitv2.py
  `check_probe_runner` now cross-checks the `probes/README.md` inventory
  table against the real `probes/*/main.go` tree (audit finding KVA-102:
  README claimed 15 probes and omitted `ui-kit-sync`; README updated to 16).
  The old README drift is now a gate failure.
- KVA-103: `ui-kit/PIN.md` §Update path reworded to not name
  metaproject-only surfaces (`.pi/memory/Decisions.md`, `docs/evidence/`).
  KVA-104: `KitV2/.gitignore` now ignores `.pytest_cache/`.

## ui-kit registration + re-sync (2026-08-08, owner mission)

- **D-2026-08-08-01 (re-pin zone to cd00eb5d / ui-agent-kit 0.1.1)**: upstream
  jumped f9bdd9b -> cd00eb5d (+5392 lines: agent chat + assistant-ui
  component families, agent-chat pattern/example). Sourced GitHub-direct at
  HEAD (no git tags upstream — pin by SHA per gotcha). npm 0.1.1 tarball
  `sdk/` verified byte-identical to the pinned `sdk/` (diff -rq empty) but
  npm is never the source. copy-rules.json regenerated from upstream
  `cli/manifest.json` (4th rule: agent-chat example -> src/components/
  example-agent). Full gate PASS inside the helper (validators, Go 22/22,
  UI 9/9, 44 router tests, gofmt/vet/test-race, probes 16/16).
- **D-2026-08-08-02 (single registration point — root settings.json)**: the
  ui-kit skills are now declared in `KitV2/.pi/settings.json`
  (`["../rules","../recipes","../ui-kit/skills"]`, additive). The SDK's
  nested `ui-kit/.pi/settings.json` is DEAD: deleted from the zone and added
  to the re-sync helper's exclusion list so upstream's copy is never
  resurrected. This supersedes the earlier inert-by-default stance (Z13
  §3.3/§6 updated, capabilities.yaml updated). Discoverability is
  unconditional; ACTIVATION is conditional (skill descriptions + AGENTS.md
  Wails section + router separation + Wails-only sync tool) — a plain Go
  project never applies a UI rule or copies a UI file.
- **D-2026-08-08-03 (kit-audit gains a read-only ui-kit dimension)**: the
  audit prompt detects pin drift (PIN.md SHA vs upstream HEAD) and routes
  the maintainer to the manual update workflow; it never syncs itself
  (audit safety contract + Z13 "no silent updates").

## Merged root AGENTS.md + v2.6.0 (2026-08-08, owner mission)

- **D-2026-08-08-04 (merged root AGENTS.md)**: `KitV2/AGENTS.md` is now the
  single agent file for the kit — it merges the pinned `ui-kit/AGENTS.md`
  instructions into a dedicated "UI work — Wails projects" section (adapted
  to the kit's reality, never deformed; EVERY instruction from both files
  preserved — no instruction may be dropped during a merge). The section
  carries a checksum marker (`<!-- ui-kit/AGENTS.md sha256: … -->`); the
  re-sync helper `.agent/sync-ui-kit-from-upstream.sh` refuses to finish when
  the marker drifts, forcing the maintainer to update the merged prose +
  marker at every SDK update (Z13 §4, update-ui-kit prompt updated). Written
  per the agent-instructions skill (dense, non-redundant, layer-1
  discipline). The pinned `ui-kit/AGENTS.md` stays untouched (Z13 verbatim
  mirror).
- **D-2026-08-08-05 (release v2.6.0)**: the ui-agent-kit integration release
  — pinned ui-kit zone at cd00eb5d (0.1.1), single registration point in
  root settings.json, merged root AGENTS.md, separate UI routing corpus
  (11 scenarios), hardened re-sync helper, zero pi-lens blocking errors.
  Version bumped 2.5.0 → 2.6.0 across manifest.yaml, capabilities.yaml,
  install.sh, README.md; router meta regenerated. Full gate PASS; installer
  verified end-to-end.
- **D-2026-08-08-06 (workspace-init — form factor and name)**: the day-0
  project foundation protocol ships as the workflow skill
  `.pi/skills/workspace-init/SKILL.md` (category `workflow`), not a prompt:
  Z8 role boundary (procedures = skills, checklists = prompts), the
  `setup-matt-pocock-skills` precedent (one-shot init), and the need for
  `references/` + document templates. Name `workspace-init` (owner
  arbitration 2026-08-08): names what it produces (`workspace/`).
  Governance zone Z14 = `.agent/kit-governance/24-zone-workspace-init.md`
  (modeled on Z12).
- **D-2026-08-08-07 (workspace-init — strongly recommended, not
  blocking)**: the protocol is suggested by the skill and the kit
  AGENTS.md "Project Foundation" section for a new consumer project, never
  a hard gate; a skipped init is recorded in project memory. No MANDATORY
  lexeme on this subject (charter §16.1.4 / Z8 rule 6); the skill's
  process absolutes ("never write before validation", "never re-run over
  an existing workspace/", "never lose AGENTS.md content") are recorded in
  the enforcement registry `.agent/instructions.md` as guidance-only
  (2026-08-08, Z14).
- **D-2026-08-08-08 (workspace/ layout)**: consumer-side capture =
  `workspace/CONSTITUTION.md` (adapted from the spec-kit constitution
  template: mission, core principles, kernel-first mandate, stack
  decisions, governance with semver), `ARCHITECTURE.md` (kernel/modules
  boundary, one-line module contracts, SDK plan), optional `DOMAIN.md`
  (glossary, grill-with-docs pattern), `decisions/` (D-YYYY-MM-DD-NN,
  same format as this file), `research/` (dated, sourced notes). The
  documents are produced at runtime in the consumer project — never
  shipped by the kit (like `structure.md`, Layer 5.1); the shipped
  `references/templates/*.md` are **document gabarits**, not Z5 code
  templates.
- **D-2026-08-08-09 (AGENTS.md placeholder mechanics, reverse of Z13)**:
  `KitV2/AGENTS.md` carries a generic "Project Foundation" pointer
  section; the init session writes the per-project section into the
  consumer's AGENTS.md under an identifiable marker
  (`<!-- workspace-init sha256: <hash of CONSTITUTION.md + ARCHITECTURE.md> -->`).
  Content is project-owned (written from the local session, never synced
  from the kit), existing content is never lost, uninitialized projects
  get no noise. The ui-kit merge precedent (Z13 §4) provides the marker
  mechanics; the flow direction is inverted.
- **D-2026-08-08-10 (spec-driven-dev articulation)**: the skill's "Before
  You Begin" continuity check now inventories `workspace/` (reads
  CONSTITUTION.md + ARCHITECTURE.md when present) and Phase 0 must be
  consistent with them — one bullet + one line, composition without
  duplicating spec-driven-dev logic (owner arbitration 2026-08-08). The
  interview is adapted from the `grilling` primitive (mattpocock/skills),
  the kernel/modules definition cites Mark Richards, the SDK rationale
  cites Ousterhout (deep modules) — never home-made definitions.
