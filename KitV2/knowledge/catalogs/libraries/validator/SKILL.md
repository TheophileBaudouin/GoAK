---
name: validator
description: "go-playground/validator — struct validation via tags (validate:\"required,email\"). Use when validating input structs at trust boundaries, registering custom rules, or producing structured field errors."
category: library
tags: [validation, struct, tags, input]
last-verified: 2026-08-02
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
