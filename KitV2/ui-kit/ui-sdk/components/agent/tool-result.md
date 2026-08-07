# tool-result

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

Output of a finished tool call: success/error state + pretty-printed JSON, or a custom
`children` renderer (e.g. a chart or table built from the result). Presentational and
dependency-free.

## Dependencies

- Frozen base (consumer): `@/lib/utils`
- npm: `lucide-react`

## Usage

```tsx
import { ToolResult } from "@/components/agent/tool-result"

<ToolResult toolName="analyze_data" result={stats} />
<ToolResult toolName="run_command" isError result={error} />
```

> In a Thread, `AgentChat` renders `ToolResult` under the matching `ToolCallCard` when a
> tool call completes. Use it directly for external agent runtimes.
