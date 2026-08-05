# Evidence — recipes prioritaires (2026-08-05)

Cette fiche enregistre seulement les résultats effectivement exécutés. Les
scénarios non exécutés restent `BLOCKED`, jamais `PASS`.

| Vérification | État initial |
| --- | --- |
| Admission golang-migrate v4.19.1 | PASS — sources dépôt, release, pkg.go.dev et migrations vérifiées le 2026-08-05 ; fiche et décision écrite. |
| Tests unitaires et `-race` | PASS — `go test -race ./...` le 2026-08-05. |
| Probes session/JWT/observabilité/OpenAPI | PASS — quatre nouvelles probes et les neuf probes totales ont affiché `PASS`. |
| Scénario PostgreSQL réel avec `DATABASE_URL` | BLOCKED — variable absente ; aucune base non jetable n'a été utilisée. |
| Validateurs, format, vet, lint, sécurité et routeur | PASS — validateurs instruction/cognitif/strict, `go mod tidy/verify`, gofmt, vet, golangci-lint, gosec, govulncheck et router check le 2026-08-05. |
| Revue fresh-context | BLOCKED — l'agent lecture seule a atteint une limite de service avant toute lecture ou écriture. |

La dernière revue locale en lecture seule a vérifié les chemins supprimés,
le diff sans whitespace (`git diff --check`), les compteurs dérivés et les
limites de contrat OpenAPI. Elle ne remplace pas la revue fresh-context exigée.
