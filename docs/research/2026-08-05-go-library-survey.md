# Étude bibliothèques Go candidates — KitV2

- **Date :** 2026-08-05
- **Périmètre :** recherche multi-domain, validation contre les gates du Kit, rapport actionnable.
- **Nature :** recherche + recommandation. **Aucune modification du produit KitV2** (admission = décision soumise à approbation, charte §boundaries).
- **Données :** GitHub API, proxy.golang.org, OSV (advisories), OpenSSF Scorecard, recherche web. Toutes les données sont datées au 2026-08-05 ; les métriques de maintenance sont sujettes à évolution.

---

# 1. Résumé exécutif

| Mesure | Valeur |
| --- | --- |
| Bibliothèques identifiées en phase découverte | 31 |
| Analysées en profondeur (données dures) | 18 |
| **Approuvées pour intégration immédiate** | **8** |
| Approuvées avec WARNING (réserves documentées) | 1 |
| Refusées (gate échouée, raison précise) | 7 |
| À surveiller (future intégration) | 6 |
| Pointeurs stdlib recommandés (hors catalogue librairies) | 3 (x/crypto, x/time, x/sync) |

## Tendances observées

1. **Le critère « maintenu » élimine massivement.** Sur 6 bibliothèques évaluées pour la sérialisation/réseau léger, 4 sont mortes ou moribondes (msgpack, r3labs/sse, yaml.v3 upstream, xxhash en dormance). L'écosystème Go « émergent » 2025-2026 est un champ de jeunes projets < 12 mois sans track record — aucun ne passe la gate d'admission.
2. **La sécurité devient un différentiateur décisif.** 8 des 18 candidats ont un historique d'advisories ; tous sont corrigés dans les versions courantes, mais le *pattern* compte : pgx (3 SQLi classe placeholder en 2 ans), kin-openapi (fail-open auth), OTel (2 CVEs baggage). Le Kit doit coder le **pin minimal** (≥ version de correctif) et les **pièges** dans chaque fiche.
3. **Les gaps réels du catalogue sont : performance (compression), crypto d'application (age), stockage embarqué (bbolt), driver PostgreSQL (pgx), client S3 (minio-go), OpenAPI (kin-openapi), markdown (goldmark), TLS automatisé (certmagic), infra de tests (testcontainers).**
4. **OTel est déjà couvert** par `knowledge/observability/otel-go.yaml` (pointeur Source). Pas besoin d'un module catalogue : promouvoir `prometheus-client_golang` du format legacy YAML vers le format fiche SKILL.md couvrirait le gap métriques à moindre coût.
5. **Les bibliothèques zéro-dépendance, fuzzées, pure Go dominent le haut du classement** (klauspost/compress, goldmark, age, bbolt) — exactement le profil que les gates du Kit récompensent.

---

# 2. Gates du Kit appliquées

## 2.1 Grille de gates

| Gate | Critères vérifiés |
| --- | --- |
| **G1 — Compatibilité technique** | Go ≥ 1.25 (module kit `go 1.25.6`) ; zéro cgo ; architecture stdlib-first ; pas de framework imposé ; pas de couplage cloud |
| **G2 — Qualité** | Idiomatique ; tests présents et passants ; CI configurée ; lisible de bout en bout (critère jugé par couche, cf. admission go-git) |
| **G3 — Sécurité** | Historique OSV : 0 vuln non corrigée ; version minimale ≥ dernière version corrigée ; OpenSSF Scorecard ; fuzzing |
| **G4 — Performance** | Réputation mesurée ; pas de régression documentée ; coût d'allocation connu |
| **G5 — Maintenance** | Commit/release < 6 mois ; maintien multi-années ; communauté active |
| **G6 — Licence** | MIT / BSD / Apache-2.0 (compatible produit MIT-license) ; pas de copyleft fort |
| **G7 — Intégration** | Dépendances directes minimales ; pas de conflit de versions ; coût de maintenance maîtrisé ; usage réel démontré |
| **ADM — Admission 9 critères** | Les 9 critères du Kit (dont : étoiles ≠ justification ; raison réelle exigée) |

Score global : pondération maturité 25 % · qualité 20 % · sécurité 25 % · maintenance 20 % · intégration 10 %. Note indicative, la décision repose sur les gates, pas le score.

---

# 3. Tableau des bibliothèques candidates

| Nom | Domaine | URL | Version (2026-08-05) | Score | Gates | Décision |
| --- | --- | --- | --- | --- | --- | --- |
| filippo.io/age | crypto | github.com/FiloSottile/age | v1.3.1 | 8.8 | G1-G7 PASS | **APPROUVÉE** |
| go.etcd.io/bbolt | stockage embarqué | github.com/etcd-io/bbolt | v1.5.0 | 8.7 | G1-G7 PASS | **APPROUVÉE** |
| github.com/klauspost/compress | performance | github.com/klauspost/compress | v1.19.1 | 8.6 | G1-G7 PASS | **APPROUVÉE** |
| github.com/yuin/goldmark | parsing | github.com/yuin/goldmark | v1.8.5 | 8.2 | G1-G7 PASS | **APPROUVÉE** |
| github.com/jackc/pgx/v5 | stockage/PostgreSQL | github.com/jackc/pgx | v5.10.0 | 8.0 | G1-G7 PASS (pin ≥ 5.9.2) | **APPROUVÉE** |
| github.com/minio/minio-go/v7 | stockage/S3 | github.com/minio/minio-go | v7.2.1 | 7.8 | G1-G7 PASS (G7 léger) | **APPROUVÉE** |
| github.com/getkin/kin-openapi | API/OpenAPI | github.com/getkin/kin-openapi | v0.146.0 | 7.6 | G1-G7 PASS (pièges doc.) | **APPROUVÉE** |
| github.com/testcontainers/testcontainers-go | tests infra | github.com/testcontainers/testcontainers-go | v0.43.0 | 7.5 | G1-G7 PASS (G2/G7 WARNING) | **APPROUVÉE** |
| github.com/caddyserver/certmagic | infra/TLS | github.com/caddyserver/certmagic | v0.25.4 | 7.0 | G1-G7 PASS (G7 WARNING) | **APPROUVÉE (WARNING)** |
| go.opentelemetry.io/otel | observabilité | github.com/open-telemetry/opentelemetry-go | v1.45.0 | 8.9 (scorecard) | G1/G3/G5 PASS ; **ADM-8 FAIL** (taille multi-modules) | **À SURVEILLER** |
| github.com/miekg/dns | réseau/DNS | github.com/miekg/dns (→ Codeberg) | v1.1.72 | 6.0 | G5 WARNING (migration), G2 WARNING | **À SURVEILLER** |
| github.com/oapi-codegen/oapi-codegen | API/codegen | github.com/oapi-codegen/oapi-codegen | v2.8.0 | 5.8 | G2/G7 WARNING (taille, 307 issues, v3 exp.) | **À SURVEILLER** |
| github.com/goccy/go-yaml | parsing/YAML | github.com/goccy/go-yaml | v1.18+ | 5.5 | G4 WARNING (régressions doc.), G2 WARNING | **À SURVEILLER** |
| github.com/joshuafuller/sse | réseau/SSE | github.com/joshuafuller/sse | v3 | 4.8 | G5 WARNING (adoption faible) | **À SURVEILLER** |
| github.com/cespare/xxhash/v2 | performance/hash | github.com/cespare/xxhash | v2 | 5.2 | **G5 FAIL** (0 commit depuis 2024-07) | **REFUSÉE** |
| github.com/vmihailenco/msgpack | sérialisation | github.com/vmihailenco/msgpack | v5.4.1 | 4.5 | **G5 FAIL** (inactif depuis 2024-06) | **REFUSÉE** |
| github.com/r3labs/sse | réseau/SSE | github.com/r3labs/sse | v2.10.0 | 4.0 | **G5 FAIL** (inactif depuis 2023) | **REFUSÉE** |
| maurice2k/ultrapool | concurrence | github.com/maurice2k/ultrapool | — | 3.5 | **G5/G7 FAIL** (trop jeune, perf non vérifiée) | **REFUSÉE** |
| iyashjayesh/go-adaptive-pool | concurrence | github.com/iyashjayesh/go-adaptive-pool | — | 3.0 | **G5/G7 FAIL** (créé 2025-12, 32 stars) | **REFUSÉE** |
| last9/go-agent | observabilité | github.com/last9/go-agent | — | 3.5 | **G5/G7 FAIL** (très jeune) | **REFUSÉE** |
| hollis-labs/go-otel | observabilité | github.com/hollis-labs/go-otel | — | 3.0 | **G5/G7 FAIL** (très jeune) | **REFUSÉE** |
| lowbit-dev/sse | réseau/SSE | github.com/lowbit-dev/sse | — | 3.5 | **G5/G7 FAIL** (jeune, adoption nulle) | **REFUSÉE** |
| kanata996/hah | API | github.com/kanata996/hah | — | 3.0 | **G5/G7 FAIL** (jeune) | **REFUSÉE** |
| ChiragRayani/resilix | résilience | github.com/ChiragRayani/resilix | — | 3.5 | **G5/G7 FAIL** (jeune, zéro dép. mais zéro adoption) | **REFUSÉE** |

*Note : go-redis, prometheus-client_golang, zap, zerolog, gorm, sqlx, etc. existent déjà au catalogue (format legacy YAML, kind Source) — hors périmètre « nouvelle intégration », voir §6.2.*

---

# 4. Intégrations approuvées

Pour chaque bibliothèque : pourquoi elle passe les gates, vérifications effectuées (données datées 2026-08-05), plan d'intégration (conforme Z2 §9, une bibliothèque à la fois).

## 4.1 filippo.io/age — crypto d'application (chiffrement de fichiers/secrets)

**Gates :** G1 PASS (pure Go, go 1.24, 6 deps) · G2 PASS (auteur = mainteneur crypto reconnu, revue externe) · G3 PASS (1 advisory GHSA-32gq-x56h-299c — exécution de binaire via plugin name, corrigé v1.2.1 ; v1.3.1 sain ; fuzzing 10/10) · G4 PASS (X25519 + ChaCha20-Poly1305, zéro choix de chiffrement exposés) · G5 PASS (23 088 stars, push 2026-03, v1.3.0 2025-11 avec PQ X25519MLKEM768) · G6 PASS (BSD-3-Clause) · G7 PASS (usage réel massif, licence écologique).

**Vérifications :** GitHub API (stars/push/release) · OSV (1 vuln corrigée) · Scorecard 4.7 avec **anomalie de données** : `Maintained:0` contredit par le push du 2026-03-20 (cache Scorecard périmé) — signalé ici, à ne pas interpréter comme un refus.

**Plan d'intégration :**

- Fiche `catalogs/libraries/age/SKILL.md` (format N1 §4, 6 sections) + artefact `age.yaml` minimal si question distincte (crypto file format).
- Pièges à documenter : advisory plugin v1.2.1 ; **ne pas** utiliser age pour du chiffrement réseau (pas un protocole) ; pin ≥ v1.2.1.
- Minimal use : `age.Encrypt(..., "age1...")` / `age.Decrypt(..., identity)`.

## 4.2 go.etcd.io/bbolt — stockage embarqué clé-valeur

**Gates :** G1 PASS (go 1.25, pure Go, MIT) · G2 PASS (API stable depuis des années, 9 663 stars, CI, code-review 10/10) · G3 PASS (0 advisory OSV, scorecard 7.3) · G4 PASS (performances documentées, modèle B+tree classique) · G5 PASS (push 2026-08-03, v1.5.0 2026-06-21) · G6 PASS (MIT) · G7 PASS (maintenu par etcd-io, base de etcd/Caddy/litestream).

**Vérifications :** GitHub API · OSV (0) · Scorecard 7.3 · proxy.golang (v1.5.0).

**Plan d'intégration :**

- Fiche `catalogs/libraries/bbolt/SKILL.md`. Déjà un dossier `bbolt/` ? — non, seul `modernc-sqlite` couvre l'embarqué SQL ; bbolt couvre le KV (question distincte).
- Piège à documenter : **une seule écriture transactionnelle à la fois** (verrou exclusif) ; pas de réplication ; lecture seule possible avec `Options.ReadOnly`.
- Minimal use : `bbolt.Open("db", 0600, nil)` + `tx.CreateBucket` / `Get` / `Put`.

## 4.3 github.com/klauspost/compress — compression (zstd, s2, flate, gzip)

**Gates :** G1 PASS (go 1.24, **0 dépendance directe**, pure Go) · G2 PASS (tests massifs, CI, fuzzing 10/10, SAST 10/10, scorecard 7.4) · G3 PASS (1 advisory GO-2026-5841 — OOB read dans `s2`, corrigé v1.18.7 ; **pin ≥ 1.18.7**) · G4 PASS (référence perf pure Go) · G5 PASS (5 599 stars, push 2026-08-04, v1.19.1 2026-07-20) · G6 PASS (BSD-3-Clause — le probe GitHub affiche NOASSERTION, fichier LICENSE vérifié : BSD) · G7 PASS (utilisé par MinIO, Grafana, etc. ; zéro conflit).

**Vérifications :** GitHub API · OSV (fix v1.18.7) · Scorecard 7.4 · LICENSE raw (BSD-3) · go.mod (0 require).

**Plan d'intégration :**

- Fiche `catalogs/libraries/compress/SKILL.md` (le dossier actuel est un YAML legacy : `...libraries/` — vérifier le nom exact à l'admission).
- Piège : advisory s2 ; ne remplacer gzip/flate stdlib qu'avec bench à l'appui (G4 « mesuré »).
- Minimal use : `zstd.NewWriter(nil)` / `s2.Encode(nil, src)`.

## 4.4 github.com/yuin/goldmark — parsing markdown (CommonMark)

**Gates :** G1 PASS (go 1.22, **0 dépendance**, pure Go) · G2 PASS (conformité CommonMark 0.31.2, tests extensifs) · G3 PASS (1 advisory GO-2026-5320 — XSS via raw HTML/attr, corrigé v1.7.17 ; **pin ≥ 1.7.17** ; fuzzing 10/10) · G4 PASS (parser sans allocations majeures, benchmarks publiés) · G5 PASS (4 927 stars, push 2026-08-02, v1.8.5 2026-07-28) · G6 PASS (MIT) · G7 PASS (usage réel : Hugo, etc.).

**Vérifications :** GitHub API · OSV (fix v1.7.17) · go.mod (0 require).

**Plan d'intégration :**

- Fiche `catalogs/libraries/goldmark/SKILL.md`.
- Piège : **XSS** — ne jamais rendre du HTML non sanitisé côté serveur sans `html` sanitisation ; v2 en beta (breaking pour extensions) à surveiller.
- Minimal use : `goldmark.Convert(src, &buf)`.

## 4.5 github.com/jackc/pgx/v5 — driver PostgreSQL (interface native + stdlib)

**Gates :** G1 PASS (go 1.25, MIT, pure Go, interface `database/sql` disponible via `pgx/v5/stdlib`) · G2 PASS (14 093 stars, tests + CI, fuzzing 10/10) · G3 **PASS avec pin obligatoire** : 4 advisories — CVE-2024-27304 (SQLi, fix v5.5.5), CVE-2026-33815/33816 (placeholder confusion, fix v5.9.0), **GO-2026-5004 (SQLi dollar-quoted literals, fix v5.9.2)** → **pin ≥ v5.9.2, actuel v5.10.0 sain** · G4 PASS (interface native 20-63 % plus rapide que database/sql selon benchs publics) · G5 PASS (push 2026-08-01) · G6 PASS (MIT) · G7 PASS (standard de facto, usage massif).

**Vérifications :** GitHub API · OSV (4 advisories, tous corrigés ≤ 5.9.2 ; détail GO-2026-5004 vérifié : range v5 introduit 0 → fix 5.9.2) · proxy.golang (v5.10.0) · Scorecard 4.6 (code-review 1/10, token-permissions 0 — WARNING process, compensé par fuzzing).

**Plan d'intégration :**

- Fiche `catalogs/libraries/pgx/SKILL.md`.
- Pièges : SQLi classe placeholder (voir GO-2026-5004 — ne pas activer le protocole simple avec littéraux `$tag$` non contrôlés) ; `QueryExecModeCacheStatement` + requêtes dynamiques = surface SQLi ; toujours `pgxpool` et paramètres `$1..$n`.
- Minimal use : `pgxpool.New(ctx, url)` + `pool.Query(ctx, "SELECT ... WHERE id=$1", id)`.
- Alternative enregistrée : lib/pq (maintenance minimale, rejetée).

## 4.6 github.com/minio/minio-go/v7 — client S3 (object storage)

**Gates :** G1 PASS (go 1.25, Apache-2.0, pure Go) · G2 PASS (2 984 stars, CI, code-review 9/10) · G3 PASS (0 advisory OSV) · G4 PASS (client mature, streaming multipart) · G5 PASS (très actif : push 2026-08-04, v7.2.0 2026-05-27) · G6 PASS (Apache-2.0) · G7 PASS avec léger WARNING (14 deps directes — le plus lourd des approuvés) ; usage réel massif.

**Vérifications :** GitHub API · OSV (0) · proxy.golang (v7.2.1).

**Plan d'intégration :**

- Fiche `catalogs/libraries/minio-go/SKILL.md`.
- Piège : 14 deps → `go mod tidy` sous surveillance ; compatibilité S3 ≠ 100 % (API MinIO étendues) ; préférer l'interface AWS `s3manager` pour compatibilité AWS stricte.
- Minimal use : `minio.New(endpoint, &minio.Options{Creds: ...})` + `PutObject`.

## 4.7 github.com/getkin/kin-openapi — parsing/validation OpenAPI 3

**Gates :** G1 PASS (go 1.25, MIT, pure Go) · G2 PASS (3 270 stars, très actif, 220 contributeurs) · G3 **PASS avec pièges documentés** : 4 advisories tous corrigés — nil-pointer panic (fix 0.144.0), **fail-open auth bypass** `ValidationHandler.Load()` (fix 0.144.0), data amplification (fix 0.131.0) → **pin ≥ 0.144.0, actuel 0.146.0 sain** · G4 PASS (validation de schéma en mémoire, perf raisonnable) · G5 PASS (release v0.146.0 le 2026-08-03 !) · G6 PASS (MIT) · G7 PASS (standard de facto, utilisé par oapi-codegen, F5, Kong).

**Vérifications :** GitHub API · OSV (4 advisories, fixes ≤ 0.144.0) · Scorecard 4.3 (pas de fuzzing — WARNING).

**Plan d'intégration :**

- Fiche `catalogs/libraries/kin-openapi/SKILL.md`.
- Pièges : **fail-open par défaut de `ValidationHandler`** (authentication bypass si `NoopAuthenticationFunc`) — configurer explicitement un authenticateur ; DoS par payload compressé (fix 0.131.0) ; préférer `openapi3filter.ValidateRequest`.
- Minimal use : `openapi3.NewLoader().LoadFromData(spec)` + `Validate(ctx)`.

## 4.8 github.com/testcontainers/testcontainers-go — infra de test (containers)

**Gates :** G1 PASS (MIT, go ≥ 1.22 — vérifier la directive exacte à l'admission) · G2 PASS avec WARNING (4 940 stars, CI 10/10, SAST 10/10, mais repo 24.9 MB, ~60 kLOC — critère « lisible de bout en bout » jugé par couche/modules) · G3 PASS (0 advisory OSV, scorecard 6.1) · G4 PASS (n/a — infra de test) · G5 PASS (très actif, v0.43.0 2026-06-19, releases fréquentes) · G6 PASS (MIT) · G7 PASS avec WARNING (**exige Docker** à l'exécution des tests ; le Kit ne doit l'inclure que comme dépendance de test, jamais runtime).

**Vérifications :** GitHub API · OSV (0) · Scorecard 6.1.

**Plan d'intégration :**

- Fiche `catalogs/libraries/testcontainers-go/SKILL.md` + usage exclusif en `_test.go` / recipes de tests d'intégration.
- Piège : les probes du Kit tournent en CI — ne pas rendre la gate dépendante de Docker ; scénario d'usage marqué `PARTIAL` si Docker absent.
- Minimal use : `testcontainers.GenericContainer(ctx, req)` + `Start` / `Terminate`.

## 4.9 github.com/caddyserver/certmagic — TLS automatisé (ACME) — **APPROUVÉE AVEC WARNING**

**Gates :** G1 PASS (go 1.25, Apache-2.0) · G2 PASS (5 589 stars, moteur TLS de Caddy, code-review 5/10) · G3 PASS (0 advisory OSV ; scorecard 4.5 — pas de fuzzing, WARNING) · G4 PASS (ACME complet, gestion OCSP/renouvellement) · G5 PASS (v0.25.3 2026-05, push 2026-07-17) · G6 PASS (Apache-2.0) · G7 **WARNING** : 10 deps directes, scorecard process moyen → coût de maintenance réel ; usage massif (Caddy) compense.

**Vérifications :** GitHub API · OSV (0) · proxy.golang (v0.25.4).

**Plan d'intégration :**

- Fiche `catalogs/libraries/certmagic/SKILL.md`.
- Piège : jamais utiliser `certmagic.Default` (state global partagé — isoler par instance) ; rate limits Let's Encrypt ; renouvellement + OCSP = monitoring requis.
- Minimal use : `certmagic.New(ctx, certmagic.Default)` + `ManageAsync(ctx, []string{domain})`.

---

# 5. Bibliothèques refusées — raisons précises

| Bibliothèque | Gate échouée | Raison (évidence) |
| --- | --- | --- |
| **cespare/xxhash/v2** | G5 (maintenance) | 0 commit depuis 2024-07-03, scorecard `Maintained:0`. Produit stable et correct (2 139 stars, MIT) mais le critère 1 du Kit exige un maintien récent. **Note :** grade « dépendance » — il reste acceptable comme dépendance transitive (déjà vendored par klauspost/compress) ; pas de fiche catalogue. |
| **vmihailenco/msgpack** | G5 (maintenance) | Dernier commit 2024-06-04, dernière release v5.4.1 (2023-10-26). > 2 ans d'inactivité. |
| **r3labs/sse** | G5 (maintenance) | Dernier push 2024-06, v2.10.0 daté 2023-01. SSE = stdlib possible (`text/event-stream` + `http.Flusher`) — le Kit doit recommander le stdlib ici. |
| **maurice2k/ultrapool** | G5/G7 | Projet récent sans track record ; gains perf (nanosecondes) auto-déclarés, non vérifiés ; zéro évidence d'usage réel. |
| **iyashjayesh/go-adaptive-pool** | G5/G7 | Créé 2025-12, 32 stars, 4 issues ouvertes. |
| **last9/go-agent** | G5/G7 | Créé fin 2025, adoption quasi nulle. |
| **hollis-labs/go-otel** | G5/G7 | Créé 2026, < 10 stars. |
| **lowbit-dev/sse** | G5/G7 | Jeune, adoption nulle ; design stdlib-first intéressant → à revoir dans 12 mois. |
| **kanata996/hah** | G5/G7 | Jeune, adoption nulle. |
| **ChiragRayani/resilix** | G5/G7 | Jeune, adoption nulle ; le Kit couvre déjà retry/backoff par patterns stdlib (x/sync, recipes). |

**Règle confirmée :** les bibliothèques « émergentes » échouent le critère 1 (activité) et le critère 7 (usage réel) du Kit. C'est une feature, pas un bug : la gate protège le produit de la dette de maintenance.

---

# 6. Bibliothèques à surveiller (future intégration)

| Bibliothèque | Pourquoi surveiller | Condition d'admission |
| --- | --- | --- |
| **open-telemetry/opentelemetry-go** (v1.45.0) | Scorecard **8.9** (meilleure note sécurité de l'échantillon), fuzzing 10/10, security-policy 10/10. Échoue ADM-8 (« lisible de bout en bout ») : ~30 modules, repo 31.5 MB. | Déjà couvert par `knowledge/observability/otel-go.yaml`. Promouvoir `prometheus-client_golang` (legacy YAML → fiche SKILL.md) d'abord ; admettre OTel comme **cas exceptionnel documenté** si un module vété « observabilité unifiée » devient requis. |
| **miekg/dns** (v1.1.72) | 8 743 stars, fuzzing 10/10, SAST 9/10. Repo primaire migré vers **Codeberg**, v2 (0.6.x) en développement sur Codeberg → instabilité de source. | Admissible quand la v2 est stable et le repo primaire stabilisé. |
| **oapi-codegen** (v2.8.0) | 8 503 stars, actif ; mais repo 18.9 MB, 307 issues ouvertes, v3 expérimentale, conflit de version signalé avec kin-openapi v0.134.0. | C'est un outil de codegen (CLI) plus qu'une bibliothèque : attendre v3 stable ; kin-openapi couvre déjà le besoin API. |
| **goccy/go-yaml** | Alternative performante à yaml.v3 (upstream non maintenu) ; mais régressions mémoire documentées (≥ v1.9.3) et résultats de bench contradictoires. | Revenir quand la courbe de régression est stable ; décision intermédiaire : documenter `gopkg.in/yaml.v3` comme « dernière version conservée » dans un pointeur. |
| **joshuafuller/sse** (fork v3) | Fork maintenu de r3labs/sse, 40+ correctifs ; adoption faible. | Admissible si adoption > seuil et usage réel démontré ; sinon stdlib SSE. |
| **go-redis / prometheus-client_golang** (déjà au catalogue, format legacy YAML) | Promouvoir au format fiche SKILL.md (N1 §4) — les 6 sections décisionnelles manquent. | Promotion = décision écrite (Z2 §4.3), pas une nouvelle admission. |

---

# 7. Recommandations pour le Kit

## 7.1 Améliorations de processus (découlent de cette étude)

1. **Encoder le « pin minimal » dans les fiches.** Toute fiche de bibliothèque avec historique d'advisories doit porter la version minimale exigée (ex. `pgx ≥ 5.9.2`, `kin-openapi ≥ 0.144.0`, `compress ≥ 1.18.7`, `goldmark ≥ 1.7.17`) et la date de vérification. Vérifiable par C2 : champ frontmatter `min-pin` ou section « Versions de sécurité ».
2. **Ajouter un pointeur stdlib pour `x/crypto` (argon2/bcrypt), `x/time/rate`, `x/sync` (errgroup/singleflight/semaphore).** `knowledge/stdlib/` couvre `sync` mais pas les modules `golang.org/x/*` — ce sont les réponses minimales à 3 questions récurrentes (hash de mot de passe, rate limit, concurrence structurée). Schéma Source existant, coût ≈ 3 artefacts.
3. **Traiter SSE par stdlib** : recommandation pattern (pas de bibliothèque) — `http.Flusher` + `text/event-stream` + reconnect/backoff ; noter la morte r3labs/sse en anti-pattern de catalogue.
4. **Promouvoir prometheus-client_golang du YAML legacy vers la fiche SKILL.md** (gap métriques) avant d'envisager OTel comme module.
5. **Cadrer le critère « lisible de bout en bout »** : go-git est admis « par couche » ; écrire explicitement que l'admission juge la lisibilité par couche/module, sinon OTel, pgx et testcontainers seront refusés/repris arbitrairement.

## 7.2 Nouvelles opportunités détectées

- **Domaines encore non couverts après cette vague :** résilience (retry/circuit-breaker — le Kit recommande déjà les patterns stdlib ; surveiller resilix), fuzzing property-based (rapid — déjà probablement couvert par la gate de tests ? vérifier), génération de clients OpenAPI (attendre oapi-codegen v3).
- **Dépendance de confiance :** age, bbolt, goldmark et klauspost/compress forment un noyau « zéro-dette » (0-6 deps, fuzzés, pure Go) — profil à privilégier dans les futures admissions.

## 7.3 Informations manquantes (à compléter avant exécution)

- Directive `go` exacte de testcontainers-go (non vérifiée — repo large, proxy non interrogé).
- Scorecard `Maintained:0` pour age (contredit par GitHub — cache Scorecard à re-vérifier).
- LOC exacts par bibliothèque (données repo en KB seulement) ; compter à l'admission pour documenter le critère ADM-8.
- Statut exact des YAML legacy (22 fichiers kind Source) vs le plan de migration vers SKILL.md — hors périmètre de cette étude, mais préalable à toute promotion.

---

# 8. Pipeline d'intégration (procédure, à exécuter après approbation)

Conforme Z2 §9 et A1 : **une bibliothèque à la fois, jamais en parallèle** ; chaque admission est une décision écrite.

1. **Plan** dans `docs/plans/2026-08-05-<slug>.md` (fichiers à créer, ressources, dépendances).
2. **Fiche SKILL.md** : frontmatter immuable (name/description/category/tags/last-verified) + sections obligatoires N1 §4 (`Utiliser / Ne pas utiliser quand`, `Avantages`, `Inconvénients`, `Pièges connus`, `Sources vérifiées`) + sections vétées (Selection, Admission checklist 9 critères, Minimal use, Alternatives, Security note).
3. **Artefacts YAML** du graphe de connaissance pour les questions distinctes non couvertes (une question = un artefact ; zéro padding).
4. **Router** régénéré (`tools/generators/`) → index mis à jour.
5. **Gate complète** : `validate-instructions.py` + `validate-kitv2.py` + `go mod tidy && go mod verify` + `gofmt -l` + `go vet` + `golangci-lint run` + `go test -race ./...` + `gosec ./...` + `govulncheck ./...` + `probes/run.sh`.
6. **Évidence** brute dans `docs/evidence/2026-08-05/<slug>/`.
7. **Revue fresh-context** avant déclaration de complétude.

Ordre d'exécution recommandé (dette croissante) : age → bbolt → goldmark → compress → pgx → kin-openapi → minio-go → testcontainers-go → certmagic.

---

*Sources primaires consultées : GitHub API (stars, push, releases, licence), proxy.golang.org (versions, go.mod), OSV API (advisories et versions corrigées), OpenSSF Scorecard API, recherches web multi-sources. Données brutes non conservées dans ce fichier — voir les commandes de collecte de la session.*
