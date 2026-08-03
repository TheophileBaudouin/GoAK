# Retrieval contract

The product resolver implements `goretrieval/1`.

- Network is disabled by default (`GOPROXY=off`, `GOTOOLCHAIN=local`).
- `pkg-doc` and `toolchain` use the pinned local Go toolchain (`go doc`,
  `go help`, and known GOROOT command source paths).
- `effective-go` uses the shipped content-addressed bundle pinned by commit and
  verified by SHA-256.
- Every response includes source, unit, status, bounded matches, and provenance.
- `hit` means content was found and verified; `miss` means an indexed unit or
  blob failed; `stale` means the requested version does not match; `blocked`
  means the exact prerequisite is unavailable.
- Retrieval is metadata-first and deterministic. It never loads all sources or
  reconstructs missing knowledge from model memory.
- `Online=true` is an explicit opt-in and is never used by product workflows.

The bundle includes Go project attribution and license text. Refresh pins and
all referencing metadata atomically; do not update one source record alone.
