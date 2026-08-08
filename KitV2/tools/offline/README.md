# Offline source resolver

This tool resolves bounded, pinned official Go sources and local toolchain
capabilities from the self-contained bundle under `bundle/`. It is product
runtime code, not an evidence store or a network client.

## Inputs and outputs

- `manifest.go` and `bundle/manifest.json` define the pinned source units,
  checksums, licenses, and attribution.
- `search.go`, `excerpt.go`, and `offline.go` provide bounded lookup and
  excerpts without external network access.
- `toolchain.go` and `version.go` resolve local Go documentation and version
  metadata.
- `offline_test.go` verifies checksums, lookup boundaries, misses, and
  truncation behavior.

## Verification

Run `go test ./tools/offline/...` for mechanical checks and
`go run ./probes/offline` for the observable consumer scenario. The probe must
finish with `offline: PASS`; it does not claim to cover network retrieval or
unbundled documentation.
