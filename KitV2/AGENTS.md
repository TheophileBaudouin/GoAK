# Go Agent Development Kit

KitV2 is the standalone consumable Go agent kit.

## Source of truth

- `rules/` — agent rules and principles.
- `knowledge/` — sourced product indexes and decision context; it must not duplicate rule or recipe bodies or metaproject history.
- `recipes/` — runnable Go recipes, tests, and procedure documents.
- `snippets/` — metadata-bearing, focused examples linked to a canonical recipe or rule.
- `templates/` — runnable project bases or explicitly labelled partial contracts.
- `probes/` — product-facing runnable verification scenarios, including the offline retrieval probe.
- `tools/offline/` — stdlib-only resolver, manifest, pinned source bundle, and attribution files.
- `.pi/` — native Pi settings, prompt templates, and skills loaded after trust.

If two files answer the same question, keep one canonical answer and replace the other with a pointer. The source registry never overrides the kit charter or these rules; source-derived content remains subject to evidence and validation gates.

## Workflow

Use the native `.pi/prompts/` workflow templates in order for non-trivial work.

## Validation

From `KitV2/` run:

```sh
python3 tools/validators/validate-kitv2.py
go test ./...
test -z "$(gofmt -l .)"
go vet ./...
```

Run `bash probes/run.sh` separately. The local kit gate also runs
`golangci-lint`, `gosec`, and `govulncheck`; if a consumer environment lacks a
required tool, report the gate as `PARTIAL`, never as passing.

## Limits

Always preserve errors, cancellation, input validation, and observable evidence. Ask before adding dependencies or changing the manifest contract. Never claim an unexecuted scenario passed or treat static checks as proof of user intent.
