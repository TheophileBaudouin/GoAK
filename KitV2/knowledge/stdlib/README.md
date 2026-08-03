# Official Go source routing

These entries are pointer-only routing metadata. They do not copy official
reference bodies. Resolve a source pointer through the complete offline bundle
when one is shipped, or through the local Go toolchain in a consumer project.

These entries are graph metadata, not source bodies. The standalone product
ships `tools/offline/` with its manifest, resolver, pinned Effective Go bundle,
and attribution. Resolution is offline by default: an unavailable unit returns
`blocked`; it is never reconstructed from model memory. `pkg.go.dev` and
Toolchain units resolve through the pinned local Go toolchain; Effective Go
resolves through the shipped content-addressed bundle.
