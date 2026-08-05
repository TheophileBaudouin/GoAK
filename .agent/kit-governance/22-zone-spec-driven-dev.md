# Z12 — Zone `spec-driven-dev` (workflow de transformation à grande échelle)

- **Contrat MetaProjet** — régit `KitV2/.pi/skills/spec-driven-dev/` et
  `KitV2/.pi/skills/deep-discuss/` (skills de workflow), plus la discipline
  de review findings-first fusionnée dans `KitV2/.pi/skills/go-code-review/`.
- **Origine** : intégration de la logique du dépôt MIT
  `zhu1090093659/spec_driven_develop` (v1.15.0) adaptée au kit et au harnais
  Pi — décisions D-2026-08-05-16…20, analyse
  `docs/research/2026-08-05-spec-driven-dev-analysis.md`, plan
  `docs/plans/2026-08-05-spec-driven-dev-integration.md`.

## 1. Mission

Le workflow de référence du kit pour les **transformations à grande échelle**
(rewrite, migration, overhaul, refactor de tout un projet) : pipeline en sept
phases (0-6) — capture d'intention, analyse profonde avec santé S.U.P.E.R,
raffinement ancré, décomposition avec lots de livraison, suivi inter-sessions
(MASTER.md), exécution confirmée avec contrôle adaptatif, archive. Il remplace
l'ancienne chaîne de prompts `workflow-clarify → plan → tasks → implement →
verify` (supprimée le 2026-08-05) et compose les ressources restantes du kit
(`workflow-memory`, `go-*`, `kit-resource-routing`, `go-code-review`) par
cross-références — jamais par duplication.

## 2. Format

```text
KitV2/.pi/skills/spec-driven-dev/
├── SKILL.md                    # phases 0-6, frontmatter complet (category: workflow)
└── references/
    ├── behavioral-rules.md     # 19 règles non négociables
    ├── super-philosophy.md     # S.U.P.E.R + frontière avec les règles du kit
    ├── adaptive-control.md     # télémetry, drift, seuils, réponses
    ├── parallel-protocol.md    # dispatch/review tiercés, writer model
    └── templates/              # analysis, plan, progress, governance, archive
```

`KitV2/.pi/skills/deep-discuss/SKILL.md` : discussion structurée 7 phases.

## 3. Règles

1. **Mode local uniquement** : pas de GitHub (Issues/Milestones/PRs/gh CLI) —
   décision utilisateur D-2026-08-05-18. Le suivi vit dans
   `docs/progress/` (MASTER.md + fichiers de phase) ; les lots de livraison
   sont des unités locales d'intégration/validation, jamais des PR.
2. **Frontière S.U.P.E.R** : S.U.P.E.R est une lentille d'évaluation de santé
   et une checklist de revue, pas une doctrine de conception Go. En cas de
   conflit, les règles sourcées du kit priment (`rules/core/philosophy`,
   `rules/core/universal`) — encodé dans `references/super-philosophy.md` §
   « Frontière avec les règles du kit ».
3. **Contrôle adaptatif obligatoire** : télémetry post-tâche (effort, delta
   S.U.P.E.R, dépendances imprévues), `drift_score` cumulé, seuils 20/40/60 %,
   réponses automatiques annoter/replanifier/ré-évaluer. L'état adaptatif
   persiste dans MASTER.md (jamais seulement en mémoire de conversation).
4. **Archive obligatoire** : phase 6 toujours exécutée ; tous les artefacts
   sous `docs/archives/<projet>/` avec index.
5. **Règle mémoire** (kit, PAS méta-projet) : tout agent utilisant le kit
   vérifie quels fichiers `.pi/memory/` existent réellement — le bootstrap Pi
   ne crée pas `Decisions.md` par défaut. Ne jamais supposer l'ensemble
   standard ; créer les fichiers manquants sans copier d'historique externe.
   Encodé dans `KitV2/AGENTS.md` et `workflow-memory.md`.
6. **Composition, pas duplication** : la skill compose les prompts/skills
   existants (`workflow-memory`, `go-implementation-plan`, `go-code-review`,
   `go-testing-verification`, `kit-resource-routing`) ; elle n'introduit pas
   de second workflow qui répondrait à la même question.
7. **Langue** : corps des skills/références en français, `description:`
   frontmatter en anglais (découvrabilité Pi) — D-2026-08-05-17. Les corps
   anglais pré-existants des skills `go-*` (avant 2026-08-05) restent en
   l'état (grandfathered) ; les sections ajoutées par l'intégration
   spec-driven sont en français — conversion complète des bases anglaises =
   passe dédiée à part.
8. **Sous-agents = décision économique** : dispatch tiercé (Tier 0 défaut,
   Tier 1 un codeur, Tier 2 lanes ≤ 4 disjointes) mappé sur le mécanisme
   natif Pi ; en absence de sous-agents, exécution séquentielle. Les rôles
   spec-driven (project-analyzer, task-architect, task-executor,
   code-reviewer) sont documentés en mapping, jamais livrés comme fichiers.

## 4. Anti-patterns

- Skill spec-driven sans S.U.P.E.R, sans contrôle adaptatif ou sans archive.
- Réintroduction de GitHub/PR dans le workflow local.
- Doublon avec l'ancienne chaîne workflow-* (prompts supprimés ; ne pas les
  recréer).
- S.U.P.E.R imposé comme doctrine de conception Go contre les règles sourcées.
- `Decisions.md` supposé présent sans vérification.
- Prompt ou skill qui ré-explique une référence canonique (single-sourcing).

## 5. Critères de validation (C2 / audit)

- [ ] Frontmatter complet (name == dossier, category: workflow, description EN
      ≤ 1024, tags, last-verified) pour spec-driven-dev et deep-discuss.
- [ ] SKILL.md ≤ 500 lignes ; références `references/**` présentes et liens
      relatifs résolus.
- [ ] Les 3 documents templates de la phase 1 (project-overview,
      module-inventory, risk-assessment) sont couverts par
      `references/templates/analysis.md`.
- [ ] Absence de `github-integration.md` ou de références gh/PR dans la skill.
- [ ] `go-code-review` porte la discipline findings-first (cibles, focus,
      format) sans dépasser 500 lignes.
- [ ] Router indexé (skills : spec-driven-dev, deep-discuss) et
      `--check` vert.
- [ ] Aucun prompt `workflow-{clarify,plan,tasks,implement,verify}` résiduel
      (vérifié par l'audit, catégorie de finding nommée).

## 6. Questions ouvertes

- L'intégration GitHub (GITHUB_FULL/STANDARD) reste écartée par décision
  utilisateur ; à réévaluer seulement si un consommateur en fait la demande
  explicite.
- Les scripts du dépôt source (export-progress.py, install-*.sh,
  review-context.py) ne sont pas portés : pas de surface d'installation
  multi-agent ni de besoin d'export externe dans le kit. À réévaluer avec la
  future CLI `gak`.
