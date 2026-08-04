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
4. `INDEX.md` est **censé être** généré (C2 compare à l'arborescence —
   contrôle contracté C2 §2, générateur en attente) ; en attendant, contrôle
   de revue (Z2 §9.3) et aucun domaine fantôme.
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

## 9. Pipeline de complétion du graphe (bibliothèque du catalogue)

Déclencheur : une bibliothèque admise dans `catalogs/libraries/` (ou un
pointeur promu) doit être couverte par le graphe ; toute demande de
complétion suit ce pipeline — **une bibliothèque à la fois, jamais en
parallèle** ; une bibliothèque n'est terminée que pipeline complet fait.

### 9.1 Étapes obligatoires (dans l'ordre)

1. **Analyse** — lire la ressource existante (catalog SKILL.md, artefacts
   liés) ; résumer rôle, fonctionnalités, écosystème, cas d'usage, pièges.
2. **Audit de couverture** — comparer la couverture existante du graphe (grep
   des ids et des questions par dossier) ; lister manques réels, incomplets,
   doublons, obsolètes.
3. **Recherche documentaire** — par thème (security, performance,
   observability, architecture, patterns, anti-patterns, stdlib) ; sources
   primaires uniquement (docs officielles, spec, issues officielles, GHSA,
   CWE, OWASP) ; vérifier chaque URL ajoutée.
4. **Question utilisateur** — seulement si décision éditoriale non dérivable
   par analyse/recherche ; une question à la fois ; jamais une question dont
   la réponse est trouvable par analyse.
5. **Planification** — `docs/plans/<date>-<slug>.md` : fichiers à créer et à
   modifier, ressources, dépendances.
6. **Découpage** — micro-tâches atomiques, vérifiables, indépendantes (todo).
7. **Exécution** — une bibliothèque entièrement finie avant la suivante ;
   conformité et cohérence vérifiées après chaque artefact.
8. **Validation** — gate complète (voir 9.3).
9. **Rapport** — par bibliothèque + global : fichiers, recherches, décisions,
   questions, problèmes, restants ; évidence brute dans
   `docs/evidence/<date>/<slug>/`.

### 9.2 Admission d'un artefact de complétion (manques réels)

- **Admission C0 §4** (question distincte — ni règle, ni recette, ni
  pattern/anti-pattern, ni catalog — et source primaire vérifiée, URL
  vivante) ; spécifique pipeline : vérifier les Notes des catalogs, qui
  couvrent souvent les limites d'une bibliothèque (contrôle de revue).
- **Schéma complet** de la catégorie (Z2 §3) et métadonnées Z10.
- **Une question = un artefact** : le volume non justifié est un échec
  d'admission, pas une option.
- **`debugging/` reste vide** par contrat (Z2 §7) : un échec n'y entre que
  observé, vérifié, avec procédure actionnable.
- **Paires référencées** quand l'homologue existe (Z2 §4.2 ; convention du
  corpus : le pattern pointe son homologue négatif, l'anti-pattern référence
  ses sources primaires).
- **Catalog admis = fiche complète** : tout SKILL.md de `catalogs/libraries/`
  porte les 6 sections décisionnelles obligatoires du format fiche (N1 §4)
  avant admission ; les sections préexistantes (Selection, Admission, Minimal
  use, Alternatives, Notes) sont conservées.

### 9.3 Contrôles de sortie (vérifiables)

- [ ] C2 : `validate-kitv2.py` PASS — métadonnées, relations résolues, router
      (schémas par catégorie et fraîcheur 12/18 mois : contrôles contractés,
      en attente d'implémentation).
- [ ] C2 : router régénéré après tout ajout/suppression de YAML knowledge
      (`python3 .agent/router/build_index.py --check` PASS).
- [ ] Contrôle de revue : `knowledge/INDEX.md` à jour (générateur en attente,
      Z2 §4) ; zéro domaine fantôme.
- [ ] Contrôle de revue : aucune URL morte dans `relationships.references`
      (spot-check des ajouts) ; aucune duplication de question.
- [ ] Gate C0 §8 : validators + gate Go + probes.

Le write-gate C0 §4, la revue fresh-context C0 §6.3 et la décision écrite
(Decisions.md) s'appliquent sans être dupliqués ici.

## 10. Questions ouvertes

- Les 6 YAML de découverte (awesome-go, go-by-example…) restent YAML Source —
  confirmé par la décision (pointeurs).
- Faut-il un domaine `cloud/` réel (INDEX le mentionne) ? Tant qu'aucun
  artefact cloud n'est admis, le domaine n'existe pas (règle 5).
- Le pipeline §9 est-il vérifiable automatiquement (une checklist C2
  « complétion par bibliothèque ») ou reste-t-il un contrôle de revue ?
