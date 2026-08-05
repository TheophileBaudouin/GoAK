---
name: spec-driven-dev
category: workflow
tags: [spec-driven, workflow, planning, analysis, s-u-p-e-r, adaptive-control, large-scale, migration, refactor]
last-verified: 2026-08-05
description: "Spec-driven development workflow for large-scale Go transformations (rewrite, migration, overhaul, whole-project refactor). Use when the user requests a large-scale project transformation that needs deep analysis, phased task decomposition, progress continuity across sessions, and execution within one session — not for ordinary single-task work. Runs the seven-phase pipeline: intent capture, deep analysis with S.U.P.E.R health scoring, grounded intent refinement, task decomposition with delivery batches, progress tracking (MASTER.md), confirmed execution with adaptive control, and archive. Local-only: no GitHub dependency. Composes the kit's existing prompts and skills (memory, planning, review, testing) instead of duplicating them."
---

# Spec-driven develop

Tu exécutes le workflow **Spec-Driven Development** — un pipeline en sept
phases (0-6) pour les transformations à grande échelle. Termine les phases de
préparation (analyse, planification, mise en place du suivi), puis exécute le
plan — le tout dans une seule session.

**Règles comportementales** : `references/behavioral-rules.md` — lis-les et
suit-les à chaque phase ; elles sont non négociables.

## Configuration

| Chemin | Défaut | Rôle |
|:---|:---|:---|
| Sortie analyse | `docs/analysis/` | documents de la phase 1 |
| Sortie plan | `docs/plan/` | documents de la phase 3 |
| Sortie suivi | `docs/progress/` | documents de suivi (dont MASTER.md) |
| Surfaces d'instructions | résolues par projet | contraintes projet pour les agents (phase 4) |
| Surface mémoire | `.pi/memory/` d'abord | faits durables via la mémoire native de l'agent ; pas de fallback fichier silencieux |
| Sortie archive | `docs/archives/<projet>/` | artefacts archivés (phase 6) |
| Mode de suivi | `LOCAL_ONLY` | workflow local pur (aucune dépendance GitHub) |
| Lots de livraison | par phase | lots = unités locales d'intégration et de validation |
| Contrôle adaptatif | activé | seuils de dérive : annoter=20 %, replanifier=40 %, ré-évaluer=60 % des tâches de phase |

**Références canoniques** (chaque sujet a exactement un home — cite-le, ne le
ré-explique jamais) :

| Référence | Possède |
|:---|:---|
| `references/behavioral-rules.md` | Toutes les règles comportementales (1-19) |
| `references/adaptive-control.md` | Collecte de télémetry, calcul de dérive, actions de réponse, stockage d'état, activation du contrôleur |
| `references/parallel-protocol.md` | Admission dispatch/review (tiers), protocole lanes/worktree, boucle de revue, risque de fusion, contrôles post-intégration |
| `references/super-philosophy.md` | Principes S.U.P.E.R + checklist de revue en 10 points |
| `references/templates/` | Schémas de chaque document généré (analysis, plan, progress, governance, archive) |

## Avant de commencer : continuité inter-sessions

**CRITIQUE** : avant toute phase, inventorie et lis les surfaces
d'instructions et de mémoire existantes du projet (`AGENTS.md`, la mémoire
native `.pi/memory/` — **vérifie quels fichiers sont réellement présents,
`Decisions.md` peut manquer au bootstrap** — tout fichier de règles
plateforme existant).

Puis vérifie si `docs/progress/MASTER.md` existe déjà :

- S'il **existe** : lis-le immédiatement. Tu reprends une tâche en cours.
  Identifie la phase courante et le travail accompli ; continue exactement là
  où la session précédente s'est arrêtée. Ne redémarre pas à la phase 0.
- S'il **n'existe pas** : nouveau départ. Passe à la phase 0.

Après chargement de l'état, peuple l'outil de suivi natif de la plateforme
(ex. todo) avec les tâches en attente de la phase active : contenu = description
de la tâche, statut = in-progress pour la tâche active, priorité mappée
P0=high, P1=medium, P2=low. Si aucun outil natif n'existe, saute cette étape —
MASTER.md suffit.

---

## Phase 0 : capture rapide de l'intention

**But** : capturer la direction générale de la transformation en 1-2 phrases —
juste assez pour donner un axe à l'analyse de la phase 1.

**Actions** :

1. Extrais du message de l'utilisateur : le type de transformation, l'état
   cible approximatif, et les contraintes explicitement énoncées.
2. Résume la direction en 1-2 phrases. Ne pose PAS de questions approfondies
   ici — l'analyse de la phase 1 révélera quoi demander. Confirme :
   « Je comprends que tu veux [direction]. Laisse-moi d'abord analyser le
   projet actuel pour te poser les bonnes questions. »
3. Si l'intention est totalement floue, pose UNE question de haut niveau pour
   déterminer le type de transformation.

**Sortie** : un énoncé de direction préliminaire guidant la phase 1. PAS la
définition finale de la tâche — elle vient en phase 2.

---

## Phase 1 : analyse profonde du projet

**But** : construire une compréhension complète du codebase actuel, éclairée
par la direction de la phase 0.

**Actions** :

1. Avant d'analyser, appelle `search_kit_resources` (skill
   `kit-resource-routing`) pour router vers les règles, recettes et
   catalogues pertinents — ne scanne pas l'arbre du kit manuellement.
2. Lance les analyses en parallèle (sous-agents `scout`/`researcher` si
   disponibles, sinon toi-même séquentiellement), découpées par focus :
   - **Architecture & Stack** : structure, arborescence, stack technique,
     points d'entrée, commandes de build/run.
   - **Inventaire des modules** : responsabilité, surface d'API publique,
     taille, dépendances — évalués contre les cinq principes S.U.P.E.R avec
     un score par principe.
   - **Risques, Tests & Gouvernance** : risques de transformation, hotspots
     de complexité, conventions, couverture de tests, surfaces
     d'instructions/mémoire — plus un résumé de santé S.U.P.E.R avec les
     hotspots de violation (cibles prioritaires du plan).
   Donne à chaque analyse la direction de la phase 0 ET
   `references/super-philosophy.md`.
3. Consolide les sorties, résous les contradictions, et écris les documents
   `docs/analysis/` depuis `references/templates/analysis.md` :
   `project-overview.md`, `module-inventory.md` (scores S.U.P.E.R par module),
   `risk-assessment.md` (résumé de santé S.U.P.E.R).

**Sortie** : `docs/analysis/` complet (trois documents). L'évaluation
S.U.P.E.R est la ligne de base architecturale de toutes les phases suivantes.

---

## Phase 2 : raffinement et confirmation de l'intention

**But** : avec le projet analysé, finaliser la définition de la tâche par une
discussion ancrée dans l'analyse.

**Actions** :

1. Présente les résultats clés de la phase 1 : résumé d'architecture bref,
   problèmes de santé S.U.P.E.R notables, points de couplage/complexité
   pertinents pour la transformation.
2. Pose des **questions ciblées ancrées dans l'analyse** — spécifiques et
   informées, pas génériques (ex. sur les dépendances circulaires trouvées,
   les hypothèses d'environnement codées en dur, les contrats d'interface
   manquants). Utilise l'outil de questions structuré de la plateforme
   (`ask_user_question` dans Pi) — jamais du texte brut. Confirme au minimum :
   - **Périmètre** — quels modules de l'inventaire sont dans le périmètre ;
   - **Cible** — technologie/architecture/état cible ;
   - **Contraintes** — délais, compatibilité ascendante, bibliothèques,
     cibles de déploiement ;
   - **Priorités** — performance, maintenabilité, parité de fonctionnalités
     (utilise l'évaluation des risques) ;
   - **Priorités S.U.P.E.R** — quelles violations corriger maintenant vs
     différer ;
   - **Politique de test** — quelles couches de test protègent les
     changements ; faut-il établir un harnais de test minimal s'il n'y en a
     pas ;
   - **Gouvernance du projet** — surfaces d'instructions canoniques ; surface
     mémoire native ou fallback explicitement nommé.
3. Résume la compréhension raffinée et obtiens une confirmation explicite.

**Sortie** : la définition de tâche autoritaire et confirmée guidant les
phases 3-6.

---

## Phase 3 : décomposition de la tâche

**But** : décomposer la transformation en tâches gérables et traçables,
organisées en phases, avec des lanes parallèles et des lots de livraison
cohérents.

**Actions** :

1. Lance l'architecte de tâches (sous-agent `planner` si disponible, sinon
   toi-même) avec l'analyse complète de la phase 1 ET la définition confirmée
   de la phase 2. Si plusieurs stratégies sont plausibles, explore 2 approches
   différentes (ex. bottom-up vs strangler fig) et garde le meilleur résultat.
   Compose la logique de planification du kit (`go-implementation-plan`,
   artefact de plan, registre de sources) — ne duplique pas.
2. La décomposition doit produire :
   - **Phases** ordonnées par dépendance ; les phases précoces priorisent la
     correction des hotspots de violation S.U.P.E.R avant les nouvelles
     fonctionnalités.
   - **Tâches**, chacune avec : description, priorité (P0/P1/P2), effort
     (S/M/L/XL), dépendances, drivers de design S.U.P.E.R, critères
     d'acceptation, attente de test, et impact mémoire/gouvernance. Les
     critères d'acceptation de chaque tâche incluent implicitement le passage
     du S.U.P.E.R Quick Check pour ses principes listés.
     - **Tests par défaut** : les tâches qui changent des fonctionnalités
       visibles, du comportement, des contrats d'API, des schémas, des
       migrations, du parsing, du routage, des permissions, du cache ou de la
       persistance DOIVENT ajouter ou mettre à jour des tests automatisés ;
       les tâches de documentation/config peuvent marquer tests N/A avec une
       raison explicite.
     - **Gouvernance par défaut** : les tâches qui introduisent une règle
       stable, un gotcha ou une convention doivent inclure la mise à jour de
       la surface mémoire résolue (et des surfaces d'instructions si la règle
       affecte les futurs agents).
   - **Lanes d'exécution parallèles** par phase : regroupe les tâches
     mutuellement indépendantes ; évalue le risque de fusion (chevauchenent de
     fichiers).
   - **Lots de livraison** (unités locales, pas de PR) : après revue de
     l'ensemble des tâches de la phase (dépendances, chevauchenent de
     fichiers, validation partagée, risque de rollout, frontière de
     rollback), assigne chaque tâche à exactement un lot. Défaut : un lot
     cohérent par phase ; ne divise que pour une raison documentée de
     revueabilité, de release/rollback, de propriété, d'isolation de risque,
     de dépendance ou de politique. Enregistre par lot : ID, but, IDs de
     tâches, vagues d'exécution, lanes, branche d'intégration, validation
     combinée, ordre de dépendance, raison de division.
   - **Graphe de dépendances** en diagramme Mermaid (sous-graphes pour les
     frontières de lots et les lanes) et **jalons** aux frontières de phases.
3. Écris les documents `docs/plan/` depuis `references/templates/plan.md` :
   `task-breakdown.md`, `dependency-graph.md`, `milestones.md`.
4. **Initialise l'état du contrôle adaptatif** : pour chaque phase, calcule
   les seuils de dérive en pourcentage et ajoute le bloc adaptatif YAML à
   MASTER.md (phase 4) conformément à `references/adaptive-control.md` §
   « Stockage de l'état adaptatif ».

**Sortie** : `docs/plan/` complet (trois documents) avec état adaptatif
initialisé.

---

## Phase 4 : documentation du suivi de progression

**But** : créer un système de suivi de progression et de gouvernance qui
survit aux conversations.

**Actions** :

Utilise `references/templates/progress.md` pour les documents de progression
et `references/templates/governance.md` pour les enregistrements de
gouvernance.

### Surface de gouvernance du projet

1. **Inventorie les surfaces existantes** : fichiers d'instructions partagés
   (`AGENTS.md` ou équivalent), règles plateforme existantes, et la mémoire
   native de l'agent `.pi/memory/` — **vérifie quels fichiers mémoire existent
   réellement** (le bootstrap Pi peut ne créer que Brief/Progress/Gotchas/
   Agent, sans `Decisions.md`) ; ne suppose jamais l'ensemble standard.
2. **Mets à jour les surfaces d'instructions sans écraser** : règles partagées
   → `AGENTS.md` ; règles plateforme existantes seulement si elles existent ou
   sont demandées. Préserve les sections écrites par l'utilisateur, les
   commandes locales et les contraintes de sécurité. Si une règle existante
   entre en conflit avec le plan, ne la remplace pas silencieusement — enregistre
   le conflit dans MASTER.md et demande à l'utilisateur au prochain point de
   contrôle.
3. **Résous la surface mémoire** : préfère la mémoire native `.pi/memory/` ;
   ne crée jamais silencieusement un fichier mémoire Markdown de secours ;
   utilise un fallback repo-local seulement sur confirmation utilisateur ou
   déclaration existante du projet. Enregistre la résolution dans MASTER.md
   « Governance Status ».

Ne crée pas de sources de vérité concurrentes.

### Suivi local (`LOCAL_ONLY`)

1. Crée `docs/progress/MASTER.md` : nom/description de la tâche, mode
   `LOCAL_ONLY`, liens vers les documents d'analyse/plan, table de synthèse
   des phases, liens vers les fichiers de phase, « Current Status »,
   « Next Steps ».
2. Crée un `docs/progress/phase-N-<nom-court>.md` par phase : tâches en
   checkbox avec critères d'acceptation inline plus une section « Notes ».
3. Ajoute la section « Adaptive Control State » et une table « Task Telemetry
   Log » à MASTER.md conformément à `references/adaptive-control.md` §
   « Stockage de l'état adaptatif ».

### Commun à tous les modes

- Les phases utilisent `- [ ] Phase N: <nom> (0/X tâches)` liant le fichier de
  phase ; `- [x] Phase N: <nom> (X/X tâches)` quand terminé.
- « Current Status » est mis à jour au début et à la fin de chaque session de
  travail.

**Sortie** : `docs/progress/` complet avec MASTER.md et les fichiers de phase.

---

## Phase 5 : confirmation et exécution

**But** : présenter les artefacts de préparation, obtenir la confirmation,
puis exécuter le plan.

**Actions** :

### 5a. Résumé et confirmation

1. Présente : définition de la tâche (phase 2), résultats clés (phase 1),
   plan par phases avec comptes de tâches (phase 3), aperçu des lots de
   livraison et raisons de division (phase 3), description du système de
   progression (phase 4), et le modèle d'exécution (dispatch tiercé :
   orchestrateur-direct par défaut ; sous-agents exécuteur/reviewer selon
   `references/parallel-protocol.md` § « Admission au dispatch »).
2. Liste tous les artefacts générés (documents d'analyse, plan et
   progression ; surfaces d'instructions et de mémoire résolues).
3. Demande à l'utilisateur : « Toute la préparation est terminée. Prêt à
   commencer l'exécution ? » (outil de questions structuré).

### 5b. Exécution

1. **Traite chaque phase séquentiellement.** Avant d'éditer, relis les tâches
   ouvertes de la phase et revalide les lots planifiés contre les dépendances
   actuelles, les fichiers affectés, le périmètre de revue et les règles du
   dépôt. Si le mapping doit changer, mets à jour `task-breakdown.md`,
   MASTER.md et le champ « Delivery Batch » de chaque tâche affectée ;
   commente la raison du regroupement pour que toutes les surfaces
   d'exécution concordent.
2. **Choisis le tier d'exécution de chaque lot** selon les critères
   d'admission de `references/parallel-protocol.md` § « Admission au dispatch
   (exécution tiercée) » :
   - **Tier 0 — orchestrateur-direct (défaut)** : effort S/M, ≤ 3 fichiers,
     contexte déjà en main, ou acceptation vérifiable par machine. Exécute
     directement sur la branche d'intégration du lot.
   - **Tier 1 — un seul codeur** : lots L/XL ou exploration lourde en
     contexte. Délègue le lot complet à un sous-agent `worker`.
   - **Tier 2 — lanes parallèles** : seulement si TOUT tient — ensembles de
     fichiers de lanes disjoints, ≥ L d'effort par lane, vérifiabilité
     indépendante, ≤ 4 lanes. Lance un `worker` par lane prête dans des
     worktrees isolés, en vagues, chacun avec le contexte complet du lot plus
     son sous-ensemble de tâches. Les agents de lane ne créent jamais de PR
     ni d'états partagés.
   - Convention de branche : celle du dépôt ; sinon
     `batch/{batch_id}-{slug}` (intégration) et `work/{batch_id}-{lane_id}-
     {slug}` (lanes Tier 2).
3. **Revue avant intégration** selon `references/parallel-protocol.md` §
   « Admission à la revue (revue tiercée) » :
   - **L1 — validation machine (toujours)** : checks ciblés de chaque tâche
     plus validation combinée du lot.
   - **L2 — revue du diff par l'orchestrateur (défaut)** : lis le diff
     intégré contre les critères d'acceptation de chaque tâche.
   - **L3 — reviewer indépendant (réservé)** : un reviewer par lane, obligatoire
     pour les lanes Tier 2 et le travail à haut risque (contrats/formats de
     portage, code logique, invariants sémantiques transverses) — utilise la
     skill `go-code-review`. Verdict APPROVED | FIXED | ESCALATE ; n'intègre
     que les lanes APPROVED ou FIXED ; résous ESCALATE toi-même (avec
     l'utilisateur si besoin). Tu restes l'autorité de vérification des
     critères d'acceptation et le seul writer des états partagés.
4. **Après chaque tâche** — suis `references/adaptive-control.md` §
   « Activation du contrôleur » : collecte la télémetry, mets à jour le
   `drift_score` cumulé, écris la télémetry dans MASTER.md, et exécute les
   réponses automatiques aux seuils. Pour les lanes parallèles, les agents
   de lane renvoient leur télémetry par tâche et tu l'enregistres une fois
   lors de l'intégration du lot.
5. **Intègre et valide chaque lot** : consolide les branches de lane revues
   sur la branche d'intégration du lot ; règle les chevauchenents ; exécute
   les checks par tâche plus la validation combinée et les contrôles
   d'architecture post-intégration ; vérifie toi-même les critères
   d'acceptation de chaque tâche terminée (L2). Un lot = une intégration
   validée (commit local ou branche selon la convention du dépôt) ; pas de PR.
6. **Mises à jour de progression** : coche les tâches dans les fichiers de
   phase ; mets à jour les comptes de MASTER.md ; connaissance durable →
   surface mémoire résolue (`.pi/memory/`) ; changements de comportement
   d'agent → surfaces d'instructions résolues.
7. **Quand toutes les tâches sont terminées** (toutes les cases cochées) :
   passe à la phase 6.

**Sortie** : toutes les tâches planifiées implémentées et vérifiées.

---

## Phase 6 : archive

**Déclencheur** : toutes les tâches terminées — toutes les cases `[x]`.

**But** : archiver tous les artefacts du workflow pour traçabilité, puis
nettoyer les répertoires de travail.

**Actions** :

1. Annonce la fin à l'utilisateur.
2. Détermine le nom du répertoire d'archive depuis le nom de la tâche de la
   phase 2 (minuscules, tirets, pas de caractères spéciaux) :
   `docs/archives/<nom-du-projet>/`. Structure cible et index :
   `references/templates/archive.md`.
3. Déplace `docs/analysis/`, `docs/plan/` et `docs/progress/` dans
   l'archive ; copie des instantanés ou notes d'export pour les surfaces
   d'instructions et de mémoire résolues dans
   `docs/archives/<nom-du-projet>/governance/` ; déplace tout autre fichier
   temporaire du workflow.
4. Crée ou met à jour `docs/archives/README.md` avec une entrée : nom du
   projet, description en une ligne, plage de dates, lien vers le MASTER.md
   archivé.
5. Supprime les répertoires désormais vides `docs/analysis/`, `docs/plan/`,
   `docs/progress/`. Garde les surfaces d'instructions et de mémoire actives
   en place ; seuls leurs instantanés vivent sous l'archive.
6. Suggère à l'utilisateur de committer l'archive dans le contrôle de
   version.

**Sortie** : tous les artefacts sous `docs/archives/<nom-du-projet>/` avec un
index `docs/archives/README.md` à jour.
