# AGENTS.md

This repository uses agents-stack v3 — a Goal-QA-Driven development harness.

## Key Paths

- .agents-stack/<ID>/ — workstream artifacts (spec.md, plan.md, tasks.md, report.md, handoff.md, qa-report.md, changelog.md, status.json)
- .agents-stack/tracked-work.json — active/parked workstream registry
- .agents-stack/reference/ — project knowledge (architecture.md, design.md)
- .agents/skills/using-agents-stack/ — router SKILL.md and phase SKILL.md files

## Pipeline

spec → plan → tasks → analyze → implement → qa → release

Each phase has a corresponding SKILL.md in `.agents/skills/using-agents-stack/<phase>/SKILL.md` — **load it before executing the phase.** The skill defines the phase contract, output format, verification gates, and handoff protocol. Skipping the skill = working without the spec.

| Phase | Skill Location | Output | Purpose |
|-------|---------------|--------|---------|
| spec | `using-agents-stack/spec/SKILL.md` | spec.md | What & Why: goal, stories, edge cases, BDD ACs |
| plan | `using-agents-stack/plan/SKILL.md` | plan.md | How: architecture, API, DB, impact analysis, test strategy |
| tasks | `using-agents-stack/tasks/SKILL.md` | tasks.md | Task breakdown with 5-dimension verification |
| analyze | `using-agents-stack/analyze/SKILL.md` | report.md | Pre-implementation alignment gate: spec×plan×tasks consistency + plan vs codebase reality |
| implement | `using-agents-stack/implement/SKILL.md` | code + handoff.md | RED-GREEN-REFACTOR per task, each passes before next |
| qa | `using-agents-stack/qa/SKILL.md` | qa-report.md | Independent verification against SPEC |
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

Single source of truth for routing user intent. Check this table on every message before falling back to artifact-driven routing:

| User Intent | Route To | Action |
|-------------|----------|--------|
| **Pipeline phase** — "spec this" / "think through this" / "plan the architecture" / "design the system" / "break this down" / "task list" / "analyze this" / "对齐检查" / "implement this" / "code it" / "QA this" / "verify" / "test" / "release" / "ship it" | `using-agents-stack` | Load orchestrator; it routes to the correct phase based on artifact state |
| **Active workstream** — `.agents-stack/tracked-work.json` has active entry + development intent | `using-agents-stack` | Resume workstream from strongest checkpoint |
| **Code review** — "code review" / "review this code" / "幫我 review" | `agentic-engineering-principles` | Direct skill dispatch |
| **Frontend QA** — "browser test" / "UI check" / "check frontend" | `frontend-qa` | Direct skill dispatch |
| **Frontend design** — "design review" / "UI/UX" / "design this" | `frontend-design` | Direct skill dispatch |
| **Complexity audit** — "complexity audit" / "prune" / "over-engineered" | `prune-review` | Dispatch prune-review specialist |
| **Reflect/learn** — "remember this" / "log this error" / "show past learnings" | `reflect` | Record or query learnings |
| **Ad-hoc development** (one-off bugfix, feature, refactor, question, exploration — no workstream context) | **Direct execution** | No pipeline routing. Implement directly or load domain skill. |
