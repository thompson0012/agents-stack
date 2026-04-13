#!/usr/bin/env python3
"""Check that init.sh bootstrap seeds still match committed starter files."""

from __future__ import annotations

import argparse

from live_control import ControlPlaneError, compare_bootstrap_alignment, live_paths, load_text, resolve_repo_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare docs/scripts/init.sh bootstrap seeds against committed files under the same repo root."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing docs/scripts/init.sh and docs/live/*. Defaults to the current working directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    paths = live_paths(repo_root)

    try:
        load_text(paths.init_script)
    except ControlPlaneError as exc:
        print(f"Bootstrap alignment validation failed: {exc}")
        return 1

    drifts = compare_bootstrap_alignment(repo_root)
    if drifts:
        print(f"Bootstrap alignment drift detected for {repo_root}:")
        for drift in drifts:
            print(f"\n== {drift.relative_path} ==")
            print(drift.diff or "files differ")
        return 1

    print(f"Bootstrap alignment validation passed for {repo_root}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
