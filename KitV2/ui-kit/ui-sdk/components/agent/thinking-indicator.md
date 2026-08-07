# thinking-indicator

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

Status pill showing the agent lifecycle: idle · thinking · planning · executing ·
waiting_approval · completed · error. Icon + label always travel together (WCAG 1.4.1),
spins while in progress, announces via `role="status"` when live.

## Dependencies

- Frozen base (consumer): `@/components/ui/badge`, `@/lib/utils`
- npm: `lucide-react`

## Usage

```tsx
import { ThinkingIndicator } from "@/components/agent/thinking-indicator"

// Controlled mode (any external agent runtime):
<ThinkingIndicator status={agent.status} />

// Thread mode (assistant-ui runtime present):
const status = useAgentStatus()
<ThinkingIndicator status={status} />
```

> Also available as a `data-status` attribute hook on the badge for custom styling.
