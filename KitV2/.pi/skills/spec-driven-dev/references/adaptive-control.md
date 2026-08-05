# Protocole de contrôle adaptatif

Boucle fermée de contrôle pour le workflow Spec-Driven Develop : comment la
télémetry d'exécution est collectée, comment la dérive plan-vs-réalité est
mesurée, et quelles actions correctives automatiques se déclenchent quand la
dérive dépasse les seuils.

---

## Concepts centraux

| Concept de théorie du contrôle | Mapping workflow |
|:---|:---|
| **Système** | Le codebase sous transformation |
| **Point de consigne** | Définition de tâche confirmée (phase 2) + principes S.U.P.E.R |
| **Contrôleur** | La skill workflow (phases 0-6) + ce protocole |
| **Actionneur** | Exécuteurs de lots et workers de lanes |
| **Capteur** | Collecte de télémetry post-tâche |
| **Signal d'erreur** | `drift_score` — écart cumulé plan-vs-réalité |

---

## Collecte de télémetry

Après avoir terminé chaque tâche et AVANT de la marquer comme terminée,
collecte trois signaux.

### Effort réel

Compare l'effort estimé (depuis `task-breakdown.md`) à l'effort réel :

| Niveau | Critères |
|:---|:---|
| S | Terminé en < 30 minutes, aucun problème inattendu |
| M | 30 min – 2 heures, surprises mineures |
| L | 2 – 4 heures, ou complexité inattendue significative |
| XL | > 4 heures, ou remise en cause fondamentale |

Enregistre le **delta d'effort** en niveaux entre estimé et réel (estimé M /
réel M → 0 ; S → L → +2 ; L → M → -1).

### Delta de score S.U.P.E.R

Exécute la checklist en 10 points de `super-philosophy.md` § « Checklist de
revue de code S.U.P.E.R ». Enregistre `super_score` (passes sur 10) et
`super_delta` (variation vs l'état pré-tâche). Pas d'amélioration là où les
drivers S.U.P.E.R de la tâche promettaient une amélioration → delta = 0 (compté
comme écart) ; régression → négatif.

### Dépendances imprévues

Compte les dépendances découvertes pendant l'exécution qui n'étaient PAS dans
le champ « Dependencies » de la tâche : fichiers non listés modifiés, tâches
prérequises non identifiées, bibliothèques/API externes ayant nécessité des
changements.

---

## Calcul du score de dérive

### Contribution de dérive par tâche

```text
task_drift = max(0, effort_delta) + (1 si super_delta <= 0 ET la tâche avait
des drivers S.U.P.E.R sinon 0) + min(deps_imprevues, 2)
```

Seuls les deltas d'effort positifs comptent. Les dépendances imprévues sont
plafonnées à 2 par tâche.

### Score de dérive cumulé

```text
drift_score = somme de tous les task_drift des tâches terminées
```

### Seuils en pourcentage

Relatifs au **nombre total de tâches de la phase courante**, calculés une fois
au début de la phase :

```text
threshold_annotate = ceil(total_tasks * 0.20)
threshold_replan   = ceil(total_tasks * 0.40)
threshold_rescope  = ceil(total_tasks * 0.60)
```

---

## Actions de réponse automatiques

### Annoter (dérive ≥ threshold_annotate)

Écart léger ; le plan reste viable. Automatiquement :

1. Ajoute une ligne d'avertissement à l'entrée de la prochaine tâche dans le
   fichier de phase (LOCAL_ONLY).
2. Mets à jour l'état adaptatif (§ « Stockage de l'état adaptatif »).

### Replanifier (dérive ≥ threshold_replan)

Écart significatif ; la décomposition restante est probablement inexacte.
Automatiquement :

1. **HALTE** — ne démarre pas la tâche suivante.
2. Annote le MASTER.md :

```text
   🔄 Adaptive Control: Replanning triggered (drift_score={n}).
   Remaining tasks will be re-decomposed based on execution learnings.
   ```

3. **Re-entre en phase 3** pour le périmètre restant uniquement, en utilisant
   la télémetry des tâches terminées comme entrée d'estimation ; préserve les
   tâches terminées ; crée de nouvelles tâches sous la même phase.
4. Réinitialise `drift_score` à 0 pour le segment replanifié.
5. LOCAL_ONLY : archive les anciennes entrées du fichier de phase et crée les
   nouvelles.

### Ré-évaluer (dérive ≥ threshold_rescope)

Écart sévère ; le périmètre ou la stratégie peut être fondamentalement faux.
Automatiquement :

1. **HALTE**.
2. Ajoute l'annotation de ré-évaluation dans MASTER.md :

```text
   ## Adaptive Control: Scope Re-evaluation

   drift_score has reached {n}, exceeding the rescope threshold of {threshold}.

   ### Execution Summary
   | Metric | Value |
   |--------|-------|
   | Tasks completed | X/Y |
   | Average effort delta | +Z levels |
   | SUPER improvement rate | N% |
   | Unplanned dependencies | W total |

   ### Recommendation
   The current scope/strategy appears misaligned with project reality.
   Returning to Phase 2 for scope confirmation with the user.
   ```

3. **Re-entre en phase 2** avec les données d'exécution accumulées comme
   contexte.
4. Après re-confirmation du périmètre par l'utilisateur, re-entre en phase 3
   pour tout le travail restant.
5. LOCAL_ONLY : même flux via les annotations de MASTER.md.

---

## Stockage de l'état adaptatif (LOCAL_ONLY)

**Stockage principal** : `docs/progress/MASTER.md` — section « Adaptive
Control State » :

```markdown
## Adaptive Control State

| Field | Value |
|-------|-------|
| drift_score | 0 |
| strategy | bottom-up |
| threshold_annotate | 2 |
| threshold_replan | 4 |
| threshold_rescope | 6 |
| total_tasks | 10 |
| completed_tasks | 0 |
| last_updated | 2026-05-17 |

### Task Telemetry Log

| Task ID | Est. | Actual | Δ Effort | SUPER Score | SUPER Δ | Unplanned Deps | Task Drift |
|---------|------|--------|----------|-------------|---------|----------------|------------|
```text

---

## Activation du contrôleur

### Début de session

Au début de chaque conversation, APRÈS la lecture de MASTER.md :

1. Lis la section « Adaptive Control State » de MASTER.md.
2. Parse `drift_score` et les seuils.
3. Si `drift_score` dépasse déjà un seuil (d'une session précédente),
   déclenche la réponse AVANT d'exécuter une nouvelle tâche.
4. Rapporte l'état adaptatif dans le statut d'ouverture de la session.

### Post-tâche

Pour l'exécution séquentielle, après chaque tâche terminée :

1. Collecte la télémetry (§ « Collecte de télémetry »).
2. Calcule la contribution de dérive de la tâche et le nouveau
   `drift_score` cumulé (§ « Calcul du score de dérive »).
3. Persiste l'état adaptatif mis à jour (§ « Stockage de l'état
   adaptatif »).
4. Écris la télémetry dans MASTER.md avec le score cumulé mis à jour.
5. Si un seuil est dépassé → exécute la réponse AVANT la tâche suivante ;
   sinon continue.

Pour les lanes parallèles, les exécuteurs de lanes font les étapes 1-2 et
renvoient leur télémetry par tâche, mais jamais les étapes 3-5 —
l'orchestrateur enregistre et applique les contributions une fois par lot,
empêchant les incréments dupliqués et les écritures concurrentes.

### Post-intégration de lot

Après avoir consolidé tout le travail d'un lot de livraison :

1. Collecte toute télémetry de lane pas encore enregistrée.
2. Ajoute la somme des seules contributions non enregistrées à
   `drift_score` une fois ; persiste.
3. Écris la télémetry de chaque tâche non enregistrée dans MASTER.md avec le
   score cumulé post-lot.
4. Vérifie que la télémetry existe pour chaque tâche du lot.
5. Si un seuil est dépassé → déclenche la réponse AVANT le lot de livraison
   suivant.

---

## Intégration au workflow

| Phase du workflow | Intégration du contrôle adaptatif |
|:---|:---|
| Phase 3 (Décomposition) | Initialise l'état adaptatif ; calcule les seuils. |
| Phase 4 (Suivi) | MASTER.md inclut la section télémetry et l'état adaptatif. |
| Phase 5 (Exécution) | Chaque tâche terminée déclenche « Post-tâche » ; chaque intégration de lot déclenche « Post-intégration ». |
| Phase 6 (Archive) | L'archive inclut le résumé de télémetry final et l'historique de dérive comme rétrospective. |
