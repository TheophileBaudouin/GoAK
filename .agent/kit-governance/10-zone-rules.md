# Z1 — Zone `rules/` (règles)

- **Contrat MetaProjet** — régit `KitV2/rules/`.
- **Rapport d'audit :** §2.1. **Décision :** budget core ≤ 6 modules / ≤ 300
  lignes approuvé (2026-08-04).

## 1. Mission

La couche « doit toujours être vrai » du Kit (charte Layer 1). Les règles
répondent à « qu'est-ce qui doit rester vrai pour tout code Go généré ou
revu ? » — elles ne contiennent jamais d'implémentation.

## 2. Structure

- `rules/core/` — règles **universelles, chargées chaque session** (coût
  permanent) : `philosophy`, `concurrency`, `errors`, `universal`,
  `validation/{golangci-lint,gosec,govulncheck}`.
- `rules/registry/` — règles de **domaine chargées à la demande** :
  `doc-comments`, `logging`, `testing` (exemples).

## 3. Règles de frontière (inviolables)

1. **core ≠ registry** : une règle core ne référence jamais un module registry
   (les universelles ne dépendent pas du chargé-à-la-demande).
2. Une règle ne contient pas de code de production (charte §3) — au plus un
   extrait minimal de démonstration lié à son impératif.
3. Une règle ne duplique pas un pattern/anti-pattern de `knowledge/` — elle le
   référence (relation explicite).
4. Rien d'autre que des règles dans ce dossier : ni recettes, ni mémoire, ni
   contrats.

## 4. Budget de compacité core (décision 2026-08-04)

- **≤ 6 modules** dans `rules/core/` ; **≤ 300 lignes** par SKILL.md.
- **Unité de compte : « module » = dossier top-level de `rules/core/`
  contenant au moins une SKILL.md** (5 au 2026-08-04 : concurrency, errors,
  philosophy, universal, validation — `validation/` compte pour 1 module même
  s'il contient 3 SKILL.md).
- Tout ajout core au-dessus du budget est **bloqué** : il exige une décision
  écrite (Decisions.md) et le retrait/regroupement d'un module existant.
- Contrôle C2 : décompte des modules (dossiers top-level) + taille max par
  fichier.

## 5. Schéma d'une règle (obligatoire — cf. modèle `testing`)

1. **Impératif** : la règle, en une phrase actionnable.
2. **Quand appliquer** : périmètre d'application.
3. **Frontière** : ce que la règle ne couvre PAS (explicite).
4. **Contre-exemples** : cas où la règle semble s'appliquer mais non.
5. **Vérification** : comment contrôler la conformité (commande, grep, review).
6. **Sources** : primaires, vérifiées.

## 6. Maintenance

- **Ajout core** : décision écrite + budget re-vérifié (C2 bloque au-delà).
- **Ajout registry** : admission = source primaire + frontière + vérification
  actionnable + absence de contradiction avec les règles existantes.
- **Modification** : bump `version` (major si plus stricte) + `last_verified` +
  vérification des artefacts qui référencent la règle.

## 7. Patterns

- Une règle = un impératif vérifiable + un « ne couvre PAS ».
- Les règles core citent les sources officielles (Effective Go, Code Review
  Comments, Go Proverbs) et seulement les autres règles core.

## 8. Anti-patterns

- Règle vague (« use idiomatic Go ») sans frontière ni vérification.
- Ajout « just this once » dans core (dérive du budget permanent).
- Règle qui contient un corps de pattern (duplication knowledge/).
- `.md` vides (régression déjà corrigée — C2 la détecte).

## 9. Critères de validation

- [ ] C2 : budget core (≤ 6 modules, ≤ 300 lignes) vérifié.
- [ ] C2 : schéma de règle complet (impératif, frontière, vérification,
      sources).
- [ ] C2 : aucune référence core → registry.
- [ ] Fraîcheur 12/18 mois (C0).

## 10. Questions ouvertes

- `universal` (renommé 2026-08-04) : vérifier que son contenu est bien core et
  pas registry (revue au prochain audit).
- Faut-il une règle core « budget de session » chiffrée autre que le nb de
  modules ?
