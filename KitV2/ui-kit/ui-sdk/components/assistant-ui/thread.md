# thread

| | |
| --- | --- |
| Registry | @assistant-ui (official shadcn registry) |
| License | MIT |
| Source | <https://github.com/assistant-ui/assistant-ui> · <https://r.assistant-ui.com/thread.json> |
| Category | component (assistant-ui) |

Chat container with message list, composer, auto-scroll, attachments and accessibility
built in. The entry point of the agent chat base: conversation display, streaming,
reasoning, tool groups and follow-up suggestions are wired here. Rendering slots
(`AssistantMessage`, `Welcome`, `ToolFallback`, `ToolGroup`, `ReasoningGroup`) can be
overridden via the `components` prop — the agent components (`components/agent/`) plug in
there.

## Dependencies

- Frozen base (consumer): `@/components/ui/button`, `@/lib/utils`
- assistant-ui base: `@/components/assistant-ui/attachment`, `follow-up-suggestions`,
  `markdown-text`, `reasoning`, `tool-fallback`, `tool-group`, `tooltip-icon-button`
- npm: `@assistant-ui/react`, `lucide-react`, `react`

## Usage

```tsx
import { Thread } from "@/components/assistant-ui/thread"

// Requires an assistant-ui Runtime (AssistantRuntimeProvider) — see
// docs/patterns/agent-chat.md and the agent-chat example screen.
export function Chat() {
  return (
    <div className="h-full">
      <Thread />
    </div>
  )
}
```

> Needs the assistant-ui runtime + a data source (AI SDK, LangGraph, custom transport, or
> the external-store mock). The agent components (`AgentChat`, `AgentMessage`…) extend this
> base with agent state, tool call cards, approvals and artifact previews.
> `@import "tw-shimmer"` must be added to the consumer's CSS for the shimmer dot styles.
> See `patterns/agent-chat.md` for the integration.
