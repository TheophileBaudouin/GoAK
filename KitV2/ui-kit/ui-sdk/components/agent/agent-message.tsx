import {
  Bot,
  Check,
  ChevronLeft,
  ChevronRight,
  Copy,
  Download,
  MoreHorizontal,
  RefreshCw,
} from "lucide-react";
import {
  ActionBarMorePrimitive,
  ActionBarPrimitive,
  AuiIf,
  BranchPickerPrimitive,
  ErrorPrimitive,
  MessagePrimitive,
  groupPartByType,
  useAuiState,
  type MessageStatus,
} from "@assistant-ui/react";

import { MarkdownText } from "@/components/assistant-ui/markdown-text";
import {
  Reasoning,
  ReasoningContent,
  ReasoningRoot,
  ReasoningText,
  ReasoningTrigger,
} from "@/components/assistant-ui/reasoning";
import {
  ToolGroupContent,
  ToolGroupRoot,
  ToolGroupTrigger,
} from "@/components/assistant-ui/tool-group";
import { TooltipIconButton } from "@/components/assistant-ui/tooltip-icon-button";
import { cn } from "@/lib/utils";

import { type AgentStatus } from "./agent-status";
import { ThinkingIndicator } from "./thinking-indicator";
import { AgentToolCallUI } from "./tool-call-ui";

function messageStatusToAgentStatus(status: MessageStatus): AgentStatus {
  switch (status.type) {
    case "running":
      return "thinking";
    case "requires-action":
      return status.reason === "interrupt" ? "waiting_approval" : "executing";
    case "complete":
      return "completed";
    case "incomplete":
      return status.reason === "cancelled" ? "completed" : "error";
  }
}

/**
 * Assistant message variant with agent metadata: avatar, agent name and a
 * per-message `ThinkingIndicator` (derived from the message status). Replaces
 * the default assistant message when passed as `ThreadComponents.AssistantMessage`
 * (AgentChat does it by default).
 *
 * The part rendering mirrors the assistant-ui reference thread: grouped
 * reasoning, grouped tool calls, markdown text, registered tool UIs, and the
 * kit's `AgentToolCallUI` fallback (tool cards + approvals).
 */
export function AgentMessage() {
  const status = useAuiState((s) => s.message.status);

  return (
    <MessagePrimitive.Root
      data-role="assistant"
      data-slot="agent-message"
      className="group/message relative -mb-7.5 flex gap-3 pb-7.5"
    >
      <div
        data-slot="agent-message-avatar"
        className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-full bg-primary/10"
      >
        <Bot aria-hidden className="size-4 text-primary" />
      </div>

      <div className="min-w-0 flex-1">
        <div className="mb-1.5 flex items-center gap-2 px-2">
          <span className="text-sm font-medium">Agent</span>
          <ThinkingIndicator status={status ? messageStatusToAgentStatus(status) : "completed"} />
        </div>

        <div className="text-foreground px-2 leading-relaxed [overflow-wrap:anywhere]">
          <MessagePrimitive.GroupedParts
            groupBy={groupPartByType({
              reasoning: ["group-chainOfThought", "group-reasoning"],
              "tool-call": ["group-chainOfThought", "group-tool"],
              "standalone-tool-call": [],
            })}
          >
            {({ part, children }) => {
              switch (part.type) {
                case "group-chainOfThought":
                  return <div data-slot="agent-chain-of-thought">{children}</div>;
                case "group-tool":
                  return (
                    <ToolGroupRoot variant="ghost">
                      <ToolGroupTrigger
                        count={part.indices.length}
                        active={part.status.type === "running"}
                      />
                      <ToolGroupContent>{children}</ToolGroupContent>
                    </ToolGroupRoot>
                  );
                case "group-reasoning": {
                  const running = part.status.type === "running";
                  return (
                    <ReasoningRoot variant="ghost" streaming={running}>
                      <ReasoningTrigger active={running} />
                      <ReasoningContent aria-busy={running}>
                        <ReasoningText>{children}</ReasoningText>
                      </ReasoningContent>
                    </ReasoningRoot>
                  );
                }
                case "text":
                  return <MarkdownText />;
                case "reasoning":
                  return <Reasoning {...part} />;
                case "tool-call":
                  return part.toolUI ?? <AgentToolCallUI {...part} />;
                case "data":
                  return part.dataRendererUI;
                case "indicator":
                  return (
                    <span
                      data-slot="agent-message-indicator"
                      role="status"
                      className="animate-pulse"
                      aria-label="Agent is working"
                    >
                      {"●"}
                    </span>
                  );
                default:
                  return null;
              }
            }}
          </MessagePrimitive.GroupedParts>

          <MessagePrimitive.Error>
            <ErrorPrimitive.Root className="mt-2 rounded-md border border-destructive bg-destructive/10 p-3 text-sm text-destructive dark:bg-destructive/5">
              <ErrorPrimitive.Message className="line-clamp-2" />
            </ErrorPrimitive.Root>
          </MessagePrimitive.Error>
        </div>

        <div
          data-slot="agent-message-footer"
          className="ms-2 flex min-h-7 items-center pt-1.5"
        >
          <BranchPicker />
          <AssistantActionBar />
        </div>
      </div>
    </MessagePrimitive.Root>
  );
}

/** Copy / reload / export actions (parity with the reference thread). */
function AssistantActionBar() {
  return (
    <ActionBarPrimitive.Root
      hideWhenRunning
      autohide="not-last"
      className="text-muted-foreground animate-in fade-in -ms-1 flex gap-1 duration-200"
    >
      <ActionBarPrimitive.Copy asChild>
        <TooltipIconButton tooltip="Copy">
          <AuiIf condition={(s) => s.message.isCopied}>
            <Check className="animate-in zoom-in-50 fade-in duration-200 ease-out" />
          </AuiIf>
          <AuiIf condition={(s) => !s.message.isCopied}>
            <Copy className="animate-in zoom-in-75 fade-in duration-150" />
          </AuiIf>
        </TooltipIconButton>
      </ActionBarPrimitive.Copy>
      <ActionBarPrimitive.Reload asChild>
        <TooltipIconButton tooltip="Refresh">
          <RefreshCw />
        </TooltipIconButton>
      </ActionBarPrimitive.Reload>
      <ActionBarMorePrimitive.Root>
        <ActionBarMorePrimitive.Trigger asChild>
          <TooltipIconButton
            tooltip="More"
            className="data-[state=open]:bg-accent"
          >
            <MoreHorizontal />
          </TooltipIconButton>
        </ActionBarMorePrimitive.Trigger>
        <ActionBarMorePrimitive.Content
          side="bottom"
          align="start"
          sideOffset={6}
          className="bg-popover/95 text-popover-foreground data-[state=open]:fade-in-0 data-[state=open]:zoom-in-95 data-[state=open]:animate-in data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[state=closed]:animate-out data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 z-50 min-w-32 overflow-hidden rounded-xl border p-1.5 shadow-lg backdrop-blur-sm"
        >
          <ActionBarPrimitive.ExportMarkdown asChild>
            <ActionBarMorePrimitive.Item className="hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground flex cursor-pointer items-center gap-2 rounded-lg px-2.5 py-1.5 text-sm outline-none select-none">
              <Download className="size-4" />
              Export as Markdown
            </ActionBarMorePrimitive.Item>
          </ActionBarPrimitive.ExportMarkdown>
        </ActionBarMorePrimitive.Content>
      </ActionBarMorePrimitive.Root>
    </ActionBarPrimitive.Root>
  );
}

/** Branch navigation (regenerate branches), parity with the reference thread. */
function BranchPicker({ className }: { className?: string }) {
  return (
    <BranchPickerPrimitive.Root
      hideWhenSingleBranch
      className={cn(
        "text-muted-foreground -ms-2 me-2 inline-flex items-center text-xs",
        className,
      )}
    >
      <BranchPickerPrimitive.Previous asChild>
        <TooltipIconButton tooltip="Previous">
          <ChevronLeft />
        </TooltipIconButton>
      </BranchPickerPrimitive.Previous>
      <span className="font-medium">
        <BranchPickerPrimitive.Number /> / <BranchPickerPrimitive.Count />
      </span>
      <BranchPickerPrimitive.Next asChild>
        <TooltipIconButton tooltip="Next">
          <ChevronRight />
        </TooltipIconButton>
      </BranchPickerPrimitive.Next>
    </BranchPickerPrimitive.Root>
  );
}
