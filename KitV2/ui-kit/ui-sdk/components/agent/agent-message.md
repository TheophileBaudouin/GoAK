# agent-message

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

Assistant message variant with agent metadata: avatar, agent name and a per-message
`ThinkingIndicator` (derived from the assistant-ui message status), plus the message
**action bar** (copy / reload / export as Markdown) and **branch picker** — parity with the
reference thread's assistant message. Part rendering mirrors the reference thread:
grouped reasoning, grouped tool calls, markdown text, registered tool UIs and the kit's
`AgentToolCallUI` fallback (tool cards + approvals).

## Dependencies

- npm: `@assistant-ui/react`, `lucide-react`
- assistant-ui base: `@/components/assistant-ui/markdown-text`, `reasoning`, `tool-group`
- Kit: `./agent-status`, `./thinking-indicator`, `./tool-call-ui`

## Usage

```tsx
// Default in AgentChat — override a single thread:
import { AgentChat } from "@/components/agent/agent-chat"

<AgentChat components={{ AssistantMessage: MyMessage }} />
```
