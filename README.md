# Go Agent Development Kit (GoAK)

Kit de développement Go pour agents de code : règles, recettes, snippets,
templates, catalogues sourcés et vérifications exécutables, organisés en graphe
de connaissances typé (pas un dossier de snippets, pas un framework). Le produit
consommable est `KitV2/` ; la racine du dépôt est le metaprojet qui le
gouverne (charte, registre de sources, plans et évidence).

## Installation — une commande

```sh
curl -fsSL https://raw.githubusercontent.com/TheophileBaudouin/GoAK/v2.1.0/install.sh | sh -s -- go-agent-kit
```

Installe le produit dans `./go-agent-kit` (ref épinglée par défaut `v2.1.0` ;
surchargez avec `GAK_REF=main` ou `GAK_REF=<commit>` pour une autre référence).
L'installation est vérifiée par le validateur produit ; un outil manquant est
signalé `PARTIAL`, jamais `PASS`.

## Prise en main

```sh
cd go-agent-kit
pi                                  # charge AGENTS.md, .pi/prompts et .pi/skills
bash probes/run.sh                  # probes exécutables du produit (toolchain Go requise)
```

Les templates de workflow natifs `.pi/prompts/workflow-*` guident le travail
non trivial (clarifier → planifier → tâches → implémenter → vérifier).

## Gate de validation du produit

Depuis `KitV2/` (ou le répertoire installé) :

```sh
python3 tools/validators/validate-kitv2.py
go test ./...
test -z "$(gofmt -l .)"
go vet ./...
bash probes/run.sh
```

La gate locale complète ajoute `golangci-lint`, `gosec` et `govulncheck`
(outils épinglés dans `$(go env GOPATH)/bin`).

## Structure du dépôt

- `KitV2/` — le produit consommable (standalone) : `rules/`, `recipes/`,
  `snippets/`, `templates/`, `knowledge/`, `probes/`, `tools/offline/`
  (resolveur hors-ligne + bundle Effective Go épinglé), `.pi/`.
- `.agent/`, `.pi/memory/`, `docs/` — gouvernance metaprojet uniquement,
  jamais installée chez un consommateur.
- `install.sh` — installeur bootstrap de la version arborescente.

## Statut

Première version benchmarkable : `v2.1.0` (marqueur de version, pas encore une
politique de release formelle). Le CLI canonique de distribution (`gak` :
`init`, `update`, `doctor`, `validate`, `remove`, `info`), le module Go publié
et le pipeline de release restent à venir ; `install.sh` est l'installeur
transitoire.
