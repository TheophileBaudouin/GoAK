---
description: Clarify a non-trivial Go project request into a behavior-first specification before planning or coding. Use at the start of new work or when requirements are ambiguous.
argument-hint: "[request]"
---

# Clarify — produce the specification, not code

Do not create or modify application code. Convert the request into a short,
plain-language specification that a non-programmer can verify.

## Goal

State who needs what outcome and why. Use observable verbs: run, click, send,
see, save, export, receive.

## Context

Inspect only the minimum existing files needed to understand the request. Record
relevant recipes, entry points, interfaces, data already present, and constraints.
Do not paste whole files into the specification.

## Constraints

List inputs, outputs, error behavior, persistence, security/trust boundaries,
platform/runtime limits, compatibility requirements, and explicit exclusions.
Mark each item as confirmed, assumed, or unknown.

## Done when

Define acceptance criteria as concrete scenarios:

- Given a starting state,
- when the user runs a command or performs an action,
- then a visible result occurs.

Use a default-fail list: each criterion starts `PENDING`, never `PASS`.
Ask only questions whose answers would change behavior, architecture, or risk.
If no question is necessary, state assumptions explicitly and continue.

End with a `Clarify complete` block containing the specification, open questions,
assumptions, acceptance criteria, and the next artifact path. No implementation
plan or code belongs in this step.
