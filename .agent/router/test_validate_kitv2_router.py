#!/usr/bin/env python3
"""Tests for the product validator's router check (Z7: each new control needs
positive and negative cases). Imports validate-kitv2.py from the product and
runs check_router() against a temp tree with a freshly built index."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from build_index import build as build_index

KIT = Path(__file__).resolve().parents[2] / "KitV2"
VALIDATOR = KIT / "tools" / "validators" / "validate-kitv2.py"

spec = importlib.util.spec_from_file_location("validate_kitv2", VALIDATOR)
if spec is None or spec.loader is None:
    raise SystemExit(f"cannot load validator module from {VALIDATOR}")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)

SKILL = """---
name: {name}
description: "{description}"
category: {category}
tags: [go]
last-verified: 2026-08-05
---

# {name}
"""

PROMPT = """---
name: {name}
description: "{description}"
---

# {name}
"""

YAML_DOC = """---
id: {rid}
title: {title}
kind: Pattern
version: 1
status: active
owner: go-agent-kit
tags: [go]
go_version: "1.25+"
dependencies: []
last_verified: 2026-08-05
problem: >-
  {problem}
"""

SNIPPET = """id: {rid}
purpose: {purpose}
tags: [go]
go_version: "1.25"
dependencies: [stdlib]
"""


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.kit = root / "KitV2"
        (self.kit / "rules" / "core").mkdir(parents=True)
        (self.kit / "knowledge" / "patterns").mkdir(parents=True)
        (self.kit / "snippets" / "snp").mkdir(parents=True)
        (self.kit / ".pi" / "prompts").mkdir(parents=True)
        (self.kit / "manifest.yaml").write_text(
            "name: go-agent-kit-v2\nversion: 2.2.0\nschema_version: 1\n",
            encoding="utf-8",
        )
        (self.kit / "rules" / "core" / "SKILL.md").write_text(
            SKILL.format(
                name="rule-errors",
                description="Handle errors once: sentinel, typed, opaque.",
                category="rule",
            ),
            encoding="utf-8",
        )
        (self.kit / "knowledge" / "patterns" / "p.yaml").write_text(
            YAML_DOC.format(
                rid="pattern:concurrency:pipeline",
                title="Pipeline stages",
                problem="Parallelize sequential stages.",
            ),
            encoding="utf-8",
        )
        (self.kit / "snippets" / "snp" / "SNIPPET.yaml").write_text(
            SNIPPET.format(
                rid="http-json-response",
                purpose="Encode a JSON HTTP response.",
            ),
            encoding="utf-8",
        )
        (self.kit / ".pi" / "prompts" / "workflow-x.md").write_text(
            PROMPT.format(name="workflow-x", description="Plan a task."),
            encoding="utf-8",
        )
        self.router = self.kit / "router"
        build_index(self.kit, self.router, "2.2.0")
        validate.ROOT = self.kit  # type: ignore[attr-defined]

    def tearDown(self) -> None:
        self.tmp.cleanup()
        validate.ROOT = KIT  # type: ignore[attr-defined]

    def test_positive(self) -> None:
        self.assertEqual(validate.check_router(), [])

    def test_missing_index(self) -> None:
        (self.router / "index.json").unlink()
        errors = validate.check_router()
        self.assertTrue(
            any("index.json and meta.json are required" in e for e in errors)
        )

    def test_checksum_drift(self) -> None:
        (self.router / "index.json").write_text(
            (self.router / "index.json")
            .read_text(encoding="utf-8")
            .replace("Pipeline stages", "Pipeline stages edited"),
            encoding="utf-8",
        )
        errors = validate.check_router()
        self.assertTrue(any("checksum" in e for e in errors))

    def test_missing_coverage(self) -> None:
        # a new resource not in the index must be reported
        (self.kit / "recipes").mkdir(parents=True)
        (self.kit / "recipes" / "recipe-new").mkdir()
        (self.kit / "recipes" / "recipe-new" / "SKILL.md").write_text(
            SKILL.format(
                name="recipe-new",
                description="A brand new recipe.",
                category="recipe",
            ),
            encoding="utf-8",
        )
        errors = validate.check_router()
        self.assertTrue(any("index missing" in e for e in errors))

    def test_version_drift(self) -> None:
        (self.router / "meta.json").write_text(
            json.dumps({"version": "9.9.9"}) + "\n",
            encoding="utf-8",
        )
        errors = validate.check_router()
        self.assertTrue(any("does not match manifest version" in e for e in errors))

    def test_stale_entry(self) -> None:
        resources = json.loads(
            (self.router / "index.json").read_text(encoding="utf-8")
        )["resources"]
        resources.append(
            {
                "id": "bogus",
                "kind": "rule",
                "path": "rules/bogus/SKILL.md",
                "description": "stale",
                "tags": [],
                "terms": ["stale"],
            }
        )
        (self.router / "index.json").write_text(
            json.dumps({"schema": 1, "resources": resources}) + "\n",
            encoding="utf-8",
        )
        errors = validate.check_router()
        self.assertTrue(
            any("stale entries" in e or "does not exist" in e for e in errors)
        )


class RouterScenariosFixture(unittest.TestCase):
    """check_router_scenarios: the contract file's schema and id linkage.

    Ranking itself is the metaproject node gate (test_router_scenarios.py);
    here only the shipped contract's integrity is validated (Z7: each new
    control needs positive and negative cases)."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.kit = root / "KitV2"
        self.router = self.kit / "router"
        (self.router).mkdir(parents=True)
        (self.kit / "manifest.yaml").write_text(
            "name: go-agent-kit-v2\nversion: 2.5.0\nschema_version: 1\n",
            encoding="utf-8",
        )
        (self.router / "index.json").write_text(
            json.dumps(
                {
                    "schema": 1,
                    "resources": [
                        {
                            "id": "naming",
                            "kind": "rule",
                            "path": "rules/registry/naming/SKILL.md",
                            "description": "naming conventions",
                            "tags": [],
                            "terms": ["naming"],
                        }
                    ],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.contract = {
            "schema": 1,
            "scenarios": [
                {
                    "query": "go naming conventions package names",
                    "expect": ["naming"],
                },
                {"query": "quantum computing", "expect": [], "offDomain": True},
            ],
        }
        validate.ROOT = self.kit  # type: ignore[attr-defined]

    def tearDown(self) -> None:
        self.tmp.cleanup()
        validate.ROOT = KIT  # type: ignore[attr-defined]

    def write_contract(self) -> None:
        (self.router / "scenarios.json").write_text(
            json.dumps(self.contract) + "\n",
            encoding="utf-8",
        )

    def test_positive(self) -> None:
        self.write_contract()
        self.assertEqual(validate.check_router_scenarios(), [])

    def test_missing_contract(self) -> None:
        errors = validate.check_router_scenarios()
        self.assertTrue(any("missing routing-quality contract" in e for e in errors))

    def test_invalid_json(self) -> None:
        (self.router / "scenarios.json").write_text("{not json", encoding="utf-8")
        errors = validate.check_router_scenarios()
        self.assertTrue(any("invalid JSON" in e for e in errors))

    def test_unresolved_expected_id(self) -> None:
        self.contract["scenarios"][0]["expect"] = ["does-not-exist"]
        self.write_contract()
        errors = validate.check_router_scenarios()
        self.assertTrue(
            any("does-not-exist" in e and "not in the index" in e for e in errors)
        )

    def test_off_domain_with_expect(self) -> None:
        self.contract["scenarios"][1]["expect"] = ["naming"]
        self.write_contract()
        errors = validate.check_router_scenarios()
        self.assertTrue(
            any("off-domain scenario must expect no ids" in e for e in errors)
        )

    def test_bad_query_length(self) -> None:
        self.contract["scenarios"][0]["query"] = "ab"
        self.write_contract()
        errors = validate.check_router_scenarios()
        self.assertTrue(any("3..300 char" in e for e in errors))


class UiKitChecksFixture(unittest.TestCase):
    """Z13 checks: ui-kit skills keep Pi-compatible frontmatter (positive and
    negative), and the Go routing corpus never contains a ui-kit path."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.kit = Path(self.tmp.name)
        (self.kit / "ui-kit" / "skills" / "frontend-design").mkdir(parents=True)
        (self.kit / "router").mkdir(parents=True)
        (self.kit / "ui-kit" / "skills" / "frontend-design" / "SKILL.md").write_text(
            SKILL.format(
                name="frontend-design",
                description="Distinctive visual design guidance for Wails apps.",
                category="rule",
            ),
            encoding="utf-8",
        )
        (self.kit / "ui-kit" / "AGENTS.md").write_text(
            "# ui-agent-kit SDK\n",
            encoding="utf-8",
        )
        (self.kit / "ui-kit" / "PIN.md").write_text(
            "| Pinned commit (SHA) | `f9bdd9b5237a9154f86050e0f5df583c66e2496e` |\n"
            "| Sync date | 2026-08-07 |\n",
            encoding="utf-8",
        )
        (self.kit / "ui-kit" / "ui-sdk" / "components").mkdir(parents=True)
        (self.kit / "ui-kit" / "copy-rules.json").write_text(
            json.dumps([{"src": "ui-sdk/components", "dst": "src/components"}]),
            encoding="utf-8",
        )
        self.index = {
            "schema": 1,
            "resources": [
                {
                    "id": "rule-errors",
                    "kind": "rule",
                    "path": "rules/core/SKILL.md",
                    "description": "Handle errors once.",
                    "tags": [],
                    "terms": ["error"],
                }
            ],
        }
        (self.kit / "router" / "index.json").write_text(
            json.dumps(self.index), encoding="utf-8"
        )
        validate.ROOT = self.kit  # type: ignore[attr-defined]

    def tearDown(self) -> None:
        self.tmp.cleanup()
        validate.ROOT = KIT  # type: ignore[attr-defined]

    def test_ui_skills_positive(self) -> None:
        self.assertEqual(validate.check_ui_kit_skills(), [])

    def test_ui_pin_positive(self) -> None:
        self.assertEqual(validate.check_ui_kit_pin(), [])

    def test_ui_pin_missing_record(self) -> None:
        (self.kit / "ui-kit" / "PIN.md").unlink()
        errors = validate.check_ui_kit_pin()
        self.assertTrue(any("missing pin record" in e for e in errors))

    def test_ui_pin_malformed_sha(self) -> None:
        (self.kit / "ui-kit" / "PIN.md").write_text(
            "| Pinned commit (SHA) | `not-a-sha` |\n| Sync date | 2026-08-07 |\n",
            encoding="utf-8",
        )
        errors = validate.check_ui_kit_pin()
        self.assertTrue(any("well-formed 40-hex" in e for e in errors))

    def test_ui_copy_rules_positive(self) -> None:
        self.assertEqual(validate.check_ui_kit_copy_rules(), [])

    def test_ui_copy_rules_missing_file(self) -> None:
        (self.kit / "ui-kit" / "copy-rules.json").unlink()
        errors = validate.check_ui_kit_copy_rules()
        self.assertTrue(any("missing copy rules" in e for e in errors))

    def test_ui_copy_rules_stale_source(self) -> None:
        (self.kit / "ui-kit" / "copy-rules.json").write_text(
            json.dumps([{"src": "ui-sdk/does-not-exist", "dst": "src/x"}]),
            encoding="utf-8",
        )
        errors = validate.check_ui_kit_copy_rules()
        self.assertTrue(any("missing in the zone" in e for e in errors))

    def test_ui_skills_missing_description(self) -> None:
        path = self.kit / "ui-kit" / "skills" / "frontend-design" / "SKILL.md"
        path.write_text(
            SKILL.format(
                name="frontend-design",
                description="",
                category="rule",
            ),
            encoding="utf-8",
        )
        errors = validate.check_ui_kit_skills()
        self.assertTrue(any("description must be a 1..1024" in e for e in errors))

    def test_ui_skills_name_mismatch(self) -> None:
        path = self.kit / "ui-kit" / "skills" / "frontend-design" / "SKILL.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "name: frontend-design", "name: wrong-name"
            ),
            encoding="utf-8",
        )
        errors = validate.check_ui_kit_skills()
        self.assertTrue(any("name does not match directory" in e for e in errors))

    def test_disjointness_positive(self) -> None:
        self.assertEqual(validate.check_ui_corpus_disjointness(), [])

    def test_disjointness_rejects_ui_path_in_go_index(self) -> None:
        self.index["resources"].append(
            {
                "id": "frontend-design",
                "kind": "skill",
                "path": "ui-kit/skills/frontend-design/SKILL.md",
                "description": "UI design guidance.",
                "tags": [],
                "terms": ["design"],
            }
        )
        (self.kit / "router" / "index.json").write_text(
            json.dumps(self.index), encoding="utf-8"
        )
        errors = validate.check_ui_corpus_disjointness()
        self.assertTrue(any("corpora must stay disjoint" in e for e in errors))

    def _write_ui_contract(self, scenarios: list[dict]) -> None:
        (self.kit / "ui-kit" / "scenarios.json").write_text(
            json.dumps({"schema": 1, "scenarios": scenarios}),
            encoding="utf-8",
        )

    def test_ui_scenarios_positive(self) -> None:
        self._write_ui_contract(
            [
                {
                    "query": "wails desktop app login screen design",
                    "expect": ["frontend-design"],
                },
                {"query": "go worker pool errgroup", "offDomain": True, "expect": []},
            ]
        )
        self.assertEqual(validate.check_ui_router_scenarios(), [])

    def test_ui_scenarios_unresolved_id(self) -> None:
        self._write_ui_contract(
            [
                {
                    "query": "wails desktop app login screen design",
                    "expect": ["does-not-exist"],
                }
            ]
        )
        errors = validate.check_ui_router_scenarios()
        self.assertTrue(any("does-not-exist" in e for e in errors))

    def test_ui_scenarios_missing_contract(self) -> None:
        errors = validate.check_ui_router_scenarios()
        self.assertTrue(any("missing UI routing-quality contract" in e for e in errors))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    unittest.main()
