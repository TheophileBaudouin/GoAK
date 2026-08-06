# Project template catalog

## Policy (owner directive, 2026-08-04)

The Kit's templates are **never written by an agent**. Each template is a
slightly adapted copy of a **real open-source project**:

- **MIT** license (fully open) — mandatory;
- reliable project: maintained, tested, CI, active community;
- **ultra-specific and minimal**: almost exclusively the template's
  technology — one stack, no out-of-scope ancillary technology; small,
  browsable-end-to-end codebase, clear and modular structure (integration by
  copying well-delimited modules, simple modification);
- **single responsibility**, directly reusable with very few modifications;
- conformant to the Kit rules (idiomatic, stdlib-first, no imposed
  framework);
- **functional**: compiles and passes its tests — a non-functional template
  is forbidden;
- minimal Kit adaptations **documented** (diff + reasons);
- attribution: source, pinned version, license, adaptations (including the
  technical scope: one technology, no ancillary technology).

The agent documents and adapts; it does not develop the template. Better
**fewer templates, very high quality**, improved by the community, than
home-made skeletons.

## Current status

The inherited agent-generated scaffolds were removed on 2026-08-05. The
catalog keeps only three real, pinned, MIT, verified projects:

| Template | Status | Source | Scope |
| --- | --- | --- | --- |
| rest-api | sourced | leeprovoost/go-rest-api-template | HTTP REST stdlib-first |
| cli | sourced | danjdewhurst/go-toc | Markdown TOC generation CLI |
| worker | sourced | sangianpatrick/go-workerpool | bounded worker pool |

The `grpc`, `microservice`, `monolith`, `cloud-service`, and `desktop-app`
shapes remain a roadmap without an operational template. `desktop-app` is
covered at recipe + probe level (`recipe-desktop-app`, `probes/desktop-app`)
but no conforming MIT source was found in the 2026-08-05 desktop-app research
(no real single-responsibility Wails application). No scaffold must be
recreated to represent them: a shape without a conforming MIT source stays
planned.

## Admitting a new template (sourced)

1. Identify a real open-source MIT project, **ultra-specific** (one
   technology, no ancillary stack), **minimal** (small, browsable, clear
   modular structure), single-responsibility, conformant to the Kit rules.
2. Pin the version (commit/release) and verify the MIT license.
3. Copy the project into `templates/<shape>/` with `LICENSE`,
   `ATTRIBUTION.md` (source, version, adaptations) and `README.md` (status,
   source, observable scenario).
4. Adapt **minimally** to the Kit; each adaptation is documented in
   `ATTRIBUTION.md` with its reason.
5. Verify: compile, tests, executed and recorded observable scenario
   (`PASS`/`PARTIAL`/`BLOCKED`).
6. Update this catalog and the validator (expected template shape).

The existing recipes remain the canonical implementation evidence for the
shapes that do not yet have a conforming MIT source.
