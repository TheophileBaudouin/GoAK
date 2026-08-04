# Evidence — Patterns KitV2 (2026-08-04)

## Requête

Remplir `KitV2/knowledge/patterns/` avec des patterns **positifs** de qualité
professionnelle et utilisables, via le même process complet que les
anti-patterns (recherche → rapport → plan → implémentation → gate → revue),
sans mélange avec les anti-patterns.

## Séparation patterns / anti-patterns

- Dossier distinct : `knowledge/patterns/` (anti-patterns : `knowledge/anti-patterns/`).
- Namespace d'ids distinct : `pattern:<domaine>:<slug>` (jamais
  `pattern:antipattern:*` — vérifié en script).
- Schéma distinct : problem/context/solution/benefits/costs/related
  (positif) vs symptom/detect/problem/fix/when_ok (négatif).
- Lien déclaré vers l'anti-pattern homologue via `relationships.references`
  (ids de graphe résolus par le validateur) — 33 homologues référencés.

## Processus

1. Recherche web orientée patterns (4 lots de 4 requêtes) ; synthèse :
   `docs/research/2026-08-04-patterns-research.md`.
2. Plan : `docs/plans/2026-08-04-patterns.md` (38 entrées, format, répartition).
3. Implémentation : 38 fichiers YAML sous `KitV2/knowledge/patterns/`
   (go 8, concurrency 3, resilience 3, http/api 4, database 4, architecture 2,
   testing 4, observability 2, cli 1, messaging 3, config-cache 2, security 2).

## Sources

50 URLs uniques vérifiées HTTP 200 le 2026-08-04 (go.dev, pkg.go.dev,
dave.cheney.net, go.dev/wiki, microservices.io, AWS prescriptive guidance,
blog.cloudflare.com, RFC 9457/8288, IETF idempotency-key, martinfowler.com,
xunitpatterns.com, clig.dev, redis.io, kafka.apache.org, confluent.io,
12factor.net, CWE/OWASP, golang.org/x/sync).

## Gate (2026-08-04, depuis KitV2/)

- `validate-instructions.py` : PASS · `validate-kitv2.py` : PASS (45 skills —
  les patterns ne sont pas des SKILL.md, count inchangé)
- `gofmt -l .` : vide · `go vet ./...` : propre · `golangci-lint run ./...` :
  0 issues · `go test ./...` : 11 packages ok · `gosec ./...` : 0 issues
- `probes/run.sh` : 5 PASS
- Contraintes scriptées : 38 ids uniques au format `pattern:<domaine>:<slug>`,
  aucun id anti-pattern, prose ≤ 80 (hors URLs), relations references non
  vides, tous les ids anti-pattern homologues résolus.

## Revue fraîche-contexte (subagent read-only)

Verdict initial : **REQUEST-CHANGES** — structure saine (séparation PASS,
exactitude Go 1.22+ PASS, duplication PASS, actionnabilité PASS, références
croisées PASS, conformité au plan 38/38) mais 2 URL mortes (MAJOR).

Correctifs appliqués et re-vérifiés :

- testing-seam-injection : martinfowler.com/articles/unitTestPractices.html
  (404) → martinfowler.com/bliki/UnitTest.html (200).
- architecture-modular-monolith : microservices.io/patterns/modular-monolith.html
  (404, absent du sitemap) → microservices.io/patterns/monolithic.html (200).
- security-secrets-management : « gitleaks — gate du kit » → « scan de
  secrets en CI (gitleaks) » (gitleaks n'est pas dans la gate documentée).
- messaging-transactional-outbox : homologue `msg-offset-commit-misorder`
  ajouté à relationships.references (conformité au plan).
- go-minimal-layout : « cmd/ uniquement pour plusieurs binaires » →
  « cmd/ pour les binaires du module » (aligné sur go.dev/doc/modules/layout).
- 50/50 URLs re-vérifiées 200 après correctifs.

## Incident (restauré)

Pendant le lot patterns, l'arborescence `KitV2/recipes/` (41 fichiers) a été
trouvée vidée dans le working tree (39 suppressions non commitées ; HEAD
intact). Restaurée via `git restore KitV2/recipes/` ; gate re-vérifiée verte
(45 skills). Cause exacte non identifiée (aucune commande rm sur recipes dans
la session) — voir Gotchas.md pour la règle préventive.

## Statut

PASS. 38 patterns livrés, gate complète verte, revue indépendante intégrée,
incident recipes restauré et documenté.
