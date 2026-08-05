# Protocole d'exécution parallèle

Ce protocole définit quand et comment l'orchestrateur dispatche des
sous-agents pendant le travail de développement, et comment les résultats
revus sont intégrés. Les tâches sont des unités de travail ; les lots de
livraison sont des unités d'intégration et de validation. Il s'applique à
toute l'implémentation, pas à une phase spécifique.

---

## Admission au dispatch (exécution tiercée)

Le dispatch de sous-agents est une décision économique, pas un défaut. Un
sous-agent paie un coût de démarrage à froid (il relit les tâches, les
fichiers et les règles que tu détiens déjà) et une surcharge d'orchestration
(worktrees, handoffs, intégration). Ne dispatche que quand le gain de
parallélisme et la valeur d'isolation de contexte dépassent ce coût.

Choisis par lot de livraison :

- **Tier 0 — orchestrateur-direct (défaut)** : tâches d'effort S/M, ≤ 3
  fichiers touchés, contexte déjà en main, ou acceptation vérifiable par
  machine. Exécute directement sur la branche d'intégration du lot. Pas de
  sous-agents, pas de worktrees.
- **Tier 1 — un seul codeur** : lots de tâches L/XL, lecture exploratoire
  lourde, ou sorties assez longues pour polluer ton contexte. Délègue le lot
  complet à un sous-agent `worker`.
- **Tier 2 — lanes parallèles** : seulement si TOUT tient — ensembles de
  fichiers de lanes disjoints, chaque lane ≥ L d'effort, chaque lane
  vérifiable indépendamment, et ≤ 4 lanes. Lance un `worker` par lane prête
  dans des worktrees isolés.

Si la plateforme ne supporte pas les sous-agents, exécute toutes les tâches
séquentiellement toi-même (Tier 0).

---

## Admission à la revue (revue tiercée)

Applique le niveau de revue le moins coûteux qui correspond au risque :

- **L1 — validation machine (toujours)** : checks d'acceptation ciblés plus
  validation combinée du lot.
- **L2 — revue du diff par l'orchestrateur (défaut)** : tu lis le diff
  intégré contre les critères d'acceptation de chaque tâche.
- **L3 — reviewer indépendant (réservé)** : un reviewer par lane (skill
  `go-code-review`). Obligatoire pour chaque lane Tier 2 et pour tout travail
  à haut risque : changements de contrats/formats de portage, code logique,
  invariants sémantiques transverses.

Modèle writer (voir `behavioral-rules.md` règles 18-19) :

- Chaque lane Tier 2 reçoit exactement un `worker` (codeur), puis exactement
  un reviewer, dans le même worktree sur la même branche de lane.
- Le reviewer vérifie le diff de la lane contre les critères d'acceptation
  par tâche et commite des corrections directement sur la branche de lane —
  commits `fix:` append-only qui référencent mais ne ferment jamais de tâches.
- Les reviewers n'écrivent jamais MASTER.md, ni l'état de dérive/adaptatif, ni
  les surfaces d'instructions ou de mémoire ; leurs rapports de revue
  reviennent à toi.
- Tu n'intègres que les lanes dont le verdict est APPROVED ou FIXED ;
  ESCALATE est résolu par toi (avec l'utilisateur si besoin). Tu restes
  l'autorité de vérification des critères d'acceptation et le seul writer des
  états partagés.

---

## Quand paralléliser

Au début de chaque phase de développement, lis chaque tâche ouverte de la
phase et consulte `docs/plan/task-breakdown.md` pour les lots de livraison et
les assignations de lanes. Revalide le regroupement planifié contre les
dépendances actuelles, le chevauchenent de fichiers, les tests partagés, le
périmètre de revue, les frontières de rollback et les critères d'admission au
dispatch ci-dessus avant d'éditer.

- Traite les lots de livraison dans l'ordre des dépendances ; ne considère
  pas un lot comme terminé dès qu'une tâche est implémentée.
- Un lot ne qualifie pour le Tier 2 que via les critères d'admission. S'il
  qualifie, dérive des vagues d'exécution prêtes pour les dépendances,
  intègre chaque vague, puis branche la vague suivante sur la base
  d'intégration mise à jour. Chaque lane reçoit le contexte complet du lot
  plus son sous-ensemble de tâches assigné.
- Sinon, exécute au Tier 0 ou Tier 1 — ne force pas le parallélisme.

---

## Comment lancer des exécuteurs de tâches parallèles

Pour chaque lane parallèle de la vague prête pour les dépendances :

1. Prépare l'entrée de chaque `worker` :
   - ID du lot de livraison, but, justification, validation combinée, et
     ensemble ordonné complet des tâches ;
   - ID de lane assigné plus ses IDs et descriptions de tâches du plan ;
   - Critères d'acceptation par tâche, attentes de test et justifications
     explicites de non-test, si présentes ;
   - Impact mémoire/gouvernance par tâche et mises à jour de surface
     attendues, si présentes ;
   - Chemins des fichiers sources pertinents (depuis
     `docs/analysis/module-inventory.md`) ;
   - Standards de codage et contexte de gouvernance projet résolus.
2. Lance tous les agents de lane prêts **dans un seul message** (c'est ainsi
   que les plateformes atteignent le vrai parallélisme). Chaque agent travaille
   dans un worktree isolé pour prévenir les conflits de fichiers. Ne lance pas
   une lane en aval tant que ses commits prérequis ne sont pas intégrés.
   - Suis la convention de branche du dépôt ; sinon chaque lane utilise
     `work/{batch_id}-{lane_id}-{slug}`. Les agents de lane committent leur
     travail et renvoient des références de branche/commits, mais ne créent
     pas d'états partagés.
3. Quand un codeur revient DONE, dispatche un reviewer pour la lane (revue
   L3) avec : l'ID de lane, son sous-ensemble de tâches et les critères
   d'acceptation par tâche (la checklist du reviewer), le rapport de handoff
   du codeur, la branche + chemin du worktree et les commandes de validation
   de lane. Le reviewer vérifie le diff, commite des corrections sur la
   branche de lane, et renvoie un rapport de revue (verdict APPROVED | FIXED |
   ESCALATE). Résous ESCALATE avant d'intégrer cette lane.
4. Quand toutes les lanes portent un verdict APPROVED ou FIXED, consolide
   leurs résultats :
   - Vérifie le rapport de revue de chaque lane et re-vérifie toi-même les
     critères d'acceptation (L2) ;
   - Consolide les commits de lane sur la branche d'intégration du lot
     (`batch/{batch_id}-{slug}` sauf convention du dépôt) ; règle les conflits
     là ;
   - Exécute les checks ciblés de chaque tâche plus la validation combinée du
     lot pour vérifier la cohérence de l'intégration ;
   - Vérifie les critères d'acceptation de chaque tâche terminée et poste sa
     télémetry par tâche (y compris la télémetry du reviewer, enregistrée une
     fois ici). Dans les runs parallèles, l'orchestrateur est le seul writer
     de la dérive cumulée, de MASTER.md et de l'état adaptatif ;
   - Vérifie que les mises à jour de surfaces d'instructions ou de mémoire
     signalées sont cohérentes et ne créent pas de sources de vérité
     concurrentes.

---

## Synchronisation de la progression

Après que l'orchestrateur a consolidé un lot de livraison :

- Applique les rapports de complétion des lanes au fichier de progression de
  la phase une fois ; les agents de lane n'écrivent pas l'état partagé.
- Mets à jour MASTER.md avec les compteurs de complétion finaux précis.
- Mets à jour l'outil de suivi natif de la plateforme pour refléter toutes les
  tâches terminées.
- Réconcilie les mises à jour de surface mémoire des agents parallèles avant
  de continuer.
- Garde les surfaces d'instructions résolues alignées si une lane a changé
  les instructions d'agent au niveau projet.

---

## Atténuation du risque de fusion

`task-breakdown.md` inclut des évaluations de risque de fusion pour les lanes
parallèles. Applique ces gardes :

- **Risque faible** : fusionne librement — les lanes touchent des fichiers
  différents.
- **Risque moyen** : fusionne séquentiellement, exécute les tests entre chaque
  fusion.
- **Risque élevé** : envisage d'exécuter ces tâches séquentiellement au lieu
  d'en parallèle, ou utilise l'isolation par worktree avec résolution de
  conflits soigneuse.

---

## Validation d'architecture post-intégration

Après que la suite de tests passe sur les résultats parallèles intégrés,
effectue ces contrôles au niveau architecture. Ils vont au-delà de la
correction fonctionnelle pour vérifier l'intégrité structurelle entre les
frontières de lanes.

### Conformité S.U.P.E.R inter-lanes

Vérifie que l'exécution parallèle n'a pas introduit de violations
inter-lanes :

- **S (Rôle unique)** : aucun module n'a gagné de responsabilités depuis
  plusieurs lanes.
- **U (Flux unidirectionnel)** : aucune dépendance circulaire introduite entre
  du code touché par des lanes différentes.
- **P (Ports)** : les contrats d'interface aux frontières de lanes restent
  intacts — si la lane A a changé l'API d'un module, l'usage de la lane B s'y
  conforme toujours.
- **R (Remplaçable)** : aucune lane n'a créé de couplage implicite rendant les
  modules d'une autre lane plus difficiles à remplacer.

### Télémetry agrégée

Après avoir consolidé les résultats parallèles d'un lot de livraison,
agrège la télémetry du contrôle adaptatif :

1. Somme uniquement les contributions `task_drift` renvoyées par les agents de
   lane et pas encore enregistrées.
2. Ajoute cette somme au `drift_score` cumulé une fois dans MASTER.md.
3. Évalue les seuils contre le nouveau score cumulé.
4. Si un seuil est dépassé → déclenche la réponse appropriée (voir
   `references/adaptive-control.md` § « Actions de réponse automatiques »)
   AVANT de démarrer le lot de livraison suivant.
