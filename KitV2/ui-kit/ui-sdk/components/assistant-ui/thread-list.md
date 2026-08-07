# thread-list

| | |
| --- | --- |
| Registry | @assistant-ui (official shadcn registry) |
| License | MIT |
| Source | <https://github.com/assistant-ui/assistant-ui> · <https://r.assistant-ui.com/thread-list.json> |
| Category | component (assistant-ui) |

Conversation history sidebar: new thread, search, date-grouped items (Today / Yesterday /
Earlier), running indicator, rename / archive / delete via a more-menu, skeleton loading
state. Built on `ThreadListPrimitive` + the frozen base (`Button`, `Input`, `Skeleton`).
The **conversation history** piece of the agent chat kit — pair it with `AgentChat` in a
desktop split layout (sidebar + chat).

## Dependencies

- Frozen base (consumer): `@/components/ui/button`, `@/components/ui/input`,
  `@/components/ui/skeleton`
- assistant-ui base: `@/components/assistant-ui/tooltip-icon-button`
- npm: `@assistant-ui/react`, `lucide-react`

## Usage

```tsx
import { ThreadList } from "@/components/assistant-ui/thread-list"

// Inside an AssistantRuntimeProvider with a thread-list-capable runtime
// (AI SDK cloud threads, LangGraph, or a custom ExternalStore thread list):
<div className="flex h-[600px]">
  <aside className="w-64 border-r p-2">
    <ThreadList />
  </aside>
  <div className="flex-1">
    <AgentChat />
  </div>
</div>
```

> Requires a runtime that exposes threads (`s.threads`): `useChatRuntime` with cloud
> threads, LangGraph, or a custom thread-list adapter. The single-thread external-store
> mock used by the example renders one item.
