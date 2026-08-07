import { useEffect, useRef, useState } from "react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { CheckCircle2 } from "lucide-react";

import { ThreadList } from "@/components/assistant-ui/thread-list";
import { AgentChat } from "@/components/agent/agent-chat";
import { ApprovalCard } from "@/components/agent/approval-card";
import { ArtifactPreview } from "@/components/agent/artifact-preview";
import { ExecutionTimeline } from "@/components/agent/execution-timeline";
import { ThinkingIndicator } from "@/components/agent/thinking-indicator";
import { ToolCallCard } from "@/components/agent/tool-call";
import { ToolResult } from "@/components/agent/tool-result";
import { AGENT_STATUS_ORDER, type AgentStatus } from "@/components/agent/agent-status";

import { useMockAgentChat } from "./mock-runtime";

/** Interactive demo of the agent chat kit — no backend required (mock runtime). */
export function AgentChatDemo() {
  const runtime = useMockAgentChat();

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="flex h-[720px] gap-6 p-6">
        <aside
          aria-label="Conversation history"
          className="w-64 shrink-0 overflow-hidden rounded-xl border p-2"
        >
          <ThreadList />
        </aside>

        <section aria-label="Agent chat" className="min-w-0 flex-1 overflow-hidden rounded-xl border">
          <AgentChat />
        </section>

        <aside
          aria-label="Agent components gallery"
          className="w-80 shrink-0 space-y-5 overflow-y-auto"
        >
          <ComponentGallery />
        </aside>
      </div>
    </AssistantRuntimeProvider>
  );
}

function ComponentGallery() {
  const [approval, setApproval] = useState<"pending" | "approved" | "denied">("pending");
  const [copied, setCopied] = useState(false);
  const copiedTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  useEffect(() => () => clearTimeout(copiedTimer.current), []);

  return (
    <>
      <GallerySection title="Agent status">
        <div className="flex flex-wrap gap-2">
          {AGENT_STATUS_ORDER.map((status) => (
            <ThinkingIndicator key={status} status={status as AgentStatus} />
          ))}
        </div>
      </GallerySection>

      <GallerySection title="Human approval">
        {approval === "pending" ? (
          <ApprovalCard
            title="Run `npm install` in the current project?"
            description="Downloads and installs ~200 packages."
            toolName="run_command"
            onApprove={() => setApproval("approved")}
            onDeny={() => setApproval("denied")}
          />
        ) : (
          <p className="flex items-center gap-2 rounded-xl border bg-muted/30 px-3 py-2 text-sm">
            <CheckCircle2 aria-hidden className="size-4 text-primary" />
            {approval === "approved" ? "Approved — the tool ran." : "Denied — the tool was skipped."}
          </p>
        )}
      </GallerySection>

      <GallerySection title="Tool call + result">
        <div className="space-y-2">
          <ToolCallCard
            toolName="search_docs"
            args={{ query: "wails constraints" }}
            status="complete"
          />
          <ToolResult
            toolName="search_docs"
            result={{ matches: ["frontend/dist via go:embed", "HashRouter"] }}
          />
        </div>
      </GallerySection>

      <GallerySection title="Execution timeline">
        <ExecutionTimeline
          steps={[
            { id: "plan", title: "Planning the change", status: "complete", duration: "0.4s" },
            { id: "search", title: "Searching the codebase", status: "complete", duration: "0.8s" },
            { id: "edit", title: "Editing files", status: "running" },
            { id: "verify", title: "Running tests", status: "pending" },
          ]}
        />
      </GallerySection>

      <GallerySection title="Artifact preview">
        <ArtifactPreview
          title="release-notes.md"
          meta="Markdown · 2 KB"
          onCopy={() => {
            setCopied(true);
            clearTimeout(copiedTimer.current);
            copiedTimer.current = setTimeout(() => setCopied(false), 1500);
          }}
          onDownload={() => undefined}
        >
          <pre className="text-xs leading-relaxed text-muted-foreground">
            {copied ? "Copied to clipboard ✓" : "## v0.2.0\n\n- Agent chat components…"}
          </pre>
        </ArtifactPreview>
      </GallerySection>
    </>
  );
}

function GallerySection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section aria-label={title}>
      <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
        {title}
      </h2>
      {children}
    </section>
  );
}
