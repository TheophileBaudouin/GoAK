# Plan de correction post-audit KitV2 — 2026-08-05

Source : audit `docs/research/2026-08-05-kitv2-audit-report.md` (2026-08-05T10:45:00Z,
17 findings KVA-001→KVA-017). Journal de décision :
`.pi/memory/Decisions.md` (D-2026-08-05-01 → -07). Recherche Phase 1 :
`docs/research/2026-08-05-kitv2-correction-research/` (01..05).

Règles du cycle : une tâche = un changement vérifiable ; preuve d'exécution
(commande + sortie brute) exigée ; rollback immédiat si un validateur vert
régresse ; périmètre KitV2 sauf sortie documentée.

---

## P0 — Bloquant gate

### KVA-001 — `validate-cognitive.py` rouge (double base de résolution)

- **Rappel** : `validate-cognitive.py` exit 1 : « unresolved relationship
  target pattern:security:secrets-management / pattern:security:auth-session-vs-jwt »
  dans `knowledge/stdlib/x-crypto.yaml` et `x-oauth2.yaml`. Le catalogue
  `.agent/cognitive/source-catalog.yaml` ne déclare aucun id pattern. Les ids
  EXISTENT dans le produit (`knowledge/patterns/`) — `validate-kitv2` PASS.
  Sections : C0 §8, charte §13. Impact : gate méta-projet rouge ; la mémoire
  « gate PASS » (2026-08-05) contredit l'état réel.
- **Décision (D-2026-08-05-04)** : corriger la source de vérité du contrôle —
  ajouter une source `source:security:owasp-session-jwt-cheatsheets` au
  catalogue avec transformations + target_status active/materialized_by pour
  les 2 patterns. La base de résolution de validate-cognitive EST le catalogue
  (design documenté) ; l'arbre produit reste la vérité de validate-kitv2.
  **Sortie de périmètre** : `.agent/cognitive/source-catalog.yaml` (méta-projet),
  exigée par le finding.
- **Fichiers impactés** : `.agent/cognitive/source-catalog.yaml` (1 source
  ajoutée).
- **Critère de vérification** : `python3 .agent/validators/validate-cognitive.py`
  → rc 0, sortie `cognitive: PASS`.

---

## P1 — Structurel, risque élevé

### KVA-002 — 25 `.gitkeep` vides livrés

- **Rappel** : 25 fichiers 0 octet trackés, extraits par `install.sh` ;
  6 dossiers recettes roadmap vides ; `recipes/README.md` absent. C0 §7, N1 §6,
  Z3 §4.1, Z4 §4.3.
- **Décision** : supprimer les 25 `.gitkeep` ; créer `recipes/README.md`
  (roadmap des 6 recettes planifiées avec critères) ; compléter
  `snippets/README.md` (roadmap des 8 catégories vides) ; `tools/README.md` et
  `tools/offline/README.md` créés dans KVA-012 (roadmap `tools/generators`).
- **Fichiers impactés** : 25 × `**/.gitkeep` (git rm) ; `recipes/README.md`
  (création) ; `snippets/README.md` (roadmap ajoutée).
- **Critère de vérification** : `git ls-files KitV2 | grep -c .gitkeep` = 0 ;
  `validate-kitv2.py` rc 0 ; `bash probes/run.sh` rc 0 (aucun impact).

### KVA-003 — `probes/run.sh` : liste en dur

- **Rappel** : `for probe in cli-minimal rest-chi sqlite-sqlc worker-shutdown offline`.
  Z6 §2, C2 §2 (découverte par glob obligatoire).
- **Décision** : réécrire avec glob `"$root"/probes/*/` filtrant `main.go` ;
  ajouter le contrôle C2 « run.sh ne contient pas de liste littérale » dans la
  vague validateur (KVA-007).
- **Fichiers impactés** : `probes/run.sh`.
- **Critère** : `bash probes/run.sh` → 5 probes exécutées, rc 0 ;
  `bash -n probes/run.sh` rc 0.

### KVA-004 — 3 `check.sh` gofmt-only

- **Rappel** : `snippets/{bounded-worker,errors-once,http-json}/check.sh` =
  gofmt uniquement, mute le fichier (`gofmt -w`), aucun comportement prouvé.
  Z4 §4.2. Les `example.go` sont des packages (pas de main) → besoin de tests.
- **Décision** : ajouter `example_test.go` par snippet (assertions sur le
  comportement central : bounded worker = limite + propagation d'erreur +
  annulation ; errors-once = wrap `%w` + nil ; http-json = status +
  Content-Type + corps JSON) ; réécrire `check.sh` = `gofmt -l` (lecture seule,
  sans `-w`) + `go test ./...` (compilation + exécution). Contrôle C2 « check.sh
  doit contenir go run/go test » dans la vague validateur.
- **Fichiers impactés** : 3 × `check.sh`, 3 × `example_test.go` (création).
- **Critère** : `bash snippets/*/check.sh` rc 0 chacun ; `go test -race ./...`
  rc 0 (les nouveaux tests passent) ; démonstration négative : un check.sh
  gofmt-only est rejeté par le nouveau contrôle C2.

### KVA-005 — 21 YAML Niveau B dans `catalogs/libraries/`

- **Rappel** : 21 YAML Source actifs dans une zone contractée SKILL.md ;
  N1 §2 « on ne mélange pas deux formats pour le même rôle sans contrat »,
  Z2 §2 ne documente pas ce cas.
- **Décision (D-2026-08-05-01)** : contractualiser dans Z2 §2 —
  `catalogs/libraries/*.yaml` = pointeurs Source « Niveau B » actifs (source
  conditionnelle, non vétée) ; `pointers/` = pointeurs `proposed` « à
  considérer » ; promotion = admission 9 critères (Z2 §4.3). Aucun déplacement.
  **Sortie de périmètre** : `.agent/kit-governance/11-zone-knowledge.md`.
- **Fichiers impactés** : `.agent/kit-governance/11-zone-knowledge.md` (§2).
- **Critère** : relecture du contrat cohérente ; `validate-cognitive.py` rc 0 ;
  aucun changement d'arborescence (git status KitV2 inchangé sur ce point).

### KVA-006 — Statut `partial` vs vocabulaire Z5 (7 templates)

- **Rappel** : `templates/*/template.yaml` `status: partial` ; Z5 §4 définit
  planned/sourced/legacy/deprecated ; TEMPLATES.md dit `legacy` ;
  capabilities dit « runnable-minimal-bases-and-explicit-partials ».
- **Décision (D-2026-08-05-02)** : `status: legacy` dans les 7 `template.yaml` ;
  ligne de statut des 7 `templates/*/README.md` → `LEGACY` ; `capabilities.yaml`
  statut capacité templates → `legacy-scaffolds`. Contrôle C2 du vocabulaire Z5
  dans la vague validateur.
- **Fichiers impactés** : 7 × `template.yaml`, 7 × `README.md`,
  `capabilities.yaml`.
- **Critère** : `grep -h status: templates/*/template.yaml` = 7 × legacy ;
  `validate-kitv2.py` rc 0.

---

## P2 — Moyen

### KVA-007 — Validateur sans tests + constantes en dur

- **Rappel** : 0 fichier `test_*` (C2 §3 exige tests +/−) ;
  `EXPECTED_PRODUCT_SKILLS = 65` en dur (C2 §5).
- **Décision (D-2026-08-05-07)** : créer `tools/validators/test_validate_kitv2.py`
  (unittest, stdlib, fixtures temporaires hors dépôt) couvrant les contrôles
  existants (frontmatter skill, knowledge metadata/relations, snippets, bundle,
  router, empty markdown) et les nouveaux (KVA-003/004/006 + fraîcheur + comptes
  dérivés) avec cas positifs et négatifs. Supprimer `EXPECTED_PRODUCT_SKILLS`
  au profit de la dérivation (KVA-008). Le fichier de tests s'exécute avec
  `python3 -m unittest` depuis `tools/validators/`.
- **Fichiers impactés** : `tools/validators/validate-kitv2.py`,
  `tools/validators/test_validate_kitv2.py` (création).
- **Critère** : `python3 -m unittest tools/validators/test_validate_kitv2.py`
  (ou `cd tools/validators && python3 -m unittest`) → OK ; `validate-kitv2.py`
  rc 0 ; `KITV2_STRICT_CATALOG=1 ...` rc 0.

### KVA-008 — `coverage.*` en dur dans capabilities.yaml

- **Rappel** : 6 comptes (65/13/10/42/5/7) codés en dur, seul product_skills
  partiellement contrôlé. C1 §3.3 « coverage interdit en dur : le validateur le
  recalcule depuis l'arborescence ».
- **Décision (D-2026-08-05-07)** : `validate-kitv2.py` calcule les 6 comptes
  depuis l'arbre (SKILL.md rules/recipes/catalogs, probes/*/main.go,
  templates/*/template.yaml) et les compare à `capabilities.yaml coverage.*` ;
  mismatch = erreur. `EXPECTED_PRODUCT_SKILLS` supprimé.
- **Fichiers impactés** : `validate-kitv2.py`, `test_validate_kitv2.py`.
- **Critère** : test négatif (valeur volontairement fausse → rc 1) inclus dans
  la suite ; valeur réelle → rc 0.

### KVA-009 — Fraîcheur 4 recettes (370 j)

- **Rappel** : `recipe-cli-minimal`, `recipe-desktop-app`,
  `recipe-graceful-shutdown`, `recipe-worker-pool` : `last-verified 2025-07-31`.
  C0 §5 (12 mois → warning ; 18 mois → déprécié).
- **Décision** : recherche 03-recipes-freshness (2026-08-05) : 3 CONFORME
  (pratiques inchangées, sources pkg.go.dev datées) → bump `last-verified:
  2026-08-05` ; `recipe-desktop-app` À CORRIGER → mettre à jour la section
  « ⚠ Wails v3 is Beta-to-GA » (iOS/Android désormais expérimentaux, plus
  « unsupported » — source v3.wails.io/status/ consultée 2026-08-05) + bump.
- **Fichiers impactés** : 4 × `recipes/*/SKILL.md` (bump last-verified ;
  - correction section mobile pour desktop-app).
- **Critère** : `grep last-verified recipes/recipe-*/SKILL.md` = 2026-08-05 ×4 ;
  `validate-kitv2.py` rc 0.

### KVA-010 — 5 URLs mortes + statut 18 pkg.go.dev

- **Rappel** : 5 URLs mortes confirmées (refactoring.guru/large-class 404,
  axonops 000, xunitpatterns ×2 404, gitlab cznic/sqlite issues 404) ; 17-18
  pkg.go.dev en 429 (rate-limit) À VÉRIFIER.
- **Décision** : recherche 01-kva010-urls + 02-pkgdev-429 + re-vérification curl
  indépendante (2026-08-05) : les 5 remplacements proposés sont tous HTTP 200 ;
  les 18 pkg.go.dev sont toutes vivantes (200) → aucun remplacement pkg.go.dev
  nécessaire. Appliquer les 5 remplacements :
  - `arch-god-object.yaml` : `https://refactoring.guru/refactoring/smells/large-class`
    → `https://refactoring.guru/smells/large-class`
  - `msg-offset-commit-misorder.yaml` : `https://docs.axonops.com/.../anti-patterns/`
    → `https://docs.confluent.io/platform/current/clients/consumer.html`
  - `test-over-mocking.yaml` : `http://xunitpatterns.com/MockObject.html`
    → `http://xunitpatterns.com/Mock%20Object.html`
  - `test-sleep-based.yaml` : `http://xunitpatterns.com/Sleepy%20Test.html`
    → `http://xunitpatterns.com/Slow%20Tests.html`
  - `modernc-sqlite/SKILL.md` : `https://gitlab.com/cznic/sqlite/-/issues`
    → `https://gitlab.com/cznic/sqlite/-/work_items`
- **Fichiers impactés** : 4 YAML anti-patterns + 1 SKILL.md catalog.
- **Critère** : après édition, re-vérification HTTP des 5 nouvelles URLs (200) ;
  `validate-kitv2.py` rc 0 ; strict rc 0.

### KVA-011 — Pointeurs `proposed` livrés et indexés + bootstrap-cli-runtime

- **Rappel** : 5 pointeurs proposed indexés par le router (Z10 §5.3 « proposed
  invisible » vs Z11 §3.1 couverture complète) ; bootstrap-cli-runtime proposed
  dans le produit avec mention `.agent/`. N1 §5.
- **Décision (D-2026-08-05-03)** : documenter l'exception dans Z10 §5.3 :
  les pointeurs Source « à considérer » (`catalogs/libraries/pointers/`,
  `status: proposed`) et les artefacts d'architecture proposés livrés par
  décision sont indexés par le router et marqués proposed — découvrabilité
  intentionnelle (pratique B1, recherche 05). Aucun changement de code ni de
  router. La mention `.agent/` de bootstrap-cli-runtime est traitée en KVA-014.
  **Sortie de périmètre** : `.agent/kit-governance/19-registre-artefacts.md`.
- **Fichiers impactés** : `.agent/kit-governance/19-registre-artefacts.md` (§5.3).
- **Critère** : relecture cohérente ; validateurs rc 0 ; aucun changement produit.

### KVA-012 — README manquants

- **Rappel** : `tools/offline/` sans README (Z7 §3.1 « outil sans README
  n'existe pas ») ; `recipes/README.md` + `tools/README.md` absents (Z3 §4.1) ;
  `.pi/README.md` « à créer » (Z8 §3.3).
- **Décision** : créer `recipes/README.md` (roadmap 6 recettes planifiées +
  critères), `tools/README.md` (zone : mission, outils, gates),
  `tools/offline/README.md` (mission, entrées/sorties, gate qui l'exécute),
  `.pi/README.md` (contrat de chemins Z8 §3.3).
- **Fichiers impactés** : 4 créations.
- **Critère** : présence des 4 fichiers ; `validate-kitv2.py` rc 0.

---

## P3 — Faible

### KVA-013 — Hygiène `.gitignore` / junk

- **Rappel** : `.DS_Store` non ignoré dans KitV2/.gitignore ; 5 `.DS_Store` +
  `.ruff_cache/` + `__pycache__/` sur disque.
- **Décision** : ajouter `.DS_Store` à `KitV2/.gitignore` ; supprimer les
  artefacts machine du working tree (5 × .DS_Store, .ruff_cache/,
  **pycache**/).
- **Fichiers impactés** : `KitV2/.gitignore`, suppression de junk.
- **Critère** : `git status --porcelain -- KitV2` ne montre que les
  changements intentionnels ; `find KitV2 -name .DS_Store` = 0.

### KVA-014 — Mentions méta-projet dans le produit

- **Rappel** : `knowledge/debugging/README.md:41` (docs/evidence),
  `bootstrap-cli-runtime.yaml:37` (`.agent/`). N1 §5.
- **Décision** : reformuler sans chemins méta-projet : debugging/README →
  « l'évidence brute appartient au metaprojet (hors produit) » ;
  bootstrap-cli-runtime → « le control-plane de gouvernance du metaprojet
  n'est jamais installé comme runtime consommateur ».
- **Fichiers impactés** : 2.
- **Critère** : grep `.agent/`/`docs/evidence` dans KitV2 (hors validateur et
  hors chaînes de contrôle) = 0 nouvelle occurrence ; validateurs rc 0.

### KVA-015 — Renommage `recipe-cli-interactif` → `recipe-cli-interactive`

- **Rappel** : id français (N1 §1) ; Z3 §4.2 acte le renommage.
- **Décision (D-2026-08-05-05)** : `git mv` du dossier ; frontmatter `name`,
  titre, ligne `go test` du SKILL.md ; références produit (testing-seam-injection
  ×2, cli-subcommands-conventions ×1, test-implementation-details ×1, bubbletea
  ×1) ; `.agent/cognitive/technology-documentation.yaml` ×1 ; router régénéré.
  docs/ historiques non modifiés.
- **Fichiers impactés** : dossier + 2 fichiers de la recette, 5 références
  produit, 1 référence méta-projet, `router/index.json` + `meta.json`
  (régénérés).
- **Critère** : `validate-kitv2.py` rc 0 (name == dossier) ;
  `python3 .agent/router/build_index.py --check` propre ; `go test -race ./...`
  rc 0 ; `grep -rn 'recipe-cli-interactif' KitV2` = 0.

### KVA-016 — Contrat Z2 §2 obsolète

- **Rappel** : Z2 §2 « pointers/ … non créé à ce jour » — le dossier existe
  depuis 2026-08-05 (5 pointeurs).
- **Décision (D-2026-08-05-06)** : mettre à jour Z2 §2 (état réel + KVA-005).
- **Fichiers impactés** : `.agent/kit-governance/11-zone-knowledge.md` (§2).
- **Critère** : relecture cohérente ; validateurs rc 0.

### KVA-017 — Incident d'inspection (binaires go build)

- **Rappel** : 7 binaires créés puis supprimés pendant l'audit ; état restauré.
- **Décision** : aucune action (résolu, preuve : `git status --porcelain -- KitV2` = 0).

---

## Ordre d'exécution et séquencement des gates

1. KVA-001 (gate méta verte) → 2. KVA-006 → 3. KVA-003 + KVA-004 →
2. KVA-002 + KVA-012 → 5. KVA-009 → 6. KVA-010 → 7. KVA-007 + KVA-008
(validateur étendu + tests — après les fixes pour que les nouveaux contrôles
passent) → 8. KVA-005 + KVA-011 + KVA-016 (contrats, sortie de périmètre) →
3. KVA-013 + KVA-014 → 10. KVA-015 (renommage + router) → 11. Gate complète
finale + rapport de clôture.

Gates intermédiaires après chaque groupe : `validate-kitv2.py` (+ strict si
contenu catalog), `validate-instructions.py`, `validate-cognitive.py` (après
KVA-001), `go test ./...` (après KVA-004/015), `bash probes/run.sh` (après
KVA-003).
