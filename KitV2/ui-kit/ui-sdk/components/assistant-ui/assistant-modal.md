# assistant-modal

| | |
| --- | --- |
| Registry | @assistant-ui (official shadcn registry) |
| License | MIT |
| Source | <https://github.com/assistant-ui/assistant-ui> · <https://r.assistant-ui.com/assistant-modal.json> |
| Category | component (assistant-ui) |

Chat-in-a-popover launcher (bottom-right floating button opening a full Thread): the
classic AI-copilot pattern — "ask the assistant" from anywhere without leaving the
current screen. Built on `AssistantModalPrimitive` + the harvested `Thread`.

## Dependencies

- assistant-ui base: `@/components/assistant-ui/thread`, `tooltip-icon-button`
- npm: `@assistant-ui/react`, `lucide-react`

## Usage

```tsx
import { AssistantModal } from "@/components/assistant-ui/assistant-modal"

// Inside an AssistantRuntimeProvider — one instance per app:
<AssistantModal />
```

> The modal reuses the standard `Thread` (conversation, streaming, tool groups,
> attachments). For agent-specific rendering inside the modal, pass a `Thread` variant —
> or wrap it with the kit's `AgentChat`-style components via `components`.
