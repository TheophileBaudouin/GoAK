# use-agent-status

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | hook (agent) |

Reactive agent lifecycle status of the current assistant-ui thread. Derives
`thinking` / `executing` / `waiting_approval` / `completed` / `error` / `idle` from
streaming state, running tool parts and pending approval gates. The pure
`deriveAgentStatus` function is exported for external agent runtimes.

## Dependencies

- npm: `@assistant-ui/react`

## Usage

```tsx
import { useAgentStatus } from "@/components/agent/use-agent-status"
import { ThinkingIndicator } from "@/components/agent/thinking-indicator"

const status = useAgentStatus() // requires AssistantRuntimeProvider
<ThinkingIndicator status={status} />
```

> `planning` is a semantic stage the agent reports itself — it is not observable
> from a thread; pass it as a controlled `status` prop where applicable.
