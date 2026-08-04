# Rapport d'intégration — 9 bibliothèques approuvées (2026-08-05)

- **Plan :** `docs/plans/2026-08-05-library-integration.md`
- **Survey source :** `docs/research/2026-08-05-go-library-survey.md`
- **Pipeline :** Z2 §9 (une bibliothèque à la fois), A1, N1 §4, C2, Z11.
- **Évidence brute :** `docs/evidence/2026-08-05/library-integration/gate.log`

## 1. Fichiers créés (14)

### Fiches catalogues (9) — `KitV2/knowledge/catalogs/libraries/<id>/SKILL.md`

| id | Module (version vérifiée) | Compile minimal use | Advisory / pin |
| --- | --- | --- | --- |
| age | filippo.io/age v1.3.1 | roundtrip OK | GHSA-32gq-x56h-299c · ≥ 1.2.1 |
| bbolt | go.etcd.io/bbolt v1.5.0 | roundtrip OK | 0 advisory |
| compress | klauspost/compress v1.19.1 | zstd+s2 OK | GO-2026-5841 · ≥ 1.18.7 |
| goldmark | yuin/goldmark v1.8.5 | convert OK | GO-2026-5320 · ≥ 1.7.17 |
| pgx | jackc/pgx/v5 v5.10.0 | build OK | 4 advisories · ≥ 5.9.2 |
| kin-openapi | getkin/kin-openapi v0.146.0 | validate OK | 4 advisories · ≥ 0.144.0 |
| minio-go | minio/minio-go/v7 v7.2.1 | build OK | 0 advisory |
| testcontainers-go | testcontainers v0.43.0 | build OK (Docker absent → PARTIAL) | 0 advisory |
| certmagic | caddyserver/certmagic v0.25.4 | build OK | 0 advisory |

Chaque fiche : frontmatter immuable · Selection (raison réelle) · Admission
checklist (9 critères) · Minimal use (compilé hors kit, /tmp) · Alternatives
with verdicts · Security note (pin + advisory) · 6 sections N1 §4 (Utiliser /
Ne pas utiliser quand, Avantages, Inconvénients, Pièges connus, Sources
vérifiées).

### Artefacts YAML du graphe (5 — manques réels après audit de couverture)

| Fichier | id | Question distincte |
| --- | --- | --- |
| security/file-encryption.yaml | source:security:file-encryption | chiffrement fichiers au repos (age) vs secrets-management |
| architecture/embedded-kv.yaml | source:architecture:embedded-kv | KV embarqué (bbolt) vs SQL embarqué vs serveur |
| performance/compression-selection.yaml | source:performance:compression-selection | zstd vs s2 vs stdlib gzip (mesuré) |
| anti-patterns/sec-unsanitized-rendering.yaml | pattern:antipattern:sec-unsanitized-rendering | XSS par rendu markdown/template non sanitisé |
| anti-patterns/db-placeholder-cache-injection.yaml | pattern:antipattern:db-placeholder-cache-injection | SQLi modes de requête pgx + littéraux dollar-quoted |

kin-openapi, minio-go, testcontainers-go, certmagic : **0 artefact YAML**
(questions déjà couvertes : sec-fail-open, sec-hardcoded-credentials,
fakes-over-mocks, go-mutable-global-state — les pièges vivent dans les fiches).

## 2. Fichiers modifiés (5)

- `KitV2/tools/validators/validate-kitv2.py` — EXPECTED_PRODUCT_SKILLS 51 → 60
  (constante de gate, suit l'arborescence ; dette C2 §5 « à dériver » inchangée).
- `KitV2/capabilities.yaml` — product_skills 45 → 60 (corrige dérive 45 vs 51) ;
  knowledge_catalogs 31 → 40.
- `KitV2/router/index.json` + `meta.json` — régénérés (232 → 246 ressources).
- `KitV2/go.mod` + `go.sum` — bump transitif `golang.org/x/text` v0.28.0 →
  v0.40.0 (fix GO-2026-5970 signalé par govulncheck ; aucun nouveau module).

## 3. Gate complète (sorties brutes dans gate.log)

| Check | Résultat |
| --- | --- |
| validate-kitv2.py | PASS (60 product skills, router 246) |
| validate-instructions.py | PASS |
| gofmt -l | vide |
| go vet | OK |
| golangci-lint | 0 issues |
| go test -race | 11 packages ok |
| gosec | 0 issues |
| govulncheck | No vulnerabilities found |
| probes (5) | cli-minimal, rest-chi, sqlite-sqlc, worker-shutdown, offline — PASS |
| router --check | up to date |

## 4. Décisions et points honnêtes

- **testcontainers-go** : exécution du minimal use `PARTIAL` (Docker absent de
  la machine) — jamais PASS sans exécution (A1). Compile vérifié.
- **certmagic** : approuvé avec WARNING G7 (10 deps, scorecard 4.5) — documenté
  dans la fiche, coût de maintenance à suivre.
- **Aucune dépendance ajoutée au module kit** : fiches + artefacts uniquement ;
  les snippets minimal use sont compilés dans des modules /tmp hors kit.
- **0 artefact padding** : 5 YAML pour 9 bibliothèques, chaque question
  distincte vérifiée par audit de couverture (grep ids existants).

## 5. Revue fresh-context

Sous-agent réviseur indépendant (context: fresh) — verdict **APPROVE-WITH-NITS**
(0 BLOCKER, 0 MAJOR). Vérifications confirmées : frontmatter 9/9, sections
A1/N1 §4 9/9, schéma YAML 5/5, relations résolues (18 ids existants), pins
sécurité croisés OSV/GitHub exacts, gate re-exécutée, zéro duplication, zéro
référence metaprojet.

**Nits corrigés (2026-08-05, après revue)** :

1. goldmark : URL GHSA 404 → `https://osv.dev/vulnerability/GO-2026-5320`
   (fiche + YAML).
2. pgx YAML : URL GHSA-9jj7-4m8r-rfcm 404 → OSV GO-2026-4772.
3. pgx fiche : compte 4 → **5 advisories distincts** (ajout GO-2024-2567, fix
   v5.5.2) ; CVE-2024-27304 fix v5.5.5 → **v5.5.4** (advisory officiel).
4. pgx fiche : « 3 CVEs placeholder » → « 2 SQLi + 2 memory-safety ».
5. compress fiche : libellé s2 « OOB read » → « integer overflow + écriture
   hors bornes » (GHSA officiel).
6. age fiche : admission checklist réordonnée chronologiquement.

Nit #7 (fiches préexistantes sans Security note) : hors périmètre, harmonisation
à prévoir en passe ultérieure — enregistré comme piste d'amélioration.

## 6. Restants (hors périmètre)

- Intégration des bibliothèques « à surveiller » (otel, miekg/dns, oapi-codegen,
  goccy/yaml, joshuafuller/sse) — condition d'admission dans le survey.
- Promotion des 22 YAML legacy (kind Source) vers fiches SKILL.md — préalable
  séparé.
- Dérivation de EXPECTED_PRODUCT_SKILLS (dette C2 §5).
