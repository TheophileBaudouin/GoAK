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
	export interface SessionStartEvent {
		reason: "startup" | "reload" | "new" | "resume" | "fork";
		previousSessionFile?: string;
	}
	export interface ExtensionUi {
		setWidget(
			key: string,
			lines: string[] | undefined,
			options?: { placement?: string },
		): void;
	}
	export interface ExtensionContext {
		hasUI: boolean;
		mode: "tui" | "rpc" | "json" | "print";
		cwd: string;
		ui: ExtensionUi;
		sessionManager: {
			getEntries(): Array<{
				type: string;
				customType?: string;
				data?: unknown;
			}>;
			getBranch(): Array<{
				type: string;
				customType?: string;
				data?: unknown;
			}>;
		};
	}
	export interface SessionEntry {
		type: string;
		customType?: string;
		data?: unknown;
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
		on(
			event: "session_start",
			handler: (
				event: SessionStartEvent,
				ctx: ExtensionContext,
			) => void | Promise<void>,
		): void;
		appendEntry(customType: string, data?: Record<string, unknown>): void;
		registerEntryRenderer(
			customType: string,
			renderer: (
				entry: SessionEntry,
				options: { expanded: boolean },
				theme: PiTheme,
			) => unknown,
		): void;
	}
	export interface PiTheme {
		bg(color: string, text: string): string;
		fg(color: string, text: string): string;
		bold(text: string): string;
	}
}

declare module "@earendil-works/pi-tui" {
	export class Text {
		constructor(
			content: string,
			paddingX?: number,
			paddingY?: number,
			background?: unknown,
		);
		setText(content: string): void;
	}
	export class Box {
		constructor(
			paddingX?: number,
			paddingY?: number,
			background?: (text: string) => string | undefined,
		);
		addChild(child: unknown): void;
		setBgFn(fn: (text: string) => string | undefined): void;
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
	export function existsSync(path: string | URL): boolean;
	export function statSync(path: string | URL): {
		isDirectory(): boolean;
		isFile(): boolean;
	};
	export function readdirSync(
		path: string | URL,
		options?: { withFileTypes?: boolean },
	): Array<{ name: string; isDirectory(): boolean; isFile(): boolean }>;
}

declare module "node:path" {
	export function basename(path: string, suffix?: string): string;
	export function dirname(path: string): string;
	export function extname(path: string): string;
	export function join(...paths: string[]): string;
	export function relative(from: string, to: string): string;
	export const sep: string;
}
