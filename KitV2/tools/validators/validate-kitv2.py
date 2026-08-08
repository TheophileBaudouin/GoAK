#!/usr/bin/env python3
"""Validate the standalone KitV2 product."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Layer 5.1 drift gate for templates (shared with tools/generators).
structure_md = _load_module(
    "structure_md", ROOT / "tools" / "generators" / "structure_md.py"
)
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
    r"^##+\s+(?:Verified sources|Sources v[ée]rifi[ée]es)\s*$",
    re.IGNORECASE | re.MULTILINE,
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
        return [f"{path}: missing 'Verified sources' section"]
    source_text = text[source_heading.end() :]
    if not re.search(r"https?://", source_text):
        errors.append(f"{path}: Verified sources must contain a URL")
    if not re.search(r"20\d{2}-\d{2}-\d{2}", source_text):
        errors.append(f"{path}: Verified sources must contain a verification date")
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


def check_snippet_chain(root: Path = ROOT) -> list[str]:
    """D-2026-08-05-11 cross-file freshness: a snippet must be re-verified
    when its canonical source changes. Mechanical form: when both the snippet
    and its canonical source carry a last-verified date, the snippet date must
    be >= the canonical date. Missing dates are ignored (Z4 §3: the field is
    recommended, not required). Source resolution itself stays check_snippet's
    responsibility."""
    errors: list[str] = []
    for path in sorted((root / "snippets").glob("*/SNIPPET.yaml")):
        try:
            values = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            errors.append(f"{path}: invalid YAML: {error}")
            continue
        if not isinstance(values, dict):
            continue
        snippet_date = values.get("last_verified", "")
        source = values.get("source", "")
        if isinstance(snippet_date, date) and not isinstance(snippet_date, str):
            snippet_date = snippet_date.isoformat()
        if not isinstance(snippet_date, str) or not snippet_date:
            continue
        if not isinstance(source, str) or not source:
            continue
        source_path = (path.parent / source).resolve()
        try:
            canonical_date = parse_frontmatter(source_path).get("last-verified", "")
        except (OSError, ValueError):
            continue  # missing/unreadable canonical is a different check
        if canonical_date and snippet_date < canonical_date:
            errors.append(
                f"{path}: last_verified {snippet_date} older than canonical "
                f"source {source_path} ({canonical_date}) — re-verify the snippet"
            )
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
    readme = ROOT / "probes" / "README.md"
    if readme.exists():
        probes = sorted(
            probe.parent.name for probe in (ROOT / "probes").glob("*/main.go")
        )
        inventory = sorted(
            re.findall(
                r"^\| `([a-z0-9-]+)` \|", readme.read_text(encoding="utf-8"), re.M
            )
        )
        if inventory != probes:
            missing = sorted(set(probes) - set(inventory))
            extra = sorted(set(inventory) - set(probes))
            errors.append(
                f"{readme}: probe inventory out of sync "
                f"(missing {missing or 'none'}, extra {extra or 'none'})"
            )
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
            if not template.get("usage-evidence"):
                errors.append(
                    f"{path}: sourced template missing usage-evidence "
                    "(charter §16.1.3: documented real usage at admission)"
                )
            if not template.get("structure.md"):
                errors.append(
                    f"{path}: sourced template missing structure.md declaration "
                    "(charter Layer 5.1: generation or validation mechanism)"
                )
            if template.get("license") != "MIT":
                errors.append(f"{path}: sourced template license must be MIT")
            for required in ("LICENSE", "ATTRIBUTION.md", "README.md", "structure.md"):
                if not path.parent.joinpath(required).exists():
                    errors.append(f"{path.parent}: sourced template missing {required}")
            attribution = path.parent / "ATTRIBUTION.md"
            if attribution.exists() and "Technical scope" not in attribution.read_text(
                encoding="utf-8"
            ):
                errors.append(f"{attribution}: missing Technical scope section")
            structure_file = path.parent / "structure.md"
            if structure_file.exists():
                errors.extend(
                    f"{structure_file}: {defect}"
                    for defect in structure_md.check(
                        path.parent, structure_file.read_text(encoding="utf-8")
                    )
                )
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
    ui_kit_skills = list((ROOT / "ui-kit" / "skills").rglob("SKILL.md"))
    return {
        "product_skills": len(rules) + len(recipes) + len(catalogs),
        "rules": len(rules),
        "recipes": len(recipes),
        "knowledge_catalogs": len(catalogs),
        "probes": len(probes),
        "project_templates": len(templates),
        "ui_kit_skills": len(ui_kit_skills),
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
    go_mod = ROOT / "go.mod"
    required: dict[str, str] = {}
    if go_mod.exists():
        for match in re.finditer(
            r"require\s*\((.*?)\)", go_mod.read_text(encoding="utf-8"), re.DOTALL
        ):
            for line in match.group(1).splitlines():
                fields = line.split()
                if len(fields) >= 2 and not fields[0].startswith("//"):
                    required[fields[0]] = fields[1]
    for module in manifest.get("modules", []):
        path, version = module.get("path", ""), module.get("version", "")
        pinned = required.get(path)
        if pinned is None:
            errors.append(f"{manifest_path}: module {path!r} is not required by go.mod")
        elif pinned != version:
            errors.append(
                f"{manifest_path}: module {path!r} pinned {version}, go.mod requires {pinned}"
            )
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


def check_declared_skill_dirs() -> list[str]:
    """Every root-level .md file in a declared skill directory must carry a
    frontmatter `description` (Pi semantics: a directory listed in
    .pi/settings.json "skills" loads its root .md files as individual
    skills when it has no SKILL.md at its root, and skills with a missing
    description are NOT loaded — recipes/README.md regression, where Pi
    reported "[Skill conflicts] … description is required").

    A `description` (and a valid `name`) makes the file load cleanly;
    `disable-model-invocation: true` keeps a pure index out of the system
    prompt while staying loadable by path."""
    errors: list[str] = []
    settings = ROOT / ".pi" / "settings.json"
    if not settings.exists():
        return []  # the UI-registration check reports the missing settings
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []  # malformed settings is reported elsewhere
    skills = data.get("skills") if isinstance(data, dict) else None
    if not isinstance(skills, list):
        return []
    for entry in skills:
        if not isinstance(entry, str) or not entry.startswith("../"):
            continue
        declared = (ROOT / entry.removeprefix("../")).resolve()
        if not declared.is_dir():
            continue
        if (declared / "SKILL.md").exists():
            continue  # a skill root: only SKILL.md loads, root .md files are inert
        for path in sorted(declared.glob("*.md")):
            if not path.is_file():
                continue
            try:
                values = parse_frontmatter(path)
            except ValueError as error:
                errors.append(str(error))
                continue
            if not values.get("description"):
                errors.append(
                    f"{path}: root .md in a declared skill directory needs a "
                    "frontmatter description (Pi loads it as a skill; missing "
                    "description = skill not loaded + conflict warning)"
                )
            name = values.get("name")
            if name and not re.fullmatch(r"[a-z0-9-]+", str(name)):
                errors.append(f"{path}: skill name {name!r} must be lowercase a-z0-9-")
    return errors


def check_no_metaproject_paths() -> list[str]:
    """A shipped file must never reference build-repository-only material.

    The installed product is the standalone kit: a consumer copy has no
    control directory, no charter, no dated decision or audit records, and
    no repository-folder name, so any such occurrence in a shipped file
    points at something that does not exist (regression guard)."""
    errors: list[str] = []
    extensions = {
        ".md",
        ".yaml",
        ".yml",
        ".ts",
        ".json",
        ".go",
        ".sh",
        ".txt",
        ".py",
    }
    markers = (
        (re.escape(".agent/"), "control-directory path"),
        ("KIT_CHARTER", "charter reference"),
        ("metaproject", "build-repository mention"),
        ("metaprojet", "build-repository mention"),
        ("meta-project", "build-repository mention"),
        (r"D-20\d{2}-\d{2}-\d{2}-\d{2}", "dated decision reference"),
        (r"KVA-\d+", "audit-finding reference"),
        (r"\bKitV2/", "repository-folder path"),
        (r"\bZ1[0-9]\b", "governance-contract reference"),
    )
    skip = {"validate-kitv2.py", "test_validate_kitv2.py"}
    local_owned = {"PIN.md", "scenarios.json"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix not in extensions:
            continue
        if path.name in skip:
            continue  # the checker and its test legitimately name the markers
        if path.is_relative_to(ROOT / "ui-kit") and path.name not in local_owned:
            continue  # the ui-kit mirror is a verbatim upstream pin (never
            # hand-edited); only its local-owned files must stay clean
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker, label in markers:
            if re.search(marker, text, flags=re.IGNORECASE):
                errors.append(f"{path}: {label} must not ship")
                break
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
    """Validate the generated router index: artifact present, schema
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


def check_router_scenarios() -> list[str]:
    """Validate the routing-quality contract: scenarios.json is a
    well-formed {query → expected resource ids} list, every expected id
    exists in the index, and off-domain scenarios expect no resources.

    This checks the contract file's integrity only. The actual ranking
    verification (expected ids within top-K under the real runtime scoring)
    is the ranking gate (node) — see router/scenarios.json header. The
    ranking gate is not duplicated here because the product validator must
    stay node-free; the scenario file is shipped so consumers and CI can
    run the node gate themselves."""
    errors: list[str] = []
    router = ROOT / "router"
    scenarios_path = router / "scenarios.json"
    index_path = router / "index.json"
    if not scenarios_path.exists():
        return [f"{scenarios_path}: missing routing-quality contract"]
    try:
        contract = json.loads(scenarios_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{scenarios_path}: invalid JSON: {error}"]
    if not isinstance(contract, dict) or contract.get("schema") != 1:
        return [f"{scenarios_path}: expected schema-1 contract mapping"]
    scenarios = contract.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return [f"{scenarios_path}: scenarios list is empty or missing"]
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
        indexed_ids = {
            resource.get("id")
            for resource in index.get("resources", [])
            if isinstance(resource, dict)
        }
    except (OSError, json.JSONDecodeError):
        indexed_ids = set()  # index drift is check_router's responsibility
    for number, scenario in enumerate(scenarios, start=1):
        where = f"{scenarios_path}: scenario #{number}"
        if not isinstance(scenario, dict):
            errors.append(f"{where}: expected a mapping")
            continue
        query = scenario.get("query")
        if not isinstance(query, str) or not 3 <= len(query) <= 300:
            errors.append(f"{where}: query must be a 3..300 char string")
        expect = scenario.get("expect")
        if not isinstance(expect, list) or not all(
            isinstance(item, str) and item for item in expect
        ):
            errors.append(f"{where}: expect must be a non-empty list of ids")
            expect = []
        top = scenario.get("top")
        if top is not None and (not isinstance(top, int) or not 1 <= top <= 8):
            errors.append(f"{where}: top must be an int in 1..8")
        off_domain = scenario.get("offDomain")
        if off_domain is not None and not isinstance(off_domain, bool):
            errors.append(f"{where}: offDomain must be a boolean")
        if off_domain and expect:
            errors.append(f"{where}: off-domain scenario must expect no ids")
        for expected_id in expect:
            if expected_id not in indexed_ids:
                errors.append(f"{where}: expected id {expected_id!r} not in the index")
    return errors


def check_ui_kit_pin() -> list[str]:
    """the ui-kit zone must carry a valid pin record and the SDK's
    own AGENTS.md, so the vendored content stays attributable and the zone
    stays self-contained."""
    errors: list[str] = []
    zone = ROOT / "ui-kit"
    agents = zone / "AGENTS.md"
    if not agents.exists():
        errors.append(
            f"{agents}: missing — the ui-kit zone must ship the SDK AGENTS.md"
        )
    pin = zone / "PIN.md"
    if not pin.exists():
        return errors + [f"{pin}: missing pin record"]
    text = pin.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"\| Pinned commit \(SHA\) \| `[0-9a-f]{40}` \|", text):
        errors.append(f"{pin}: missing a well-formed 40-hex pinned SHA")
    if not re.search(r"\| Sync date \| \d{4}-\d{2}-\d{2} \|", text):
        errors.append(f"{pin}: missing a YYYY-MM-DD sync date")
    return errors


def check_workspace_init_placeholder() -> list[str]:
    """Z14 — the kit AGENTS.md must carry the "Project Foundation" pointer
    section, delimited by its begin/end markers.

    The product always shows the not-yet-initialized state: the init
    session writes the per-project section into the CONSUMER project's
    AGENTS.md, never into the kit's. So the only valid state here is both
    markers present, begin before end, and the expected section title
    between them. A missing or altered section is a regression guard
    failure (two manual merge mechanisms live in this file — UI work and
    Project Foundation — and neither may silently swallow the other)."""
    errors: list[str] = []
    path = ROOT / "AGENTS.md"
    if not path.exists():
        return [f"{path}: missing"]
    text = path.read_text(encoding="utf-8", errors="replace")
    begin = "<!-- workspace-init section: begin -->"
    end = "<!-- workspace-init section: end -->"
    ib = text.find(begin)
    ie = text.find(end)
    if ib == -1 or ie == -1:
        return [
            f"{path}: Project Foundation section markers missing "
            "(workspace-init section begin/end)"
        ]
    if ib > ie:
        return [f"{path}: Project Foundation markers out of order"]
    between = text[ib + len(begin) : ie]
    if "## Project Foundation" not in between:
        return [f"{path}: Project Foundation section title missing between the markers"]
    return errors


def check_agents_md_contract(warnings: list[str]) -> list[str]:
    """Z9 §9 (D-2026-08-08-19/21) — the consumer AGENTS.md is an execution
    contract with a frozen canonical structure, a size budget, no
    historical content, and two owner-mandated top blocks. A rewrite must
    restructure, never append; these anchors make the structure checkable
    so the file cannot silently drift back into a manual."""
    errors: list[str] = []
    path = ROOT / "AGENTS.md"
    if not path.exists():
        return [f"{path}: missing"]
    text = path.read_text(encoding="utf-8", errors="replace")
    size = len(text.encode("utf-8"))
    if size > 16384:
        errors.append(
            f"{path}: {size} bytes exceed the 16 KiB budget (Z9 §9.4) — "
            "delegate detail to the zone sources instead of growing the root"
        )
    elif size > 12288:
        warnings.append(
            f"{path}: {size} bytes — near the 16 KiB budget (Z9 §9.4), "
            "prefer delegation over addition"
        )
    # Owner-mandated top blocks (Z9 §9.1a, D-2026-08-08-21): present, in
    # order, before "## Normative levels", with their sentinel sentences.
    # They are immutable across rewrites — dropping or renaming them fails.
    mandatory_blocks = (
        (
            "## Before doing anything",
            "Always use subagents. You are the orchestrator.",
        ),
        ("## Absolute rules", "You must always check which step of the to-do list"),
    )
    prev = -1
    for heading, sentinel in mandatory_blocks:
        index = text.find("\n" + heading)
        if index == -1:
            errors.append(
                f"{path}: mandatory block {heading!r} missing (Z9 §9.1a — "
                "owner-mandated top blocks must survive every rewrite)"
            )
            continue
        if sentinel not in text:
            errors.append(
                f"{path}: mandatory block {heading!r} missing sentinel "
                f"{sentinel!r} (Z9 §9.1a)"
            )
        if index <= prev:
            errors.append(
                f"{path}: mandatory blocks out of order (Z9 §9.1a — "
                "Before doing anything → Absolute rules, at the top)"
            )
        prev = index
    normative = text.find("\n## Normative levels")
    if prev != -1 and normative != -1 and prev > normative:
        errors.append(
            f"{path}: mandatory top blocks must precede '## Normative levels' "
            "(Z9 §9.1a)"
        )
    for heading in (
        "## Normative levels",
        "## Non-Negotiable Rules",
        "## Repository map",
        "## Task Routing",
        "## Memory",
        "## Validation",
        "## Limits",
    ):
        if f"\n{heading}" not in text:
            errors.append(
                f"{path}: required section {heading!r} missing (Z9 §9.1 "
                "canonical structure)"
            )
    positions = [
        text.find("\n" + heading)
        for heading in (
            "## Normative levels",
            "## Non-Negotiable Rules",
            "## Repository map",
            "## Task Routing",
            "## Memory",
            "## Validation",
            "## Limits",
        )
    ]
    if all(index != -1 for index in positions) and positions != sorted(positions):
        errors.append(
            f"{path}: required sections out of canonical order (Z9 §9.1 — "
            "Identity → Before doing anything → Absolute rules → Normative "
            "levels → … → Validation → Limits)"
        )
    for pattern, label in (
        (r"\(removed \d{4}", "removed-system history"),
        (r"replaces the former", "former-system history"),
        (r"\bbest practices\b", "'best practices' substitution"),
    ):
        if re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(
                f"{path}: {label} must not appear (Z9 §9.2) — describe "
                "the current state only"
            )
    return errors


def check_consumer_onboarding() -> list[str]:
    """The consumer onboarding system (D-2026-08-08-14..18) — shipped user
    guide, /goak-help entry point, onboarding banner, AGENTS.md pointer.

    The kit must always ship a self-contained onboarding surface: the user
    guide (.pi/docs/GOAK.md) with Get Started + deep-usage sections, the
    /goak-help prompt that points the agent at the local guide, the banner
    data file with the three entries (Get Started / large feature / small
    feature), the onboarding extension that appends it once at session
    start, and the marker-delimited "User guide" section in AGENTS.md. Any
    of these missing or drifted is a regression-guard failure: a consumer
    must be able to learn the kit from the kit itself, with no external
    documentation."""
    errors: list[str] = []

    guide = ROOT / ".pi" / "docs" / "GOAK.md"
    if not guide.is_file():
        errors.append(f"{guide}: missing — the consumer user guide is required")
    else:
        text = guide.read_text(encoding="utf-8", errors="replace")
        for heading in (
            "Get Started",
            "Commands",
            "Workflows",
            "Kit structure",
            "Troubleshooting",
        ):
            if heading not in text:
                errors.append(f"{guide}: required guide section {heading!r} missing")

    prompt = ROOT / ".pi" / "prompts" / "goak-help.md"
    if not prompt.is_file():
        errors.append(f"{prompt}: missing — the /goak-help command is required")
    else:
        text = prompt.read_text(encoding="utf-8", errors="replace")
        if ".pi/docs/GOAK.md" not in text:
            errors.append(
                f"{prompt}: must point the agent at the local guide "
                "(.pi/docs/GOAK.md) — a stale or external path is drift"
            )

    banner = ROOT / ".pi" / "onboarding" / "banner.md"
    if not banner.is_file():
        errors.append(f"{banner}: missing — the onboarding banner content is required")
    else:
        text = banner.read_text(encoding="utf-8", errors="replace")
        upper = text.upper()
        if "GET STARTED" not in upper:
            errors.append(f"{banner}: Get Started entry missing")
        if (
            upper.count("NEW FEATURE") < 2
            or "LARGE" not in upper
            or "SMALL" not in upper
        ):
            errors.append(
                f"{banner}: large and small feature entries missing "
                "(two NEW FEATURE entries expected)"
            )
        if "/goak-help" not in text:
            errors.append(f"{banner}: must point to the /goak-help entry point")

    extension = ROOT / ".pi" / "extensions" / "kit-onboarding.ts"
    if not extension.is_file():
        errors.append(f"{extension}: missing — the onboarding extension is required")
    else:
        text = extension.read_text(encoding="utf-8", errors="replace")
        for marker in ("session_start", "appendEntry", "registerEntryRenderer"):
            if marker not in text:
                errors.append(
                    f"{extension}: onboarding behavior marker {marker!r} missing"
                )

    agents = ROOT / "AGENTS.md"
    if not agents.exists():
        errors.append(f"{agents}: missing")
    else:
        text = agents.read_text(encoding="utf-8", errors="replace")
        begin = "<!-- user guide section: begin -->"
        end = "<!-- user guide section: end -->"
        ib = text.find(begin)
        ie = text.find(end)
        if ib == -1 or ie == -1:
            errors.append(f"{agents}: User guide section markers missing")
        elif ib > ie:
            errors.append(f"{agents}: User guide section markers out of order")
        elif "## User guide" not in text[ib + len(begin) : ie]:
            errors.append(
                f"{agents}: User guide section title missing between the markers"
            )
    return errors


def check_ui_kit_registration(
    root: Path | None = None,
) -> list[str]:
    """D-2026-08-08-02 — single registration point for the UI skills.

    The root .pi/settings.json must declare ../ui-kit/skills (additive with
    the Go skills), and the zone must contain NO nested
    ui-kit/.pi/settings.json (dead by design: deleted from the zone and
    excluded from re-syncs). A second registration source would resurrect
    the pre-registration failure mode (copied-but-invisible content)."""
    errors: list[str] = []
    root = root or ROOT
    settings = root / ".pi" / "settings.json"
    if not settings.exists():
        return [f"{settings}: missing — cannot verify the UI skill registration"]
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{settings}: invalid JSON: {error}"]
    skills = data.get("skills") if isinstance(data, dict) else None
    if not isinstance(skills, list) or "../ui-kit/skills" not in skills:
        errors.append(
            f"{settings}: the UI skill path '../ui-kit/skills' is not declared — "
            "the ui-kit zone is invisible to Pi without this registration (D-2026-08-08-02)"
        )
    for original in ("../rules", "../recipes"):
        if not isinstance(skills, list) or original not in skills:
            errors.append(
                f"{settings}: existing Go skill path {original!r} must be preserved "
                "(registration is additive)"
            )
    nested = root / "ui-kit" / ".pi" / "settings.json"
    if nested.exists():
        errors.append(
            f"{nested}: dead nested registration — the root .pi/settings.json is the "
            "single registration point (D-2026-08-08-02)"
        )
    return errors


def check_ui_kit_copy_rules() -> list[str]:
    """copy-rules.json (local-owned) drives the consumer sync tool.

    The file must be a list of {src, dst} with every src present inside the
    ui-kit zone (a rule pointing at a missing folder = stale rules that would
    make the consumer tool abort or copy nothing)."""
    errors: list[str] = []
    rules_path = ROOT / "ui-kit" / "copy-rules.json"
    if not rules_path.exists():
        return [f"{rules_path}: missing copy rules"]
    try:
        rules = json.loads(rules_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{rules_path}: invalid JSON: {error}"]
    if not isinstance(rules, list):
        return [f"{rules_path}: expected a list of {{src, dst}} rules"]
    for number, rule in enumerate(rules, start=1):
        if (
            not isinstance(rule, dict)
            or not isinstance(rule.get("src"), str)
            or not isinstance(rule.get("dst"), str)
            or not rule["src"]
            or not rule["dst"]
        ):
            errors.append(
                f"{rules_path}: rule #{number} must carry non-empty src and dst"
            )
            continue
        src_dir = ROOT / "ui-kit" / rule["src"]
        if not src_dir.is_dir():
            errors.append(
                f"{rules_path}: rule #{number} src {rule['src']!r} missing in the zone "
                "(stale copy rules — regenerate via the re-sync helper)"
            )
    return errors


def check_ui_kit_skills() -> list[str]:
    """ui-kit skills must stay Pi-discoverable as instructions.

    The vendored SDK owns its frontmatter schema (upstream ui-agent-kit), so
    only the Pi-native minimum is checked here: name + description, kebab-case
    name matching its directory. The kit facet fields (category/tags/
    last-verified) are deliberately NOT required — adding them would mean
    editing vendored SDK content (forbidden)."""
    errors: list[str] = []
    for path in sorted((ROOT / "ui-kit" / "skills").rglob("SKILL.md")):
        try:
            values = parse_frontmatter(path)
        except ValueError as error:
            errors.append(str(error))
            continue
        name = values.get("name")
        description = values.get("description")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"{path}: invalid or missing name")
        if path.parent.name != name:
            errors.append(f"{path}: name does not match directory")
        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            errors.append(f"{path}: description must be a 1..1024 char string")
    return errors


def check_ui_corpus_disjointness() -> list[str]:
    """the two routing corpora never mix.

    The Go index (router/index.json) must contain no path under ui-kit/, so a
    Go query can never surface a UI resource. The reverse direction (the UI
    index contains only ui-kit/ paths) is verified by the metaproject gate
    (run_ui_scenarios.mjs), which builds the UI index with the same shared
    core the runtime tool uses — node-free validator cannot build it here."""
    errors: list[str] = []
    index_path = ROOT / "router" / "index.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [f"{index_path}: unreadable — index drift is check_router's job"]
    for resource in index.get("resources", []):
        if not isinstance(resource, dict):
            continue
        path = str(resource.get("path", ""))
        if path.startswith("ui-kit/"):
            errors.append(
                f"{index_path}: Go corpus contains UI resource {path!r} "
                f"(id {resource.get('id')!r}) — corpora must stay disjoint"
            )
    return errors


def ui_kit_index_ids() -> set[str]:
    """Id convention of the UI index builder (kit-ui-router-core.ts):
    skills use their frontmatter name; ui-rules/patterns/ux/docs .md files use
    their filename stem (docs/authoring-guides/ excluded); the components
    index is the fixed id components-index. The metaproject gate verifies the
    REAL builder output; this node-free mirror keeps the contract's id
    linkage checkable anywhere. Convention drift is caught by the gate."""
    ids: set[str] = set()
    for path in (ROOT / "ui-kit" / "skills").rglob("SKILL.md"):
        try:
            values = parse_frontmatter(path)
        except ValueError:
            continue
        name = values.get("name")
        if isinstance(name, str) and name:
            ids.add(name)
    for zone in ("ui-rules", "patterns", "ux"):
        for path in (ROOT / "ui-kit" / zone).rglob("*.md"):
            ids.add(path.stem)
    for sub in ("docs", Path("ui-sdk") / "docs"):
        for path in (ROOT / "ui-kit" / sub).rglob("*.md"):
            if "authoring-guides" in path.parts:
                continue
            ids.add(path.stem)
    ids.add("components-index")
    return ids


def check_ui_router_scenarios() -> list[str]:
    """node-free integrity check of the UI routing-quality
    contract (ui-kit/scenarios.json): well-formed {query → expected ids}
    list, every expected id produced by the UI index builder, off-domain
    scenarios expect nothing. The actual ranking verification is the
    metaproject gate (run_ui_scenarios.mjs, node) — same two-layer split as
    the Go scenarios contract."""
    errors: list[str] = []
    scenarios_path = ROOT / "ui-kit" / "scenarios.json"
    if not scenarios_path.exists():
        return [f"{scenarios_path}: missing UI routing-quality contract"]
    try:
        contract = json.loads(scenarios_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"{scenarios_path}: invalid JSON: {error}"]
    if not isinstance(contract, dict) or contract.get("schema") != 1:
        return [f"{scenarios_path}: expected schema-1 contract mapping"]
    scenarios = contract.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return [f"{scenarios_path}: scenarios list is empty or missing"]
    known_ids = ui_kit_index_ids()
    for number, scenario in enumerate(scenarios, start=1):
        where = f"{scenarios_path}: scenario #{number}"
        if not isinstance(scenario, dict):
            errors.append(f"{where}: expected a mapping")
            continue
        query = scenario.get("query")
        if not isinstance(query, str) or not 3 <= len(query) <= 300:
            errors.append(f"{where}: query must be a 3..300 char string")
        expect = scenario.get("expect")
        if not isinstance(expect, list) or not all(
            isinstance(item, str) and item for item in expect
        ):
            errors.append(f"{where}: expect must be a non-empty list of ids")
            expect = []
        top = scenario.get("top")
        if top is not None and (not isinstance(top, int) or not 1 <= top <= 8):
            errors.append(f"{where}: top must be an int in 1..8")
        off_domain = scenario.get("offDomain")
        if off_domain is not None and not isinstance(off_domain, bool):
            errors.append(f"{where}: offDomain must be a boolean")
        if off_domain and expect:
            errors.append(f"{where}: off-domain scenario must expect no ids")
        for expected_id in expect:
            if expected_id not in known_ids:
                errors.append(
                    f"{where}: expected id {expected_id!r} not produced by the "
                    "UI index builder"
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
    errors.extend(check_snippet_chain())
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
    errors.extend(check_declared_skill_dirs())
    errors.extend(check_router())
    errors.extend(check_router_scenarios())
    errors.extend(check_ui_kit_copy_rules())
    errors.extend(check_ui_kit_skills())
    errors.extend(check_ui_kit_pin())
    errors.extend(check_ui_kit_registration())
    errors.extend(check_ui_corpus_disjointness())
    errors.extend(check_workspace_init_placeholder())
    errors.extend(check_agents_md_contract(warnings))
    errors.extend(check_consumer_onboarding())
    errors.extend(check_ui_router_scenarios())
    errors.extend(check_probe_runner())
    errors.extend(check_template_status())
    errors.extend(check_template_build(warnings))
    errors.extend(check_bundle())
    errors.extend(check_no_metaproject_paths())
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
