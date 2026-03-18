#!/usr/bin/env python3
"""Package a reusable skill directory as a portable ZIP archive."""

from __future__ import annotations

import argparse
import fnmatch
import sys
import zipfile
from pathlib import Path

from validate import Issue, validate_skill

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", "node_modules", ".git", "dist", "runs", "benchmarks"}
EXCLUDE_FILES = {".DS_Store"}
EXCLUDE_GLOBS = {"*.pyc", "*.log"}


def fail(message: str) -> int:
    print(f"Error: {message}", file=sys.stderr)
    return 1


def should_exclude(rel_path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in rel_path.parts):
        return True
    if rel_path.name in EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(rel_path.name, pattern) for pattern in EXCLUDE_GLOBS)


def summarize_validation(issues: list[Issue], strict: bool) -> tuple[bool, list[Issue]]:
    blocking_levels = {"error"}
    if strict:
        blocking_levels.add("warning")
    blockers = [issue for issue in issues if issue.level in blocking_levels]
    return not blockers, blockers


def package_skill(skill_dir: Path, output_path: Path, strict: bool) -> tuple[Path | None, str]:
    issues = validate_skill(skill_dir)
    ok, blockers = summarize_validation(issues, strict)
    if not ok:
        lines = [f"{issue.level.upper()}: {issue.message}" for issue in blockers]
        return None, "\n".join(["Validation failed before packaging.", *lines])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path = output_path.resolve()
    root = skill_dir.parent.resolve()

    included = 0
    skipped = 0

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in skill_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.resolve() == output_path:
                skipped += 1
                continue
            rel_path = file_path.relative_to(root)
            if should_exclude(rel_path):
                skipped += 1
                continue
            archive.write(file_path, rel_path)
            included += 1

    warning_count = sum(issue.level == "warning" for issue in issues)
    message = (
        f"Packaged {skill_dir.name} to {output_path} "
        f"({included} file(s) included, {skipped} skipped, {warning_count} warning(s))."
    )
    return output_path, message


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package a skill directory into a portable ZIP archive.")
    parser.add_argument("skill_dir", help="Path to the skill directory.")
    parser.add_argument(
        "--output",
        default=None,
        help="Full output path for the archive (default: <skill-parent>/dist/<name>.zip).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat validation warnings as packaging failures.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_dir = Path(args.skill_dir).expanduser().resolve()

    if not skill_dir.exists():
        return fail(f"skill directory does not exist: {skill_dir}")
    if not skill_dir.is_dir():
        return fail(f"skill path is not a directory: {skill_dir}")

    output_path = Path(args.output).expanduser() if args.output else skill_dir.parent / "dist" / f"{skill_dir.name}.zip"

    try:
        archive_path, message = package_skill(skill_dir, output_path, args.strict)
    except OSError as exc:
        return fail(str(exc))
    except zipfile.BadZipFile as exc:
        return fail(f"could not create archive: {exc}")

    print(message)
    return 0 if archive_path else 1


if __name__ == "__main__":
    raise SystemExit(main())
