from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

VALIDATOR = Path(__file__).with_name("validate-kitv2.py")
spec = importlib.util.spec_from_file_location("validate_kitv2", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


class ValidatorTests(unittest.TestCase):
    def test_existing_product_structure_passes(self) -> None:
        self.assertEqual(
            module.check_skill(module.ROOT / "rules/core/philosophy/SKILL.md"), []
        )
        self.assertEqual(module.check_coverage(), [])
        self.assertEqual(module.check_probe_runner(), [])
        self.assertEqual(module.check_template_status(), [])
        self.assertEqual(module.check_recipe_dependencies([]), [])
        self.assertEqual(module.check_manifest_capabilities_coherence([]), [])

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

    def test_coverage_detects_drift_without_writing_the_repo(self) -> None:
        """KVA-011 — drift detection must not mutate the shipped file."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = module.ROOT / "capabilities.yaml"
            target = root / "capabilities.yaml"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                original.read_text(encoding="utf-8").replace(
                    "product_skills: 71", "product_skills: 70"
                ),
                encoding="utf-8",
            )
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_coverage()
        self.assertTrue(any("coverage.product_skills" in error for error in errors))
        # The shipped file is untouched.
        self.assertIn("product_skills: 71", original.read_text(encoding="utf-8"))

    def test_template_build_fails_on_broken_template(self) -> None:
        if shutil.which("go") is None:
            self.skipTest("go not on PATH")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            template_dir = root / "templates" / "broken"
            write(template_dir / "template.yaml", "name: broken\nstatus: sourced\n")
            write(template_dir / "go.mod", "module broken\n\ngo 1.25\n")
            write(template_dir / "main.go", "package main\nfunc main( {\n")
            warnings: list[str] = []
            errors = module.check_template_build(warnings, root=root)
        self.assertTrue(any("does not compile" in error for error in errors), errors)

    def test_template_build_passes_on_buildable_template(self) -> None:
        if shutil.which("go") is None:
            self.skipTest("go not on PATH")
        warnings: list[str] = []
        self.assertEqual(module.check_template_build(warnings, module.ROOT), [])

    def test_manifest_capabilities_coherence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / "manifest.yaml",
                "capabilities: [alpha, beta]\ncanonical:\n  alpha: a/\n  beta: b/\n",
            )
            write(
                root / "capabilities.yaml",
                "capabilities:\n"
                "  alpha:\n"
                "    source: a/\n"
                "    status: complete\n"
                "    criteria: works\n"
                "  beta:\n"
                "    source: b/\n"
                "    status: partial\n"
                "    criteria: works\n",
            )
            self.assertEqual(module.check_manifest_capabilities_coherence([], root), [])

            # Drift: manifest declares a capability the catalog does not.
            write(
                root / "manifest.yaml",
                "capabilities: [alpha, beta, gamma]\ncanonical:\n  alpha: a/\n",
            )
            errors = module.check_manifest_capabilities_coherence([], root)
        self.assertTrue(
            any("!= capabilities.yaml keys" in error for error in errors), errors
        )

    def test_recipe_dependencies_reject_unvetted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / "go.mod",
                "module example.com/kit\n\ngo 1.25\n\n"
                "require (\n"
                "\texample.com/unvetted v1.0.0\n"
                "\texample.com/vetted v1.0.0\n"
                ")\n",
            )
            write(
                root / "knowledge" / "catalogs" / "libraries" / "vetted" / "SKILL.md",
                "---\nname: vetted\ndescription: example.com/vetted fiche\n"
                "category: library\ntags: [x]\nlast-verified: 2026-08-05\n---\n",
            )
            errors = module.check_recipe_dependencies([], root=root)
        self.assertTrue(
            any("example.com/unvetted" in error for error in errors), errors
        )
        self.assertFalse(
            any("vetted" in error and "unvetted" not in error for error in errors)
        )

    def test_snippet_chain_requires_fresh_dependent(self) -> None:
        """KVA-105 — a snippet older than its canonical source must fail."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / "recipes" / "recipe-x" / "SKILL.md",
                "---\nname: recipe-x\ndescription: canonical\n"
                "category: recipe\ntags: [x]\nlast-verified: 2026-08-05\n---\n",
            )
            write(
                root / "snippets" / "sx" / "SNIPPET.yaml",
                "id: sx\npurpose: p\nsource: ../../recipes/recipe-x/SKILL.md\n"
                "last_verified: 2026-08-04\nfiles: [example.go]\ntests: [check.sh]\n",
            )
            errors = module.check_snippet_chain(root=root)
        self.assertTrue(
            any("older than canonical" in error for error in errors), errors
        )

    def test_snippet_chain_accepts_fresh_or_undated(self) -> None:
        """KVA-105 — fresh dependents and missing dates are accepted."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / "recipes" / "recipe-x" / "SKILL.md",
                "---\nname: recipe-x\ndescription: canonical\n"
                "category: recipe\ntags: [x]\nlast-verified: 2026-08-05\n---\n",
            )
            write(
                root / "snippets" / "sa" / "SNIPPET.yaml",
                "id: sa\npurpose: p\nsource: ../../recipes/recipe-x/SKILL.md\n"
                "last_verified: 2026-08-06\nfiles: [example.go]\ntests: [check.sh]\n",
            )
            write(
                root / "snippets" / "sb" / "SNIPPET.yaml",
                "id: sb\npurpose: p\nsource: ../../recipes/recipe-x/SKILL.md\n"
                "files: [example.go]\ntests: [check.sh]\n",
            )
            self.assertEqual(module.check_snippet_chain(root=root), [])


if __name__ == "__main__":
    unittest.main()
