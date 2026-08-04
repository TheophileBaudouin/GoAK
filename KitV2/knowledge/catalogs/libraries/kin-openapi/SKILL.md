---
name: kin-openapi
description: "github.com/getkin/kin-openapi v0.146.0 — OpenAPI 3.0/3.1 parser, validator, and openapi3filter request/response validation for Go. Use when choosing an OpenAPI library (spec load, validate, request routing). Not a code generator (see oapi-codegen, watch list) and its ValidationHandler defaults to fail-open — configure auth explicitly."
category: library
tags: [api, openapi, openapi3, validation, spec, rest]
last-verified: 2026-08-05
---

# kin-openapi — OpenAPI 3 parsing et validation

## Selection

[`github.com/getkin/kin-openapi`](https://github.com/getkin/kin-openapi)
(v0.146.0, Go 1.25+).

**Why it passes the gate** (actual reason, not stars): it is the reference
OpenAPI 3 implementation in Go — spec load, schema validation, and
`openapi3filter` for runtime request/response validation — with 220+
contributors and near-daily releases. All 4 security advisories are fixed in
current; the fiche documents its fail-open default (a real footgun).

## Admission checklist

- [x] Actively maintained — v0.146.0 (2026-08-03), push 2026-08-03
- [x] Single responsibility — OpenAPI 3 spec parsing + validation
- [x] Idiomatic Go — openapi3.T types, net/http-friendly filter
- [x] Tests present + CI — yes; 110 issues actifs (triage vivant)
- [x] Documentation — README + godoc + openapi3filter examples
- [x] Real-world usage — oapi-codegen, Kong, F5, nombreux gateways
- [x] Readable end-to-end — ~12 kLOC, layered (loader/schema/filter)
- [x] Justified by need — le catalogue ne couvrait pas la couche contrat API ;
      NOT popularity

## Minimal use

```go
doc, _ := openapi3.NewLoader().LoadFromData(spec) // []byte du spec
doc.Validate(ctx)                                  // validation de la spec
// Validation de requête à chaud : openapi3filter.ValidateRequest(...)
```

Compilé et vérifié (LoadFromData + Validate) avec v0.146.0 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `oapi-codegen` (watch list) | Génération de code client/serveur : outil, pas bibliothèque ; attendre v3 stable ; kin-openapi reste le socle. |
| `swaggo/swag` | Génération de spec depuis annotations — complémentaire (sens inverse : code → spec). |
| stdlib + validation manuelle | Perd le contrat OpenAPI exécutable (spec = source de vérité) ; kin-openapi rend le contrat vérifiable. |
| `pb33f/libopenapi` | Alternative émergente, moins éprouvée dans l'écosystème Go. |

## Security note

- Historique : **4 advisories, tous corrigés** — GHSA-wq9g-9vfc-cfq9 /
  GO-2025-3533 (data amplification, fix 0.131.0) ; GHSA-jpcw-4wr7-c3vq
  (nil-pointer panic, fix 0.144.0) ; **GHSA-r277-6w6q-xmqw (Fail-Open
  Authentication Bypass — `ValidationHandler.Load()` avec
  `NoopAuthenticationFunc` par défaut, fix 0.144.0)**.
  **Épingler ≥ 0.144.0** ; v0.146.0 sain (vérifié 2026-08-05, OSV).
- Le défaut fail-open de `ValidationHandler` est un piège de conception :
  configurer un authentificateur explicite (voir
  `pattern:antipattern:sec-fail-open`).

## Utiliser cette librairie quand

- Le contrat OpenAPI 3 est la source de vérité d'une API (chargement,
  validation de spec, validation runtime des requêtes/réponses).
- Construire un middleware de validation générique sur un serveur `net/http`
  ou chi.
- Vérifier la conformité d'un spec avant de générer du code client.

## Ne pas utiliser cette librairie quand

- Besoin de génération de code client/serveur : `oapi-codegen` (en
  surveillance) ou un générateur dédié.
- Swagger 2.0 (non supporté en 3.x moderne) : convertir d'abord.
- Validation de schémas JSON génériques sans OpenAPI : un validateur JSON
  schema dédié suffit.

## Avantages

- OpenAPI 3.0 + 3.1, loader robuste, validation complète (chemins, schémas,
  requêtes).
- `openapi3filter` : validation runtime de requêtes/réponses dans le pipeline
  HTTP (net/http et chi).
- Maintenu très activement (releases quasi quotidiennes, 220 contributeurs).
- Interopère avec l'écosystème contrat (oapi-codegen consomme ses types).

## Inconvénients

- 4 advisories de sécurité depuis 2025 (fixes rapides mais surface d'erreur
  réelle) : épingler les versions, suivre les releases.
- Pas de fuzzing déclaré (scorecard 4.3) ; pas de génération de code.
- API riche : `openapi3filter` demande une configuration attentive
  (authentification, options de validation).

## Pièges connus

- **Fail-open par défaut** : `ValidationHandler` n'authentifie pas sauf
  configuration explicite (GHSA-r277-6w6q-xmqw) — toujours définir
  `AuthenticationFunc` ou rejeter les requêtes non authentifiées en amont.
- Payloads compressés amplifiés (fix 0.131.0) : borner la taille des corps
  avant validation.
- Nil-pointer panic sur paramètres `content` sans schéma (fix 0.144.0) :
  épingler ≥ 0.144.0.
- Versionnage rapide : les types changent entre releases mineures — épingler
  une version exacte et tester à chaque bump.

## Sources vérifiées

- [getkin/kin-openapi (repo officiel, v0.146.0)](https://github.com/getkin/kin-openapi)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/getkin/kin-openapi](https://pkg.go.dev/github.com/getkin/kin-openapi)
  — vérifié 2026-08-05
- [Advisory GHSA-r277-6w6q-xmqw (fail-open auth, fix 0.144.0)](https://github.com/getkin/kin-openapi/security/advisories/GHSA-r277-6w6q-xmqw)
  — vérifié 2026-08-05 (sécurité officielle)
- [Advisory GHSA-jpcw-4wr7-c3vq (nil-ptr, fix 0.144.0)](https://github.com/getkin/kin-openapi/security/advisories/GHSA-jpcw-4wr7-c3vq)
  — vérifié 2026-08-05 (sécurité officielle)
- OSV : 4 advisories pour `github.com/getkin/kin-openapi`, tous corrigés
  ≤ 0.144.0 (requête API 2026-08-05)
- Artefacts internes : `pattern:antipattern:sec-fail-open`,
  `pattern:http:middleware-chain`, catalog `chi`
