---
name: testcontainers-go
description: "github.com/testcontainers/testcontainers-go v0.43.0 — programmatic container lifecycle for integration tests (PostgreSQL, Redis, Kafka, ...). Use when choosing a testing infrastructure for real-dependency integration tests. Requires Docker at test time; test-only dependency, never a runtime dependency."
category: library
tags: [testing, integration, containers, docker, testcontainers, test-infra]
last-verified: 2026-08-05
---

# testcontainers-go — dépendances réelles dans les tests

## Selection

[`github.com/testcontainers/testcontainers-go`](https://github.com/testcontainers/testcontainers-go)
(v0.43.0).

**Why it passes the gate** (actual reason, not stars): it is the standard way
to spin up real dependencies (DB, queue, cache) inside integration tests with
a clean lifecycle (start/terminate), CI-tested (scorecard CI-Tests 10/10,
SAST 10/10), zero advisories, and modular subpackages (postgres, redis, kafka,
…) that keep the dependency surface scoped.

## Admission checklist

- [x] Actively maintained — v0.43.0 (2026-06-19), releases fréquentes
- [x] Single responsibility — lifecycle de conteneurs pour les tests
- [x] Idiomatic Go — `ContainerRequest` + modules, no magic
- [x] Tests present + CI — CI 10/10, SAST 10/10 (scorecard 6.1)
- [x] Documentation — golang.testcontainers.org + godoc + quickstart
- [x] Real-world usage — massif (intégration, CI, smoke tests)
- [x] Readable end-to-end — large (~60 kLOC) mais par module/layer
- [x] Justified by need — le catalogue couvrait fakes/mocks mais pas les
      tests d'intégration réels ; NOT popularity

## Minimal use

```go
req := testcontainers.ContainerRequest{
    Image:        "redis:7-alpine",
    ExposedPorts: []string{"6379/tcp"},
}
c, _ := testcontainers.GenericContainer(ctx, testcontainers.GenericContainerRequest{
    ContainerRequest: req,
    Started:          true,
})
defer c.Terminate(ctx)
port, _ := c.MappedPort(ctx, "6379")
```

Compilé avec v0.43.0 le 2026-08-05. **Exécution : exige Docker** — sur une
machine sans Docker (cas présent), le scénario est `PARTIAL`, pas PASS.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `testingcontainers` maison (shell docker) | Réinvention du lifecycle (wait, logs, ports, cleanup) : anti-pattern, voir `pattern:testing:fakes-over-mocks` pour la frontière. |
| `ory/dockertest` | Alternative plus légère ; moins de modules, maintenance moins structurée ; testcontainers est le standard actuel. |
| Fakes/stubs uniquement | Suffisant pour les unit tests ; insuffisant pour valider les contrats réels (SQL dialect, wire protocol). Voir la frontière ci-dessous. |
| Base de données embarquée (modernc-sqlite) | Pas représentatif de PostgreSQL : différent de ce que testcontainers résout. |

## Security note

- **0 advisory** OSV (vérifié 2026-08-05).
- Images : épingler des tags précis (`redis:7-alpine`), jamais `latest` —
  reproductibilité + supply chain (images non signées par défaut).
- **Dépendance de test uniquement** : le module ne doit jamais entrer dans le
  graphe de production (`go.mod` test-only). Les probes du Kit ne doivent pas
  dépendre de Docker pour la gate (marquer PARTIAL si absent).
- Les conteneurs ont accès réseau local par défaut : configurer les réseaux
  et les ports exposés au minimum nécessaire.

## Utiliser cette librairie quand

- Les tests d'intégration doivent valider un contrat réel (dialecte SQL,
  protocole, comportement de cache/queue) non couvert par des fakes.
- CI disposant de Docker : lifecycle propre, wait strategies, logs
  diagnosticables.
- Reproduire des dépendances versionnées (bases, brokers) sans serveur
  partagé.

## Ne pas utiliser cette librairie quand

- Docker n'est pas disponible (CI restreinte, environnement embarqué) :
  préférer fakes ou services dédiés — jamais rendre la gate dépendante de
  Docker.
- Le test ne touche pas de dépendance externe (unit test pur) : fakes/mocks
  suffisent (voir `pattern:testing:fakes-over-mocks`).
- Le coût de démarrage (10-60 s par conteneur) dépasse le bénéfice pour des
  vérifications triviales.

## Avantages

- Lifecycle complet géré (pull, start, wait, ports, terminate) — zéro
  shell-script maison.
- Modules par dépendance (postgres, redis, kafka, mongo, …) : surface scoped.
- Wait strategies (port, log, HTTP) : robuste face aux démarrages lents.
- Standard de l'écosystème : CI 10/10, SAST 10/10, zéro advisory.

## Inconvénients

- **Exige Docker** à l'exécution : limite les environnements de test.
- Repo large (~60 kLOC) : le critère « lisible de bout en bout » est jugé par
  module ; les releases cassent parfois l'API (breaking changes fréquents).
- Coût de démarrage des conteneurs dans les tests (lenteur CI).
- Dépendance transitive non négligeable : restreinte aux tests.

## Pièges connus

- Épingler les images (jamais `latest`) et les versions de testcontainers
  (breaking changes aux frontières de release).
- Toujours `Terminate` (defer) : un conteneur orphelin fuit des ressources et
  fausse les tests suivants.
- `MappedPort` après `Started:true` ; pour des services lents, configurer une
  wait strategy explicite (port/log) — pas de `time.Sleep`.
- La gate du Kit ne doit pas dépendre de Docker : scénario `PARTIAL` documenté
  si Docker absent (ne jamais marquer PASS sans exécution).

## Sources vérifiées

- [testcontainers/testcontainers-go (repo officiel, v0.43.0)](https://github.com/testcontainers/testcontainers-go)
  — vérifié 2026-08-05
- [golang.testcontainers.org (documentation officielle)](https://golang.testcontainers.org/)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/testcontainers/testcontainers-go](https://pkg.go.dev/github.com/testcontainers/testcontainers-go)
  — vérifié 2026-08-05
- OSV : aucun advisory pour `github.com/testcontainers/testcontainers-go`
  (requête API 2026-08-05)
- Artefacts internes : `pattern:testing:fakes-over-mocks`,
  `pattern:testing:httptest`, `pattern:testing:table-driven`
