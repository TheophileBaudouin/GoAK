# Z7 — Zone `tools/` (mécanique de construction et de gate)

- **Contrat MetaProjet** — régit `KitV2/tools/`.
- **Rapport d'audit :** §2.8. **Décision :** `analyzers/` supprimé (2026-08-04).

## 1. Mission

La **mécanique** du Kit — jamais du contenu de connaissance. Les outils
construisent (génération), vérifient (validators), résolvent (offline). Un
outil est testé, documenté, et exécuté par une gate ou en CI.

## 2. Structure et rôles

| Sous-zone | Rôle | État au 2026-08-04 |
| --- | --- | --- |
| `tools/validators/` | Portail de gouvernance exécutable (C2) | actif — à étendre |
| `tools/generators/` | Génération déterministe des index/comptes (INDEX.md, registre, comptes C1) | à créer (premier : générateur d'index) |
| `tools/offline/` | Résolution hors-ligne : manifest + bundle épinglé + attribution | actif, modèle de référence |

`analyzers/` a été supprimé le 2026-08-04 (vide, sans contrat) : l'analyse de
duplication est absorbée par le validateur étendu ; réintroduisible plus tard
uniquement sur décision écrite.

## 3. Règles

1. **Chaque outil = dossier + README** (mission, entrées/sorties, gate qui
   l'exécute) + test. Un outil sans README ni test n'existe pas.
2. **Déterministe et hors-ligne en CI** : pas de dépendance réseau pour les
   générateurs/validateurs.
3. **Un générateur remplace tout index/compte manuel** (C1) : INDEX.md,
   comptes de coverage, registre d'artefacts sont générés puis vérifiés par le
   validateur — jamais écrits à la main.
4. Le validateur reste le **seul** artefact qui peut faire échouer la gate
   produit ; un outil qui mute sans test est une erreur.
5. Aucune logique métier du Kit dans un outil ; un outil n'invente pas de
   connaissance, il la vérifie ou la génère.

## 4. Maintenance

- **Ajout** : mission + test + intégration CI (ou exclusion documentée) +
  mise à jour du README de zone.
- **Modification du validateur** : chaque contrôle nouveau = cas positif +
  cas négatif (tests) ; la sortie reste `PASS`/liste d'erreurs + exit code.

## 5. Patterns

- Un validateur par responsabilité (structure / fraîcheur / cohérence
  manifest) — composables.
- Sortie alignée sur probes : ligne `PASS` ou erreurs actionnables (chemin +
  raison).

## 6. Anti-patterns

- Outil « à voir plus tard » sans contrat (le cas analyzers — corrigé) ;
- constantes en dur qui dérivent (EXPECTED_PRODUCT_SKILLS=45 à dériver, cf. C2) ;
- index générés à la main ; outil non testé ; réseau en CI.

## 7. Critères de validation

- [ ] Tout outil a README + test.
- [ ] Les index/comptes du Kit sont générés (C2 vérifie l'absence de dérive).
- [ ] Gate complète verte (ou PARTIAL documenté).

## 8. Questions ouvertes

- Premier générateur : index knowledge ou registre complet d'artefacts ?
  (proposition : registre complet — il alimente INDEX.md, les comptes C1 et la
  vérification des relations.)
