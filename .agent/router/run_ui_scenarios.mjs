#!/usr/bin/env node
/**
 * UI routing-quality gate (Z13 scenarios).
 *
 * Runs every scenario in KitV2/ui-kit/scenarios.json against the UI routing
 * corpus built the same way the runtime tool builds it — `buildUiIndex` from
 * kit-ui-router-core.ts with `tokenize` from kit-resource-router-scoring.ts
 * (the ONE scoring implementation) and the shipped stopwords from
 * router/meta.json — so the gate verifies exactly what
 * `search_ui_kit_resources` returns. No scoring or index-construction
 * re-implementation anywhere.
 *
 * The gate ALSO asserts corpus disjointness, the "non-pollution" proof:
 *   - every UI index path is under ui-kit/, and
 *   - the Go index (router/index.json) contains no ui-kit/ path.
 *
 * Usage:
 *   node --no-warnings .agent/router/run_ui_scenarios.mjs [scenarios.json]
 *
 * An optional first argument overrides the scenarios file (used by the
 * negative gate tests to prove the tripwire fires).
 *
 * Requires Node with native TypeScript type stripping (>= 23.6; on 22.x pass
 * --experimental-strip-types).
 *
 * Exit 0 when every expectation holds, 1 otherwise. Off-domain scenarios
 * must be rejected (empty-over-noise); normal scenarios must surface every
 * expected id within the top-K (default 5, scenario `top` overrides).
 */

import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";
import { runSearch, tokenize } from "../../KitV2/.pi/extensions/shared/kit-resource-router-scoring.ts";
import { buildUiIndex } from "../../KitV2/.pi/extensions/shared/kit-ui-router-core.ts";

const ROOT = new URL("../../KitV2/router/", import.meta.url);
const UI_KIT = new URL("../../KitV2/ui-kit/", import.meta.url);
const scenariosArg = process.argv[2];

function loadJson(file, what, base) {
	try {
		return JSON.parse(readFileSync(new URL(file, base), "utf-8"));
	} catch (error) {
		console.error(
			`ui router scenarios: cannot load ${what} (${file}):`,
			error.message,
		);
		process.exit(1);
	}
}

const goMeta = loadJson("meta.json", "meta", ROOT);
const goIndex = loadJson("index.json", "index", ROOT);
const contract = scenariosArg
	? loadJson(
			resolve(scenariosArg),
			"ui scenarios contract",
			pathToFileURL(process.cwd() + "/"),
		)
	: loadJson("scenarios.json", "ui scenarios contract", UI_KIT);

const { index, counts } = buildUiIndex(
	UI_KIT.pathname,
	goMeta.stopwords,
	tokenize,
);
const uiMeta = {
	schema: 1,
	version: "ui-kit",
	index_sha256: "",
	counts,
	stopwords: goMeta.stopwords,
};

const failures = [];
const byId = new Map(index.resources.map((r) => [r.id, r]));

// --- disjointness: the non-pollution proof --------------------------------
for (const resource of index.resources) {
	if (!resource.path.startsWith("ui-kit/")) {
		failures.push({
			query: "(disjointness)",
			reason: `UI index contains a non-ui-kit path: ${resource.path}`,
		});
	}
}
for (const resource of goIndex.resources) {
	if (String(resource.path).startsWith("ui-kit/")) {
		failures.push({
			query: "(disjointness)",
			reason: `Go index contains a UI path: ${resource.path} (id ${resource.id})`,
		});
	}
}

let passed = 0;
for (const scenario of contract.scenarios) {
	const query = scenario.query;
	const expect = scenario.expect ?? [];
	const top = scenario.top ?? 5;
	const { results, offDomain } = runSearch(query, index, uiMeta);
	const topIds = results.slice(0, top).map((h) => h.resource.id);
	const missing = expect.filter((id) => !topIds.includes(id));

	let ok = true;
	let reason = "";
	if (scenario.offDomain) {
		ok = offDomain;
		reason = ok
			? "rejected as off-domain (empty-result message)"
			: `off-domain guard failed: offDomain=${offDomain}, ${results.length} result(s)`;
	} else if (missing.length > 0) {
		ok = false;
		reason = `expected ${missing.join(", ")} not in top-${top} (got: ${topIds.join(", ") || "no match"})`;
	}
	for (const id of expect) {
		if (!byId.has(id)) {
			ok = false;
			reason = `expected id '${id}' does not exist in the UI index`;
		}
	}
	if (ok) {
		passed += 1;
		console.log(`PASS  "${query}" -> ${topIds.join(", ") || "(empty)"}`);
	} else {
		failures.push({ query, reason });
		console.log(`FAIL  "${query}": ${reason}`);
	}
}

console.log(
	`\nui router scenarios: ${passed}/${contract.scenarios.length} PASS (${index.resources.length} ui-kit resources)`,
);
if (failures.length > 0) {
	for (const f of failures) console.log(`disjoint/contract issue: ${f.query} — ${f.reason}`);
	process.exit(1);
}
process.exit(0);
