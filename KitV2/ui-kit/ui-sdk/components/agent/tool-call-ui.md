# tool-call-ui

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

The assistant-ui tool-part renderer of the kit (`ToolCallMessagePartComponent`):
pending approval gate → `ApprovalCard` responding through `respondToApproval`; running /
requires-action call → `ToolCallCard`; completed call → `ToolCallCard` + `ToolResult`.
Used as the `ToolFallback` slot by `AgentChat` and `AgentMessage`.

## Dependencies

- npm: `@assistant-ui/react`
- Kit: `./approval-card`, `./tool-call`, `./tool-result`

## Usage

```tsx
// Wired automatically by AgentChat — override per tool name with a registered
// tool UI (makeAssistantToolUI) when a tool deserves a custom rendering.
```

> The `approval` mapping follows the assistant-ui server-side approval gate
> (`respondToApproval`) — the Vercel AI SDK `toolApproval` flow maps onto it.
