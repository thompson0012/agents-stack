#!/usr/bin/env python3
"""Validate a router skill package and its child inventory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_RELATIONSHIPS = {"routes_to", "includes"}
TOP_LEVEL_FIELDS = {"router_name", "purpose", "selection_order", "children"}
CHILD_FIELDS = {
    "name",
    "target",
    "relationship",
    "summary",
    "route_when",
    "avoid_when",
    "requires",
    "recommends",
    "fallbacks_to",
    "install_if_missing",
}
INSTALL_FIELDS = {"package", "notes"}


@dataclass
class Issue:
    level: str
    message: str


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a router skill package rooted at <router-dir>.",
    )
    parser.add_argument("router_dir", help="Path to the router skill directory.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"missing file: {path}") from exc


def extract_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter on line 1")

    end_marker = text.find("\n---\n", 4)
    if end_marker == -1:
        raise ValueError("SKILL.md must close YAML frontmatter with a second --- line")

    return text[4:end_marker], text[end_marker + 5 :]


def parse_frontmatter(block: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for raw_line in block.split("\n"):
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            raise ValueError(f"invalid frontmatter key in line: {raw_line}")
        if key in result:
            raise ValueError(f"duplicate frontmatter key: {key}")
        result[key] = value
    return result


def local_links(body: str) -> list[str]:
    targets: list[str] = []
    for raw_target in LINK_PATTERN.findall(body):
        target = raw_target.split("#", 1)[0].split("?", 1)[0].strip()
        if not target:
            continue
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        targets.append(target)
    return targets


def validate_skill(router_dir: Path) -> tuple[dict[str, str], str, list[Issue]]:
    issues: list[Issue] = []
    skill_text = read_text(router_dir / "SKILL.md")
    frontmatter_block, body = extract_frontmatter(skill_text)
    frontmatter = parse_frontmatter(frontmatter_block)

    missing = {"name", "description"} - set(frontmatter)
    for key in sorted(missing):
        issues.append(Issue("error", f"frontmatter is missing required field: {key}"))

    name = frontmatter.get("name", "")
    if name:
        if name != router_dir.name:
            issues.append(Issue("error", f"frontmatter name must match directory name: {router_dir.name}"))
        if not NAME_PATTERN.fullmatch(name):
            issues.append(Issue("error", "frontmatter name must use lowercase letters, numbers, and single hyphens only"))

    description = frontmatter.get("description", "")
    if description and not description.startswith("Use when "):
        issues.append(Issue("warning", "description should start with 'Use when '"))

    root = router_dir.resolve()
    for target in local_links(body):
        target_path = (router_dir / target).resolve()
        if not target_path.is_relative_to(root):
            issues.append(Issue("error", f"link escapes router directory: {target}"))
        elif not target_path.exists():
            issues.append(Issue("error", f"linked file does not exist: {target}"))

    return frontmatter, body, issues


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc.msg}") from exc


def validate_string_list(value: Any, label: str, required: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    if value is None:
        if required:
            issues.append(Issue("error", f"{label} is required"))
        return issues
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        issues.append(Issue("error", f"{label} must be an array of non-empty strings"))
        return issues
    if required and not value:
        issues.append(Issue("error", f"{label} must not be empty"))
    return issues


def validate_install_hint(value: Any, label: str) -> list[Issue]:
    issues: list[Issue] = []
    if value is None:
        return issues
    if not isinstance(value, dict):
        return [Issue("error", f"{label} must be an object when present")]

    extra = set(value) - INSTALL_FIELDS
    for key in sorted(extra):
        issues.append(Issue("warning", f"{label} uses non-standard field: {key}"))

    package = value.get("package")
    if not isinstance(package, str) or not package.strip():
        issues.append(Issue("error", f"{label}.package must be a non-empty string"))

    notes = value.get("notes")
    if notes is not None and (not isinstance(notes, str) or not notes.strip()):
        issues.append(Issue("error", f"{label}.notes must be a non-empty string when present"))

    return issues


def validate_children_metadata(router_dir: Path, frontmatter: dict[str, str]) -> list[Issue]:
    issues: list[Issue] = []
    metadata_path = router_dir / "references" / "children.json"
    data = read_json(metadata_path)

    if not isinstance(data, dict):
        return [Issue("error", "references/children.json must contain a JSON object")]

    extra_top_level = set(data) - TOP_LEVEL_FIELDS
    for key in sorted(extra_top_level):
        issues.append(Issue("warning", f"references/children.json uses non-standard top-level field: {key}"))

    router_name = data.get("router_name")
    if not isinstance(router_name, str) or not router_name.strip():
        issues.append(Issue("error", "references/children.json router_name must be a non-empty string"))
    elif frontmatter.get("name") and router_name != frontmatter["name"]:
        issues.append(Issue("error", f"references/children.json router_name must match frontmatter name: {frontmatter['name']}"))

    purpose = data.get("purpose")
    if not isinstance(purpose, str) or not purpose.strip():
        issues.append(Issue("error", "references/children.json purpose must be a non-empty string"))

    issues.extend(validate_string_list(data.get("selection_order"), "references/children.json selection_order", required=True))

    children = data.get("children")
    if not isinstance(children, list) or not children:
        issues.append(Issue("error", "references/children.json children must be a non-empty array"))
        return issues

    child_names: set[str] = set()
    pending_fallbacks: list[tuple[str, str]] = []

    for index, child in enumerate(children, start=1):
        label = f"references/children.json child #{index}"
        if not isinstance(child, dict):
            issues.append(Issue("error", f"{label} must be an object"))
            continue

        extra_child_fields = set(child) - CHILD_FIELDS
        for key in sorted(extra_child_fields):
            issues.append(Issue("warning", f"{label} uses non-standard field: {key}"))

        name = child.get("name")
        if not isinstance(name, str) or not name.strip():
            issues.append(Issue("error", f"{label} name must be a non-empty string"))
            child_name = None
        else:
            child_name = name.strip()
            if child_name in child_names:
                issues.append(Issue("error", f"references/children.json contains duplicate child name: {child_name}"))
            else:
                child_names.add(child_name)

        target = child.get("target")
        if not isinstance(target, str) or not target.strip():
            issues.append(Issue("error", f"{label} target must be a non-empty string"))

        relationship = child.get("relationship")
        if relationship is None:
            relationship = "routes_to"
        if not isinstance(relationship, str) or relationship not in ALLOWED_RELATIONSHIPS:
            issues.append(Issue("error", f"{label} relationship must be one of: {', '.join(sorted(ALLOWED_RELATIONSHIPS))}"))

        summary = child.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            issues.append(Issue("error", f"{label} summary must be a non-empty string"))

        issues.extend(validate_string_list(child.get("route_when"), f"{label} route_when", required=True))
        issues.extend(validate_string_list(child.get("avoid_when"), f"{label} avoid_when"))
        issues.extend(validate_string_list(child.get("requires"), f"{label} requires"))
        issues.extend(validate_string_list(child.get("recommends"), f"{label} recommends"))
        issues.extend(validate_string_list(child.get("fallbacks_to"), f"{label} fallbacks_to"))
        issues.extend(validate_install_hint(child.get("install_if_missing"), f"{label} install_if_missing"))

        if child_name:
            for relation_name in child.get("fallbacks_to", []) or []:
                pending_fallbacks.append((child_name, relation_name))
    for source, target in pending_fallbacks:
        if target not in child_names:
            issues.append(Issue("error", f"child '{source}' references unknown fallback target: {target}"))

    return issues


def main() -> int:
    args = parse_args()
    router_dir = Path(args.router_dir).expanduser().resolve()
    if not router_dir.exists():
        return fail(f"router directory does not exist: {router_dir}")
    if not router_dir.is_dir():
        return fail(f"router path is not a directory: {router_dir}")

    issues: list[Issue] = []
    try:
        frontmatter, _, skill_issues = validate_skill(router_dir)
        issues.extend(skill_issues)
        issues.extend(validate_children_metadata(router_dir, frontmatter))
    except (FileNotFoundError, ValueError) as exc:
        return fail(str(exc))

    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]

    for issue in issues:
        print(f"{issue.level}: {issue.message}")

    if errors:
        return 1
    if args.strict and warnings:
        return 1

    print(f"Validated router skill: {router_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
