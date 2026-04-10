#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

FAILED_PHASES = {"build_failed", "review_failed"}
RUNNABLE_BACKLOG_STATUSES = {
    "in_progress",
    "proposed",
    "contracted",
    "executing",
    "awaiting_review",
    "in_review",
    "build_failed",
    "review_failed",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify whether a failed sprint may retry generator execution."
    )
    parser.add_argument("workstream_id", help="Sprint/workstream identifier to verify.")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing docs/live and .harness (default: current directory).",
    )
    return parser.parse_args()


def read_json(path: Path, missing_reason: str, invalid_reason: str) -> tuple[dict[str, Any] | None, list[str]]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, [missing_reason]

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None, [invalid_reason]

    if not isinstance(data, dict):
        return None, [invalid_reason]
    return data, []


def read_required_text(path: Path, missing_reason: str) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [missing_reason]
    return [] if text.strip() else [missing_reason]


def require_int(data: dict[str, Any], field: str, missing_reason: str, invalid_reason: str) -> tuple[int | None, list[str]]:
    if field not in data:
        return None, [missing_reason]
    value = data[field]
    if isinstance(value, bool) or not isinstance(value, int):
        return None, [invalid_reason]
    return value, []


def append_unique(reasons: list[str], additions: list[str]) -> None:
    for reason in additions:
        if reason not in reasons:
            reasons.append(reason)


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    workstream_id = args.workstream_id

    tracked_work_path = repo_root / "docs" / "live" / "tracked-work.json"
    sprint_dir = repo_root / ".harness" / workstream_id
    status_path = sprint_dir / "status.json"

    reasons: list[str] = []

    tracked_work, tracked_errors = read_json(
        tracked_work_path,
        "missing_tracked_work",
        "invalid_tracked_work_json",
    )
    append_unique(reasons, tracked_errors)

    status, status_errors = read_json(
        status_path,
        "missing_status_json",
        "invalid_status_json",
    )
    append_unique(reasons, status_errors)

    phase: str | None = None
    attempt_count: int | None = None
    max_attempts: int | None = None

    if status is not None:
        raw_phase = status.get("phase")
        if not isinstance(raw_phase, str) or not raw_phase.strip():
            reasons.append("missing_status_phase")
        else:
            phase = raw_phase.strip()
            if phase not in FAILED_PHASES:
                reasons.append("invalid_failed_phase")

        attempt_count, attempt_errors = require_int(
            status,
            "attempt_count",
            "missing_attempt_count",
            "invalid_attempt_count",
        )
        append_unique(reasons, attempt_errors)

        max_attempts, max_errors = require_int(
            status,
            "max_attempts",
            "missing_max_attempts",
            "invalid_max_attempts",
        )
        append_unique(reasons, max_errors)

        clean_restore_ref = status.get("clean_restore_ref")
        if not isinstance(clean_restore_ref, str) or not clean_restore_ref.strip():
            reasons.append("missing_clean_restore_ref")

    if tracked_work is not None:
        runnable_active_sprint_id = tracked_work.get("runnable_active_sprint_id")
        if not isinstance(runnable_active_sprint_id, str) or not runnable_active_sprint_id.strip():
            append_unique(reasons, ["single_runnable_invariant_not_satisfied"])
            runnable_active_sprint_id = None
        else:
            runnable_active_sprint_id = runnable_active_sprint_id.strip()
            if runnable_active_sprint_id != workstream_id:
                reasons.append("live_retry_target_mismatch")

        compound_pending = tracked_work.get("compound_pending_feature_ids")
        if not isinstance(compound_pending, list):
            reasons.append("missing_compound_pending_feature_ids")
        elif compound_pending:
            reasons.append("compound_queue_not_empty")

        backlog = tracked_work.get("backlog")
        backlog_entry: dict[str, Any] | None = None
        runnable_backlog_ids: list[str] = []
        if not isinstance(backlog, list):
            reasons.append("missing_backlog")
        else:
            for item in backlog:
                if not isinstance(item, dict):
                    continue
                item_id = item.get("id")
                if item_id == workstream_id:
                    backlog_entry = item
                status_value = item.get("status")
                if (
                    isinstance(item_id, str)
                    and isinstance(status_value, str)
                    and status_value in RUNNABLE_BACKLOG_STATUSES
                ):
                    runnable_backlog_ids.append(item_id)
            if backlog_entry is None:
                reasons.append("live_backlog_entry_missing")

        if runnable_active_sprint_id is not None:
            if len(runnable_backlog_ids) != 1 or runnable_backlog_ids[0] != runnable_active_sprint_id:
                append_unique(reasons, ["single_runnable_invariant_not_satisfied"])

        if backlog_entry is not None:
            live_phase = backlog_entry.get("status")
            if not isinstance(live_phase, str) or not live_phase.strip():
                reasons.append("missing_live_failed_phase")
            elif phase is not None and live_phase != phase:
                reasons.append("failed_phase_mismatch")

    if phase == "review_failed":
        append_unique(
            reasons,
            read_required_text(sprint_dir / "review.md", "missing_review_evidence"),
        )
    elif phase == "build_failed":
        append_unique(
            reasons,
            read_required_text(sprint_dir / "runtime.md", "missing_runtime_evidence"),
        )

    if attempt_count is not None and max_attempts is not None:
        if max_attempts <= 0:
            reasons.append("invalid_max_attempts")
        elif attempt_count >= max_attempts:
            reasons.append("attempt_budget_exhausted")

    verdict = "allow" if not reasons else "deny"
    print(json.dumps({"verdict": verdict, "reasons": reasons}))
    return 0 if verdict == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
