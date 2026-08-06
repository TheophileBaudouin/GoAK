---
name: recipe-openapi-validation
description: "Validate a startup-loaded embedded OpenAPI document plus bounded net/http requests and buffered responses with a required non-noop AuthenticationFunc. Use when OpenAPI is an executable API contract; not for streaming, hijacking, unbounded bodies, generated code, or fail-open authentication."
category: recipe
tags: [openapi, validation, api, http, contract, security]
last-verified: 2026-08-05
---

# recipe-openapi-validation — executable HTTP contract

## Purpose and use cases

Load and validate an embedded OpenAPI document at startup, then validate the
request **and** the response of a `net/http` handler. The middleware bounds
bodies, resolves the route, requires a real `AuthenticationFunc`, and only
lets a response out after validating its status, headers, and body.

Use when OpenAPI is the API's real contract. The contract is not a generator
and does not replace the business authentication decision.

## Prerequisites and architecture

- `Config.Spec` comes from `go:embed` or from bytes controlled at startup.
- `AuthenticationFunc` is mandatory and `NoopAuthenticationFunc` is rejected.
- `MaxBodyBytes` bounds both the request and the response buffer.
- The `400`, `413`, and `500` error responses must be present in the document,
  as in `openapi.yaml`, with a stable generic shape.

The recipe uses kin-openapi's legacy router and its filter validator. It does
not use `ValidationHandler`, whose pinned version does not validate responses.
This justifies the small local adapter over a duplicated incomplete middleware.

## Components and choices

- `github.com/getkin/kin-openapi v0.146.0` — `kin-openapi` catalog; OpenAPI 3
  parsing, route matching, and validation.
- `openapi3filter.ValidateRequest`/`ValidateResponse` — contract at input and
  at output.
- bounded buffer — an invalid or oversized response becomes a generic
  contract-conformant error; its content and the validator's detail are not
  disclosed.

## Rejected alternatives

- `ValidationHandler`: rejected because it still carries `TODO: validateResponse`.
- `NoopAuthenticationFunc`, a missing callback, or fail-open: rejected.
- Request-only validation: lets the API violate its contract on output.
- Streaming, `Hijacker`, `Flusher`, WebSocket, and bodies beyond the limit:
  incompatible with fully buffered validation.

## Example

```go
validator, err := openapivalidation.New(context.Background(), openapivalidation.Config{
	Spec: openapivalidation.ExampleSpec, MaxBodyBytes: 1 << 20,
	AuthenticationFunc: func(ctx context.Context, input *openapi3filter.AuthenticationInput) error {
		return verifyBearer(ctx, input.RequestValidationInput.Request.Header.Get("Authorization"))
	},
})
if err != nil {
	return err
}
handler := validator.Middleware(appHandler)
```

## Good practices and pitfalls

- Validate the document at startup: an invalid contract prevents the service
  from starting.
- Define in the document every status/header emitted by the handler.
- Keep limits proportionate; compressed payloads and large objects require a
  separate upload recipe.
- Never include the body, token, or validation detail in the client error or
  the invalid-response logs.

## Limits and extensions

The legacy router does not cover every path/extension form; test the
contract's real routes. No streaming, hijacking, metric export,
client/server generation, or business authorization. These needs change the
boundary and require a dedicated recipe.

## Observable scenario and verification

```sh
go test ./recipes/recipe-openapi-validation/...
go run ./probes/openapi-validation
```

The probe validates an authenticated `POST /widgets` and a `201` response,
then prints `openapi-validation: PASS`. The tests prove an invalid request, a
masked invalid response, and an oversized body.

## Primary sources

- [kin-openapi openapi3filter](https://pkg.go.dev/github.com/getkin/kin-openapi/openapi3filter)
  — validation inputs and authentication function.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — contract
  for operations, responses, and security requirements.

