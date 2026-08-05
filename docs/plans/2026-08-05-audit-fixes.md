# Plan — Correction des findings de l'audit KitV2 2026-08-05

## Goal

Fermer les 11 findings KVA-001…KVA-011 issus de l'audit diagnostic du
2026-08-05 (ledger : 447 chemins, gate verte, 1 CRITIQUE + 2 ÉLEVÉ + MOYENS),
en ne modifiant que ce que l'audit recommande, sans changer la charte ni le
frontmatter publié.

## Context

- Audit complet : `KitV2/` (442 audités, 5 exclus gitignorés, 0 bloqué),
  commit `dff83d8`.
- Findings : KVA-001 (template rest-api non livré, CRITIQUE), KVA-002
  (vocabulaire manifest↔capabilities), KVA-003 (core→registry dans
  `rules/core/errors`), KVA-004 (schéma de règle — décision utilisateur :
  aligner Z1 §5 sur A1, Option A), KVA-005 (probes/README périmé), KVA-006
  (x/sync non vétée + contrôle Z3 §8 absent), KVA-007 (duplication validate
  koanf/viper), KVA-008 (gate AGENTS.md incomplète), KVA-009 (titre dupliqué
  stdlib), KVA-010 (réf. « AGENTS.md (Conventions) » morte), KVA-011 (test
  écrivant dans capabilities.yaml).
- Recherche faite : upstream `leeprovoost/go-rest-api-template`@4f2d17f tracké
  `cmd/api-service/{main.go,Makefile,VERSION}` ; pattern `.gitignore`
  `api-service` vise le binaire produit par `cmd/api-service/Makefile`
  (`go build -o api-service .`) mais avale le dossier source. Convention Go :
  ignorer `bin/` + chemins de binaires explicites.

## Constraints

- Ne pas toucher à la charte, au frontmatter publié (N1/A1), ni aux évaluations
  des templates legacy.
- Une seule écriture par vérité ; toute nouvelle référence = cross-référence
  taggée.
- Gate complète verte à la fin (validateurs strict + normaux, build_index
  --check, gofmt, vet, lint, test -race, gosec, govulncheck, probes, tests
  unitaires validateurs).
- Router régénéré après tout ajout/suppression de YAML knowledge.
- Revue fresh-context (subagent read-only) avant déclaration de fin (C0 §6.3).

## Done when

- KVA-001…KVA-011 fermés avec preuve ; gate verte ; router 256 ressources ;
  manifest/capabilities cohérents (kebab, 11 capacités) ; décisions écrites
  dans `.pi/memory/Decisions.md` ; gotcha du `.gitignore` enregistré ;
  commit unique propre ; compte rendu final.

## Étapes

1. KVA-001 : corriger `templates/rest-api/.gitignore` (remplacer `api-service`
   par `bin/` + `/cmd/api-service/api-service`), `git add cmd/api-service/`,
   note d'adaptation dans ATTRIBUTION.md, vérifier `go build ./...` +
   `go run ./cmd/api-service` (smoke local).
2. KVA-001b : contrôle gate « template compilable » dans `validate-kitv2.py`
   (`check_template_build` : `go build ./...` par template sourced, skip +
   warning si go absent) + tests positif/négatif.
3. KVA-002 : aligner `manifest.yaml` et `capabilities.yaml` (vocabulaire kebab
   identique, 11 capacités, `criteria:` par capacité) + contrôle C2
   `check_manifest_capabilities_coherence` + tests.
4. KVA-003 + KVA-010 : corriger les références de `rules/core/errors`
   (supprimer les mentions `rules/logging` et « AGENTS.md (Conventions) »).
5. KVA-004 (Option A) : reformuler Z1 §5 (éléments sémantiques, en-têtes
   libres) ; ajouter les frontières manquantes aux règles concernées
   (concurrency, philosophy, golangci-lint, gosec, govulncheck, doc-comments,
   testing) ; décision dans Decisions.md.
6. KVA-005 : réécrire `probes/README.md` (inventaire réel 15 probes, contrat
   d'ajout, découverte run.sh, limites connues).
7. KVA-006 : ajouter `knowledge/stdlib/x-sync.yaml` (pointeur Source) +
   contrôle C2 `check_recipe_dependencies` (deps directes de go.mod ⊆ corpus
   vété) + tests.
8. KVA-007 : cross-référence koanf↔viper (justification de parallélisme dans
   les deux SKILL.md) + note décision.
9. KVA-008 : corriger la section Validation de `AGENTS.md` (gate C2 §4 exacte)
   et la revendication coverage de `rules/registry/testing`.
10. KVA-009 : renommer le titre de `knowledge/stdlib/pkg-doc-offline.yaml`.
11. KVA-011 : réécrire `test_coverage_detects_drift` (ROOT injectable / mock,
    plus d'écriture dans le dépôt).
12. Version manifest/capabilities 2.4.1 + régénération router (`build_index.py`).
13. Gate complète + tests validateurs + probes.
14. Revue fresh-context (subagent read-only).
15. Mémoire (Progress, Gotchas, Decisions) + commit + compte rendu.
