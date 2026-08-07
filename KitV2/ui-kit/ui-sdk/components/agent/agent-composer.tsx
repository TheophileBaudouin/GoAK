import { ArrowUp, Square } from "lucide-react";
import { ComposerPrimitive, useAuiState } from "@assistant-ui/react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

import { ThinkingIndicator } from "./thinking-indicator";
import { useAgentStatus } from "./use-agent-status";

export type AgentComposerProps = {
  className?: string;
  placeholder?: string;
};

/**
 * Status-aware message composer: shows the agent `ThinkingIndicator` above the
 * input while the agent is active, swaps Send ↔ Stop while a run is in flight,
 * and keeps the frozen-base keyboard contract (Enter to send, Shift+Enter for a
 * newline, Escape stops when running — handled by `ComposerPrimitive`).
 *
 * The default Thread embeds its own composer; use `AgentComposer` in custom
 * layouts (side-panel chat, embedded chat card, split view with a timeline).
 */
export function AgentComposer({ className, placeholder = "Send a message…" }: AgentComposerProps) {
  const isRunning = useAuiState((s) => s.thread.isRunning);
  const status = useAgentStatus();
  const showStatus =
    status === "thinking" ||
    status === "executing" ||
    status === "planning" ||
    status === "waiting_approval";

  return (
    <ComposerPrimitive.Root className={cn("flex w-full flex-col gap-2", className)}>
      {showStatus && (
        <div className="flex items-center justify-between px-1">
          <ThinkingIndicator status={status} />
        </div>
      )}
      <div
        data-slot="agent-composer-shell"
        className="flex items-end gap-2 rounded-xl border bg-muted/30 p-2 focus-within:border-ring"
      >
        <ComposerPrimitive.Input
          className="max-h-32 min-h-10 w-full resize-none bg-transparent px-2.5 py-1.5 text-base outline-none placeholder:text-muted-foreground/80"
          rows={1}
          enterKeyHint="send"
          aria-label="Message input"
          placeholder={placeholder}
        />
        {isRunning ? (
          <ComposerPrimitive.Cancel asChild>
            <Button
              type="button"
              variant="default"
              size="icon"
              className="shrink-0 rounded-full"
              aria-label="Stop generating"
            >
              <Square aria-hidden className="size-3.5 fill-current" />
            </Button>
          </ComposerPrimitive.Cancel>
        ) : (
          <ComposerPrimitive.Send asChild>
            <Button
              type="button"
              variant="default"
              size="icon"
              className="shrink-0 rounded-full"
              aria-label="Send message"
            >
              <ArrowUp aria-hidden />
            </Button>
          </ComposerPrimitive.Send>
        )}
      </div>
    </ComposerPrimitive.Root>
  );
}
