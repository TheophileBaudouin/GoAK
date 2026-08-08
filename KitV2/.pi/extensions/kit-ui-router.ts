/**
 * Kit UI Router — Pi native tool `search_ui_kit_resources`.
 *
 * READ-ONLY companion of `search_kit_resources` for the ui-kit zone (pinned
 * ui-agent-kit SDK). It answers UI/interface queries (Wails/React screens,
 * components, styling, accessibility, UX) with a compact top-K of ui-kit
 * resources — NEVER Go resources. The two corpora are separate routing
 * domains: this tool only ever reads `ui-kit/`, and the Go tool only
 * ever reads `router/`. It never writes, never rebuilds anything, and never
 * loads kit file contents into the index.
 *
 * Index construction lives in `kit-ui-router-core.ts` (single source, shared
 * with the routing-quality gate); scoring reuses `kit-resource-router-scoring.ts`
 * (the ONE scoring implementation) with the shipped stopwords read from
 * `router/meta.json`.
 */

/// <reference lib="es2022" />
/// <reference path="./types/pi-env.d.ts" />

import { readFileSync } from "node:fs";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import {
	DESC_SNIPPET,
	DEFAULT_RESULTS,
	MAX_RESULTS,
	runSearch,
	tokenize,
	type MetaFile,
} from "./shared/kit-resource-router-scoring.js";
import { buildUiIndex, uiKitPresent } from "./shared/kit-ui-router-core.js";

function loadStopwords(routerDir: URL): string[] {
	let meta: MetaFile;
	try {
		meta = JSON.parse(
			readFileSync(new URL("meta.json", routerDir), "utf-8"),
		) as MetaFile;
	} catch (error) {
		throw new Error(
			`invalid router meta.json: ${
				error instanceof Error ? error.message : String(error)
			}`,
		);
	}
	return meta.stopwords ?? [];
}

function formatResults(
	query: string,
	results: ReturnType<typeof runSearch>["results"],
	limit: number,
	counts: Record<string, number>,
): string {
	if (results.length === 0) {
		return [
			`No ui-kit resource matches "${query}".`,
			"The UI SDK has no directly relevant resource for this query.",
			"Reformulate with UI-specific terms (screen, component, rule, pattern), or conclude that no ui-kit resource applies.",
		].join("\n");
	}
	const lines: string[] = [];
	lines.push(
		`UI kit search: "${query}" → ${results.length} match(es), showing top ${Math.min(limit, results.length)}.`,
	);
	for (const hit of results.slice(0, limit)) {
		lines.push(
			`\n[${hit.resource.kind}] ${hit.resource.id} (score ${hit.score.toFixed(2)})`,
		);
		lines.push(`path: ${hit.resource.path}`);
		lines.push(`matched terms: ${hit.matched.slice(0, 10).join(", ")}`);
		const snippet = hit.resource.description.replace(/\s+/g, " ").trim();
		lines.push(
			snippet.length > DESC_SNIPPET
				? `${snippet.slice(0, DESC_SNIPPET)}…`
				: snippet,
		);
	}
	lines.push(
		`\nUI kit coverage: ${Object.entries(counts)
			.map(([kind, count]) => `${kind} ${count}`)
			.join(" · ")}.`,
	);
	lines.push(
		"For Wails projects: read ui-kit/AGENTS.md before interface work; the UI skills activate when working inside frontend/.",
	);
	return lines.join("\n");
}

export default function (pi: ExtensionAPI) {
	pi.registerTool({
		name: "search_ui_kit_resources",
		label: "Search ui-agent-kit resources",
		description:
			"Find which ui-agent-kit SDK resources (ui-rules, patterns, UX memory, design skills, component index, Wails constraints) are relevant to a UI task in a Wails desktop project (Go + React frontend). Returns a compact top-K with paths, matched terms, and short descriptions — never full files. Call it BEFORE writing any interface code in a Wails project; it routes to the UI corpus only, never to Go resources. If the project has no Wails frontend (no wails.json + frontend/), the UI corpus does not apply.",
		promptSnippet:
			"Find the ui-agent-kit resources relevant to a UI task (compact top-K with paths)",
		promptGuidelines: [
			"Before creating or modifying any UI (screens, components, styles, accessibility, UX) in a Wails project, call search_ui_kit_resources with the task's UI terms and read the top matching resource (rule, pattern, or skill) before writing code — this is mandatory, not optional.",
			"For Go backend work use search_kit_resources instead: the two corpora never mix, and a UI resource is never the answer to a Go query (and vice versa).",
			"If search_ui_kit_resources returns no match, say so and proceed with general UI knowledge — do not guess that a ui-kit resource exists.",
		],
		parameters: Type.Object({
			query: Type.String({
				description:
					"What the agent is looking for in the UI SDK: 3–8 technical terms in English, one concern per query. Example: 'wails login screen keyboard navigation'.",
				minLength: 3,
				maxLength: 300,
			}),
			limit: Type.Optional(
				Type.Integer({
					description:
						"Max results to return (1–8, default 5). Keep small to protect context.",
					minimum: 1,
					maximum: MAX_RESULTS,
					default: DEFAULT_RESULTS,
				}),
			),
		}),
		async execute(_toolCallId, params) {
			const uiKitDir = new URL("../../ui-kit/", import.meta.url);
			const routerDir = new URL("../../router/", import.meta.url);
			if (!uiKitPresent(uiKitDir.pathname)) {
				return {
					content: [
						{
							type: "text",
							text: "No ui-kit SDK zone found at the kit root — this install does not ship the UI corpus. Go tasks are served by search_kit_resources.",
						},
					],
					details: { matched: 0 },
				};
			}
			let index;
			let counts;
			try {
				({ index, counts } = buildUiIndex(
					uiKitDir.pathname,
					loadStopwords(routerDir),
					tokenize,
				));
			} catch (error) {
				throw new Error(
					`cannot build the ui-kit index: ${
						error instanceof Error ? error.message : String(error)
					}`,
				);
			}
			const meta: MetaFile = {
				schema: 1,
				version: "ui-kit",
				index_sha256: "",
				counts,
				stopwords: loadStopwords(routerDir),
			};
			const { results, offDomain } = runSearch(params.query, index, meta);
			const limit = Math.min(params.limit ?? DEFAULT_RESULTS, MAX_RESULTS);
			return {
				content: [
					{
						type: "text",
						text: offDomain
							? `No ui-kit resource matches "${params.query}" — the query appears outside the UI SDK's domain (most terms have no coverage). Reformulate with UI-specific terms or conclude that no ui-kit resource applies.`
							: formatResults(params.query, results, limit, counts),
					},
				],
				details: { matched: offDomain ? 0 : results.length },
			};
		},
	});
}
