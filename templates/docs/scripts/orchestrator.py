#!/usr/bin/env python3
"""Reference harness orchestrator helper for starter repositories.

The helper scans `.harness/*/status.json`, enforces the single-active-sprint
rule, and records resume metadata that a top-level orchestrator can use to
dispatch a fresh worker. It does not perform child phase work inline, and the
state files remain the source of truth.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT_SECONDS = 15 * 60
TERMINAL_PHASES = {"archived", "completed", "cancelled"}
STALE_PHASES = {"in_progress", "in_review"}
ARTIFACT_FILES = (
    "sprint_proposal.md",
    "contract.md",
    "handoff.md",
    "review.md",
    "runtime.md",
    "qa.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect harness sprint status files and prepare fresh-worker dispatch for stale work."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root that contains the .harness directory.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Maximum age for an active heartbeat before the orchestrator records a fresh-worker resume checkpoint.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the worker dispatch plan without rewriting status files."
    )
    return parser.parse_args()


def load_statuses(harness_root: Path) -> list[dict[str, Any]]:
    statuses: list[dict[str, Any]] = []
    for status_path in sorted(harness_root.glob("*/status.json")):
        with status_path.open("r", encoding="utf-8") as handle:
            status = json.load(handle)
        statuses.append(
            {
                "path": status_path,
                "sprint_dir": status_path.parent,
                "status": status,
            }
        )
    return statuses


def is_active(status: dict[str, Any]) -> bool:
    phase = str(status.get("phase", "unknown"))
    return phase not in TERMINAL_PHASES


def find_active_sprints(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [entry for entry in entries if is_active(entry["status"])]


def describe_sprint(entry: dict[str, Any]) -> str:
    status = entry["status"]
    sprint_id = status.get("sprint_id", entry["sprint_dir"].name)
    phase = status.get("phase", "unknown")
    return f"{sprint_id} ({phase}) at {entry['path']}"


def artifact_snapshot(sprint_dir: Path) -> dict[str, bool]:
    return {name: (sprint_dir / name).exists() for name in ARTIFACT_FILES}


def infer_resume_target(
    previous_phase: str,
    status: dict[str, Any],
    sprint_dir: Path,
) -> tuple[str, str, str]:
    """Return the artifact and worker phase the orchestrator should dispatch next."""
    review_path = sprint_dir / "review.md"
    handoff_path = sprint_dir / "handoff.md"
    contract_path = sprint_dir / "contract.md"
    proposal_path = sprint_dir / "sprint_proposal.md"

    if previous_phase == "in_review":
        resume_from = "handoff.md" if handoff_path.exists() else "contract.md"
        return (
            resume_from,
            "adversarial_live_review",
            "Dispatch a fresh adversarial-live-review worker. It must read the generator handoff, verify the workspace matches it, then rerun the review.",
        )

    if review_path.exists() and status.get("review_status") == "fail":
        return (
            "review.md",
            "generator_execution",
            "Dispatch a fresh generator-execution worker. It must read review.md, apply the failing directives within the contract boundary, then refresh handoff.md for another review pass.",
        )

    if handoff_path.exists():
        return (
            "handoff.md",
            "adversarial_live_review",
            "Dispatch a fresh adversarial-live-review worker. It must read handoff.md, confirm the checkpoint against the repo, then continue the pending review.",
        )

    if contract_path.exists():
        return (
            "contract.md",
            "generator_execution",
            "Dispatch a fresh generator-execution worker. It must read contract.md, confirm the allowed files, and resume implementation from the last verified checkpoint.",
        )

    if proposal_path.exists():
        return (
            "sprint_proposal.md",
            "evaluator_contract_review",
            "Dispatch a fresh evaluator-contract-review worker. It must read sprint_proposal.md and decide whether the sprint should be approved, revised, or cancelled.",
        )

    fallback = status.get("resume_from") or "status.json"
    return (
        str(fallback),
        "generator_proposal",
        "Dispatch a fresh generator-proposal worker. It must reconstruct the sprint intent from the remaining state files before resuming work.",
    )


def recover_stale_sprint(
    entry: dict[str, Any],
    now: int,
    timeout_seconds: int,
    dry_run: bool,
) -> dict[str, Any]:
    """Record the next fresh-worker dispatch plan for a stale active sprint."""
    status = dict(entry["status"])
    previous_phase = str(status.get("phase", "unknown"))
    last_updated_at = int(status.get("last_updated_at", 0) or 0)
    stale_for_seconds = max(0, now - last_updated_at)
    resume_from, resume_phase, next_checkpoint = infer_resume_target(
        previous_phase, status, entry["sprint_dir"]
    )
    previous_active_pids = list(status.get("active_pids", []))

    recovered_status = dict(status)
    recovered_status.update(
        {
            "phase": "paused_by_timeout",
            "owner_role": "orchestrator",
            "last_updated_at": now,
            "resume_from": resume_from,
            "resume_phase": resume_phase,
            "next_checkpoint": next_checkpoint,
            "active_pids": [],
            "worker_subject": f"Resume {status.get('sprint_id', entry['sprint_dir'].name)} via {resume_phase}",
            "tool_scope_profile": f"{resume_phase}_scoped",
            "spawn_depth": 1,
            "parent_worker_id": "orchestrator",
            "timeout_recovery": {
                "recovered_at": now,
                "timeout_seconds": timeout_seconds,
                "stale_for_seconds": stale_for_seconds,
                "previous_phase": previous_phase,
                "previous_owner_role": status.get("owner_role"),
                "previous_resume_from": status.get("resume_from"),
                "previous_resume_phase": status.get("resume_phase"),
                "previous_next_checkpoint": status.get("next_checkpoint"),
                "previous_active_pids": previous_active_pids,
                "artifact_snapshot": artifact_snapshot(entry["sprint_dir"]),
            },
        }
    )

    if not dry_run:
        with entry["path"].open("w", encoding="utf-8") as handle:
            json.dump(recovered_status, handle, indent=2)
            handle.write("\n")

    return {
        "sprint_id": recovered_status.get("sprint_id", entry["sprint_dir"].name),
        "path": str(entry["path"]),
        "stale_for_seconds": stale_for_seconds,
        "resume_from": resume_from,
        "resume_phase": resume_phase,
        "next_checkpoint": next_checkpoint,
        "dry_run": dry_run,
    }


def main() -> int:
    args = parse_args()
    repo_root = Path(args.root).resolve()
    harness_root = repo_root / ".harness"

    if not harness_root.exists():
        print(f"No harness directory found at {harness_root}.")
        return 0

    entries = load_statuses(harness_root)
    if not entries:
        print(f"No sprint status files found under {harness_root}.")
        return 0

    active_entries = find_active_sprints(entries)
    if len(active_entries) > 1:
        print("ERROR: expected at most one active sprint, but found:")
        for entry in active_entries:
            print(f"- {describe_sprint(entry)}")
        return 2

    if not active_entries:
        print("No active sprint found.")
        return 0

    active_entry = active_entries[0]
    status = active_entry["status"]
    sprint_id = status.get("sprint_id", active_entry["sprint_dir"].name)
    phase = str(status.get("phase", "unknown"))
    last_updated_at = int(status.get("last_updated_at", 0) or 0)
    age_seconds = max(0, int(time.time()) - last_updated_at)

    print(f"Active sprint: {sprint_id} ({phase})")
    print(f"Status file: {active_entry['path']}")
    print(f"Heartbeat age: {age_seconds} seconds")

    if phase not in STALE_PHASES:
        print("Sprint is not in a stale-detectable execution phase. No recovery needed.")
        return 0

    if age_seconds <= args.timeout_seconds:
        print("Sprint heartbeat is within the timeout window. No recovery needed.")
        return 0

    recovery = recover_stale_sprint(
        active_entry,
        int(time.time()),
        args.timeout_seconds,
        args.dry_run,
    )

    action = "Would prepare fresh-worker dispatch for" if args.dry_run else "Prepared fresh-worker dispatch for"
    print(f"{action} stale sprint {recovery['sprint_id']}.")
    print(f"Worker resume from: {recovery['resume_from']}")
    print(f"Worker phase: {recovery['resume_phase']}")
    print(f"Worker checkpoint: {recovery['next_checkpoint']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
