#!/usr/bin/env python3
"""Validate the standalone KitV2 product."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CATEGORIES = {"recipe", "rule", "pattern", "library", "reference-project", "checklist"}
GRAPH_KINDS = {
    "Rule",
    "Recipe",
    "Pattern",
    "Snippet",
    "Template",
    "Capability",
    "Evaluation",
    "DecisionRecord",
    "Source",
    "Memory",
}
GRAPH_STATUSES = {"proposed", "active", "deprecated", "rejected"}
GRAPH_RELATIONS = {
    "depends_on",
    "uses",
    "implements",
    "extends",
    "references",
    "requires",
    "supersedes",
    "validated_by",
    "generated_from",
}
GRAPH_ID_RE = re.compile(
    r"^(?:rule|recipe|pattern|snippet|template|capability|evaluation|decision-record|source|memory):[^:]+:.+$"
)
URL_RE = re.compile(r"^https?://")
EXPECTED_PRODUCT_SKILLS = 45
EXPECTED_TEMPLATES = {
    "rest-api",
    "grpc",
    "cli",
    "worker",
    "microservice",
    "monolith",
    "cloud-service",
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: malformed frontmatter")
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"')
    return values


def check_skill(path: Path) -> list[str]:
    try:
        values = parse_frontmatter(path)
    except ValueError as error:
        return [str(error)]
    errors: list[str] = []
    missing = {
        "name",
        "description",
        "category",
        "tags",
        "last-verified",
    } - values.keys()
    if missing:
        errors.append(f"{path}: missing {sorted(missing)}")
    if not NAME_RE.fullmatch(values.get("name", "")):
        errors.append(f"{path}: invalid name")
    if path.parent.name != values.get("name"):
        errors.append(f"{path}: name does not match directory")
    if not values.get("description") or len(values["description"]) > 1024:
        errors.append(f"{path}: description must be 1..1024 characters")
    if values.get("category") not in CATEGORIES:
        errors.append(f"{path}: invalid category")
    if not values.get("tags", "").startswith("["):
        errors.append(f"{path}: tags must be a YAML list")
    if not DATE_RE.fullmatch(values.get("last-verified", "")):
        errors.append(f"{path}: last-verified must be YYYY-MM-DD")
    if len(path.read_text(encoding="utf-8").splitlines()) > 500:
        errors.append(f"{path}: exceeds 500 lines")
    return errors


def check_snippet(path: Path) -> list[str]:
    keys = {
        line.split(":", 1)[0] + ":"
        for line in path.read_text().splitlines()
        if ":" in line
    }
    missing = {"id:", "purpose:", "source:", "files:", "tests:"} - keys
    return [f"{path}: missing {sorted(missing)}"] if missing else []


def check_bundle() -> list[str]:
    errors: list[str] = []
    bundle = ROOT / "tools" / "offline" / "bundle"
    manifest_path = bundle / "manifest.json"
    if not manifest_path.exists():
        return [f"{manifest_path}: missing"]
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{manifest_path}: invalid JSON: {error}"]
    if manifest.get("protocol") != "goretrieval/1" or manifest.get("schema") != 1:
        errors.append(f"{manifest_path}: unsupported protocol or schema")
    for source in manifest.get("sources", []):
        for field in ("id", "pin", "pin_type", "verifier", "license", "attribution"):
            if not source.get(field):
                errors.append(f"{manifest_path}: source missing {field}")
        if source.get("index"):
            index = bundle / source["index"]
            if not index.exists():
                errors.append(f"{index}: missing")
            elif hashlib.sha256(index.read_bytes()).hexdigest() != source.get(
                "index_sha256"
            ):
                errors.append(f"{index}: checksum mismatch")
            elif index.stat().st_size > 16384:
                errors.append(f"{index}: exceeds 16384 bytes")
        license_path = bundle / source.get("license", "")
        if not license_path.exists():
            errors.append(f"{license_path}: license/attribution file missing")
    for blob in (bundle / "blobs").glob("*"):
        if blob.is_file():
            if blob.stat().st_size > 524288:
                errors.append(f"{blob}: exceeds 524288 bytes")
            if hashlib.sha256(blob.read_bytes()).hexdigest() != blob.name:
                errors.append(f"{blob}: filename does not match SHA-256")
    return errors


def check_knowledge_metadata() -> list[str]:
    errors: list[str] = []
    required = {
        "id",
        "title",
        "kind",
        "version",
        "status",
        "owner",
        "tags",
        "go_version",
        "dependencies",
        "last_verified",
    }
    paths = sorted((ROOT / "knowledge").rglob("*.yaml"))
    artifacts: dict[Path, dict] = {}
    for path in paths:
        try:
            artifact = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            errors.append(f"{path}: invalid YAML: {error}")
            continue
        if isinstance(artifact, dict):
            artifacts[path] = artifact
    known_ids = {
        artifact["id"]
        for artifact in artifacts.values()
        if isinstance(artifact.get("id"), str)
    }
    for path, artifact in artifacts.items():
        if not isinstance(artifact, dict):
            errors.append(f"{path}: expected a metadata mapping")
            continue
        missing = required - artifact.keys()
        if missing:
            errors.append(f"{path}: missing metadata {sorted(missing)}")
        if not isinstance(artifact.get("id"), str) or not GRAPH_ID_RE.fullmatch(
            artifact["id"]
        ):
            errors.append(f"{path}: invalid stable id")
        if artifact.get("kind") not in GRAPH_KINDS:
            errors.append(f"{path}: invalid kind {artifact.get('kind')!r}")
        if artifact.get("status") not in GRAPH_STATUSES:
            errors.append(f"{path}: invalid status {artifact.get('status')!r}")
        relationships = artifact.get("relationships", {})
        if not isinstance(relationships, dict):
            errors.append(f"{path}: relationships must be a mapping")
        else:
            for relation, targets in relationships.items():
                if relation not in GRAPH_RELATIONS:
                    errors.append(f"{path}: unknown relationship {relation!r}")
                elif not isinstance(targets, list):
                    errors.append(f"{path}: relationship {relation!r} must be a list")
                elif any(
                    not isinstance(target, str)
                    or not GRAPH_ID_RE.fullmatch(target)
                    and not (relation == "references" and URL_RE.match(target))
                    for target in targets
                ):
                    errors.append(
                        f"{path}: relationship {relation!r} has invalid target"
                    )
                elif any(
                    isinstance(target, str)
                    and GRAPH_ID_RE.fullmatch(target)
                    and target not in known_ids
                    for target in targets
                ):
                    errors.append(
                        f"{path}: relationship {relation!r} has unresolved target"
                    )
        if any(
            isinstance(value, str) and value.startswith((".agent/", "../"))
            for value in artifact.values()
        ):
            errors.append(
                f"{path}: product metadata must not depend on metaproject paths"
            )
    return errors


def check_empty_markdown() -> list[str]:
    """Reject zero-byte .md files: Pi loads any .md under a declared skill
    directory and requires at least a description, so empty placeholders
    break skill discovery (rules/architecture.md regression)."""
    errors: list[str] = []
    for path in ROOT.rglob("*.md"):
        if path.is_file() and path.stat().st_size == 0:
            errors.append(f"{path}: empty markdown file breaks skill discovery")
    return errors


def main() -> int:
    errors: list[str] = []
    for required in (
        "manifest.yaml",
        "capabilities.yaml",
        "AGENTS.md",
        ".pi/settings.json",
    ):
        if not (ROOT / required).exists():
            errors.append(f"{required}: missing")
    for forbidden in (ROOT / ".pi" / "memory", ROOT / ".agent", ROOT / "evaluations"):
        if forbidden.exists():
            errors.append(f"{forbidden}: forbidden in standalone product")
    skills = (
        list((ROOT / "rules").rglob("SKILL.md"))
        + list((ROOT / "recipes").rglob("SKILL.md"))
        + list((ROOT / "knowledge" / "catalogs").rglob("SKILL.md"))
    )
    for path in skills:
        errors.extend(check_skill(path))
    if len(skills) != EXPECTED_PRODUCT_SKILLS:
        errors.append(
            f"skills: expected {EXPECTED_PRODUCT_SKILLS}, found {len(skills)}"
        )
    for path in (ROOT / "snippets").glob("*/SNIPPET.yaml"):
        errors.extend(check_snippet(path))
        if (
            not (path.parent / "example.go").exists()
            or not (path.parent / "check.sh").exists()
        ):
            errors.append(f"{path.parent}: example.go and check.sh are required")
    for path in (ROOT / ".pi" / "prompts").glob("*.md"):
        try:
            if not parse_frontmatter(path).get("description"):
                errors.append(f"{path}: description is required")
        except ValueError as error:
            errors.append(str(error))
    errors.extend(check_knowledge_metadata())
    errors.extend(check_empty_markdown())
    for name in EXPECTED_TEMPLATES:
        for required in (
            "template.yaml",
            "README.md",
            "go.mod",
            "main.go",
            "main_test.go",
        ):
            if not (ROOT / "templates" / name / required).exists():
                errors.append(f"templates/{name}: missing {required}")
    errors.extend(check_bundle())
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(
        f"kitv2: PASS ({len(skills)} product skills, 3 snippets, standalone, offline bundle)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
