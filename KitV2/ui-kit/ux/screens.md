# Screens — ui-agent-kit

> Last updated: 2026-08-08
> Must be read before any interface change. Must be updated after any significant change.
> See docs/authoring-guides/ux-screens.md for the detailed format and analysis method.

## Agent chat

- Purpose: converse with an AI agent — send a message, watch it think, call tools, ask
  for approval, and receive generated artifacts.
- Content: conversation (user + agent messages), agent status indicator, tool call cards
  and results, approval card, execution timeline, artifact previews, composer.
- Actions: Send / Stop message, Accept / Deny an approval, expand tool call arguments,
  copy / open / download an artifact.
- Notes: reference implementation `ui-sdk/examples/agent-chat/` (mock runtime — no
  backend needed); production wiring documented in `sdk/patterns/agent-chat.md`. Screen
  name shared with the `user-flows.md` agent conversation flow when it exists.
