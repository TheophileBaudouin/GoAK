# Pattern — Agent chat

## When to use

For any screen where a user converses with an AI agent: autonomous agents, AI copilots,
development assistants, multi-agent platforms. The conversation is **not** a plain chat:
it interleaves user messages with agent activity — reasoning, tool calls, results,
human approvals, generated artifacts.

## How to organize the information

1. **Use assistant-ui as the conversation base** — never a home-grown chat. The Thread
   (chat, streaming, composer, attachments) comes from the assistant-ui base
   (`ui-sdk/components/assistant-ui/`); the kit's agent components sit **on top** of it
   (`ui-sdk/components/agent/`). `AgentChat` wires them together.
2. **Separate the four concerns** (constitution — no business logic in infrastructure):
   - *conversation display* — `AgentChat` / `AgentMessage` (messages, streaming);
   - *agent state* — `AgentStatus` (`use-agent-status.ts`), surfaced by `ThinkingIndicator`;
   - *tool actions* — `ToolCallCard` + `ToolResult` (and registered per-tool UIs);
   - *user validation* — `ApprovalCard` for human-in-the-loop gates.
3. Agent lifecycle: `idle → thinking → planning → executing → waiting_approval →
   completed | error`. `planning` is a semantic stage the agent reports; the others are
   derivable from the thread (`useAgentStatus`).
4. Sensitive operations (command execution, file modification, external actions) go
   through an **approval gate** — the backend requests approval, the `ApprovalCard`
   renders Accept / Deny / shortcuts, the decision resumes the run.
5. For multi-step work, a side panel with `ExecutionTimeline` + `ArtifactPreview` next to
   the chat gives the "mission control" view (desktop layout, `ui-rules/06-layout.md`).
6. **Conversation history** (multi-conversation apps): `ThreadList` in a desktop sidebar —
   new thread, search, date groups, rename/archive/delete. Requires a thread-list-capable
   runtime (AI SDK cloud threads, LangGraph, custom `ExternalStore` thread list).
7. **Copilot pattern** (ask from anywhere): `AssistantModal` — a floating button opening a
   full Thread popover, without leaving the current screen.
8. **Multi-agent platforms**: render sub-agent conversations inside tool call UIs via the
   tool part's `messages` field (`ThreadMessage[]` nested threads) — see the assistant-ui
   multi-agent guide; keep the kit components for the outer conversation.

## Common mistakes

- Building a chat from scratch instead of using the assistant-ui base (the point of the
  kit).
- Rendering tool calls as raw JSON in the message flow (use `ToolCallCard` / grouped
  tool groups).
- Auto-approving sensitive actions — every approval gate must be visible and
  user-controlled (`ApprovalCard`).
- Using color alone for status (WCAG 1.4.1) — `ThinkingIndicator`/`ExecutionTimeline`
  pair icon + label.
- Hiding the agent's activity: users must see thinking / tool execution states, not a
  silent spinner.
- Backend coupling inside components: the kit components are presentational; the
  runtime (AI SDK, LangGraph, custom transport, Go streaming endpoint) is the consumer's
  choice.

## Best practices

- Streaming first: show partial text, reasoning and tool calls as they arrive.
- Status + icon + label everywhere a status appears (`ui-rules/02-colors.md`,
  `05-accessibility.md`).
- Keep the composer alive during runs (Send → Stop), disable only when the backend
  reports it (`AgentComposer`).
- Keyboard: Enter to send, Shift+Enter newline, Esc to stop (`ui-rules/08-keyboard.md`).
- Static-only build: the kit is UI-only and runtime-agnostic — perfect for Wails
  (`docs/wails-constraints.md`).
- **Code blocks**: the kit's markdown renders code blocks with a language header + copy
  button but no syntax highlighting (assistant-ui default). For highlighting, wire
  `react-shiki` (recommended by assistant-ui for performance) into the markdown
  components — see the assistant-ui syntax-highlighting guide; keep the kit itself
  dependency-light.

## Components/blocks recommended

- `ui-sdk/components/assistant-ui/thread.tsx` — the assistant-ui conversation base
  (registry: r.assistant-ui.com, MIT).
- `ui-sdk/components/assistant-ui/thread-list.tsx` — conversation history sidebar.
- `ui-sdk/components/assistant-ui/assistant-modal.tsx` — copilot chat-in-popover.
- `ui-sdk/components/agent/agent-chat.tsx`, `agent-message.tsx`, `agent-composer.tsx`,
  `use-agent-status.ts` — conversation + agent state.
- `ui-sdk/components/agent/tool-call.tsx`, `tool-result.tsx`, `tool-call-ui.tsx` — tool
  actions (auto-wired by `AgentChat`).
- `ui-sdk/components/agent/approval-card.tsx` — human validation (AI SDK `toolApproval`
  / assistant-ui `respondToApproval`).
- `ui-sdk/components/agent/execution-timeline.tsx`, `artifact-preview.tsx`,
  `thinking-indicator.tsx` — multi-step views.
- `ui-sdk/examples/agent-chat/` — the reference demo screen (mock runtime, no backend).
- Backend options: Vercel AI SDK (`ai` + `@ai-sdk/react` via
  `@assistant-ui/react-ai-sdk`), LangGraph (`@assistant-ui/react-langgraph`), or a custom
  assistant-ui transport (e.g. a Go SSE endpoint in Wails).

## Sources

- assistant-ui official docs — <https://www.assistant-ui.com/docs> (Thread, primitives,
  AI SDK runtime), registry <https://r.assistant-ui.com/thread.json>, MIT.
- Vercel AI SDK — streaming, tool calling, `toolApproval` human-in-the-loop:
  <https://ai-sdk.dev/docs/ai-sdk-ui/chatbot-tool-usage>, <https://ai-sdk.dev/docs/agents/tool-approvals>.
- Apple HIG (desktop chat conventions) via `skills/macos-design-guidelines`; WCAG 2.2
  (status not color-only, focus, announcements) via `skills/web-platform-guidelines`.
