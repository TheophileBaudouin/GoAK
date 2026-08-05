# Tâches — recipes prioritaires KitV2 (2026-08-05)

| ID | État | Tâche | Dépend de |
| --- | --- | --- | --- |
| PR-01 | PASS | Créer plan, ledger de sources et décisions durables. | — |
| PR-02 | PASS | Admettre golang-migrate v4.19.1 et mettre à jour le pattern migrations. | PR-01 |
| PR-03 | PASS | Ajouter les dépendances Go admises et vérifier le graphe module. | PR-02 |
| PR-04 | PASS | Implémenter session scs, tests et probe. | PR-03 |
| PR-05 | PASS | Implémenter JWT HS256, tests et probe. | PR-03 |
| PR-06 | PARTIAL | Implémenter pgx/migrations et test réel tagué ; exécution réelle bloquée. | PR-02, PR-03 |
| PR-07 | PASS | Implémenter slog/expvar, tests race et probe. | PR-01 |
| PR-08 | PASS | Implémenter validation OpenAPI, tests et probe. | PR-03 |
| PR-09 | PASS | Mettre à jour roadmap, capacités, versions, dérive et mémoires. | PR-04 à PR-08 |
| PR-10 | PASS | Générer routeur et exécuter la validation complète. | PR-09 |
| PR-11 | BLOCKED | `DATABASE_URL` absente ; aucun PostgreSQL jetable n'a été contacté. | PR-06 |
| PR-12 | BLOCKED | Réviseur fresh-context indisponible (limite de service), sans lecture ni écriture. | PR-10 |
