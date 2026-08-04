# Évidence — Semantic Resource Router (2026-08-05)

## Objet

Système de routage sémantique par index pour le kit : un agent Pi trouve les
ressources pertinentes (~206) sans charger le kit dans le contexte. Index
généré par le méta-projet (`.agent/router/build_index.py`), embarqué en
lecture seule (`KitV2/router/`), interrogé par l'outil Pi natif
`search_kit_resources` (`.pi/extensions/kit-resource-router.ts`), encadré par
la skill `kit-resource-routing`.

## Décisions (validées utilisateur 2026-08-05)

BM25 sans embeddings · stockage JSON versionné · recherche obligatoire avant
tout travail technique · outil = extension Pi native. Plan :
`docs/plans/2026-08-05-resource-router.md`. Contrat de zone : Z11.

## Scénarios de routage (copie consommateur fraîche, index v2.2.0, 206 ressources)

Runs : `pi -a -p "Call search_kit_resources with query '…' …"` depuis
`/tmp/gak-consumer/target` (arborescence extraite exactement comme
`install.sh`, validateur PASS avant les runs). Sorties brutes dans `raw/`.

| Scénario | Requête | Top-1 (score) | Verdict |
| --- | --- | --- | --- |
| Évident | bounded worker pool with context cancellation | recipe-worker-pool (44.08) | ✅ attendu |
| Vague | build a go service | recipe-rest-chi (8.31) | ✅ utile |
| Sans résultat | quantum computing compiler | *No kit resource matches* (garde hors-domaine, 2/3 termes sans couverture) | ✅ vide > bruit |
| Multiples proches | http rest api with routing and json | recipe-rest-chi, checklist-api, http-json, chi (catalogues conditionnels Gin/Echo rétrogradés) | ✅ canonique d'abord |
| Français | base de donnees sqlite avec sqlc | recipe-sqlite-sqlc (26.03) | ✅ synonymes fr/en |
| Template | scaffold a new project template | go-template-cli, go-template-grpc, go-template-microservice | ✅ shapes indexées |
| Messaging | kafka producer consumer streaming | source:go:franz-go (22.15), dead-letter-queue | ✅ synonymes domaine |

## Qualité du routage

- **Faux positifs minimisés** : pénalité ×0.6 sur les catalogues conditionnels
  (« explicitly requires ») ; poids ×1.15 recette / ×1.1 règle / ×1.05 pattern.
- **Faux négatifs évités** : garde hors-domaine calculée sur les tokens
  *étendus* (synonymes = pont de vocabulaire) avec seuil 0.5 — rejette
  « quantum computing compiler » (66 %), accepte « kafka producer consumer
  streaming » (42 % via synonymes messaging).
- **Protection du contexte** : top-K ≤ 5 par défaut (max 8), résultats courts
  (chemin + termes matchés + description ≤ 200 caractères), jamais de fichiers.

## Gate (sorties dans `raw/gate.txt`)

- Builder : 11 tests OK (déterminisme, couverture, drift, schéma) ; `--check` up to date.
- Validateur produit : `kitv2: PASS (… router index 206 resources)` — vérifie
  schéma, hash index.json ↔ meta.json, couverture complète des zones
  indexables, chemins existants.
- Harness méta-projet : `instruction-artifacts: PASS` (frontmatter skill valide).
- ruff : clean.
- Gate Go (KitV2) : gofmt OK · go vet OK · `go test -race` OK ·
  golangci-lint 0 · gosec 0 · govulncheck sans vulnérabilité appelée ·
  probes 5/5 PASS.

## Installation propre

`/tmp/gak-consumer/target` : extraction tar du sous-arbre `KitV2/` (mécanique
identique à `install.sh`), validateur PASS, aucun `.pi/memory/` embarqué,
`router/index.json` + extension + skill présents. Découverte Pi réelle :
extension auto-chargée (projet approuvé `-a`), outil appelable, index résolu
via `../../router/` depuis l'extension.

## Limites connues

- LSP : l'extension produit des erreurs de résolution de modules dans un repo
  Go sans node_modules (typebox/@earendil-works fournis par le runtime Pi) —
  stubs éditeur-only dans `.pi/extensions/types/` ; le contrôle autoritaire
  est l'exécution pi (documentée ci-dessus), pas le langage server.
- Le scénario « multi » dans `raw/multi.txt` est un rendu LLM (l'agent a
  reformaté) ; la sortie déterministe de l'outil est celle des autres runs.
- La recherche ne couvre que les descriptions curées du frontmatter : un
  contenu profond non décrit peut être manqué (limite assumée du routage).

## Revue fraîche-contexte (2026-08-05)

Verdict : **APPROVE-WITH-NITS** (aucun blocage, aucune violation de
correctness ni de frontière méta-projet/kit). 5 nits corrigés :

- Décision du routeur enregistrée dans `.pi/memory/Decisions.md` (N1).
- `known_limits` « No Git repository exists » périmé retiré ; le `---`
  final de capabilities.yaml supprimé (fichier parseable) (N2).
- Docstring du builder alignée sur la sortie réelle (pas de build date) (N3).
- `check_router` vérifie désormais meta.version == manifest.version (N4) —
  cas positif + négatif ajoutés (12 tests).
- Globs snippets alignés builder/validateur (`*/SNIPPET.yaml`) (N5).
