from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

VALIDATOR = Path(__file__).with_name("validate-kitv2.py")
spec = importlib.util.spec_from_file_location("validate_kitv2", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ValidatorTests(unittest.TestCase):
    def test_existing_product_structure_passes(self) -> None:
        self.assertEqual(
            module.check_skill(module.ROOT / "rules/core/philosophy/SKILL.md"), []
        )
        self.assertEqual(module.check_coverage(), [])
        self.assertEqual(module.check_probe_runner(), [])
        self.assertEqual(module.check_template_status(), [])

    def test_skill_without_frontmatter_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skill" / "SKILL.md"
            path.parent.mkdir()
            path.write_text("# missing metadata\n", encoding="utf-8")
            errors = module.check_skill(path)
        self.assertTrue(any("missing frontmatter" in error for error in errors))

    def test_old_artifact_warns_and_very_old_artifact_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skill" / "SKILL.md"
            path.parent.mkdir()
            old = (date.today() - timedelta(days=400)).isoformat()
            path.write_text(
                f'---\nname: skill\ndescription: "Use when testing."\n'
                f"category: rule\ntags: [test]\nlast-verified: {old}\n---\n",
                encoding="utf-8",
            )
            warnings: list[str] = []
            self.assertEqual(module.check_freshness(path, warnings), [])
            self.assertTrue(any("warning" in warning for warning in warnings))

            very_old = (date.today() - timedelta(days=600)).isoformat()
            path.write_text(path.read_text().replace(old, very_old), encoding="utf-8")
            self.assertTrue(module.check_freshness(path, []))

    def test_snippet_check_requires_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snippet = root / "SNIPPET.yaml"
            snippet.write_text(
                "id: x\npurpose: x\nsource: x\nfiles: [example.go]\ntests: [check.sh]\n",
                encoding="utf-8",
            )
            (root / "check.sh").write_text("gofmt -w example.go\n", encoding="utf-8")
            errors = module.check_snippet(snippet)
        self.assertTrue(any("must not mutate" in error for error in errors))
        self.assertTrue(any("go test or go run" in error for error in errors))

    def test_coverage_detects_drift(self) -> None:
        original = module.ROOT / "capabilities.yaml"
        content = original.read_text(encoding="utf-8")
        try:
            original.write_text(
                content.replace("product_skills: 71", "product_skills: 70"),
                encoding="utf-8",
            )
            errors = module.check_coverage()
        finally:
            original.write_text(content, encoding="utf-8")
        self.assertTrue(any("coverage.product_skills" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
