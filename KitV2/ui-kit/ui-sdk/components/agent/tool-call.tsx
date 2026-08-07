import { useState, type ReactNode } from "react";
import { ChevronDown, CheckCircle2, AlertTriangle, UserRound, LoaderCircle } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";

/** Presentational status of a tool call (mirrors the assistant-ui part statuses). */
export type ToolCallStatus =
  | "running"
  | "complete"
  | "requires-action"
  | "incomplete"
  | "error";

export type ToolCallCardProps = {
  /** Tool identifier, e.g. `search_files`. */
  toolName: string;
  /** Tool arguments (JSON-serializable). */
  args?: unknown;
  status?: ToolCallStatus;
  /** Optional live content below the header (e.g. a progress note). */
  children?: ReactNode;
  className?: string;
};

const STATUS_LABELS: Record<ToolCallStatus, string> = {
  running: "Running",
  complete: "Completed",
  "requires-action": "Needs input",
  incomplete: "Incomplete",
  error: "Failed",
};

function StatusIcon({ status }: { status: ToolCallStatus }) {
  switch (status) {
    case "running":
      return <LoaderCircle aria-hidden className="size-3.5 animate-spin text-primary" />;
    case "complete":
      return <CheckCircle2 aria-hidden className="size-3.5 text-primary" />;
    case "requires-action":
      return <UserRound aria-hidden className="size-3.5 text-primary" />;
    case "error":
      return <AlertTriangle aria-hidden className="size-3.5 text-destructive" />;
    default:
      return <AlertTriangle aria-hidden className="size-3.5 text-muted-foreground" />;
  }
}

/**
 * One tool call in the conversation: name, status, collapsible JSON arguments.
 * Presentational — wire it to an assistant-ui tool part via the `ToolFallback`
 * slot of `AgentChat`, or drive it from any external agent runtime.
 */
export function ToolCallCard({
  toolName,
  args,
  status = "complete",
  children,
  className,
}: ToolCallCardProps) {
  const [open, setOpen] = useState(false);
  const hasArgs = args !== undefined && args !== null;

  return (
    <Collapsible
      open={open}
      onOpenChange={setOpen}
      data-tool-status={status}
      className={cn(
        "overflow-hidden rounded-xl border bg-card text-card-foreground",
        status === "error" && "border-destructive/40",
        className,
      )}
    >
      {hasArgs ? (
        <CollapsibleTrigger className="flex w-full cursor-pointer items-center gap-2 px-3 py-2 text-sm">
          <StatusIcon status={status} />
          <span className="font-medium">{toolName}</span>
          <Badge
            variant={status === "error" ? "destructive" : "secondary"}
            className="ml-auto"
          >
            {STATUS_LABELS[status]}
          </Badge>
          <ChevronDown
            aria-hidden
            className={cn(
              "size-4 text-muted-foreground transition-transform",
              open && "rotate-180",
            )}
          />
        </CollapsibleTrigger>
      ) : (
        <div className="flex items-center gap-2 px-3 py-2 text-sm">
          <StatusIcon status={status} />
          <span className="font-medium">{toolName}</span>
          <Badge
            variant={status === "error" ? "destructive" : "secondary"}
            className="ml-auto"
          >
            {STATUS_LABELS[status]}
          </Badge>
        </div>
      )}
      {hasArgs && (
        <CollapsibleContent>
          <pre className="max-h-48 overflow-auto border-t bg-muted/40 px-3 py-2 text-xs leading-relaxed">
            {JSON.stringify(args, null, 2)}
          </pre>
        </CollapsibleContent>
      )}
      {children}
    </Collapsible>
  );
}
