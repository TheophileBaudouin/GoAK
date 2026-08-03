# Go Agent Kit Engineering Charter

## 0. Purpose & Authority

This charter is the governing authority of the Go Agent Kit.

The Go Agent Kit is **not** a documentation repository. It is a **cognitive operating system for code agents**, designed to maximize deterministic reasoning, reusable knowledge, and production-quality code generation.

Every artifact contained within the kit exists to improve an agent's ability to:

* Understand
* Decide
* Generate
* Validate
* Learn

The following artifact types are governed by this charter:

* Rules
* Recipes
* Patterns
* Snippets
* Templates
* Capabilities
* Evaluations
* Decision Records
* Sources
* Memory

This charter is the single process authority.

If any artifact conflicts with this charter, the artifact is incorrect and must be updated. The charter is never overridden by a lower-level artifact.

---

# 1. Design Philosophy

The Go Agent Kit is built around one fundamental principle:

> An agent should never invent knowledge that the kit can explicitly provide.

Therefore:

* Knowledge is preferred over prompting.
* Reusable assets are preferred over repeated instructions.
* Composition is preferred over duplication.
* Deterministic behavior is preferred over creativity.
* Observable validation is preferred over assumptions.

The objective is not to make the agent "smarter", but to make it **more reliable, reproducible, and predictable**.

---

# 2. Knowledge Graph Architecture

The Go Agent Kit is not organized as a collection of folders.

It is a **typed knowledge graph**.

Each artifact is an explicit knowledge object with a defined role, metadata, dependencies, and relationships.

The primary object types are:

* **Rule** — Permanent constraints governing architecture, coding standards, validation, security, or quality.
* **Recipe** — Ordered procedures describing how to accomplish a repeatable task.
* **Pattern** — Reusable architectural or design solutions.
* **Snippet** — Production-ready implementation fragments.
* **Template** — Complete project skeletons assembled from other artifacts.
* **Capability** — A declared ability of the agent (REST, gRPC, Kafka, CLI, PostgreSQL, etc.).
* **Evaluation** — Executable validation procedures and observable acceptance criteria.
* **Decision Record** — Historical architectural decisions and rationale.
* **Source** — Official documentation, specifications, RFCs, or maintained reference implementations.
* **Memory** — Persistent project-specific knowledge that does not belong in operational artifacts.

Every object must possess:

* a stable identifier
* explicit metadata
* defined relationships
* a single responsibility

Supported relationships include, but are not limited to:

* `depends_on`
* `uses`
* `implements`
* `extends`
* `references`
* `requires`
* `supersedes`
* `validated_by`
* `generated_from`

The knowledge graph—not the folder hierarchy—is the authoritative representation of the kit.

---

# 3. Cognitive Layers

Every artifact belongs to exactly one cognitive layer.

## Layer 1 — Rules

Rules define permanent constraints.

Rules answer:

> What must always be true?

Rules include:

* architecture policies
* coding standards
* validation requirements
* security requirements
* review policies

Rules never contain implementation details.

Rules remain stable over time.

---

## Layer 2 — Recipes

Recipes define repeatable workflows.

Recipes answer:

> How is this task performed?

Examples include:

* Create REST API
* Add PostgreSQL
* Add JWT Authentication
* Create Worker
* Configure OpenTelemetry
* Publish Docker Image

Recipes are procedural.

---

## Layer 3 — Patterns

Patterns describe reusable architectural solutions.

Patterns answer:

> Which design should be selected?

Examples include:

* Repository Pattern
* Worker Pool
* Fan-Out/Fan-In
* Graceful Shutdown
* CQRS
* Event Bus
* Dependency Injection

Patterns are implementation-agnostic.

---

## Layer 4 — Snippets

Snippets provide production-ready implementations.

Every snippet must include:

* metadata
* dependencies
* supported Go version
* usage constraints
* tests

Snippets answer:

> How is this implemented?

A snippet without validation is incomplete.

---

## Layer 5 — Templates

Templates assemble complete projects.

Examples include:

* REST Service
* CLI
* Worker
* gRPC Service
* Shared Library

Templates are composed from Recipes, Patterns, and Snippets.

Templates never duplicate implementation.

---

## Layer 6 — Evaluations

Evaluations verify generated solutions.

Every evaluation contains:

* validation commands
* expected behavior
* observable scenario
* acceptance criteria

Evaluations never explain implementation.

They measure correctness.

---

## Layer 7 — Memory

Memory records historical knowledge.

Memory stores:

* architectural decisions
* rejected alternatives
* migration history
* project-specific rationale

Memory never defines operational behavior.

---

# 4. Single Source of Truth

Every piece of knowledge exists exactly once.

Examples:

* Validation commands belong only in Rules.
* Graceful shutdown implementation belongs only in Snippets.
* Repository Pattern belongs only in Patterns.
* REST API bootstrap belongs only in Recipes.
* Historical decisions belong only in Decision Records.
* Official references belong only in Sources.

Duplication is a defect.

Whenever two artifacts can answer the same question, at least one is incorrect.

---

# 5. Metadata First

Every reusable artifact must be machine-readable.

Minimum metadata:

```yaml
id:
title:
kind:
version:
status:
owner:
tags:
go_version:
dependencies:
last_verified:
```

Optional metadata:

```yaml
framework:
database:
cloud:
complexity:
maturity:
references:
capabilities:
relationships:
```

Agents discover artifacts through metadata, never through filenames.

---

# 6. Evidence Before Inclusion

No artifact is added because it "seems useful."

Every artifact must originate from one of the following:

* Official documentation
* RFC or specification
* Maintained reference implementation
* Observed production failure
* Proven community standard

Every artifact records its sources.

Unsupported knowledge belongs in research, not in the operational kit.

---

# 7. Composition Over Duplication

Large solutions are assembled from reusable knowledge.

They are never copied.

The composition hierarchy is:

```
Template
    ↓
Recipe
    ↓
Pattern
    ↓
Snippet
```

Each layer composes lower layers.

No layer duplicates another.

---

# 8. Deterministic Generation

Equivalent inputs should produce equivalent outputs.

Therefore:

* Rules must be deterministic.
* Recipes must be ordered.
* Snippets must be self-contained.
* Templates must be reproducible.
* Evaluations must be executable.

Hidden assumptions are defects.

Implicit behavior is forbidden.

---

# 9. Validation

Every executable artifact must be validated.

Validation includes, when applicable:

* dependency verification
* formatting
* static analysis
* linting
* testing
* race detection
* vulnerability scanning
* observable runtime behavior

Compilation alone is insufficient.

Passing tests alone is insufficient.

Observable behavior must satisfy the evaluation criteria.

---

# 10. Progressive Knowledge

Knowledge grows only after evidence.

The lifecycle of reusable knowledge is:

```
Problem
    ↓
Research
    ↓
Decision
    ↓
Pattern
    ↓
Snippet
    ↓
Recipe
    ↓
Template
    ↓
Evaluation
```

Knowledge must not skip stages.

---

# 11. Agent Independence

Every artifact must be understandable in isolation.

No artifact may depend upon prior conversation or hidden context.

Cross-references are permitted.

Hidden dependencies are prohibited.

An agent loading a single artifact must possess sufficient information to use it correctly.

---

# 12. Versioning

Artifacts evolve independently.

Breaking changes require:

* version increment
* migration documentation
* updated evaluations

Deprecated artifacts remain available until all dependent artifacts have migrated.

---

# 13. Knowledge Relationships

Relationships between artifacts are first-class citizens.

Every relationship must be explicit.

Examples include:

* Rule validates Snippet
* Recipe uses Pattern
* Template assembles Recipes
* Capability requires Rules
* Evaluation validates Template
* Decision Record references Sources

Relationships are never inferred from folder structure.

---

# 14. Quality Gates

An artifact is accepted only if:

* Metadata is complete.
* Sources are recorded.
* Relationships are declared.
* Validation passes.
* No duplicated knowledge exists.
* Composition rules are respected.
* The artifact improves reuse.
* The artifact can be independently consumed by an agent.

---

# 15. Definition of Done

A change is complete only when:

* Every affected evaluation passes.
* Metadata is complete and current.
* Sources are recorded.
* Relationships are updated.
* No duplicate knowledge has been introduced.
* Dependent recipes remain valid.
* Templates remain reproducible.
* The knowledge graph remains internally consistent.
* The change increases the overall reusability and determinism of the kit.

---

# 16. Core Principles

Every contribution to the Go Agent Kit must respect these principles:

1. Knowledge over prompting.
2. Composition over duplication.
3. Determinism over creativity.
4. Evidence over opinion.
5. Validation over assumptions.
6. Machine-readable before human-readable.
7. Stable identifiers over file paths.
8. Explicit relationships over implicit structure.
9. Reusable knowledge over project-specific instructions.
10. Continuous evolution driven by observed evidence.

These principles are immutable unless this charter itself is formally revised.
