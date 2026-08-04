---
name: mcp-go-sdk
description: "github.com/modelcontextprotocol/go-sdk v1.7 — official Go SDK for the Model Context Protocol (client, server, resources, prompts, tools, auth, streams). Use when building MCP servers or clients (agent tool interop with Claude, IDEs, other agents) and you want the reference implementation maintained with the MCP spec."
category: library
tags: [mcp, protocol, agent, tools, llm, interoperability]
last-verified: 2026-08-04
---

# mcp-go-sdk — Model Context Protocol (official)

## Selection

[`github.com/modelcontextprotocol/go-sdk`](https://github.com/modelcontextprotocol/go-sdk)
(v1.7.0, Go 1.25+, ~4.9k★, pushed 2026-08-04).

**Why it passes the gate** (actual reason, not stars): the **official** Go
implementation of the Model Context Protocol, maintained in collaboration with
Google, tracking the spec (multiple protocol versions supported). It provides
client and server packages with typed `resources`, `prompts`, `tools`, JSON-RPC
transport, auth, and streaming — the interoperability standard for agent
ecosystems (Claude Code, IDEs, multi-agent). Single responsibility (the MCP
protocol), idiomatic Go, active releases (v1.7.0, 2026).

## Admission checklist

- [x] Actively maintained — v1.7.0 (2026-08), regular versioned releases
- [x] Single responsibility — MCP protocol (client + server)
- [x] Idiomatic Go — typed APIs, context-aware
- [x] Tests present + CI — yes
- [x] Documentation — README, spec-aligned docs, examples
- [x] Real-world usage — the reference SDK for MCP in Go
- [x] Readable end-to-end — yes, compact protocol core
- [x] Justified by need — agent interop requires a standard; MCP is it

## Minimal use (server)

```go
server := mcp.NewServer(mcp.ServerOptions{})
// register tools, resources, prompts; serve over stdio or streamable HTTP
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Hand-rolled JSON-RPC over stdio/HTTP | Reinvents the spec, breaks interop; not justified. |
| coder/websocket as raw transport | Transport layer only — the SDK is the protocol layer; websocket remains a valid transport *under* MCP. |

## Notes

- Issue-mined (417 issues): roadmap tracking (#328, 80r) and session
  recovery proposals (#148) — pin exact versions; the SDK is pre-1.0-era
  API-stable but still evolving (see roadmap).
- MCP is the interop layer for the agent direction of this kit (Claude
  Code–compatible tooling); catalog admission, recipe only once a runnable
  consumer scenario exists.
