---
name: certmagic
description: "github.com/caddyserver/certmagic v0.25.4 — automatic HTTPS for Go servers: ACME issuance, renewal, OCSP, and certificate management (the TLS engine behind Caddy). Use when choosing a TLS automation library. Not a full TLS/ACME client replacement for exotic CAs, and avoid its package-level Default global (isolate instances)."
category: library
tags: [tls, acme, https, certificates, letsencrypt, certmagic, security]
last-verified: 2026-08-05
---

# certmagic — TLS automatisé (ACME)

## Selection

[`github.com/caddyserver/certmagic`](https://github.com/caddyserver/certmagic)
(v0.25.4, Go 1.25+).

**Why it passes the gate** (actual reason, not stars): it is the most complete
ACME integration in Go (issuance, renewal window, OCSP, on-demand TLS) and the
engine behind Caddy — a small (~6 kLOC), focused library with zero security
advisories. Approved with WARNING: 10 direct dependencies and a moderate
scorecard (4.5, no fuzzing) — the maintenance cost is real and must be
tracked.

## Admission checklist

- [x] Actively maintained — v0.25.3 (2026-05-11), push 2026-07-17
- [x] Single responsibility — automatic HTTPS / certificate lifecycle
- [x] Idiomatic Go — cache + config instances, net/http & tls integration
- [x] Tests present + CI — yes; Caddy production use as continuous test
- [x] Documentation — README + godoc + Caddy docs
- [x] Real-world usage — Caddy (moteur TLS), nombreux serveurs Go
- [x] Readable end-to-end — small (~6 kLOC), layered
- [x] Justified by need — le catalogue ne couvrait pas l'automatisation TLS ;
      NOT popularity (WARNING G7 : 10 deps, scorecard process moyen)

## Minimal use

```go
cache := certmagic.NewCache(certmagic.CacheOptions{})
magic := certmagic.New(cache, certmagic.Config{})   // instance isolée
err := magic.ManageAsync(ctx, []string{"example.org"})
```

Compilé avec v0.25.4 le 2026-08-05 (compile only — émission ACME réelle non
exécutée ici).

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `golang.org/x/crypto/acme/autocert` | Plus léger mais moins complet (renouvellement, OCSP, on-demand) ; certmagic est le choix complet. |
| Gestion manuelle (acme client + cron) | Réinvente le renouvellement : classe d'erreur connue (cert expiré = outage silencieux). |
| Reverse proxy externe (Caddy/nginx) | Valable pour l'edge ; certmagic embarque le même moteur côté application. |
| `certbot` (interne au déploiement) | Hors processus Go ; certmagic intègre le cycle de vie au runtime. |

## Security note

- **0 advisory** OSV (vérifié 2026-08-05).
- Ne jamais utiliser `certmagic.Default` (config globale mutable partagée — voir
  `pattern:antipattern:go-mutable-global-state`) : créer un cache + config par
  instance.
- Rate limits Let's Encrypt : tester avec l'environnement de staging
  (`ACMEIssuer.Test`), jamais le endpoint de production dans les tests.
- OCSP/révocation et renouvellement sont gérés par certmagic, mais le
  **monitoring** (cert proche d'expiration, échec de renouvellement) reste à
  la charge de l'application.

## Utiliser cette librairie quand

- Un serveur Go doit servir du HTTPS avec certificats ACME gérés
  automatiquement (issuance + renouvellement + OCSP).
- L'application a besoin de TLS on-demand (certificats à la demande par
  hostname).
- Caddy-style : zéro opération manuelle de certificats souhaitée.

## Ne pas utiliser cette librairie quand

- Le besoin est un simple `tls.Config` avec un certificat déjà fourni :
  `crypto/tls` + `autocert` (ou fichier) suffisent — zéro dépendance.
- CA exotiques / protocoles ACME non standards : vérifier le support de
  l'issuer (ACME standard, Zerossl) avant d'adopter.
- L'application ne contrôle pas l'edge (proxy externe) : la gestion TLS vit
  dans le proxy, pas ici.

## Avantages

- Cycle de vie TLS complet : issuance, renouvellement (fenêtre), OCSP,
  on-demand.
- Moteur éprouvé par Caddy en production massive.
- API par instance (cache + config) : testable, sans global si on évite
  `Default`.
- Intégration `net/http` et `crypto/tls` propre.

## Inconvénients

- 10 dépendances directes (la plus lourde surface des approuvés 2026-08-05) —
  WARNING G7.
- Scorecard process moyen (4.5, pas de fuzzing, token-permissions 0).
- L'émission ACME réelle dépend de l'environnement (ports 80/443, DNS,
  network) : tests d'intégration contraignants.
- API riche : config par défaut commode mais piégeuse (global Default).

## Pièges connus

- **`certmagic.Default` = état global mutable partagé** : en multitenant ou
  tests, créer cache + config par instance (voir
  `pattern:antipattern:go-mutable-global-state`).
- Rate limits ACME : toujours staging en dev/test, production seulement après
  validation.
- Certificats stockés par défaut dans `~/.local/share/certmagic` (ou
  configurés) : prévoir la persistance et le backup (perte = re-issuance +
  rate limits).
- L'échec silencieux de renouvellement n'est pas détecté par la lib :
  monitorer l'expiration (alerte avant le `RenewalWindowRatio`).

## Sources vérifiées

- [caddyserver/certmagic (repo officiel, v0.25.4)](https://github.com/caddyserver/certmagic)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/caddyserver/certmagic](https://pkg.go.dev/github.com/caddyserver/certmagic)
  — vérifié 2026-08-05
- OSV : aucun advisory pour `github.com/caddyserver/certmagic` (requête API
  2026-08-05)
- Artefacts internes : `pattern:antipattern:go-mutable-global-state`,
  `pattern:security:fail-closed-auth`, `source:security:file-encryption`
