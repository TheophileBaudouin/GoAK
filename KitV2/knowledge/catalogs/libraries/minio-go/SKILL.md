---
name: minio-go
description: "github.com/minio/minio-go/v7 v7.2.1 — Go client for S3-compatible object storage. Use for MinIO, S3, R2, or compatible object APIs; not for local files, non-S3 services, or a strict AWS-only SDK contract."
category: library
tags: [storage, s3, object-storage, minio, aws, client]
last-verified: 2026-08-05
---

# minio-go — client stockage objet S3

## Selection

[`github.com/minio/minio-go/v7`](https://github.com/minio/minio-go) v7.2.1,
released 2026-06-26, is MinIO's pure-Go S3-compatible client. It covers bucket,
object, multipart, presigned URL, policy, and notification operations. It is
admitted for this focused object-storage boundary, active maintenance, tests,
documentation, and real use; not for popularity. Server advisories are not
client SDK advisories and must not be conflated.

## Admission checklist

- [x] Current v7.2.1 stable module and active maintenance.
- [x] Single responsibility: S3-compatible object client.
- [x] Context-aware typed API with tests, CI, and documentation.
- [x] Flexible credential providers and multipart/presigned operations.
- [x] Production use across MinIO and compatible object stores.

## Minimal use

```go
func upload(ctx context.Context, data []byte) error {
    client, err := minio.New("play.min.io", &minio.Options{
        Creds: credentials.NewStaticV4("user", "pass", ""),
        Secure: true,
    })
    if err != nil {
        return fmt.Errorf("create object client: %w", err)
    }
    _, err = client.PutObject(ctx, "bucket", "key.txt", bytes.NewReader(data),
        int64(len(data)), minio.PutObjectOptions{})
    if err != nil {
        return fmt.Errorf("put object: %w", err)
    }
    return nil
}
```

Use environment/IAM credential chains instead of the placeholder static
credentials in real deployments. Bound object sizes and contexts at the
application boundary.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `aws-sdk-go-v2/service/s3` | Prefer when the application is AWS-only and already uses the full AWS SDK. |
| `s3manager` | Compose when AWS-specific transfer orchestration is required. |
| Direct HTTP/SigV4 | Reject hand-written signing; it recreates a security-sensitive protocol boundary. |
| Local filesystem | Use `os`/`io` for local files; S3 clients do not simplify that case. |

## Utiliser cette librairie quand

- The service reads/writes objects on MinIO, AWS S3, R2, or another S3-compatible
  backend.
- Multipart uploads, presigned URLs, bucket lifecycle, and object operations
  are required without a full multi-service cloud SDK.
- Multiple S3-compatible endpoints share one client boundary.

## Ne pas utiliser cette librairie quand

- The project needs AWS services beyond S3 and already standardizes on AWS SDK
  v2.
- Storage is local files, native GCS, Azure Blob, or a non-S3 protocol.
- Strict AWS-only API compatibility is more important than MinIO extensions.

## Avantages

- Broad S3-compatible API with context, multipart, presigned, and credential
  chain support.
- Pure Go and smaller responsibility than a full cloud SDK.
- Current stable v7 line with active MinIO maintenance.

## Inconvénients

- Larger transitive surface than a tiny custom object boundary; scan it with
  `go mod verify` and `govulncheck`.
- MinIO extensions can exceed strict AWS S3 compatibility expectations.
- Upload retries depend on reader seekability and known-size choices.

## Pièges connus

- Never hardcode credentials; use environment, IAM, or a protected provider.
- Use HTTPS outside an explicitly trusted local network.
- Give uploads a bounded size and a cancellable context; unknown-size uploads
  can use more memory and retries need a replayable reader.
- Give presigned URLs an explicit expiry and never cache them past that expiry.
- Distinguish the MinIO server's advisories from the client SDK's own advisory
  record when reviewing dependencies.

## Sources vérifiées

- [Official minio-go repository](https://github.com/minio/minio-go) — API,
  maintenance, license, checked 2026-08-05.
- [minio-go v7 on pkg.go.dev](https://pkg.go.dev/github.com/minio/minio-go/v7)
  — exact version and API, checked 2026-08-05.
- [MinIO Go API reference](https://docs.min.io/aistor/developers/sdk/go/api/) —
  object/bucket operations, checked 2026-08-05.
- [minio-go advisories](https://github.com/minio/minio-go/security/advisories)
  — client-specific security status, checked 2026-08-05.
- [Issue #2078](https://github.com/minio/minio-go/issues/2078) — non-seekable
  reader retry behavior, checked 2026-08-05.
- [Issue #989](https://github.com/minio/minio-go/issues/989) — unknown-size
  upload memory behavior, checked 2026-08-05.
