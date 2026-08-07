# execution-timeline

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

Vertical execution timeline of an agent run: ordered steps with status icons
(pending / running / complete / error), connector line, optional durations and
descriptions. Status is always icon + text (WCAG 1.4.1 — sr-only label per step).
Presentational.

## Dependencies

- Frozen base (consumer): `@/lib/utils`
- npm: `lucide-react`

## Usage

```tsx
import { ExecutionTimeline } from "@/components/agent/execution-timeline"

<ExecutionTimeline
  steps={[
    { id: "search", title: "Searching the codebase", status: "complete", duration: "0.8s" },
    { id: "edit", title: "Editing files", status: "running" },
    { id: "verify", title: "Running tests", status: "pending" },
  ]}
/>
```

> Pair it with a side panel layout next to `AgentChat` for a "mission control" view —
> see the agent-chat pattern.
