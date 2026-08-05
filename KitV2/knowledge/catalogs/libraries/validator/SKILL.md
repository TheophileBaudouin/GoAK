---
name: validator
description: "github.com/go-playground/validator/v10 v10.30.3 — struct and field validation with tags, cross-field rules, collection diving, and custom validators. Use at Go input boundaries; not as a sanitizer, authorization policy, or replacement for domain validation."
category: library
tags: [validation, input, structs, security, api]
last-verified: 2026-08-05
---

# validator — validation de structures

## Selection

[`github.com/go-playground/validator/v10`](https://github.com/go-playground/validator)
v10.30.3, released 2026-05-29, validates Go structs/fields through tags,
cross-field rules, collection diving, aliases, and custom functions. It is
admitted for explicit input validation, active maintenance, tests, documentation,
and broad Go use; use the versioned `/v10` import path for new projects.

## Admission checklist

- [x] Current stable v10.30.3 and active upstream maintenance.
- [x] Single responsibility: struct/field validation.
- [x] Built-in tags, custom validators, aliases, and collection traversal exist.
- [x] Tests, CI, documentation, and recent security-relevant fixes exist.
- [x] Validation is distinct from sanitization, authorization, and business rules.

## Minimal use

```go
func validateSignup(input Signup) error {
    if err := validate.Struct(input); err != nil {
        return fmt.Errorf("invalid signup: %w", err)
    }
    return nil
}
```

Expose a stable application error shape rather than returning raw field names,
namespace details, or internal values to an untrusted client.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Manual validation | Prefer for a tiny type with one or two invariants; keep domain rules explicit. |
| `ozzo-validation`/other validators | Evaluate when fluent rules or a different error model is required; pin and source independently. |
| JSON Schema/OpenAPI validation | Prefer when the external schema is the source of truth; this package validates Go values. |
| Sanitizer | Separate concern; validation must not be treated as HTML/SQL/path sanitization. |

## Utiliser cette librairie quand

- HTTP, CLI, config, or message inputs map to Go structs with repeatable field
  and cross-field constraints.
- Tags/aliases and collection traversal improve readability without hiding the
  domain policy.
- The application converts validation errors into a stable public response.

## Ne pas utiliser cette librairie quand

- Validation is a single trivial condition or a domain invariant that should be
  visible in a constructor/service.
- Input needs sanitization, canonicalization, authorization, or permission
  checks instead of shape validation.
- The raw validator namespace/value should be exposed to users.

## Avantages

- Large built-in tag set for common shape, network, identifier, and collection
  constraints.
- Custom field/struct validators and aliases support application-specific rules.
- Works on ordinary Go values without imposing an HTTP framework.

## Inconvénients

- Reflection/tag strings can hide rules from ordinary code navigation.
- Validation tags do not define authorization, normalization, or business policy.
- Error translation and public-field mapping remain application responsibilities.
- A broad tag set can encourage over-validation or unstable external contracts.

## Pièges connus

- Validate at the trust boundary, then apply domain invariants again where state
  changes; a tag is not proof of authorization.
- Do not return `Field`, `Namespace`, or `Value` blindly when they reveal secrets
  or internal struct layout.
- Review hostname/FQDN/IP validator behavior and pin current releases; security-
  relevant validation fixes are part of normal upgrades.
- Register custom validators once in an explicit validator instance and test
  them with table-driven cases.

## Sources vérifiées

- [Official validator repository](https://github.com/go-playground/validator) —
  API, maintenance, license, checked 2026-08-05.
- [validator v10 on pkg.go.dev](https://pkg.go.dev/github.com/go-playground/validator/v10)
  — current module and API, checked 2026-08-05.
- [Latest release API](https://api.github.com/repos/go-playground/validator/releases/latest)
  — v10.30.3/version date, checked 2026-08-05.
- [Validator security page](https://github.com/go-playground/validator/security)
  — package-specific advisory status, checked 2026-08-05.
- [Validator README](https://raw.githubusercontent.com/go-playground/validator/master/README.md)
  — tags, custom validation, and support policy, checked 2026-08-05.
