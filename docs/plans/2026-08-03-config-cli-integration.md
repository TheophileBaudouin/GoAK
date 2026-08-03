# Configuration and CLI integration — points 3 and 4

## Goal

Integrate the source registry's high-priority Viper, Koanf, and Cobra entries
into the existing Go Agent Kit without replacing the stdlib-first defaults or
creating duplicate knowledge.

## Owner decision

The owner explicitly authorized **real dependencies** for this wave. This
permits `go.mod`, `go.sum`, the offline module allowlist, product catalogs,
recipes, coverage metadata, and validation updates.

## Existing architecture preserved

- `recipe-cli-minimal` remains the canonical single-command/flat-flag solution.
- Koanf's existing catalog remains the canonical configuration comparison and
  selection record.
- Viper is an alternative configuration implementation, not a replacement for
  the Koanf decision.
- Cobra is used only for multi-command CLIs where subcommands, completion, and
  generated help justify the dependency.
- `.agent/` remains source governance; `.pi/` remains load-on-demand runtime;
  KitV2 receives only product artifacts and tests.
- Official source bodies are not copied into recipes or skill bodies.

## Minimal product additions

- Add Viper and Cobra library catalogs; refresh Koanf catalog provenance.
- Add runnable, tested recipes:
  - `recipe-config-viper`
  - `recipe-config-koanf`
  - `recipe-cli-cobra`
- Add direct dependencies required by those recipes.
- Add module allowlist entries and checksums through the existing Go module and
  offline resolver path.
- Update product skill/recipe coverage metadata and validator expectations.
- Add graph metadata YAML for the new recipes/capabilities/evaluations only if
  required by existing product relationship validation; do not duplicate bodies.

## Source decisions

- Viper v1.21.0: singleton-free `viper.New()`, explicit precedence, config
  decoding, environment binding; document case-insensitive keys and
  non-concurrent read/write limitations.
- Koanf v2.3.5: modular providers/parsers, explicit cascade, case-sensitive
  keys, strict merge option; use v2 module path and separate provider/parser
  modules.
- Cobra v1.10.2: command tree, `RunE`, `ExecuteC`, persistent/local flags,
  required/mutually exclusive validation, generated help and completion;
  avoid `CheckErr` in testable code.
- No official `llms.txt` exists for these libraries; the metaproject source
  registry records official URLs and bounded source-cache units instead.

## Dependencies

1. Fetch and verify official source metadata.
2. Add Go modules and confirm checksums.
3. Implement recipes and tests.
4. Add catalog/metadata projections and coverage updates.
5. Update offline module allowlist and offline probe.
6. Run complete validation and fresh review.

## Risks

- Dependency growth: mitigated by explicit owner approval and narrow recipes.
- Viper/Koanf duplication: mitigated by separate selection boundaries and shared
  configuration concepts kept in the existing Koanf catalog.
- Cobra global state and `os.Exit`: mitigated by `NewCommand` factories,
  `RunE`, and `ExecuteC` tests.
- Offline module availability: module paths are allowlisted and validation
  runs with local cache/offline settings; missing caches return blocked.
- Published skill count changes from 28 to 33; this is authorized by the
  owner and updated atomically with capabilities and validator expectations.

## Done

- All new recipes compile and run tests.
- Product and metaproject validators pass.
- `GOPROXY=off` probes pass with all new module allowlist entries available.
- Full Go/security/vulnerability gate passes.
- Fresh reviewer confirms no duplicate canonical body or broken product boundary.
