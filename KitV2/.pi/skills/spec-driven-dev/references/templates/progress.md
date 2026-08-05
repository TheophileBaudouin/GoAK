# Templates des documents de progression

Templates des documents de suivi générés en phase 4 (Documentation du suivi
de progression). Sortie vers `docs/progress/`.

---

## MASTER.md (mode LOCAL_ONLY)

```markdown
# MASTER — Spec-Driven Develop Run

## Tâche

**Nom** : <nom de la tâche (phase 2)>
**Mode de suivi** : `LOCAL_ONLY`
**Définition de tâche confirmée** : <lien ou résumé court>

## Documents

- Analyse : [project-overview.md](../analysis/project-overview.md) ·
  [module-inventory.md](../analysis/module-inventory.md) ·
  [risk-assessment.md](../analysis/risk-assessment.md)
- Plan : [task-breakdown.md](../plan/task-breakdown.md) ·
  [dependency-graph.md](../plan/dependency-graph.md) ·
  [milestones.md](../plan/milestones.md)

## Phases

- [ ] Phase 1: <nom> (0/N tâches) — [fichier de phase](phase-1-<nom>.md)
- [ ] Phase 2: <nom> (0/N tâches) — [fichier de phase](phase-2-<nom>.md)

## Gouvernance Status

| Surface | Statut | Notes |
|:--------|:-------|:------|
| `AGENTS.md` | existant / créé / non utilisé | règles agent partagées |
| `.pi/memory/` | vérifié — fichiers présents : | **vérifier quels fichiers existent réellement (Decisions.md peut manquer au bootstrap Pi)** |
| Fallback mémoire | approuvé / non | jamais créé silencieusement |

## Current Status

<état actuel, mis à jour au début et à la fin de chaque session de travail>

## Next Steps

<prochaine action exacte>

---

## Adaptive Control State

| Field | Value |
|-------|-------|
| drift_score | 0 |
| strategy | <stratégie> |
| threshold_annotate | <calculé> |
| threshold_replan | <calculé> |
| threshold_rescope | <calculé> |
| total_tasks | <compte> |
| completed_tasks | 0 |
| last_updated | <ISO-8601> |

### Task Telemetry Log

| Task ID | Est. | Actual | Δ Effort | SUPER Score | SUPER Δ | Unplanned Deps | Task Drift |
|---------|------|--------|----------|-------------|---------|----------------|------------|
```

---

## Fichier de phase (mode LOCAL_ONLY)

Un `docs/progress/phase-N-<nom-court>.md` par phase.

```markdown
# Phase N : <nom de la phase>

**But** : <but de la phase>
**Prérequis** : <ce qui doit être fait avant>

## Tâches

- [ ] **T1.1** — <description>
  - **Priorité** : P0/P1/P2 | **Effort** : S/M/L/XL
  - **Dépend de** : <IDs ou "Aucun">
  - **Lane** : A/B/—
  - **S.U.P.E.R** : <principes>
  - **Critères d'acceptation** :
    - [ ] <critère vérifiable>
    - [ ] Passe le S.U.P.E.R Quick Check pour : <principes>
    - [ ] Satisfait l'attente de test : <tests ou raison de non-test>
    - [ ] Met à jour les surfaces mémoire/instructions résolues si la
          connaissance durable ou les instructions d'agent ont changé

## Notes

<!-- Décisions, conflits, contexte — règle 3 des règles comportementales -->
```
