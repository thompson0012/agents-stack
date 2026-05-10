#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validation_common import (
    BLOCKING_SEVERITIES,
    NONE_MARKERS,
    append_unique,
    parse_bool,
    parse_contract_check_results,
    parse_findings,
    parse_list,
    parse_scalar,
    read_json,
    read_text,
    split_sections,
)

REVIEW_PHASES = {"review_recorded", "review_failed"}



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
    all_acceptance_criteria_accounted_for: bool | None = None
    declared_criteria_total: int | None = None
    declared_criteria_checked: int | None = None
    declared_open_blocking_findings_count: int | None = None
    contract_checks: list[dict[str, str]] = []
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
            criteria_total_value = parse_scalar(coverage_section, "criteria_total")
            criteria_checked_value = parse_scalar(coverage_section, "criteria_checked")
            all_accounted_value = parse_scalar(
                coverage_section, "all_acceptance_criteria_accounted_for"
            )

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

            if criteria_total_value is None:
                append_unique(reasons, ["missing_criteria_total"])
            else:
                try:
                    declared_criteria_total = int(criteria_total_value)
                except ValueError:
                    append_unique(reasons, ["invalid_criteria_total"])
                else:
                    if declared_criteria_total < 0:
                        append_unique(reasons, ["invalid_criteria_total"])

            if criteria_checked_value is None:
                append_unique(reasons, ["missing_criteria_checked"])
            else:
                try:
                    declared_criteria_checked = int(criteria_checked_value)
                except ValueError:
                    append_unique(reasons, ["invalid_criteria_checked"])
                else:
                    if declared_criteria_checked < 0:
                        append_unique(reasons, ["invalid_criteria_checked"])

            all_acceptance_criteria_accounted_for = parse_bool(all_accounted_value)
            if all_acceptance_criteria_accounted_for is None:
                append_unique(reasons, ["missing_all_acceptance_criteria_accounted_for"])

        contract_results_section = sections.get("contract check results")
        if contract_results_section is None:
            append_unique(reasons, ["missing_contract_check_results_section"])
        else:
            contract_checks, contract_check_errors = parse_contract_check_results(contract_results_section)
            append_unique(reasons, contract_check_errors)

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
            open_count_value = parse_scalar(
                convergence_section, "open_blocking_findings_count"
            )

            if convergence_value is None:
                append_unique(reasons, ["missing_convergence_status"])
            else:
                convergence_status = convergence_value.strip().lower()
                if convergence_status not in {"open", "closed"}:
                    append_unique(reasons, ["invalid_convergence_status"])

            if open_count_value is None:
                append_unique(reasons, ["missing_open_blocking_findings_count"])
            else:
                try:
                    declared_open_blocking_findings_count = int(open_count_value)
                except ValueError:
                    append_unique(reasons, ["invalid_open_blocking_findings_count"])
                else:
                    if declared_open_blocking_findings_count < 0:
                        append_unique(reasons, ["invalid_open_blocking_findings_count"])

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

    if declared_criteria_checked is not None and declared_criteria_checked != len(contract_checks):
        append_unique(reasons, ["criteria_checked_mismatch"])
    if declared_criteria_total is not None and declared_criteria_checked is not None:
        if declared_criteria_checked > declared_criteria_total:
            append_unique(reasons, ["criteria_checked_exceeds_total"])
    if all_acceptance_criteria_accounted_for is True:
        if declared_criteria_total is not None and declared_criteria_checked is not None:
            if declared_criteria_total != declared_criteria_checked:
                append_unique(reasons, ["acceptance_criteria_accounting_mismatch"])
    if all_acceptance_criteria_accounted_for is False and coverage_status == "complete":
        append_unique(reasons, ["complete_coverage_without_full_acceptance_accounting"])
    if coverage_status == "complete" and contract_checks:
        if any(check["status"] == "NOT_RUN" for check in contract_checks):
            append_unique(reasons, ["complete_coverage_with_unchecked_contract_result"])

    if declared_open_blocking_findings_count is not None and declared_open_blocking_findings_count != len(computed_open_blockers):
        append_unique(reasons, ["open_blocking_findings_count_mismatch"])

    if convergence_status == "closed" and computed_open_blockers:
        append_unique(reasons, ["closed_convergence_with_open_blockers"])
    if convergence_status == "open" and not computed_open_blockers and coverage_status == "complete":
        append_unique(reasons, ["open_convergence_without_blockers"])

    if verdict_text == "PASS":
        if coverage_status != "complete":
            append_unique(reasons, ["pass_requires_complete_coverage"])
        if all_acceptance_criteria_accounted_for is not True:
            append_unique(reasons, ["pass_requires_full_acceptance_accounting"])
        if convergence_status != "closed":
            append_unique(reasons, ["pass_requires_closed_convergence"])
        if computed_open_blockers:
            append_unique(reasons, ["pass_has_open_blockers"])
        if any(check["status"] != "PASS" for check in contract_checks):
            append_unique(reasons, ["pass_has_non_pass_contract_check"])
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
        "criteria_total": declared_criteria_total,
        "criteria_checked": declared_criteria_checked,
        "all_acceptance_criteria_accounted_for": all_acceptance_criteria_accounted_for,
        "convergence_status": convergence_status,
        "declared_open_blocking_findings_count": declared_open_blocking_findings_count,
        "computed_open_blocking_findings_count": len(computed_open_blockers),
        "open_blocking_ids": computed_open_blockers,
    }
    print(json.dumps({"verdict": verdict, "reasons": reasons, "summary": summary}))
    return 0 if verdict == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
