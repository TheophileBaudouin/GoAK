# Pi integration

This directory contains the native Pi runtime surface of the installed Kit.

- `settings.json` loads product modules through paths relative to `.pi/`:
  `../rules` and `../recipes` (always-visible skill surface: rules and
  runnable procedures). Library fiches (`../knowledge/catalogs`) are routed
  on demand via `search_kit_resources` instead of being listed in every
  prompt — this keeps the always-visible surface small so rules stay
  salient.
- `prompts/` contains manually invoked workflow and checklist orchestrators.
- `skills/` contains durable workflow procedures loaded by context.
- `extensions/` contains the read-only semantic resource router and its
  editor-only runtime type declarations.

The installed product is self-contained: these paths resolve after the
installer strips the repository prefix and places KitV2 at the consumer root.
Consumer projects create their own `.pi/memory/`; no consumer history ships
with this product.
