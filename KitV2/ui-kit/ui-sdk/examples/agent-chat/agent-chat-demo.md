# agent-chat-demo

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party example) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | example |

Interactive demo of the agent chat kit, buildable **without a backend**: a mock
assistant-ui runtime (`useExternalStoreRuntime` + a scripted reasoning → tool call →
result → answer sequence) drives the Thread, and a side gallery shows every pure
component (statuses, approval card, tool call/result, execution timeline, artifact
preview). Wired into the app as a consumer would — the reference for `AgentChat`.

## Dependencies

- npm: `@assistant-ui/react`, `lucide-react`
- Kit: `@/components/agent/*` (the whole agent kit)

## Usage

```tsx
import { AgentChatDemo } from "@/components/example-agent/agent-chat-demo"

<AgentChatDemo />
```

> Swap `useMockAgentChat` for a real runtime (Vercel AI SDK via
> `@assistant-ui/react-ai-sdk`, LangGraph, or a custom transport) — the screen
> itself stays unchanged.
