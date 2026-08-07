#!/usr/bin/env node
/**
 * Routing-quality gate (Z11 scenarios).
 *
 * Runs every scenario in KitV2/router/scenarios.json against the REAL
 * runtime scoring (kit-resource-router-scoring.ts — the same module the
 * search_kit_resources tool uses), so the gate verifies exactly what the
 * agent sees. No scoring re-implementation anywhere.
 *
 * Usage:
 *   node --no-warnings .agent/router/run_scenarios.mjs [scenarios.json]
 *
 * An optional first argument overrides the scenarios file (used by the
 * negative gate tests to prove the tripwire fires).
 *
 * Requires Node with native TypeScript type stripping (>= 23.6; on 22.x pass
 * --experimental-strip-types) to import the shared scoring module directly.
 *
 * Exit 0 when every expectation holds, 1 otherwise. Off-domain scenarios
 * must be rejected (empty-over-noise); normal scenarios must surface every
 * expected id within the top-K (default 5, scenario `top` overrides).
 */

import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";
import { runSearch } from "../../KitV2/.pi/extensions/shared/kit-resource-router-scoring.ts";

const ROOT = new URL("../../KitV2/router/", import.meta.url);
const scenariosArg = process.argv[2];

function loadJson(file, what, base) {
	try {
		return JSON.parse(readFileSync(new URL(file, base), "utf-8"));
	} catch (error) {
		console.error(
			`router scenarios: cannot load ${what} (${file}):`,
			error.message,
		);
		process.exit(1);
	}
}

const index = loadJson("index.json", "index", ROOT);
const meta = loadJson("meta.json", "meta", ROOT);
const contract = scenariosArg
	? loadJson(
			resolve(scenariosArg),
			"scenarios contract",
			pathToFileURL(process.cwd() + "/"),
		)
	: loadJson("scenarios.json", "scenarios contract", ROOT);

const byId = new Map(index.resources.map((r) => [r.id, r]));
const failures = [];
let passed = 0;

for (const scenario of contract.scenarios) {
	const query = scenario.query;
	const expect = scenario.expect ?? [];
	const top = scenario.top ?? 5;
	const { results, offDomain } = runSearch(query, index, meta);
	const topIds = results.slice(0, top).map((h) => h.resource.id);
	const missing = expect.filter((id) => !topIds.includes(id));

	let ok = true;
	let reason = "";
	if (scenario.offDomain) {
		// The scoring layer must recognize the query as off-domain; the tool
		// then suppresses the weak matches and shows the empty-result message.
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
			reason = `expected id '${id}' does not exist in the index`;
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
	`\nrouter scenarios: ${passed}/${contract.scenarios.length} PASS (index v${meta.version}, ${index.resources.length} resources)`,
);
process.exit(failures.length === 0 ? 0 : 1);
