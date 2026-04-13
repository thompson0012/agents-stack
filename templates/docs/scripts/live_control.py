#!/usr/bin/env python3
"""Shared parsing, rendering, and validation helpers for live control-plane scripts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path
from typing import Any

TRACKED_WORK_RELATIVE = Path("docs/live/tracked-work.json")
ROADMAP_RELATIVE = Path("docs/live/roadmap.md")
CURRENT_FOCUS_RELATIVE = Path("docs/live/current-focus.md")
PROGRESS_RELATIVE = Path("docs/live/progress.md")
INIT_SCRIPT_RELATIVE = Path("docs/scripts/init.sh")

ROADMAP_TITLE = "# Initiative Roadmap"
ROADMAP_INTRO = (
    "This file is the non-runnable roadmap for broader goals. It does not select the runnable sprint; "
    "`docs/live/tracked-work.json` still does that."
)
ROADMAP_CANONICAL_NOUN = (
    "- Canonical tracked noun: `workstream`; `sprint` is the execution lifecycle label for a "
    "workstream, not a separate durable entity."
)
ROADMAP_BACKLINK_NOTE = (
    "- Backlog items may carry `roadmap_ref: docs/live/roadmap.md#initiative-roadmap` as a direct "
    "backlink when that makes the item easier to trace; the file-level `roadmap_path` remains the "
    "canonical roadmap pointer."
)
CURRENT_FOCUS_TITLE = "# Current Focus"
CURRENT_FOCUS_INTRO = "This file is a live resume anchor. It is not a second contract."
CURRENT_FOCUS_CONTRACT_TRUTH = (
    "# Contract truth: If a sprint is later opened, `.harness/<workstream-id>/contract.md` becomes "
    "the only runnable sprint contract."
)

RUNNABLE_STATUSES = {
    "build_failed",
    "contracted",
    "executing",
    "in_progress",
    "in_review",
    "paused_by_timeout",
    "review_failed",
}
PARKED_STATUSES = {"awaiting_human", "escalated_to_human"}
TERMINAL_STATUSES = {"archived", "cancelled", "completed", "done", "passed"}

REQUIRED_TRACKED_WORK_KEYS: dict[str, type | tuple[type, ...]] = {
    "project": str,
    "idea_backlog_path": str,
    "current_focus_path": str,
    "roadmap_path": str,
    "records_root_path": str,
    "single_runnable_active_sprint": bool,
    "runnable_active_sprint_id": (str, type(None)),
    "parked_sprint_ids": list,
    "compound_pending_feature_ids": list,
    "backlog": list,
}
TRACKED_WORK_POINTERS = {
    "idea_backlog_path": "docs/live/ideas.md",
    "current_focus_path": "docs/live/current-focus.md",
    "roadmap_path": "docs/live/roadmap.md",
    "records_root_path": "docs/records/",
}


class ControlPlaneError(ValueError):
    """Raised when live control-plane state is malformed."""


@dataclass(frozen=True)
class LivePaths:
    repo_root: Path
    tracked_work: Path
    roadmap: Path
    current_focus: Path
    progress: Path
    init_script: Path


@dataclass(frozen=True)
class BootstrapDrift:
    relative_path: str
    diff: str


@dataclass(frozen=True)
class RoadmapState:
    source_goal: str
    current_slice: str
    remaining_slices: list[str]
    stop_condition: str
    summary: str


@dataclass(frozen=True)
class CurrentFocusState:
    current_objective: str
    source_goal_lineage: str
    current_roadmap_stage: str
    next_owner: str
    next_file_to_open: str


def resolve_repo_root(raw_repo_root: str) -> Path:
    return Path(raw_repo_root).expanduser().resolve()


def live_paths(repo_root: Path) -> LivePaths:
    return LivePaths(
        repo_root=repo_root,
        tracked_work=repo_root / TRACKED_WORK_RELATIVE,
        roadmap=repo_root / ROADMAP_RELATIVE,
        current_focus=repo_root / CURRENT_FOCUS_RELATIVE,
        progress=repo_root / PROGRESS_RELATIVE,
        init_script=repo_root / INIT_SCRIPT_RELATIVE,
    )


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ControlPlaneError(f"missing required file: {path}") from exc


def load_optional_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def load_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ControlPlaneError(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ControlPlaneError(f"invalid JSON in {path}: {exc}") from exc


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def normalize_markdown_label(value: str) -> str:
    cleaned = re.sub(r"[*_`#]", "", value)
    cleaned = cleaned.strip().strip(":")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.lower()


def extract_markdown_field(text: str, labels: tuple[str, ...]) -> str | None:
    wanted = {normalize_markdown_label(label) for label in labels}
    for raw_line in text.splitlines():
        candidate = raw_line.strip().lstrip("-* ").strip()
        if not candidate or ":" not in candidate:
            continue
        raw_label, raw_value = candidate.split(":", 1)
        value = raw_value.strip()
        if normalize_markdown_label(raw_label) in wanted and value:
            return value
    return None


def extract_markdown_section(text: str, headings: tuple[str, ...]) -> str | None:
    wanted = {normalize_markdown_label(heading) for heading in headings}
    collecting = False
    collected: list[str] = []
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("#"):
            if collecting:
                break
            collecting = normalize_markdown_label(stripped.lstrip("#").strip()) in wanted
            continue
        if collecting and stripped:
            collected.append(stripped)
    return "\n".join(collected) if collected else None


def control_doc_field(text: str | None, *, labels: tuple[str, ...], headings: tuple[str, ...] = ()) -> str | None:
    if not text:
        return None
    return extract_markdown_field(text, labels) or extract_markdown_section(text, headings)

def first_present(*values: str | None) -> str | None:
    for value in values:
        if value:
            return value
    return None


def load_live_control(repo_root: Path) -> dict[str, Any]:
    paths = live_paths(repo_root)
    roadmap_text = load_optional_text(paths.roadmap)
    focus_text = load_optional_text(paths.current_focus)

    return {
        "roadmap_path": paths.roadmap,
        "roadmap_exists": roadmap_text is not None,
        "focus_path": paths.current_focus,
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
                    "current roadmap stage",
                ),
                headings=(
                    "roadmap status",
                    "initiative status",
                    "status",
                    "current roadmap stage",
                ),
            ),
            control_doc_field(
                focus_text,
                labels=("current roadmap stage", "roadmap stage"),
                headings=("current roadmap stage", "roadmap stage"),
            ),
        ),
        "remaining_work": control_doc_field(
            roadmap_text,
            labels=(
                "remaining work",
                "visible remaining-work summary",
                "ordered remaining slices/stages",
                "open work",
                "next steps",
            ),
            headings=(
                "remaining work",
                "visible remaining-work summary",
                "ordered remaining slices/stages",
                "open work",
                "next steps",
            ),
        ),
        "current_objective": first_present(
            control_doc_field(
                focus_text,
                labels=("current objective", "objective", "stage goal"),
                headings=("current objective", "objective", "stage goal"),
            ),
            control_doc_field(
                roadmap_text,
                labels=("current objective", "plan goal", "stage goal"),
                headings=("current objective", "plan goal", "stage goal"),
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


def parse_roadmap_text(text: str) -> RoadmapState:
    source_goal = control_doc_field(text, labels=("source goal",), headings=("source goal",))
    current_slice = control_doc_field(text, labels=("current slice",), headings=("current slice",))
    stop_condition = control_doc_field(
        text,
        labels=("stop or re-authorization condition",),
        headings=("stop or re-authorization condition",),
    )
    summary = control_doc_field(
        text,
        labels=("visible remaining-work summary",),
        headings=("visible remaining-work summary",),
    )
    remaining_slices = parse_numbered_list(text, "ordered remaining slices/stages")
    errors: list[str] = []
    if source_goal is None:
        errors.append("missing roadmap field: Source goal")
    if current_slice is None:
        errors.append("missing roadmap field: Current slice")
    if not remaining_slices:
        errors.append("missing roadmap numbered list: Ordered remaining slices/stages")
    if stop_condition is None:
        errors.append("missing roadmap field: Stop or re-authorization condition")
    if summary is None:
        errors.append("missing roadmap field: Visible remaining-work summary")
    if errors:
        raise ControlPlaneError("; ".join(errors))
    return RoadmapState(
        source_goal=source_goal,
        current_slice=current_slice,
        remaining_slices=remaining_slices,
        stop_condition=stop_condition,
        summary=summary,
    )


def render_roadmap(state: RoadmapState) -> str:
    remaining = state.remaining_slices or ["None recorded yet."]
    rendered_remaining = "\n".join(
        f"  {index}. {item}" for index, item in enumerate(remaining, start=1)
    )
    return "\n".join(
        [
            ROADMAP_TITLE,
            "",
            ROADMAP_INTRO,
            "",
            ROADMAP_CANONICAL_NOUN,
            ROADMAP_BACKLINK_NOTE,
            f"- Source goal: {state.source_goal}",
            f"- Current slice: {state.current_slice}",
            "- Ordered remaining slices/stages:",
            rendered_remaining,
            f"- Stop or re-authorization condition: {state.stop_condition}",
            f"- Visible remaining-work summary: {state.summary}",
            "",
        ]
    )


def parse_current_focus_text(text: str) -> CurrentFocusState:
    current_objective = control_doc_field(text, labels=("current objective",), headings=("current objective",))
    source_goal_lineage = control_doc_field(
        text,
        labels=("source-goal lineage",),
        headings=("source-goal lineage",),
    )
    current_roadmap_stage = control_doc_field(
        text,
        labels=("current roadmap stage",),
        headings=("current roadmap stage",),
    )
    next_owner = control_doc_field(text, labels=("next owner",), headings=("next owner",))
    next_file_to_open = control_doc_field(
        text,
        labels=("next file to open",),
        headings=("next file to open",),
    )
    errors: list[str] = []
    if CURRENT_FOCUS_CONTRACT_TRUTH not in text:
        errors.append("missing current-focus contract-truth reminder")
    if current_objective is None:
        errors.append("missing current-focus field: Current objective")
    if source_goal_lineage is None:
        errors.append("missing current-focus field: Source-goal lineage")
    if current_roadmap_stage is None:
        errors.append("missing current-focus field: Current roadmap stage")
    if next_owner is None:
        errors.append("missing current-focus field: Next owner")
    if next_file_to_open is None:
        errors.append("missing current-focus field: Next file to open")
    if errors:
        raise ControlPlaneError("; ".join(errors))
    return CurrentFocusState(
        current_objective=current_objective,
        source_goal_lineage=source_goal_lineage,
        current_roadmap_stage=current_roadmap_stage,
        next_owner=next_owner,
        next_file_to_open=next_file_to_open,
    )


def render_current_focus(state: CurrentFocusState) -> str:
    return "\n".join(
        [
            CURRENT_FOCUS_TITLE,
            "",
            CURRENT_FOCUS_INTRO,
            "",
            f"- Current objective: {state.current_objective}",
            f"- Source-goal lineage: {state.source_goal_lineage}",
            f"- Current roadmap stage: {state.current_roadmap_stage}",
            f"- Next owner: {state.next_owner}",
            f"- Next file to open: {state.next_file_to_open}",
            CURRENT_FOCUS_CONTRACT_TRUTH,
            "",
        ]
    )


def parse_numbered_list(text: str, label: str) -> list[str]:
    prefix = normalize_markdown_label(f"- {label}:")
    lines = text.splitlines()
    collected: list[str] = []
    capture = False
    for raw_line in lines:
        if not capture:
            capture = normalize_markdown_label(raw_line.strip()) == prefix
            continue
        stripped = raw_line.strip()
        if not stripped:
            continue
        if raw_line.startswith("-") or raw_line.startswith("#"):
            break
        match = re.match(r"^\s*\d+\.\s+(.*\S)\s*$", raw_line)
        if not match:
            break
        collected.append(match.group(1))
    return collected


def parse_progress_event_text(value: str) -> str:
    lines = [line.rstrip() for line in value.splitlines()]
    filtered = [line for line in lines if line.strip()]
    if not filtered:
        raise ControlPlaneError("progress event must contain non-empty text")
    return "\n".join(filtered) + "\n"


def validate_control_files(paths: LivePaths) -> list[str]:
    errors: list[str] = []
    roadmap_text = load_optional_text(paths.roadmap)
    focus_text = load_optional_text(paths.current_focus)
    if roadmap_text is None:
        errors.append(f"missing roadmap file: {paths.roadmap}")
    else:
        first_line = roadmap_text.splitlines()[0].strip() if roadmap_text.splitlines() else ""
        if first_line != ROADMAP_TITLE:
            errors.append(f"roadmap title must be '{ROADMAP_TITLE}'")
        try:
            parse_roadmap_text(roadmap_text)
        except ControlPlaneError as exc:
            errors.append(str(exc))
    if focus_text is None:
        errors.append(f"missing current-focus file: {paths.current_focus}")
    else:
        first_line = focus_text.splitlines()[0].strip() if focus_text.splitlines() else ""
        if first_line != CURRENT_FOCUS_TITLE:
            errors.append(f"current-focus title must be '{CURRENT_FOCUS_TITLE}'")
        if CURRENT_FOCUS_INTRO not in focus_text:
            errors.append("current-focus intro line is missing or changed")
        try:
            parse_current_focus_text(focus_text)
        except ControlPlaneError as exc:
            errors.append(str(exc))
    return errors


def validate_tracked_work(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["tracked-work.json must be a JSON object"]
    for key, expected_type in REQUIRED_TRACKED_WORK_KEYS.items():
        if key not in data:
            errors.append(f"tracked-work.json missing top-level key: {key}")
            continue
        if not isinstance(data[key], expected_type):
            errors.append(f"tracked-work.json key '{key}' has wrong type")
    for key, expected in TRACKED_WORK_POINTERS.items():
        value = data.get(key)
        if isinstance(value, str) and value != expected:
            errors.append(f"tracked-work.json key '{key}' must point to {expected!r}, got {value!r}")
    if data.get("single_runnable_active_sprint") is not True:
        errors.append("tracked-work.json must keep single_runnable_active_sprint set to true")
    if "evidence_path" in data:
        errors.append("tracked-work.json top-level must not define evidence_path; keep it on backlog items only")

    backlog = data.get("backlog")
    if not isinstance(backlog, list):
        return errors

    ids: set[str] = set()
    runnable_ids: list[str] = []
    parked_ids: list[str] = []
    backlog_index: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(backlog):
        label = f"backlog[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{label} must include non-empty string id")
            continue
        if item_id in ids:
            errors.append(f"duplicate backlog id: {item_id}")
        ids.add(item_id)
        backlog_index[item_id] = item
        for field in ("title", "summary", "status"):
            if field in item and not isinstance(item[field], str):
                errors.append(f"backlog item {item_id} field '{field}' must be a string when present")
        dependencies = item.get("dependencies", [])
        if not isinstance(dependencies, list) or any(not isinstance(dep, str) for dep in dependencies):
            errors.append(f"backlog item {item_id} dependencies must be a list of strings")
        roadmap_ref = item.get("roadmap_ref")
        if roadmap_ref is not None and not (
            isinstance(roadmap_ref, str) and roadmap_ref.startswith("docs/live/roadmap.md")
        ):
            errors.append(f"backlog item {item_id} roadmap_ref must point into docs/live/roadmap.md")
        for key, prefix in (("record_paths", "docs/records/"), ("reference_paths", "docs/reference/")):
            value = item.get(key)
            if value is None:
                continue
            if not isinstance(value, list) or any(not isinstance(entry, str) or not entry.startswith(prefix) for entry in value):
                errors.append(f"backlog item {item_id} {key} must be a list of paths under {prefix}")
        evidence_path = item.get("evidence_path")
        if evidence_path is not None:
            if not isinstance(evidence_path, str):
                errors.append(f"backlog item {item_id} evidence_path must be a string")
            elif not (
                re.fullmatch(r"\.harness/[^/]+/?", evidence_path)
                or re.fullmatch(r"docs/archive/[^/]+/?", evidence_path)
            ):
                errors.append(
                    f"backlog item {item_id} evidence_path must point to one canonical .harness/ or docs/archive/ directory"
                )
        status = item.get("status")
        if status in RUNNABLE_STATUSES:
            runnable_ids.append(item_id)
            if evidence_path is None:
                errors.append(f"runnable backlog item {item_id} must declare canonical evidence_path")
        if status in PARKED_STATUSES:
            parked_ids.append(item_id)
            if evidence_path is None:
                errors.append(f"parked backlog item {item_id} must declare canonical evidence_path")

    runnable_active_sprint_id = data.get("runnable_active_sprint_id")
    if len(runnable_ids) > 1:
        errors.append(f"single-runnable-sprint invariant violated by backlog items: {', '.join(runnable_ids)}")
    if runnable_ids:
        expected_id = runnable_ids[0]
        if runnable_active_sprint_id != expected_id:
            errors.append(
                "runnable_active_sprint_id must match the only runnable backlog item: "
                f"expected {expected_id!r}, got {runnable_active_sprint_id!r}"
            )
    elif runnable_active_sprint_id is not None:
        errors.append("runnable_active_sprint_id must be null when no runnable backlog item exists")

    parked_sprint_ids = data.get("parked_sprint_ids")
    if isinstance(parked_sprint_ids, list):
        if any(not isinstance(item, str) for item in parked_sprint_ids):
            errors.append("parked_sprint_ids must contain only strings")
        else:
            expected = sorted(parked_ids)
            actual = sorted(parked_sprint_ids)
            if expected != actual:
                errors.append(f"parked_sprint_ids must match parked backlog items: expected {expected}, got {actual}")

    compound_pending = data.get("compound_pending_feature_ids")
    if isinstance(compound_pending, list):
        missing = [item_id for item_id in compound_pending if item_id not in backlog_index]
        if missing:
            errors.append(
                "compound_pending_feature_ids references missing backlog ids: " + ", ".join(missing)
            )
    return errors


def extract_init_seeds(text: str) -> dict[str, str]:
    pattern = re.compile(
        r'write_file_if_missing\s+"(?P<path>[^"]+)"\s+\'(?P<content>.*?)\'(?=\n+\s*(?:write_file_if_missing|ensure_dir|$))',
        re.DOTALL,
    )
    seeds: dict[str, str] = {}
    for match in pattern.finditer(text):
        relative_path = match.group("path")
        seeds[relative_path] = match.group("content")
    return seeds


def compare_bootstrap_alignment(repo_root: Path) -> list[BootstrapDrift]:
    paths = live_paths(repo_root)
    seed_text = load_text(paths.init_script)
    seeds = extract_init_seeds(seed_text)
    drifts: list[BootstrapDrift] = []
    for relative_path, expected in sorted(seeds.items()):
        candidate = repo_root / relative_path
        if not candidate.exists():
            continue
        actual = load_text(candidate)
        normalized_expected = expected.removesuffix("\n")
        normalized_actual = actual.removesuffix("\n")
        if normalized_actual == normalized_expected:
            continue
        diff = "\n".join(
            unified_diff(
                normalized_expected.splitlines(),
                normalized_actual.splitlines(),
                fromfile=f"init.sh:{relative_path}",
                tofile=str(candidate.relative_to(repo_root)),
                lineterm="",
            )
        )
        drifts.append(BootstrapDrift(relative_path=relative_path, diff=diff))
    return drifts
