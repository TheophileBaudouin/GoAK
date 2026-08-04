#!/usr/bin/env python3
"""Tests for the metaproject router index builder (stdlib unittest)."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from build_index import build, check, collect_resources, tokenize

SKILL = """---
name: {name}
description: "{description}"
category: {category}
tags: [go, {tag}]
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

PATTERN = """---
id: {rid}
title: {title}
kind: Pattern
version: 1
status: active
owner: go-agent-kit
tags: [go, {tag}]
go_version: "1.25+"
dependencies: []
last_verified: 2026-08-05
problem: >-
  {problem}
"""

SNIPPET = """id: {rid}
purpose: {purpose}
tags: [go, {tag}]
go_version: "1.25"
dependencies: [stdlib]
"""


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.kit = root / "KitV2"
        self.out = root / "out"
        (self.kit / "rules" / "core").mkdir(parents=True)
        (self.kit / "recipes" / "recipe-foo").mkdir(parents=True)
        (self.kit / "knowledge" / "catalogs" / "chi").mkdir(parents=True)
        (self.kit / "knowledge" / "patterns").mkdir(parents=True)
        (self.kit / "knowledge" / "anti-patterns").mkdir(parents=True)
        (self.kit / "knowledge" / "stdlib").mkdir(parents=True)
        (self.kit / "snippets" / "snp").mkdir(parents=True)
        (self.kit / ".pi" / "prompts").mkdir(parents=True)
        (self.kit / ".pi" / "skills" / "workflow-x").mkdir(parents=True)

        (self.kit / "rules" / "core" / "SKILL.md").write_text(
            SKILL.format(
                name="rule-errors",
                description="Handle errors once: sentinel, typed, opaque.",
                category="rule",
                tag="errors",
            ),
            encoding="utf-8",
        )
        (self.kit / "recipes" / "recipe-foo" / "SKILL.md").write_text(
            SKILL.format(
                name="recipe-foo",
                description="Build a REST API with chi: routes, middleware.",
                category="recipe",
                tag="http",
            ),
            encoding="utf-8",
        )
        (self.kit / "knowledge" / "catalogs" / "chi" / "SKILL.md").write_text(
            SKILL.format(
                name="chi",
                description="go-chi/chi v5 router for idiomatic HTTP.",
                category="library",
                tag="http",
            ),
            encoding="utf-8",
        )
        (self.kit / "knowledge" / "patterns" / "pipeline.yaml").write_text(
            PATTERN.format(
                rid="pattern:concurrency:pipeline",
                title="Pipeline stages",
                tag="concurrency",
                problem="Parallelize sequential data processing stages.",
            ),
            encoding="utf-8",
        )
        (self.kit / "knowledge" / "anti-patterns" / "n1.yaml").write_text(
            PATTERN.format(
                rid="pattern:antipattern:n-plus-one",
                title="N+1 queries",
                tag="database",
                problem="One extra query per row in a loop.",
            ),
            encoding="utf-8",
        )
        (self.kit / "knowledge" / "stdlib" / "go-cmd.yaml").write_text(
            PATTERN.format(
                rid="source:go:command",
                title="Go command reference",
                tag="tooling",
                problem="Authoritative docs for the go command line.",
            ),
            encoding="utf-8",
        )
        (self.kit / "snippets" / "snp" / "SNIPPET.yaml").write_text(
            SNIPPET.format(
                rid="http-json-response",
                purpose="Encode a JSON HTTP response with an explicit status.",
                tag="json",
            ),
            encoding="utf-8",
        )
        (self.kit / ".pi" / "prompts" / "workflow-x.md").write_text(
            PROMPT.format(
                name="workflow-x",
                description="Plan a task before implementation.",
            ),
            encoding="utf-8",
        )
        (self.kit / ".pi" / "skills" / "workflow-x" / "SKILL.md").write_text(
            SKILL.format(
                name="workflow-x",
                description="Plan first, then implement.",
                category="workflow",
                tag="planning",
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_tokenize(self) -> None:
        self.assertEqual(
            tokenize("REST APIs, concurrency!", {"the"}),
            ["rest", "apis", "concurrency"],
        )
        self.assertEqual(tokenize("the go", {"the"}), ["go"])
        # 1-char tokens are dropped
        self.assertEqual(tokenize("a b", set()), [])

    def test_coverage_and_shapes(self) -> None:
        resources = collect_resources(self.kit, set())
        by_id = {r["id"]: r for r in resources}
        self.assertEqual(
            set(by_id),
            {
                "rule-errors",
                "recipe-foo",
                "chi",
                "pattern:concurrency:pipeline",
                "pattern:antipattern:n-plus-one",
                "source:go:command",
                "http-json-response",
                "workflow-x",
            },
        )
        # the prompt and the workflow skill share the id "workflow-x"
        self.assertEqual(len([r for r in resources if r["id"] == "workflow-x"]), 2)
        kinds = {r["kind"] for r in resources}
        self.assertEqual(
            kinds,
            {
                "rule",
                "recipe",
                "catalog",
                "pattern",
                "anti-pattern",
                "source",
                "snippet",
                "prompt",
                "skill",
            },
        )
        for r in resources:
            self.assertTrue(r["path"])
            self.assertTrue(r["description"])
            self.assertTrue(r["terms"])
        pipeline = by_id["pattern:concurrency:pipeline"]
        self.assertIn("pipeline", pipeline["terms"])
        self.assertIn("parallelize", pipeline["terms"])

    def test_deterministic(self) -> None:
        meta1 = build(self.kit, self.out, "1.0.0")
        first = (self.out / "index.json").read_bytes()
        meta2 = build(self.kit, self.out, "1.0.0")
        second = (self.out / "index.json").read_bytes()
        self.assertEqual(first, second)
        self.assertEqual(meta1["index_sha256"], hashlib.sha256(first).hexdigest())
        self.assertEqual(meta1, meta2)

    def test_check_clean_then_drift(self) -> None:
        build(self.kit, self.out, "1.0.0")
        ok, problems = check(self.kit, self.out)
        self.assertTrue(ok, problems)
        # drift: change a description
        (self.kit / "recipes" / "recipe-foo" / "SKILL.md").write_text(
            SKILL.format(
                name="recipe-foo",
                description="Build a gRPC service: proto, codegen, server.",
                category="recipe",
                tag="grpc",
            ),
            encoding="utf-8",
        )
        ok, problems = check(self.kit, self.out)
        self.assertFalse(ok)
        self.assertTrue(any("drift" in p for p in problems))
        # rebuild → clean again
        build(self.kit, self.out, "1.0.0")
        ok, problems = check(self.kit, self.out)
        self.assertTrue(ok, problems)

    def test_check_missing(self) -> None:
        ok, problems = check(self.kit, self.out)
        self.assertFalse(ok)
        self.assertTrue(any("missing" in p for p in problems))

    def test_meta_schema(self) -> None:
        meta = build(self.kit, self.out, "2.2.0")
        self.assertEqual(meta["schema"], 1)
        self.assertEqual(meta["version"], "2.2.0")
        self.assertEqual(meta["counts"]["recipe"], 1)
        self.assertIn("stopwords", meta)
        index = json.loads((self.out / "index.json").read_text(encoding="utf-8"))
        self.assertEqual(index["schema"], 1)
        self.assertEqual(len(index["resources"]), 9)


if __name__ == "__main__":
    unittest.main()
