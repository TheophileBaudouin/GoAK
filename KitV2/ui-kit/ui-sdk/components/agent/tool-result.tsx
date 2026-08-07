import { type ReactNode } from "react";
import { CheckCircle2, XCircle } from "lucide-react";

import { cn } from "@/lib/utils";

export type ToolResultProps = {
  /** Tool identifier, shown as a heading. */
  toolName: string;
  /** Tool output (JSON-serializable) — rendered pretty-printed. */
  result?: unknown;
  /** Set when the result is a tool execution error. */
  isError?: boolean;
  /** Replace the default JSON rendering (e.g. a component built from the result). */
  children?: ReactNode;
  className?: string;
};

/**
 * The output of a finished tool call: success or error state, pretty-printed JSON
 * (or a custom `children` renderer). Presentational and dependency-free.
 */
export function ToolResult({
  toolName,
  result,
  isError = false,
  children,
  className,
}: ToolResultProps) {
  const hasChildren = children !== undefined && children !== null;

  return (
    <div
      data-tool-result={isError ? "error" : "success"}
      className={cn(
        "overflow-hidden rounded-xl border bg-muted/30",
        isError ? "border-destructive/40" : "border-border",
        className,
      )}
    >
      <div
        className={cn(
          "flex items-center gap-2 border-b px-3 py-1.5 text-xs font-medium",
          isError ? "border-destructive/20 text-destructive" : "border-border text-muted-foreground",
        )}
      >
        {isError ? (
          <XCircle aria-hidden className="size-3.5" />
        ) : (
          <CheckCircle2 aria-hidden className="size-3.5 text-primary" />
        )}
        <span>{toolName}</span>
      </div>
      {hasChildren ? (
        <div className="px-3 py-2">{children}</div>
      ) : (
        <pre className="max-h-64 overflow-auto px-3 py-2 text-xs leading-relaxed">
          {JSON.stringify(result, null, 2)}
        </pre>
      )}
    </div>
  );
}
