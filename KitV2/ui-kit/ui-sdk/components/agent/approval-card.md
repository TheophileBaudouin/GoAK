# approval-card

| | |
| --- | --- |
| Registry | ui-agent-kit (first-party) |
| License | MIT |
| Source | in-house — see `patterns/agent-chat.md` |
| Category | component (agent) |

Human-approval gate for sensitive agent actions (command execution, file modification,
external action): Accept / Deny buttons, optional decision shortcuts (allow-once,
allow-always…) and a `busy` state while the decision is processed. Built on the frozen
base `Button`.

## Dependencies

- Frozen base (consumer): `@/components/ui/button`, `@/lib/utils`
- npm: `lucide-react`

## Usage

```tsx
import { ApprovalCard } from "@/components/agent/approval-card"

<ApprovalCard
  title="Run `npm install` in the current project?"
  description="Downloads and installs ~200 packages."
  toolName="run_command"
  busy={sending}
  onApprove={() => respondToApproval({ approved: true })}
  onDeny={() => respondToApproval({ approved: false })}
/>
```

> Backend wiring: assistant-ui tool part → `respondToApproval`; Vercel AI SDK →
> `toolApproval` + `addToolApprovalResponse` (see `docs/patterns/agent-chat.md`).
> In a Thread, `AgentChat` renders this card automatically when a tool part carries a
> pending server-side approval gate.
