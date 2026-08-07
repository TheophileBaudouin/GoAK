# attachment

| | |
| --- | --- |
| Registry | @assistant-ui (official shadcn registry) |
| License | MIT |
| Source | <https://github.com/assistant-ui/assistant-ui> |
| Category | component (assistant-ui) |

Attachment primitives for the chat: file picker button on the composer
(`ComposerAddAttachment`), attachment previews inside the composer (`ComposerAttachments`)
and rendered on user messages (`UserMessageAttachments`).

## Dependencies

- Frozen base (consumer): `@/components/ui/avatar`, `@/components/ui/dialog`,
  `@/components/ui/tooltip`
- npm: `@assistant-ui/react`, `zustand`, `lucide-react`, `react`

## Usage

```tsx
import { ComposerAddAttachment, ComposerAttachments, UserMessageAttachments } from "@/components/assistant-ui/attachment"
```

> Rendered automatically by `thread.tsx` inside the composer and user messages.
