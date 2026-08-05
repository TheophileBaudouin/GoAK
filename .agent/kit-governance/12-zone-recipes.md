# Z3 — Zone `recipes/` (recettes runnables)

- **Contrat MetaProjet** — régit `KitV2/recipes/`.
- **Rapport d'audit :** §2.4. **Décision :** module Go unique (2026-08-04).

## 1. Mission

La couche « comment exécuter cette tâche » : des procédures **ordonnées,
runnables et testées**. Une recette répond à « comment faire X proprement dans
Go » et se termine par un **scénario observable exécuté** — jamais par une
simple compilation.

## 2. Structure d'une recette

```text
recipe-<domaine>-<sujet>/
├── SKILL.md          # frontmatter Pi + corps (progressive disclosure)
├── <code>.go         # package importable (module go-agent-kit-v2)
├── <code>_test.go    # tests ciblés
└── (éventuels fichiers : schema.sql, sqlc.yaml…)
```

## 3. Corps obligatoire de la SKILL.md (modèle : `recipe-worker-pool`)

1. **Problem** — la tâche en une phrase.
2. **Solution** — code minimal qui marche (stdlib ou bibliothèque vétée).
3. **Why not the alternatives** — au moins deux alternatives écartées avec
   verdict (dont la stdlib quand elle suffit).
4. **Verify the behavior (observable)** — commande à exécuter, sorties
   attendues, ce que l'observation prouve.
5. **Run the tests** — la commande de test ; le test ne remplace pas le
   scénario.
6. **Limits** — frontière d'application.
7. **Sources** — primaires.

## 4. Règles

1. **Aucun placeholder** : une recette planifiée est une ligne de roadmap dans
   `recipes/README.md` (avec critères), pas un dossier `.gitkeep`.
2. Nommage : `recipe-<domaine>-<sujet>`, kebab-case ASCII (N1). La recette
   interactive est publiée sous `recipe-cli-interactive` depuis la correction
   post-audit du 2026-08-05.
3. Toute dépendance utilisée par une recette doit être **vétée** dans
   `catalogs/libraries/` (admission 9 critères) — C2 vérifie la correspondance.
4. Une recette référence les patterns/snippets qu'elle utilise (`uses`) et sa
   bibliothèque ; elle ne duplique pas leur code.
5. Les recettes vivent dans le module unique `go-agent-kit-v2` (décision
   2026-08-04) ; une recette à module isolé exige une décision écrite
   (dépendance lourde).
6. Toute recette « cœur » est exercée par une probe (`probes/`) — relation
   `validated_by` (Z6).

## 5. Maintenance

- **Ajout** : code compilant + test + scénario exécuté avec verdict
  (`PASS`/`PARTIAL`/`BLOCKED`) + limites + sources + relations résolues.
- **Modification** : re-run test + scénario ; re-run des probes qui importent la
  recette ; bump `last_verified`/`version` si comportement changé.

## 6. Patterns

- « Verify the behavior » : le scénario est la preuve, pas la compilation.
- Recette ↔ probe : composition (la probe importe la recette), pas duplication.
- Stdlib d'abord : la section « why not » élimine les frameworks quand la
  stdlib suffit.

## 7. Anti-patterns

- Recette écrite sans avoir été exécutée ; verdict affirmé sans exécution.
- Recette qui duplique une autre ou un snippet.
- Dépendance non vétée ; framework choisi pour le confort.
- Placeholder vide qui attend.

## 8. Critères de validation

- [ ] C2 : SKILL.md complète (Problem, Solution, alternatives, scénario,
      limites, sources) et ≤ 500 lignes.
- [ ] C2 : `go test` ciblé + scénario exécuté tracé (verdict explicite).
- [ ] C2 : dépendances ⊆ bibliothèques vétées.
- [ ] Fraîcheur 12/18 mois.

## 9. Questions ouvertes

- Faut-il des « recettes de forme » (shape) distinctes des recettes de tâche ?
  (aujourd'hui les templates sourcés MIT prendront ce rôle — voir Z5.)
- Le renommage `recipe-cli-interactif` → `recipe-cli-interactive` a été
  réalisé le 2026-08-05 ; les références produit et le router sont alignés.
