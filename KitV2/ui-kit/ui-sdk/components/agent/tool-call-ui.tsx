import { useState } from "react";
import {
  type ToolApprovalOption,
  type ToolApprovalResponse,
  type ToolCallMessagePartProps,
} from "@assistant-ui/react";

import { ApprovalCard, type ApprovalOption } from "./approval-card";
import { ToolCallCard, type ToolCallStatus } from "./tool-call";
import { ToolResult } from "./tool-result";

const APPROVAL_KIND_LABELS: Record<string, string> = {
  "allow-once": "Allow once",
  "allow-always": "Always allow",
  "reject-once": "Deny once",
  "reject-always": "Always deny",
};

/**
 * Only the 4 standard kinds are resolvable by the kit. Custom (`_`-prefixed)
 * kinds cannot be answered with a bare optionId (the assistant-ui contract
 * requires an explicit `approved` value) — hosts using them render their own
 * bar. Mirrors the vendored tool-fallback behavior.
 */
const KNOWN_KINDS = new Set(Object.keys(APPROVAL_KIND_LABELS));

function approvalOptionToCard(option: ToolApprovalOption): ApprovalOption {
  return {
    id: option.id,
    label: option.label ?? APPROVAL_KIND_LABELS[option.kind] ?? "Approve",
    description: option.description,
  };
}

function mapStatus(
  status: ToolCallMessagePartProps["status"],
  isError: boolean | undefined,
): ToolCallStatus {
  if (isError) return "error";
  if (status.type === "incomplete" && status.reason === "error") return "error";
  if (status.type === "running") return "running";
  if (status.type === "complete") return "complete";
  if (status.type === "requires-action") return "requires-action";
  return "incomplete";
}

/**
 * Default tool-call renderer of the agent kit, wired to an assistant-ui tool
 * part. Handles the three cases:
 * - pending server-side approval gate → `ApprovalCard` (Accept / Deny /
 *   shortcuts) responding through `respondToApproval`, guarded against
 *   double-submit;
 * - running / waiting tool call → `ToolCallCard` with live status;
 * - completed call → `ToolCallCard` + `ToolResult` (or error state).
 *
 * Registered tool UIs (by tool name) keep taking precedence — this is the
 * fallback used by `AgentChat` / `AgentMessage` (the `ToolFallback` slot).
 */
export function AgentToolCallUI({
  toolName,
  args,
  status,
  result,
  isError,
  approval,
  interrupt,
  respondToApproval,
}: ToolCallMessagePartProps) {
  const [submitted, setSubmitted] = useState(false);

  const pendingApproval =
    approval !== undefined &&
    approval.approved === undefined &&
    approval.resolution === undefined;

  if (pendingApproval) {
    const options = approval.options
      ?.filter((option) => KNOWN_KINDS.has(option.kind))
      .map(approvalOptionToCard);

    const respond = (response: ToolApprovalResponse) => {
      if (submitted) return;
      setSubmitted(true);
      respondToApproval(response);
    };

    return (
      <ApprovalCard
        title={`Allow the agent to run ${toolName}?`}
        description={approval.reason}
        toolName={toolName}
        options={options}
        busy={submitted}
        onApprove={() => respond({ approved: true })}
        onDeny={() => respond({ approved: false })}
        onOption={(optionId) => respond({ optionId })}
      />
    );
  }

  if (interrupt !== undefined) {
    return <ToolCallCard toolName={toolName} args={args} status="requires-action" />;
  }

  return (
    <div className="flex flex-col gap-1.5">
      <ToolCallCard
        toolName={toolName}
        args={args}
        status={mapStatus(status, isError)}
      />
      {result !== undefined && (
        <ToolResult toolName={toolName} result={result} isError={isError} />
      )}
    </div>
  );
}
