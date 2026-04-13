#!/usr/bin/env python3
"""Render the canonical current-focus resume anchor."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from live_control import CurrentFocusState, ControlPlaneError, live_paths, render_current_focus, resolve_repo_root, write_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render docs/live/current-focus.md in the fixed canonical resume-anchor format."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing docs/live/current-focus.md. Defaults to the current working directory.",
    )
    parser.add_argument("--current-objective", help="Current objective line.")
    parser.add_argument("--source-goal-lineage", help="Source-goal lineage line.")
    parser.add_argument("--current-roadmap-stage", help="Current roadmap stage line.")
    parser.add_argument("--next-owner", help="Next owner line.")
    parser.add_argument("--next-file-to-open", help="Next file to open line.")
    parser.add_argument(
        "--json",
        help="Inline JSON object with current_objective, source_goal_lineage, current_roadmap_stage, next_owner, and next_file_to_open.",
    )
    parser.add_argument(
        "--json-file",
        help="Path to a JSON object file with current_objective, source_goal_lineage, current_roadmap_stage, next_owner, and next_file_to_open.",
    )
    parser.add_argument(
        "--output",
        help="Optional write target. Defaults to docs/live/current-focus.md under --repo-root.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the rendered anchor to stdout.",
    )
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if args.json is not None and args.json_file is not None:
        raise ControlPlaneError("choose either --json or --json-file, not both")
    if args.json is not None:
        payload.update(json.loads(args.json))
    if args.json_file is not None:
        with open(args.json_file, "r", encoding="utf-8") as handle:
            payload.update(json.load(handle))
    cli_fields = {
        "current_objective": args.current_objective,
        "source_goal_lineage": args.source_goal_lineage,
        "current_roadmap_stage": args.current_roadmap_stage,
        "next_owner": args.next_owner,
        "next_file_to_open": args.next_file_to_open,
    }
    for key, value in cli_fields.items():
        if value is not None:
            payload[key] = value
    return payload


def normalize_state(payload: dict[str, Any]) -> CurrentFocusState:
    required = (
        "current_objective",
        "source_goal_lineage",
        "current_roadmap_stage",
        "next_owner",
        "next_file_to_open",
    )
    missing = [key for key in required if not isinstance(payload.get(key), str) or not str(payload[key]).strip()]
    if missing:
        raise ControlPlaneError("missing required current-focus fields: " + ", ".join(missing))
    return CurrentFocusState(
        current_objective=str(payload["current_objective"]).strip(),
        source_goal_lineage=str(payload["source_goal_lineage"]).strip(),
        current_roadmap_stage=str(payload["current_roadmap_stage"]).strip(),
        next_owner=str(payload["next_owner"]).strip(),
        next_file_to_open=str(payload["next_file_to_open"]).strip(),
    )


def resolve_output_path(repo_root: Path, raw_output: str) -> Path:
    candidate = Path(raw_output).expanduser()
    return candidate.resolve() if candidate.is_absolute() else (repo_root / candidate).resolve()


def main() -> int:
    args = parse_args()
    try:
        payload = load_payload(args)
        state = normalize_state(payload)
        repo_root = resolve_repo_root(args.repo_root)
        default_paths = live_paths(repo_root)
        output_path = default_paths.current_focus if args.output is None else resolve_output_path(repo_root, args.output)
        rendered = render_current_focus(state)
        if args.output is not None or not args.stdout:
            write_text(output_path, rendered)
        if args.stdout:
            print(rendered, end="")
    except ControlPlaneError as exc:
        print(f"Current-focus render failed: {exc}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"Current-focus render failed: invalid JSON payload: {exc}")
        return 1

    if args.output is not None or not args.stdout:
        print(f"Wrote canonical current focus to {output_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
