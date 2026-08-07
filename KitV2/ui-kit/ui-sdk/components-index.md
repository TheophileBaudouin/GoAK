# Component index — ui-agent-kit

> The single source of truth for every component/block/layout in `ui-sdk/`. Maintained per
> docs/authoring-guides/components-index-entry.md. Last updated: 2026-08-08.

Frozen base components (shadcn/ui, Radix base, 61 pieces) are **not** listed here: they live
in the consumer's app, installed via the shadcn CLI. This index lists the kit's additions.

| Component | Category | Short description | Status |
| --- | --- | --- | --- |
| agent-chat | component (agent) | Agent chat container (assistant-ui Thread + agent components) | Ready |
| agent-composer | component (agent) | Status-aware composer (ThinkingIndicator, Send/Stop) | Ready |
| agent-message | component (agent) | Assistant message with agent metadata + status | Ready |
| agent-status | component (agent) | AgentStatus/StepStatus vocabulary + a11y labels | Ready |
| approval-card | component (agent) | Human approval gate (Accept/Deny/shortcuts) | Ready |
| artifact-preview | component (agent) | Generated artifact preview with actions | Ready |
| attachment | component (assistant-ui) | Composer/user-message attachments (assistant-ui registry) | Ready |
| assistant-modal | component (assistant-ui) | Chat-in-popover copilot launcher (assistant-ui registry) | Ready |
| thread-list | component (assistant-ui) | Conversation history sidebar (assistant-ui registry) | Ready |
| execution-timeline | component (agent) | Agent run steps with status icons | Ready |
| follow-up-suggestions | component (assistant-ui) | Suggestion chips (assistant-ui registry) | Ready |
| markdown-text | component (assistant-ui) | Streaming markdown with copy (assistant-ui registry) | Ready |
| reasoning | component (assistant-ui) | Collapsible reasoning block (assistant-ui registry) | Ready |
| thinking-indicator | component (agent) | Agent lifecycle status pill | Ready |
| thread | component (assistant-ui) | Chat container (assistant-ui registry) — agent chat base | Ready |
| tool-call | component (agent) | Tool call card (name, status, args) | Ready |
| tool-call-ui | component (agent) | assistant-ui tool part renderer (toolUI fallback) | Ready |
| tool-fallback | component (assistant-ui) | Default tool call rendering (assistant-ui registry) | Ready |
| tool-group | component (assistant-ui) | Collapsible tool call group (assistant-ui registry) | Ready |
| tool-result | component (agent) | Tool output (JSON or custom children) | Ready |
| tooltip-icon-button | component (assistant-ui) | Tooltip icon button (assistant-ui registry) | Ready |
| use-agent-status | component (agent) | Hook deriving AgentStatus from the thread | Ready |
| command-menu-01 | block | command-menu (page block) | Ready |
| command-menu-02 | block | command-menu (page block) | Ready |
| file-upload-05 | block | file-upload (page block) | Ready |
| form-layout-01 | block | form-layout (page block) | Ready |
| login-03 | block | login (page block) | Ready |
| onboarding-03 | block | onboarding (page block) | Ready |
| stats-12 | block | stats-12 (page block) | Ready |
| auth-change-password | component | auth-change-password | Ready |
| auth-session-manager | component | auth-session-manager | Ready |
| avatar-stack | component | avatar-stack | Ready |
| billing-subscription-settings | component | billing-subscription-settings | Ready |
| dropzone | component | dropzone | Ready |
| dropzone-core | component | dropzone-core | Ready |
| echarts-bar-chart | component | echarts-bar-chart | Ready |
| echarts-brush | component | echarts-brush | Ready |
| echarts-chart | component | echarts-chart | Ready |
| echarts-composed-chart | component | echarts-composed-chart | Ready |
| echarts-dot | component | echarts-dot | Ready |
| echarts-legend | component | echarts-legend | Ready |
| echarts-line-chart | component | echarts-line-chart | Ready |
| echarts-pie-chart | component | echarts-pie-chart | Ready |
| echarts-tooltip | component | echarts-tooltip | Ready |
| file-size-format | component | file-size-format | Ready |
| image-zoom | component | image-zoom | Ready |
| marquee | component | marquee | Ready |
| page-heading | component | page-heading | Ready |
| profile-card | component | profile-card | Ready |
| recharts-chart | component | recharts-chart | Ready |
| recharts-tooltip | component | recharts-tooltip | Ready |
| section-heading | component | section-heading | Ready |
| settings-account | component | settings-account | Ready |
| settings-activity-log | component | settings-activity-log | Ready |
| settings-api-keys | component | settings-api-keys | Ready |
| settings-notifications | component | settings-notifications | Ready |
| settings-preferences | component | settings-preferences | Ready |
| settings-security | component | settings-security | Ready |
| settings-team-members | component | settings-team-members | Ready |
| star-rating | component | star-rating | Ready |
| tagline | component | tagline | Ready |
| use-keyed-mount-effect | component | use-keyed-mount-effect | Ready |

## Legend

- **Status**: Ready = installed from a license-verified registry and organized in ui-sdk/.
- **Category**: component = reusable piece; block = full page section.
- Origin, license and usage for each piece: see its README (next to the source file).
