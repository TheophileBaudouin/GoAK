# agent-chat

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

The agent chat container: assistant-ui `Thread` (conversation, streaming, composer,
attachments, follow-up suggestions — the assistant-ui base, never a home-grown chat)
pre-wired with the agent kit components: `AgentMessage` for assistant messages
(metadata + per-message status) and `AgentToolCallUI` as the tool fallback (tool cards,
results, approval cards). `Welcome`, `ToolGroup`, `ReasoningGroup` keep the assistant-ui
defaults; every slot is overridable via `components`.

## Dependencies

- npm: `@assistant-ui/react` (via the Thread + a runtime)
- assistant-ui base: `@/components/assistant-ui/thread`
- Kit: `./agent-message`, `./tool-call-ui`
- Frozen base (consumer): `@/lib/utils`

## Usage

```tsx
import { AssistantRuntimeProvider } from "@assistant-ui/react"
import { AgentChat } from "@/components/agent/agent-chat"

const runtime = useChatRuntime({ api: "/api/agent" }) // AI SDK, LangGraph, custom…

<AssistantRuntimeProvider runtime={runtime}>
  <div className="h-[600px]">
    <AgentChat />
  </div>
</AssistantRuntimeProvider>
```

> Backend-agnostic: any assistant-ui runtime works (Vercel AI SDK via
> `@assistant-ui/react-ai-sdk`, LangGraph, custom transports, or the
> external-store mock used by the example screen). For a Wails app, expose a
> streaming endpoint from the Go backend or call an external API from the
> frontend — see `docs/patterns/agent-chat.md`.
