# Phase 2 — contrats de gouvernance du Kit : évidence

- **Date :** 2026-08-04
- **Plan :** `docs/plans/2026-08-04-kit-governance-phase2.md`
- **Décisions :** `.pi/memory/Decisions.md` (2026-08-04, sections
  « phase 1 decisions » et « décisions phase 2 »)
- **Revue fresh-context :** subagent reviewer `56441ae1` — verdict
  REQUEST-CHANGES → 2 blocages corrigés (fermetures de blocs Markdown sur 7
  contrats ; évidence+mémoire) + nits intégrés (Z2 état réel pointers/,
  Z1 unité de compte module, C1 états cibles, 17-zone-pi/20-auteur-modules
  questions closes, Z10 note extends). Décision `category: workflow`
  enregistrée.

## Changements du Kit (produit)

1. **Supprimé** `KitV2/embeddings/` (héritage vide — décision propriétaire).
2. **Supprimé** `KitV2/tools/analyzers/` (vide, sans contrat — décision).
3. **Supprimé** `KitV2/templates/api-service/` (placeholder orphelin sans
   roadmap — rétroactif conforme à N1 §6, non couvert par EXPECTED_TEMPLATES).
4. **Renommé** `KitV2/rules/core/rules/universal/` →
   `KitV2/rules/core/universal/` (anomalie d'imbrication ; validateur
   name==parent conservé).
5. **Créé** `KitV2/knowledge/debugging/README.md` (contrat de domaine :
   admission sur échec observé et vérifié, roadmap).
6. **Modifié** `KitV2/templates/TEMPLATES.md` + `template-contract.md`
   (politique MIT : jamais de template agent-écrit ; squelettes marqués
   `legacy`, candidats au remplacement par des templates sourcés MIT).
7. **Modifié** frontmatter des 5 skills `KitV2/.pi/skills/*/SKILL.md`
   (ajout `category: workflow`, `tags`, `last-verified` — contenu intact).

## Changements du MetaProjet

1. **Créé** `.agent/kit-governance/` — 15 contrats + README d'index :
   C0 (00-charte-d-application), C1 (01-manifest-capabilities),
   C2 (02-validation-gate), Z1–Z10 (10-zone-rules … 19-registre-artefacts),
   A1 (20-auteur-modules), N1 (30-conventions).
2. **Modifié** `.agent/instructions.md` (référence les contrats, règle
   « une règle de contrat non vérifiable est une hypothèse »).
3. **Modifié** `docs/research/2026-08-04-kit-audit-governance.md` §4.7
   (décisions résolues) et `docs/plans/` (plan phase 2).
4. **Modifié** `.pi/memory/Decisions.md` (phase 1 + phase 2, extension
   `category: workflow`) et Gotchas (dérive des comptes manuels).

## Résultats de gate

`validation.raw.txt` : validateur `kitv2: PASS (45 product skills, 3 snippets,
standalone, offline bundle)` ; gofmt clean ; `go vet` PASS ; `go test -race`
PASS (recettes + tools/offline) ; golangci-lint 0 issues ; gosec 0 issues ;
govulncheck : aucune vulnérabilité appelée ; probes 5/5 PASS (cli-minimal,
rest-chi, sqlite-sqlc, worker-shutdown, offline).

## Reste ouvert (contracté, pas bloquant)

- Migration `catalogs/libraries/` → séparation modules SKILL.md / pointeurs
  YAML (`pointers/`) : décidée, **non exécutée** (22 YAML Source en racine) —
  tracée en roadmap (Z2).
- Extension du validateur selon C2 (fraîcheur 12/18, cohérence
  manifest↔capabilities, comptes dérivés, découverte probes, qualité des
  descriptions) : contractée, implémentation à planifier.
- `tools/generators/` : à créer (premier : registre d'artefacts généré).
- `known_limits` structuré : état cible (C1).
- Remplacement des 7 squelettes templates `legacy` par des templates sourcés
  MIT (Z5) : recherche de candidats à lancer.

## Mise à jour (post-revue)

- `validate-instructions.py` (metaprojet) étendu : les skills de workflow
  `.pi/skills/` acceptent désormais `category` (valeur kit-only `workflow`),
  `tags`, `last-verified` (schéma ALLOWED_WORKFLOW_FIELDS / REQUIRED =
  name, description, last-verified). Test négatif vérifié (skill sans
  `last-verified` → 1 erreur). Ruff : all checks passed.
