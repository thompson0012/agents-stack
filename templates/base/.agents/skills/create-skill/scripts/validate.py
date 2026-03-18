#!/usr/bin/env python3
"""Validate a portable skill package against conservative cross-runtime defaults."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {"name", "description"}
OPTIONAL_PORTABLE_FIELDS = {"license", "compatibility", "allowed-tools", "metadata"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TAG_PATTERN = re.compile(r"<[A-Za-z/!][^>]*>")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RECOMMENDED_MAX_BODY_LINES = 500
RECOMMENDED_MAX_DESCRIPTION_CHARS = 320


@dataclass
class Issue:
    level: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a skill package rooted at <skill-dir>.",
    )
    parser.add_argument("skill_dir", help="Path to the skill directory.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    return parser.parse_args()


def read_skill(skill_dir: Path) -> str:
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(f"missing SKILL.md in {skill_dir}")
    return skill_path.read_text(encoding="utf-8").replace("\r\n", "\n")


def extract_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter on line 1")

    end_marker = text.find("\n---\n", 4)
    if end_marker == -1:
        raise ValueError("SKILL.md must close YAML frontmatter with a second --- line")

    frontmatter = text[4:end_marker]
    body = text[end_marker + 5 :]
    return frontmatter, body


def parse_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'\"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(block: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    lines = block.split("\n")
    index = 0

    while index < len(lines):
        raw_line = lines[index]
        if not raw_line.strip():
            index += 1
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent != 0:
            raise ValueError(f"unexpected indentation in frontmatter: {raw_line}")
        if ":" not in raw_line:
            raise ValueError(f"invalid frontmatter line: {raw_line}")

        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()

        if not key:
            raise ValueError(f"invalid frontmatter key in line: {raw_line}")
        if key in result:
            raise ValueError(f"duplicate frontmatter key: {key}")

        if value in {">", "|"}:
            index += 1
            collected: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                if candidate.startswith((" ", "\t")) or not candidate.strip():
                    collected.append(candidate.lstrip())
                    index += 1
                    continue
                if candidate_indent == 0:
                    break
            result[key] = "\n".join(collected).strip()
            continue

        if value == "":
            index += 1
            nested: dict[str, str] = {}
            while index < len(lines):
                candidate = lines[index]
                if not candidate.strip():
                    index += 1
                    continue
                candidate_indent = len(candidate) - len(candidate.lstrip(" "))
                if candidate_indent == 0:
                    break
                if candidate_indent < 2:
                    raise ValueError(f"invalid nested indentation for {key}: {candidate}")
                nested_line = candidate[2:]
                if ":" not in nested_line:
                    raise ValueError(f"invalid nested frontmatter line: {candidate}")
                nested_key, nested_raw = nested_line.split(":", 1)
                nested_key = nested_key.strip()
                if not nested_key:
                    raise ValueError(f"invalid nested key in line: {candidate}")
                if nested_key in nested:
                    raise ValueError(f"duplicate nested key under {key}: {nested_key}")
                nested[nested_key] = parse_scalar(nested_raw)
                index += 1
            result[key] = nested
            continue

        result[key] = parse_scalar(value)
        index += 1

    return result


def local_link_targets(text: str) -> list[str]:
    targets: list[str] = []
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.split("#", 1)[0].split("?", 1)[0].strip()
        if not target:
            continue
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        targets.append(target)
    return targets


def validate_links(skill_dir: Path, body: str) -> list[Issue]:
    issues: list[Issue] = []
    skill_root = skill_dir.resolve()

    for target in local_link_targets(body):
        target_path = (skill_dir / target).resolve()
        if not str(target_path).startswith(str(skill_root)):
            issues.append(Issue("error", f"link escapes skill directory: {target}"))
            continue
        if not target_path.exists():
            issues.append(Issue("error", f"linked file does not exist: {target}"))
            continue

        parts = Path(target).parts
        if parts and parts[0] in {"references", "scripts", "assets"} and len(parts) > 2:
            issues.append(
                Issue(
                    "warning",
                    f"link goes deeper than one hop from SKILL.md: {target}",
                )
            )

    return issues


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path.name}: {exc.msg}") from exc


def validate_evals_file(path: Path, skill_name: str) -> list[Issue]:
    issues: list[Issue] = []
    try:
        data = read_json(path)
    except (FileNotFoundError, ValueError) as exc:
        return [Issue("error", str(exc))]

    if not isinstance(data, dict):
        return [Issue("error", f"{path.name} must contain a JSON object")]

    if data.get("skill_name") != skill_name:
        issues.append(Issue("error", f"{path.name} skill_name must match frontmatter name: {skill_name}"))

    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        issues.append(Issue("error", f"{path.name} must contain a non-empty evals array"))
        return issues

    seen_ids: set[str] = set()
    for index, entry in enumerate(evals, start=1):
        label = f"{path.name} eval #{index}"
        if not isinstance(entry, dict):
            issues.append(Issue("error", f"{label} must be an object"))
            continue

        entry_id = entry.get("id")
        prompt = entry.get("prompt")
        expected_output = entry.get("expected_output")
        files = entry.get("files", [])
        notes = entry.get("notes")

        if not isinstance(entry_id, str) or not entry_id.strip():
            issues.append(Issue("error", f"{label} id must be a non-empty string"))
        elif entry_id in seen_ids:
            issues.append(Issue("error", f"{path.name} contains duplicate eval id: {entry_id}"))
        else:
            seen_ids.add(entry_id)

        if not isinstance(prompt, str) or not prompt.strip():
            issues.append(Issue("error", f"{label} prompt must be a non-empty string"))
        if not isinstance(expected_output, str) or not expected_output.strip():
            issues.append(Issue("error", f"{label} expected_output must be a non-empty string"))
        if not isinstance(files, list) or any(not isinstance(item, str) or not item.strip() for item in files):
            issues.append(Issue("error", f"{label} files must be an array of non-empty strings"))
        if notes is not None and (not isinstance(notes, str) or not notes.strip()):
            issues.append(Issue("error", f"{label} notes must be a non-empty string when present"))

        extra_keys = set(entry) - {"id", "prompt", "expected_output", "files", "notes"}
        for extra_key in sorted(extra_keys):
            issues.append(Issue("warning", f"{label} uses non-standard field: {extra_key}"))

    return issues


def validate_trigger_evals_file(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    try:
        data = read_json(path)
    except (FileNotFoundError, ValueError) as exc:
        return [Issue("error", str(exc))]

    if not isinstance(data, list) or not data:
        return [Issue("error", f"{path.name} must contain a non-empty JSON array")]

    seen_ids: set[str] = set()
    for index, entry in enumerate(data, start=1):
        label = f"{path.name} entry #{index}"
        if not isinstance(entry, dict):
            issues.append(Issue("error", f"{label} must be an object"))
            continue

        entry_id = entry.get("id")
        query = entry.get("query")
        should_trigger = entry.get("should_trigger")
        why = entry.get("why")

        if not isinstance(entry_id, str) or not entry_id.strip():
            issues.append(Issue("error", f"{label} id must be a non-empty string"))
        elif entry_id in seen_ids:
            issues.append(Issue("error", f"{path.name} contains duplicate trigger id: {entry_id}"))
        else:
            seen_ids.add(entry_id)

        if not isinstance(query, str) or not query.strip():
            issues.append(Issue("error", f"{label} query must be a non-empty string"))
        if not isinstance(should_trigger, bool):
            issues.append(Issue("error", f"{label} should_trigger must be true or false"))
        if why is not None and (not isinstance(why, str) or not why.strip()):
            issues.append(Issue("error", f"{label} why must be a non-empty string when present"))

        extra_keys = set(entry) - {"id", "query", "should_trigger", "why"}
        for extra_key in sorted(extra_keys):
            issues.append(Issue("warning", f"{label} uses non-standard field: {extra_key}"))

    return issues


def validate_optional_eval_files(skill_dir: Path, skill_name: str) -> list[Issue]:
    issues: list[Issue] = []
    evals_dir = skill_dir / "evals"
    if not evals_dir.exists():
        return issues
    if not evals_dir.is_dir():
        return [Issue("error", "evals exists but is not a directory")]

    evals_path = evals_dir / "evals.json"
    trigger_path = evals_dir / "trigger-evals.json"

    if evals_path.exists():
        issues.extend(validate_evals_file(evals_path, skill_name))
    if trigger_path.exists():
        issues.extend(validate_trigger_evals_file(trigger_path))

    return issues


def validate_frontmatter(frontmatter: dict[str, Any], skill_dir_name: str) -> list[Issue]:
    issues: list[Issue] = []

    missing_fields = REQUIRED_FIELDS - set(frontmatter)
    for key in sorted(missing_fields):
        issues.append(Issue("error", f"missing frontmatter field: {key}"))

    unknown_fields = set(frontmatter) - REQUIRED_FIELDS - OPTIONAL_PORTABLE_FIELDS
    for key in sorted(unknown_fields):
        issues.append(Issue("warning", f"non-portable frontmatter field: {key}"))

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if name:
        if not isinstance(name, str):
            issues.append(Issue("error", "name must be a string"))
        else:
            if len(name) > 64:
                issues.append(Issue("error", "name must be 64 characters or fewer"))
            if not NAME_PATTERN.fullmatch(name):
                issues.append(
                    Issue(
                        "error",
                        "name must use lowercase letters, numbers, and single hyphens only",
                    )
                )
            if skill_dir_name != name:
                issues.append(
                    Issue(
                        "error",
                        f"name must match directory name exactly: expected {skill_dir_name}",
                    )
                )

    if description:
        if not isinstance(description, str):
            issues.append(Issue("error", "description must be a string"))
        else:
            if not description.startswith("Use when"):
                issues.append(Issue("error", "description must start with 'Use when'"))
            if TAG_PATTERN.search(description):
                issues.append(Issue("error", "description must not contain XML or HTML-like tags"))
            if len(description) > RECOMMENDED_MAX_DESCRIPTION_CHARS:
                issues.append(
                    Issue(
                        "warning",
                        f"description is long ({len(description)} chars); portability drops as discovery text grows",
                    )
                )

    for scalar_key in ("license", "compatibility", "allowed-tools"):
        if scalar_key in frontmatter and not isinstance(frontmatter[scalar_key], str):
            issues.append(Issue("error", f"{scalar_key} must be a string when present"))

    if "metadata" in frontmatter and not isinstance(frontmatter["metadata"], dict):
        issues.append(Issue("error", "metadata must be a nested mapping when present"))

    return issues


def validate_skill(skill_dir: Path) -> list[Issue]:
    issues: list[Issue] = []

    try:
        text = read_skill(skill_dir)
        frontmatter_block, body = extract_frontmatter(text)
        frontmatter = parse_frontmatter(frontmatter_block)
    except (FileNotFoundError, OSError, ValueError) as exc:
        return [Issue("error", str(exc))]

    issues.extend(validate_frontmatter(frontmatter, skill_dir.name))

    if not body.strip():
        issues.append(Issue("error", "SKILL.md body must not be empty"))
    else:
        body_lines = body.rstrip("\n").count("\n") + 1
        if body_lines > RECOMMENDED_MAX_BODY_LINES:
            issues.append(
                Issue(
                    "warning",
                    f"SKILL.md body has {body_lines} lines; consider moving detail into references/",
                )
            )
        if "##" not in body:
            issues.append(Issue("warning", "SKILL.md body has no secondary headings"))

    issues.extend(validate_links(skill_dir, body))

    name = frontmatter.get("name")
    if isinstance(name, str) and name:
        issues.extend(validate_optional_eval_files(skill_dir, name))

    return issues


def report(issues: list[Issue]) -> int:
    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]

    if not issues:
        print("Validation passed with no issues.")
        return 0

    for issue in errors + warnings:
        print(f"{issue.level.upper()}: {issue.message}")

    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s)")
    return len(errors)


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir).expanduser().resolve()

    if not skill_dir.exists():
        print(f"Error: skill directory does not exist: {skill_dir}", file=sys.stderr)
        return 1
    if not skill_dir.is_dir():
        print(f"Error: skill path is not a directory: {skill_dir}", file=sys.stderr)
        return 1

    issues = validate_skill(skill_dir)
    error_count = report(issues)

    if error_count:
        return 1
    if args.strict and any(issue.level == "warning" for issue in issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
