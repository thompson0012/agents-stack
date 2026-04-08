#!/usr/bin/env python3
"""Advisory-only retry-guard synthesis experiment.

This script is intentionally non-authoritative. It reads the current hand-authored
retry guard sources and emits a stdout report for human inspection only.

Boundaries:
- no disk writes
- no router or worker integration
- no imports from verify_retry_guard.py
- no generated artifact persists after process exit

Any future promotion of this experiment would require a separate contracted slice.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GuardSourcePaths:
    skill_dir: Path
    verifier: Path
    eval_readme: Path
    fixtures: Path
    orchestrator_reference: Path
    state_machine_reference: Path
    children_reference: Path


@dataclass(frozen=True)
class GuardScriptSummary:
    failed_phases: tuple[str, ...]
    deny_reasons: tuple[str, ...]
    required_status_fields: tuple[str, ...]
    tracked_work_fields: tuple[str, ...]
    evidence_files: tuple[str, ...]


@dataclass(frozen=True)
class FixtureSummary:
    fixture_ids: tuple[str, ...]
    phase_gates: tuple[str, ...]
    mentions_build_failed: bool
    mentions_review_failed: bool


@dataclass(frozen=True)
class ReferenceSummary:
    path: Path
    lines: tuple[str, ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compile an advisory retry-guard report from current hand-authored sources."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing templates/.agents/skills (default: current directory).",
    )
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").replace("\r\n", "\n")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"missing file: {path}") from exc


def resolve_paths(repo_root: Path) -> GuardSourcePaths:
    skill_dir = repo_root / "templates" / ".agents" / "skills" / "using-agents-stack"
    return GuardSourcePaths(
        skill_dir=skill_dir,
        verifier=skill_dir / "scripts" / "verify_retry_guard.py",
        eval_readme=skill_dir / "evals" / "README.md",
        fixtures=skill_dir / "evals" / "guard-eval-fixtures.md",
        orchestrator_reference=skill_dir / "references" / "orchestrator-worker.md",
        state_machine_reference=skill_dir / "references" / "state-machine.md",
        children_reference=skill_dir / "references" / "children.json",
    )


def string_literal(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def path_tail_literal(node: ast.AST) -> str | None:
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        return path_tail_literal(node.right) or path_tail_literal(node.left)
    return string_literal(node)


def extract_guard_script_summary(path: Path) -> GuardScriptSummary:
    module = ast.parse(read_text(path), filename=str(path))

    failed_phases: set[str] = set()
    deny_reasons: set[str] = set()
    required_status_fields: set[str] = set()
    tracked_work_fields: set[str] = set()
    evidence_files: set[str] = set()

    for node in ast.walk(module):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "FAILED_PHASES" and isinstance(node.value, ast.Set):
                    for item in node.value.elts:
                        value = string_literal(item)
                        if value:
                            failed_phases.add(value)

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                owner = node.func.value.id
                if owner == "reasons" and node.func.attr == "append" and node.args:
                    value = string_literal(node.args[0])
                    if value:
                        deny_reasons.add(value)
                if node.func.attr == "get" and node.args:
                    field = string_literal(node.args[0])
                    if not field:
                        continue
                    if owner == "status":
                        required_status_fields.add(field)
                    elif owner == "tracked_work":
                        tracked_work_fields.add(field)
                    elif owner == "backlog_entry":
                        tracked_work_fields.add(f"backlog[].{field}")

            if isinstance(node.func, ast.Name):
                if node.func.id == "require_int" and len(node.args) >= 2:
                    owner = node.args[0]
                    field = string_literal(node.args[1])
                    if isinstance(owner, ast.Name) and owner.id == "status" and field:
                        required_status_fields.add(field)
                    for reason_arg in node.args[2:4]:
                        reason = string_literal(reason_arg)
                        if reason:
                            deny_reasons.add(reason)
                elif node.func.id == "read_json" and len(node.args) >= 3:
                    for reason_arg in node.args[1:3]:
                        reason = string_literal(reason_arg)
                        if reason:
                            deny_reasons.add(reason)
                elif node.func.id == "read_required_text" and node.args:
                    filename = path_tail_literal(node.args[0])
                    if filename:
                        evidence_files.add(filename)
                    if len(node.args) >= 2:
                        reason = string_literal(node.args[1])
                        if reason:
                            deny_reasons.add(reason)

    return GuardScriptSummary(
        failed_phases=tuple(sorted(failed_phases)),
        deny_reasons=tuple(sorted(deny_reasons)),
        required_status_fields=tuple(sorted(required_status_fields)),
        tracked_work_fields=tuple(sorted(tracked_work_fields)),
        evidence_files=tuple(sorted(evidence_files)),
    )


FIXTURE_ID_PATTERN = re.compile(r"^- id: ([a-z0-9-]+)$", re.MULTILINE)
PHASE_GATE_PATTERN = re.compile(r"^\s*phase_or_artifact_gate: (.+)$", re.MULTILINE)


def extract_fixture_summary(path: Path) -> FixtureSummary:
    text = read_text(path)
    fixture_ids = tuple(FIXTURE_ID_PATTERN.findall(text))
    phase_gates = tuple(line.strip() for line in PHASE_GATE_PATTERN.findall(text))
    return FixtureSummary(
        fixture_ids=fixture_ids,
        phase_gates=phase_gates,
        mentions_build_failed="build_failed" in text,
        mentions_review_failed="review_failed" in text,
    )


def extract_reference_summary(path: Path, needle: str) -> ReferenceSummary:
    lines: list[str] = []
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if needle in raw_line or any(token in raw_line for token in ("attempt_count", "max_attempts", "clean_restore_ref", "build_failed", "review_failed", "awaiting_human", "escalated_to_human")):
            if line:
                lines.append(line)
    return ReferenceSummary(path=path, lines=tuple(lines))


def format_bullets(values: tuple[str, ...]) -> list[str]:
    return [f"- {value}" for value in values]


def synthesize_suggestions(script: GuardScriptSummary, fixtures: FixtureSummary) -> tuple[str, ...]:
    suggestions: list[str] = [
        "Keep any future compiler lane read-only and stdout-only; the current references already treat retry eligibility as hand-authored verdict-plus-reasons logic, not an installable policy source.",
        "Do not synthesize child routing decisions. The current sources keep `verify_retry_guard.py` bounded to allow/deny evidence while `children.json` and the references still own route selection.",
    ]

    if "build_failed" in script.failed_phases and not fixtures.mentions_build_failed:
        suggestions.append(
            "Add an explicit `build_failed` retry fixture before promoting synthesis beyond experiment status; the current fixture examples cover `review_failed` clean resume but not the sibling failed-phase lane."
        )

    if "review.md" in script.evidence_files and "runtime.md" in script.evidence_files:
        suggestions.append(
            "Preserve phase-specific evidence requirements in any future promotion. The existing verifier distinguishes `review_failed` via `review.md` and `build_failed` via `runtime.md`; a compiled guard must not flatten those into one generic failure shape."
        )

    return tuple(suggestions)


def render_report(paths: GuardSourcePaths) -> str:
    script_summary = extract_guard_script_summary(paths.verifier)
    fixture_summary = extract_fixture_summary(paths.fixtures)
    reference_summaries = [
        extract_reference_summary(paths.orchestrator_reference, "verify_retry_guard.py"),
        extract_reference_summary(paths.state_machine_reference, "verify_retry_guard.py"),
        extract_reference_summary(paths.children_reference, "verify_retry_guard.py"),
        extract_reference_summary(paths.eval_readme, "guard-eval-fixtures.md"),
    ]
    suggestions = synthesize_suggestions(script_summary, fixture_summary)

    sections: list[str] = [
        "# Advisory guard synthesis report",
        "",
        "This output is experimental and non-authoritative. It is a human-readable synthesis of the current hand-authored retry guard sources.",
        "",
        "## Inputs scanned",
        *format_bullets(
            (
                str(paths.verifier.relative_to(paths.skill_dir.parent.parent.parent.parent)),
                str(paths.orchestrator_reference.relative_to(paths.skill_dir.parent.parent.parent.parent)),
                str(paths.state_machine_reference.relative_to(paths.skill_dir.parent.parent.parent.parent)),
                str(paths.children_reference.relative_to(paths.skill_dir.parent.parent.parent.parent)),
                str(paths.fixtures.relative_to(paths.skill_dir.parent.parent.parent.parent)),
                str(paths.eval_readme.relative_to(paths.skill_dir.parent.parent.parent.parent)),
            )
        ),
        "",
        "## Observed retry-guard contract from `verify_retry_guard.py`",
        "### Failed phases handled",
        *format_bullets(script_summary.failed_phases),
        "",
        "### Required status fields",
        *format_bullets(script_summary.required_status_fields),
        "",
        "### Required tracked-work fields",
        *format_bullets(script_summary.tracked_work_fields),
        "",
        "### Phase-specific evidence files",
        *format_bullets(script_summary.evidence_files),
        "",
        "### Deny reasons emitted today",
        *format_bullets(script_summary.deny_reasons),
        "",
        "## Current reference alignment",
    ]

    for summary in reference_summaries:
        sections.append(f"### {summary.path.name}")
        if summary.lines:
            sections.extend(f"- {line}" for line in summary.lines)
        else:
            sections.append("- No matching retry-guard lines found.")
        sections.append("")

    sections.extend(
        [
            "## Guard-fixture coverage snapshot",
            "### Fixture ids present",
            *format_bullets(fixture_summary.fixture_ids),
            "",
            "### Phase gates present",
            *format_bullets(fixture_summary.phase_gates),
            "",
            f"- Mentions build_failed: {'yes' if fixture_summary.mentions_build_failed else 'no'}",
            f"- Mentions review_failed: {'yes' if fixture_summary.mentions_review_failed else 'no'}",
            "",
            "## Advisory suggestions",
            *format_bullets(suggestions),
        ]
    )

    return "\n".join(sections) + "\n"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    paths = resolve_paths(repo_root)

    try:
        report = render_report(paths)
    except (FileNotFoundError, SyntaxError, ValueError) as exc:
        return fail(str(exc))

    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
