# Interview framework — the design-tree foundation interview

This file specifies the Phase 3 interview of the `workspace-init` skill. It
adapts the **grilling** primitive (mattpocock/skills — adapted, never
copied verbatim; the source is the skill `skills/productivity/grilling` of
the `mattpocock/skills` repository) to the kernel-first foundation domain.
Read it before the interview and follow it exactly.

## 1. The model: a design tree

Model the subject — the project foundation — as a **design tree**: every
decision branches into the decisions that hang off it.

Example fragment:

```text
Foundation
├── Kernel/modules boundary        ← the root decision
│   ├── Which concerns are cross-cutting (kernel)?
│   ├── Which features become modules?
│   └── What is each module's one-line contract?
├── Stack
│   ├── Language level / toolchain
│   ├── Persistence / transports
│   └── Libraries (justified against the kit catalog)
├── Non-negotiables
│   └── Project-specific rules on top of the kit rules
└── Testing policy
    ├── Test layers per module
    └── Isolation guarantees
```

The four clusters are the trunk. Every other question hangs off one of
them.

## 2. The round, the frontier, who decides

- **Frontier** = every decision whose prerequisites are already settled —
  the questions you can ask now without guessing at answers you have not
  heard yet.
- **Round** = one frontier, asked in full and answered in full. Two
  questions never share a round if one depends on the other.
- **Question format** — each question numbered and titled, body with the
  concrete choices, then your recommended answer alone:

```text
❓ **Q1** — *question title*: question body, including the choices

➡️ your recommended answer
```

The user answers by number ("1 yes, 2 the second option, 3 no — here's
why"). Thirteen questions typically land in about three rounds, not
thirteen.

- **Facts are yours, decisions are the user's.** When a frontier question
  needs a fact from the environment (files, kit index, web), look it up or
  dispatch a sub-agent — never ask the user for anything you could find
  yourself. Do not block on it: a running exploration is an unsettled
  prerequisite, so only the questions downstream of it wait.
- **Recompute after every round.** Settled answers push the frontier
  outward and unblock dependent questions. The next round is recomputed,
  never pre-written.

## 3. The four decision clusters — questions must converge on these

Every question must be justified by what is still missing to decide one of
the four clusters. A question that cannot be traced to a missing decision
is dropped. Concrete shapes to reach for (adapt wording to the project —
these are patterns, not a fixed questionnaire):

### 3.1 Kernel/modules boundary (the root)

- Cross-cutting concerns that must live in the kernel: shared
  contracts/types, bootstrap and lifecycle, config, logging, errors,
  optionally a command/event bus or an injection point. Ask which of these
  the project actually has — do not assume all of them.
- Feature candidates that become modules. Shape each as a one-line
  contract: "Module X owns responsibility R, exposed to other modules
  through contract C, depending only on the kernel SDK."
- The SDK surface: which kernel packages are public (the SDK), which are
  internal (`internal/` per `pattern:go:internal-packages`). A module that
  needs a kernel capability not yet in the SDK is a signal to grow the SDK
  — record it as a decision, do not let the module reach into internals.
- Registry/wiring: how modules are registered and composed at bootstrap
  (init-based registry + `pattern:go:constructor-injection` at a single
  `wire()`/`newApp()` point). Ask only if the project has more than one
  module shape; a single-module project records the boundary and moves on.

### 3.2 Stack

- Language level and toolchain constraints (the kit targets modern Go;
  record the consumer's actual toolchain — do not assume).
- Persistence, transports, and libraries: every pick must be justified
  against the kit catalog (Phase 1) — a library already catalogued is
  decided by pointer, not re-interviewed. Only gaps (uncommon stack,
  platform constraint) are open questions here.
- Build/run/deploy constraints that shape the boundary (single binary vs
  multiple processes, static embedding, offline).

### 3.3 Non-negotiable writing rules

- The kit rules already cover error wrapping, naming, zero-value design,
  doc-comments, channel ownership (the routing tool's default guidelines).
  The interview records only what is **project-specific on top**: license,
  team conventions, legacy constraints, generated-code policy.
- Ask: "Which of these existing rules does this project explicitly adopt
  as non-negotiable, and what does this project add?" — never re-derive
  the kit rules.

### 3.4 Testing policy

- Test-first by default: every module gets a black-box suite at its public
  API (`pattern:testing:blackbox-package-tests`), isolated from the other
  modules — the explicit objective is that a regression in one module
  never fails another's tests.
- Which test layers protect what: unit (pure logic via
  `pattern:testing:seam-injection`), integration (through the kernel
  contracts), observable scenario (probes/recipe bar).
- Fakes over mocks (`pattern:testing:fakes-over-mocks`); when a mock
  framework is genuinely justified (unstable interface), record it.

## 4. Termination

The session is done when the **frontier is empty**: every branch of the
design tree visited, nothing left silently assumed. Then stop and ask the
user to confirm the shared understanding **before any write** (Phase 4
restitution). An empty frontier without the user's confirmation is not
completion.

## 5. Pitfalls

- **The agent answering its own decisions** — the surrounding task ("set
  up the foundation") reads as licence to keep moving; it is not. Facts
  are found, decisions are asked.
- **Generic questions** — "what is the architecture?" is a failure; the
  question must name the concrete choices and what the answer settles.
- **Asking for facts** — a version, a capability, a kit entry: look it up.
- **Capping the question count** — there is no cap; the frontier decides.
  If a user prefers one question at a time, honor it (the round-based
  default is an optimization, not a contract).
- **Assuming the four clusters** — a CRUD-utility project may have no
  bus, no registry, no SDK beyond one package. The tree is recomputed per
  project; the clusters are the trunk, not a mandatory checklist of
  artifacts.
