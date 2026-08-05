# Plan — Intégration spec-driven-dev dans le kit Go Agent Kit (mise à jour majeure)

## Goal

Intégrer toute la logique du dépôt `zhu1090093659/spec_driven_develop` (MIT,
v1.15.0) dans le kit : le workflow spec-driven en 7 phases (0-6), la
philosophie S.U.P.E.R, le contrôle adaptatif (drift/telemetry), le protocole
d'exécution tiercé, les templates de documents, deep-discuss et la discipline
de review findings-first — **adaptés au harnais Pi et aux règles existantes du
kit, traduits en français sans dénaturer la logique**, puis bornés dans la
gouvernance méta-projet (contrat Z12 + kit-audit) pour que cet atout majeur
soit toujours pris en compte.

## Context

### Analyse du dépôt source (vérifiée par clone lecture seule, commit 14f8c0f)

- **Cœur** : `plugins/spec-driven-develop/skills/spec-driven-develop/SKILL.md`
  (7 phases : 0 intent, 1 analyse profonde, 2 refinement, 3 décomposition, 4
  progress/governance, 5 confirm+exécution, 6 archive) + 6 références
  (behavioral-rules 19 règles, super-philosophy S.U.P.E.R, adaptive-control,
  parallel-protocol, github-integration, templates analysis/plan/progress/
  governance/archive).
- **Skills compagnons** : `deep-discuss` (discussion structurée 7 phases, en
  chinois) et `review-spd` (review findings-first, 3 cibles : uncommitted /
  date-range / branche-PR, 5 focus de review).
- **Agents** : project-analyzer, task-architect, task-executor, code-reviewer
  (prompts de sous-agents Claude Code).
- **Scripts** : review-context.py (collecteur git), export-progress.py,
  validate.sh (garde de cohérence), install-*.sh.
- Analyse détaillée : `docs/research/2026-08-05-spec-driven-dev-analysis.md`.

### État du kit (vérifié)

- Chaîne workflow existante : `.pi/prompts/workflow-{clarify,plan,tasks,
  implement,verify}.md` (5 prompts, indexés au router : prompt=8) +
  `workflow-memory.md`, `checklist-api.md`, `checklist-release.md`.
- Skills `.pi/skills/` : go-code-review, go-idiomatic-implementation,
  go-implementation-plan, go-source-retrieval, go-testing-verification,
  kit-resource-routing (6, indexés au router : skill=6).
- `KitV2/AGENTS.md` dit « Use the native `.pi/prompts/` workflow templates in
  order » — à remplacer.
- Contrat Z8 (17-zone-pi.md) cite `workflow-clarify`, `workflow-plan`, … en
  exemple du rôle « prompts = orchestrateurs » — à mettre à jour.
- `workflow-memory.md` initialise la mémoire consommateur sans mentionner que
  le bootstrap Pi peut ne pas créer `Decisions.md`.

### Décisions utilisateur (2026-08-05, questions posées)

1. **Stratégie : remplacer la chaîne existante.** Les phases 0-6 deviennent LE
   workflow du kit ; les 5 prompts workflow-*sont supprimés (migration
   documentée). La skill spec-driven-dev compose les prompts/skills restants
   (workflow-memory, go-*, kit-resource-routing) par cross-références.
2. **Langue : français + frontmatter EN.** Corps des skills/références en
   français (style kit-audit), `description:` frontmatter en anglais
   (découvrabilité Pi, format validé).
3. **Périmètre : LOCAL_ONLY uniquement.** Pas de GitHub (Issues/Milestones/
   PRs/gh CLI) : workflow local pur (docs/analysis, plan, progress, archives),
   delivery batches = unités d'intégration/validation locales (sans PR).
   Sous-agents : le protocole tiercé est conservé mais mappé sur le mécanisme
   natif Pi (subagent tool) et reste une décision économique ; en absence de
   sous-agents, exécution séquentielle orchestrateur.
4. **Bornage : contrat Z12 + audit, sans charte.** Nouveau contrat
   `.agent/kit-governance/22-zone-spec-driven-dev.md`, nouvelle dimension et
   catégorie de finding kit-audit, décisions D-2026-08-05-16…, Brief/Progress.
   `KIT_CHARTER.md` inchangé.

### Conflits identifiés à résoudre (adaptation, pas copie)

- **S.U.P.E.R vs doctrine Go sourcée** : S.U.P.E.R s'appuie sur Clean/Hexagonal
  Architecture (U, P) ; le kit refuse la doctrine Clean Code/OOP en défaut
  (AGENTS.md racine) et `rules/core/philosophy` prescrit le plus petit design
  justifié, stdlib-first, sans structure universelle. **Résolution** : S.U.P.E.R
  est conservé comme **lentille d'évaluation de santé** du workflow (scoring,
  hotspots) et comme **checklist de revue**, avec une frontière explicite : en
  cas de conflit avec une règle sourcée du kit (philosophy, universal), la
  règle du kit prime ; P se lit « interfaces consommateur + contrats
  explicites » (doctrine kit), E se lit « configuration par env, zéro chemin
  codé » (déjà kit), R = remplaçabilité (déjà kit), U = direction des
  dépendances consommateur-possédées (déjà kit). Encodé dans la référence
  super-philosophy adaptée + Z12.
- **Progress mémoire vs MASTER.md** : la mémoire consommateur `.pi/memory/`
  (durable) et `docs/progress/MASTER.md` (état du run) sont deux surfaces
  distinctes, non concurrentes — le template governance adapté le dit
  explicitement (« no competing truth sources » conservé).
- **review-spd vs go-code-review** : deux reviews de code = doublon interdit
  (charte §4). **Résolution** : la discipline findings-first de review-spd
  (3 cibles, sévérités, 5 focus, format de sortie) est **fusionnée dans
  go-code-review** (une seule skill de review), pas une skill parallèle.
- **deep-discuss vs workflow-clarify** : clarifier ≈ Phase 2 ; deep-discuss est
  une discussion d'analyse (pas un spec) — complémentaire, aucune duplication.

## Constraints

- Un seul writer sur le worktree ; paralléliser uniquement la recherche en
  lecture (analyse du dépôt source déjà faite).
- Les règles du kit priment sur S.U.P.E.R en cas de conflit (frontière
  explicite ci-dessus).
- Langue : corps FR, frontmatter EN (name/description/category/tags/
  last-verified au format validate-instructions.py ; `category: workflow`).
- Pas de GitHub dans l'adaptation (LOCAL_ONLY) ; pas de fichiers d'agents
  livrés (mapping vers les rôles Pi documenté dans la skill).
- Chaque nouveau SKILL.md ≤ 500 lignes, nom == dossier, description EN ≤ 1024.
- La chaîne remplacée est supprimée APRÈS vérification des références (router,
  Z8, docs) ; aucune référence morte résiduelle.
- Gate complète produit obligatoire (KitV2 est touché) + validateurs
  méta-projet + revue fresh-context.
- Trois échecs identiques → stop et rapport.

## Done when

- Skill `spec-driven-dev` (SKILL.md + references/behavioral-rules.md,
  super-philosophy.md, adaptive-control.md, parallel-protocol.md,
  templates/{analysis,plan,progress,governance,archive}.md) livrée, FR/EN,
  LOCAL_ONLY, frontière S.U.P.E.R encodée.
- Skill `deep-discuss` livrée (FR/EN, adaptée du chinois).
- `go-code-review` augmenté de la discipline findings-first
  (references/reviewer-focus.md + 3 cibles + planning par taille), sans
  dépasser 500 lignes.
- Prompts workflow-{clarify,plan,tasks,implement,verify} supprimés ; router
  régénéré (prompt 8→3, skill 6→8) ; Z8 mis à jour ; AGENTS.md produit mis à
  jour (workflow = spec-driven-dev).
- `workflow-memory.md` adapté : règle « vérifier les fichiers mémoire présents,
  Decisions.md peut manquer au bootstrap Pi » ; règle ajoutée dans
  `KitV2/AGENTS.md` (règle kit, PAS méta-projet).
- Contrat Z12 (`22-zone-spec-driven-dev.md`) + README kit-governance indexé ;
  kit-audit : dimension + catégorie de finding + §5-E ; décisions
  D-2026-08-05-16… ; Brief/Progress/Gotchas à jour.
- Analyse du dépôt source : `docs/research/2026-08-05-spec-driven-dev-analysis.md`.
- Gate complète verte (validators strict+normal, gofmt, vet, lint, test -race,
  gosec, govulncheck, probes) + validateurs méta-projet + revue fresh-context
  APPROVE avant déclaration de fin.

## Étapes / micro-tâches

### A. Analyse (fait)

1. (fait) Clone lecture seule + inventaire 57 fichiers.
2. (fait) Lecture SKILL.md core + 6 références + deep-discuss + review-spd +
   agents + scripts + templates.
3. (fait) Cartographie du recouvrement kit (workflow-* ≈ phases 2-5).
4. (fait) Questions utilisateur (4 réponses : remplacer, FR/EN, LOCAL_ONLY,
   Z12 sans charte).
5. Écrire `docs/research/2026-08-05-spec-driven-dev-analysis.md` (preuve).

### B. Skill spec-driven-dev (KitV2/.pi/skills/spec-driven-dev/)

1. `SKILL.md` — phases 0-6 adaptées : Phase 0 intent ; Phase 1 analyse
   profonde (3 docs, S.U.P.E.R health, recherche kit via search_kit_resources) ;
   Phase 2 refinement (questions structurées, compose go-implementation-plan) ;
   Phase 3 décomposition (compose workflow-tasks logic → tasks + batches
   locaux) ; Phase 4 progress (MASTER.md + phase files, résolution mémoire
   .pi/memory + governance) ; Phase 5 exécution (dispatch tiercé local +
   review tiercée, télémetry adaptative) ; Phase 6 archive. Description EN,
   corps FR, ≤ 500 lignes.
2. `references/behavioral-rules.md` (FR) — 19 règles traduites 1:1, adaptées :
   questions via l'outil structuré Pi (ask_user_question), dual-write progress
   (todo Pi + MASTER.md), mémoire durable → .pi/memory.
3. `references/super-philosophy.md` (FR) — S.U.P.E.R + checklist 10 points,
   avec la section « Frontière avec les règles du kit » (les règles sourcées
   priment).
4. `references/adaptive-control.md` (FR) — télémetry (effort, SUPER delta,
   deps imprévues), drift_score, seuils 20/40/60, réponses annotate/replan/
   rescope, stockage LOCAL_ONLY (MASTER.md), activation session/post-task/
   post-batch.
5. `references/parallel-protocol.md` (FR) — dispatch tiercé (Tier 0 défaut,
    Tier 1 un coder, Tier 2 lanes ≤4 disjointes) mappé sur le mécanisme natif
    Pi ; review tiercée L1 machine / L2 orchestrateur / L3 reviewer indépendant
    (→ skill go-code-review) ; modèle writer (orchestrateur = seul writer des
    états partagés).
6. `references/templates/analysis.md` (FR) — 3 templates (project-overview,
    module-inventory avec scores S.U.P.E.R, risk-assessment avec santé S.U.P.E.R).
7. `references/templates/plan.md` (FR) — task-breakdown (phases, lanes,
    delivery batches locaux), dependency-graph (Mermaid), milestones.
8. `references/templates/progress.md` (FR) — MASTER.md + phase files +
    état adaptatif + journal télémetry.
9. `references/templates/governance.md` (FR) — résolution des surfaces
    (AGENTS.md projet, .pi/memory), règle « vérifier les fichiers mémoire
    présents », pas de truth source concurrente.
10. `references/templates/archive.md` (FR) — archive docs/archives + index.
11. Validation statique : frontmatter complet, ≤ 500 lignes, liens relatifs
    résolus, description EN.

### C. Skills compagnons

1. `KitV2/.pi/skills/deep-discuss/SKILL.md` (FR/EN) — 7 phases adaptées du
    chinois (recevoir, audit problème, analyse profonde, design, auto-review,
    revue finale, exécution optionnelle) ; déclencheurs FR/EN.
2. `KitV2/.pi/skills/go-code-review/` — fusion de la discipline review-spd :
    nouveau `references/reviewer-focus.md` (FR : 5 focus de reviewers, contrat
    de sortie findings-first, mapping de sévérités) ; SKILL.md augmenté (3
    cibles : non-commité / commits / branche ; planning de revue par taille ;
    discipline findings-first) sans dépasser 500 lignes.

### D. Remplacement de la chaîne (migration)

1. Vérifier les références (router index.json, Z8, AGENTS.md produit, docs
    méta-projet historiques = non touchés).
2. `git rm` des 5 prompts workflow-{clarify,plan,tasks,implement,verify}.md.
3. Régénérer le router (`.agent/router/build_index.py`, attendu prompt 8→3,
    skill 6→8) + vérifier `--check`.
4. Mettre à jour `KitV2/AGENTS.md` : section Workflow → spec-driven-dev
    (skill) ; ajouter la règle mémoire kit (vérifier les fichiers .pi/memory
    présents, Decisions.md peut manquer ; ne jamais supposer l'ensemble
    standard).
5. Adapter `KitV2/.pi/prompts/workflow-memory.md` : inventaire réel des
    fichiers mémoire + création des manquants (dont Decisions.md) + pas de
    copie de l'historique méta-projet.

### E. Gouvernance méta-projet (bornage)

1. `.agent/kit-governance/22-zone-spec-driven-dev.md` (Z12) : mission, format
    (SKILL.md + references + templates), règles (LOCAL_ONLY, frontière
    S.U.P.E.R, archive obligatoire, contrôle adaptatif obligatoire, mémoire
    vérifiée, composition des prompts/skills existants, pas de doublon),
    anti-patterns, critères de validation C2 (frontmatter complet, ≤ 500
    lignes, références résolues, 3 docs templates présents, pas de github-
    integration.md), questions ouvertes.
2. `.agent/kit-governance/README.md` : ligne Z12 dans l'index.
3. `.agent/kit-governance/17-zone-pi.md` (Z8) : table des rôles mise à jour
    (exemples = spec-driven-dev, workflow-memory, checklist-*) ; règle
    « workflow = skill spec-driven-dev ».
4. `.pi/prompts/kit-audit.md` : nouvelle dimension C10 « Workflow
    spec-driven-dev » (inventaire skill + références + S.U.P.E.R + contrôle
    adaptatif + archive + absence de fuite GitHub + absence de prompts
    workflow-* résiduels) ; catégorie de finding nommée ; ligne §5-E.
5. `.pi/memory/Decisions.md` : D-2026-08-05-16 (remplacement chaîne),
    -17 (langue FR/EN), -18 (LOCAL_ONLY), -19 (Z12 sans charte),
    -20 (règle mémoire kit).
6. `.pi/memory/Brief.md` : section Workflow mise à jour.
7. `.pi/memory/Progress.md` : tâche de la passe.
8. `.pi/memory/Gotchas.md` : leçons (bootstrap Pi sans Decisions.md ;
    S.U.P.E.R vs doctrine Go ; fusion review-spd→go-code-review).

### F. Validation

1. Gate produit complète (validators strict + normal, gofmt, vet, lint,
    test -race, gosec, govulncheck, probes) + validateurs méta-projet.
2. Revue fresh-context (subagent read-only, C0 §6.3) — intégrer ou trancher.
3. Commit + rapport final (fichiers touchés, checklist audit futur, confiance).

## Actions en attente (hors périmètre de cette passe)

- Aucune implémentation KitV2 différée (cette passe est l'implémentation).
- Hors périmètre volontaire : intégration GitHub (décision LOCAL_ONLY) ;
  scripts install-*/export-progress.py (pas de surface d'installation
  multi-agent dans le kit) ; fichier d'agents livrés (mapping Pi documenté).

## Annexes

### Annexe A — Frontière S.U.P.E.R vs règles du kit (texte à encoder dans super-philosophy.md et Z12)

S.U.P.E.R est la lentille d'évaluation de santé du workflow et une checklist
de revue. Elle n'est PAS une doctrine de conception Go qui remplacerait les
règles sourcées du kit. En cas de conflit, `rules/core/philosophy`,
`rules/core/universal` et les règles applicables priment. Lectures compatibles
: S ≈ responsabilité unique (déjà kit), U ≈ dépendances consommateur-possédées
et direction des imports (déjà kit), P ≈ interfaces consommateur + contrats
explicites et sérialisables (déjà kit), E ≈ config par environnement, zéro
chemin codé (déjà kit), R ≈ remplaçabilité sans effet de bord (déjà kit).
Ce qui est AJOUTÉ par S.U.P.E.R : le scoring par principe (🟢🟡🔴) dans
l'analyse, la checklist de revue en 10 points, les hotspots de violation comme
priorités du plan.

### Annexe B — Mapping des rôles d'agents spec-driven vers le harnais Pi

| Rôle spec-driven | Rôle Pi / kit | Notes |
| --- | --- | --- |
| project-analyzer | scout / researcher (subagent) | analyse par focus, sortie structurée |
| task-architect | planner (subagent) | décomposition + batches |
| task-executor | worker (subagent) | exécute un batch/lane, ne touche pas aux états partagés |
| code-reviewer | reviewer (subagent) + skill go-code-review | verdict APPROVED/FIXED/ESCALATE, fixes `fix:` sur la branche lane |

Les agents ne sont pas livrés comme fichiers : la skill documente le mapping ;
en absence de sous-agents Pi, exécution séquentielle (Tier 0).
