# Evidence — Anti-patterns KitV2 (2026-08-04)

## Requête

Remplir `KitV2/knowledge/anti-patterns/` avec un maximum d'anti-patterns
utilisables et de haute qualité : recherche web approfondie sur sources fiables,
puis rapport, plan, implémentation.

## Processus

1. Recherche web multi-angles (6 lots de 4 requêtes, 5-6 résultats/requête) sur
   12 domaines ; synthèse : `docs/research/2026-08-04-anti-patterns-research.md`.
2. Plan : `docs/plans/2026-08-04-anti-patterns.md` (47 entrées, format YAML,
   contrat de graphe).
3. Implémentation : 47 fichiers YAML sous `KitV2/knowledge/anti-patterns/`
   (go 14, database 6, http 4, architecture 6, testing 4, security 4,
   observability 2, cli 1, messaging 3, config-cache 3).

## Format par fichier

Contrat de graphe (id `pattern:antipattern:<slug>` unique, title, kind Pattern,
version, status active, owner go-agent-kit, tags, go_version, dependencies,
last_verified) + champs d'usage `symptom`/`detect`/`problem`/`fix`/`when_ok` +
`relationships.references` (sources primaires, URLs validées).

## Sources

Chaque fichier cite ≥ 1 source primaire vérifiée (go.dev, pkg.go.dev, OWASP,
blog.cloudflare.com, microsoftdocs/architecture-center, refactoring.guru,
xunitpatterns.com, testsmells.org, clig.dev, confluent.io, kafka.apache.org,
redis.io, dave.cheney.net, 100go.co, CWE, Twelve-Factor, IETF idempotency
draft, Microsoft API guidelines, martinfowler.com). URLs vérifiées HTTP 200
le 2026-08-04 (sauf dzone.com : 403 anti-bot, source légitime).

## Gate (2026-08-04, depuis KitV2/)

- `validate-instructions.py` : PASS
- `validate-kitv2.py` : PASS (45 product skills — les anti-patterns ne sont
  pas des SKILL.md, count inchangé)
- `gofmt -l .` : vide · `go vet ./...` : propre · `golangci-lint run ./...` :
  0 issues · `go test ./...` : 11 packages ok · `gosec ./...` : 0 issues
- `probes/run.sh` : cli-minimal, rest-chi, sqlite-sqlc, worker-shutdown,
  offline — 5 PASS
- Contraintes vérifiées en script : 47 ids uniques au format attendu, prose
  ≤ 80 caractères (hors URLs), YAML parse, relations references non vides.

## Revue fraîche-contexte (subagent read-only)

Verdict : **APPROVE-WITH-NITS** (0 BLOCKER). Exactitude technique Go 1.22+
PASS (3 nits), sources PASS (1 MAJOR : URL axonops morte), duplication PASS,
actionnabilité PASS (47/47 avec fix + when_ok), références croisées PASS,
conformité au plan PASS (47/47).

Correctifs appliqués (tous vérifiés) :

- MAJOR : `msg-offset-commit-misorder` — URL axonops morte remplacée par
  kafka.apache.org/documentation/#semantics (200).
- MINOR : refactoring.guru large-class corrigée ; xunitpatterns MockObject
  corrigée ; Sleepy%20Test (404) remplacée par martinfowler.com nonDeterminism ;
  gosec G104 retiré (supprimé de gosec) ; savepoints database/sql corrigés
  (hors API, SQL brut driver-dépendant) ; api-no-pagination : sources
  pagination/idempotence ajoutées (IETF idempotency-key draft, Microsoft API
  guidelines) ; synctest marqué expérimental (GOEXPERIMENT) ; `thelper` retiré
  (non lié au contexte) ; noms de recipes canoniques (recipe-sqlite-sqlc…) ;
  6 fichiers croisent `rules/core/` (errors, concurrency, philosophy).

## Statut

PASS. 47 anti-patterns livrés, gate complète verte, revue indépendante
intégrée.
