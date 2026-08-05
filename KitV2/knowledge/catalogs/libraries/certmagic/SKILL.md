---
name: certmagic
description: "github.com/caddyserver/certmagic v0.25.4 — ACME certificate issuance, renewal, OCSP, storage, and on-demand TLS for Go. Use for embedded automatic HTTPS with persistent/shared storage; not for a simple static certificate, external edge proxy, or unreviewed global defaults."
category: library
tags: [tls, acme, https, certificates, letsencrypt, certmagic, security]
last-verified: 2026-08-05
---

# certmagic — TLS automatisé ACME

## Selection

[`github.com/caddyserver/certmagic`](https://github.com/caddyserver/certmagic)
v0.25.4 is the ACME/TLS lifecycle engine used by Caddy. It supports issuance,
renewal, OCSP, on-demand TLS, multiple issuers, storage, and distributed locks.
It is admitted with a dependency-surface warning for complete embedded HTTPS;
use `autocert` or static `crypto/tls` when the smaller boundary is enough.

## Admission checklist

- [x] Current v0.25.4 tag and active upstream maintenance.
- [x] Single responsibility: automated certificate lifecycle.
- [x] Config/cache instances, `net/http`/TLS integration, tests, CI, and docs.
- [x] Production validation through Caddy and a focused API.
- [x] ACME storage, rate limits, and cluster coordination are explicit costs.

## Minimal use

```go
func manageCertificates(ctx context.Context, domains []string) error {
    cache := certmagic.NewCache(certmagic.CacheOptions{})
    config := certmagic.New(cache, certmagic.Config{})
    if err := config.ManageSync(ctx, domains); err != nil {
        return fmt.Errorf("manage certificates: %w", err)
    }
    return nil
}
```

Use staging CAs during development and configure persistent/shared storage before
running multiple instances. Monitor expiry and renewal failures as an
application operation; certificate automation is not observability.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `golang.org/x/crypto/acme/autocert` | Prefer for a simpler single-process ACME flow with fewer features/dependencies. |
| Static `crypto/tls` certificate | Prefer when certificates are issued and rotated by deployment infrastructure. |
| Caddy/nginx at the edge | Prefer when the application does not own TLS termination. |
| `lego` | Consider when a lower-level ACME client and custom issuer workflow are required. |

## Utiliser cette librairie quand

- A Go server owns HTTPS and needs automatic ACME issue/renew/OCSP lifecycle.
- On-demand TLS, multiple issuers, or shared storage/locking are real requirements.
- The deployment can provide DNS/HTTP/TLS-ALPN challenge reachability and
  persistent storage.

## Ne pas utiliser cette librairie quand

- A static certificate or small `autocert` flow covers the requirement.
- TLS terminates in an external proxy or load balancer.
- The CA/issuer is outside the supported ACME/API behavior.
- The project cannot persist certificate state or monitor renewal failures.

## Avantages

- Complete issuance, renewal, OCSP, on-demand, issuer, and storage lifecycle.
- Shared storage and locking support clustered certificate management.
- Caddy provides substantial real-world production validation.

## Inconvénients

- Larger dependency/operational surface than stdlib-adjacent autocert.
- ACME issuance depends on public DNS/network/ports and external rate limits.
- Storage, backup, alerting, and instance coordination remain deployment duties.
- Package-level default helpers can hide shared mutable configuration.

## Pièges connus

- Prefer instance `Cache`/`Config`; avoid `certmagic.Default` in tests or
  multi-tenant services.
- Use ACME staging and bounded integration tests to avoid CA rate limits.
- Persist certificate storage and backups; loss causes re-issuance pressure.
- Monitor expiry, renewal errors, issuer availability, and storage locks.
- Validate the issuer and challenge topology before exposing on-demand TLS.

## Sources vérifiées

- [Official CertMagic repository](https://github.com/caddyserver/certmagic) —
  API, maintenance, license, checked 2026-08-05.
- [CertMagic v0.25.4 package](https://pkg.go.dev/github.com/caddyserver/certmagic)
  — current tag and API, checked 2026-08-05.
- [CertMagic releases](https://github.com/caddyserver/certmagic/releases) —
  release history, checked 2026-08-05.
- [CertMagic README](https://github.com/caddyserver/certmagic/blob/v0.25.4/README.md)
  — storage, ACME, and operational behavior, checked 2026-08-05.
- [Storage source](https://github.com/caddyserver/certmagic/blob/v0.25.4/storage.go)
  — locking/shared storage, checked 2026-08-05.
- [OCSP source](https://github.com/caddyserver/certmagic/blob/v0.25.4/ocsp.go)
  — responder validation, checked 2026-08-05.
