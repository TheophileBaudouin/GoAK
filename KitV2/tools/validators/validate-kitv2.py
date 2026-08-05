#!/usr/bin/env python3
"""Validate the standalone KitV2 product."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
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
TEMPLATE_STATUSES = {"planned", "sourced", "legacy", "deprecated"}
CATALOG_MAX_AGE_DAYS = 90
REFERENCE_MAX_AGE_DAYS = 180
SOURCE_HEADING_RE = re.compile(
    r"^##+\s+Sources v[ée]rifi[ée]es\s*$", re.IGNORECASE | re.MULTILINE
)
GO_FENCE_RE = re.compile(r"^```(?:go|golang)\s*$", re.IGNORECASE)
FENCE_RE = re.compile(r"^```\s*$")
BLANK_RETURN_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\s*,\s*_\s*:=")
UNCHECKED_CALL_RE = re.compile(
    r"(?:\.Close|\.Run|\.Write|\.Copy|\.Encode|\.Decode|\.ListenAndServe|"
    r"\.Query|\.Open|\.Convert|\.LoadFromData|\.GenericContainer|"
    r"\.MappedPort)\([^)]*\)"
)


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


def check_freshness(path: Path, warnings: list[str]) -> list[str]:
    """Apply the C0 12/18-month freshness thresholds to dated artifacts."""
    try:
        if path.name == "SKILL.md":
            verified = parse_frontmatter(path).get("last-verified", "")
        elif path.suffix in {".yaml", ".yml"}:
            artifact = yaml.safe_load(path.read_text(encoding="utf-8"))
            verified = (
                artifact.get("last_verified", "") if isinstance(artifact, dict) else ""
            )
        else:
            return []
        verified_date = date.fromisoformat(str(verified))
    except (OSError, ValueError, yaml.YAMLError):
        return []
    age = (date.today() - verified_date).days
    if age > 548:
        return [f"{path}: artifact evidence is {age} days old (limit 548 days)"]
    if age > 365:
        warnings.append(
            f"{path}: artifact evidence is {age} days old (warning at 365 days)"
        )
    return []


def check_catalog_freshness(path: Path) -> list[str]:
    """Require dated source evidence for catalog modules.

    Catalog prose still needs human source review; this check only enforces the
    deterministic part of the contract: a source section and a bounded date.
    """
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    values = parse_frontmatter(path)
    source_heading = SOURCE_HEADING_RE.search(text)
    if source_heading is None:
        return [f"{path}: missing 'Sources vérifiées' section"]
    source_text = text[source_heading.end() :]
    if not re.search(r"https?://", source_text):
        errors.append(f"{path}: Sources vérifiées must contain a URL")
    if not re.search(r"20\d{2}-\d{2}-\d{2}", source_text):
        errors.append(f"{path}: Sources vérifiées must contain a verification date")
    try:
        verified = date.fromisoformat(values.get("last-verified", ""))
    except ValueError:
        return errors
    age = (date.today() - verified).days
    limit = (
        REFERENCE_MAX_AGE_DAYS
        if "reference-projects" in path.parts
        else CATALOG_MAX_AGE_DAYS
    )
    if age > limit:
        errors.append(f"{path}: catalog evidence is {age} days old (limit {limit})")
    return errors


def check_markdown_examples(path: Path) -> list[str]:
    """Tripwire for unchecked returns in fenced Go examples.

    This deliberately reports suspicious snippets rather than pretending a
    Markdown block is a complete Go package. Canonical behavior belongs in the
    compiled recipe/snippet tests.
    """
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_go = False
    for number, line in enumerate(lines, start=1):
        if GO_FENCE_RE.match(line):
            in_go = True
            continue
        if in_go and FENCE_RE.match(line):
            in_go = False
            continue
        if not in_go or "illustrative" in line.lower():
            continue
        if BLANK_RETURN_RE.search(line):
            errors.append(f"{path}:{number}: fenced Go example ignores a return value")
        if UNCHECKED_CALL_RE.search(line) and not re.search(
            r"(?:if\s+[^\n]*\berr\b|\berr\s*:=|\breturn\b|\blog\.Fatal|"
            r"//[^\n]*(?:best-effort|preserve|justif|cannot recover|"
            r"no recoverable)|_\s*=)",
            line,
        ):
            errors.append(
                f"{path}:{number}: fenced Go call may return an unchecked error"
            )
    return errors


def check_internal_duplicates(path: Path) -> list[str]:
    """Catch exact duplicate paragraphs while leaving semantic review to humans."""
    paragraphs = [
        " ".join(block.split())
        for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8"))
        if len(block.split()) >= 12
    ]
    duplicates = sorted(
        {paragraph for paragraph in paragraphs if paragraphs.count(paragraph) > 1}
    )
    return [
        f"{path}: exact duplicate paragraph detected: {paragraph[:100]}…"
        for paragraph in duplicates
    ]


def check_snippet(path: Path) -> list[str]:
    keys = {
        line.split(":", 1)[0] + ":"
        for line in path.read_text().splitlines()
        if ":" in line
    }
    missing = {"id:", "purpose:", "source:", "files:", "tests:"} - keys
    errors = [f"{path}: missing {sorted(missing)}"] if missing else []
    check = path.parent / "check.sh"
    if not check.exists():
        return errors + [f"{check}: missing executable check"]
    check_text = check.read_text(encoding="utf-8")
    if "gofmt -w" in check_text:
        errors.append(f"{check}: check must not mutate the snippet")
    if not re.search(r"\bgo\s+(?:test|run)\b", check_text):
        errors.append(f"{check}: check must compile and execute with go test or go run")
    return errors


def check_probe_runner() -> list[str]:
    runner = ROOT / "probes" / "run.sh"
    if not runner.exists():
        return [f"{runner}: missing probe runner"]
    text = runner.read_text(encoding="utf-8")
    errors: list[str] = []
    if not re.search(r"probes/\*/", text):
        errors.append(f"{runner}: must discover probes with a glob")
    if re.search(r"for\s+probe\s+in\s+(?:[a-z0-9-]+\s+){1,}[a-z0-9-]+", text):
        errors.append(f"{runner}: hardcoded probe list is forbidden")
    return errors


def check_template_status() -> list[str]:
    errors: list[str] = []
    template_paths = sorted((ROOT / "templates").glob("*/template.yaml"))
    for path in template_paths:
        try:
            template = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            errors.append(f"{path}: invalid template metadata: {error}")
            continue
        status = template.get("status") if isinstance(template, dict) else None
        if status not in TEMPLATE_STATUSES:
            errors.append(
                f"{path}: invalid status {status!r}; expected {sorted(TEMPLATE_STATUSES)}"
            )
        if status == "sourced":
            for field in ("source", "license", "last_verified"):
                if not template.get(field):
                    errors.append(f"{path}: sourced template missing {field}")
            if template.get("license") != "MIT":
                errors.append(f"{path}: sourced template license must be MIT")
            for required in ("LICENSE", "ATTRIBUTION.md", "README.md"):
                if not path.parent.joinpath(required).exists():
                    errors.append(f"{path.parent}: sourced template missing {required}")
            attribution = path.parent / "ATTRIBUTION.md"
            if attribution.exists() and "Technical scope" not in attribution.read_text(
                encoding="utf-8"
            ):
                errors.append(f"{attribution}: missing Technical scope section")
    return errors


def check_manifest_capabilities_coherence(
    warnings: list[str], root: Path = ROOT
) -> list[str]:
    """C1 §2/§3.2 — manifest.capabilities and capabilities.yaml share one
    kebab-case vocabulary, every capability carries source+status+criteria,
    and the canonical mapping agrees with capabilities.yaml sources.

    Previously only coverage.* counts were checked, so aliased or missing
    capability names (KVA-002) passed the gate.
    """
    errors: list[str] = []
    try:
        manifest = yaml.safe_load((root / "manifest.yaml").read_text(encoding="utf-8"))
        capabilities = yaml.safe_load(
            (root / "capabilities.yaml").read_text(encoding="utf-8")
        )
    except (OSError, yaml.YAMLError) as error:
        return [f"manifest/capabilities: unreadable: {error}"]
    if not isinstance(manifest, dict) or not isinstance(capabilities, dict):
        return ["manifest/capabilities: expected mappings"]
    declared = manifest.get("capabilities")
    canonical = manifest.get("canonical", {}) if isinstance(manifest, dict) else {}
    if not isinstance(declared, list) or not all(
        isinstance(item, str) and NAME_RE.fullmatch(item) for item in declared
    ):
        errors.append("manifest.yaml: capabilities must be a kebab-case list")
    declared_set = set(declared) if isinstance(declared, list) else set()
    entries = capabilities.get("capabilities", {})
    if not isinstance(entries, dict):
        return ["capabilities.yaml: capabilities must be a mapping"]
    for key in entries:
        entry = entries[key]
        if not isinstance(entry, dict) or not {"source", "status"} <= set(entry):
            errors.append(
                f"capabilities.yaml: capability {key!r} must carry source and status"
            )
    capability_keys = {
        key
        for key, entry in entries.items()
        if isinstance(entry, dict) and {"source", "status"} <= set(entry)
    }
    if declared_set != capability_keys:
        errors.append(
            "manifest.capabilities "
            f"{sorted(declared_set)} != capabilities.yaml keys {sorted(capability_keys)}"
        )
    for key in sorted(capability_keys):
        entry = entries[key]
        if not NAME_RE.fullmatch(key):
            errors.append(f"capabilities.yaml: non-kebab capability key {key!r}")
        if not isinstance(entry.get("criteria"), str) or not entry["criteria"].strip():
            errors.append(f"capabilities.yaml: {key} missing criteria (C1 §6)")
        canonical_path = canonical.get(key)
        if canonical_path is not None:
            source = str(entry.get("source", "")).rstrip("/")
            if source != str(canonical_path).rstrip("/"):
                errors.append(
                    f"capabilities.yaml: {key} source {source!r} != manifest "
                    f"canonical {str(canonical_path)!r}"
                )
    for key in sorted(set(canonical) - capability_keys):
        warnings.append(f"manifest canonical {key!r} has no capabilities.yaml entry")
    return errors


def check_recipe_dependencies(warnings: list[str], root: Path = ROOT) -> list[str]:
    """Z3 §4.3/§8 — every direct dependency of the product module must be
    vetted in the library catalog or a stdlib pointer.

    Module paths are matched against the vetted corpus (catalog SKILL.md,
    catalog YAML, stdlib pointers) by longest prefix (>= 2 segments), so
    koanf's provider submodule resolves through the koanf fiche. Indirect
    dependencies (the second require block) are exempt.
    """
    go_mod = root / "go.mod"
    if not go_mod.exists():
        return []
    text = go_mod.read_text(encoding="utf-8")
    match = re.search(r"require\s*\((.*?)\)", text, re.DOTALL)
    deps: list[str] = []
    if match:
        deps = [
            line.split()[0]
            for line in match.group(1).splitlines()
            if line.strip() and not line.strip().startswith("//")
        ]
    else:
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("require ") and "(" not in stripped:
                fields = stripped.split()
                if len(fields) >= 2:
                    deps.append(fields[1])
        if not deps:
            warnings.append(
                "go.mod: no parenthesized require block — dependency vetting "
                "check skipped (PARTIAL)"
            )
            return []
    corpus: list[str] = []
    for pattern in ("catalogs/libraries", "stdlib"):
        for path in (root / "knowledge" / pattern).rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml"}:
                try:
                    corpus.append(path.read_text(encoding="utf-8"))
                except OSError:
                    continue
    haystack = "\n".join(corpus)
    errors: list[str] = []
    for dep in deps:
        parts = dep.split("/")
        candidates = [
            "/".join(parts[: index + 1]) for index in range(len(parts) - 1, 0, -1)
        ]
        if any(candidate in haystack for candidate in candidates):
            continue
        errors.append(
            f"go.mod: dependency {dep!r} is not vetted in knowledge/catalogs "
            "or knowledge/stdlib (Z3 §4.3)"
        )
    return errors


def check_template_build(warnings: list[str], root: Path = ROOT) -> list[str]:
    """Z5 §8 — sourced templates must compile.

    Each template is a separate Go module that the root-module gate never
    builds, so a template can ship broken (the KVA-001 regression: the
    rest-api entry point was missing from the tracked tree). This check runs
    `go build ./...` inside every sourced template directory. If `go` is
    absent the check is skipped with a PARTIAL warning, mirroring the gate
    rule for missing tools.
    """
    errors: list[str] = []
    if shutil.which("go") is None:
        warnings.append(
            "templates: `go` not on PATH — template build check skipped (PARTIAL)"
        )
        return errors
    for path in sorted((root / "templates").glob("*/template.yaml")):
        try:
            template = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(template, dict) or template.get("status") != "sourced":
            continue
        template_dir = path.parent
        if not (template_dir / "go.mod").exists():
            errors.append(f"{template_dir}: sourced template missing go.mod")
            continue
        try:
            result = subprocess.run(
                ["go", "build", "./..."],
                cwd=template_dir,
                capture_output=True,
                text=True,
                timeout=180,
            )
        except subprocess.TimeoutExpired as error:
            errors.append(f"{template_dir}: template build timed out: {error}")
            continue
        if result.returncode != 0:
            tail = "\n".join((result.stderr or result.stdout).splitlines()[-6:])
            errors.append(f"{template_dir}: template does not compile:\n{tail}")
    return errors


def coverage_counts() -> dict[str, int]:
    rules = list((ROOT / "rules").rglob("SKILL.md"))
    recipes = list((ROOT / "recipes").rglob("SKILL.md"))
    catalogs = list((ROOT / "knowledge" / "catalogs").rglob("SKILL.md"))
    probes = list((ROOT / "probes").glob("*/main.go"))
    templates = list((ROOT / "templates").glob("*/template.yaml"))
    return {
        "product_skills": len(rules) + len(recipes) + len(catalogs),
        "rules": len(rules),
        "recipes": len(recipes),
        "knowledge_catalogs": len(catalogs),
        "probes": len(probes),
        "project_templates": len(templates),
    }


def check_coverage() -> list[str]:
    path = ROOT / "capabilities.yaml"
    try:
        capabilities = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        return [f"{path}: invalid capabilities metadata: {error}"]
    expected = coverage_counts()
    actual = capabilities.get("coverage", {}) if isinstance(capabilities, dict) else {}
    errors: list[str] = []
    for key, value in expected.items():
        if actual.get(key) != value:
            errors.append(
                f"{path}: coverage.{key}={actual.get(key)!r}, expected {value}"
            )
    return errors


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


INDEXABLE_GLOBS = (
    "rules/**/SKILL.md",
    "recipes/**/SKILL.md",
    "knowledge/catalogs/**/SKILL.md",
    "knowledge/**/*.yaml",
    "snippets/*/SNIPPET.yaml",
    "templates/*/template.yaml",
    ".pi/prompts/*.md",
    ".pi/skills/**/SKILL.md",
)


def check_router() -> list[str]:
    """Validate the generated router index (Z11): artifact present, schema
    valid, checksum matches meta.json, full coverage of indexable resources,
    every entry points to an existing file. The index is generated by the
    metaproject builder; any drift here blocks the release."""
    errors: list[str] = []
    router = ROOT / "router"
    index_path = router / "index.json"
    meta_path = router / "meta.json"
    if not index_path.exists() or not meta_path.exists():
        return [
            f"router/: {index_path.name} and {meta_path.name} are required "
            "(generated artifact — regenerate before release)"
        ]
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{index_path}: invalid JSON: {error}"]
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{meta_path}: invalid JSON: {error}"]
    if index.get("schema") != 1:
        errors.append(f"{index_path}: unsupported schema {index.get('schema')!r}")
    if meta.get("schema") != 1:
        errors.append(f"{meta_path}: unsupported schema {meta.get('schema')!r}")
    checksum = hashlib.sha256(index_path.read_bytes()).hexdigest()
    if meta.get("index_sha256") != checksum:
        errors.append(
            f"router/: {index_path.name} does not match the {meta_path.name} "
            "checksum — regenerate the index"
        )
    try:
        manifest_version = yaml.safe_load(
            (ROOT / "manifest.yaml").read_text(encoding="utf-8")
        ).get("version")
    except (OSError, yaml.YAMLError, AttributeError):
        manifest_version = None
    if manifest_version and meta.get("version") != manifest_version:
        errors.append(
            f"router/: meta.json version {meta.get('version')!r} does not match "
            f"manifest version {manifest_version!r} — regenerate the index"
        )
    resources = index.get("resources", [])
    if not isinstance(resources, list) or not resources:
        return errors + [f"{index_path}: resources list is empty"]
    indexed: set[str] = set()
    for resource in resources:
        if not isinstance(resource, dict):
            errors.append(f"{index_path}: non-object entry")
            continue
        path = resource.get("path")
        if not path:
            errors.append(f"{index_path}: entry {resource.get('id')!r} missing path")
            continue
        indexed.add(path)
        if not (ROOT / path).exists():
            errors.append(f"router/: entry path does not exist: {path}")
        if not resource.get("description") or not resource.get("terms"):
            errors.append(
                f"router/: entry {resource.get('id')!r} missing description or terms"
            )
    expected = {
        str(path.relative_to(ROOT))
        for pattern in INDEXABLE_GLOBS
        for path in ROOT.glob(pattern)
        if path.is_file()
    }
    missing = sorted(expected - indexed)
    if missing:
        errors.append(
            f"router/: index missing {len(missing)} resources "
            f"({missing[:5]}…) — regenerate the index"
        )
    stale = sorted(indexed - expected)
    if stale:
        errors.append(
            f"router/: index has {len(stale)} stale entries ({stale[:5]}…) — "
            "regenerate the index"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
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
    strict_catalog = os.environ.get("KITV2_STRICT_CATALOG") == "1"
    for path in skills:
        errors.extend(check_skill(path))
        errors.extend(check_freshness(path, warnings))
        if strict_catalog and path.is_relative_to(ROOT / "knowledge" / "catalogs"):
            errors.extend(check_catalog_freshness(path))
            errors.extend(check_markdown_examples(path))
            errors.extend(check_internal_duplicates(path))
        if strict_catalog and path.is_relative_to(ROOT / "recipes"):
            errors.extend(check_markdown_examples(path))
    errors.extend(check_coverage())
    errors.extend(check_manifest_capabilities_coherence(warnings))
    errors.extend(check_recipe_dependencies(warnings))
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
    for path in sorted((ROOT / "knowledge").rglob("*.yaml")):
        errors.extend(check_freshness(path, warnings))
    errors.extend(check_empty_markdown())
    errors.extend(check_router())
    errors.extend(check_probe_runner())
    errors.extend(check_template_status())
    errors.extend(check_template_build(warnings))
    errors.extend(check_bundle())
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    for warning in warnings:
        print(f"warning: {warning}")
    try:
        router_count = len(
            json.loads(
                (ROOT / "router" / "index.json").read_text(encoding="utf-8")
            ).get("resources", [])
        )
    except (OSError, json.JSONDecodeError):
        router_count = 0
    print(
        f"kitv2: PASS ({len(skills)} product skills, 3 snippets, standalone, "
        f"offline bundle, router index {router_count} resources)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
