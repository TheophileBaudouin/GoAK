# Plan — Anti-patterns KitV2 (2026-08-04)

## Goal

Remplir `KitV2/knowledge/anti-patterns/` avec 47 anti-patterns de haute
qualité : détectables, sourcés, correctifs concrets, limites explicites.
Rapport de recherche : `docs/research/2026-08-04-anti-patterns-research.md`.

## Format (contrat de graphe + champs d'usage)

Un fichier YAML par anti-pattern, dans `KitV2/knowledge/anti-patterns/`
(flat ; le dossier est navigation, le graphe est l'autorité) :

```yaml
id: pattern:antipattern:<domaine>-<slug>   # GRAPH_ID_RE : pattern:antipattern:<slug>
title: <Nom — verbe d'état>
kind: Pattern
version: 1
status: active
owner: go-agent-kit
tags: [go, <domaine>]
go_version: "1.22+"
dependencies: []
last_verified: 2026-08-04
symptom: >-      # ce qu'on voit dans le code
detect: >-       # signaux concrets (pprof, vet, golangci-lint, revue…)
problem: >-      # pourquoi c'est mauvais, conséquences
fix: >-          # correctif idiomatique
when_ok: >-      # limites / quand c'est acceptable
relationships:
  references: [<URL primaire>, ...]   # exigé par le validateur (URL ou id)
  uses: []
  validated_by: []
```

Contraintes validateur vérifiées : `kind` ∈ GRAPH_KINDS (Pattern), `status` ∈
{proposed, active, …} (active), id au format `pattern:antipattern:<slug>`,
`relationships.references` = liste d'URLs http(s) ou d'ids de graphe existants
(le validateur rejette les ids non résolus et les relations inconnues), aucune
dépendance à des chemins metaprojet (`.agent/`, `../`).

## Répartition (47)

| Domaine | Fichiers | Source primaire principale |
|---|---|---|
| go (14) | goroutine-leak, context-unused, context-key-collision, ignored-error, error-string-matching, panic-as-error, loop-variable-capture, mutable-global-state, interface-everywhere, over-structuring, init-misuse, string-concat-loop, json-omitempty-zero, shadowing | go.dev, pkg.go.dev, 100go.co, dave.cheney.net |
| database (6) | n-plus-one, select-star, function-on-column, eav, raw-transactions, pool-misconfig | sonra.io, go.dev/doc/database, pkg.go.dev/database/sql |
| http (4) | no-timeouts, rest-tunneling, rest-ignoring-http-semantics, api-no-pagination | blog.cloudflare.com, infoq.com, innoq.com |
| architecture (6) | big-ball-of-mud, god-object, bloater, distributed-monolith, nano-services, shared-database | foote.pdf, refactoring.guru, softwarepatternslexicon, dzone |
| testing (4) | brittle-tests, implementation-details, over-mocking, sleep-based | xunitpatterns.com, testsmells.org |
| security (4) | hardcoded-credentials, fail-open, no-threat-modeling, error-information-leak | owasp.org |
| observability (2) | logging-not-observability, excessive-logging | observability-antipatterns.github.io |
| cli (1) | flag-and-convention-abuse | clig.dev |
| messaging (3) | poison-pill-no-dlq, offset-commit-misorder, retry-storm | confluent.io, axonops, microsoftdocs |
| config-cache (3) | hardcoded-values, cache-stampede, cache-stale | CWE-15, AWS well-architected, redis.io, Wikipedia |

## Ordre d'implémentation

1. Lot go (14) — valeur maximale, sources officielles.
2. database + http (10).
3. architecture + testing (10).
4. security + observability (6).
5. cli + messaging + config-cache (7).

## Validation (Definition of Done)

- `python3 ../.agent/validators/validate-instructions.py` → PASS
- `python3 tools/validators/validate-kitv2.py` → PASS (aucun changement de
  count attendu : les anti-patterns ne sont pas des SKILL.md)
- Gate mécanique complète (gofmt, vet, lint, tests, gosec, govulncheck, probes)
- Aucune relation non résolue, aucun id invalide, aucun chemin metaprojet
- Evidence dans `docs/evidence/2026-08-04/anti-patterns/` avec la sortie brute
- Revue fraîche-contexte (subagent read-only) avant déclaration de fin
- Mémoire Progress/Gotchas à jour

## Risques

- **Qualité vs volume** : 47 fichiers ; chaque fichier reste ≤ 60 lignes,
  concentré sur symptom/detect/problem/fix/when_ok. Tout fichier qui ne passe
  pas la revue qualité est retiré ou fusionné — jamais ajouté « pour le compte ».
- **Sources** : les anti-patterns génériques reposent sur des sources
  convergentes (multi-sources citées) ; les sources uniques faibles sont
  marquées `when_ok` prudentes ou exclues.
