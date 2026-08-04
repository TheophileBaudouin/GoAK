#!/usr/bin/env python3
"""Build or verify the KitV2 semantic router index (generated artifact).

Metaproject-only tool. The index is a ROUTING artifact: it maps a task
description to kit resources (id, kind, path, description, tags, terms).
It never contains file contents — the source of truth stays the kit files.

Deterministic: index.json is a pure function of the KitV2 tree (sorted by id,
no timestamps). meta.json carries provenance (build date, sha256, counts,
stopwords — the stopwords are the single source shared with the runtime).

Usage:
  python3 .agent/router/build_index.py            # write KitV2/router/{index,meta}.json
  python3 .agent/router/build_index.py --check    # exit 0 if up to date, 1 on drift
  python3 .agent/router/build_index.py --out DIR  # write into an arbitrary dir (tests)

Dependency: PyYAML (already required by the existing validators).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]  # metaproject root
KIT = ROOT / "KitV2"

TOKEN_RE = re.compile(r"[a-z0-9]+")

# Small bilingual stopword list (data, not logic): both the builder and the
# runtime use the copy shipped in meta.json so they cannot drift apart.
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "can",
    "does",
    "for",
    "from",
    "has",
    "have",
    "how",
    "in",
    "into",
    "is",
    "it",
    "its",
    "not",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "use",
    "using",
    "when",
    "where",
    "which",
    "while",
    "with",
    "you",
    "your",
    "un",
    "une",
    "des",
    "les",
    "la",
    "le",
    "et",
    "de",
    "du",
    "que",
    "qui",
    "est",
    "pas",
    "pour",
    "dans",
    "sur",
    "ce",
    "cette",
    "dun",
    "au",
    "aux",
    "en",
    "par",
    "son",
    "ses",
    "avec",
}

MAX_DETAIL = 400  # truncate knowledge YAML details to keep the index compact

# YAML detail fields, in priority order, per knowledge zone.
DETAIL_FIELDS = (
    "description",
    "problem",
    "symptom",
    "purpose",
    "summary",
    "selection",
    "context",
    "when_to_use",
)


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    """Lowercase, split on non-alphanumerics, drop stopwords and 1-char tokens."""
    return [
        token
        for token in TOKEN_RE.findall(text.lower())
        if len(token) >= 2 and token not in stopwords
    ]


def collapse(text: str) -> str:
    """Collapse whitespace/newlines in multi-line YAML scalars."""
    return " ".join(text.split())


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: malformed frontmatter")
    values = yaml.safe_load(parts[1])
    return values if isinstance(values, dict) else {}


def load_yaml(path: Path) -> dict:
    try:
        values = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise ValueError(f"{path}: invalid YAML: {error}") from error
    return values if isinstance(values, dict) else {}


def description_from_yaml(artifact: dict) -> str:
    title = str(artifact.get("title", "")).strip()
    detail = ""
    for field in DETAIL_FIELDS:
        value = artifact.get(field)
        if value:
            detail = collapse(str(value))[:MAX_DETAIL]
            break
    return (title + "\n" + detail).strip() if detail else title


def resource_id(path: Path, zone: str, values: dict) -> str:
    candidate = values.get("name") or values.get("id")
    if candidate:
        return str(candidate).strip()
    if zone == "prompt":
        return path.stem
    return path.parent.name if zone == "snippet" else path.stem


def kind_for(path: Path, zone: str, kit: Path) -> str:
    if zone != "knowledge":
        return zone  # rule, recipe, catalog, snippet, prompt, skill
    rel = path.relative_to(kit / "knowledge")
    if rel.parts[0] == "patterns":
        return "pattern"
    if rel.parts[0] == "anti-patterns":
        return "anti-pattern"
    if rel.parts[0] == "catalogs":
        return "catalog"
    return "source"  # architecture, debugging, performance, security, stdlib


def collect_resources(kit: Path, stopwords: set[str]) -> list[dict]:
    resources: list[dict] = []

    def add(zone: str, path: Path, description: str, values: dict) -> None:
        rid = resource_id(path, zone, values)
        tags = values.get("tags") or []
        if not isinstance(tags, list):
            tags = [str(tags)]
        tags = [str(t) for t in tags]
        terms = tokenize(f"{rid} {description} {' '.join(tags)}", stopwords)
        resources.append(
            {
                "id": rid,
                "kind": kind_for(path, zone, kit),
                "path": str(path.relative_to(kit)),
                "description": description,
                "tags": tags,
                "terms": terms,
            }
        )

    for path in sorted((kit / "rules").rglob("SKILL.md")):
        values = frontmatter(path)
        add("rule", path, values.get("description", ""), values)
    for path in sorted((kit / "recipes").rglob("SKILL.md")):
        values = frontmatter(path)
        add("recipe", path, values.get("description", ""), values)
    for path in sorted((kit / "knowledge" / "catalogs").rglob("SKILL.md")):
        values = frontmatter(path)
        add("catalog", path, values.get("description", ""), values)
    for path in sorted((kit / "knowledge").rglob("*.yaml")):
        values = load_yaml(path)
        add("knowledge", path, description_from_yaml(values), values)
    for path in sorted((kit / "snippets").glob("*/SNIPPET.yaml")):
        values = load_yaml(path)
        add("snippet", path, str(values.get("purpose", "")), values)
    for path in sorted((kit / "templates").glob("*/template.yaml")):
        values = load_yaml(path)
        name = str(values.get("name", path.parent.name))
        purpose = str(values.get("purpose", "")).strip()
        description = f"{name} — {purpose}" if purpose else name
        add("template", path, description, values)
    for path in sorted((kit / ".pi" / "prompts").glob("*.md")):
        values = frontmatter(path)
        add("prompt", path, values.get("description", ""), values)
    for path in sorted((kit / ".pi" / "skills").rglob("SKILL.md")):
        values = frontmatter(path)
        add("skill", path, values.get("description", ""), values)

    resources.sort(key=lambda r: r["id"])
    return resources


def counts(resources: list[dict]) -> dict[str, int]:
    result: dict[str, int] = {}
    for resource in resources:
        result[resource["kind"]] = result.get(resource["kind"], 0) + 1
    return result


def compute(kit: Path, stopwords: set[str]) -> tuple[dict, str]:
    """Pure computation: the index dict plus its canonical JSON string."""
    resources = collect_resources(kit, stopwords)
    index = {
        "schema": 1,
        "resources": resources,
    }
    return index, json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True)


def build(kit: Path, out: Path, version: str) -> dict:
    _, index_bytes = compute(kit, STOPWORDS)
    index_file = index_bytes + "\n"
    meta = {
        "schema": 1,
        "version": version,
        "index_sha256": hashlib.sha256(index_file.encode("utf-8")).hexdigest(),
        "counts": counts(collect_resources(kit, STOPWORDS)),
        "stopwords": sorted(STOPWORDS),
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.json").write_text(index_file, encoding="utf-8")
    (out / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return meta


def manifest_version() -> str:
    values = load_yaml(KIT / "manifest.yaml")
    return str(values.get("version", "unknown"))


def check(kit: Path, out: Path, version: str | None = None) -> tuple[bool, list[str]]:
    problems: list[str] = []
    index_path = out / "index.json"
    meta_path = out / "meta.json"
    if not index_path.exists() or not meta_path.exists():
        return False, [
            f"{index_path.name} or {meta_path.name}: missing — run the builder"
        ]
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False, ["meta.json: invalid JSON — run the builder"]
    _, index_bytes = compute(kit, STOPWORDS)
    expected = hashlib.sha256((index_bytes + "\n").encode("utf-8")).hexdigest()
    if meta.get("index_sha256") != expected:
        problems.append("index.json: content drift — run the builder")
    if meta.get("counts") != counts(collect_resources(kit, STOPWORDS)):
        problems.append("index.json: resource drift (added/removed/changed)")
    if meta.get("stopwords") != sorted(STOPWORDS):
        problems.append("meta.json: stopwords drift — run the builder")
    return not problems, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify, do not write")
    parser.add_argument("--out", type=Path, default=KIT / "router")
    parser.add_argument("--kit", type=Path, default=KIT)
    parser.add_argument("--version", default=None)
    args = parser.parse_args(argv)

    version = args.version or manifest_version()
    if args.check:
        ok, problems = check(args.kit, args.out)
        if ok:
            print(f"router index: up to date ({args.out})")
            return 0
        for problem in problems:
            print(f"router index: {problem}", file=sys.stderr)
        return 1

    meta = build(args.kit, args.out, version)
    total = sum(meta["counts"].values())
    print(
        f"router index: written {args.out} "
        f"({total} resources, {len(meta['counts'])} kinds, "
        f"sha256 {meta['index_sha256'][:12]}…)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
