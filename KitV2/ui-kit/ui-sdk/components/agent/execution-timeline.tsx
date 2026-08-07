import { CheckCircle2, CircleDashed, LoaderCircle, XCircle } from "lucide-react";

import { cn } from "@/lib/utils";

import { type StepStatus } from "./agent-status";

export type TimelineStep = {
  /** Stable id (used as React key). */
  id: string;
  /** Step title, e.g. "Searching the codebase". */
  title: string;
  /** Optional one-line detail, e.g. a file path or count. */
  description?: string;
  status: StepStatus;
  /** Duration label, e.g. "1.2s" — shown when present. */
  duration?: string;
};

export type ExecutionTimelineProps = {
  /** Ordered agent steps, e.g. plan → execute → verify. */
  steps: readonly TimelineStep[];
  className?: string;
};

function StepIcon({ status }: { status: StepStatus }) {
  switch (status) {
    case "running":
      return <LoaderCircle aria-hidden className="size-4 animate-spin text-primary" />;
    case "complete":
      return <CheckCircle2 aria-hidden className="size-4 text-primary" />;
    case "error":
      return <XCircle aria-hidden className="size-4 text-destructive" />;
    default:
      return <CircleDashed aria-hidden className="size-4 text-muted-foreground" />;
  }
}

const STEP_LABELS: Record<StepStatus, string> = {
  pending: "Pending",
  running: "Running",
  complete: "Completed",
  error: "Failed",
};

/**
 * Vertical execution timeline of an agent run: ordered steps with status icons,
 * connector line and optional durations. Status is always conveyed by icon +
 * text label, never color alone (WCAG 1.4.1). Presentational.
 */
export function ExecutionTimeline({ steps, className }: ExecutionTimelineProps) {
  if (steps.length === 0) return null;

  return (
    <ol data-execution-timeline className={cn("space-y-0", className)}>
      {steps.map((step, index) => {
        const isLast = index === steps.length - 1;
        return (
          <li key={step.id} className="relative flex gap-3 pb-4 last:pb-0">
            {!isLast && (
              <span
                aria-hidden
                className="absolute left-[7px] top-5 h-full w-px bg-border"
              />
            )}
            <span
              data-step-status={step.status}
              className="relative z-10 mt-0.5 flex size-4 shrink-0 items-center justify-center rounded-full bg-background"
            >
              <StepIcon status={step.status} />
            </span>
            <div className="min-w-0 flex-1 pt-0.5">
              <div className="flex items-baseline justify-between gap-2">
                <p className="truncate text-sm font-medium">{step.title}</p>
                {step.duration && (
                  <span className="shrink-0 text-xs tabular-nums text-muted-foreground">
                    {step.duration}
                  </span>
                )}
              </div>
              {step.description && (
                <p className="mt-0.5 truncate text-xs text-muted-foreground">
                  {step.description}
                </p>
              )}
              <span className="sr-only">{STEP_LABELS[step.status]}</span>
            </div>
          </li>
        );
      })}
    </ol>
  );
}
