import { useCallback, useEffect, useRef, useState } from "react";
import {
  fromThreadMessageLike,
  useExternalStoreRuntime,
  type AppendMessage,
  type ThreadMessageLike,
} from "@assistant-ui/react";

/**
 * Scripted mock agent runtime for the example screen. No backend: a canned
 * multi-step response (reasoning → tool call → tool result → final text) is
 * played with timers against the external-store runtime, so every state of
 * the agent kit (thinking, executing, completed) is visible in the Thread.
 *
 * Replace this file with a real runtime in your app — see
 * `sdk/docs/patterns/agent-chat.md` for the Vercel AI SDK / Wails options.
 */

/** Normalize a message content to its part list (string shorthand → text part). */
function partsOf(message: ThreadMessageLike): Exclude<ThreadMessageLike["content"], string> {
  return typeof message.content === "string"
    ? [{ type: "text" as const, text: message.content }]
    : message.content;
}

export function useMockAgentChat() {
  const [messages, setMessages] = useState<readonly ThreadMessageLike[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);

  useEffect(() => {
    const active = timers.current;
    return () => active.forEach(clearTimeout);
  }, []);

  const later = useCallback((ms: number, fn: () => void) => {
    timers.current.push(setTimeout(fn, ms));
  }, []);

  const onNew = useCallback(
    async (message: AppendMessage) => {
      setMessages((prev) => [
        ...prev,
        { id: `user-${Date.now()}`, role: "user", content: message.content },
      ]);
      setIsRunning(true);

      const assistantId = `assistant-${Date.now()}`;
      const toolCallId = `tool-${Date.now()}`;

      // Stage 1 — reasoning (the agent thinks).
      later(400, () => {
        setMessages((prev) => [
          ...prev,
          {
            id: assistantId,
            role: "assistant",
            content: [
              {
                type: "reasoning",
                text: "The user wants to know how the agent kit runs inside Wails. Let me search the project documentation for the static-build constraints.",
              },
            ],
          },
        ]);
      });

      // Stage 2 — tool call starts (running).
      later(1400, () => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? {
                  ...m,
                  content: [
                    ...partsOf(m),
                    {
                      type: "tool-call",
                      toolCallId,
                      toolName: "search_docs",
                      args: { query: "wails static build constraints" },
                    },
                  ],
                }
              : m,
          ),
        );
      });

      // Stage 3 — tool call completes with a result.
      later(2400, () => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? {
                  ...m,
                  content: partsOf(m).map((p) =>
                    p.type === "tool-call"
                      ? {
                          ...p,
                          result: {
                            matches: [
                              "frontend/dist is embedded via //go:embed",
                              "HashRouter navigation — no history mode",
                              'vite base: "./" — relative assets',
                            ],
                          },
                        }
                      : p,
                  ),
                }
              : m,
          ),
        );
      });

      // Stage 4 — final answer; the run ends.
      later(3200, () => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantId
              ? {
                  ...m,
                  content: [
                    ...partsOf(m),
                    {
                      type: "text",
                      text: "Here is what I found. The Wails build is **static-only**: the frontend bundles to `frontend/dist` and is embedded with `//go:embed`, navigation uses **hash routing** and Vite runs with `base: \"./\"`. No SSR, no `next/*` imports — the agent kit is UI-only and works with any backend (AI SDK, LangGraph, or a Go streaming endpoint).",
                    },
                  ],
                }
              : m,
          ),
        );
        setIsRunning(false);
      });
    },
    [later],
  );

  const runtime = useExternalStoreRuntime({
    messages,
    isRunning,
    onNew,
    convertMessage: (message, index) =>
      fromThreadMessageLike(message, `fallback-${index}`, {
        type: "complete",
        reason: "unknown",
      }),
  });

  return runtime;
}
