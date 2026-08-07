#!/usr/bin/env python3
"""UI routing-quality gate (Z13): every scenario in KitV2/ui-kit/scenarios.json
must hold under the REAL runtime scoring, and the two routing corpora must
stay disjoint (the non-pollution proof).

The gate runs .agent/router/run_ui_scenarios.mjs with node — that runner
builds the UI index with kit-ui-router-core.ts (the exact module the
search_ui_kit_resources tool uses) and scores with kit-resource-router-scoring.ts
(the ONE scoring implementation), so the verification is scoring-faithful by
construction: no re-scored or re-built copy can drift. If node is unavailable
the gate is skipped with a PARTIAL message (missing tool = PARTIAL, never
PASS).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / ".agent" / "router" / "run_ui_scenarios.mjs"

CONTRACT = {
    "schema": 1,
    "scenarios": [
        {
            "query": "wails desktop app login screen design",
            "expect": ["login"],
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


@unittest.skipUnless(shutil.which("node"), "node not found — UI routing gate PARTIAL")
class UiRoutingScenarios(unittest.TestCase):
    def test_all_scenarios_pass(self) -> None:
        result = run_gate()
        if result.returncode != 0:
            self.fail(
                f"ui routing scenarios gate failed:\n{result.stdout}\n{result.stderr}"
            )
        summary = [
            line
            for line in result.stdout.splitlines()
            if "ui router scenarios:" in line
        ]
        self.assertTrue(
            summary,
            f"runner produced no summary line:\n{result.stdout}",
        )
        self.assertIn("PASS", summary[-1])

    def test_unreachable_expectation_fails(self) -> None:
        """The tripwire must fire on an unreachable expectation (a broken UI
        contract is a real defect, not decoration)."""
        contract = json.loads(json.dumps(CONTRACT))
        contract["scenarios"] = [
            {
                "query": "bounded worker pool errgroup goroutines",  # off-domain
                "expect": ["login"],  # ... so login can never rank
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
        not in the UI index (stale contract linkage)."""
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
