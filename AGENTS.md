# AGENTS.md

This repository uses agents-stack v3 — a Goal-QA-Driven development harness.

## Key Paths

- .agents-stack/<ID>/ — workstream artifacts (spec.md, plan.md, tasks.md, handoff.md, qa-report.md, changelog.md, status.json)
- .agents-stack/tracked-work.json — active/parked workstream registry
- .agents-stack/reference/ — project knowledge (architecture.md, design.md)
- .agents/skills/using-agents-stack/ — router SKILL.md and phase SKILL.md files

## Pipeline

spec → plan → tasks → implement → qa → release

| Phase | Output | Purpose |
|-------|--------|---------|
| spec | spec.md | What & Why: goal, stories, edge cases, BDD ACs |
| plan | plan.md | How: architecture, API, DB, impact analysis, test strategy |
| tasks | tasks.md | Task breakdown with 5-dimension verification |
| implement | code + handoff.md | TDD per task, each passes before next |
| qa | qa-report.md | Independent verification against SPEC |
| release | changelog.md | Changelog, reference update, archive |

## Core Invariants

1. Files beat chat memory
2. One active workstream
3. Implementer ≠ Verifier (Generator ≠ Auditor)
4. Cold start must work
5. Iteration ≠ Retry

## Quick Resume

1. Read CONSTITUTION.md, AGENTS.md, .agents-stack/tracked-work.json
2. Read .agents-stack/<ID>/status.json and strongest artifact
3. Verify checkpoint matches disk state, continue from strongest valid checkpoint

Success: a cold-start agent can read these files and continue safely without chat history.
