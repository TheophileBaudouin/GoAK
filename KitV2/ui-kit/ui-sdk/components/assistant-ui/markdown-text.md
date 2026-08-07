# markdown-text

| | |
| --- | --- |
| Registry | @assistant-ui (official shadcn registry) |
| License | MIT |
| Source | <https://github.com/assistant-ui/assistant-ui> |
| Category | component (assistant-ui) |

Streaming markdown renderer with syntax highlighting and a copy button, used for assistant
message text parts. Based on `@assistant-ui/react-markdown` + `remark-gfm`.

## Dependencies

- npm: `@assistant-ui/react-markdown`, `remark-gfm`, `lucide-react`, `react`

## Usage

```tsx
import { MarkdownText } from "@/components/assistant-ui/markdown-text"

// Rendered inside a message part (MessagePrimitive text part), typically via Thread.
<MarkdownText />
```

> Rendered automatically by `thread.tsx` for `text` parts — import directly only when
> building a custom message component.
