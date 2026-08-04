# Rapport — Complétion du graphe de connaissance (29 bibliothèques)

Date : 2026-08-04 · Plan : `docs/plans/2026-08-04-knowledge-completion.md` ·
Évidence brute : `docs/evidence/2026-08-04/knowledge-completion/evidence.md`

## Décision éditoriale (question posée)

Une seule question posée (volume) : réponse **« Manques réels uniquement »** —
un artefact par question distincte non couverte, sourcé, sans duplication ni
padding. Le contrat `debugging/` (Z2 §7, admission sur échec observé) est
respecté : dossier resté vide volontairement.

## Fichiers créés (14)

| Fichier | id | Bibliothèque | Question distincte |
| --- | --- | --- | --- |
| `anti-patterns/sec-ip-trust.yaml` | pattern:antipattern:sec-ip-trust | chi | confiance IP client depuis en-têtes proxy (RealIP, 3 GHSA) |
| `anti-patterns/sec-cswsh.yaml` | pattern:antipattern:sec-cswsh | coder-websocket | Cross-Site WebSocket Hijacking (origin absente) |
| `anti-patterns/db-codegen-dynamic-queries.yaml` | pattern:antipattern:db-codegen-dynamic-queries | sqlc | requêtes dynamiques vs codegen statique (#3414, #2061, #364) |
| `anti-patterns/sec-ssh-host-key-reuse.yaml` | pattern:antipattern:sec-ssh-host-key-reuse | ssh, wish | clé hôte partagée / régénérée (MITM, pinning) |
| `security/websocket-security.yaml` | source:websocket:security | coder-websocket | guidance WebSocket (origin, WSS, auth, monitoring) |
| `security/ssh-key-generation.yaml` | source:ssh:key-generation | keygen | génération de clés SSH (algorithmes, formats, protection) |
| `security/ssh-server-security.yaml` | source:ssh:server-security | ssh | durcissement serveur SSH Go (host keys, auth) |
| `security/mcp-tool-security.yaml` | source:mcp:tool-security | mcp-go-sdk | outils LLM/MCP comme frontière de confiance (OWASP LLM Top 10) |
| `security/input-validation.yaml` | source:security:input-validation | validator | stratégie de validation à la frontière, limites des tags |
| `performance/search-index-merge.yaml` | source:search:index-merge | bleve | Scorch segments/merges, amplification d'écriture |
| `performance/template-compiled-rendering.yaml` | source:template:compiled-rendering | templ | templates compilés vs interprétés (benchmarks) |
| `observability/ssh-metrics.yaml` | source:wish:ssh-metrics | wish | métriques Prometheus d'apps SSH (promwish) |
| `architecture/mcp-server-shape.yaml` | pattern:architecture:mcp-server-shape | mcp-go-sdk | forme d'un serveur MCP (primitives, transport, frontière) |
| `stdlib/go-html-template.yaml` | source:go:html-template | templ | pointeur html/template (auto-escaping, XSS) |

## Fichiers modifiés

- `KitV2/knowledge/INDEX.md` — domaine `cloud/` fantôme retiré (Z2 §9),
  domaine `observability/` ajouté, statuts alignés sur l'arborescence réelle.
- `KitV2/router/index.json` + `meta.json` — régénérés (206 → 231 ressources ;
  nouveau sha256 ; `--check` OK).

## Recherches effectuées (sources primaires vérifiées)

- **bleve** : index/scorch/README.md, docs/persister.md, issue #1783 (batching),
  pkg.go.dev mergeplan.
- **chi** : GHSA-9g5q-2w5x-hmxf, GHSA-rjr7-jggh-pgcp, GHSA-3fxj-6jh8-hvhx,
  PR #967 (ClientIP), MDN X-Forwarded-For, OWASP IP Spoofing, RFC 7239.
- **coder-websocket** : OWASP WebSocket Security Cheat Sheet, CWE-1385, WSTG,
  coder/websocket accept.go (OriginPatterns), MDN Writing WebSocket servers.
- **sqlc** : issues #3414, #2061, #364, #2348 ; brandur.org (limites CASE).
- **keygen/ssh** : ssh-keygen(1) OpenBSD, pkg.go.dev x/crypto/ssh (server.go,
  example_test.go), charm.land/ssh, wish README, sshd_config.5,
  security.stackexchange (clés hôte dupliquées).
- **mcp-go-sdk** : spec MCP 2026-07-28, server-concepts, architecture index,
  go.sdk.modelcontextprotocol.io (lifecycle), OWASP LLM Top 10 2025, LLM01.
- **templ** : a-h/templ/benchmarks (officiel), amaro0/templ-benchmark
  (indépendant), pkg.go.dev/html/template.
- **validator** : pkg.go.dev go-playground/validator, issue #952 (dive),
  #773/#899 (CVEs transitives), OWASP Input Validation Cheat Sheet.
- **wish** : charmbracelet/promwish, wish README, issue #325 (ordre auth/ratelimit).

## Décisions prises

1. Volume « manques réels uniquement » (réponse utilisateur).
2. Pattern streaming WebSocket **écarté** : la mécanique est déjà couverte par
   le catalog coder-websocket (Notes) — pas de question distincte (Z2 §4.1).
3. `debugging/` laissé vide (contrat Z2 §7) — aucun échec observé/vérifié avec
   procédure de diagnostic n'a été admis ; candidats mentionnés en roadmap.
4. Convention des paires : patterns → homologue négatif référencé ; les
   anti-patterns référencent des URLs primaires (convention du corpus, pas de
   nouvelle convention introduite).
5. URLs canoniques conservées même > 80 caractères (corpus existant) ; pour
   les 3 lignes `source:` signalées, échappement YAML `"...\<LF>  suite"`
   (URL résolue identique, vérifié par yaml.safe_load).
6. Bibliothèques sans manque justifié (audit complet, zéro artefact) : bubbles,
   bubbletea, cobra, colorprofile, fyne, glamour, go-git, harmonica, huh,
   koanf, lipgloss, log, modernc-sqlite, req, ristretto, sequin, testify,
   viper + pointeurs pré-1.0 — couvertes par les patterns/anti-patterns/règles
   existants et les décisions des catalogs (aucune duplication admise).

## Questions posées

Une seule (volume de complétion) — réponse : manques réels uniquement.

## Problèmes rencontrés

1. **pi-lens MD013 (ligne > 80)** sur les URLs canoniques des nouveaux YAML —
   résolu partiellement (échappement YAML sur 3 `source:`), le reste suit la
   convention corpus ; consigné en Gotcha.
2. **Advisory typos** sur le contenu français des anti-patterns (vérificateur
   anglais) — faux positifs, convention corpus (contenu FR), non bloquant.
3. **govulncheck** : 1 vulnérabilité dans des packages importés, non appelée
   par le code — état préexistant (aucun code Go modifié), conforme à la gate.

## Validation

Gate complète PASS : validate-kitv2.py (51 skills, router 231), validate-
instructions.py, gofmt, go vet, golangci-lint 0, go test -race (0 FAIL),
gosec 0, probes 5/5, router `--check` OK. CI coverage reste l'état accepté
(rouge préexistant, zéro code Go touché par ce lot).

## Éléments restants à améliorer

- `knowledge/INDEX.md` reste maintenu à la main : le générateur d'index prévu
  par Z2/C1 (tools/generators/) n'existe pas encore — à implémenter pour que
  C2 compare automatiquement (contract 16-zone-tools).
- Fraîcheur : les artefacts créés portent `last_verified: 2026-08-04` ; le
  cycle 12/18 mois les revalidera.
- La question « faut-il un domaine cloud/ réel » reste ouverte (Z2 §9) — aucun
  artefact cloud admis à ce jour.

## Addendum — Durabilisation du pipeline (gouvernance, 2026-08-04)

- **Contrats mis à jour** : `Z2 §9` (Pipeline de complétion du graphe —
  9.1 étapes, 9.2 admission manques réels, 9.3 contrôles de sortie
  vérifiables ; ancien §9 renuméroté §10), `N1 §3` (conventions YAML :
  URLs canoniques + échappement `"...\<LF>  suite"`, langue par catégorie,
  post-écriture safe_load).
- **Mémoire** : Agent.md « Library knowledge pipeline » (règle durable),
  Decisions.md « Knowledge completion pipeline (2026-08-04) », Brief.md
  (section Decisions), Gotchas.md (Notes des catalogs couvrent les limites).
- **Revue fresh-context** : APPROVE-WITH-NITS (subagent reviewer, run
  e7657d77) — nits intégrés : §4.4 Z2 reformulé (INDEX « censé être »
  généré, générateur en attente), critère C2 §9.3 précisé (schémas/fraîcheur
  = contrôles contractés non encore implémentés), formulations N1 clarifiées.
- **Gate** : validators + router --check PASS (aucun impact produit).
