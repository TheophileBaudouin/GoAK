# Plan — Semantic Resource Router (routage par index)

Date : 2026-08-05 · Statut : implémenté et revu (APPROVE-WITH-NITS, nits corrigés) · Autorité : KIT_CHARTER.md

## Goal

Permettre à un agent Pi d'obtenir, pour une tâche donnée, la direction vers les
~198 ressources du kit (règles, recettes, catalogues, patterns, anti-patterns,
snippets, prompts, skills) — sans charger le kit dans le contexte. L'index est
uniquement un routeur : la vérité reste les fichiers sources.

## Context

- Méta-projet (racine) : seul détenteur du droit d'écriture sur l'index ;
  builder déterministe ; docs et évidence versionnées.
- Kit (`KitV2/`) : embarque l'index généré, en lecture seule ; outil Pi natif
  `search_kit_resources` + skill `kit-resource-routing`.
- Décisions utilisateur 2026-08-05 : pas d'embeddings (BM25 + synonymes, le LLM
  fait le tri final sur un top-5), stockage JSON versionné, recherche
  obligatoire avant tout travail technique, outil = extension Pi native.
- Recherche web (2026-08-05) : BM25 ≥ embeddings pour le routage sur petit
  corpus ; sqlite-vec/TinyVector = dépendances inutiles à ce volume.

## Constraints

1. **Séparation stricte** : builder dans `.agent/router/` (méta-projet), jamais
   dans le kit ; runtime dans `KitV2/.pi/extensions/`, jamais dans le méta-projet.
2. **Gate produit** : `validate-kitv2.py` étendu (couverture + hash) — toute
   dérive d'index bloque la release. Le validateur produit n'est PAS modifié
   sans tests positifs/négatifs (contrat Z7).
3. **Context protection** : top-K ≤ 5 (max 8), score ≥ seuil, résultats courts,
   zéro résultat propre au lieu de bruit.
4. **Déterminisme hors-ligne** : zéro dépendance réseau dans le builder ; le
   builder n'utilise que la stdlib Python (comme les validateurs existants).
5. **Compatibilité installation** : `install.sh` extrait `KitV2/` en entier —
   la zone `router/` est embarquée sans modifier l'installeur.
6. Zones du kit modifiées : nouvelle zone `router/` (contrat Z11) + `.pi/skills/`
   (Z8) + `.pi/extensions/` (Z8) + `tools/validators/` (Z7) + manifest/capabilities
   (C1) + AGENTS.md (Z9). Chaque zone : contrat lu avant édition.

## Architecture cible

```
Méta-projet  .agent/router/build_index.py   builder (build / --check) + tests
             .agent/router/test_build_index.py
Kit          KitV2/router/index.json         artefact généré (id, kind, path,
             KitV2/router/meta.json          description, tags, terms)
             KitV2/router/README.md          doc de consommation (lecture seule)
             KitV2/.pi/extensions/kit-resource-router.ts   outil Pi natif
             KitV2/.pi/skills/kit-resource-routing/SKILL.md   skill d'usage
Gate         validate-kitv2.py  +check_router()  couverture + sha256 + chemins
Docs         docs/router/README.md          doc technique méta-projet
             .agent/kit-governance/21-zone-router.md   contrat Z11
```

Index : `resources[]` = {id, kind, path, description, tags, terms} triés par id ;
`meta.json` = {schema, version, built_at, index_sha256, counts, stopwords}.
Le runtime charge l'index, calcule df/idf en mémoire, tokenise la requête
(mêmes règles + synonymes fr/en contenus dans l'extension), score BM25
(k1=1.2, b=0.75), filtre score > 0, top-K, sortie compacte.

## Done

1. Builder déterministe testé (fixtures : déterminisme, couverture, schéma).
2. Index réel généré et passé en gate.
3. Extension Pi native testée end-to-end (pi headless, 4 scénarios).
4. Skill créée, valide pour les deux validateurs.
5. Gate complète verte (validateurs, gofmt, vet, lint, tests, gosec,
   govulncheck, probes) + installation propre vérifiée en copie consommateur.
6. Evidence dans `docs/evidence/2026-08-05/resource-router/`, mémoire à jour.
7. Revue fraîche-contexte indépendante.
