---
name: compress
description: "github.com/klauspost/compress v1.19.1 — pure-Go zstd, S2, gzip/flate, and related codecs. Use when a benchmark or format requirement justifies more than stdlib compression; not for unsupported formats, unbounded decompression, or encryption."
category: library
tags: [compression, zstd, s2, gzip, flate, performance]
last-verified: 2026-08-05
---

# compress — codecs compression Go

## Selection

[`github.com/klauspost/compress`](https://github.com/klauspost/compress) v1.19.1,
released 2026-07-20, provides pure-Go codec packages for zstd, S2, gzip/flate,
zlib, zip, huff0, and FSE. It is admitted for focused codec choice, active
maintenance, tests/fuzzing, and real production use; stdlib remains the default
when compatibility and measured performance do not require this dependency.

## Admission checklist

- [x] Current v1.19.1 release and Go 1.24+.
- [x] Single responsibility: compression codecs and related I/O helpers.
- [x] Pure Go with extensive tests, CI, benchmarks, and fuzzing.
- [x] Subpackages expose familiar `io.Reader`/`io.Writer` boundaries.
- [x] Real use in MinIO, Grafana, VictoriaMetrics, and other Go systems.

## Minimal use

```go
func compressZstd(data []byte) ([]byte, error) {
    var out bytes.Buffer
    writer, err := zstd.NewWriter(&out)
    if err != nil {
        return nil, fmt.Errorf("create zstd writer: %w", err)
    }
    if _, err := writer.Write(data); err != nil {
        _ = writer.Close()
        return nil, fmt.Errorf("write zstd data: %w", err)
    }
    if err := writer.Close(); err != nil {
        return nil, fmt.Errorf("close zstd writer: %w", err)
    }
    return out.Bytes(), nil
}
```

Choose a codec/subpackage for a format and benchmark the real workload. Use a
bounded input/output policy around every decompressor; compression is not
confidentiality.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `compress/gzip`/`flate` | Prefer for standard gzip/flate interoperability when no measured gain is required. |
| `github.com/klauspost/pgzip` | Separate module for parallel gzip; choose only when the workload justifies it. |
| Brotli/lzma/lz4 packages | Choose the library that owns the required format; this module does not implement every format. |
| Encryption | Use `age` or a transport security layer; compression is not encryption. |

## Utiliser cette librairie quand

- zstd or S2 is required in a pure-Go Go service.
- A benchmark shows a meaningful ratio, latency, or throughput gain over stdlib.
- The project needs one of the module's supported codecs and can pin/scan its
  dependency.

## Ne pas utiliser cette librairie quand

- Stdlib gzip/flate already satisfies interoperability and performance.
- The required format is Brotli, LZMA, or another codec not supplied here.
- Untrusted compressed input cannot be bounded for memory/output amplification.
- The requirement is encryption, integrity policy, or key management.

## Avantages

- Pure Go and broad codec coverage behind familiar I/O APIs.
- zstd/S2 implementations with benchmarks and production adoption.
- Subpackage selection keeps a chosen codec's surface smaller than the whole
  module.

## Inconvénients

- The module is broad; each codec has its own format and operational behavior.
- New releases can change performance and memory characteristics.
- Some formats and parallel helpers are separate modules or packages.

## Pièges connus

- Pin v1.18.7 or later: the historical S2 dictionary advisory affects older
  versions; v1.19.1 is the current checked version.
- Match framed S2 streams with `s2.NewReader`; do not pass them to block APIs.
- Bound decompressed output and memory for untrusted input.
- Test truncation and interoperability: upstream tracks zstd EOF masking and
  frame-size edge cases.
- Do not manually parallelize a codec whose writer already owns its state.

## Sources vérifiées

- [Official compress repository](https://github.com/klauspost/compress) — API,
  maintenance, license, checked 2026-08-05.
- [v1.19.1 release](https://github.com/klauspost/compress/releases/tag/v1.19.1)
  — exact version and changes, checked 2026-08-05.
- [compress on pkg.go.dev](https://pkg.go.dev/github.com/klauspost/compress) —
  supported packages, checked 2026-08-05.
- [S2 advisory](https://github.com/klauspost/compress/security/advisories/GHSA-259r-337f-4rfw)
  — fixed version and impact, checked 2026-08-05.
- [OSV GO-2026-5841](https://osv.dev/vulnerability/GO-2026-5841) — structured
  vulnerability record, checked 2026-08-05.
- [zstd issue #1128](https://github.com/klauspost/compress/issues/1128) —
  truncation behavior, checked 2026-08-05.
