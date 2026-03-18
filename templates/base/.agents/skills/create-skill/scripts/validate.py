#!/usr/bin/env python3
"""Validate a portable skill package against conservative cross-runtime defaults."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ALLOWED_FIELDS = {"name", "description"}
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


def parse_frontmatter(block: str) -> dict[str, str]:
    result: dict[str, str] = {}
    lines = block.split("\n")
    index = 0

    while index < len(lines):
        raw_line = lines[index]
        if not raw_line.strip():
            index += 1
            continue

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
                if candidate.startswith((" ", "\t")):
                    collected.append(candidate.lstrip())
                    index += 1
                    continue
                if not candidate.strip():
                    collected.append("")
                    index += 1
                    continue
                break
            result[key] = "\n".join(collected).strip()
            continue

        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'\"', "'"}:
            value = value[1:-1]
        result[key] = value
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


def validate_skill(skill_dir: Path) -> list[Issue]:
    issues: list[Issue] = []

    try:
        text = read_skill(skill_dir)
        frontmatter_block, body = extract_frontmatter(text)
        frontmatter = parse_frontmatter(frontmatter_block)
    except (FileNotFoundError, OSError, ValueError) as exc:
        return [Issue("error", str(exc))]

    extra_fields = set(frontmatter) - ALLOWED_FIELDS
    missing_fields = ALLOWED_FIELDS - set(frontmatter)

    for key in sorted(extra_fields):
        issues.append(Issue("error", f"unsupported frontmatter field: {key}"))
    for key in sorted(missing_fields):
        issues.append(Issue("error", f"missing frontmatter field: {key}"))

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if name:
        if len(name) > 64:
            issues.append(Issue("error", "name must be 64 characters or fewer"))
        if not NAME_PATTERN.fullmatch(name):
            issues.append(
                Issue(
                    "error",
                    "name must use lowercase letters, numbers, and single hyphens only",
                )
            )
        if skill_dir.name != name:
            issues.append(
                Issue(
                    "error",
                    f"name must match directory name exactly: expected {skill_dir.name}",
                )
            )

    if description:
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
