#!/usr/bin/env python3
"""Validate deterministic structure of KitV2 instruction artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "KitV2"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CATEGORY_RE = re.compile(r"^(recipe|rule|pattern|library|reference-project|checklist)$")
ALLOWED_REGISTRY_FIELDS = {"name", "description", "category", "tags", "last-verified"}
REQUIRED_REGISTRY_FIELDS = ALLOWED_REGISTRY_FIELDS
# Workflow skills (.pi/skills/) carry the kit-only `category: workflow` value
# (Decisions.md 2026-08-04) plus tags/last-verified; the rest of the schema
# matches the module schema so freshness checks apply uniformly.
ALLOWED_WORKFLOW_FIELDS = ALLOWED_REGISTRY_FIELDS
REQUIRED_WORKFLOW_FIELDS = {"name", "description", "last-verified"}


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: malformed YAML frontmatter")
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        if not line or line.startswith(" "):
            continue
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"')
    return values


def check_skill(path: Path, registry: bool) -> list[str]:
    errors: list[str] = []
    values = frontmatter(path)
    if registry:
        required, allowed = REQUIRED_REGISTRY_FIELDS, ALLOWED_REGISTRY_FIELDS
    else:
        required, allowed = REQUIRED_WORKFLOW_FIELDS, ALLOWED_WORKFLOW_FIELDS
    missing = required - values.keys()
    if missing:
        errors.append(f"{path}: missing frontmatter fields: {sorted(missing)}")
    unknown = set(values) - allowed
    if unknown:
        errors.append(f"{path}: unexpected frontmatter fields: {sorted(unknown)}")
    name = values.get("name", "")
    if not NAME_RE.fullmatch(name):
        errors.append(f"{path}: invalid name {name!r}")
    if path.parent.name != name:
        errors.append(
            f"{path}: name {name!r} does not match directory {path.parent.name!r}"
        )
    description = values.get("description", "")
    if not description or len(description) > 1024:
        errors.append(f"{path}: description must be 1..1024 characters")
    if registry:
        category = values.get("category", "")
        if not CATEGORY_RE.fullmatch(category):
            errors.append(f"{path}: invalid category {category!r}")
        if not DATE_RE.fullmatch(values.get("last-verified", "")):
            errors.append(f"{path}: last-verified must use YYYY-MM-DD")
        tags = values.get("tags", "")
        if not tags.startswith("[") or not tags.endswith("]"):
            errors.append(f"{path}: tags must be a YAML list")
    elif not DATE_RE.fullmatch(values.get("last-verified", "")):
        errors.append(f"{path}: last-verified must use YYYY-MM-DD")
    if len(path.read_text(encoding="utf-8").splitlines()) > 500:
        errors.append(f"{path}: body exceeds 500 lines")
    return errors


def check_links(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)#]+)", text):
        if target.startswith(("references/", "assets/", "scripts/")):
            resolved = path.parent / target
            if not resolved.exists():
                errors.append(f"{path}: missing relative resource {target}")
    return errors


ABSOLUTE_LEXEMES = ("mandatory", "must", "always", "never")
PROCESS_SURFACES = (
    ROOT / "AGENTS.md",
    *((ROOT / ".pi" / "prompts").glob("*.md")),
    *((ROOT / ".pi" / "skills").glob("*/SKILL.md")),
    *((ROOT / ".pi" / "extensions").glob("*.ts")),
    # recipes: KVA-005 (2026-08-08) — the KVA-106 scope names recipe process
    # instructions, so recipe SKILL.md files enter the forward scan; recipe
    # functional/API-contract lexemes are recorded in the registry under the
    # same rule-content boundary as rule bodies.
    *((ROOT / "recipes").rglob("SKILL.md")),
)


def check_absolute_instructions_registry() -> list[str]:
    """Charter §16.1.4 (D-2026-08-05-15): every absolute instruction on a
    consumer process surface must be recorded in the enforcement registry
    (.agent/instructions.md), and every recorded carrier must exist.

    Forward direction: a process surface (AGENTS.md, prompts, workflow
    SKILL.md, extension promptGuidelines, recipe SKILL.md) carrying a
    MANDATORY lexeme must have a registry row naming its path (rules/ rule
    bodies are excluded by the KVA-106 interpretation: rule-content
    boundaries are not process absolutes; recipe functional/API contracts
    are recorded under the same boundary).
    Reverse direction: every non-wildcard registry carrier path must exist
    (a cited validator/carrier that does not exist is itself a defect).
    """
    errors: list[str] = []
    meta_root = Path(__file__).resolve().parents[2]
    registry = meta_root / ".agent" / "instructions.md"
    if not registry.exists():
        errors.append(f"{registry}: enforcement registry missing (§16.1.4)")
        return errors
    text = registry.read_text(encoding="utf-8")
    recorded = {
        path.removeprefix("KitV2/") for path in re.findall(r"`(KitV2/[^`]+)`", text)
    }
    strong = ("mandatory",)
    for path in PROCESS_SURFACES:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        if any(lexeme in content.lower() for lexeme in strong):
            relative = str(path.relative_to(ROOT))
            if relative not in recorded:
                errors.append(
                    f"{path}: MANDATORY instruction not recorded in "
                    f"the enforcement registry ({registry.name}) — charter §16.1.4"
                )
    for relative in sorted(recorded):
        if relative.endswith("**") or "/**" in relative:
            continue  # rules/** wildcard row
        carrier = ROOT / relative
        if not carrier.exists():
            errors.append(f"{registry}: registry carrier does not exist: {relative}")
            continue
        content = carrier.read_text(encoding="utf-8", errors="replace").lower()
        if not any(lexeme in content for lexeme in ABSOLUTE_LEXEMES):
            errors.append(
                f"{registry}: registry carrier has no absolute lexeme: {relative}"
            )
    return errors


def main() -> int:
    errors: list[str] = []
    paths = [
        *((ROOT / ".pi" / "skills").rglob("SKILL.md")),
        *((ROOT / "rules").rglob("SKILL.md")),
        *((ROOT / "recipes").rglob("SKILL.md")),
        *((ROOT / "knowledge" / "catalogs").rglob("SKILL.md")),
    ]
    for path in sorted(paths):
        try:
            relative_parts = path.relative_to(ROOT).parts
            registry = relative_parts[0] in {"rules", "recipes", "knowledge"}
            errors.extend(check_skill(path, registry=registry))
            errors.extend(check_links(path))
        except ValueError as error:
            errors.append(str(error))
    if (ROOT / ".pi" / "memory").exists():
        errors.append(f"{ROOT / '.pi' / 'memory'}: consumer memory must not ship")
    for path in sorted((ROOT / ".pi" / "prompts").glob("*.md")):
        try:
            values = frontmatter(path)
            if not values.get("description"):
                errors.append(f"{path}: prompt description is required")
        except ValueError as error:
            errors.append(str(error))
    errors.extend(check_absolute_instructions_registry())
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("instruction-artifacts: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
