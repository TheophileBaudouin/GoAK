/**
 * Kit Resource Router — Pi native tool `search_kit_resources`.
 *
 * READ-ONLY runtime for the shipped router index (KitV2/router/). It finds
 * which kit resources (rules, recipes, catalogs, patterns, anti-patterns,
 * sources, snippets, prompts, skills) help with a task, returning a compact
 * top-K with paths, matched terms, and short descriptions. It NEVER writes,
 * never rebuilds anything, and never reads kit file contents — the source of
 * truth stays the kit files, and this tool only routes to them.
 *
 * Scoring lives in `kit-resource-router-scoring.ts` (single source shared
 * with the metaproject routing-quality gate — see router/scenarios.json).
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
	type IndexFile,
	type MetaFile,
} from "./shared/kit-resource-router-scoring.js";

function loadIndex(dir: URL): { index: IndexFile; meta: MetaFile } {
	let index: IndexFile;
	let meta: MetaFile;
	try {
		index = JSON.parse(
			readFileSync(new URL("index.json", dir), "utf-8"),
		) as IndexFile;
	} catch (error) {
		throw new Error(
			`invalid router index.json: ${
				error instanceof Error ? error.message : String(error)
			}`,
		);
	}
	try {
		meta = JSON.parse(
			readFileSync(new URL("meta.json", dir), "utf-8"),
		) as MetaFile;
	} catch (error) {
		throw new Error(
			`invalid router meta.json: ${
				error instanceof Error ? error.message : String(error)
			}`,
		);
	}
	return { index, meta };
}

function formatResults(
	query: string,
	results: ReturnType<typeof runSearch>["results"],
	limit: number,
	counts: Record<string, number>,
	version: string,
): string {
	if (results.length === 0) {
		return [
			`No kit resource matches "${query}".`,
			"The kit has no directly relevant resource for this query.",
			"Reformulate with Go-specific technical terms, or conclude that no kit resource applies.",
		].join("\n");
	}
	const lines: string[] = [];
	lines.push(
		`Kit search: "${query}" → ${results.length} match(es), showing top ${Math.min(limit, results.length)} (index v${version}).`,
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
		`\nIndex coverage: ${Object.entries(counts)
			.map(([kind, count]) => `${kind} ${count}`)
			.join(" · ")}.`,
	);
	return lines.join("\n");
}

export default function (pi: ExtensionAPI) {
	pi.registerTool({
		name: "search_kit_resources",
		label: "Search kit resources",
		description:
			"Find which Go Agent Kit resources (rules, recipes, catalogs, patterns, anti-patterns, sources, snippets, prompts, skills) are relevant to a task. Returns a compact top-K with paths, matched terms, and short descriptions — never full files. Call it BEFORE planning or implementing technical work to route to the right kit resource instead of scanning the kit tree. Use the returned paths to read only the relevant files; the index only routes, the kit files stay the source of truth.",
		promptSnippet:
			"Find the kit resources relevant to a task (compact top-K with paths)",
		promptGuidelines: [
			"Before planning or implementing any Go code, call search_kit_resources with the task's technical terms and read the top matching resource (rule, recipe, pattern, or catalog) before writing — this is mandatory, not optional.",
			"search_kit_resources applies by default on every Go task: naming conventions (rule naming), error wrapping (pattern error-wrapping-chain), channel ownership (pattern concurrency-channel-ownership), and zero-value design (pattern go-zero-value-valid) govern ordinary Go code even when the user does not name them.",
			"If search_kit_resources returns no match, say so and proceed with general Go knowledge — do not guess that a kit resource exists.",
		],
		parameters: Type.Object({
			query: Type.String({
				description:
					"What the agent is looking for: 3–8 technical terms in English, one concern per query. Example: 'bounded worker pool with context cancellation'.",
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
			const dir = new URL("../../router/", import.meta.url);
			let index: IndexFile;
			let meta: MetaFile;
			try {
				({ index, meta } = loadIndex(dir));
			} catch (error) {
				throw new Error(
					`Kit router index not found or unreadable at ${dir}: ${
						error instanceof Error ? error.message : String(error)
					}`,
				);
			}
			const { results, offDomain } = runSearch(params.query, index, meta);
			const limit = Math.min(params.limit ?? DEFAULT_RESULTS, MAX_RESULTS);
			return {
				content: [
					{
						type: "text",
						text: offDomain
							? `No kit resource matches "${params.query}" — the query appears outside the kit's domain (most terms have no coverage). Reformulate with Go-specific terms or conclude that no kit resource applies.`
							: formatResults(
									params.query,
									results,
									limit,
									meta.counts,
									meta.version,
								),
					},
				],
				details: { matched: offDomain ? 0 : results.length },
			};
		},
	});
}
