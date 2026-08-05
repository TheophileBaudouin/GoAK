# Reconstruction des recipes historiques — KitV2 2.4.0

- Date : 2026-08-05
- Auteur : Agent KitV2
- Statut : En cours (Plan approuvé)

## Objectifs

Reconstruire les 10 recipes historiques pour atteindre la qualité et le niveau de preuve 2.3.0 :
1. SKILL.md réécrits au format de référence complet (≤ 500 lignes chacun, 11 sections canoniques).
2. Façade `NewModel()` ajoutée à TUI de manière non cassante.
3. Remplacement de la probe combinée `worker-shutdown` par 2 probes distinctes `worker-pool` et `graceful-shutdown`.
4. Ajout des 5 probes dédiées pour cobra, koanf, viper, interactive, et desktop (total 15 recipes, 15 probes).
5. Alignement des métadonnées `manifest.yaml`, `capabilities.yaml`, `router/meta.json` et `router/index.json` en version `2.4.0`.

## Décisions & Évidence

- Les décisions sont enregistrées dans `.pi/memory/Decisions.md` sous la section "Reconstruction recipes historiques 2.4.0 (2026-08-05)".
- Le travail s'effectue en préservant le worktree et toutes les API publiques existantes.
