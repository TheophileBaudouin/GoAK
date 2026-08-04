---
name: validator
description: "go-playground/validator — struct validation via tags (validate:\"required,email\"). Use when validating input structs at trust boundaries, registering custom rules, or producing structured field errors."
category: library
tags: [validation, struct, tags, input]
last-verified: 2026-08-04
---

# validator — struct validation

## Selection

`go-playground/validator` (20k★, pushed 2026-07, CI + coverage, default validator
for the Gin framework — real-world adoption).

**Actual reason (not stars):** declarative, tag-driven struct validation that
centralises input rules at the type boundary, with structured `FieldError`
output you can translate into user-facing messages.

⚠ **Maintenance watch:** the README carries a "call for maintainers" note.
Admission holds today (active, CI green), but re-verify at the kit's next
`last-verified` cycle — flag this in Gotchas.

## Core usage

```go
type Signup struct {
    Email    string `json:"email"    validate:"required,email"`
    Password string `json:"password" validate:"required,min=8"`
    Age      int    `json:"age"      validate:"gte=18"`
}

v := validator.New()
err := v.Struct(signup) // nil or validator.ValidationErrors
```

Use `validator.New()` as a **singleton** — it caches parsed struct/tag metadata.
It is goroutine-safe for `Validate`, NOT for `RegisterValidation` (register once
at init).

## Custom rules + structured errors

```go
v.RegisterValidation("slug", func(fl validator.FieldLevel) bool {
    s := fl.Field().String()
    return slugRegexp.MatchString(s) // your check
})

// translate errors
var errs validator.ValidationErrors
if errors.As(err, &errs) {
    for _, fe := range errs {
        // fe.Field(), fe.Tag(), fe.Value(), fe.Namespace() — build the message YOU expose
    }
}
```

## Security note (don't leak internals)

`FieldError.Namespace()` and `.Value()` can expose internal struct paths and the
raw submitted value. Map to user-facing messages yourself; never echo
`Value()`/`Namespace()` to an untrusted client (could leak field names or PII).

## Alternatives considered

| Alternative | Verdict |
|---|---|
| hand-rolled `if` checks | Correct for ≤2-3 fields; tag validation wins as rules multiply. |
| `asaskevich/govalidator` | Older, string-based validators; validator's struct-tag model is cleaner. |
| OpenAPI/protobuf-generated validation | If your schema is the source of truth, generate from it instead of hand-tagging. |

## Utiliser cette librairie quand

- Valider des structs à la frontière de confiance (payloads HTTP, args CLI,
  appels d'outils) avec des règles déclaratives par tags.
- Des règles custom (`RegisterValidation`) et des erreurs structurées
  (`ValidationErrors` → messages utilisateur) sont nécessaires.
- La validation se multiplie au-delà de 2-3 champs (les `if` manuels perdent).

## Ne pas utiliser cette librairie quand

- Peu de champs (≤2-3) : des `if` manuels suffisent.
- Le schéma est la source de vérité (OpenAPI/protobuf) : générer la
  validation depuis le schéma plutôt que re-tagger à la main.
- La stratégie de validation sémantique (métier, cross-champs) est le vrai
  besoin : les tags sont syntaxiques (voir
  `source:security:input-validation`).

## Avantages

- Validation déclarative tag-driven, centralisée à la frontière de type.
- Erreurs structurées (`FieldError`) traduisibles en messages utilisateur.
- Adoption réelle (validator par défaut de Gin, 20k★).
- Cache des métadonnées : `validator.New()` en singleton, goroutine-safe pour
  `Validate`.

## Inconvénients

- **⚠ Maintenance watch** : appel à mainteneurs sur le README — re-vérifier au
  prochain cycle `last-verified` (Gotcha).
- Validation par réflexion : coût par champ à mesurer sur les chemins chauds.
- Tags syntaxiques seulement : la sémantique métier reste du code manuel.

## Pièges connus

- Singleton `validator.New()` (cache) ; `RegisterValidation` au init
  uniquement (pas goroutine-safe).
- Ne JAMAIS exposer `FieldError.Namespace()`/`.Value()` à un client non
  fiable (fuite de noms de champs/PII) — mapper vous-même les messages.
- Les slices/maps imbriquées ne sont PAS validées sans `dive` (issue #952).
- Les CVE historiques signalées étaient des dépendances transitives
  (golang.org/x/text, corrigées) — garder govulncheck dans la gate.

## Sources vérifiées

- [go-playground/validator (repo officiel)](https://github.com/go-playground/validator)
  — vérifié 2026-08-02
- [pkg.go.dev/github.com/go-playground/validator/v10](https://pkg.go.dev/github.com/go-playground/validator/v10)
  — vérifié 2026-08-04
- [Issue #952 — dive sur slices](https://github.com/go-playground/validator/issues/952)
  — vérifié 2026-08-04 (issue officielle)
- [Issue #899 — CVE-2021-38561 (x/text transitif)](https://github.com/go-playground/validator/issues/899)
  et [PR #881 — fix x/text](https://github.com/go-playground/validator/pull/881)
  — vérifiées 2026-08-04 (issues officielles)
- Artefact interne : `source:security:input-validation` (stratégie frontière)
