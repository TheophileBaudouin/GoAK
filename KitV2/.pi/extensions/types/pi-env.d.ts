/**
 * Editor-only ambient type declarations for Pi extension imports.
 *
 * `@earendil-works/pi-coding-agent`, `typebox`, and `node:*` are provided by
 * the Pi runtime when this extension is loaded — this repository is a Go
 * project with no node_modules, so the TypeScript language server cannot
 * resolve them. These declarations exist ONLY so the editor can type-check
 * this directory; they are never loaded by Pi (files under `types/` are not
 * auto-discovered extensions) and are deliberately conservative (`any`
 * where the real types come from the Pi runtime). The authoritative check
 * for this extension is `pi` execution, not the language server.
 */

declare module "@earendil-works/pi-coding-agent" {
	export interface ToolResultContent {
		type: string;
		text: string;
	}
	export interface ToolResult {
		content: ToolResultContent[];
		details: Record<string, unknown>;
	}
	export interface ExtensionAPI {
		registerTool(definition: {
			name: string;
			label?: string;
			description: string;
			promptSnippet?: string;
			promptGuidelines?: string[];
			parameters?: unknown;
			execute?: (
				toolCallId: string,
				// biome-ignore lint/suspicious/noExplicitAny: real types come from the Pi runtime (see file header)
				params: any,
				signal?: unknown,
				onUpdate?: unknown,
				ctx?: unknown,
			) => Promise<ToolResult> | ToolResult;
		}): void;
	}
}

declare module "typebox" {
	export const Type: {
		Object(schema: Record<string, unknown>): Record<string, unknown>;
		String(props?: Record<string, unknown>): Record<string, unknown>;
		Integer(props?: Record<string, unknown>): Record<string, unknown>;
		Optional(type: Record<string, unknown>): Record<string, unknown>;
	};
}

declare module "node:fs" {
	export function readFileSync(path: string | URL, encoding: "utf-8"): string;
}
