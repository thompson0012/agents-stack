#!/usr/bin/env python3
"""Validate the live control-plane files under a repo root."""

from __future__ import annotations

import argparse

from live_control import ControlPlaneError, live_paths, load_json, resolve_repo_root, validate_control_files, validate_tracked_work


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate docs/live control-plane state and fail closed on malformed starter or overlay state."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing docs/live/*. Defaults to the current working directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    paths = live_paths(repo_root)
    errors: list[str] = []

    try:
        tracked_work = load_json(paths.tracked_work)
    except ControlPlaneError as exc:
        errors.append(str(exc))
    else:
        errors.extend(validate_tracked_work(tracked_work))

    errors.extend(validate_control_files(paths))

    if errors:
        print(f"Live control validation failed for {repo_root}:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Live control validation passed for {repo_root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
