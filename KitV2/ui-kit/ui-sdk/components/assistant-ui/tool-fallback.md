# tool-fallback

| | |
| --- | --- |
| Registry | @assistant-ui (official shadcn registry) |
| License | MIT |
| Source | <https://github.com/assistant-ui/assistant-ui> |
| Category | component (assistant-ui) |

Default rendering for a tool call that has no registered tool UI: name, status
(running / requires-action / complete / error) and collapsible JSON arguments. Used by
`thread.tsx` when no `toolUI` is registered for the tool name.

## Dependencies

- Frozen base (consumer): `@/components/ui/collapsible`
- npm: `@assistant-ui/react`, `lucide-react`, `react`

## Usage

```tsx
import { ToolFallback } from "@/components/assistant-ui/tool-fallback"
// In ThreadComponents or MessagePrimitive.Parts tools.Fallback slot:
<ToolFallback {...part} />
```

> The agent `ToolCallCard`/`ToolResult` components are the SDK's richer replacements —
> pass them via the `ToolFallback` slot of `AgentChat`.
