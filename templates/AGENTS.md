# AGENTS.md

This repository uses agents-stack v3 — a Goal-QA-Driven development harness.

## Key Paths

- .agents-stack/<ID>/ — workstream artifacts (spec.md, plan.md, tasks.md, handoff.md, qa-report.md, changelog.md, status.json)
- .agents-stack/tracked-work.json — active/parked workstream registry
- .agents-stack/reference/ — project knowledge (architecture.md, design.md)
- .agents/skills/using-agents-stack/ — router SKILL.md and phase SKILL.md files

## Pipeline

spec → plan → tasks → implement → [integration gate] → qa → release

Each phase has a corresponding SKILL.md in `.agents/skills/using-agents-stack/<phase>/SKILL.md` — **load it before executing the phase.** The skill defines the phase contract, output format, verification gates, and handoff protocol. Skipping the skill = working without the spec.

| Phase | Skill Location | Output | Purpose |
|-------|---------------|--------|---------|
| spec | `using-agents-stack/spec/SKILL.md` | spec.md | What & Why: goal, stories, edge cases, BDD ACs |
| plan | `using-agents-stack/plan/SKILL.md` | plan.md | How: architecture, API, DB, impact analysis, test strategy |
| tasks | `using-agents-stack/tasks/SKILL.md` | tasks.md | Task breakdown with 5-dimension verification |
| implement | `using-agents-stack/implement/SKILL.md` | code + handoff.md | RED-GREEN-REFACTOR per task, each passes before next |
| integration gate | *(gate check in implement/SKILL.md)* | Zero-caller scan + cross-module wiring verification before QA |
| qa | `using-agents-stack/qa/SKILL.md` | qa-report.md | Independent verification against SPEC (fresh session required) |
| release | `using-agents-stack/release/SKILL.md` | changelog.md | Changelog, reference update, archive |

## Core Invariants

1. Files beat chat memory
2. One active workstream
3. Implementer ≠ Verifier (Generator ≠ Auditor)
4. Cold start must work
5. Iteration ≠ Retry

## Quick Resume

1. Read CONSTITUTION.md, AGENTS.md, .agents-stack/tracked-work.json
2. Read .agents-stack/<ID>/status.json and strongest artifact
3. Load the corresponding phase SKILL.md from `.agents/skills/using-agents-stack/<phase>/SKILL.md`
4. Verify checkpoint matches disk state, continue from strongest valid checkpoint

Success: a cold-start agent can read these files and continue safely without chat history.

## Contextual Skill Resolver

When the user expresses intent through natural language, map to the appropriate phase or skill. This enables NL-driven routing without requiring manual workstream creation:

| User Intent | Route To | Action |
|-------------|----------|--------|
| "spec this" / "think through this" | spec phase | Start or resume workstream, route to spec |
| "design the system" / "architecture" | plan phase | Ensure spec.md exists, route to plan |
| "break this down" / "task list" | tasks phase | Ensure plan.md exists, route to tasks |
| "implement this" / "code it" | implement phase | Ensure tasks.md exists, route to implement |
| "QA this" / "verify" / "test" | qa phase | Ensure handoff.md exists, route to qa |
| "release" / "ship it" | release phase | Ensure qa-report.md PASS, route to release |
| "code review" | agentic-engineering-principles | Load domain skill directly |
| "browser test" / "UI check" | frontend-qa | Load domain skill directly |
| "design review" / "UI/UX" | frontend-design | Load domain skill directly |
| "complexity audit" / "prune" | prune-review | Dispatch prune-review specialist |
| (fallback — general development) | using-agents-stack | Normal pipeline dispatch
