# Z10 — Registre des artefacts (graphe transversal)

- **Contrat MetaProjet** — schéma transverse appliqué à **chaque** artefact du
  Kit, quelle que soit sa zone.
- **Rapport d'audit :** §2 (graphe), charte §2/§5.

## 1. Mission

Définir le **gabarit de métadonnées et les relations** que `validate-kitv2.py`
applique à chaque artefact : un artefact est accepté si, et seulement si, son
gabarit et ses relations sont complets et résolus.

## 2. Les 10 kinds (charte §2)

`Rule`, `Recipe`, `Pattern`, `Snippet`, `Template`, `Capability`, `Evaluation`,
`DecisionRecord`, `Source`, `Memory`.

| Kind | Vit principalement dans | Format |
| --- | --- | --- |
| Rule | `rules/` | SKILL.md |
| Recipe | `recipes/` | SKILL.md + code |
| Pattern | `knowledge/patterns/` (positif) ; `knowledge/anti-patterns/` (négatif) | YAML-graphe |
| Snippet | `snippets/` | SNIPPET.yaml + code |
| Template | `templates/` | dossier projet MIT (Z5) |
| Capability | `capabilities.yaml` (+ `manifest.yaml`) | YAML |
| Evaluation | `probes/` | main.go |
| DecisionRecord | **metaprojet** (`.pi/memory/Decisions.md`, `docs/`) | Markdown — jamais dans le Kit |
| Source | `knowledge/**` (pointeurs) + `tools/offline/` (bundle) | YAML-graphe / bundle |
| Memory | **metaprojet** (`.pi/memory/`) | Markdown — jamais dans le Kit |

## 3. Métadonnées obligatoires (tous les kinds product)

```text
id:            <kind>:<domaine>:<slug>     (regex C2 : ^(rule|recipe|pattern|snippet|
                                             template|capability|evaluation|decision-record|
                                             source|memory):[^:]+:.+$)
title:         une phrase
kind:          l'un des 10
version:       semver (depuis v2 ; entier existant accepté)
status:        proposed | active | deprecated | rejected
owner:         go-agent-kit (ou équipe/mainteneur déclaré)
tags:          [kebab-case]
go_version:    version minimale testée (jamais future)
dependencies:  []
last_verified: YYYY-MM-DD
```

## 4. Relations autorisées (graphe)

`depends_on`, `uses`, `implements`, `extends`, `references`, `requires`,
`supersedes`, `validated_by`, `generated_from`.

Note de cohérence (2026-08-04) : cette liste correspond exactement à
`GRAPH_RELATIONS` de `validate-kitv2.py`. `extends` est déclaré mais
actuellement **inutilisé** dans le Kit — il reste dans le schéma publié
(aucun retrait de schéma sans décision écrite) ; le Brief du metaprojet omet
`extends` de sa liste — à corriger au prochain touch.

Règles de résolution (C2) :

1. Toute cible d'id stable doit exister dans le registre (ids connus).
2. Toute cible doit être `active` (les relations vers `proposed`/`rejected`/
   `deprecated` sont un échec, sauf `supersedes`/`references` explicites).
3. `references` accepte des URLs (sources primaires) ; les autres relations
   uniquement des ids stables.
4. Le graphe est la vérité ; le dossier n'est que navigation (charte §13).

## 5. Règles de qualité (actionnables)

1. Un artefact = **une responsabilité, une question** ; deux artefacts qui
   répondent à la même question = au moins un fautif (C0).
2. Aucune duplication de corps : les relations remplacent la copie.
3. Un artefact `proposed` est invisible pour les consommateurs ; il ne porte
   pas de relations entrantes depuis de l'`active`.
4. `last_verified` ≤ 12 mois (warning) / 18 (déprécié) — C0/C2.
5. Chaque artefact `active` avec comportement observable est `validated_by` une
   évaluation (probe) ou un scénario exécuté.

## 6. Le registre généré (Z7)

Le registre complet (id, kind, statut, zone, relations) est **généré** par
`tools/generators/` et vérifié par C2 — il remplace tout index manuel et rend
la résolution des relations vérifiable sans base de données.

## 7. Critères de validation

- [ ] C2 : gabarit complet (métadonnées §3) pour tout YAML-graphe et tout
      module SKILL.md product.
- [ ] C2 : relations résolues et règles §4 appliquées.
- [ ] C2 : fraîcheur et unicité de question (duplicates détectés par titre).

## 8. Questions ouvertes

- Version : normaliser `version:` en semver string (ex. `1.0.0`) pour tous les
  nouveaux artefacts, tout en acceptant l'entier existant — migration par
  génération ?
