---
name: kin-openapi
description: "github.com/getkin/kin-openapi v0.146.0 — OpenAPI 3 parsing, schema validation, and runtime HTTP request/response validation. Use when an OpenAPI contract is executable; not for code generation or fail-open authentication defaults."
category: library
tags: [api, openapi, openapi3, validation, spec, rest]
last-verified: 2026-08-05
---

# kin-openapi — contrat OpenAPI et validation

## Selection

[`github.com/getkin/kin-openapi`](https://github.com/getkin/kin-openapi) v0.146.0,
released 2026-08-03, provides OpenAPI 3 parsing, schema validation, Swagger v2
conversion, and `openapi3filter` request/response validation. It is admitted for
this focused contract boundary, active maintenance, tests, and integration in
Go API tooling; not for popularity and not as a code generator.

## Admission checklist

- [x] Current v0.146.0 with active frequent releases.
- [x] Single responsibility: OpenAPI loading, validation, and HTTP filtering.
- [x] `net/http`-friendly types, tests, CI, documentation, and examples.
- [x] Current release is beyond the documented security-fix boundaries.
- [x] The contract role is distinct from `oapi-codegen` generation.

## Minimal use

```go
func loadSpec(ctx context.Context, spec []byte) (*openapi3.T, error) {
    loader := openapi3.NewLoader()
    doc, err := loader.LoadFromData(spec)
    if err != nil {
        return nil, fmt.Errorf("load OpenAPI document: %w", err)
    }
    if err := doc.Validate(ctx); err != nil {
        return nil, fmt.Errorf("validate OpenAPI document: %w", err)
    }
    return doc, nil
}
```

Use `openapi3filter` separately for runtime request/response validation, and
configure authentication explicitly rather than accepting a default fail-open
path.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `oapi-codegen` | Code generation for clients/servers; complementary, not a replacement for runtime validation. |
| `pb33f/libopenapi` | Consider when source locations, overlays, diffing, and broader OpenAPI versions are primary requirements. |
| `swaggo/swag` | Code-annotation-to-spec generation; different direction from contract loading/validation. |
| Manual JSON/schema checks | Prefer only for a deliberately non-OpenAPI contract; otherwise loses executable OpenAPI semantics. |

## Utiliser cette librairie quand

- An OpenAPI 3 contract is the source of truth for spec and HTTP validation.
- A Go HTTP service needs request/response validation middleware.
- The application needs to load, validate, or convert an OpenAPI document before
  generating or serving an API.

## Ne pas utiliser cette librairie quand

- The actual requirement is client/server code generation.
- A generic JSON Schema validator is sufficient and OpenAPI adds no value.
- Authentication policy can be left implicit or fail-open.
- The project needs broad source-location preservation and libopenapi's diff/
  overlay model instead.

## Avantages

- OpenAPI 3.0/3.1 loading and validation with a standard Go API.
- `openapi3filter` integrates with `net/http` and chi request boundaries.
- Maintained active release stream and a mature Go contract ecosystem.

## Inconvénients

- Rich filter configuration creates security and resource-policy decisions.
- It is not a generator and does not manage authentication or authorization.
- The v0.x API evolves quickly; exact version pinning and upgrade tests matter.
- Parsing is not a substitute for preserving source locations or a full diff
  model when those are required.

## Pièges connus

- Configure `AuthenticationFunc` explicitly; never assume `ValidationHandler`
  authenticates by default.
- Pin v0.146.0 or a later patched release; current advisories include fail-open
  auth, resource amplification, and malformed-input panics fixed in recent
  versions.
- Bound request bodies, compressed payloads, and deep-object query parameters
  before validation.
- Treat validation errors as an HTTP boundary concern and avoid leaking spec or
  internal parser details to clients.

## Sources vérifiées

- [Official kin-openapi repository](https://github.com/getkin/kin-openapi) —
  maintenance, API, license, checked 2026-08-05.
- [v0.146.0 release](https://github.com/getkin/kin-openapi/releases/tag/v0.146.0)
  — exact current version, checked 2026-08-05.
- [kin-openapi on pkg.go.dev](https://pkg.go.dev/github.com/getkin/kin-openapi)
  — package/API boundaries, checked 2026-08-05.
- [Fail-open advisory](https://github.com/getkin/kin-openapi/security/advisories/GHSA-r277-6w6q-xmqw)
  — authentication default and fixed version, checked 2026-08-05.
- [Multipart panic advisory](https://github.com/getkin/kin-openapi/security/advisories/GHSA-mmfr-pmjx-hw9w)
  — malformed input boundary, checked 2026-08-05.
- [Deep-object resource advisory](https://github.com/getkin/kin-openapi/security/advisories/GHSA-xhj3-7xw9-vr34)
  — query resource bound, checked 2026-08-05.
- [Content parameter advisory](https://github.com/getkin/kin-openapi/security/advisories/GHSA-jpcw-4wr7-c3vq)
  — malformed validation input, checked 2026-08-05.
