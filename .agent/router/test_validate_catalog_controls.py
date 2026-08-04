#!/usr/bin/env python3
"""Positive and negative tests for catalog-specific validator controls."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "KitV2" / "tools" / "validators" / "validate-kitv2.py"
spec = importlib.util.spec_from_file_location("validate_kitv2", VALIDATOR)
if spec is None or spec.loader is None:
    raise SystemExit(f"cannot load validator module from {VALIDATOR}")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)


SOURCE = """
## Sources vérifiées

- [Official documentation](https://example.test/docs) — vérifié {verified}.
"""


def skill(body: str = "", verified: date | None = None) -> str:
    verified = verified or date.today()
    return f"""---
name: example
category: library
last-verified: {verified.isoformat()}
---

# example

{body}
"""


class CatalogControls(unittest.TestCase):
    def test_freshness_positive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                skill(SOURCE.format(verified=date.today()), verified=date.today()),
                encoding="utf-8",
            )
            self.assertEqual(validate.check_catalog_freshness(path), [])

    def test_freshness_negative(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            old = date.today() - timedelta(days=91)
            path.write_text(
                skill(SOURCE.format(verified=old), verified=old), encoding="utf-8"
            )
            self.assertTrue(validate.check_catalog_freshness(path))

    def test_example_positive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                skill("""```go
value, err := load()
if err != nil {
    return err
}
_ = value
```"""),
                encoding="utf-8",
            )
            self.assertEqual(validate.check_markdown_examples(path), [])

    def test_example_negative(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                skill("""```go
value, _ := load()
```"""),
                encoding="utf-8",
            )
            self.assertTrue(validate.check_markdown_examples(path))

    def test_duplicate_positive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                skill(
                    "first distinct paragraph with enough words to pass the scanner."
                ),
                encoding="utf-8",
            )
            self.assertEqual(validate.check_internal_duplicates(path), [])

    def test_duplicate_negative(self) -> None:
        paragraph = (
            "This exact paragraph contains enough words to be detected as a duplicate."
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(skill(f"{paragraph}\n\n{paragraph}"), encoding="utf-8")
            self.assertTrue(validate.check_internal_duplicates(path))


if __name__ == "__main__":
    unittest.main()
