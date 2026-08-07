# Design Decisions — ui-agent-kit

> Last updated: 2026-08-08
> Must be read before any interface change. Must be updated after any significant change.
> See docs/authoring-guides/ux-design-decisions.md for the detailed format and analysis method.

## D-005 — 2026-08-08: assistant-ui as the agent chat base

- Context: the SDK needed conversational AI screens (agents, copilots, dev assistants).
  Building a chat system from scratch contradicts the kit's mission (never reinvent a
  complex system).
- Decision: the agent chat base is **assistant-ui** (MIT, React 19, Radix + Tailwind +
  shadcn — same base as the frozen base). Its official shadcn registry components are
  harvested into `ui-sdk/components/assistant-ui/` (Thread, markdown, tool groups,
  reasoning, attachments); the kit's agent components (`ui-sdk/components/agent/`) are
  first-party, presentational, and runtime-agnostic (AI SDK, LangGraph, custom transport,
  Go endpoint).
- Alternatives rejected: home-grown chat (rejected: reinventing streaming, tool UI,
  approvals); tool-ui (assistant-ui/tool-ui) as foundation (rejected for now: young
  project, keep as observation); Next.js-only integrations (rejected: Wails is
  static-only).
- Source: assistant-ui docs + registry (r.assistant-ui.com, MIT); Vercel AI SDK tool
  approval patterns; pattern `sdk/patterns/agent-chat.md`.
- Status: Frozen

## D-006 — 2026-08-08: ghost is the default variant for tool groups and reasoning

- Context: assistant-ui's ToolGroup / ReasoningRoot default to the `outline` variant
  (bordered boxes around every tool call and reasoning block). For a premium desktop
  aesthetic the conversation should read flat: tool activity and reasoning are
  informational, not boxed chrome.
- Decision: the kit's default variant is **ghost** (no additional styling) for both
  `ToolGroupRoot` and `ReasoningRoot`. This is enforced at the source: the default
  variants of the harvested components were changed (documented deviation from the
  registry, re-applied by the kit copy — the consumer installs from `ui-sdk/`, not from
  the registry). `outline` / `muted` remain opt-in per usage.
- Alternatives rejected: keeping the assistant-ui default (rejected: boxed tool groups
  add visual noise to every step of an agent run).
- Source: assistant-ui ToolGroup / Reasoning variants (r.assistant-ui.com, MIT); Apple
  HIG minimal chrome (via `skills/macos-design-guidelines`).
- Status: Frozen
