# Rapport de recherche — Anti-patterns pour le Go Agent Kit (2026-08-04)

## Objectif

Remplir `KitV2/knowledge/anti-patterns/` avec un maximum d'anti-patterns
**utilisables et de haute qualité** : détectables, sourcés, avec un correctif
et des limites. Périmètre : développement Go (le produit), plus les domaines
généraux que le kit couvre déjà (HTTP/API, base de données, architecture,
tests, sécurité, observabilité, CLI, messaging, configuration/cache).

## Méthode

Recherche web multi-angles (6 lots de 4 requêtes, 5-6 résultats par requête) sur
les sources fiables et primaires. Chaque anti-pattern retenu doit avoir une
source primaire vérifiable (doc officielle Go, OWASP, architecture centers
cloud, auteurs reconnus, référence académique) — jamais un seul blog anonyme.

## Sources par domaine et évaluation

### Go — autorité primaire (officielle ou reconnue)

| Source | Type | Fiabilité |
|---|---|---|
| go.dev/blog/pipelines (Concurrency patterns) | officiel | critique |
| go.dev/blog/context | officiel | critique |
| go.dev/blog/errors-are-values | officiel | critique |
| go.dev/blog/defer-panic-and-recover | officiel | critique |
| go.dev/wiki/PanicAndRecover | wiki officiel | haute |
| go.dev/wiki/CodeReviewComments | wiki officiel | haute |
| go.dev/wiki/CodeReviewConcurrency | wiki officiel | haute |
| go.dev/doc/database/execute-transactions | officiel | critique |
| pkg.go.dev/database/sql (+ issue #27434) | officiel | critique |
| pkg.go.dev/net/http + blog.cloudflare.com (timeouts) | officiel + Cloudflare | critique |
| go.dev/doc/modules/layout | officiel | critique |
| pkg.go.dev/encoding/json (v2) + blog.trailofbits.com | officiel + Trail of Bits | haute |
| 100go.co / teivah/100-go-mistakes (livre) | référence reconnue | haute |
| dave.cheney.net (going without, Practical Go) | auteur reconnu | haute |
| go-proverbs.github.io | Rob Pike | critique |

### Domaines généraux

| Domaine | Sources primaires | Fiabilité |
|---|---|---|
| Architecture | foote.pdf (Big Ball of Mud, PLoP'97), refactoring.guru, Wikipedia (listes) | haute |
| Microservices | softwarepatternslexicon, dzone antipatterns, algomaster | moyenne-haute (convergent) |
| SQL | sonra.io (34 SQL antipatterns), slicker.me | moyenne (convergent avec la littérature) |
| Tests | testsmells.org, xunitpatterns.com (Meszaros), refactoring.guru | haute |
| Sécurité | OWASP Top 10 2025 (A06, A10), OWASP cheatsheets, CWE-15 | critique |
| Observabilité | observability-antipatterns.github.io (CNCF-style guide) | haute |
| CLI | clig.dev (Command Line Interface Guidelines), jmmv.dev | haute |
| Messaging | Confluent, Conduktor, docs.axonops.com (Kafka) | haute (vendors spécialisés) |
| Résilience | microsoftdocs/architecture-center (retry storm), AWS prescriptive guidance | critique |
| Cache/config | redis.io, Wikipedia (cache stampede), AWS well-architected, minimumcd | haute |

## Critères de qualité appliqués

1. **Source primaire vérifiable** — chaque entrée cite au moins une URL primaire
   dans `relationships.references` (le validateur l'exige : URL ou id de graphe existant).
2. **Question distincte** — ne duplique pas un corps de règle ou recipe ; répond
   « comment détecter et éviter X » en complément des règles « fais X ».
3. **Actionnable** — champs `symptom`/`detect` (signaux concrets, y compris Go :
   pprof, runtime.NumGoroutine, vet, golangci-lint), `problem` (conséquences),
   `fix` (correctif concret), `when_ok` (limites — quand l'anti-pattern est
   acceptable). La nuance `when_ok` est ce qui rend l'entrée utilisable.
4. **Go-anchored** — exemples et correctifs en Go idiomatique ; les anti-patterns
   génériques sont traduits en signaux Go (ex. `omitempty`, `database/sql`, slog).
5. **Pas de redondance** — les leçons déjà en Gotchas.md du metaprojet ne sont
   pas dupliquées en corps ; le corps reste produit (KitV2), la mémoire reste
   metaprojet.

## Candidats retenus (47) par domaine

### go (14) — coeur du produit

goroutine-leak · context-unused · context-key-collision · ignored-error ·
error-string-matching · panic-as-error · loop-variable-capture ·
mutable-global-state · interface-everywhere · over-structuring ·
init-misuse · string-concat-loop · json-omitempty-zero · shadowing

### database (6)

n-plus-one · select-star · function-on-column · eav · raw-transactions ·
pool-misconfig

### http (4)

no-timeouts · rest-tunneling · rest-ignoring-http-semantics · api-no-pagination

### architecture (6)

big-ball-of-mud · god-object · bloater · distributed-monolith · nano-services ·
shared-database

### testing (4)

brittle-tests · implementation-details · over-mocking · sleep-based

### security (4)

hardcoded-credentials · fail-open · no-threat-modeling · error-information-leak

### observability (2)

logging-not-observability · excessive-logging

### cli (1)

flag-and-convention-abuse (fusion de « abusing flags » et « ignoring
conventions » de clig.dev — même source, même question)

### messaging (3)

poison-pill-no-dlq · offset-commit-misorder · retry-storm

### config-cache (3)

hardcoded-values · cache-stampede · cache-stale

## Exclusions (et raisons)

- **Anti-patterns purement managériaux** (analysis paralysis, design by
  committee…) : hors périmètre d'un kit de code.
- **Anti-patterns sans source fiable** (blogs uniques non vérifiables) :
  exclus même si populaires.
- **Recouvrements forts** : fusionnés (CLI flags/conventions) ou éliminés
  (cfg-secrets-in-code ≈ sec-hardcoded-credentials).
- **Spécifiques à d'autres langages** (Java EE patterns, .NET) : non traduits
  en Go, exclus.

## Prochaines étapes

Plan d'implémentation → création des fichiers YAML (contrat de métadonnées du
graphe : id/title/kind/version/status/owner/tags/go_version/dependencies/
last_verified + symptom/detect/problem/fix/when_ok/relationships) → gate
complète KitV2 → evidence.
