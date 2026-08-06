#!/usr/bin/env python3
"""Routing-quality gate (Z11): every scenario in KitV2/router/scenarios.json
must hold under the REAL runtime scoring.

The gate runs .agent/router/run_scenarios.mjs with node — that runner imports
kit-resource-router-scoring.ts (the exact module the search_kit_resources tool
uses), so the verification is scoring-faithful by construction: no re-scored
copy can drift. If node is unavailable the gate is skipped with a PARTIAL
message, mirroring the template-build check (missing tool = PARTIAL, never
PASS).

Covers:
- new-wave micro-expertise routing (naming, channel ownership, zero value…),
- core routing (worker pool, error wrapping, graceful shutdown, rest chi),
- explicit-library routing (catalog fiche surfaces),
- off-domain rejection (empty-over-noise).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / ".agent" / "router" / "run_scenarios.mjs"

CONTRACT = {
    "schema": 1,
    "scenarios": [
        {
            "query": "go naming conventions package names",
            "expect": ["naming"],
        },
    ],
}


def run_gate(scenarios_path: str | None = None) -> subprocess.CompletedProcess[str]:
    command = ["node", "--no-warnings", str(RUNNER)]
    if scenarios_path is not None:
        command.append(str(scenarios_path))
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )


@unittest.skipUnless(shutil.which("node"), "node not found — routing gate PARTIAL")
class RoutingScenarios(unittest.TestCase):
    def test_all_scenarios_pass(self) -> None:
        result = run_gate()
        if result.returncode != 0:
            self.fail(
                f"routing scenarios gate failed:\n{result.stdout}\n{result.stderr}"
            )
        # The runner prints a trailing summary line: "router scenarios: N/M PASS".
        summary = [
            line for line in result.stdout.splitlines() if "router scenarios:" in line
        ]
        self.assertTrue(
            summary,
            f"runner produced no summary line:\n{result.stdout}",
        )
        self.assertIn("PASS", summary[-1])

    def test_unreachable_expectation_fails(self) -> None:
        """The gate must FAIL when an expectation cannot rank — a broken
        contract is a real defect, not decoration. This is the "good test
        fails" proof: the tripwire fires on an unreachable expectation."""
        contract = json.loads(json.dumps(CONTRACT))
        contract["scenarios"] = [
            {
                "query": "quantum computing compiler",  # off-domain: no resources
                "expect": ["naming"],  # ... so naming can never rank
            }
        ]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(contract, handle)
            path = handle.name
        try:
            result = run_gate(path)
        finally:
            Path(path).unlink(missing_ok=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)

    def test_missing_expected_id_fails(self) -> None:
        """The gate must FAIL when a scenario references a resource that is
        not in the index (stale contract linkage)."""
        contract = json.loads(json.dumps(CONTRACT))
        contract["scenarios"][0]["expect"] = ["does-not-exist"]
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(contract, handle)
            path = handle.name
        try:
            result = run_gate(path)
        finally:
            Path(path).unlink(missing_ok=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("does-not-exist", result.stdout)


if __name__ == "__main__":
    unittest.main()
