import { Thread, type ThreadComponents } from "@/components/assistant-ui/thread";
import { cn } from "@/lib/utils";

import { AgentMessage } from "./agent-message";
import { AgentToolCallUI } from "./tool-call-ui";

const DEFAULT_COMPONENTS: ThreadComponents = {
  AssistantMessage: AgentMessage,
  ToolFallback: AgentToolCallUI,
};

export type AgentChatProps = {
  /**
   * Override thread rendering slots. Kit defaults: `AssistantMessage` →
   * `AgentMessage` (metadata + status), `ToolFallback` → `AgentToolCallUI`
   * (tool cards, results, approval cards). `Welcome`, `ToolGroup` and
   * `ReasoningGroup` keep the assistant-ui defaults unless overridden.
   */
  components?: ThreadComponents;
  /** Sizing/positioning wrapper class (the Thread fills its parent height). */
  className?: string;
};

/**
 * The agent chat container: assistant-ui `Thread` (conversation, streaming,
 * composer, attachments, follow-up suggestions) pre-wired with the agent kit
 * components. Requires an `AssistantRuntimeProvider` (AI SDK, LangGraph, custom
 * transport, or the external-store mock).
 */
export function AgentChat({ components, className }: AgentChatProps) {
  return (
    <div className={cn("h-full", className)}>
      <Thread
        components={{
          ...DEFAULT_COMPONENTS,
          ...components,
        }}
      />
    </div>
  );
}
