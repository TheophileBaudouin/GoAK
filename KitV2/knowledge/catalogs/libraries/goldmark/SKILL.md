---
name: goldmark
description: "github.com/yuin/goldmark v1.8.5 — extensible CommonMark 0.31.2 parser and renderer for Go. Use for controlled Markdown parsing or HTML/AST pipelines; not for rendering untrusted HTML without sanitization or for terminal output."
category: library
tags: [markdown, commonmark, parsing, rendering, goldmark, extension]
last-verified: 2026-08-05
---

# goldmark — parser Markdown CommonMark

## Selection

[`github.com/yuin/goldmark`](https://github.com/yuin/goldmark) v1.8.5 is a
zero-dependency, extensible CommonMark 0.31.2 parser with an AST and renderer
interfaces. It is admitted for this focused parsing/rendering boundary, active
maintenance, tests, fuzzing, and real use in documentation systems, not for
popularity. The v2 line is still beta; production code should pin v1.8.5.

## Admission checklist

- [x] Current stable v1.8.5 and Go 1.22+.
- [x] Single responsibility: Markdown parsing, AST, extensions, and rendering.
- [x] CommonMark conformance tests, CI, documentation, and fuzzing exist.
- [x] Extension interfaces support GFM and application-specific AST/renderers.
- [x] The security boundary is explicit: raw HTML and URL policy remain caller
      decisions.

## Minimal use

```go
func renderMarkdown(input []byte) ([]byte, error) {
    var out bytes.Buffer
    if err := goldmark.New().Convert(input, &out); err != nil {
        return nil, fmt.Errorf("convert markdown: %w", err)
    }
    return out.Bytes(), nil
}
```

Add `extension.GFM` through `goldmark.New` when the consumer needs GFM tables,
strikethrough, or task lists. The output policy must be chosen separately from
parsing.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `bluemonday` | Sanitizer, not a parser; combine it with goldmark for untrusted HTML output. |
| `glamour` | Choose for terminal Markdown rendering; goldmark remains the parser/AST boundary. |
| `gomarkdown/markdown` | Consider when its dialect/API is required; verify maintenance independently. |
| Regex rendering | Rejected: it cannot provide CommonMark correctness or safe URL/HTML policy. |

## Utiliser cette librairie quand

- A Go service needs CommonMark parsing, HTML output, an AST, or targeted GFM
  extensions.
- The application needs custom AST transforms or renderer visitors.
- Input trust and output sanitization can be made explicit at the boundary.

## Ne pas utiliser cette librairie quand

- Untrusted Markdown is rendered without sanitization and safe HTML/URL policy.
- The target is terminal output: use Glamour for the terminal renderer.
- A different Markdown dialect is required but no compatible extension exists.
- The project wants the unstable v2 beta API in a production contract.

## Avantages

- Zero direct dependencies and tested CommonMark conformance.
- Extensible AST and renderer interfaces instead of regex or string rewriting.
- GFM and focused extensions can be selected without adopting a full framework.

## Inconvénients

- Raw HTML and dangerous-link policy require deliberate configuration and
  downstream sanitization for untrusted content.
- v2 beta is a future breaking boundary; extensions must be tested on upgrades.
- It does not provide templates, terminal rendering, or application metadata
  management.

## Pièges connus

- Use a patched release (v1.7.17 or later); current v1.8.5 addresses the
  historical HTML-rendering XSS advisory.
- Do not equate parsing with sanitization: apply a trusted HTML policy and a
  sanitizer such as bluemonday for untrusted content.
- Avoid `html.WithUnsafe()` unless raw HTML and dangerous URLs are explicitly
  part of the trusted content contract.
- Pin v1.8.5 and test third-party extensions while v2 remains beta.

## Sources vérifiées

- [Official goldmark repository](https://github.com/yuin/goldmark) — API,
  maintenance, license, checked 2026-08-05.
- [goldmark on pkg.go.dev](https://pkg.go.dev/github.com/yuin/goldmark) — API,
  CommonMark and extension behavior, checked 2026-08-05.
- [goldmark releases](https://github.com/yuin/goldmark/releases) — v1.8.5
  stable and v2 beta status, checked 2026-08-05.
- [GO-2026-5320 advisory](https://pkg.go.dev/vuln/GO-2026-5320) — historical
  HTML-rendering XSS and fixed release, checked 2026-08-05.
- [GitHub advisory](https://github.com/advisories/GHSA-c97m-vxhj-p7j6) —
  security details, checked 2026-08-05.
