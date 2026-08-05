# KitV2 Audit — 2026-08-05T10:45:00Z (rapport d'audit permanent)

> Rapport **diagnostique, non destructif et traçable** du produit `KitV2/`
> (prompt `.pi/prompts/kit-audit.md`). Aucun fichier du dépôt n'a été modifié
> par l'audit ; l'état Git de KitV2 était et reste propre (`git status
> --porcelain -- KitV2` = 0). Ce document est la copie persistée du rapport ;
> le ledger exhaustif et l'inventaire sont archivés sous
> `docs/evidence/2026-08-05/kitv2-audit/` (ledger.md, inventory-398.txt,
> scan-398.json, urlcheck-anomalies.txt, urls-checked.txt).

## A. En-tête

- **Date** : 2026-08-05T10:45:00Z (fin d'inspection) ; inventaire 2026-08-05T09:35:00Z.
- **Cible** : `/Users/theophilebaudouin/Documents/devellopement/Go/KitV2` (398 chemins) — argument : aucun (KitV2 entier).
- **Statut** : non destructif. Incident documenté : `go build ./...` dans
  `templates/*/` a produit 7 binaires (artefacts de l'inspection, absents de
  l'inventaire initial) ; supprimés uniquement ces 7 fichiers ; état restauré
  (0 changement).
- **État Git observé** : HEAD `b326c3d8` (branche `main`, ahead 28 de
  origin/main). Working tree méta-projet : `.pi/memory/{Brief,Gotchas,Progress}.md`
  modifiés, `.pi/prompts/` + `docs/plans/2026-08-05-kitv2-permanent-audit-prompt.md`
  untracked (hors cible). KitV2 propre.
- **Versions** : manifest `2.2.1`, router `meta.json 2.2.1` (index 254 ressources).

**Commandes réellement exécutées (lecture seule)** :

| Commande | Résultat |
|---|---|
| `python3 .agent/validators/validate-instructions.py` | PASS (rc 0) |
| `python3 .agent/validators/validate-cognitive.py` | **FAIL (rc 1)** — 2 cibles non résolues |
| `python3 tools/validators/validate-kitv2.py` | PASS (rc 0) — 65 skills, 3 snippets, bundle, router 254 |
| `KITV2_STRICT_CATALOG=1 python3 tools/validators/validate-kitv2.py` | PASS (rc 0) |
| `go mod verify` | PASS |
| `gofmt -l .` | propre |
| `go vet ./...` | PASS |
| `golangci-lint run ./...` | 0 issue |
| `go test -race ./...` | PASS (tous packages) |
| `gosec ./...` | 0 issue (24 fichiers, 1519 lignes) |
| `govulncheck ./...` | « No vulnerabilities found » |
| `bash probes/run.sh` | 5/5 PASS (cli-minimal, rest-chi, sqlite-sqlc, worker-shutdown, offline) |
| build+test des 7 templates | 7/7 OK |
| Vérification HTTP de 429 URLs | 24 anomalies : 17×429 pkg.go.dev (rate-limit), 403 dzone, 000 axonops, 5×404 confirmés |

**Non exécutées** : `go mod tidy` (mutation interdite) ; scénarios Pi end-to-end
depuis copie consommateur (hors périmètre non-modifiant) ; re-vérification des
17 URLs pkg.go.dev en 429 ; `ruff` (aucune config commitée).

## B. Inventaire et réconciliation

Inventaire : `find -P KitV2 \( -type f -o -type l \) -print | LC_ALL=C sort` →
**398 chemins**.

```
trouvés = 398
audités  = 389
exclus_justifiés = 9   (5 × .DS_Store, 3 × .ruff_cache/, 1 × __pycache__/*.pyc)
bloqués  = 0

398 = 389 + 9 + 0  →  ÉQUATION FERMÉE, couverture complète
```

Aucun chemin resté `À INSPECTER`. Fichiers de contexte lus, exclus du calcul
(18) : KIT_CHARTER.md, AGENTS.md (racine), install.sh, README.md (racine, non
lu en entier — hors cible), 16 contrats `.agent/kit-governance/`,
validate-instructions.py, validate-cognitive.py, source-catalog.yaml
(mécanique + grep ids), graph-schema/technology-documentation/
technology-source-units (mécanique via validateur).

## C. Verdict par fichier et par dimension

Ledger exhaustif : `docs/evidence/2026-08-05/kitv2-audit/ledger.md` (398
lignes, 15 colonnes). Synthèse des verdicts non triviaux :

- **NON CONFORME** — 25 `.gitkeep` vides livrés (C0 §7 / N1 §6 / Z3 §4.1 / Z4 §4.3).
- **NON CONFORME** — `probes/run.sh` : liste en dur (Z6 §2 / C2 §2).
- **NON CONFORME** — 3 `snippets/*/check.sh` gofmt-only (Z4 §4.2).
- **AMBIGU / À VÉRIFIER** — 21 YAML Niveau B dans `catalogs/libraries/`
  (format YAML dans zone SKILL.md, N1 §2 / Z2 §2).
- **À VÉRIFIER** — 5 pointeurs `status: proposed` indexés par le router
  (Z10 §5.3 vs Z11 §3.1) ; `bootstrap-cli-runtime.yaml` proposed + mention `.agent/`.
- **NON CONFORME** — 4 anti-patterns + `modernc-sqlite` : URLs mortes vérifiées.
- **À VÉRIFIER** — 4 recettes `last_verified` 370 j (> 12 mois, C0 §5).
- **NON CONFORME** — 7 `template.yaml` `status: partial` vs vocabulaire Z5 §4
  (TEMPLATES.md dit `legacy`).
- **NON CONFORME** — `validate-kitv2.py` sans tests (C2 §3) ; `EXPECTED_PRODUCT_SKILLS=65` en dur (C2 §5).
- **À VÉRIFIER** — `capabilities.yaml` `coverage.*` en dur (C1 §3.3).
- **À VÉRIFIER** — 3 fiches reference-projects non relues intégralement.
- **CONFORME** — mécanique produit : gate Go verte, validators produits PASS,
  probes 5/5, router cohérent, 39 fiches libraries (format N1 §4), offline,
  extension Pi, prompts, skills, règles (budget core 5 modules ≤ 300 lignes).

## D. Findings classés (KVA-001 → KVA-017)

| ID | Risque | Fichier/preuve | Section | Impact | Action (non appliquée) |
|---|---|---|---|---|---|
| KVA-001 | ÉLEVÉ | `knowledge/stdlib/x-crypto.yaml:33`, `x-oauth2.yaml:29` ; `validate-cognitive.py` exit 1 : « unresolved relationship target pattern:security:secrets-management / auth-session-vs-jwt » ; 0 id pattern dans `.agent/cognitive/source-catalog.yaml` ; ids présents dans le produit (`knowledge/patterns/`) | C0 §8, charte §13 | Gate méta-projet rouge ; mémoire « gate PASS » contredit l'état réel | Déclarer les 2 patterns dans le catalogue méta **ou** corriger la base de résolution ; re-run |
| KVA-002 | ÉLEVÉ | 25 `.gitkeep` trackés (`git ls-files`), 0 octet, extraits par `install.sh` | C0 §7, N1 §6, Z3 §4.1, Z4 §4.3 | Placeholders vides livrés ; roadmaps sans domicile (`recipes/README.md` absent) | Supprimer les .gitkeep, roadmaps dans README de zone, créer `recipes/README.md` |
| KVA-003 | ÉLEVÉ | `probes/run.sh:5` — `for probe in cli-minimal rest-chi sqlite-sqlc worker-shutdown offline` | Z6 §2, C2 §2 | Nouvelle probe non découverte ; régression Gotchas 2026-08-04 | Glob `probes/*/main.go` ; contrôle C2 |
| KVA-004 | ÉLEVÉ | `snippets/{bounded-worker,errors-once,http-json}/check.sh` — gofmt-only, mute le fichier | Z4 §4.2 | Aucun comportement prouvé ; régression errors-once étendue | check.sh réel (go run + assertions) |
| KVA-005 | ÉLEVÉ | 21 YAML actifs dans `knowledge/catalogs/libraries/` | N1 §2, Z2 §2 | Deux formats pour le même rôle sans contrat | Décision : pointeurs/ ou contrat Z2 §2 |
| KVA-006 | ÉLEVÉ | 7 `template.yaml` `status: partial` ; `TEMPLATES.md` dit `legacy` ; capabilities « runnable-minimal-bases » | Z5 §4, Z5 §2 | Statut public incohérent | Aligner sur `legacy` + contrôle C2 |
| KVA-007 | MOYEN | `validate-kitv2.py` : 0 test (`test_*` absent) ; `EXPECTED_PRODUCT_SKILLS=65` en dur | C2 §3, C2 §5 | Contrôles sans cas +/− ; compte en dur | Tests + dérivation du compte |
| KVA-008 | MOYEN | `capabilities.yaml:26-32` `coverage.*` en dur (13/10/42/5/7) | C1 §3.3 | Dérive possible non détectée | C2 : recalcul + comparaison |
| KVA-009 | MOYEN | 4 recettes `last-verified: 2025-07-31` (370 j) | C0 §5, C2 §2 | Seuil warning dépassé ; contrôle non implémenté | Implémenter fraîcheur ; re-vérifier |
| KVA-010 | MOYEN | 5 URLs mortes : `arch-god-object` (refactoring.guru 404), `msg-offset-commit-misorder` (axonops 000), `test-over-mocking` + `test-sleep-based` (xunitpatterns 404), `modernc-sqlite` (gitlab cznic/sqlite 404) ; 17 pkg.go.dev 429 À VÉRIFIER | Z2 §9.2, N1 §4 | Sources non vivantes | Remplacer/corriger ; check réseau hors gate |
| KVA-011 | MOYEN | 5 pointeurs `proposed` indexés ; `bootstrap-cli-runtime.yaml` proposed + « Root .agent/ remains metaproject governance » | Z10 §5.3, Z11 §3.1, N1 §5 | « proposed invisible » vs index ; gouvernance méta dans produit | Trancher : exclusion router ou statut dédié |
| KVA-012 | MOYEN | `tools/offline/` sans README ; `recipes/README.md` + `tools/README.md` absents ; `.pi/README.md` « à créer » | Z7 §3.1, Z3 §4.1, Z8 §3.3 | Roadmaps sans domicile ; outil sans mission | Créer les README |
| KVA-013 | FAIBLE | `.gitignore` sans `.DS_Store` ; 5 `.DS_Store` sur disque | N1 §6 (esprit) | Risque `git add -A` / packaging | Ignorer + purger |
| KVA-014 | FAIBLE | `knowledge/debugging/README.md:41` (docs/evidence), `bootstrap-cli-runtime.yaml:37` (.agent/) | N1 §5 | Mentions méta-projet (explicatives) | Reformuler |
| KVA-015 | FAIBLE | `recipes/recipe-cli-interactif/` — id français | N1 §1, Z3 §4.2 | Dette documentée | Renommer `recipe-cli-interactive` |
| KVA-016 | FAIBLE | `.agent/kit-governance/11-zone-knowledge.md` §2 « pointers/ … non créé à ce jour » | Z2 §2 | Contrat en dérive | Mettre à jour Z2 |
| KVA-017 | FAIBLE | 7 binaires créés puis supprimés (incident d'inspection) | — | Transparence | (résolu) |

## E. Lacunes d'automatisation

| Dimension | Déjà couvert | Trou | Contrôle conseillé |
|---|---|---|---|
| Frontmatter Pi | validate-instructions + validate-kitv2 | — | — |
| §5 + relations YAML | validate-cognitive (stdlib seulement, résolution catalogue méta) + validate-kitv2 (tout knowledge, résolution produit) | Double base de résolution (KVA-001) ; validate-cognitive ignore patterns/ ; validate-kitv2 ne vérifie pas le statut des cibles | Décision + extension déterministe |
| Fraîcheur 12/18 mois | — (prévu C2 §2, non implémenté) | 4 recettes > 12 mois sans warning | validate-kitv2 déterministe |
| Vivacité URLs | — | 5 mortes passées la gate | Script réseau CI hors gate ou revue |
| run.sh découverte | — (compte seul) | Liste en dur | validate-kitv2 (glob == liste) |
| check.sh réel | — (présence) | gofmt-only | validate-kitv2 (détection) |
| Statut templates | — | partial vs Z5 | validate-kitv2 (vocabulaire) |
| Comptes coverage | product_skills (constante) | 5 comptes non dérivés | validate-kitv2 (recalcul) |
| Tests validateur | — | 0 test | test_validate_*.py |
| Duplication sémantique | hash + paragraphes | Par question | Revue agent |
| Langue | — | Mixte documenté (N1 §1/§4) | Revue agent |
| Placement KIT/META | — | 27 AMBIGU | Revue agent + décision |

## F. Verdict

- **Audit : FAIL** — couverture fermée (398 = 389 + 9 + 0) mais 6 findings
  ÉLEVÉS non résolus (KVA-001 → KVA-006), `validate-cognitive.py` rouge,
  dimensions `À VÉRIFIER` (fraîcheur recettes, 17 URLs pkg.go.dev, fiches
  reference-projects, placement pointeurs). Mécanique produit saine.
- **Pollution méta-projet/Kit** : 27 fichiers AMBIGU (21 YAML Niveau B, 5
  pointeurs proposed, bootstrap-cli-runtime.yaml). Aucun fichier franchement
  META dans KitV2. 9 fichiers EXCLU (artefacts machine).
- **Prochaines actions** : voir `docs/plans/2026-08-05-kitv2-correction-plan.md`
  (cycle de correction post-audit).
