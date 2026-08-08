# [PROJECT_NAME] Constitution

> Ratified: [RATIFICATION_DATE] · Version [CONSTITUTION_VERSION] · Last
> amended: [LAST_AMENDED_DATE]

This constitution is the governing foundation of this project. Every agent
and developer reads it before feature work; the `workspace-init` session
wrote it, amendments follow the Governance section below.

## Mission

[MISSION — one paragraph: what the project does, for whom, and the
constraint that matters most (platform, deployment, team, timeline).]

## Core Principles

### [PRINCIPLE_1_NAME]

[PRINCIPLE_1_DESCRIPTION — a declarative, testable non-negotiable rule with
its rationale when not obvious. One paragraph or a short bullet list.]

### [PRINCIPLE_2_NAME]

[PRINCIPLE_2_DESCRIPTION]

### [PRINCIPLE_3_NAME]

[PRINCIPLE_3_DESCRIPTION]

### [PRINCIPLE_4_NAME]

[PRINCIPLE_4_DESCRIPTION]

### [PRINCIPLE_5_NAME]

[PRINCIPLE_5_DESCRIPTION]

The project adopts the kit's sourced rules by default (error wrapping,
naming, zero-value design, doc-comments, testing, channel ownership —
routed via `search_kit_resources`). The principles above are the
project-specific non-negotiables **on top**; they never relax a kit rule.

## Architecture Mandate — kernel first

This project is framed as **one kernel + peripheral modules**
(Microkernel / Plugin architecture — Mark Richards, *Fundamentals of
Software Architecture*):

- The **kernel** is the minimal core: shared contracts/types, bootstrap
  and lifecycle, and cross-cutting concerns ([LIST: config, logging,
  errors, command/event bus, injection point]). It contains **zero feature
  logic**.
- **Modules** are peripheral components that depend only on the SDK
  exposed by the kernel — never directly on each other, except through a
  contract carried by the kernel.
- The **SDK** is the kernel's public interface, deliberately small (deep
  module — John Ousterhout, *A Philosophy of Software Design*), documented
  as doc-commented exported API with executable examples. The SDK and its
  documentation grow in the same commit.

The concrete boundary — what lives in the kernel, the module list, and the
SDK plan — is captured in `ARCHITECTURE.md`, which is part of this
constitution by reference.

## Stack Decisions

- [STACK_DECISION_1 — toolchain/language level, with justification]
- [STACK_DECISION_2 — persistence / transports / libraries, justified
  against the kit catalog or a dated research note]
- [STACK_DECISION_3 — build/run/deploy constraints that shape the
  boundary]

## Testing Policy

[TESTING_POLICY — test-first by default; every module black-box at its
public API, isolated from the other modules; which test layers protect
what; fakes over mocks. A regression in one module must never fail
another's tests.]

## Governance

- **Guidance file**: `AGENTS.md` (Project Foundation section) and this
  file are the binding surfaces; `ARCHITECTURE.md` is the living boundary
  document.
- **Amendment procedure**: any change to a Core Principle or the
  Architecture Mandate is recorded as an amendment here and as a decision
  in `decisions/D-YYYY-MM-DD-NN.md`; `CONSTITUTION_VERSION` follows
  semantic versioning — MAJOR for principle removal/redefinition, MINOR for
  new principles or materially expanded guidance, PATCH for wording.
- **Compliance review**: every non-trivial feature work must be consistent
  with the constitution and the boundary in `ARCHITECTURE.md`; a feature
  that crosses the boundary is a constitution change, not a code shortcut.
