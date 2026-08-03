#!/usr/bin/env python3
"""Validate cognitive graph metadata and offline source routing."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PRODUCT = ROOT / "KitV2"
COGNITIVE = ROOT / ".agent" / "cognitive"
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
STATUSES = {"proposed", "active", "deprecated", "rejected"}
RELATIONS = {
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
ID_RE = re.compile(
    r"^(?:rule|recipe|pattern|snippet|template|capability|evaluation|decision-record|source|memory):[^:]+:.+$"
)


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected mapping")
    return value


def graph_objects(catalog: dict) -> set[str]:
    objects: set[str] = set()
    for source in catalog.get("sources", []):
        if isinstance(source, dict) and isinstance(source.get("id"), str):
            objects.add(source["id"])
        transformations = (
            source.get("transformations", {}) if isinstance(source, dict) else {}
        )
        for values in transformations.values():
            if isinstance(values, str):
                values = [values]
            if isinstance(values, list):
                objects.update(
                    value
                    for value in values
                    if isinstance(value, str) and ID_RE.match(value)
                )
        targets = source.get("target_status", {}) if isinstance(source, dict) else {}
        if isinstance(targets, dict):
            objects.update(
                target
                for target in targets
                if isinstance(target, str) and ID_RE.match(target)
            )
    return objects


def target_statuses(catalog: dict) -> dict[str, dict]:
    statuses: dict[str, dict] = {}
    for source in catalog.get("sources", []):
        if not isinstance(source, dict):
            continue
        targets = source.get("target_status", {})
        if isinstance(targets, dict):
            for target, metadata in targets.items():
                if isinstance(target, str) and isinstance(metadata, dict):
                    statuses[target] = metadata
    return statuses


def main() -> int:
    errors: list[str] = []
    schema = load(COGNITIVE / "graph-schema.yaml")
    catalog = load(COGNITIVE / "source-catalog.yaml")
    technology_doc = load(COGNITIVE / "technology-documentation.yaml")
    technology_units = load(COGNITIVE / "technology-source-units.yaml")
    required = set(schema["required_metadata"])
    known = graph_objects(catalog)
    statuses = target_statuses(catalog)

    required_doc = set(technology_doc["metadata"]["required"])
    unit_ids = {
        unit.get("id")
        for unit in technology_units.get("units", [])
        if isinstance(unit, dict)
    }
    for technology in technology_doc.get("technologies", []):
        missing = required_doc - technology.keys()
        if missing:
            errors.append(
                f"technology {technology.get('technology')}: missing metadata {sorted(missing)}"
            )
        if technology.get("status") not in {"active", "partial", "missing"}:
            errors.append(f"technology {technology.get('technology')}: invalid status")
        if (
            not isinstance(technology.get("official_urls"), list)
            or not technology["official_urls"]
        ):
            errors.append(
                f"technology {technology.get('technology')}: official_urls required"
            )
        for unit in technology.get("local_units", []):
            if (
                isinstance(unit, str)
                and unit.startswith("source-cache:")
                and unit not in unit_ids
            ):
                errors.append(
                    f"technology {technology.get('technology')}: unresolved source unit {unit}"
                )
    if technology_doc.get("scope") != "metaproject-only":
        errors.append("technology documentation registry must be metaproject-only")
    if technology_units.get("scope") != "metaproject-only":
        errors.append("technology source units must be metaproject-only")

    for target, metadata in statuses.items():
        status = metadata.get("status")
        if status not in STATUSES:
            errors.append(f"catalog target {target}: invalid status {status!r}")
        if status == "active":
            paths = metadata.get("materialized_by", [])
            if not isinstance(paths, list) or not paths:
                errors.append(
                    f"catalog target {target}: active target needs materialized_by"
                )
            for relative in paths if isinstance(paths, list) else []:
                if not isinstance(relative, str) or not (PRODUCT / relative).exists():
                    errors.append(
                        f"catalog target {target}: missing materialization {relative!r}"
                    )

    for path in sorted((PRODUCT / "knowledge" / "stdlib").glob("*.yaml")):
        try:
            artifact = load(path)
        except (OSError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{path}: invalid YAML: {error}")
            continue
        missing = required - artifact.keys()
        if missing:
            errors.append(f"{path}: missing metadata {sorted(missing)}")
        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, str) or not ID_RE.match(artifact_id):
            errors.append(f"{path}: invalid stable id")
        if artifact.get("kind") not in GRAPH_KINDS:
            errors.append(f"{path}: invalid kind {artifact.get('kind')!r}")
        if artifact.get("status") not in STATUSES:
            errors.append(f"{path}: invalid status {artifact.get('status')!r}")
        relationships = artifact.get("relationships", {})
        if not isinstance(relationships, dict):
            errors.append(f"{path}: relationships must be a mapping")
            continue
        for relation, targets in relationships.items():
            if relation not in RELATIONS:
                errors.append(f"{path}: unknown relationship {relation!r}")
                continue
            if not isinstance(targets, list):
                errors.append(f"{path}: relationship {relation!r} must be a list")
                continue
            for target in targets:
                if (
                    isinstance(target, str)
                    and ID_RE.match(target)
                    and target not in known
                ):
                    errors.append(f"{path}: unresolved relationship target {target}")
                if (
                    isinstance(target, str)
                    and target in statuses
                    and statuses[target].get("status") != "active"
                ):
                    errors.append(f"{path}: relationship target is not active {target}")

        source_id = artifact.get("id")
        capabilities = artifact.get("capabilities")
        if isinstance(source_id, str) and isinstance(capabilities, list):
            source_units = next(
                (
                    source.get("retrieval_units", [])
                    for source in catalog.get("sources", [])
                    if isinstance(source, dict) and source.get("id") == source_id
                ),
                None,
            )
            if isinstance(source_units, list):
                unknown_units = sorted(
                    unit for unit in capabilities if unit not in source_units
                )
                if unknown_units:
                    errors.append(
                        f"{path}: capabilities not in catalog retrieval_units: {unknown_units}"
                    )

    for path in sorted((PRODUCT / "knowledge" / "stdlib").glob("*.yaml")):
        text = path.read_text(encoding="utf-8")
        if ".agent/" in text or "../.agent" in text:
            errors.append(
                f"{path}: product metadata must not depend on metaproject paths"
            )

    product_manifest = PRODUCT / "tools" / "offline" / "bundle" / "manifest.json"
    if not product_manifest.exists():
        errors.append(f"{product_manifest}: missing self-contained bundle")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"cognitive: PASS ({len(known)} catalog objects)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
