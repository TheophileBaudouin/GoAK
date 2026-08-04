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
 * Search = BM25 (k1=1.2, b=0.75) over the precomputed terms of each resource
 * description, plus a small query-time synonym expansion (runtime-only by
 * design — see metaproject contract Z11). Stopwords come from meta.json so
 * the builder and the runtime cannot drift apart.
 */

import { readFileSync } from "node:fs";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

interface Resource {
	id: string;
	kind: string;
	path: string;
	description: string;
	tags: string[];
	terms: string[];
}

interface IndexFile {
	schema: number;
	resources: Resource[];
}

interface MetaFile {
	schema: number;
	version: string;
	index_sha256: string;
	counts: Record<string, number>;
	stopwords: string[];
}

// Query-time expansion only: synonyms live exclusively in the runtime.
// Bilingual (the kit content is mostly English, the user may think French).
const SYNONYMS: Record<string, string[]> = {
	api: ["http", "rest", "web", "endpoint", "handler"],
	rest: ["api", "http", "web", "endpoint"],
	http: ["api", "rest", "web", "net", "handler"],
	web: ["http", "api", "rest", "frontend"],
	endpoint: ["api", "handler", "route"],
	route: ["router", "http", "api"],
	db: ["database", "sql", "sqlite", "query"],
	database: ["sql", "sqlite", "db", "query", "data"],
	sql: ["database", "db", "sqlite", "query"],
	sqlite: ["database", "db", "sql"],
	cli: ["command", "terminal", "flag", "cobra"],
	command: ["cli", "terminal", "flag"],
	tui: ["terminal", "interactive", "cli", "bubbletea"],
	interactive: ["tui", "terminal", "cli"],
	log: ["logging", "slog", "observability"],
	logging: ["log", "slog", "observability"],
	observability: ["logging", "metrics", "tracing", "slog"],
	config: ["configuration", "viper", "koanf", "env"],
	configuration: ["config", "viper", "koanf"],
	worker: ["pool", "concurrency", "goroutine", "errgroup", "parallel"],
	concurrency: ["worker", "goroutine", "errgroup", "parallel", "async"],
	goroutine: ["concurrency", "worker", "go"],
	errgroup: ["concurrency", "worker", "pool"],
	cancel: ["context", "timeout", "shutdown"],
	timeout: ["context", "cancel", "shutdown", "retry"],
	shutdown: ["graceful", "signal", "cancel"],
	graceful: ["shutdown", "signal"],
	retry: ["timeout", "backoff", "resilience"],
	grpc: ["rpc", "proto", "server"],
	rpc: ["grpc", "server", "client"],
	server: ["http", "grpc", "rpc", "api"],
	test: ["testing", "unit", "table", "benchmark"],
	testing: ["test", "unit", "verify"],
	template: ["scaffold", "project", "bootstrap"],
	scaffold: ["template", "project", "bootstrap"],
	json: ["marshal", "serialize", "encoding"],
	context: ["cancel", "timeout", "deadline"],
	security: ["auth", "vuln", "gosec", "secret"],
	auth: ["security", "token", "login"],
	deploy: ["container", "docker", "release", "ci"],
	docker: ["container", "deploy"],
	container: ["docker", "deploy"],
	source: ["offline", "bundle", "reference", "documentation"],
	offline: ["source", "bundle", "toolchain"],
	codegen: ["generate", "sqlc", "templ", "proto"],
	generate: ["codegen", "sqlc", "templ"],
	sqlc: ["database", "sql", "codegen"],
	kafka: ["messaging", "message", "broker", "event", "streaming", "queue"],
	messaging: ["message", "broker", "queue", "kafka", "event"],
	message: ["messaging", "broker", "queue", "publish"],
	broker: ["messaging", "message", "queue", "kafka"],
	queue: ["messaging", "broker", "message"],
	streaming: ["messaging", "stream", "kafka", "event"],
	event: ["messaging", "event-driven", "kafka"],
	publish: ["messaging", "message", "subscribe"],
	subscribe: ["messaging", "message", "consumer"],
	producer: ["messaging", "publish", "kafka"],
	consumer: ["messaging", "subscribe", "kafka"],
	// French → English helpers
	base: ["database", "db", "sql"],
	donnees: ["database", "data", "db"],
	concurrence: ["concurrency", "worker", "goroutine"],
	requete: ["query", "sql", "database"],
	serveur: ["server", "http"],
	tache: ["task", "worker"],
	erreur: ["error", "errors"],
	securite: ["security", "auth"],
	deploiement: ["deploy", "container", "docker"],
};

const TOKEN_RE = /[a-z0-9]+/g;
const BM25_K1 = 1.2;
const BM25_B = 0.75;
const MAX_RESULTS = 8;
const DEFAULT_RESULTS = 5;
const DESC_SNIPPET = 200;
// Canonical resources beat conditional catalogs for generic queries (Z11
// routing-quality bar): rules/recipes/patterns answer the task directly,
// catalog/source entries often only document an explicitly requested library.
const KIND_WEIGHT: Record<string, number> = {
	rule: 1.1,
	recipe: 1.15,
	pattern: 1.05,
};
// Conditional entries say they apply only when the library is explicitly
// requested — they must not outrank the canonical recipe for a generic query.
const CONDITIONAL_RE = /explicitly requires|consider when|consider only/i;
// Off-domain guard: when more than half of the expanded query terms exist in
// no document, the query is probably outside the kit — return nothing rather
// than a weak false positive (empty-over-noise rule). Synonyms count in the
// expanded set because they are the kit's domain bridge: a query whose terms
// can be mapped into corpus vocabulary is in-domain (e.g. "kafka producer
// consumer streaming"), one that cannot is rejected (e.g. "quantum computing
// compiler").
const MAX_ZERO_COVERAGE = 0.5;

function tokenize(text: string, stopwords: Set<string>): string[] {
	const out: string[] = [];
	for (const match of text.toLowerCase().matchAll(TOKEN_RE)) {
		const token = match[0];
		if (token.length >= 2 && !stopwords.has(token)) out.push(token);
	}
	return out;
}

function expandQuery(tokens: string[]): string[] {
	const expanded = new Set(tokens);
	for (const token of tokens) {
		for (const synonym of SYNONYMS[token] ?? []) expanded.add(synonym);
	}
	return [...expanded];
}

interface Scored {
	resource: Resource;
	score: number;
	matched: string[];
}

function bm25(
	resources: Resource[],
	queryTokens: string[],
	k1: number,
	b: number,
): { results: Scored[]; offDomain: boolean } {
	const n = resources.length;
	if (n === 0) return { results: [], offDomain: false };
	const df = new Map<string, number>();
	const docLen: number[] = [];
	let sumLen = 0;
	for (const resource of resources) {
		const seen = new Set<string>();
		for (const term of resource.terms) {
			if (!seen.has(term)) {
				seen.add(term);
				df.set(term, (df.get(term) ?? 0) + 1);
			}
		}
		docLen.push(resource.terms.length);
		sumLen += resource.terms.length;
	}
	const avgLen = sumLen / n;
	const idf = (term: string): number =>
		Math.log(1 + (n - (df.get(term) ?? 0) + 0.5) / ((df.get(term) ?? 0) + 0.5));

	const zeroCoverage = queryTokens.filter((term) => !df.has(term)).length;
	const offDomain =
		queryTokens.length > 0 &&
		zeroCoverage / queryTokens.length > MAX_ZERO_COVERAGE;

	const results: Scored[] = [];
	for (let i = 0; i < n; i++) {
		const resource = resources[i];
		const freq = new Map<string, number>();
		for (const term of resource.terms) {
			freq.set(term, (freq.get(term) ?? 0) + 1);
		}
		let score = 0;
		const matched: string[] = [];
		for (const term of queryTokens) {
			const f = freq.get(term);
			if (!f) continue;
			const denom = f + k1 * (1 - b + (b * docLen[i]) / avgLen);
			score += idf(term) * ((f * (k1 + 1)) / denom);
			matched.push(term);
		}
		if (score > 0) {
			const weight = KIND_WEIGHT[resource.kind] ?? 1;
			const conditional = CONDITIONAL_RE.test(resource.description) ? 0.6 : 1;
			results.push({
				resource,
				score: score * weight * conditional,
				matched,
			});
		}
	}
	results.sort((a, z) => z.score - a.score);
	return { results, offDomain };
}

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
	results: Scored[],
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
			"Use search_kit_resources before planning or implementing a technical task to find which kit rules, recipes, or catalogs apply; then read the returned paths (never the whole kit) before relying on content.",
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
			const stopwords = new Set(meta.stopwords);
			const queryTokens = expandQuery(tokenize(params.query, stopwords));
			const { results, offDomain } = bm25(
				index.resources,
				queryTokens,
				BM25_K1,
				BM25_B,
			);
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
