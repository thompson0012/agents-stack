#!/usr/bin/env python3
"""Apply narrow structured mutations to docs/live/roadmap.md."""

from __future__ import annotations

import argparse
import json
from typing import Any

from live_control import (
    ControlPlaneError,
    RoadmapState,
    live_paths,
    load_optional_text,
    parse_progress_event_text,
    parse_roadmap_text,
    render_roadmap,
    resolve_repo_root,
    write_text,
)

ALLOWED_OPS = {
    "set_source_goal",
    "set_current_slice",
    "set_remaining_slices",
    "set_stop_condition",
    "set_summary",
    "append_progress_event",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply structured roadmap mutations without arbitrary Markdown edits."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing docs/live/*. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--ops-json",
        help="Inline JSON payload describing allowed ops. Accepts an object or an array of {op, value} entries.",
    )
    parser.add_argument(
        "--ops-file",
        help="Path to a JSON payload file. Useful when the payload is multiline.",
    )
    parser.add_argument("--set-source-goal", help="Set the roadmap Source goal field.")
    parser.add_argument("--set-current-slice", help="Set the roadmap Current slice field.")
    parser.add_argument(
        "--set-remaining-slices",
        nargs="+",
        metavar="SLICE",
        help="Replace the ordered remaining slices/stages list.",
    )
    parser.add_argument("--set-stop-condition", help="Set the Stop or re-authorization condition field.")
    parser.add_argument("--set-summary", help="Set the Visible remaining-work summary field.")
    parser.add_argument(
        "--append-progress-event",
        help="Append a literal progress entry block to docs/live/progress.md.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and render the updated roadmap without writing files.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the resulting roadmap Markdown after applying ops.",
    )
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> list[dict[str, Any]]:
    sources_used = sum(
        1
        for candidate in (
            args.ops_json,
            args.ops_file,
            args.set_source_goal,
            args.set_current_slice,
            args.set_remaining_slices,
            args.set_stop_condition,
            args.set_summary,
            args.append_progress_event,
        )
        if candidate is not None
    )
    if sources_used == 0:
        raise ControlPlaneError("no roadmap ops supplied")

    ops: list[dict[str, Any]] = []
    if args.ops_json is not None and args.ops_file is not None:
        raise ControlPlaneError("choose either --ops-json or --ops-file, not both")
    if args.ops_json is not None:
        ops.extend(normalize_payload(json.loads(args.ops_json)))
    if args.ops_file is not None:
        with open(args.ops_file, "r", encoding="utf-8") as handle:
            ops.extend(normalize_payload(json.load(handle)))
    if args.set_source_goal is not None:
        ops.append({"op": "set_source_goal", "value": args.set_source_goal})
    if args.set_current_slice is not None:
        ops.append({"op": "set_current_slice", "value": args.set_current_slice})
    if args.set_remaining_slices is not None:
        ops.append({"op": "set_remaining_slices", "value": args.set_remaining_slices})
    if args.set_stop_condition is not None:
        ops.append({"op": "set_stop_condition", "value": args.set_stop_condition})
    if args.set_summary is not None:
        ops.append({"op": "set_summary", "value": args.set_summary})
    if args.append_progress_event is not None:
        ops.append({"op": "append_progress_event", "value": args.append_progress_event})
    return ops


def normalize_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        if "ops" in payload:
            return normalize_payload(payload["ops"])
        ops: list[dict[str, Any]] = []
        field_to_op = {
            "source_goal": "set_source_goal",
            "current_slice": "set_current_slice",
            "remaining_slices": "set_remaining_slices",
            "stop_condition": "set_stop_condition",
            "summary": "set_summary",
            "progress_event": "append_progress_event",
        }
        for field, op_name in field_to_op.items():
            if field in payload:
                ops.append({"op": op_name, "value": payload[field]})
        if not ops:
            raise ControlPlaneError("JSON object payload did not contain any supported roadmap fields")
        return ops
    if not isinstance(payload, list):
        raise ControlPlaneError("JSON payload must be an object or an array of ops")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise ControlPlaneError(f"ops[{index}] must be an object")
        op = item.get("op")
        if op not in ALLOWED_OPS:
            raise ControlPlaneError(f"ops[{index}] uses unsupported op {op!r}")
        normalized.append({"op": op, "value": item.get("value")})
    return normalized


def load_existing_state(paths) -> RoadmapState:
    roadmap_text = load_optional_text(paths.roadmap)
    if roadmap_text is None:
        raise ControlPlaneError(f"missing roadmap file: {paths.roadmap}")
    return parse_roadmap_text(roadmap_text)


def apply_ops(state: RoadmapState, ops: list[dict[str, Any]]) -> tuple[RoadmapState, str | None]:
    source_goal = state.source_goal
    current_slice = state.current_slice
    remaining_slices = list(state.remaining_slices)
    stop_condition = state.stop_condition
    summary = state.summary
    progress_event: str | None = None

    for entry in ops:
        op = entry["op"]
        value = entry.get("value")
        if op == "set_source_goal":
            source_goal = require_non_empty_string(op, value)
        elif op == "set_current_slice":
            current_slice = require_non_empty_string(op, value)
        elif op == "set_remaining_slices":
            remaining_slices = require_string_list(op, value)
        elif op == "set_stop_condition":
            stop_condition = require_non_empty_string(op, value)
        elif op == "set_summary":
            summary = require_non_empty_string(op, value)
        elif op == "append_progress_event":
            progress_event = parse_progress_event_text(require_non_empty_string(op, value))
        else:
            raise ControlPlaneError(f"unsupported op {op!r}")

    return (
        RoadmapState(
            source_goal=source_goal,
            current_slice=current_slice,
            remaining_slices=remaining_slices,
            stop_condition=stop_condition,
            summary=summary,
        ),
        progress_event,
    )


def require_non_empty_string(op: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ControlPlaneError(f"{op} requires a non-empty string value")
    return value.strip()


def require_string_list(op: str, value: Any) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ControlPlaneError(f"{op} requires a non-empty list of strings")
    normalized = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ControlPlaneError(f"{op} requires a non-empty list of strings")
        normalized.append(item.strip())
    return normalized


def append_progress(paths, event: str) -> None:
    existing = load_optional_text(paths.progress)
    if existing is None:
        raise ControlPlaneError(f"missing progress ledger: {paths.progress}")
    content = existing
    if not content.endswith("\n"):
        content += "\n"
    if content and not content.endswith("\n\n"):
        content += "\n"
    content += event
    write_text(paths.progress, content)


def main() -> int:
    args = parse_args()
    try:
        ops = load_payload(args)
        repo_root = resolve_repo_root(args.repo_root)
        paths = live_paths(repo_root)
        updated_state, progress_event = apply_ops(load_existing_state(paths), ops)
        rendered = render_roadmap(updated_state)
        if not args.dry_run:
            write_text(paths.roadmap, rendered)
            if progress_event is not None:
                append_progress(paths, progress_event)
        if args.stdout:
            print(rendered, end="")
    except ControlPlaneError as exc:
        print(f"Roadmap ops failed: {exc}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"Roadmap ops failed: invalid JSON payload: {exc}")
        return 1

    if args.dry_run:
        print(f"Validated roadmap ops against {paths.roadmap}.")
    else:
        print(f"Updated roadmap at {paths.roadmap}.")
        if progress_event is not None:
            print(f"Appended progress event to {paths.progress}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
