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
        self.assertIn("product_skills: 73", original.read_text(encoding="utf-8"))

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

    def test_no_metaproject_paths_catches_leakage(self) -> None:
        """KVA-102 — a shipped file referencing the metaproject marker fails."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            marker = "." + "agent/"  # built dynamically: the string is the check target
            write(
                root / "router" / "README.md", f"run `{marker}router/x` from the root\n"
            )
            write(root / "tools" / "ok.py", "print('clean')\n")
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_no_metaproject_paths()
        self.assertTrue(any("README.md" in error for error in errors), errors)
        self.assertFalse(any("ok.py" in error for error in errors), errors)

    def test_no_metaproject_markers_catch_build_repo_material(self) -> None:
        """The consumer kit must never reference build-repository-only
        material: charter, dated decisions, audit findings, the repository
        folder name, or governance contracts."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, snippet in (
                ("a.md", "see KIT_CHARTER.md Layer 5.1\n"),
                ("b.md", "recorded in the metaproject journal\n"),
                ("c.md", "decision D-2026-08-08-06 applies\n"),
                ("d.md", "audit finding KVA-102 closed\n"),
                ("e.md", "read KitV2/AGENTS.md\n"),
                ("f.md", "governed by the Z13 contract\n"),
                ("g.md", "fundamental rule D-2026-08-05-21\n"),
            ):
                write(root / name, snippet)
            write(root / "ok.md", "plain content\n")
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_no_metaproject_paths()
        self.assertEqual(len(errors), 7, errors)
        self.assertTrue(any("a.md" in error for error in errors), errors)
        self.assertTrue(any("g.md" in error for error in errors), errors)
        self.assertFalse(any("ok.md" in error for error in errors), errors)

    def test_workspace_init_placeholder_passes_with_section(self) -> None:
        """Z14 — the pointer section with both markers and the title is the
        valid (not-yet-initialized) state of the kit AGENTS.md."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / "AGENTS.md",
                "<!-- workspace-init section: begin -->\n"
                "## Project Foundation — new consumer projects\n"
                "pointer content\n"
                "<!-- workspace-init section: end -->\n",
            )
            with mock.patch.object(module, "ROOT", root):
                self.assertEqual(module.check_workspace_init_placeholder(), [])

    def test_workspace_init_placeholder_fails_when_section_lost(self) -> None:
        """Z14 — a removed Project Foundation section fails the gate."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / "AGENTS.md", "only other content\n")
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_workspace_init_placeholder()
        self.assertTrue(any("AGENTS.md" in error for error in errors), errors)

    def test_workspace_init_placeholder_fails_when_marker_altered(self) -> None:
        """Z14 — a swallowed marker (e.g. a manual merge dropped the end
        marker) fails the gate, never silently passing."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / "AGENTS.md",
                "<!-- workspace-init section: begin -->\n"
                "## Project Foundation — new consumer projects\n",
            )
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_workspace_init_placeholder()
        self.assertTrue(any("markers missing" in error for error in errors), errors)

    def test_probe_inventory_out_of_sync_fails(self) -> None:
        """KVA-102 — the probes README table must match the real probe tree."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / "probes" / "run.sh", 'for probe in "$root"/probes/*/; do\n')
            write(root / "probes" / "alpha" / "main.go", "package main\n")
            write(root / "probes" / "beta" / "main.go", "package main\n")
            write(
                root / "probes" / "README.md",
                "## Inventory\n\n| Probe | Recipe |\n| --- | --- |\n"
                "| `alpha` | recipe-alpha |\n",
            )
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_probe_runner()
        self.assertTrue(any("out of sync" in error for error in errors), errors)
        self.assertTrue(any("beta" in error for error in errors), errors)

    def test_probe_inventory_in_sync_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / "probes" / "run.sh", 'for probe in "$root"/probes/*/; do\n')
            write(root / "probes" / "alpha" / "main.go", "package main\n")
            write(
                root / "probes" / "README.md",
                "## Inventory\n\n| Probe | Recipe |\n| --- | --- |\n"
                "| `alpha` | recipe-alpha |\n",
            )
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_probe_runner()
        self.assertEqual(errors, [])

    def test_ui_kit_registration_passes_when_root_settings_declares_skills(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "settings.json",
                '{\n  "skills": ["../rules", "../recipes", "../ui-kit/skills"]\n}\n',
            )
            errors = module.check_ui_kit_registration(root)
        self.assertEqual(errors, [])

    def test_ui_kit_registration_fails_without_ui_skill_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "settings.json",
                '{\n  "skills": ["../rules", "../recipes"]\n}\n',
            )
            errors = module.check_ui_kit_registration(root)
        self.assertTrue(any("../ui-kit/skills" in error for error in errors), errors)

    def test_ui_kit_registration_fails_on_nested_settings_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "settings.json",
                '{\n  "skills": ["../rules", "../recipes", "../ui-kit/skills"]\n}\n',
            )
            write(
                root / "ui-kit" / ".pi" / "settings.json",
                '{\n  "skills": ["../skills"]\n}\n',
            )
            errors = module.check_ui_kit_registration(root)
        self.assertTrue(
            any("single registration point" in error for error in errors), errors
        )

    def test_ui_kit_registration_fails_when_go_skill_paths_dropped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "settings.json",
                '{\n  "skills": ["../ui-kit/skills"]\n}\n',
            )
            errors = module.check_ui_kit_registration(root)
        self.assertTrue(any("../rules" in error for error in errors), errors)

    def test_consumer_onboarding_passes_with_full_surface(self) -> None:
        """The complete onboarding surface (guide, /goak-help, banner,
        extension, AGENTS.md section) is the valid shipped state."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "docs" / "GOAK.md",
                "# Guide\n\n## Get Started\nsteps\n\n## Commands\n\n"
                "## Workflows\n\n## Kit structure\n\n## Troubleshooting\n",
            )
            write(
                root / ".pi" / "prompts" / "goak-help.md",
                "---\ndescription: Explain GOAK from the local guide.\n---\n"
                "Read `.pi/docs/GOAK.md` first.\n",
            )
            write(
                root / ".pi" / "onboarding" / "banner.md",
                "1. GET STARTED — /goak-help\n"
                "2. NEW FEATURE — LARGE change\n"
                "3. NEW FEATURE — SMALL change\n",
            )
            write(
                root / ".pi" / "extensions" / "kit-onboarding.ts",
                '// onboarding extension\npi.on("session_start", () => {}\n'
                'pi.appendEntry("goak-onboarding", { lines })\n'
                'pi.registerEntryRenderer("goak-onboarding", () => {})\n',
            )
            write(
                root / "AGENTS.md",
                "<!-- user guide section: begin -->\n"
                "## User guide\npointer\n"
                "<!-- user guide section: end -->\n",
            )
            errors = module.check_consumer_onboarding()
        self.assertEqual(errors, [])

    def test_consumer_onboarding_fails_when_guide_missing(self) -> None:
        """A shipped kit without the user guide fails the gate."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / "AGENTS.md", "content\n")
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_consumer_onboarding()
        self.assertTrue(any("GOAK.md" in error for error in errors), errors)

    def test_consumer_onboarding_fails_when_goak_points_to_stale_path(self) -> None:
        """/goak-help must point at the local guide; a stale or external path
        is drift (the agent would answer from memory or old docs)."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "prompts" / "goak-help.md",
                "---\ndescription: Explain GOAK.\n---\n"
                "Explain the kit from your general knowledge.\n",
            )
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_consumer_onboarding()
        self.assertTrue(any("local guide" in error for error in errors), errors)

    def test_consumer_onboarding_fails_when_banner_entry_missing(self) -> None:
        """The banner must carry the three entries (Get Started, large,
        small); a partial banner fails the gate."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "onboarding" / "banner.md",
                "1. GET STARTED — /goak-help\n2. NEW FEATURE — LARGE change\n",
            )
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_consumer_onboarding()
        self.assertTrue(any("small feature" in error for error in errors), errors)

    def test_consumer_onboarding_fails_when_agents_section_lost(self) -> None:
        """A removed AGENTS.md User guide pointer section fails the gate
        (same marker discipline as the Project Foundation section)."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / "AGENTS.md", "only other content\n")
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_consumer_onboarding()
        self.assertTrue(any("markers missing" in error for error in errors), errors)

    def test_declared_skill_dirs_passes_with_descriptions(self) -> None:
        """Root .md files in declared skill dirs with a frontmatter
        description load cleanly (recipes/README.md fix)."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "settings.json",
                '{\n  "skills": ["../rules", "../recipes"]\n}\n',
            )
            write(
                root / "recipes" / "README.md",
                "---\nname: recipes\ndescription: Index of the shipped recipes.\n"
                "disable-model-invocation: true\n---\n# Recipes\ncontent\n",
            )
            with mock.patch.object(module, "ROOT", root):
                self.assertEqual(module.check_declared_skill_dirs(), [])

    def test_declared_skill_dirs_fails_without_description(self) -> None:
        """Pi loads root .md files of a declared skill dir as skills; a
        missing description breaks loading and shows a conflict warning."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(
                root / ".pi" / "settings.json",
                '{\n  "skills": ["../recipes"]\n}\n',
            )
            write(root / "recipes" / "README.md", "# Recipes\ncontent\n")
            with mock.patch.object(module, "ROOT", root):
                errors = module.check_declared_skill_dirs()
        self.assertTrue(
            any("description" in e or "frontmatter" in e for e in errors), errors
        )


if __name__ == "__main__":
    unittest.main()
