import { useMemo } from "react";
import { useAuiState, type ThreadMessage } from "@assistant-ui/react";

import { type AgentStatus } from "./agent-status";

/**
 * Derive the agent lifecycle status from a thread state.
 *
 * Pure and exported so external agent runtimes can reuse the same mapping:
 * - last message is still streaming → thinking / executing (running tool part)
 * - a tool part carries a pending approval gate → waiting_approval
 * - the last assistant message has an errored part → error
 * - otherwise → completed (or idle for an empty thread).
 *
 * `planning` is not observable from a thread: it is a semantic stage the agent
 * reports itself — pass it as a controlled status where applicable.
 */
export function deriveAgentStatus({
  isRunning,
  messages,
}: {
  isRunning: boolean;
  messages: readonly ThreadMessage[];
}): AgentStatus {
  if (messages.length === 0) return "idle";

  const last = messages[messages.length - 1];
  if (last.role !== "assistant") return isRunning ? "thinking" : "completed";

  let hasPendingApproval = false;
  let hasRunningTool = false;
  let hasError = false;
  let hasReasoning = false;

  for (const part of last.content) {
    if (part.type === "tool-call") {
      const approval = part.approval;
      if (approval && approval.approved === undefined && !approval.resolution) {
        hasPendingApproval = true;
      } else if (part.interrupt !== undefined) {
        hasPendingApproval = true;
      } else if (part.result === undefined) {
        hasRunningTool = true;
      }
      if (part.isError) hasError = true;
    } else if (part.type === "reasoning") {
      hasReasoning = true;
    }
  }

  if (hasPendingApproval) return "waiting_approval";
  if (isRunning) {
    if (hasRunningTool) return "executing";
    if (hasReasoning) return "thinking";
    return "thinking";
  }
  if (hasError) return "error";
  return "completed";
}

/**
 * Reactive agent status of the current thread. Requires an assistant-ui
 * `AssistantRuntimeProvider` (a Thread). For external agent runtimes, pass the
 * status directly to the presentational components (`ThinkingIndicator`,
 * `AgentComposer`…) instead.
 */
export function useAgentStatus(): AgentStatus {
  const isRunning = useAuiState((s) => s.thread.isRunning);
  const messages = useAuiState((s) => s.thread.messages);

  return useMemo(
    () => deriveAgentStatus({ isRunning, messages }),
    [isRunning, messages],
  );
}
