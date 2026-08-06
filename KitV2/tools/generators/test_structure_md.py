"""Tests for the structure.md generator/checker (charter Layer 5.1)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "generators"))

import structure_md  # noqa: E402


class StructureMdCheckTest(unittest.TestCase):
    def test_real_templates_pass(self) -> None:
        for template in ("cli", "rest-api", "worker"):
            with self.subTest(template=template):
                project = ROOT / "templates" / template
                text = (project / "structure.md").read_text(encoding="utf-8")
                self.assertEqual(
                    structure_md.check(project, text),
                    [],
                    f"{template}/structure.md must be drift-free",
                )

    def test_generated_skeleton_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "app"
            (project / "cmd").mkdir(parents=True)
            (project / "internal" / "store").mkdir(parents=True)
            (project / "cmd" / "main.go").write_text(
                "package main\nfunc main() {}\n", encoding="utf-8"
            )
            (project / "internal" / "store" / "store.go").write_text(
                "package store\n", encoding="utf-8"
            )
            (project / "internal" / "store" / "store_test.go").write_text(
                "package store\n", encoding="utf-8"
            )
            skeleton = structure_md.generate(project)
            # A bare skeleton is not yet conforming: the semantic sections
            # are human-completed before the drift check runs (Layer 5.1).
            completed = (
                skeleton.replace(
                    "<!-- Describe one concrete behavior and walk it through the directories. -->",
                    "A request flows from cmd/ (entry point) into internal/store.",
                )
                .replace(
                    "<!-- What is private implementation, what is public API or entry point. -->",
                    "internal/ is private implementation; cmd/main.go is the entry point.",
                )
                .replace(
                    "<!-- Tests and observable scenarios: list the test locations and how to run\n"
                    "them. The tree facts above enumerate every test file. -->",
                    "Run `go test ./...`; tests live in internal/store/store_test.go.",
                )
            )
            self.assertEqual(structure_md.check(project, completed), [])

    def test_tampered_fact_is_caught(self) -> None:
        project = ROOT / "templates" / "rest-api"
        text = (project / "structure.md").read_text(encoding="utf-8")
        tampered = text.replace("internal_boundary: present", "internal_boundary: absent")
        defects = structure_md.check(project, tampered)
        self.assertTrue(
            any("internal_boundary" in d for d in defects),
            f"expected a boundary drift defect, got {defects}",
        )

    def test_phantom_directory_is_caught(self) -> None:
        project = ROOT / "templates" / "cli"
        text = (project / "structure.md").read_text(encoding="utf-8")
        tampered = text.replace(
            "top_dirs: .github; cmd; internal",
            "top_dirs: .github; cmd; internal; phantom",
        )
        defects = structure_md.check(project, tampered)
        self.assertTrue(any("top_dirs" in d for d in defects), defects)

    def test_missing_role_entry_is_caught(self) -> None:
        project = ROOT / "templates" / "rest-api"
        text = (project / "structure.md").read_text(encoding="utf-8")
        tampered = text.replace("- `pkg/` —", "- `pkgx/` —")
        defects = structure_md.check(project, tampered)
        self.assertTrue(any("`pkg/`" in d for d in defects), defects)


if __name__ == "__main__":
    unittest.main()
