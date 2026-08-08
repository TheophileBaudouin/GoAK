# Pi integration

This directory contains the native Pi runtime surface of the installed Kit.

- `settings.json` loads product modules through paths relative to `.pi/`:
  `../rules` and `../recipes` (always-visible skill surface: rules and
  runnable procedures). Library fiches (`../knowledge/catalogs`) are routed
  on demand via `search_kit_resources` instead of being listed in every
  prompt — this keeps the always-visible surface small so rules stay
  salient. The UI SDK (`../ui-kit/skills`) is deliberately NOT listed here:
  it is a separate routing corpus (see `search_ui_kit_resources`) and stays
  inert for non-Wails projects.
- `prompts/` contains manually invoked workflow and checklist orchestrators
  (`/checklist-api`, `/checklist-release`, `/workflow-memory`) and the
  `/goak` entry point, which orders the agent to read the shipped user guide
  (`docs/GOAK.md`) instead of answering from memory.
- `skills/` contains durable workflow procedures loaded by context.
- `extensions/` contains the read-only semantic resource routers (`search_kit_resources`
  for Go, `search_ui_kit_resources` for the ui-kit SDK zone), the onboarding
  banner extension (`kit-onboarding.ts`), and their editor-only runtime type
  declarations. The two routing corpora never mix: the Go tool only reads
  `router/`, the UI tool only reads `ui-kit/`.
- `docs/` contains the consumer user guide (`GOAK.md`) — the shipped source
  of truth for how to use the kit; it works with no other documentation and
  is not dependent on the build repository.
- `onboarding/` contains the banner content (`banner.md`) rendered by the
  onboarding extension at session start: Get Started, new large feature,
  new small feature. It is orientation only, never a second documentation.

The installed product is self-contained: these paths resolve after the
installer strips the repository prefix and places the kit at the consumer root.
Consumer projects create their own `.pi/memory/`; no consumer history ships
with this product.
