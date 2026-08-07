import { ShieldQuestion, Check, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export type ApprovalOption = {
  id: string;
  label: string;
  description?: string;
};

export type ApprovalCardProps = {
  /** What is being approved (e.g. "Run `npm install` on the current project"). */
  title: string;
  /** Optional context shown under the title. */
  description?: string;
  /** Tool requesting the approval. */
  toolName?: string;
  /** Decision shortcuts (e.g. allow-once / allow-always), rendered as buttons. */
  options?: readonly ApprovalOption[];
  /** Disables the buttons while the decision is being processed. */
  busy?: boolean;
  onApprove?: () => void;
  onDeny?: () => void;
  /** Fired with the option id for shortcut decisions. */
  onOption?: (optionId: string) => void;
  className?: string;
};

/**
 * Human-approval gate for a sensitive agent action (command execution, file
 * modification, external action). Accept / Deny, or option shortcuts
 * (allow-once, allow-always…). Presentational — wire the callbacks to the
 * backend's approval API (`respondToApproval` in an assistant-ui tool part,
 * `toolApproval` in the Vercel AI SDK).
 */
export function ApprovalCard({
  title,
  description,
  toolName,
  options,
  busy = false,
  onApprove,
  onDeny,
  onOption,
  className,
}: ApprovalCardProps) {
  return (
    <div
      data-approval="pending"
      role="group"
      aria-label={`Approval required: ${title}`}
      className={cn(
        "rounded-xl border border-primary/40 bg-primary/5 p-4",
        className,
      )}
    >
      <div className="flex items-start gap-3">
        <div className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-full bg-primary/15">
          <ShieldQuestion aria-hidden className="size-4.5 text-primary" />
        </div>
        <div className="min-w-0 flex-1">
          <p className="text-sm font-medium">{title}</p>
          {description && (
            <p className="mt-0.5 text-sm text-muted-foreground">{description}</p>
          )}
          {toolName && (
            <p className="mt-1 text-xs text-muted-foreground">Tool: {toolName}</p>
          )}

          <div className="mt-3 flex flex-wrap items-center gap-2">
            {options?.map((option) => (
              <Button
                key={option.id}
                type="button"
                size="sm"
                variant="outline"
                disabled={busy}
                onClick={() => onOption?.(option.id)}
              >
                {option.label}
              </Button>
            ))}
            {!options || options.length === 0 ? (
              <>
                <Button
                  type="button"
                  size="sm"
                  disabled={busy}
                  onClick={onApprove}
                >
                  <Check aria-hidden className="size-4" />
                  Accept
                </Button>
                <Button
                  type="button"
                  size="sm"
                  variant="ghost"
                  disabled={busy}
                  onClick={onDeny}
                >
                  <X aria-hidden className="size-4" />
                  Deny
                </Button>
              </>
            ) : (
              <Button
                type="button"
                size="sm"
                variant="ghost"
                disabled={busy}
                onClick={onDeny}
              >
                Deny
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
