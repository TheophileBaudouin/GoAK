---
description: Turn an approved behavior specification into a minimal, source-backed Go architecture and acceptance plan. Use only after workflow-clarify.
argument-hint: "[clarified specification]"
---

# Plan — choose the smallest design that can prove the behavior

Do not create or modify application code. Read the clarification artifact and
confirm it has no unresolved decision that affects the result. If it does, stop
with `BLOCKED` and return to clarify.

## Goal

Restate the behavior being implemented and the acceptance scenarios that must
pass. Separate required behavior from optional ideas.

## Context

Before reading source bodies, select artifacts by stable ID and tags through the
`go-source-retrieval` skill. Resolve Go API and toolchain claims with the local
resolver (`go doc`, `go help`, or the shipped bundle) and record provenance.

Select an existing kit recipe when it matches. Otherwise justify the smallest
layout and standard-library boundary that fit the behavior. Name only the files,
packages, entry points, and data flow that the implementation actually needs.

## Constraints

Document trust boundaries, error/cancellation behavior, persistence, operational
limits, compatibility, dependencies, and public contracts. For each dependency,
record the simpler option considered and why it is insufficient. Cite primary
documentation for rules and APIs; do not use popularity as evidence.

## Done when

Write an ordered plan where every step has:

- one outcome;
- exact files or interfaces involved;
- a mechanical check;
- a behavior check or evidence artifact;
- a dependency on earlier steps.

Specify the exact command or user action for final verification. Include risks,
rollback/stop conditions, and what a fresh reviewer should challenge.

End with `Plan complete` plus the artifact path and approval request. No code.
