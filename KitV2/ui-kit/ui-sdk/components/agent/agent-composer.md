# agent-composer

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

Status-aware message composer: shows the agent `ThinkingIndicator` above the input while
the agent is active, swaps Send ↔ Stop while a run is in flight, and keeps the
frozen-base keyboard contract (Enter to send, Shift+Enter newline, Escape stops — handled
by `ComposerPrimitive`).

## Dependencies

- npm: `@assistant-ui/react`, `lucide-react`
- Frozen base (consumer): `@/components/ui/button`, `@/lib/utils`
- Kit: `./thinking-indicator`, `./use-agent-status`

## Usage

```tsx
// Custom layout (split view, embedded chat card) — the default Thread composer
// is already wired inside AgentChat.
import { AgentComposer } from "@/components/agent/agent-composer"

<AgentComposer placeholder="Ask the agent…" />
```
