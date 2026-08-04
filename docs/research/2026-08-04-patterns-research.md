# Rapport de recherche — Patterns positifs pour le Go Agent Kit (2026-08-04)

## Objectif

Remplir `KitV2/knowledge/patterns/` avec des patterns **positifs** de qualité
professionnelle et utilisables : solutions récurrentes avec problème/contexte/
solution/forces, sourcées, et liées aux rules/recipes/anti-patterns existants.

## Séparation stricte patterns / anti-patterns

| Dimension | Anti-patterns (livrés) | Patterns (ce lot) |
|---|---|---|
| Dossier | `knowledge/anti-patterns/` | `knowledge/patterns/` |
| Namespace d'ids | `pattern:antipattern:<slug>` | `pattern:<domaine>:<slug>` (go, database, http, architecture…) |
| Schéma | symptom/detect/problem/fix/when_ok (négatif : ce qu'on voit, ce qui casse) | problem/context/solution/benefits/costs (positif : ce qu'on fait, pourquoi, limites) |
| Corps | détection et correctifs | forme de la solution et forces |
| Lien croisé | références entre anti-patterns | `related` → rules/recipes + anti-pattern homologue dans `relationships.references` |

Aucun corps d'anti-pattern dans les patterns : la paire est liée par référence
de graphe (`pattern:antipattern:<slug>` existe et est résolu par le validateur),
jamais fusionnée.

## Méthode

4 lots de 4 requêtes web orientées patterns (concurrency Go, erreurs, contexte,
DI, microservices/resilience, REST, testing, architecture, cache, outbox,
observability, CLI, config) sur sources primaires ou autorités reconnues.

## Sources par domaine (évaluation)

| Domaine | Sources primaires | Fiabilité |
|---|---|---|
| Go concurrency | go.dev/blog/pipelines, pkg.go.dev/golang.org/x/sync/errgroup | critique |
| Go errors | dave.cheney.net (don't just check errors), go.dev/wiki/ErrorValueFAQ, pkg.go.dev/errors | critique |
| Go context | go.dev/blog/context, pkg.go.dev/context | critique |
| DI | gofaq.org (constructor injection), pratique documentée | haute |
| Résilience | microservices.io/patterns, AWS prescriptive guidance (retry-backoff, circuit-breaker) | critique |
| REST/API | IETF idempotency-key draft, RFC 9457 (Problem Details), Microsoft API guidelines, microservices.io | critique |
| Testing | go.dev/wiki/TableDrivenTests, pkg.go.dev/net/http/httptest, xunitpatterns (Test Double taxonomy) | critique |
| Architecture | go.dev/doc/modules/layout (internal/), microservices.io, hexagonal (ports-adapters) | haute |
| Cache | redis.io, golang.org/x/sync/singleflight, AWS (stale-while-revalidate) | critique |
| Messaging | microservices.io (transactional-outbox), AWS transactional-outbox, Confluent | critique |
| Observabilité | go.dev/blog/slog, pkg.go.dev/log/slog, microsoft engineering playbook (correlation-id) | critique |
| CLI | clig.dev, gcloud command conventions | haute |
| Config | 12factor.net/config, CWE-15 | critique |
| Sécurité | OWASP, 12factor, CWE | critique |

## Critères de qualité

1. **Source primaire** dans `relationships.references` (URL vérifiée) + id de
   graphe de l'anti-pattern homologue quand il existe (résolu par le validateur).
2. **Question distincte** — les patterns décrivent la FORME de la solution
   (problem/context/solution/forces) ; les rules donnent les règles
   opérationnelles, les recipes le code exécutable. `related` croise les trois
   sans dupliquer de corps.
3. **Actionnable** — `solution` concrète (API, shape, bibliothèque du kit),
   `benefits` (pourquoi), `costs` (limites/trade-offs — la nuance qui rend le
   pattern utilisable).
4. **Go-anchored** — exemples et vocabulaire idiomatiques (slog, errgroup,
   internal/, httptest, singleflight…), en phase avec go 1.22+.
5. **Pas de recouvrement** — un pattern par question ; les patterns triviaux
   couverts par une règle seule ne sont pas ajoutés.

## Candidats retenus (38) par domaine

### go (8)

error-wrapping-chain · sentinel-errors · contextual-worker ·
private-context-keys · concrete-returns · constructor-injection ·
minimal-layout · string-builder

### concurrency (3)

worker-pool · pipeline · singleflight

### resilience (3)

timeout-deadlines · retry-backoff-jitter · circuit-breaker

### http/api (4)

middleware-chain · rest-resource-modeling · rest-cursor-pagination ·
api-idempotency-keys

### database (4)

query-batching · transaction-boundary · pool-config · versioned-migrations

### architecture (2)

modular-monolith · ports-adapters

### testing (4)

table-driven · seam-injection · fakes-over-mocks · httptest

### observability (2)

structured-logging · correlation-ids

### cli (1)

subcommands-conventions

### messaging (3)

dead-letter-queue · transactional-outbox · idempotent-consumer

### config-cache (2)

twelve-factor-config · stale-while-revalidate

### security (2)

secrets-management · fail-closed-auth

## Exclusions

- Patterns purement organisationnels (saga orchestré complexe, CQRS complet) :
  hors portée des besoins du kit ou recouvrant recipes existantes ; mentionnés
  en `related` quand pertinents (ex. outbox ↔ saga dans le contexte).
- Patterns déjà entièrement incarnés par une règle sans forme propre (ex.
  « utiliser les interfaces ») — la règle `rules/core/` est l'autorité.
- Spécifiques à d'autres écosystèmes.

## Prochaines étapes

Plan → création des 38 fichiers YAML (contrat de graphe + problem/context/
solution/benefits/costs/related/references) → gate complète → revue
fraîche-contexte → evidence.
