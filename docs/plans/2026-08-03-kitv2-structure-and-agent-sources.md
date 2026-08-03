# KitV2 Structure and Agent Sources Plan

**Goal:** Align the standalone `KitV2/` product with the requested structural surfaces while preserving its existing Pi-native resources and canonical artifact locations, and record the two supplied repositories as sources for prompt/skill research.

**Constraints:** Keep one canonical body per artifact; do not copy external repository content into the kit; do not ship consumer memory or metaproject history; preserve existing runnable recipes, probes, and templates.

## Changes

1. Add the requested structural category directories inside `KitV2/` as explicit empty markers or indexes where the existing product has no canonical artifact yet.
2. Move the product validator into `KitV2/tools/validators/` and update active product references.
3. Keep product metadata in `KitV2/manifest.yaml` and `KitV2/capabilities.yaml`; do not add `KitV2/.agent/`, because that path is reserved for metaproject governance and the native runtime surface remains `.pi/`.
4. Remove local cache and subagent artifacts from the working tree.
5. Record the supplied strict source registry and the two explicitly requested repository source records under the metaproject `.agent/sources/`; do not ship them as KitV2 content.
6. Run structural/product validation and obtain an independent read-only review before completion.
