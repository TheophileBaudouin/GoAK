# tooltip-icon-button

| | |
| --- | --- |
| Registry | @assistant-ui (official shadcn registry) |
| License | MIT |
| Source | <https://github.com/assistant-ui/assistant-ui> |
| Category | component (assistant-ui) |

Icon button with a tooltip wrapper, used for the composer send/stop actions, the action
bar (copy, refresh) and the scroll-to-bottom button.

## Dependencies

- Frozen base (consumer): `@/components/ui/button`, `@/components/ui/tooltip`
- npm: `radix-ui`, `react`

## Usage

```tsx
import { TooltipIconButton } from "@/components/assistant-ui/tooltip-icon-button"

<TooltipIconButton tooltip="Send" aria-label="Send message">
  <SendIcon />
</TooltipIconButton>
```

> Requires `TooltipProvider` around the app (frozen base tooltip contract).
