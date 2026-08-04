# Plan — Complétion du graphe de connaissance (29 bibliothèques)

Date : 2026-08-04 · Statut : planifié · Autorité : KIT_CHARTER.md, `.agent/kit-governance/` (Z2, N1, C2)

## Goal

Pour chacune des 29 bibliothèques de `KitV2/knowledge/catalogs/libraries/`
(+ 4 pointeurs pré-1.0), compléter les dossiers de `KitV2/knowledge/` **hors
`catalogs/`** : `patterns/`, `anti-patterns/`, `stdlib/`, `security/`,
`performance/`, `observability/`, `architecture/`, `debugging/` — en ne créant
que les artefacts qui répondent à une question distincte non déjà couverte,
sourcés sur des références primaires, conformes aux contrats Z2/N1/C2.

## Context

- Décision propriétaire (question éditoriale) : **manques réels uniquement** —
  un artefact par question distincte, pas de volume non justifié.
- L'état mesuré : patterns 38, anti-patterns 47, stdlib 21 (pointeurs-only),
  security 2, performance 1, observability 1, architecture 1, debugging 0
  (vide par contrat Z2 §7 : admission sur échec observé et vérifié uniquement).
- Le validateur C2 exige : métadonnées complètes, id/kinds/statuts valides,
  relations résolues, absence de chemins metaprojet. Le router (index.json)
  doit être régénéré après ajout de YAML (`.agent/router/build_index.py`).
- `INDEX.md` est censé être généré (C2) mais aucun générateur n'existe encore ;
  il liste un domaine `cloud/` fantôme (Z2 §9) — à corriger dans ce lot.

## Constraints

- Ne jamais dupliquer un artefact existant (Z2 §4.1) : avant chaque création,
  vérifier la couverture par id/relation (grep ids) et par question.
- Paires pattern ↔ anti-pattern référencées quand l'homologue existe (Z2 §4.2),
  en suivant la convention du corpus (patterns → homologue négatif ; les
  anti-patterns existants référencent des URLs primaires).
- `debugging/` reste vide : aucun échec observé/vérifiée avec procédure de
  diagnostic n'est admis dans ce lot (contrat Z2 §7) — rapporté, pas rempli.
- `go_version` = version minimale testée, jamais future. `last_verified` =
  2026-08-04 (date système). Contenu en français pour patterns/anti-patterns,
  anglais pour les pointeurs Source (convention du corpus).
- Le produit ne référence jamais le metaprojet (aucun chemin `../`, `.agent/`).

## Done

- [ ] Audit bibliothèque par bibliothèque (29) : analyse + audit de couverture
      + conclusion « manque » ou « couvert », rapporté par bibliothèque.
- [ ] Recherche web ciblée pour chaque thème à créer (sources primaires
      vérifiées, URL vivantes).
- [ ] Création des artefacts YAML justifiés (≈13 prévus) : schémas complets,
      relations résolues, fraîcheur OK.
- [ ] Correction `knowledge/INDEX.md` (domaine cloud fantôme, arborescence
      réelle).
- [ ] Gate complète PASS : validate-kitv2.py (avec router régénéré),
      validate-instructions.py, gofmt, vet, golangci-lint, go test -race,
      gosec, govulncheck, probes.
- [ ] Évidence `docs/evidence/2026-08-04/knowledge-completion/` + mémoire
      synchronisée + rapport final.

## Plan d'attaque (ordre catalogue, une bibliothèque à la fois)

| # | Bibliothèque | Manque identifié (question distincte) |
| --- | --- | --- |
| 1 | bleve | perf : merges Scorch (à confirmer par recherche) |
| 2 | bubbles | aucun |
| 3 | bubbletea | aucun (testing-seam-injection couvre) |
| 4 | chi | anti-pattern : confiance IP proxy (RealIP) |
| 5 | cobra | aucun |
| 6 | coder-websocket | anti-pattern CSWSH ; security WS ; pattern streaming (à confirmer) |
| 7 | colorprofile | aucun |
| 8 | fyne | aucun (catalog couvre choix + test headless) |
| 9 | glamour | aucun |
| 10 | go-git | aucun (catalog couvre limites) |
| 11 | harmonica | aucun |
| 12 | huh | aucun |
| 13 | keygen | security : génération de clés SSH |
| 14 | koanf | aucun |
| 15 | lipgloss | aucun |
| 16 | log | aucun |
| 17 | mcp-go-sdk | architecture : forme d'un serveur MCP ; security : outils LLM |
| 18 | modernc-sqlite | aucun (catalog couvre cgo vs pur-Go) |
| 19 | req | aucun (go-mutable-global-state couvre) |
| 20 | ristretto | aucun (catalog + cache-* couvrent) |
| 21 | sequin | aucun |
| 22 | sqlc | anti-pattern : requêtes dynamiques vs codegen statique |
| 23 | ssh | security : durcissement serveur SSH ; anti-pattern : clé hôte réutilisée |
| 24 | templ | perf : templates compilés ; stdlib : html/template |
| 25 | testify | aucun |
| 26 | validator | à vérifier par recherche (limites validation par tags) |
| 27 | viper | aucun |
| 28 | wish | observability : métriques apps SSH |
| — | (pointeurs) | aucun (pré-1.0, hors admission) |

Artefacts prévus (≈13) :

- anti-patterns/ : `sec-ip-trust`, `sec-cswsh`, `db-codegen-dynamic-queries`,
  `sec-ssh-host-key-reuse`
- security/ : `ssh-server-security`, `ssh-key-generation`, `websocket-security`,
  `mcp-tool-security`
- performance/ : `template-compiled-rendering`, `search-index-merge`
- observability/ : `ssh-metrics`
- architecture/ : `mcp-server-shape` (kind Pattern)
- patterns/ : `messaging-websocket-streaming` (à confirmer par recherche)
- stdlib/ : `go-html-template`

## Risques

- Un manque identifié peut tomber après recherche si la source primaire est
  introuvable ou faible → rapporté comme « non justifié ».
- Le router doit être régénéré sinon C2 échoue (compteur + couverture).
- La CI coverage reste rouge (état accepté) — ne pas l'aggraver : ce lot ne
  touche aucun code Go.
