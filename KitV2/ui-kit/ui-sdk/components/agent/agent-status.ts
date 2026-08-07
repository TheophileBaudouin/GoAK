/**
 * Shared agent-status vocabulary for the agent chat kit.
 *
 * Pure module — no UI, no assistant-ui dependency. The status enum is the
 * contract between the data layer (useAgentStatus, or any external agent
 * runtime) and the presentational components (ThinkingIndicator,
 * ExecutionTimeline, AgentComposer…).
 */

/** Lifecycle of an agent run, as surfaced to the user. */
export type AgentStatus =
  | "idle"
  | "thinking"
  | "planning"
  | "executing"
  | "waiting_approval"
  | "completed"
  | "error";

/** Status of one step inside an execution timeline. */
export type StepStatus = "pending" | "running" | "complete" | "error";

/** Human label per agent status (used for a11y — never color-only). */
export const AGENT_STATUS_LABELS: Record<AgentStatus, string> = {
  idle: "Idle",
  thinking: "Thinking…",
  planning: "Planning…",
  executing: "Executing…",
  waiting_approval: "Awaiting your approval",
  completed: "Completed",
  error: "Error",
};

/** Ordered statuses — a run progresses along this line (usable for a11y). */
export const AGENT_STATUS_ORDER: readonly AgentStatus[] = [
  "idle",
  "thinking",
  "planning",
  "executing",
  "waiting_approval",
  "completed",
  "error",
] as const;
