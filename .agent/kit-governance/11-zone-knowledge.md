# Z2 — Zone `knowledge/` (graphe de décision sourcé)

- **Contrat MetaProjet** — régit `KitV2/knowledge/`.
- **Rapport d'audit :** §2.2, §2.3. **Décision :** bibliothèques SKILL.md vétées
  - pointeurs YAML séparés (2026-08-04).

## 1. Mission

La couche « pourquoi / quand choisir » : le graphe de décision sourcé du Kit.
Un artefact de connaissance répond à **une question distincte** qu'aucune règle
ou recette ne couvre, et cite sa source primaire. Il n'est jamais le corps d'une
règle/recette (charte §4) ni la mémoire du metaprojet.

## 2. Sous-domaines et formats (règle de choix)

| Sous-domaine | Format | Contenu type |
| --- | --- | --- |
| `patterns/` | YAML-graphe | solutions réutilisables (schéma positif) |
| `anti-patterns/` | YAML-graphe | échecs sourcés (schéma négatif) |
| `stdlib/` | YAML-graphe | **pointeurs-only** vers sources officielles |
| `catalogs/libraries/` | **SKILL.md** (vétées, admission 9 critères) | décisions de sélection |
| `catalogs/libraries/pointers/` | YAML-graphe Source | pointeurs « à considérer » (prévu par décision 2026-08-04, non créé à ce jour) |
| `catalogs/reference-projects/` | SKILL.md | projets **extract-only** |
| `catalogs/*.yaml` (découverte) | YAML-graphe Source | index de découverte (awesome-go, …) |
| `security/`, `performance/`, `observability/`, `architecture/`, `debugging/` | YAML-graphe | guidance sourcée par domaine |

## 3. Schémas obligatoires

**Pattern (positif)** : `problem` (contexte), `context` (quand), `solution`,
`benefits`, `costs`, `related` (+ homologues négatifs référencés).

**Anti-pattern (négatif)** : `symptom`, `detect` (contrôles actionnables),
`problem`, `fix`, `when_ok` (+ homologue positif référencé quand il existe).

**Source / pointeur** : `source` (URL), `selection` (quand le charger),
`limits` (ce qu'il ne prouve pas), `relationships.references`.

## 4. Règles

1. Admission : source primaire + question distincte + schéma complet + relations
   résolues (C2).
2. Les paires pattern/anti-pattern se référencent mutuellement (règle : tout
   anti-pattern admet un homologue positif quand il existe).
3. **Promotion pointeur → module vété** : admission 9 critères passée, usage
   réel, maintien vérifié, `last_verified` frais — la promotion est une
   décision écrite et déplace le fichier vers `catalogs/libraries/`.
4. `INDEX.md` est **généré** (C2 compare à l'arborescence) — jamais maintenu à
   la main ; aucun domaine fantôme.
5. Un domaine vide n'existe pas : soit ≥ 1 artefact actif, soit un README
   contrat + roadmap (`debugging/` — voir §7).
6. `knowledge/` n'héberge ni historique metaprojet ni évidence brute.

## 5. Patterns

- Pointer-only pour les sources officielles massives (stdlib) : zéro copie de
  corps, résolution via `tools/offline/`.
- Paires référencées pattern ↔ anti-pattern (déjà en place — généraliser).
- « Une question, un artefact » : détectable par C2 (recherche de
  titres/questions en double).

## 6. Anti-patterns

- Deux formats pour le même rôle sans contrat (le cas `libraries/` de
  l'audit — décidé le 2026-08-04 ; migration en cours, voir §4.3).
- Artefact « utile » sans source ; source sans question distincte.
- Duplication d'un corps de recette/règle.
- INDEX ou comptes manuels.

## 7. `debugging/` (cas particulier)

Contrat de domaine déjà écrit dans `KitV2/knowledge/debugging/README.md` :
admission sur échec observé et vérifié uniquement, schéma Source/Pattern,
roadmap de candidats (fuite de goroutine, course flaky, deadlock, lenteur).
Le dossier reste vide tant que l'évidence n'est pas admise — c'est un choix,
pas un vide accidentel.

## 8. Critères de validation

- [ ] C2 : schéma par catégorie vérifié (sections obligatoires).
- [ ] C2 : relations résolues ; paires référencées.
- [ ] C2 : fraîcheur 12/18 mois ; INDEX généré à jour.
- [ ] Promotion pointeur → module : décision écrite tracée.

## 9. Questions ouvertes

- Les 6 YAML de découverte (awesome-go, go-by-example…) restent YAML Source —
  confirmé par la décision (pointeurs).
- Faut-il un domaine `cloud/` réel (INDEX le mentionne) ? Tant qu'aucun
  artefact cloud n'est admis, le domaine n'existe pas (règle 5).
