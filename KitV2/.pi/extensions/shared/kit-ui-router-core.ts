/**
 * Kit UI Router — shared UI index construction.
 *
 * Pure, dependency-free (node builtins only) builder shared between:
 *  - the Pi extension `kit-ui-router.ts` (runtime tool `search_ui_kit_resources`), and
 *  - the metaproject UI routing-quality gate (`run_ui_scenarios.mjs`).
 *
 * Single source of truth for how the ui-kit zone (pinned ui-agent-kit SDK)
 * becomes a routing index: which files are indexed, their ids, kinds, and
 * descriptions. The Go corpus (`router/index.json`) is never touched — the
 * UI corpus is a separate routing domain by design (Z13 §3.4).
 *
 * The SCORING is not implemented here and the tokenizer is INJECTED by the
 * caller (see `Tokenizer` below), so this module imports nothing
 * runtime-visible: one file serves both runtimes (jiti for the Pi extension,
 * plain node for the gate) — the same reason the shared scoring module
 * imports nothing. Stopwords come from the shipped `router/meta.json`
 * (single source), read by the caller.
 */

import {
	existsSync,
	readFileSync,
	readdirSync,
	statSync,
} from "node:fs";
import { basename, dirname, extname, join, relative, sep } from "node:path";
import type { IndexFile, Resource } from "./kit-resource-router-scoring.js";

export interface UiKitIndex {
	index: IndexFile;
	counts: Record<string, number>;
}

/**
 * The tokenizer comes from the shared scoring module
 * (`kit-resource-router-scoring.ts`), injected by each caller:
 * - the Pi extension imports it with a `.js` specifier (jiti maps to .ts);
 * - the metaproject gate imports it with a `.ts` specifier (node ≥ 23.6
 *   native type stripping).
 * Type-only imports are erased at runtime in both runtimes.
 */
export type Tokenizer = (
	text: string,
	stopwords: Set<string>,
) => string[];

interface Frontmatter {
	name?: string;
	description?: string;
}

/** Extract name + description from a Pi-style frontmatter block. */
export function frontmatterOf(text: string): Frontmatter {
	if (!text.startsWith("---\n")) return {};
	const end = text.indexOf("\n---", 4);
	if (end < 0) return {};
	const block = text.slice(4, end);
	const name = /^name:\s*(.+)$/m.exec(block)?.[1]?.trim();
	const description = /^description:\s*(.+)$/m.exec(block)?.[1]?.trim();
	const strip = (value?: string) =>
		value?.replace(/^["']|["']$/g, "").replace(/\\n/g, " ").trim();
	return { name: name?.trim(), description: strip(description) };
}

/** First H1 heading, or "" when absent. */
export function firstHeading(text: string): string {
	const match = /^#\s+(.+)$/m.exec(text);
	return match?.[1]?.trim() ?? "";
}

/** First meaningful prose lines, collapsed, capped. */
export function intro(text: string, max = 200): string {
	const lines = text
		.split("\n")
		.map((line) => line.trim())
		.filter((line) => line && !line.startsWith("#"));
	return lines.join(" ").replace(/\s+/g, " ").slice(0, max);
}

function listFiles(dir: string): string[] {
	if (!existsSync(dir)) return [];
	const out: string[] = [];
	for (const entry of readdirSync(dir, { withFileTypes: true })) {
		const abs = join(dir, entry.name);
		if (entry.isDirectory()) out.push(...listFiles(abs));
		else out.push(abs);
	}
	return out;
}

const MARKDOWN_DESC_INDEX = 300; // heading + capped intro for .md resources

/**
 * Build the UI routing index from the ui-kit zone.
 *
 * Ids follow a documented convention (Z13 §7): skills use their frontmatter
 * `name`; knowledge .md files use their filename stem; the components index
 * is a single "components" resource. Paths are emitted relative to the
 * zone's parent (e.g. `ui-kit/skills/frontend-design/SKILL.md`) so the gate
 * can assert corpus disjointness (paths ⊆ ui-kit/).
 */
export function buildUiIndex(
	uiKitDir: string,
	stopwords: string[],
	tokenize: Tokenizer,
): UiKitIndex {
	const root = dirname(uiKitDir);
	const stop = new Set(stopwords);
	const resources: Resource[] = [];

	const add = (
		kind: string,
		absPath: string,
		description: string,
		id?: string,
	): void => {
		const rel = relative(root, absPath).split(sep).join("/");
		const rid =
			id ?? (kind === "skill" ? rel.split("/")[2] : basename(rel, extname(rel)));
		const tags: string[] = [];
		const terms = tokenize(`${rid} ${description} ${tags.join(" ")}`, stop);
		resources.push({
			id: rid,
			kind,
			path: rel,
			description,
			tags,
			terms,
		});
	};

	// skills/*/SKILL.md — Pi-native skills (frontmatter description)
	for (const dir of listFiles(join(uiKitDir, "skills"))) {
		if (basename(dir) !== "SKILL.md") continue;
		const text = readFileSync(dir, "utf-8");
		const fm = frontmatterOf(text);
		const description =
			fm.description ??
			`${firstHeading(text)} — ${intro(text, MARKDOWN_DESC_INDEX)}`;
		add("skill", dir, description, fm.name ?? basename(dirname(dir)));
	}

	// ui-rules/ patterns/ ux/ — knowledge .md files
	for (const [zone, kind] of [
		["ui-rules", "rule"],
		["patterns", "pattern"],
		["ux", "ux"],
	] as const) {
		for (const file of listFiles(join(uiKitDir, zone))) {
			if (!file.endsWith(".md")) continue;
			const text = readFileSync(file, "utf-8");
			add(kind, file, `${firstHeading(text)} — ${intro(text, MARKDOWN_DESC_INDEX)}`);
		}
	}

	// docs/ and ui-sdk/docs/ — background docs (design systems, Wails
	// constraints, consumption contract). docs/authoring-guides/ is
	// deliberately NOT indexed: those files describe how to WRITE new rules/
	// patterns (meta-docs), and their intro prose drowns design queries
	// (e.g. "spacing/typography" matching ui-rules-file). They remain in the
	// tree and reachable by reading the docs resources.
	for (const sub of ["docs", join("ui-sdk", "docs")]) {
		for (const file of listFiles(join(uiKitDir, sub))) {
			if (!file.endsWith(".md")) continue;
			if (relative(join(uiKitDir, sub), file).includes("authoring-guides")) {
				continue;
			}
			const text = readFileSync(file, "utf-8");
			add("doc", file, `${firstHeading(text)} — ${intro(text, MARKDOWN_DESC_INDEX)}`);
		}
	}

	// ui-sdk/components-index.md — single routing resource for the component catalog
	const componentsIndex = join(uiKitDir, "ui-sdk", "components-index.md");
	if (existsSync(componentsIndex)) {
		const text = readFileSync(componentsIndex, "utf-8");
		add(
			"components",
			componentsIndex,
			`Components index — ${intro(text, MARKDOWN_DESC_INDEX)}`,
			"components-index",
		);
	}

	resources.sort((a, b) => a.id.localeCompare(b.id));
	const counts: Record<string, number> = {};
	for (const resource of resources) {
		counts[resource.kind] = (counts[resource.kind] ?? 0) + 1;
	}
	return { index: { schema: 1, resources }, counts };
}

/** True when the ui-kit zone looks present (defensive guard for the tool). */
export function uiKitPresent(uiKitDir: string): boolean {
	return existsSync(uiKitDir) && statSync(uiKitDir).isDirectory();
}
