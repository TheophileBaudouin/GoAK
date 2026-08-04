# Z4 — Zone `snippets/` (vues vérifiées d'implémentation canonique)

- **Contrat MetaProjet** — régit `KitV2/snippets/`.
- **Rapport d'audit :** §2.5.

## 1. Mission

Des fragments de code **métadonnés, vérifiés et liés à une source canonique**
(recette, règle ou pattern). Un snippet n'est jamais une seconde implémentation :
c'est une vue focalisée de code qui vit canoniquement ailleurs.

## 2. Structure d'un snippet

```text
<sujet>/
├── SNIPPET.yaml   # métadonnées
├── example.go     # fragment compilant, autonome
└── check.sh       # vérification EXÉCUTANTE (compile + run/assertions)
```

## 3. SNIPPET.yaml — champs obligatoires (modèle : `bounded-worker`)

`id`, `type` (domaine), `purpose`, `tags`, `go_version`, `dependencies`,
`when_to_use`, `avoid_when`, `source` (**chemin relatif résolu** vers la
recette/règle/pattern canonique), `complexity`, `files`, `tests`.

## 4. Règles

1. **`source` obligatoire et résolue** : C2 vérifie que le chemin existe et
   pointe vers un artefact canonique ; un snippet orphelin est un échec.
2. **`check.sh` exécute réellement** : au minimum compilation + exécution du
   fragment (ou assertions) — un check qui ne vérifie que `gofmt` est
   insuffisant (régression détectée à l'audit : `errors-once/check.sh`).
3. Les snippets ne remplacent pas la taxonomie : la catégorie = domaine du
   graphe (concurrency, database, http, …). **Aucune catégorie vide** : les
   catégories planifiées vivent en roadmap dans `snippets/README.md`.
4. Un snippet n'introduit pas de nouvelle connaissance : s'il faut du nouveau
   contenu, c'est une recette/pattern qui l'héberge, le snippet pointe.
5. `go_version` = version minimale testée.

## 5. Maintenance

- **Ajout** : compil + check.sh exécutant vert + source canonique résolue +
  métadonnées complètes + fraîcheur.
- **Modification** : re-run check.sh ; vérifier que la source canonique n'a pas
  changé de forme (sinon mettre à jour le snippet ou le retirer).

## 6. Patterns

- Un snippet = un point de vue sur un artefact existant, jamais un nouveau
  corps de connaissance.
- check.sh minimaliste mais réel : `go run` + assertions, ou `go test` d'un
  package jetable.

## 7. Anti-patterns

- Snippet orphelin ; snippet qui devient la référence (dérive) ; check qui ne
  vérifie rien ; catégorie vide qui attend ; code non compilant.

## 8. Critères de validation

- [ ] C2 : SNIPPET.yaml complet (champs §3).
- [ ] C2 : `source` résolu ; `check.sh` compilant **et** exécutant.
- [ ] Fraîcheur 12/18 mois.

## 9. Questions ouvertes

- Frontière avec `knowledge/stdlib/` : stdlib = pointeurs de docs, snippets =
  code exécutable. Une table de routage « question → snippet ou stdlib ? »
  est-elle utile ? (proposition : non — la description L1 du snippet suffit.)
