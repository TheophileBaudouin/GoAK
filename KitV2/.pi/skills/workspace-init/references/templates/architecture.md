# [PROJECT_NAME] — Architecture: kernel + modules

Boundary document of this project (part of the constitution by reference).
`CONSTITUTION.md` holds the non-negotiables; this file holds the concrete
boundary and the SDK plan.

> Last updated: [LAST_UPDATED] · Version [ARCHITECTURE_VERSION]

## Kernel

The kernel is the minimal core. It owns:

- **Shared contracts/types** — [LIST: e.g. domain types, error kinds,
  context conventions] in package(s) [PACKAGE_PATHS].
- **Bootstrap and lifecycle** — [LIST: startup, graceful shutdown, wiring]
  at [BOOTSTRAP_PATH].
- **Cross-cutting concerns** — [LIST: config, logging, errors, optional
  command/event bus, injection point] in package(s) [PACKAGE_PATHS].

The kernel contains **zero feature logic**: a feature that needs a kernel
capability extends the SDK (documented, same commit), it never reaches
into kernel internals.

## SDK plan

The SDK is the kernel's public interface — deliberately small, deep
(John Ousterhout, *A Philosophy of Software Design*):

- Public packages (the SDK): [LIST_PACKAGES] — every exported identifier
  doc-commented per the kit `doc-comments` rule, with executable examples
  for the main entry points.
- Internal packages: [LIST_INTERNAL] under `internal/` — importable only
  inside the module (Go compiler enforcement).
- Documentation contract: doc comments + `Example` functions are the
  contract; prose that duplicates code is not written.

## Modules

| Module | One-line contract | Depends on |
| --- | --- | --- |
| [MODULE_1] | [MODULE_1_CONTRACT] | kernel SDK only |
| [MODULE_2] | [MODULE_2_CONTRACT] | kernel SDK only |

Rules: a module depends only on the kernel SDK, never on another module
directly (except through a contract carried by the kernel). A module's
contract is its public API; everything else is its private
implementation.

## Module registry and bootstrap

[REGISTRY_APPROACH — e.g. init-based registry + constructor injection at a
single wire()/newApp() point (kit pattern
`pattern:go:constructor-injection`); how a module registers; how the
kernel composes them; what happens at startup and shutdown.]

## Testing policy per module

- Every module carries a black-box test suite at its public API,
  isolated from the other modules — a regression in one module never fails
  another's tests (kit patterns
  `pattern:testing:blackbox-package-tests`,
  `pattern:testing:seam-injection`, `pattern:testing:fakes-over-mocks`).
- Kernel tests cover the shared contracts and the bootstrap/lifecycle.
- Integration tests cross the kernel contracts, not module internals.

## Boundary rules — never

- No feature logic in the kernel.
- No direct module→module dependency outside a kernel-carried contract.
- No module reaching into kernel internals or another module's internals.
- No exported SDK symbol without a doc comment; no SDK growth without its
  documentation in the same commit.
