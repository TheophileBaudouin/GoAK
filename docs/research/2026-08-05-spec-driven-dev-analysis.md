# Analyse en profondeur — zhu1090093659/spec_driven_develop

Date : 2026-08-05. Méthode : clone lecture seule (commit `14f8c0f`, 57
fichiers, 724K) hors du dépôt, lecture de chaque fichier, cartographie du
recouvrement avec le kit. Licence : MIT (LICENSE vérifié). Ce document est la
preuve d'analyse du plan d'intégration `docs/plans/2026-08-05-spec-driven-dev-
integration.md` ; il ne copie pas les corps (traduction/adaptation dans le
kit).

## 1. Structure du dépôt

```text
spec_driven_develop/
├── AGENTS.md / CLAUDE.md              # instructions projet (agents)
├── README.md / README.zh-CN.md        # documentation bilingue
├── plugins/spec-driven-develop/       # plugin autonome
│   ├── .claude-plugin/plugin.json     # manifest Claude Code
│   ├── .codex-plugin/plugin.json      # manifest Codex
│   ├── opencode-plugin.js             # entrée opencode
│   ├── skills/
│   │   ├── spec-driven-develop/       # CŒUR du workflow
│   │   │   ├── SKILL.md               # 7 phases (0-6), v1.15.0
│   │   │   └── references/
│   │   │       ├── behavioral-rules.md    # 19 règles non négociables
│   │   │       ├── super-philosophy.md    # S.U.P.E.R
│   │   │       ├── parallel-protocol.md   # dispatch/review tiercés
│   │   │       ├── adaptive-control.md    # boucle fermée (drift)
│   │   │       ├── github-integration.md  # Issues/Milestones/PRs
│   │   │       └── templates/             # analysis, plan, progress,
│   │   │                                  # governance, archive
│   │   ├── deep-discuss/SKILL.md      # discussion structurée 7 phases (zh)
│   │   └── review-spd/
│   │       ├── SKILL.md               # review findings-first
│   │       ├── references/ (output-format, reviewer-template)
│   │       └── scripts/review-context.py
│   └── agents/ (project-analyzer, task-architect, task-executor,
│                code-reviewer)
├── scripts/ (install-*, validate.sh, export-progress.py, review-context.py)
└── docs/archives/ (2 runs archivés : adaptive-control-layer,
                    orchestrator-centric-execution-model)
```

## 2. Le cœur : 7 phases (SKILL.md spec-driven-develop)

| Phase | Nom | Sortie |
| --- | --- | --- |
| 0 | Quick Intent Capture | énoncé de direction 1-2 phrases |
| 1 | Deep Project Analysis | `docs/analysis/` (project-overview, module-inventory avec scores S.U.P.E.R, risk-assessment avec santé S.U.P.E.R) + pré-vol GitHub |
| 2 | Intent Refinement | définition de tâche confirmée (questions ciblées) |
| 3 | Task Decomposition | `docs/plan/` (task-breakdown, dependency-graph Mermaid, milestones) + delivery batches + états adaptatifs |
| 4 | Progress Tracking | `docs/progress/MASTER.md` + phase files + résolution gouvernance/mémoire |
| 5 | Confirm & Execute | exécution tiercée + review tiercée + batch PR (GitHub) + télémetry adaptative |
| 6 | Archive | `docs/archives/<projet>/` + index |

Concepts structurants : **S.U.P.E.R** (S single purpose, U unidirectional
flow, P ports over implementation, E environment-agnostic, R replaceable
parts + checklist de revue 10 points, scoring 🟢🟡🔴) ; **contrôle adaptatif**
(télémetry effort/SUPER/deps imprévues, drift_score cumulé, seuils 20/40/60 %
→ annotate/replan/rescope) ; **dispatch tiercé** (Tier 0 orchestrateur direct,
Tier 1 un coder, Tier 2 lanes parallèles ≤4 disjointes) ; **review tiercée**
(L1 machine, L2 diff orchestrateur, L3 reviewer indépendant, verdicts
APPROVED/FIXED/ESCALATE) ; **writer model** (orchestrateur = seul writer des
états partagés ; reviewers commitent `fix:` sur la branche lane uniquement) ;
**behavioral rules** (19, dont : jamais sauter de phase, confirmation à chaque
frontière, dual-write des progress, MASTER.md en premier à chaque session,
télémetry obligatoire post-tâche, résolution de gouvernance obligatoire, pas
de truth source concurrente, tests par défaut, learnings durables → mémoire,
sub-agents = décision économique).

## 3. Skills compagnons

- **deep-discuss** (chinois) : 7 phases de discussion structurée (recevoir,
  audit du problème = quality gate, analyse profonde multi-angle avec
  confiances, design 2-3 options, auto-review, revue finale, exécution
  optionnelle « go »). Philosophie : « ne pas se précipiter vers la réponse ».
- **review-spd** : review findings-first ; 3 cibles mutuellement exclusives
  (uncommitted par défaut, date-range avec défaut 3 jours, branche vs main ou
  base explicite) ; planning par taille (petit = Correctness+Tests, moyen = +
  Regression, grand/risque = + Security/Performance) ; 5 focus de reviewers
  (correctness, regression, tests, security, performance) ; format de sortie
  findings-first par sévérité avec Impact/Evidence/Trigger/Fix/Test gap ;
  « No findings » préféré aux findings faibles.

## 4. Agents (prompts de sous-agents Claude Code)

- **project-analyzer** : analyse par focus (architecture & stack, inventaire
  modules avec S.U.P.E.R, risques/tests/gouvernance) ; sortie alignée sur les
  templates analysis.
- **task-architect** : stratégie (bottom-up/top-down/strangler/big-bang),
  phases, tâches (critères d'acceptation checkbox vérifiables indépendamment),
  lanes, delivery batches, milestones, graphe Mermaid, chemin critique.
- **task-executor** : exécute un batch complet ou une lane ; contrat d'entrée
  (batch, tâches, critères, télémetry) ; isolation (pas de PR, pas de closing
  keywords, pas d'états partagés) ; rapport de handoff structuré ; BLOCKED
  explicite.
- **code-reviewer** : reviewer indépendant d'une lane ; vérifie les critères
  d'acceptation en exécutant lui-même les checks ; fixes `fix:` append-only ;
  verdicts APPROVED/FIXED/ESCALATE ; interdictions (pas d'Issues/PRs, pas de
  MASTER.md/drift/gouvernance).

## 5. Scripts

- `validate.sh` : garde de cohérence (références résolues, parité manifest/
  fichiers, version 4 sites, JSON, ESM, py_compile, smoke exporter) —
  équivalent du rôle C2 dans le dépôt source.
- `review-context.py` : collecteur de contexte git (uncommitted / --since/
  --until / --branch --base) — script utilitaire de review-spd.
- `export-progress.py` : export JSON des progress (Linear/Jira/Notion).
- `install-*.sh` : installation multi-agents (Claude/Codex/opencode/Cursor).

## 6. Leçons et pièges du dépôt (utiles à l'adaptation)

- **Skills-only** : les workflows s'invoquent par skills, pas par slash
  commands — le kit doit suivre (skill auto-déclenchée par la description).
- **Single-sourcing** : chaque sujet a exactement un home canonique (une
  référence par topic) ; les prompts ne ré-expliquent jamais, ils citent.
- **Dual-write progress** : pas de point de défaillance unique pour l'état.
- **Tests par défaut** : toute tâche de feature exige des tests, sinon
  raison explicite + validation la plus proche.
- **Gouvernance par défaut** : toute règle stable → surface mémoire résolue ;
  jamais de truth source concurrente ; fallback fichier seulement si choisi.
- **Sub-agents = décision économique** : cold-start tax vs gain de parallélisme.
- **S.U.P.E.R est de la doctrine d'architecture** : Clean/Hexagonal/12-Factor
  — en conflit potentiel avec la doctrine Go sourcée du kit (à borner).

## 7. Cartographie du recouvrement avec le kit (avant intégration)

| spec-driven | Kit existant | Verdict |
| --- | --- | --- |
| Phase 0 intent | aucun | manquant → ajouter |
| Phase 1 analyse profonde | scout/researcher (subagents) | manquant comme phase → ajouter |
| Phase 2 refinement | workflow-clarify | recouvrement → remplacer |
| Phase 3 décomposition | workflow-plan + workflow-tasks | recouvrement → remplacer |
| Phase 4 progress/gouvernance | workflow-memory | recouvrement partiel → adapter |
| Phase 5 exécution | workflow-implement + workflow-verify | recouvrement → remplacer |
| Phase 6 archive | aucun | manquant → ajouter |
| S.U.P.E.R | rules/core/philosophy, universal | conflit doctrinal → borner |
| adaptive control | « 3 échecs → stop » | complémentaire → ajouter |
| review-spd | go-code-review | doublon → fusionner |
| deep-discuss | aucun | complémentaire → ajouter |
| github-integration | aucun (LOCAL_ONLY décidé) | exclu (décision) |
| 4 agents | subagent contracts Pi (scout/planner/worker/reviewer) | mapping documenté |

Décisions d'intégration (utilisateur, 2026-08-05) : remplacer la chaîne
workflow-* par les phases 0-6 ; français + frontmatter EN ; LOCAL_ONLY
uniquement ; bornage par contrat Z12 + audit, sans toucher KIT_CHARTER.md.

## Confiance

Faits vérifiés par lecture directe des fichiers (chemins, numéros de phases,
règles 1-19, checklist 10 points, seuils 20/40/60). Interprétations (leçon
« S.U.P.E.R = doctrine en conflit potentiel », mapping des rôles) étiquetées
comme telles.
