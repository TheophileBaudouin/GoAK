# tool-call

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

One tool call in the conversation: tool name, status (running / complete /
requires-action / incomplete / error), collapsible JSON arguments. Built on the frozen
base `Collapsible` + `Badge` primitives.

## Dependencies

- Frozen base (consumer): `@/components/ui/badge`, `@/components/ui/collapsible`,
  `@/lib/utils`
- npm: `lucide-react`

## Usage

```tsx
import { ToolCallCard } from "@/components/agent/tool-call"

<ToolCallCard toolName="search_files" args={{ query: "wails" }} status="running" />
```

> In a Thread, the kit wires it automatically: `AgentChat` maps every tool call part to
> `ToolCallCard` (+ `ToolResult` on completion) through the `ToolFallback` slot.
