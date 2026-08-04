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

## Utiliser cette librairie quand

- Construire un serveur ou client MCP (interop avec Claude, IDEs, agents) et
  vouloir l'implémentation de référence maintenue avec la spec.
- Exposer des `tools`, `resources`, `prompts` typés avec transport JSON-RPC
  (stdio, HTTP streamable) et auth.
- L'interopérabilité agentique standardisée prime (pas un protocole maison).

## Ne pas utiliser cette librairie quand

- Un simple JSON-RPC maison suffit pour un cas isolé (mais il casse
  l'interop).
- Le besoin est uniquement un transport WebSocket : `coder/websocket` est le
  transport, le SDK est la couche protocole.
- Aucun écosystème MCP cible : le protocole ajoute de la complexité.

## Avantages

- SDK **officiel** du MCP, maintenu avec Google, aligné spec (plusieurs
  versions de protocole).
- Client + serveur, resources/prompts/tools typés, JSON-RPC, auth, streaming.
- Standard d'interop des écosystèmes d'agents (Claude Code, IDEs, multi-agent).
- Releases régulières (v1.7.0, 2026-08), API Go idiomatique context-aware.

## Inconvénients

- Écosystème pré-1.0-era : l'API est stable mais évolue encore (roadmap
  #328, session recovery #148) — épingler les versions exactes.
- Protocole riche : coût d'apprentissage et de configuration réel pour un
  usage simple.
- Pas encore de recette kit exécutable (scénario consommateur à établir).

## Pièges connus

- Pinner la version exacte (l'API peut bouger entre releases ; issue-mining
  #328/#148).
- Traiter chaque primitive (tools/resources/prompts) comme une frontière de
  confiance : l'entrée du modèle est non fiable (voir
  `source:mcp:tool-security` — OWASP LLM Top 10).
- Structurer le serveur selon la spec (host/client/server, primitives,
  transport) — voir `pattern:architecture:mcp-server-shape`.

## Sources vérifiées

- [modelcontextprotocol/go-sdk (repo officiel, v1.7.0)](https://github.com/modelcontextprotocol/go-sdk)
  — vérifié 2026-08-04
- [Spec MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)
  — vérifié 2026-08-04 (spec officielle)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
  — vérifié 2026-08-04
- Artefacts internes : `pattern:architecture:mcp-server-shape`,
  `source:mcp:tool-security`, catalog `coder-websocket`
