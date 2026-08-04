# Plan — Intégration des 9 bibliothèques approuvées (survey 2026-08-05)

- **Date :** 2026-08-05
- **Décision source :** survey `docs/research/2026-08-05-go-library-survey.md` (8 approuvées + 1 avec WARNING).
- **Pipeline :** Z2 §9 (une bibliothèque à la fois), A1 (format SKILL.md), N1 §4 (fiche 6 sections), C2 (gate), Z11 (router).
- **Statut :** exécution après approbation utilisateur (2026-08-05).

## Ordre d'exécution (dette croissante)

age → bbolt → compress → goldmark → pgx → kin-openapi → minio-go → testcontainers-go → certmagic.

## Fichiers à créer

### Fiches catalogues (`KitV2/knowledge/catalogs/libraries/<id>/SKILL.md`)

| id | Module | Version pin | Notes sécurité (fiche) |
| --- | --- | --- | --- |
| age | filippo.io/age | ≥ v1.2.1 (advisory plugin), cible v1.3.1 | GHSA-32gq-x56h-299c |
| bbolt | go.etcd.io/bbolt | v1.5.0 | 0 advisory |
| compress | github.com/klauspost/compress | ≥ 1.18.7 (s2 OOB), cible 1.19.1 | GO-2026-5841 |
| goldmark | github.com/yuin/goldmark | ≥ 1.7.17 (XSS), cible 1.8.5 | GO-2026-5320 |
| pgx | github.com/jackc/pgx/v5 | ≥ 5.9.2 (SQLi placeholder), cible 5.10.0 | GO-2026-5004 + 3 autres |
| kin-openapi | github.com/getkin/kin-openapi | ≥ 0.144.0 (fail-open/nil-ptr), cible 0.146.0 | 4 advisories |
| minio-go | github.com/minio/minio-go/v7 | v7.2.1 | 0 advisory |
| testcontainers-go | github.com/testcontainers/testcontainers-go | v0.43.0 | 0 advisory ; Docker requis (tests only) |
| certmagic | github.com/caddyserver/certmagic | v0.25.4 | 0 advisory ; éviter `certmagic.Default` |

Chaque fiche : frontmatter immuable + Selection (raison réelle, pas les étoiles) +
Admission checklist (9 critères) + Minimal use (compilé en /tmp, hors kit) +
Alternatives considered + Security note + 6 sections N1 §4 (Utiliser / Ne pas
utiliser quand, Avantages, Inconvénients, Pièges connus, Sources vérifiées).

### Artefacts YAML du graphe (manques réels seulement, après audit de couverture)

| Fichier | id | Question distincte | Domaine |
| --- | --- | --- | --- |
| `security/file-encryption.yaml` | `source:security:file-encryption` | Chiffrement de fichiers au repos (age) vs secrets-management (config) | security |
| `architecture/embedded-kv.yaml` | `source:architecture:embedded-kv` | KV embarqué (bbolt) vs SQL embarqué (modernc-sqlite) vs serveur | architecture |
| `performance/compression-selection.yaml` | `source:performance:compression-selection` | Choix algorithme de compression (zstd/gzip/s2) selon ratio/latence | performance |
| `anti-patterns/sec-unsanitized-rendering.yaml` | `pattern:antipattern:sec-unsanitized-rendering` | Rendu HTML non sanitisé (markdown/templates) → XSS (goldmark GO-2026-5320) | anti-patterns |
| `anti-patterns/db-placeholder-cache-injection.yaml` | `pattern:antipattern:db-placeholder-cache-injection` | Injection via modes de cache de statements + littéraux dollar-quoted (pgx GO-2026-5004) | anti-patterns |

kin-openapi, minio-go, testcontainers-go, certmagic : **0 artefact YAML** —
couverture existante suffisante (sec-fail-open, go-mutable-global-state,
fakes-over-mocks, database:pool-config) ; les pièges vivent dans les fiches.

## Fichiers à modifier

1. `KitV2/tools/validators/validate-kitv2.py` — `EXPECTED_PRODUCT_SKILLS` 51 → 60
   (constante de la gate, doit suivre l'arborescence ; dette C2 §5 « à dériver »
   inchangée).
2. `KitV2/capabilities.yaml` — `product_skills: 45 → 60` (corrige la dérive
   existante 45 vs 51) ; `knowledge_catalogs: 31 → 40`.
3. Router régénéré : `python3 .agent/router/build_index.py` (racine) puis
   `--check` (Z11 §4). `knowledge/INDEX.md` : aucun nouveau domaine → inchangé.

## Validation

- Gate complète depuis `KitV2/` (C2 §4) : validate-kitv2.py, go mod tidy/verify,
  gofmt, vet, golangci-lint, go test -race, gosec, govulncheck, probes.
- Minimal use compilé : chaque snippet fiche compilé dans un module /tmp avec la
  dépendance (évidence de compilation, hors kit).
- Évidence brute : `docs/evidence/2026-08-05/library-integration/` (sorties gate).
- Revue fresh-context avant complétude.

## Hors périmètre

- Aucune dépendance ajoutée au module kit (fiches uniquement ; snippets illustratifs).
- Aucune admission des bibliothèques « à surveiller » (otel, miekg/dns, …).
