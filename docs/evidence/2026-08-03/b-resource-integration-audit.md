# Audit d'intégration des ressources Niveau B et audit global du registre

Date: 2026-08-03
Référence: `.agent/sources/Go-dev-kit-sources-et-references.md`
Plan: `docs/plans/2026-08-03-b-resource-integration-audit.md`

## Ressources Niveau B (selon projet) — 6/6 intégrées

Chaque ressource a été vérifiée une seule à la fois; les listes de niveaux du
registre n'ont pas été modifiées.

| Ressource | État initial | Intégration |
| --- | --- | --- |
| GORM | Absente (mention de rejet dans `catalogs/libraries/sqlc/SKILL.md` uniquement) | `knowledge/catalogs/libraries/gorm.yaml` (Source conditionnelle) |
| Fiber | Absente | `knowledge/catalogs/libraries/fiber.yaml` |
| Kafka (franz-go) | Absente (mot « kafka » comme exemple de module dans `knowledge/architecture/bootstrap-cli-runtime.yaml`) | `knowledge/catalogs/libraries/franz-go-kafka.yaml` |
| RabbitMQ (amqp091-go) | Absente | `knowledge/catalogs/libraries/amqp091-go.yaml` |
| Resty | Absente | `knowledge/catalogs/libraries/resty.yaml` |
| Cookiecutter | Absente | `knowledge/catalogs/cookiecutter.yaml` (ID `source:scaffolding:cookiecutter`, hors `libraries/` car outil non-Go) |

Justification du motif: les 6 ressources sont « selon projet » et aucune n'est
un défaut du kit (net/http + chi, sqlc/database-sql, slog, stdlib). L'entrée
Source conditionnelle est l'intégration minimale conforme déjà utilisée par
l'audit Niveau S/A (zap, redis, nats, air, go-blueprint, openai-go) : critères
de sélection, limites honnêtes, URL de source primaire vérifiée par requête
bornée le 2026-08-03 (toutes vivantes, aucune archivée), zéro dépendance
ajoutée, zéro recette non validée.

## Audit global — matrice de couverture (59/59)

56 entrées du corps du document couvertes par un ID graph Source ou un catalog
SKILL.md + 3 entrées couvertes par une règle de validation.

### Niveau S (7/7)

pkg.go.dev → `stdlib/pkg-doc-offline.yaml` · Effective Go → `stdlib/effective-go-offline.yaml` ·
Go Language Specification → `stdlib/go-language-specification.yaml` · Go Modules → `stdlib/go-modules.yaml` ·
Go Toolchains → `stdlib/go-toolchains.yaml` · go command → `stdlib/go-command.yaml` ·
Go Security Best Practices → `security/go-security-best-practices.yaml`

### Niveau A (27/27)

Go Toolchain → `stdlib/toolchain-offline.yaml` · Go Fuzzing → `stdlib/go-fuzzing.yaml` ·
Go Race Detector → `stdlib/go-race-detector.yaml` · Go Profiling → `performance/go-profiling.yaml` ·
Go Vulnerability Database → `security/go-vulnerability-database.yaml` · context → `stdlib/go-context.yaml` ·
errors → `stdlib/go-errors.yaml` · sync et sync/atomic → `stdlib/go-sync.yaml` ·
net/http → `stdlib/go-net-http.yaml` · database/sql → `stdlib/go-database-sql.yaml` ·
slog → `stdlib/go-slog.yaml` · OpenTelemetry → `observability/otel-go.yaml` ·
sqlc → `catalogs/libraries/sqlc/SKILL.md` · chi → `catalogs/libraries/chi/SKILL.md` ·
Cobra → `catalogs/libraries/cobra/SKILL.md` · Koanf → `catalogs/libraries/koanf/SKILL.md` ·
Zap → `catalogs/libraries/zap.yaml` · Validator → `catalogs/libraries/validator/SKILL.md` ·
Redis → `catalogs/libraries/redis.yaml` · NATS → `catalogs/libraries/nats.yaml` ·
Testify → `catalogs/libraries/testify/SKILL.md` · Air → `catalogs/libraries/air.yaml` ·
go-blueprint → `catalogs/libraries/go-blueprint.yaml` · Go by Example → `catalogs/go-by-example.yaml` ·
Awesome Go → `catalogs/awesome-go.yaml` · OpenAI Go SDK → `catalogs/libraries/openai-go.yaml`

### Niveau B (6/6 — cette session)

Voir tableau ci-dessus.

### Entrées non classées dans les listes de niveaux (19/19)

Déjà couvertes par une règle: govulncheck, gosec, golangci-lint →
`rules/core/validation/{govulncheck,gosec,golangci-lint}/`.
Déjà couverte: Viper → `catalogs/libraries/viper/SKILL.md` + `recipes/recipe-config-viper/`.
Ajoutées comme Source conditionnelle ou référence officielle: Go Release Policy
→ `stdlib/go-release-policy.yaml`; Zerolog → `catalogs/libraries/zerolog.yaml`;
Google UUID → `catalogs/libraries/google-uuid.yaml`; Gin → `catalogs/libraries/gin.yaml`;
Echo → `catalogs/libraries/echo.yaml`; sqlx → `catalogs/libraries/sqlx.yaml`;
golang-migrate → `catalogs/libraries/golang-migrate.yaml`; GoMock →
`catalogs/libraries/uber-go-mock.yaml`; Prometheus Client Go →
`catalogs/libraries/prometheus-client.yaml`; Mockery → `catalogs/libraries/mockery.yaml`;
JWT Go → `catalogs/libraries/golang-jwt.yaml`; Ollama API Go →
`catalogs/libraries/ollama-go.yaml`; Go Cookbook → `catalogs/go-cookbook.yaml`;
GitHub Code Search → `catalogs/github-code-search.yaml`; Sourcegraph →
`catalogs/sourcegraph.yaml`.

## Observations d'audit (incohérences identifiées, aucune correction nécessaire)

1. **Sens inverse kit > registre** : le kit possède des catalogues validés qui
   n'ont pas de libellé dans le registre (req extract-only, templ,
   modernc-sqlite, prompts/recipes internes). Ce n'est pas un défaut : le
   registre est une source de classement, pas un plafond; l'admission gate du
   kit reste l'autorité. Documenté, aucun changement.
2. **Viper dans le corps mais absent des listes S/A/B** : déjà intégré
   (catalog + recette, point source 3 du registre traité le 2026-08-03).
3. **go-redis / NATS / Zap / etc. intégrés comme références conditionnelles**
   sans dépendance — cohérent avec la politique stdlib-first.
4. **`capabilities.yaml` (`knowledge_catalogs: 13`)** : compte les catalogues
   SKILL.md (10 libraries + 3 reference-projects); les entrées Source YAML ne
   sont pas comptées dans ce nombre. Cohérent avec sa signification d'origine;
   non modifié.
5. **Zéro doublon d'ID graph** : 49 IDs `source:*` uniques vérifiés par
   `uniq -d`.

## Cohérence croisée

- `gorm.yaml` référence explicitement le rejet ORM du catalog sqlc (pas de
  contradiction).
- `resty.yaml` documente sa relation avec le catalog `req` extract-only.
- `sqlx.yaml` s'aligne sur le fallback requêtes dynamiques du catalog sqlc.
- `franz-go.yaml` et `amqp091-go.yaml` marquent explicitement l'exigence broker
  et l'absence de recette/recette non validée.
- Aucun artefact ajouté ne dépend d'un chemin metaprojet (validé par
  `validate-kitv2.py`), aucun `.go` ajouté, aucune dépendance go.mod ajoutée.

## Validation exécutée

```text
python3 .agent/validators/validate-instructions.py: PASS
python3 tools/validators/validate-kitv2.py: PASS (33 product skills, standalone, offline bundle)
grep IDs dupliqués: PASS (0 doublon, 49 ids source)
go mod verify: non requis (aucune dépendance modifiée)
go vet ./...: PASS
gofmt output gate: PASS
golangci-lint run ./...: PASS (0 issues)
go test -race ./...: PASS
gosec ./...: PASS (0 issues)
govulncheck ./...: PASS (0 called vulnerabilities)
bash probes/run.sh: PASS (5 probes)
Matrice de couverture automatisée: 59/59 entrées couvertes
git status registre: inchangé (les listes de niveaux n'ont pas été touchées)
```

## Limites

- Aucune des 21 entrées ajoutées n'est une recette exécutable : ce sont des
  références Source conditionnelles. Leur « exploitabilité » est la sélection
  - les limites + la source vérifiée, conformément au motif S/A. Les recettes
  (ex. Kafka, RabbitMQ, GORM) restent des extensions futures soumises à
  l'admission gate.
- Pas de review indépendante par sous-agent frais dans cette passe (audit
  séquentiel mono-agent); les faits (URL, pushed_at, IDs, gate) sont tous
  vérifiés par commande, pas par intuition.
