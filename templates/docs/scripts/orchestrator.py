#!/usr/bin/env python3
"""Reference harness orchestrator helper for starter repositories.

The helper inspects durable harness state, enforces the one-runnable-sprint rule,
understands parked human-gated sprints, and prepares fresh-worker dispatch plans.
It does not perform child phase work inline, and the state files remain the source
of truth.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT_SECONDS = 15 * 60
TERMINAL_PHASES = {"archived", "completed", "cancelled"}
PARKED_PHASES = {"awaiting_human", "escalated_to_human"}
STALE_PHASES = {"in_progress", "in_review"}
RETRYABLE_PHASES = {"review_failed", "build_failed"}
DEPENDENCY_SATISFIED_STATUSES = {"archived", "completed", "done", "passed"}
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
        description=(
            "Inspect harness state, report routing decisions, and optionally record "
            "timeout recovery metadata for stale work."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root that contains .harness and docs/live/tracked-work.json.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=(
            "Maximum age for an execution heartbeat before timeout recovery metadata "
            "may be recorded for a stale runnable sprint."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the dispatch plan without rewriting status files.",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def load_optional_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def normalize_markdown_label(value: str) -> str:
    cleaned = re.sub(r"[*_`#]", "", value)
    cleaned = cleaned.strip().strip(":")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.lower()


def extract_markdown_field(text: str, labels: tuple[str, ...]) -> str | None:
    wanted = {normalize_markdown_label(label) for label in labels}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        candidate = line.lstrip("-* ").strip()
        if ":" not in candidate:
            continue
        raw_label, raw_value = candidate.split(":", 1)
        value = raw_value.strip()
        if normalize_markdown_label(raw_label) in wanted and value:
            return value
    return None


def extract_markdown_section(text: str, headings: tuple[str, ...]) -> str | None:
    wanted = {normalize_markdown_label(heading) for heading in headings}
    active_heading: str | None = None
    collected: list[str] = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            heading = normalize_markdown_label(stripped.lstrip("#").strip())
            if active_heading is not None:
                break
            if heading in wanted:
                active_heading = heading
            continue
        if active_heading is None or not stripped:
            continue
        collected.append(stripped)
    if not collected:
        return None
    return "\n".join(collected)


def first_present(*values: str | None) -> str | None:
    for value in values:
        if value:
            return value
    return None


def control_doc_field(
    text: str | None,
    *,
    labels: tuple[str, ...],
    headings: tuple[str, ...] = (),
) -> str | None:
    if not text:
        return None
    return first_present(
        extract_markdown_field(text, labels),
        extract_markdown_section(text, headings),
    )


def load_live_control(repo_root: Path) -> dict[str, Any]:
    live_root = repo_root / "docs" / "live"
    roadmap_path = live_root / "roadmap.md"
    focus_path = live_root / "current-focus.md"
    roadmap_text = load_optional_text(roadmap_path)
    focus_text = load_optional_text(focus_path)

    return {
        "roadmap_path": roadmap_path,
        "roadmap_exists": roadmap_text is not None,
        "focus_path": focus_path,
        "focus_exists": focus_text is not None,
        "source_goal": control_doc_field(
            roadmap_text,
            labels=("source goal", "source objective", "initiative goal"),
            headings=("source goal",),
        ),
        "roadmap_status": first_present(
            control_doc_field(
                roadmap_text,
                labels=(
                    "roadmap status",
                    "initiative status",
                    "status",
                    "current roadmap phase",
                ),
                headings=(
                    "roadmap status",
                    "initiative status",
                    "status",
                    "current roadmap phase",
                ),
            ),
            control_doc_field(
                focus_text,
                labels=("current roadmap phase", "roadmap phase"),
                headings=("current roadmap phase", "roadmap phase"),
            ),
        ),
        "remaining_work": control_doc_field(
            roadmap_text,
            labels=(
                "remaining work",
                "visible remaining-work summary",
                "ordered remaining slices/phases",
                "open work",
                "next steps",
            ),
            headings=(
                "remaining work",
                "visible remaining-work summary",
                "ordered remaining slices/phases",
                "open work",
                "next steps",
            ),
        ),
        "current_objective": first_present(
            control_doc_field(
                focus_text,
                labels=("current objective", "objective", "phase goal"),
                headings=("current objective", "objective", "phase goal"),
            ),
            control_doc_field(
                roadmap_text,
                labels=("current objective", "plan goal", "phase goal"),
                headings=("current objective", "plan goal", "phase goal"),
            ),
        ),
        "next_owner": first_present(
            control_doc_field(
                focus_text,
                labels=("next owner", "owner", "resume owner"),
                headings=("next owner", "owner"),
            ),
            control_doc_field(
                roadmap_text,
                labels=("next owner", "owner"),
                headings=("next owner", "owner"),
            ),
        ),
    }


def load_statuses(harness_root: Path) -> list[dict[str, Any]]:
    statuses: list[dict[str, Any]] = []
    for status_path in sorted(harness_root.glob("*/status.json")):
        status = load_json(status_path)
        statuses.append(
            {
                "path": status_path,
                "sprint_dir": status_path.parent,
                "status": status,
            }
        )
    return statuses


def normalize_phase(status: dict[str, Any]) -> str:
    return str(status.get("phase", "unknown")).strip()


def is_terminal(status: dict[str, Any]) -> bool:
    return normalize_phase(status) in TERMINAL_PHASES


def is_parked(status: dict[str, Any]) -> bool:
    return normalize_phase(status) in PARKED_PHASES


def is_runnable(status: dict[str, Any]) -> bool:
    phase = normalize_phase(status)
    return phase not in TERMINAL_PHASES and phase not in PARKED_PHASES


def find_runnable_sprints(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [entry for entry in entries if is_runnable(entry["status"])]


def find_parked_sprints(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [entry for entry in entries if is_parked(entry["status"])]


def describe_sprint(entry: dict[str, Any]) -> str:
    status = entry["status"]
    sprint_id = status.get("sprint_id", entry["sprint_dir"].name)
    phase = normalize_phase(status)
    return f"{sprint_id} ({phase}) at {entry['path']}"


def artifact_snapshot(sprint_dir: Path) -> dict[str, bool]:
    return {name: (sprint_dir / name).exists() for name in ARTIFACT_FILES}


def coerce_optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def attempt_budget(status: dict[str, Any]) -> tuple[int | None, int | None]:
    return coerce_optional_int(status.get("attempt_count")), coerce_optional_int(
        status.get("max_attempts")
    )


def retry_budget_state(status: dict[str, Any]) -> tuple[str, str]:
    attempt_count, max_attempts = attempt_budget(status)
    if attempt_count is None or max_attempts is None:
        return (
            "missing",
            "Retry budget missing: both attempt_count and max_attempts must be recorded before automatic retry.",
        )
    if attempt_count >= max_attempts:
        return (
            "exhausted",
            f"Retry budget exhausted: attempt_count={attempt_count}, max_attempts={max_attempts}.",
        )
    return (
        "available",
        f"Retry budget available: attempt_count={attempt_count}, max_attempts={max_attempts}; next automatic retry would be attempt {attempt_count + 1}.",
    )


def clean_restore_message(status: dict[str, Any]) -> tuple[bool, str]:
    clean_restore_ref = status.get("clean_restore_ref")
    if clean_restore_ref:
        return (
            True,
            f"Clean restore required before retry: {clean_restore_ref}",
        )
    return (
        False,
        "Clean restore requirement missing: record clean_restore_ref before automatic retry.",
    )


def infer_timeout_resume_target(
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
            "adversarial-live-review",
            "Dispatch a fresh adversarial-live-review worker. It must read the generator handoff, verify the workspace matches it, then rerun the review.",
        )

    if review_path.exists() and status.get("review_status") == "fail":
        return (
            "review.md",
            "generator-execution",
            "Dispatch a fresh generator-execution worker. It must read review.md, stay inside the contract boundary, apply the recorded defects, and refresh handoff.md before another review pass.",
        )

    if handoff_path.exists():
        return (
            "handoff.md",
            "adversarial-live-review",
            "Dispatch a fresh adversarial-live-review worker. It must read handoff.md, confirm the checkpoint against the repo, then continue the pending review.",
        )

    if contract_path.exists():
        return (
            "contract.md",
            "generator-execution",
            "Dispatch a fresh generator-execution worker. It must read contract.md, confirm the allowed files, and resume implementation from the last verified checkpoint.",
        )

    if proposal_path.exists():
        return (
            "sprint_proposal.md",
            "evaluator-contract-review",
            "Dispatch a fresh evaluator-contract-review worker. It must read sprint_proposal.md and decide whether the sprint should be approved, revised, or cancelled.",
        )

    fallback = status.get("resume_from") or "status.json"
    return (
        str(fallback),
        "generator-execution",
        "Dispatch a fresh generator-execution worker. It must continue the execution lane from the strongest remaining evidence without guessing a different child.",
    )


def recover_stale_sprint(
    entry: dict[str, Any],
    now: int,
    timeout_seconds: int,
    dry_run: bool,
) -> dict[str, Any]:
    """Record the next fresh-worker dispatch plan for a stale runnable sprint."""
    status = dict(entry["status"])
    previous_phase = normalize_phase(status)
    last_updated_at = int(status.get("last_updated_at", 0) or 0)
    stale_for_seconds = max(0, now - last_updated_at)
    resume_from, resume_phase, next_checkpoint = infer_timeout_resume_target(
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
            "worker_subject": (
                f"Resume {status.get('sprint_id', entry['sprint_dir'].name)} via {resume_phase}"
            ),
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


def load_tracked_work(repo_root: Path) -> tuple[dict[str, Any] | None, str | None, Path]:
    tracked_work_path = repo_root / "docs" / "live" / "tracked-work.json"
    if not tracked_work_path.exists():
        return None, f"Missing backlog file: {tracked_work_path}", tracked_work_path
    try:
        data = load_json(tracked_work_path)
    except json.JSONDecodeError as exc:
        return None, f"Invalid JSON in {tracked_work_path}: {exc}", tracked_work_path
    if not isinstance(data, dict):
        return None, f"Expected top-level object in {tracked_work_path}", tracked_work_path
    return data, None, tracked_work_path


def runnable_active_pointer(features: dict[str, Any]) -> Any:
    pointer = features.get("runnable_active_sprint_id")
    if pointer in (None, ""):
        pointer = features.get("active_sprint_id")
    return pointer


def compound_queue_ids(
    features: dict[str, Any], tracked_work_path: Path
 ) -> tuple[list[str] | None, str | None]:
    raw_queue = features.get("compound_pending_feature_ids", [])
    if raw_queue is None:
        raw_queue = []
    if not isinstance(raw_queue, list):
        return None, f"Expected compound_pending_feature_ids array in {tracked_work_path}"
    queue: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(raw_queue):
        item_id = str(item).strip()
        if not item_id:
            return None, (
                f"compound_pending_feature_ids entry #{index} in {tracked_work_path} is empty."
            )
        if item_id in seen:
            return None, f"compound_pending_feature_ids contains duplicate id {item_id}."
        seen.add(item_id)
        queue.append(item_id)
    return queue, None


def get_backlog(features: dict[str, Any], tracked_work_path: Path) -> tuple[list[dict[str, Any]] | None, str | None]:
    backlog = features.get("backlog")
    if not isinstance(backlog, list):
        return None, f"Expected backlog array in {tracked_work_path}"
    entries: list[dict[str, Any]] = []
    for index, item in enumerate(backlog):
        if not isinstance(item, dict):
            return None, f"Backlog entry #{index} in {tracked_work_path} is not an object"
        entries.append(item)
    return entries, None


def backlog_index(backlog: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(item["id"]): item
        for item in backlog
        if isinstance(item.get("id"), str) and item.get("id")
    }


def backlog_priority(item: dict[str, Any], index: int) -> tuple[int, int]:
    priority = item.get("priority")
    if isinstance(priority, bool):
        priority = None
    if isinstance(priority, int):
        return priority, index
    return 10**9, index


def dependency_status_satisfied(status: Any) -> bool:
    return str(status).strip().lower() in DEPENDENCY_SATISFIED_STATUSES


def select_next_feature(
    backlog: list[dict[str, Any]],
    candidate_statuses: set[str],
 ) -> tuple[dict[str, Any] | None, list[str], dict[str, list[str]]]:
    errors: list[str] = []
    blocked_reasons: dict[str, list[str]] = {}
    ready: list[tuple[tuple[int, int], dict[str, Any]]] = []
    by_id = backlog_index(backlog)

    if len(by_id) != len(backlog):
        errors.append("Backlog ids must be unique and non-empty.")
        return None, errors, blocked_reasons

    for index, item in enumerate(backlog):
        item_id = str(item.get("id", "")).strip()
        if not item_id:
            errors.append(f"Backlog entry #{index} is missing id.")
            continue

        status = str(item.get("status", "")).strip().lower()
        if status not in candidate_statuses:
            continue

        dependencies = item.get("dependencies", [])
        if dependencies is None:
            dependencies = []
        if not isinstance(dependencies, list):
            errors.append(f"{item_id} has non-list dependencies.")
            continue

        blockers: list[str] = []
        for dependency in dependencies:
            dependency_id = str(dependency).strip()
            if not dependency_id:
                blockers.append("empty dependency id")
                continue
            dependency_item = by_id.get(dependency_id)
            if dependency_item is None:
                errors.append(f"{item_id} depends on missing backlog item {dependency_id}.")
                continue
            dependency_status = dependency_item.get("status")
            if not dependency_status_satisfied(dependency_status):
                blockers.append(f"{dependency_id} is {dependency_status}")

        if blockers:
            blocked_reasons[item_id] = blockers
            continue

        ready.append((backlog_priority(item, index), item))

    if errors:
        return None, errors, blocked_reasons
    if not ready:
        return None, [], blocked_reasons
    ready.sort(key=lambda pair: pair[0])
    return ready[0][1], [], blocked_reasons


def print_control_value(label: str, value: str) -> None:
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    if not lines:
        return
    if len(lines) == 1:
        print(f"{label}: {lines[0]}")
        return
    print(f"{label}:")
    for line in lines:
        print(f"  {line}")


def report_live_control(control: dict[str, Any]) -> None:
    print("Live control plane:")
    roadmap_note = " (missing)" if not control["roadmap_exists"] else ""
    focus_note = " (missing)" if not control["focus_exists"] else ""
    print(f"- roadmap file: {control['roadmap_path']}{roadmap_note}")
    print(f"- current focus file: {control['focus_path']}{focus_note}")

    source_goal = control.get("source_goal")
    if source_goal:
        print_control_value("Source goal", str(source_goal))
    elif control["roadmap_exists"]:
        print("Source goal: unspecified in docs/live/roadmap.md")

    current_objective = control.get("current_objective")
    if current_objective:
        print_control_value("Current objective", str(current_objective))
    elif control["focus_exists"]:
        print("Current objective: unspecified in docs/live/current-focus.md")
    else:
        print(f"Current objective: unavailable (missing {control['focus_path']})")

    next_owner = control.get("next_owner")
    if next_owner:
        print_control_value("Next owner", str(next_owner))
    elif control["focus_exists"]:
        print("Next owner: unspecified in docs/live/current-focus.md")
    else:
        print(f"Next owner: unavailable (missing {control['focus_path']})")

    roadmap_status = control.get("roadmap_status")
    remaining_work = control.get("remaining_work")
    if control["roadmap_exists"]:
        if roadmap_status:
            print_control_value("Roadmap status", str(roadmap_status))
        else:
            print("Roadmap status: unspecified in docs/live/roadmap.md")
        if remaining_work:
            print_control_value("Remaining work", str(remaining_work))
        else:
            print("Remaining work: unspecified in docs/live/roadmap.md")
    else:
        print(f"Roadmap status: unavailable (missing {control['roadmap_path']})")
        print(
            "Remaining work: unavailable until docs/live/roadmap.md exists; routing falls back to docs/live/tracked-work.json backlog selection and sprint-local evidence."
        )
    print()


def report_parked_sprints(parked_entries: list[dict[str, Any]]) -> None:
    if not parked_entries:
        return
    print("Parked sprints:")
    for entry in parked_entries:
        status = entry["status"]
        sprint_id = status.get("sprint_id", entry["sprint_dir"].name)
        phase = normalize_phase(status)
        pause_reason = status.get("pause_reason") or status.get("escalation_reason")
        human_action = status.get("human_action_required")
        print(f"- {sprint_id} ({phase})")
        if pause_reason:
            print(f"  reason: {pause_reason}")
        if human_action:
            print(f"  human action required: {human_action}")


def report_compound_queue(
    features: dict[str, Any] | None,
    features_error: str | None,
    tracked_work_path: Path,
 ) -> int | None:
    if features_error or features is None:
        return None

    backlog, backlog_error = get_backlog(features, tracked_work_path)
    if backlog_error:
        print(f"ERROR: {backlog_error}")
        return 2
    assert backlog is not None

    queue, queue_error = compound_queue_ids(features, tracked_work_path)
    if queue_error:
        print(f"ERROR: {queue_error}")
        return 2
    assert queue is not None
    if not queue:
        return None

    by_id = backlog_index(backlog)
    missing = [item_id for item_id in queue if item_id not in by_id]
    if missing:
        print(
            "ERROR: compound_pending_feature_ids references missing backlog items: "
            + ", ".join(missing)
        )
        return 2

    print(f"Compound queue pending: {', '.join(queue)}")
    first_item = by_id[queue[0]]
    print(
        f"First queued feature: {queue[0]} - {first_item.get('title', 'untitled')}"
    )
    evidence_path = (
        first_item.get("evidence_path")
        or first_item.get("archive_path")
        or first_item.get("local_state_path")
    )
    if evidence_path:
        print(f"Evidence path: {evidence_path}")
    active_pointer = runnable_active_pointer(features)
    if active_pointer not in (None, ""):
        print(f"Runnable sprint remains visible but held behind compounding: {active_pointer}")
    print(
        "Route: compound-capture must run before any runnable sprint resume or new backlog selection."
    )
    return 0


def report_next_backlog_feature(
    features: dict[str, Any] | None,
    features_error: str | None,
    tracked_work_path: Path,
 ) -> int:
    if features_error:
        print(f"ERROR: {features_error}")
        return 2
    if features is None:
        print(f"ERROR: missing readable backlog state at {tracked_work_path}")
        return 2

    active_pointer = runnable_active_pointer(features)
    if active_pointer not in (None, ""):
        print(
            f"ERROR: live state at {tracked_work_path} still names runnable active sprint {active_pointer} even though no runnable local sprint exists."
        )
        return 2

    backlog, backlog_error = get_backlog(features, tracked_work_path)
    if backlog_error:
        print(f"ERROR: {backlog_error}")
        return 2
    assert backlog is not None

    brainstorm_item, errors, blocked_brainstorm = select_next_feature(
        backlog, {"needs_brainstorm"}
    )
    if errors:
        print("ERROR: backlog is inconsistent:")
        for error in errors:
            print(f"- {error}")
        return 2

    pending_item, errors, blocked_pending = select_next_feature(backlog, {"pending"})
    if errors:
        print("ERROR: backlog is inconsistent:")
        for error in errors:
            print(f"- {error}")
        return 2

    if brainstorm_item is not None:
        print(
            f"Next dependency-ready brainstorm candidate: {brainstorm_item.get('id')} - {brainstorm_item.get('title', 'untitled')}"
        )
        print(
            "Route: generator-brainstorm should refine docs/live/ideas.md and/or promote this candidate because no runnable active sprint exists."
        )
        return 0

    if pending_item is not None:
        print(
            f"Next dependency-ready feature: {pending_item.get('id')} - {pending_item.get('title', 'untitled')}"
        )
        print(
            "Route: generator-proposal should open a sprint proposal for this feature because no compound or brainstorm work outranks it."
        )
        return 0

    print("No dependency-ready `needs_brainstorm` or `pending` feature found.")
    blocked_reasons: dict[str, list[str]] = {}
    for source in (blocked_brainstorm, blocked_pending):
        for item_id, blockers in source.items():
            blocked_reasons.setdefault(item_id, []).extend(blockers)
    if blocked_reasons:
        print("Tracked items are blocked by:")
        for item_id, blockers in sorted(blocked_reasons.items()):
            print(f"- {item_id}: {', '.join(blockers)}")
    return 0


def validate_active_pointer(
    features: dict[str, Any] | None,
    features_error: str | None,
    tracked_work_path: Path,
    active_sprint_id: str,
) -> tuple[bool, str | None]:
    if features_error or features is None:
        return True, None
    pointer = runnable_active_pointer(features)
    if pointer in (None, ""):
        return (
            False,
            f"Live state at {tracked_work_path} does not name runnable active sprint {active_sprint_id}.",
        )
    if str(pointer) != active_sprint_id:
        return (
            False,
            f"Live state points at runnable active sprint {pointer}, but local runnable sprint is {active_sprint_id}.",
        )
    return True, None


def report_retry_plan(entry: dict[str, Any]) -> int:
    status = entry["status"]
    phase = normalize_phase(status)
    sprint_id = status.get("sprint_id", entry["sprint_dir"].name)
    resume_from = status.get("resume_from") or (
        "review.md" if phase == "review_failed" else "runtime.md"
    )
    last_verified_step = status.get("last_verified_step") or "unspecified"
    budget_state, budget_message = retry_budget_state(status)
    has_restore, restore_message = clean_restore_message(status)

    print(f"Retryable sprint: {sprint_id} ({phase})")
    print(f"Resume from: {resume_from}")
    print(f"Last verified step: {last_verified_step}")
    print(restore_message)
    print(budget_message)

    if budget_state == "exhausted":
        print("Human escalation required: automatic retry must stop until a human changes the plan or budget.")
        return 0

    if budget_state == "missing" or not has_restore:
        print("Automatic retry blocked: record missing retry metadata before dispatching generator-execution.")
        return 0

    print("Next worker phase: generator-execution")
    print(
        "Worker checkpoint: restore the named clean boundary first, then dispatch a fresh generator-execution worker for the same sprint."
    )
    return 0


def report_timeout_state(entry: dict[str, Any], args: argparse.Namespace) -> int:
    status = entry["status"]
    sprint_id = status.get("sprint_id", entry["sprint_dir"].name)
    phase = normalize_phase(status)
    last_updated_at = int(status.get("last_updated_at", 0) or 0)
    age_seconds = max(0, int(time.time()) - last_updated_at)

    print(f"Active sprint: {sprint_id} ({phase})")
    print(f"Status file: {entry['path']}")
    print(f"Heartbeat age: {age_seconds} seconds")

    if phase == "paused_by_timeout":
        print("Timeout recovery is already recorded in status.json.")
        print(f"Worker resume from: {status.get('resume_from', 'status.json')}")
        print(f"Worker phase: {status.get('resume_phase', 'unknown')}")
        print(f"Worker checkpoint: {status.get('next_checkpoint', 'unspecified')}")
        return 0

    if phase not in STALE_PHASES:
        print("Sprint is not in a stale-detectable execution phase. No timeout recovery needed.")
        return 0

    if age_seconds <= args.timeout_seconds:
        print("Sprint heartbeat is within the timeout window. No timeout recovery needed.")
        return 0

    recovery = recover_stale_sprint(
        entry,
        int(time.time()),
        args.timeout_seconds,
        args.dry_run,
    )
    action = (
        "Would prepare fresh-worker dispatch for"
        if args.dry_run
        else "Prepared fresh-worker dispatch for"
    )
    print(f"{action} stale sprint {recovery['sprint_id']}.")
    print(f"Worker resume from: {recovery['resume_from']}")
    print(f"Worker phase: {recovery['resume_phase']}")
    print(f"Worker checkpoint: {recovery['next_checkpoint']}")
    return 0


def main() -> int:
    args = parse_args()
    repo_root = Path(args.root).resolve()
    harness_root = repo_root / ".harness"
    features, features_error, tracked_work_path = load_tracked_work(repo_root)
    live_control = load_live_control(repo_root)

    entries: list[dict[str, Any]] = []
    if harness_root.exists():
        try:
            entries = load_statuses(harness_root)
        except json.JSONDecodeError as exc:
            print(f"ERROR: invalid JSON in harness status: {exc}")
            return 2
    elif features_error:
        print(f"ERROR: {features_error}")
        return 2
    report_live_control(live_control)
    if not entries:
        compound_result = report_compound_queue(features, features_error, tracked_work_path)
        if compound_result is not None:
            return compound_result
        print("No sprint status files found under .harness/.")
        return report_next_backlog_feature(features, features_error, tracked_work_path)

    runnable_entries = find_runnable_sprints(entries)
    parked_entries = find_parked_sprints(entries)

    if len(runnable_entries) > 1:
        print("ERROR: expected at most one runnable sprint, but found:")
        for entry in runnable_entries:
            print(f"- {describe_sprint(entry)}")
        report_parked_sprints(parked_entries)
        return 2

    compound_result = report_compound_queue(features, features_error, tracked_work_path)
    if compound_result is not None:
        report_parked_sprints(parked_entries)
        return compound_result

    if not runnable_entries:
        print("No runnable active sprint found.")
        report_parked_sprints(parked_entries)
        return report_next_backlog_feature(features, features_error, tracked_work_path)

    active_entry = runnable_entries[0]
    active_status = active_entry["status"]
    sprint_id = str(active_status.get("sprint_id", active_entry["sprint_dir"].name))
    pointer_ok, pointer_error = validate_active_pointer(
        features,
        features_error,
        tracked_work_path,
        sprint_id,
    )
    if not pointer_ok and pointer_error:
        print(f"ERROR: {pointer_error}")
        return 2

    phase = normalize_phase(active_status)
    if phase == "escalated_to_human":
        print(f"Sprint {sprint_id} is escalated_to_human.")
        print(active_status.get("escalation_reason") or "Human intervention required.")
        return 0

    if phase in RETRYABLE_PHASES:
        return report_retry_plan(active_entry)

    return report_timeout_state(active_entry, args)


if __name__ == "__main__":
    raise SystemExit(main())
