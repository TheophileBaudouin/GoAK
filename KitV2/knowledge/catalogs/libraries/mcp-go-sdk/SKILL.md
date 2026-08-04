---
name: mcp-go-sdk
description: "github.com/modelcontextprotocol/go-sdk v1.7.0 — official Go SDK for Model Context Protocol clients and servers, including tools, resources, prompts, auth, and stdio/streamable HTTP transports. Use for MCP interoperability; not for hand-rolled JSON-RPC or raw WebSocket transport."
category: library
tags: [mcp, protocol, agent, tools, llm, interoperability]
last-verified: 2026-08-05
---

# mcp-go-sdk — SDK MCP officiel

## Selection

[`github.com/modelcontextprotocol/go-sdk`](https://github.com/modelcontextprotocol/go-sdk)
v1.7.0, released 2026-07-28, is the official Go SDK for the Model Context
Protocol. It provides typed clients/servers and protocol transports while
tracking the evolving MCP specification. It is admitted for standard agent
interoperability, active maintenance, tests, documentation, and real use; not
for popularity.

## Admission checklist

- [x] Current stable v1.7.0, Go 1.25+, and active upstream releases.
- [x] Single responsibility: MCP protocol client/server implementation.
- [x] Typed tools, resources, prompts, JSON-RPC, auth, and transports.
- [x] Tests, CI, protocol documentation, and security advisories are maintained.
- [x] The official SDK boundary is distinct from a raw WebSocket transport.

## Minimal use

```go
func newServer() *mcp.Server {
    return mcp.NewServer(&mcp.Implementation{Name: "goak", Version: "1"}, nil)
}
```

Register tools/resources/prompts and serve through the transport selected by the
MCP contract. Treat every tool argument and resource request as untrusted input;
validate it at the server boundary and define authorization separately.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `mark3labs/mcp-go` | Viable independent SDK with a different API and transport model; compare protocol-version support before choosing. |
| `coder/websocket` | Transport only; it does not implement MCP messages or lifecycle semantics. |
| Hand-written JSON-RPC | Rejected for interoperable MCP: it duplicates protocol versioning and security work. |
| No MCP | Prefer a simpler private API when no MCP client/host ecosystem is required. |

## Utiliser cette librairie quand

- A Go client or server must interoperate with MCP hosts, IDEs, or agents.
- The application exposes tools, resources, or prompts through the protocol.
- Standard MCP transports, auth, and protocol negotiation are required.

## Ne pas utiliser cette librairie quand

- The requirement is only raw WebSocket or JSON-RPC transport.
- No MCP host/client ecosystem is part of the product contract.
- A private local protocol is simpler and interoperability has no value.
- The project cannot pin and re-test an evolving protocol SDK.

## Avantages

- Official Go implementation aligned with the current MCP specification.
- Client and server APIs for tools, resources, prompts, auth, and transports.
- Typed context-aware boundaries make validation and cancellation explicit.
- Recent security fixes and protocol revisions are released upstream.

## Inconvénients

- MCP is a rich protocol with a meaningful learning/configuration cost.
- The specification and SDK evolve rapidly; exact version pinning is required.
- Protocol revision changes can affect transports and lifecycle assumptions.
- The SDK does not decide application authorization or tool safety policy.

## Pièges connus

- Pin v1.7.0 or later and read the matching protocol revision before integrating.
- Validate tool inputs, resource identifiers, prompt arguments, and output sizes;
  model-controlled input is a trust boundary.
- Do not assume every transport supports every protocol revision; verify stdio
  and streamable HTTP behavior against the selected spec.
- Track the SDK's documented rough edges and protocol-version negotiation issues
  during upgrades.
- Never expose a tool merely because it compiles: define authorization,
  capability, timeout, and audit policy separately.

## Sources vérifiées

- [Official Go SDK repository](https://github.com/modelcontextprotocol/go-sdk)
  — API, maintenance, license, checked 2026-08-05.
- [v1.7.0 release](https://github.com/modelcontextprotocol/go-sdk/releases/tag/v1.7.0)
  — exact version and protocol changes, checked 2026-08-05.
- [SDK package documentation](https://pkg.go.dev/github.com/modelcontextprotocol/go-sdk)
  — package boundaries, checked 2026-08-05.
- [MCP protocol documentation](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/protocol.md)
  — implementation/protocol mapping, checked 2026-08-05.
- [SDK rough edges](https://github.com/modelcontextprotocol/go-sdk/blob/main/docs/rough_edges.md)
  — known limitations, checked 2026-08-05.
- [JSON key advisory](https://github.com/modelcontextprotocol/go-sdk/security/advisories/GHSA-wvj2-96wp-fq3f)
  — fixed security boundary, checked 2026-08-05.
- [Origin/tool execution advisory](https://github.com/modelcontextprotocol/go-sdk/security/advisories/GHSA-89xv-2j6f-qhc8)
  — HTTP trust boundary, checked 2026-08-05.
- [DNS rebinding advisory](https://github.com/modelcontextprotocol/go-sdk/security/advisories/GHSA-xw59-hvm2-8pj6)
  — HTTP server protection, checked 2026-08-05.
