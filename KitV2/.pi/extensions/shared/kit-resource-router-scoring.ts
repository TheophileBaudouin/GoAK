/**
 * Kit Resource Router — shared scoring core.
 *
 * Pure, dependency-free BM25 routing logic shared between:
 *  - the Pi extension `kit-resource-router.ts` (runtime tool), and
 *  - the metaproject routing-quality gate (`run_scenarios.mjs`).
 *
 * Single source of truth for tokenize/expandQuery/bm25 and every constant
 * that influences ranking. The extension and the gate therefore CANNOT
 * drift apart: a scenario verifies the exact scoring the agent sees.
 * Imports nothing (no Pi API, no typebox) so it runs under plain Node.
 */

export interface Resource {
	id: string;
	kind: string;
	path: string;
	description: string;
	tags: string[];
	terms: string[];
}

export interface IndexFile {
	schema: number;
	resources: Resource[];
}

export interface MetaFile {
	schema: number;
	version: string;
	index_sha256: string;
	counts: Record<string, number>;
	stopwords: string[];
}

export const TOKEN_RE = /[a-z0-9]+/g;
export const BM25_K1 = 1.2;
export const BM25_B = 0.75;
export const MAX_RESULTS = 8;
export const DEFAULT_RESULTS = 5;
export const DESC_SNIPPET = 200;
// Canonical resources beat conditional catalogs for generic queries (Z11
// routing-quality bar): rules/recipes/patterns answer the task directly,
// catalog/source entries often only document an explicitly requested library.
export const KIND_WEIGHT: Record<string, number> = {
	rule: 1.1,
	recipe: 1.15,
	pattern: 1.05,
};
// Conditional entries say they apply only when the library is explicitly
// requested — they must not outrank the canonical recipe for a generic query.
export const CONDITIONAL_RE =
	/explicitly requires|consider when|consider only/i;
// Off-domain guard: when more than half of the expanded query terms exist in
// no document, the query is probably outside the kit — return nothing rather
// than a weak false positive (empty-over-noise rule). Synonyms count in the
// expanded set because they are the kit's domain bridge: a query whose terms
// can be mapped into corpus vocabulary is in-domain (e.g. "kafka producer
// consumer streaming"), one that cannot is rejected (e.g. "quantum computing
// compiler").
export const MAX_ZERO_COVERAGE = 0.5;

// Query-time expansion only: synonyms live exclusively in the runtime.
// Bilingual (the kit content is mostly English, the user may think French).
export const SYNONYMS: Record<string, string[]> = {
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

export function tokenize(text: string, stopwords: Set<string>): string[] {
	const out: string[] = [];
	for (const match of text.toLowerCase().matchAll(TOKEN_RE)) {
		const token = match[0];
		if (token.length >= 2 && !stopwords.has(token)) out.push(token);
	}
	return out;
}

export function expandQuery(tokens: string[]): string[] {
	const expanded = new Set(tokens);
	for (const token of tokens) {
		for (const synonym of SYNONYMS[token] ?? []) expanded.add(synonym);
	}
	return [...expanded];
}

export interface Scored {
	resource: Resource;
	score: number;
	matched: string[];
}

export function bm25(
	resources: Resource[],
	queryTokens: string[],
	k1: number,
	b: number,
	domainTokens: string[] = queryTokens,
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

	// Domain rejection is a property of the USER'S vocabulary, not of the
	// recall-boosting synonym expansion: an expansion term that never occurs
	// in the corpus (e.g. a Go-flavored synonym of "message" queried against
	// the UI corpus) must not flip a legitimate in-domain query to
	// off-domain. runSearch therefore passes the raw (pre-expansion) tokens
	// as domainTokens; direct bm25 callers keep the historical behavior.
	const zeroCoverage = domainTokens.filter((term) => !df.has(term)).length;
	const offDomain =
		domainTokens.length > 0 &&
		zeroCoverage / domainTokens.length > MAX_ZERO_COVERAGE;

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

/** Full pipeline used by both the runtime tool and the scenarios gate.
 * Callers slice `results` themselves for their own top-K. */
export function runSearch(
	query: string,
	index: IndexFile,
	meta: MetaFile,
): { results: Scored[]; offDomain: boolean } {
	const stopwords = new Set(meta.stopwords);
	const rawTokens = tokenize(query, stopwords);
	const queryTokens = expandQuery(rawTokens);
	const { results, offDomain } = bm25(
		index.resources,
		queryTokens,
		BM25_K1,
		BM25_B,
		rawTokens,
	);
	return { results, offDomain };
}
