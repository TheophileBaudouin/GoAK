# Analyse de placement — catalogue technologique Go-Agent-Kit (26 technologies)

- **Date :** 2026-08-04
- **Portée :** mapping des 26 technologies du catalogue fourni par l'utilisateur
  (« Go-Agent-Kit Technology Knowledge Base ») sur l'architecture existante de
  `KitV2/` (produit consommable) et du metaprojet (registre des sources).
- **Objet :** décider, pour chaque technologie, si elle est **déjà couverte**,
  **candidate** (à admettre via le portail d'admission), **rejetée** (avec le
  critère et la preuve), ou **hors produit** (spécification/outil externe).
- **Statut :** RECHERCHE — aucune modification du Kit ni du registre. Les
  décisions finales d'admission restent soumises au portail d'admission, à
  l'approbation, et au contrat de zone concerné.
- **Portail d'admission appliqué :** 9 critères (maintenance active vérifiée —
  pas le nombre d'étoiles ; responsabilité unique ; Go idiomatique lisible ;
  tests ; CI ; documentation ; usage réel ; taille parcourable ; raison
  réelle explicite).

---

## 0. Méthode et sources

1. **Cartographie terrain** : inventaire de `KitV2/` (recipes, knowledge
   catalogs, stdlib, observability), du registre des sources
   (`.agent/sources/Go-dev-kit-sources-et-references.md`, 970 lignes), et du
   routeur (`KitV2/router/`) pour déterminer ce qui existe déjà.
2. **Vérification primaire de chaque candidate** : API GitHub (pushed_at,
   archived, stars), go.mod des modules, notes de release, issues ouvertes.
   Les « Summary » de recherche web ont été recoupés avec les données brutes
   API lorsque le statut était douteux (voir §2).
3. **Grille de décision** : décision d'ordre du metaprojet (stdlib d'abord,
   recette existante ensuite, dépendance nouvelle en dernier) + le portail
   d'admission 9 critères + le principe du catalogue lui-même :
   « Never add a technology only because it exists. »

Sources primaires consultées (2026-08-04) :

- api.github.com/repos/{cloudwego/eino, tmc/langchaingo, dgraph-io/ristretto,
  go-git/go-git, fyne-io/fyne, tree-sitter/go-tree-sitter,
  smacker/go-tree-sitter, goccy/go-json, mxschmitt/playwright-go,
  blevesearch/bleve, modelcontextprotocol/go-sdk, asg017/sqlite-vec,
  asg017/sqlite-vec-go-bindings, coder/websocket}
- go.mod : `github.com/tree-sitter/go-tree-sitter`,
  `github.com/mxschmitt/playwright-go`
- coder.com/blog/websocket (annonce de la reprise de nhooyr/websocket)
- tmc/langchaingo issue #1486 (« is this project dead? »)

---

## 1. Matrice de couverture (26 technologies)

| # | Technologie (catalogue) | Importance | État Kit actuel | Décision de placement |
|---|--------------------------|:---:|-----------------|----------------------|
| 1 | Eino | ★5 | absent | **Candidate** — knowledge catalog (patterns d'orchestration) |
| 2 | Langchaingo | ★4 | absent | **Rejetée** — maintenance incertaine (#1486) |
| 3 | Bubble Tea | ★5 | ✅ catalog `bubbletea` + `recipe-cli-interactif` | **Déjà couverte** (import charm.land/bubbletea/v2) |
| 4 | Lipgloss | ★5 | ✅ catalog `lipgloss` | **Déjà couverte** |
| 5 | Cobra | ★4 | ✅ catalog `cobra` + `recipe-cli-cobra` | **Déjà couverte** |
| 6 | Wails | ★5 | ⚠ `recipe-desktop-app` existe, **absent du registre des sources** | **Déjà couverte (écart : registre)** — ajouter Wails au registre |
| 7 | Fyne | ★4 | absent | **Candidate** — catalog, alternative sans navigateur à Wails |
| 8 | Tree-sitter | ★5 | absent | **Candidate** — **attention** : le binding listé (smacker) est abandonné ; utiliser `tree-sitter/go-tree-sitter` (officiel) |
| 9 | Go AST (go/ast) | ★5 | absent de knowledge/stdlib | **Candidate** — knowledge/stdlib (analyse de code native) |
| 10 | gopls | ★5 | absent | **Hors produit** — outil officiel (toolchain), pas une bibliothèque |
| 11 | LSP Protocol | ★5 | absent | **Hors produit** — spécification ; référence registre |
| 12 | go-git | ★5 | absent | **Candidate** — catalog + candidat recette (pas de recette git dans le Kit) |
| 13 | MCP | ★5 | absent | **Candidate forte** — catalog + SDK officiel Go ; alignée direction « Claude Code compatible » |
| 14 | SQLite | ★5 | ✅ via `modernc-sqlite` + `recipe-sqlite-sqlc` | **Déjà couverte** |
| 15 | modernc SQLite | ★4 | ✅ catalog `modernc-sqlite` | **Déjà couverte** |
| 16 | Ristretto | ★4 | absent | **Candidate** — catalog cache |
| 17 | sqlite-vec | ★5 | absent | **Candidate conditionnelle** — voir limites §4.3 |
| 18 | Bleve | ★4 | absent | **Candidate** — catalog recherche plein texte |
| 19 | OpenTelemetry Go | ★4 | ✅ registre + `knowledge/observability/otel-go.yaml` | **Déjà couverte** |
| 20 | goccy/go-json | ★3 | absent | **Rejetée** — maintenance en rafales, bénéfice marginal vs encoding/json |
| 21 | Koanf | ★4 | ✅ catalog `koanf` + `recipe-config-koanf` | **Déjà couverte** |
| 22 | nhooyr websocket | ★4 | absent | **Rejetée** — dépréciée, successeur `coder/websocket` (voir §2.1) |
| 23 | Playwright Go | ★5 | absent | **Candidate** — catalog computer-use ; **import déplacé** `mxschmitt/playwright-go` |
| 24 | Tesseract | ★4 | absent | **Hors produit** — dépendance C/CGO ; à noter comme capacité externe, pas une lib Go |
| 25 | sync.Pool | ★5 | ✅ `knowledge/stdlib/go-sync.yaml` (pools mentionnés) | **Déjà couverte** |
| 26 | errgroup | ★5 | ✅ `recipe-worker-pool` (errgroup.SetLimit) | **Déjà couverte (écart : registre)** — `golang.org/x/sync` absent du registre |

**Bilan :** 11 déjà couvertes · 8 candidates · 4 rejetées · 3 hors produit ·
2 écarts de registre (Wails, errgroup/x-sync).

---

## 2. Corrections de faits au catalogue source (vérifiées, 2026-08-04)

Quatre entrées du catalogue sont obsolètes ou inexactes par rapport aux
sources primaires. Toute admission future doit utiliser les références
corrigées.

### 2.1 nhooyr/websocket → dépréciée, successeur coder/websocket

- `github.com/nhooyr/websocket` n'est **plus maintenue** ; l'auteur a annoncé
  la reprise par Coder : `github.com/coder/websocket` (même API, import path
  différent). Source : coder.com/blog/websocket.
- **Décision :** l'entrée du catalogue est **rejetée telle quelle**. Si une
  recette WebSocket voit le jour, elle doit citer `coder/websocket`.

### 2.2 Tree-sitter : le binding listé est abandonné

- `smacker/go-tree-sitter` : dernière poussée 2024-08-27, considéré abandonné
  (0 commit/90 jours, issues le confirmant).
- Le binding **officiel** existe : `tree-sitter/go-tree-sitter`
  (module `github.com/tree-sitter/go-tree-sitter`, poussé 2025-11-16, 285★,
  non archivé, description « Go bindings for tree-sitter »).
- **Décision :** toute admission tree-sitter doit référencer l'officiel,
  jamais smacker.

### 2.3 Playwright Go : import path déplacé

- `playwright-community/playwright-go` redirige (Moved Permanently) vers
  `mxschmitt/playwright-go` ; le module est `github.com/mxschmitt/playwright-go`
  (poussé 2026-07-17, 3458★). Releases fréquentes (roll driver v1.61.1).
- **Décision :** référencer `mxschmitt/playwright-go`.

### 2.4 Bubble Tea : import déjà corrigé dans le Kit

- Le catalogue liste `github.com/charmbracelet/bubbletea` ; le Kit connaît déjà
  la vérité : v2 stable à `charm.land/bubbletea/v2` (gotcha 2026-08-01,
  `tea.KeyPressMsg`, `tea.NewView(s)`). Aucun changement nécessaire.

---

## 3. Décisions de placement par famille

### 3.1 Frameworks agent (Eino, Langchaingo) — zone knowledge

Le Kit n'est pas un framework : « compact registry of sourced Go patterns ».
Les frameworks d'orchestration n'entrent **pas comme dépendances de recettes**,
mais comme **patterns étudiables** (zone `knowledge/catalogs/libraries/` ou
`knowledge/architecture/`).

- **Eino** (cloudwego, ByteDance) : maintenu activement (~12k★, v0.9
  « agentic-runtime », nouvelles abstractions AgenticMessage). Le catalogue
  lui-même recommande « Study architecture patterns. Use only where
  abstractions provide value. » → **candidate** pour un catalog de type
  « étudier les patterns d'orchestration, ne pas dépendre » (même posture que
  `req` = extract-only dans le Kit).
- **Langchaingo** (tmc) : maintenance **incertaine** — issue #1486
  « is this project dead? » (2026), pas de release épinglée, PR fusionnées
  sporadiques. Échec du critère 1 (maintenance active) du portail →
  **rejetée**, à réévaluer si le projet reprend.

### 3.2 TUI / CLI / Desktop (Bubble Tea, Lipgloss, Cobra, Wails, Fyne)

- Bubble Tea, Lipgloss, Cobra : **déjà couvertes** (catalogs + recettes).
- **Wails : écart de registre.** La recette `recipe-desktop-app` (wails v3,
  logique de service testable, pinning explicite car v3 Beta-to-GA) existe,
  mais Wails n'est **pas** dans `.agent/sources/`. → ajouter une entrée
  registre (Niveau A — très utile) et vérifier la cohérence du router.
- **Fyne** : très actif (v2.8.0, « biggest release since v2.0.0 », Go 1.22+).
  Alternative pure Go sans navigateur. → candidate catalog ; à positionner
  comme « choisir Fyne quand l'app est pure Go/embarqué, Wails quand le
  frontend web est souhaité ».

### 3.3 Code intelligence (Tree-sitter, Go AST, gopls, LSP)

- **Tree-sitter (officiel)** : candidat catalog (parsing incrémental pour
  agents coding). Voir correction §2.2.
- **Go AST (go/ast)** : stdlib ; le Kit a déjà `knowledge/stdlib/` (14 unités)
  mais pas go/ast → candidate knowledge/stdlib (analyse de code, refactoring,
  génération).
- **gopls / LSP Protocol** : **hors produit** — ce sont un outil officiel et
  une spécification, pas des dépendances Go. Leur place est le registre des
  sources (références) et la connaissance toolchain, pas les catalogs de
  bibliothèques.

### 3.4 Git / MCP / WebSocket (intégrations agents)

- **go-git** : actif (v5.19.1, v6 alpha, 310 contributeurs, utilisé par
  Gitea/Pulumi, Apache-2.0). → candidate catalog **+ candidat recette** : le
  Kit n'a aucune recette git alors que la direction « Claude Code style
  agents » en aura besoin (commits, diffs, analyse de repo).
- **MCP** : spécification + SDK officiel Go (`modelcontextprotocol/go-sdk`,
  v1.7.0, maintenu avec Google). → candidate forte : c'est le standard
  d'interopérabilité agents/outils, essentiel pour « Claude Code compatible
  agents ». Un catalog + une future recette serveur MCP.
- **WebSocket** : voir §2.1 — coder/websocket en remplacement.

### 3.5 Stockage / recherche (SQLite, modernc, sqlite-vec, Bleve)

- SQLite / modernc : **déjà couvertes**.
- **sqlite-vec** : maintenance **conditionnelle** — v0.1.7 « revival »
  (workflows réparés, tests), mais doc stale et bindings Go officiels dans un
  dépôt séparé (`asg017/sqlite-vec-go-bindings`), CGO + WASM selon l'usage.
  → candidate seulement si un besoin local RAG/vectoriel se matérialise ;
  noter que le router du Kit a explicitement écarté les embeddings (décision
  2026-08-05) — cohérence à vérifier avant toute admission.
- **Bleve** : actif (v2.5.7, 11 contributeurs actifs, Apache-2.0). → candidate
  catalog (recherche plein texte locale ; complémentaire de sqlite-vec).

### 3.6 Cache / observabilité / config / JSON

- **Ristretto** : actif (v2.4.0, releases 2025, « production-ready »). →
  candidate catalog cache.
- OpenTelemetry / Koanf : **déjà couvertes**.
- **goccy/go-json** : maintenance en rafales (v0.10.6 mars 2026 mais 0
  activité sur 90 jours précédents). Importance ★3 dans le catalogue ; le Kit
  privilégie encoding/json (anti-pattern `go-json-omitempty-zero`). → **rejetée**
  (critère 1 fragile + bénéfice marginal, YAGNI).

### 3.7 Browser / vision (Playwright Go, Tesseract)

- **Playwright Go** : actif, import corrigé §2.3. → candidate catalog
  (computer-use agents, web automation). Recette seulement si un scénario
  exécutable observable est défini (le binaire driver est lourd — portail :
  « small enough to read end-to-end » à nuancer).
- **Tesseract** : bibliothèque C, bindings Go via CGO. Le Kit privilégie
  zéro-CGO (modernc vs mattn). → **hors produit** : à noter comme capacité
  externe (sous-processus/CLI), pas comme dépendance Go.

### 3.8 Performance (sync.Pool, errgroup)

- sync.Pool : couvert par `knowledge/stdlib/go-sync.yaml`.
- **errgroup** : couvert par `recipe-worker-pool`, mais `golang.org/x/sync`
  est **absent du registre des sources** → écart à combler (Niveau A).

---

## 4. Évaluation des candidates selon les 7 critères du catalogue

Grille (réduite) appliquée aux 8 candidates :

| Candidate | Réduit la complexité ? | Améliore la capacité agent ? | Réduit les tokens ? | Petite machine ? | Doc ? | Maintenu ? | Remplaçable ? | Verdict |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---------|
| Eino (patterns) | non (étudier) | oui | non | n/a | oui | ✅ | oui | catalog extract-only |
| Fyne | oui (pur Go) | indirect | n/a | oui | oui | ✅ | oui | catalog |
| go-tree-sitter | oui | oui (parsing) | oui (précis) | oui | partielle | ✅ | oui | catalog |
| go/ast | oui (stdlib) | oui | oui | oui | oui | ✅ | n/a | knowledge/stdlib |
| go-git | oui | oui | n/a | oui | oui | ✅ | oui | catalog + recette |
| MCP Go SDK | oui (standard) | oui (interop) | n/a | oui | oui | ✅ | oui | catalog + recette |
| Ristretto | oui | oui (cache) | oui | oui | oui | ✅ | oui | catalog |
| sqlite-vec | oui (local) | oui (RAG) | oui | oui | ⚠ stale | ⚠ revival | oui | conditionnelle |
| Bleve | oui | oui (recherche) | oui | moyen | oui | ✅ | oui | catalog |
| Playwright Go | oui (automation) | oui (computer-use) | non | non (driver lourd) | oui | ✅ | oui | catalog (recette à condition) |

---

## 5. Rejets enregistrés (critère + preuve)

| Technologie | Critère du portail | Preuve |
|-------------|-------------------|--------|
| nhooyr/websocket | maintenance (dépréciée) | coder.com/blog/websocket ; le dépôt n'est plus maintenu |
| Langchaingo | maintenance (incertaine) | tmc/langchaingo#1486 « is this project dead? » |
| goccy/go-json | maintenance fragile + YAGNI | v0.10.6 (2026-03) mais 0 activité/90 j avant ; encoding/json suffit pour le Kit |
| smacker/go-tree-sitter | maintenance (abandonné) | dernière poussée 2024-08-27 ; remplacé par l'officiel |

---

## 6. Recommandations et prochaines étapes

**Aucune modification n'est faite par ce document.** Les prochaines étapes
proposées, chacune soumise au contrat de zone + portail + approbation :

1. **Écarts de registre (rapides, sans débat)** : ajouter `wails` et
   `golang.org/x/sync` (errgroup) au registre des sources ; régénérer le
   routeur.
2. **Vague candidate knowledge (catalogs)** : Eino (extract-only patterns),
   Fyne, go-tree-sitter (officiel), Ristretto, Bleve, Playwright Go (import
   corrigé), MCP Go SDK — chacune avec un SKILL.md passant `validate-kitv2.py`
   et une vérification issue-mining (thèmes ≥3 occurrences) avant admission.
3. **Candidates knowledge/stdlib** : go/ast.
4. **Candidats recette (à étudier)** : go-git (commits/diffs/repo analysis),
   MCP (serveur outil). Chacune exige un scénario exécutable observable.
5. **Registre des sources (hors produit)** : gopls, LSP Protocol, Tesseract
   (capacité externe), sqlite-vec (avec ses limites documentées).
6. **Réévaluation planifiée** : Langchaingo (si reprise de maintenance),
   sqlite-vec (si doc + bindings stabilisés).

---

## 7. Rappel du principe directeur

Le catalogue lui-même le dit et le Kit le codifie : *Never add a technology
only because it exists. A dependency must solve a concrete problem.* Sur les
26 technologies, 11 sont déjà couvertes ; les admissions à venir doivent
toutes démontrer un besoin concret observable — aucune ne doit entrer « parce
que c'est dans le catalogue ».

---

## Addendum — Core Infrastructure (4 technologies) — revue critique

- **Date :** 2026-08-04
- **Source :** « Go-Agent-Kit Technology Knowledge Base — Core Infrastructure
  Addendum » (coder/websocket, tree-sitter/go-tree-sitter,
  mxschmitt/playwright-go, temporalio/sdk-go).
- **Posture demandée :** être critique avec ce document d'ajout et vérifier que
  chaque technologie « a sa place dans le kit suivant les règles de celui-ci ».
- **Méthode :** mêmes portails que §0 — vérification primaire API GitHub
  (pushed_at, archived, tags, releases), go.mod, structure du dépôt, puis
  application stricte des règles du Kit : décision d'ordre, portail 9 critères,
  **exclusion pré-1.0/expérimental** (précédent ligne 795 du registre :
  fantasy, catwalk… exclus), **préférence zéro-CGO** (modernc > mattn),
  « petit et parcourable », « petite machine ».

## Résultat global

Le tableau « Technology Selection Summary » de l'addendum dit **« Recommended:
Yes » pour les 4 sans aucune condition**. La revue critique conclut :

| Technologie | Addendum | Verdict Kit (revue critique) |
|-------------|----------|------------------------------|
| coder/websocket | Yes ★5 | ✅ **Candidate catalog** — conforme, sans condition |
| tree-sitter/go-tree-sitter | Yes ★5 | ⚠ **BLOQUÉE** — pré-1.0 (v0.24.0) + CGO ; exclue par les règles actuelles |
| mxschmitt/playwright-go | Yes ★5 | ⚠ **Candidate catalog conditionnelle** — binaire driver lourd |
| temporalio/sdk-go | Yes ★5 | ❌ **REJETÉE** pour le Kit — échoue 3 critères + décision d'ordre ; au mieux entrée registre |

Seul coder/websocket passe sans condition. Les trois autres nécessitent une
décision propriétaire explicite ou une réévaluation — l'addendum ne fournit
aucun des deux.

## 8.1 coder/websocket — candidate catalog ✅

- **Vérifié :** v1.8.15 (2026-06-15), non archivé, 5373★, cadence régulière
  (v1.8.12 → v1.8.15 sur 2024-2026). Successeur officiel de nhooyr/websocket
  (correction déjà documentée §2.1 de ce rapport).
- **Règles du Kit :** version ≥1.0 ✅ · zéro-CGO ✅ (pur Go) · responsabilité
  unique ✅ (transport WebSocket seulement, l'addendum le dit) · petit ✅ ·
  remplaçable ✅ (API proche de gorilla/websocket).
- **Placement :** knowledge catalog (library) + futur candidat recette
  transport streaming — cohérent avec les usages cités (streaming LLM, MCP
  transport). Pas de recette immédiate : aucun scénario exécutable n'est
  défini dans le Kit aujourd'hui.
- **Réserve :** l'addendum dit « Primary WebSocket implementation for
  Go-Agent-Kit ». Exact pour la couche transport ; il ne faut pas en faire une
  dépendance de recette tant qu'aucun besoin concret n'existe (YAGNI).

## 8.2 tree-sitter/go-tree-sitter — BLOQUÉE par les règles actuelles ⚠

- **Vérifié :** **aucune release GitHub « latest »** ; tags `v0.24.0`, `v0.23.x`
  → **pré-1.0**. Dépôt actif (23 fichiers .go, poussé 2025-11-16, non
  archivé), mais :
  - **Exclusion pré-1.0 du registre** : la ligne 795 du registre des sources
    exclut explicitement « les bibliothèques pré-1.0 ou expérimentales
    (fantasy, catwalk, …) ». go-tree-sitter v0.24.0 est dans ce cas.
  - **CGO obligatoire** : `language.go` contient `#cgo CFLAGS: … -std=c11`,
    `import "C"`, `unsafe` ; go.mod dépend de `mattn/go-pointer` + grammaires C
    (`tree-sitter-go`…). Le Kit privilégie zéro-CGO (modernc.org/sqlite au
    lieu de mattn/go-sqlite3). CGO = build tags, cross-compilation et petites
    machines compliqués.
- **Ce que dit l'addendum :** « Recommended: Yes » — sans mentionner ni la
  version pré-1.0 ni le CGO. La recommandation ignore deux règles du Kit.
- **Placement honnête :** (a) réévaluer après une release ≥1.0, ou (b) décision
  propriétaire explicite pour lever l'exclusion pré-1.0, avec une réserve CGO
  documentée dans la recette/catalog. En attendant : **pas d'admission**. Le
  besoin « code intelligence » reste couvert par go/ast (stdlib, zéro-CGO) et
  par les outils externes gopls/LSP (registre des sources).

## 8.3 mxschmitt/playwright-go — candidate catalog conditionnelle ⚠

- **Vérifié :** module `github.com/mxschmitt/playwright-go` (correction §2.3),
  actif (roll driver v1.61.1, poussé 2026-07-17, 3458★).
- **Règles du Kit :** version ≥1.0 ✅ · maintenance ✅ · doc ✅ · mais :
  - **« petit et parcourable de bout en bout »** : binding sur un driver
    binaire énorme (Chromium/Firefox/WebKit téléchargés à l'install) —
    échoue l'esprit du critère « small enough to read end-to-end ».
  - **Petite machine** : l'addendum admet « higher resource consumption ».
- **Placement honnête :** catalog **extract-only** (mêmes patterns que `req` /
  ardanlabs-service) : documenter quand l'automatisation navigateur se
  justifie (« API first » — l'addendum le dit lui-même) sans en faire une
  dépendance de recette tant qu'aucun scénario exécutable observé n'existe.
  L'usage « computer-use agents » reste une capacité externe à documenter.

## 8.4 temporalio/sdk-go — REJETÉE pour le Kit ❌

- **Vérifié :** v1.47.0 (2026-07-28), actif, non archivé, 941★. **395 fichiers
  .go**, **19 dépendances directes** (gogo/protobuf, grpc-middleware,
  nexus-rpc/sdk-go, robfig/cron, facebookgo/clock…), **exige un serveur
  Temporal externe**.
- **Critères du portail :**
  - « petit et parcourable de bout en bout » → **échec** (395 fichiers).
  - « petite machine » / déploiement simple → **échec** (infrastructure serveur
    externe, opérations supplémentaires — l'addendum l'admet).
  - responsabilité unique → discutable (workflows + retries + timers + task
    queues + human-in-the-loop = un framework distribué, pas une lib).
  - « remplaçable » → **échec** : l'infrastructure verrouille l'écosystème.
  - **Décision d'ordre du Kit** : la recette `recipe-worker-pool`
    (errgroup.SetLimit) couvre déjà le fan-out borné avec première-erreur ;
    `recipe-graceful-shutdown` couvre la fermeture propre. Pour les workflows
    multi-étapes simples, stdlib + errgroup suffisent (l'addendum admet
    « Overkill for simple synchronous tasks »).
- **Ce que dit l'addendum :** « Recommended: Yes » pour le layer
  « reliability and execution » — mais ce layer contredit l'objectif du Kit
  (réduire les décisions, rester vérifiable par le comportement observable
  d'applications petites et composables).
- **Placement honnête :** au mieux une **entrée registre des sources**
  (Niveau B — selon projet) documentant le pattern « durable execution »
  (déterminisme des workflows, retry policies, replay) comme référence pour
  les agents longue durée — sans dépendance, sans recette, sans catalog
  library. Une admission library/recette exigerait une décision propriétaire
  explicite contraire aux règles actuelles.

## 8.5 Intégration philosophy — alignée, à nuancer

L'addendum affirme : « These technologies solve different problems…
Each dependency must justify itself. » C'est exactement la philosophie du Kit.
La nuance : les 4 couches proposées (communication / compréhension / monde
extérieur / exécution) sont toutes **optionnelles** — aucune n'est requise par
un agent Go minimal, et deux d'entre elles (tree-sitter, Temporal) ne peuvent
pas entrer telles quelles aujourd'hui. « Prefer small, composable,
well-maintained, replaceable, Go-native » : coder/websocket ✅, les trois
autres doivent attendre une décision ou une réévaluation.

## 8.6 Bilan révisé (26 + 4)

- **Déjà couvertes :** 11 (inchangé).
- **Candidates :** coder/websocket, Fyne, go-git, MCP Go SDK, Ristretto, Bleve,
  go/ast + **Eino (patterns)**, **playwright-go (extract-only)** → 9.
- **Conditionnelles / bloquées :** sqlite-vec (revival), **tree-sitter
  (pré-1.0 + CGO — réévaluer ≥1.0 ou décision)**.
- **Rejetées :** nhooyr/websocket, Langchaingo, goccy/go-json,
  smacker/go-tree-sitter + **temporalio/sdk-go (pour le Kit)**.
- **Hors produit :** gopls, LSP Protocol, Tesseract.
- **Écarts de registre :** Wails, golang.org/x/sync (errgroup).

**Règle d'action :** l'addendum recommande 4 technologies en bloc ; le Kit n'en
admet qu'une sans condition. Toute admission future doit citer cette revue et
lever explicitement les blocages (version ≥1.0, zéro-CGO, petitesse,
remplaçabilité) — pas le « Recommended: Yes » de l'addendum.
