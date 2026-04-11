#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

BLOCKING_SEVERITIES = {"P0", "P1", "P2", "P3"}
NONE_MARKERS = {"", "none", "null", "n/a", "na", "-"}
REVIEW_PHASES = {"reviewed_pass", "reviewed_fail", "reviewed_blocked", "review_failed"}
FINDING_PATTERN = re.compile(
    r"^\s*-\s*`?(?P<id>[^`|]+?)`?\s*\|\s*severity=(?P<severity>[A-Za-z0-9_-]+)\s*\|\s*status=(?P<status>[A-Za-z0-9_-]+)\s*\|\s*duplicate_of=(?P<duplicate_of>[^|]*)\s*$"
)


class ValidationError(Exception):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate review convergence metadata before state-update publishes tracked-work or progress mutations."
        )
    )
    parser.add_argument("workstream_id", help="Sprint/workstream identifier to validate.")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing docs/live and .harness (default: current directory).",
    )
    return parser.parse_args()


def append_unique(reasons: list[str], additions: list[str]) -> None:
    for reason in additions:
        if reason not in reasons:
            reasons.append(reason)


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


def read_text(path: Path, missing_reason: str) -> tuple[str | None, list[str]]:
    try:
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except FileNotFoundError:
        return None, [missing_reason]

    if not text.strip():
        return None, [missing_reason]
    return text, []


def split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("## "):
            current = line[3:].strip().lower()
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return sections


def parse_scalar(section_lines: list[str], key: str) -> str | None:
    needle = f"- {key}:"
    for line in section_lines:
        stripped = line.strip()
        if stripped.startswith(needle):
            return stripped[len(needle) :].strip()
    return None


def parse_list(section_lines: list[str], key: str) -> list[str] | None:
    needle = f"- {key}:"
    for index, line in enumerate(section_lines):
        stripped = line.strip()
        if not stripped.startswith(needle):
            continue

        inline = stripped[len(needle) :].strip()
        if inline == "[]":
            return []
        if inline:
            return [inline]

        values: list[str] = []
        cursor = index + 1
        while cursor < len(section_lines):
            candidate = section_lines[cursor]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                cursor += 1
                continue
            if candidate.startswith("  - ") or candidate.startswith("\t- "):
                values.append(candidate_stripped[2:].strip())
                cursor += 1
                continue
            if candidate_stripped.startswith("- "):
                break
            cursor += 1
        return values
    return None


def normalize_duplicate(value: str) -> str | None:
    lowered = value.strip().lower()
    if lowered in NONE_MARKERS:
        return None
    return value.strip()


def parse_findings(section_lines: list[str]) -> tuple[list[dict[str, str | None]], list[str]]:
    findings: list[dict[str, str | None]] = []
    reasons: list[str] = []

    for line in section_lines:
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        match = FINDING_PATTERN.match(stripped)
        if match is None:
            if stripped.startswith("- `") or "severity=" in stripped or "duplicate_of=" in stripped:
                append_unique(reasons, ["invalid_finding_format"])
            continue
        finding_id = match.group("id").strip()
        severity = match.group("severity").strip().upper()
        status = match.group("status").strip().upper()
        duplicate_of = normalize_duplicate(match.group("duplicate_of"))
        findings.append(
            {
                "id": finding_id,
                "severity": severity,
                "status": status,
                "duplicate_of": duplicate_of,
            }
        )

    if not findings:
        append_unique(reasons, ["missing_findings_list"])
    return findings, reasons


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    workstream_id = args.workstream_id
    sprint_dir = repo_root / ".harness" / workstream_id
    review_path = sprint_dir / "review.md"
    status_path = sprint_dir / "status.json"

    reasons: list[str] = []

    status_data, status_errors = read_json(
        status_path,
        "missing_status_json",
        "invalid_status_json",
    )
    append_unique(reasons, status_errors)

    review_text, review_errors = read_text(review_path, "missing_review_md")
    append_unique(reasons, review_errors)

    status_phase: str | None = None
    if status_data is not None:
        raw_phase = status_data.get("phase")
        if not isinstance(raw_phase, str) or not raw_phase.strip():
            append_unique(reasons, ["missing_status_phase"])
        else:
            status_phase = raw_phase.strip()
            if status_phase not in REVIEW_PHASES:
                append_unique(reasons, ["status_not_at_review_checkpoint"])

        sprint_id = status_data.get("sprint_id")
        if sprint_id is not None and sprint_id != workstream_id:
            append_unique(reasons, ["status_sprint_id_mismatch"])

    verdict_text: str | None = None
    coverage_status: str | None = None
    convergence_status: str | None = None
    declared_open_blocking_count: int | None = None
    findings: list[dict[str, str | None]] = []
    computed_open_blockers: list[str] = []

    if review_text is not None:
        sections = split_sections(review_text)

        status_section = sections.get("status")
        if not status_section:
            append_unique(reasons, ["missing_review_status_section"])
        else:
            for line in status_section:
                stripped = line.strip()
                if stripped in {"PASS", "FAIL", "BLOCKED"}:
                    verdict_text = stripped
                    break
            if verdict_text is None:
                append_unique(reasons, ["invalid_review_status"])

        coverage_section = sections.get("coverage metadata")
        if not coverage_section:
            append_unique(reasons, ["missing_coverage_metadata"])
        else:
            areas_reviewed = parse_list(coverage_section, "areas_reviewed")
            areas_not_reviewed = parse_list(coverage_section, "areas_not_reviewed")
            coverage_value = parse_scalar(coverage_section, "coverage_status")

            if areas_reviewed is None:
                append_unique(reasons, ["missing_areas_reviewed"])
                areas_reviewed = []
            if areas_not_reviewed is None:
                append_unique(reasons, ["missing_areas_not_reviewed"])
                areas_not_reviewed = []
            if not areas_reviewed:
                append_unique(reasons, ["empty_areas_reviewed"])

            if coverage_value is None:
                append_unique(reasons, ["missing_coverage_status"])
            else:
                coverage_status = coverage_value.strip().lower()
                if coverage_status not in {"complete", "incomplete"}:
                    append_unique(reasons, ["invalid_coverage_status"])
                elif coverage_status == "complete":
                    normalized_gaps = {item.strip().lower() for item in areas_not_reviewed if item.strip()}
                    if normalized_gaps and not normalized_gaps.issubset(NONE_MARKERS):
                        append_unique(reasons, ["coverage_complete_with_gaps"])

        findings_section = sections.get("findings") or sections.get("findings ledger")
        if findings_section is None:
            append_unique(reasons, ["missing_findings_section"])
        else:
            findings, finding_errors = parse_findings(findings_section)
            append_unique(reasons, finding_errors)

        convergence_section = sections.get("convergence summary")
        if not convergence_section:
            append_unique(reasons, ["missing_convergence_metadata"])
        else:
            convergence_value = parse_scalar(convergence_section, "convergence_status")
            open_count_value = parse_scalar(convergence_section, "open_blocking_count")

            if convergence_value is None:
                append_unique(reasons, ["missing_convergence_status"])
            else:
                convergence_status = convergence_value.strip().lower()
                if convergence_status not in {"open", "closed"}:
                    append_unique(reasons, ["invalid_convergence_status"])

            if open_count_value is None:
                append_unique(reasons, ["missing_open_blocking_count"])
            else:
                try:
                    declared_open_blocking_count = int(open_count_value)
                except ValueError:
                    append_unique(reasons, ["invalid_open_blocking_count"])
                else:
                    if declared_open_blocking_count < 0:
                        append_unique(reasons, ["invalid_open_blocking_count"])

    finding_index = {str(finding["id"]): finding for finding in findings}
    seen_ids: set[str] = set()
    for finding in findings:
        finding_id = str(finding["id"])
        if finding_id in seen_ids:
            append_unique(reasons, ["duplicate_finding_id"])
            continue
        seen_ids.add(finding_id)

    for finding in findings:
        duplicate_of = finding["duplicate_of"]
        if duplicate_of is None:
            continue
        if duplicate_of == finding["id"]:
            append_unique(reasons, ["self_duplicate_reference"])
            continue
        target = finding_index.get(str(duplicate_of))
        if target is None:
            append_unique(reasons, ["unknown_duplicate_reference"])
            continue
        if str(target["status"]).upper() != "OPEN":
            append_unique(reasons, ["duplicate_targets_non_open_finding"])

    for finding in findings:
        if str(finding["severity"]).upper() not in BLOCKING_SEVERITIES:
            continue
        if str(finding["status"]).upper() != "OPEN":
            continue
        if finding["duplicate_of"] is not None:
            continue
        computed_open_blockers.append(str(finding["id"]))

    if declared_open_blocking_count is not None and declared_open_blocking_count != len(computed_open_blockers):
        append_unique(reasons, ["open_blocking_count_mismatch"])

    if convergence_status == "closed" and computed_open_blockers:
        append_unique(reasons, ["closed_convergence_with_open_blockers"])
    if convergence_status == "open" and not computed_open_blockers and coverage_status == "complete":
        append_unique(reasons, ["open_convergence_without_blockers"])

    if verdict_text == "PASS":
        if coverage_status != "complete":
            append_unique(reasons, ["pass_requires_complete_coverage"])
        if convergence_status != "closed":
            append_unique(reasons, ["pass_requires_closed_convergence"])
        if computed_open_blockers:
            append_unique(reasons, ["pass_has_open_blockers"])
    elif verdict_text == "FAIL":
        pass
    elif verdict_text == "BLOCKED":
        if computed_open_blockers:
            append_unique(reasons, ["blocking_findings_require_fail"])

    verdict = "allow" if not reasons else "deny"
    summary = {
        "workstream_id": workstream_id,
        "review_status": verdict_text,
        "status_phase": status_phase,
        "coverage_status": coverage_status,
        "convergence_status": convergence_status,
        "declared_open_blocking_count": declared_open_blocking_count,
        "computed_open_blocking_count": len(computed_open_blockers),
        "open_blocking_ids": computed_open_blockers,
    }
    print(json.dumps({"verdict": verdict, "reasons": reasons, "summary": summary}))
    return 0 if verdict == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
