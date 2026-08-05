# C2 — Validation gate (portail de gouvernance exécutable)

- **Contrat MetaProjet** — régit `KitV2/tools/validators/validate-kitv2.py` et
  la gate du produit.
- **Rapport d'audit :** §2.8, §1.3 (problème 6).
- **Décisions :** seuil de fraîcheur 12/18 mois approuvé (2026-08-04).

## 1. Mission

`validate-kitv2.py` est le **portail de gouvernance** : il transforme les
règles des contrats (C0, C1, Z1–Z10, A1, N1) en contrôles exécutables. Un
contenu qui viole un contrat doit faire échouer la gate. La charte cesse d'être
déclarative : elle devient vérifiable.

## 2. Contrôles exigés (à implémenter progressivement ; chaque ajout a son test)

### Structure (existant, à étendre)

- Fichiers racine obligatoires (manifest, capabilities, AGENTS.md, .pi/settings).
- Absence des dossiers interdits (`.agent/`, `.pi/memory/`, `evaluations/`).
- Frontmatter SKILL.md (name/description/category/tags/last-verified ; name ==
  dossier parent ; ≤ 500 lignes) — existant.
- Snippets (SNIPPET.yaml + example.go + check.sh) — existant.
- Templates (forme attendue par shape) — existant.
- Bundle offline (manifest, checksums, tailles, licences) — existant.
- Aucun `.md` vide — existant.

### Cohérence (nouveau)

- Chemins `canonical`/`source` de manifest+capabilities existants.
- Vocabulaire manifest↔capabilities identique.
- Comptes recalculés == comptes affichés (zéro compte en dur) — voir C1.
- `run.sh` découvre les probes (glob `probes/*/main.go`) — la liste en dur est
  un échec.
- INDEX généré à jour (knowledge/INDEX.md == arborescence réelle ; aucun
  domaine fantôme).
- Relations des YAML-graphe résolues et jamais vers du `proposed`/inexistant
  (existant, étendre au statut).

### Fraîcheur (nouveau — décision 2026-08-04)

- `last_verified` > 12 mois → warning ; > 18 mois → erreur (statut déprécié
  proposé) pour tout artefact daté (SKILL.md, YAML-graphe, SNIPPET.yaml).
- Catalogue strict opt-in : `KITV2_STRICT_CATALOG=1 python3
  tools/validators/validate-kitv2.py` vérifie les catalogues : section
  `Sources vérifiées` datée, âge (90 jours pour libraries, 180 jours pour
  reference-projects), retours suspects dans les blocs Go et paragraphes
  exactement dupliqués. La duplication sémantique reste une revue humaine.

### Qualité des descriptions (nouveau)

- `description` de chaque SKILL.md : contient l'activation (« Use when » /
  « Load when » / équivalent) — une description sans condition d'activation
  est un échec (goulot de découvrabilité, cf. Red Hat/Anthropic).
- Description > 1024 caractères → échec (déjà contrôlé).

### Par catégorie (nouveau — aligné sur A1)

- Recette : présence d'une section de scénario observable et d'un test ; le
  scénario porte un verdict explicite (`PASS`/`PARTIAL`/`BLOCKED`) — pas de
  recette sans scénario.
- Bibliothèque (module SKILL.md) : critères d'admission énoncés (admission
  checklist) ; alternatives considérées présentes.
- Template : `LICENSE` MIT + `ATTRIBUTION.md` (source, version, adaptations)
  pour tout template non-legacy.
- Rule : impératif + frontière (« ne couvre PAS ») + sources présents.

## 3. Fonctionnement

- Sortie : liste d'erreurs sur stderr + exit code 1 si erreur ; sinon une ligne
  `kitv2: PASS (…)`.
- Chaque contrôle est une fonction isolée, testable, avec un cas positif et un
  cas négatif (tests `test_validate_*.py` — la suite ruff fait partie de la
  gate du metaprojet).
- Les warnings (fraîcheur 12 mois, notes) ne font pas échouer mais sont
  imprimés avec préfixe `warning:`.
- CI (`.github/workflows/ci.yml`) exécute le validateur + la gate Go sur le
  produit.

## 4. Gate Go complète (depuis `KitV2/`)

```sh
python3 tools/validators/validate-kitv2.py
go mod tidy && go mod verify
test -z "$(gofmt -l .)"
go vet ./...
golangci-lint run ./...
go test -race ./...
gosec ./...
govulncheck ./...
bash probes/run.sh
```

Règles :

- `PATH="$PATH:$(go env GOPATH)/bin"` avant les outils (golangci-lint, gosec,
  govulncheck).
- Outil manquant → gate **PARTIAL** documentée, jamais PASS.
- Les checks mécaniques prouvent des propriétés du code ; le scénario
  observable (probe/recette) prouve le comportement ; jamais l'un pour l'autre.

## 5. Anti-patterns

- Validateur qui mute sans test ; contrôle sans cas négatif.
- Compte en dur dans le validateur (EXPECTED_PRODUCT_SKILLS doit devenir dérivé
  ou vérifié contre capabilities — actuellement 45 en dur : à dériver).
- Gate verte malgré un contrat violé.
- Sortie illisible (erreurs sans chemin ni raison actionnable).

## 6. Critères de validation du contrat

- [ ] Chaque contrôle listé en §2 existe (ou est planifié avec issue).
- [ ] Un jeu de tests négatifs couvre chaque contrôle.
- [ ] La gate complète (structure + Go + probes) tourne en CI.
- [ ] Les comptes dérivés remplacent les constantes en dur.
- [ ] Fraîcheur 12/18 mois implémentée.

## 7. Questions ouvertes

- EXPECTED_PRODUCT_SKILLS (45) : dériver depuis l'arborescence ou depuis
  capabilities.yaml ? (proposition : arborescence, capabilities vérifié contre.)
- Faut-il un mode `--strict` (warnings = erreurs) pour la CI ?
