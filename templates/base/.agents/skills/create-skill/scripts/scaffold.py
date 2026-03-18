#!/usr/bin/env python3
"""Scaffold a portable skill directory with starter evaluation files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"
SKILL_TEMPLATE_PATH = ASSET_DIR / "skill-template.md"
EVALS_TEMPLATE_PATH = ASSET_DIR / "evals-template.json"
TRIGGER_TEMPLATE_PATH = ASSET_DIR / "trigger-evals-template.json"


def fail(message: str) -> int:
    print(f"Error: {message}", file=sys.stderr)
    return 1


def validate_name(name: str) -> str | None:
    if not name:
        return "skill name is required"
    if len(name) > 64:
        return "skill name must be 64 characters or fewer"
    if not NAME_PATTERN.fullmatch(name):
        return "skill name must use lowercase letters, numbers, and single hyphens only"
    return None


def load_template(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise RuntimeError(f"missing template: {path}") from exc
    except PermissionError as exc:
        raise RuntimeError(f"cannot read template: {path}") from exc


def display_title(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def render_template(template: str, name: str) -> str:
    replacements = {
        "__SKILL_NAME__": name,
        "__SKILL_TITLE__": display_title(name),
        "__TRIGGER__": "[trigger conditions and symptoms]",
        "__OVERVIEW__": "Describe the repeatable job this skill handles.",
    }

    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    return rendered


def ensure_empty_target(skill_dir: Path) -> None:
    if skill_dir.exists():
        if not skill_dir.is_dir():
            raise RuntimeError(f"target exists and is not a directory: {skill_dir}")
        if any(skill_dir.iterdir()):
            raise RuntimeError(f"target directory is not empty: {skill_dir}")
    else:
        skill_dir.mkdir(parents=True, exist_ok=False)


def write_file(path: Path, content: str, created: list[Path]) -> None:
    path.write_text(content, encoding="utf-8")
    created.append(path)


def build_structure(skill_dir: Path, skill_md: str, evals_json: str, trigger_json: str) -> list[Path]:
    created: list[Path] = []
    for subdir in ("references", "scripts", "assets", "evals"):
        path = skill_dir / subdir
        path.mkdir(exist_ok=True)
        created.append(path)

    write_file(skill_dir / "SKILL.md", skill_md, created)
    write_file(skill_dir / "evals" / "evals.json", evals_json, created)
    write_file(skill_dir / "evals" / "trigger-evals.json", trigger_json, created)
    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a portable skill directory with starter SKILL and eval files.",
    )
    parser.add_argument("name", help="Skill directory name and frontmatter name.")
    parser.add_argument(
        "--path",
        default=".",
        help="Parent directory that will contain the skill (default: current directory).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    name_error = validate_name(args.name)
    if name_error:
        return fail(name_error)

    parent = Path(args.path).expanduser().resolve()
    if not parent.exists():
        return fail(f"parent directory does not exist: {parent}")
    if not parent.is_dir():
        return fail(f"parent path is not a directory: {parent}")

    skill_dir = parent / args.name

    try:
        skill_template = load_template(SKILL_TEMPLATE_PATH)
        evals_template = load_template(EVALS_TEMPLATE_PATH)
        trigger_template = load_template(TRIGGER_TEMPLATE_PATH)
        ensure_empty_target(skill_dir)
        created = build_structure(
            skill_dir,
            render_template(skill_template, args.name),
            render_template(evals_template, args.name),
            render_template(trigger_template, args.name),
        )
    except (OSError, RuntimeError) as exc:
        return fail(str(exc))

    print(f"Created skill scaffold at: {skill_dir}")
    for path in created:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
