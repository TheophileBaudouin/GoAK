import {
  Brain,
  CheckCircle2,
  CircleDashed,
  Hammer,
  ListChecks,
  ShieldQuestion,
  XCircle,
  type LucideIcon,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

import { AGENT_STATUS_LABELS, type AgentStatus } from "./agent-status";

const STATUS_ICONS: Record<AgentStatus, LucideIcon> = {
  idle: CircleDashed,
  thinking: Brain,
  planning: ListChecks,
  executing: Hammer,
  waiting_approval: ShieldQuestion,
  completed: CheckCircle2,
  error: XCircle,
};

/** Spins only for the in-progress statuses (Reduce Motion is handled by tw-animate-css). */
const STATUS_SPINNING: ReadonlySet<AgentStatus> = new Set([
  "thinking",
  "planning",
  "executing",
]);

export type ThinkingIndicatorProps = {
  /** Agent lifecycle status (see agent-status). */
  status: AgentStatus;
  /** Override the a11y label (defaults to the status label). */
  label?: string;
  className?: string;
};

/**
 * Compact status pill showing the agent lifecycle:
 * idle · thinking · planning · executing · waiting_approval · completed · error.
 *
 * Presentational: pass any status, from `useAgentStatus` or from an external
 * agent runtime. Icon + label always travel together (WCAG 1.4.1 — the label
 * is never conveyed by color alone). Announcement-friendly: `role="status"`.
 */
export function ThinkingIndicator({
  status,
  label,
  className,
}: ThinkingIndicatorProps) {
  const Icon = STATUS_ICONS[status];
  const spinning = STATUS_SPINNING.has(status);
  const isLive = status === "thinking" || status === "planning" || status === "executing";

  return (
    <Badge
      variant={status === "error" ? "destructive" : "secondary"}
      data-status={status}
      role={isLive ? "status" : undefined}
      aria-live={isLive ? "polite" : undefined}
      className={cn("gap-1.5", className)}
    >
      <Icon
        aria-hidden
        className={cn("size-3.5", spinning && "animate-spin")}
      />
      <span>{label ?? AGENT_STATUS_LABELS[status]}</span>
    </Badge>
  );
}
