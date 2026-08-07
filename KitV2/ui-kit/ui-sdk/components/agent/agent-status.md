# agent-status

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

Shared vocabulary of the agent chat kit: the `AgentStatus` union
(`idle | thinking | planning | executing | waiting_approval | completed | error`), the
`StepStatus` union for timeline steps, and a11y labels. Pure module — no UI, no
assistant-ui dependency. Every agent component consumes this contract.

## Dependencies

- None (TypeScript only)

## Usage

```ts
import { AGENT_STATUS_LABELS, type AgentStatus } from "@/components/agent/agent-status"
```

> The status lifecycle mirrors the Vercel AI SDK agent patterns (streaming, tool calling,
> human approval) — see `patterns/agent-chat.md` for the mapping.
