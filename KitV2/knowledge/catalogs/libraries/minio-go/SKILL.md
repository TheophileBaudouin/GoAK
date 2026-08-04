---
name: minio-go
description: "github.com/minio/minio-go/v7 v7.2.1 — official MinIO client SDK for Amazon S3-compatible object storage. Use when choosing an S3 client in Go. Not for filesystems or non-S3 storage, and its API is broader than the AWS SDK — pin the AWS interface for strict AWS-only compatibility."
category: library
tags: [storage, s3, object-storage, minio, aws, client]
last-verified: 2026-08-05
---

# minio-go — client S3 (object storage)

## Selection

[`github.com/minio/minio-go/v7`](https://github.com/minio/minio-go) (v7.2.1,
Go 1.25+).

**Why it passes the gate** (actual reason, not stars): it is the official,
actively maintained client for S3-compatible object storage (MinIO, AWS S3,
R2, GCS-interop) — pure Go, code-review 9/10, zero security advisories, and
a stable v7 API. Single responsibility (S3 client), real-world usage massive.

## Admission checklist

- [x] Actively maintained — v7.2.0 (2026-05-27), push 2026-08-04
- [x] Single responsibility — S3-compatible object storage client
- [x] Idiomatic Go — typed options, context support, no magic
- [x] Tests present + CI — yes; code-review 9/10 (scorecard 5.3)
- [x] Documentation — godoc + examples + MinIO docs
- [x] Real-world usage — MinIO, AWS-compatible stacks, cloud tooling
- [x] Readable end-to-end — ~30 kLOC, layered (credentials/transport/api)
- [x] Justified by need — le catalogue ne couvrait pas le stockage objet ;
      NOT popularity

## Minimal use

```go
client, _ := minio.New("play.min.io", &minio.Options{
    Creds:  credentials.NewStaticV4("user", "pass", ""),
    Secure: true,
})
info, err := client.PutObject(ctx, "bucket", "key.txt",
    bytes.NewReader(data), int64(len(data)), minio.PutObjectOptions{})
```

Compilé (client + PutObject) avec v7.2.1 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `aws-sdk-go-v2` (service/s3) | SDK AWS officiel, lourd (multi-services) ; minio-go est plus léger et suffit pour S3-compatible. Choisir AWS SDK si l'écosystème AWS v2 est déjà requis. |
| `aws-sdk-go` v1 | Ancienne génération, maintenance en déclin ; non retenue. |
| `s3manager` (aws-sdk) | Upload parallèle intégré à l'AWS SDK ; à composer si le besoin dépasse minio-go (rare en pratique). |
| HTTP direct (signature V4 maison) | Anti-pattern : la signature AWS est une classe d'erreur connue ; jamais de client maison. |

## Security note

- **0 advisory** OSV (vérifié 2026-08-05).
- Crédentials : passer par `credentials` (static, env, IAM, chain) — jamais de
  clés en dur dans le code (voir `pattern:antipattern:sec-hardcoded-credentials`).
- TLS : `Secure: true` par défaut de facto ; forcer HTTPS hors réseaux
  locaux de confiance.
- 14 dépendances directes (le plus lourd des approuvés 2026-08-05) : suivre
  `go mod verify` + govulncheck dans la gate.

## Utiliser cette librairie quand

- L'application écrit/ lit des objets sur un stockage S3-compatible (MinIO,
  AWS S3, R2, autres).
- Besoin d'upload/download, presigned URLs, bucket lifecycle, multipart —
  avec un client léger et maintenu.
- Le code cible plusieurs backends S3-compatible interchangeables.

## Ne pas utiliser cette librairie quand

- L'écosystème AWS v2 complet est déjà une dépendance : utiliser
  `aws-sdk-go-v2` (un seul SDK).
- Stockage non-S3 (fichiers locaux, GCS natif, Azure Blob) : driver dédié.
- Strict besoin AWS-only avec garanties de compatibilité maximales : évaluer
  l'AWS SDK v2 (le spectre d'API de minio-go dépasse S3).

## Avantages

- Client S3 officiel MinIO : actif, stable (v7), zéro advisory.
- Léger face à l'AWS SDK, API S3-compatible large (presigned, multipart,
  notifications).
- Code-review 9/10, chaîne de credentials flexible (env, IAM, static).
- Adopté massivement dans l'écosystème Go de stockage objet.

## Inconvénients

- 14 dépendances directes (surface transitive plus large que les autres
  approuvés).
- Spectre d'API plus large que S3 strict (extensions MinIO) : pour une cible
  AWS seule, l'AWS SDK v2 reste le choix de compatibilité stricte.
- Pas de support natif de requêtes SQL/analytiques objets (hors périmètre
  client).

## Pièges connus

- Ne pas hardcoder les credentials (anti-pattern dédié) ; préférer
  `credentials.NewEnvAWS()` ou une chaîne de credentials explicite.
- Multipart : vérifier l'état de l'upload sur erreur (parties orphelines) ;
  utiliser `PutObject` avec des objets < 64 Mo en simple PUT.
- Les URLs presignées expirent : générer avec une durée explicite, ne pas
  mettre en cache plus longtemps que l'expiration.
- Versionnage : v7 = API stable, mais les options évoluent — épingler une
  version exacte et tester à chaque bump (releases fréquentes).

## Sources vérifiées

- [minio/minio-go (repo officiel, v7.2.1)](https://github.com/minio/minio-go)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/minio/minio-go/v7](https://pkg.go.dev/github.com/minio/minio-go/v7)
  — vérifié 2026-08-05
- OSV : aucun advisory pour `github.com/minio/minio-go/v7` (requête API
  2026-08-05)
- Artefacts internes : `pattern:antipattern:sec-hardcoded-credentials`,
  `pattern:security:secrets-management`, `source:security:file-encryption`
