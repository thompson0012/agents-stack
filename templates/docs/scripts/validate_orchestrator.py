#!/usr/bin/env python3
"""Regression check for canonical worker phase names in orchestrator dispatch."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory

CANONICAL_PHASES = {
    "adversarial-live-review",
    "evaluator-contract-review",
    "generator-execution",
    "generator-proposal",
}


def load_orchestrator():
    script_path = Path(__file__).with_name("orchestrator.py")
    spec = spec_from_file_location("templates_docs_scripts_orchestrator", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load orchestrator module from {script_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_case(name: str, result: tuple[str, str, str], expected_artifact: str, expected_phase: str) -> None:
    artifact, phase, message = result
    if artifact != expected_artifact or phase != expected_phase:
        raise AssertionError(
            f"{name}: expected ({expected_artifact!r}, {expected_phase!r}), got ({artifact!r}, {phase!r}); {message}"
        )
    if phase not in CANONICAL_PHASES:
        raise AssertionError(f"{name}: non-canonical worker phase returned: {phase!r}")


def run_case(orchestrator, *, previous_phase: str, status: dict[str, str], files: list[str], expected_artifact: str, expected_phase: str, name: str) -> None:
    with TemporaryDirectory() as tmpdir:
        sprint_dir = Path(tmpdir)
        for filename in files:
            (sprint_dir / filename).write_text(f"{filename}\n", encoding="utf-8")
        check_case(
            name,
            orchestrator.infer_timeout_resume_target(previous_phase, status, sprint_dir),
            expected_artifact,
            expected_phase,
        )


def main() -> int:
    orchestrator = load_orchestrator()

    run_case(
        orchestrator,
        previous_phase="in_review",
        status={},
        files=["handoff.md"],
        expected_artifact="handoff.md",
        expected_phase="adversarial-live-review",
        name="in_review",
    )
    run_case(
        orchestrator,
        previous_phase="executing",
        status={"review_status": "fail"},
        files=["review.md"],
        expected_artifact="review.md",
        expected_phase="generator-execution",
        name="review_failed",
    )
    run_case(
        orchestrator,
        previous_phase="executing",
        status={},
        files=["handoff.md"],
        expected_artifact="handoff.md",
        expected_phase="adversarial-live-review",
        name="handoff_present",
    )
    run_case(
        orchestrator,
        previous_phase="executing",
        status={},
        files=["contract.md"],
        expected_artifact="contract.md",
        expected_phase="generator-execution",
        name="contract_present",
    )
    run_case(
        orchestrator,
        previous_phase="executing",
        status={},
        files=["sprint_proposal.md"],
        expected_artifact="sprint_proposal.md",
        expected_phase="evaluator-contract-review",
        name="proposal_present",
    )
    run_case(
        orchestrator,
        previous_phase="executing",
        status={"resume_from": "status.json"},
        files=[],
        expected_artifact="status.json",
        expected_phase="generator-execution",
        name="fallback",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
