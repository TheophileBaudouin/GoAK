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


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    unittest.main()
