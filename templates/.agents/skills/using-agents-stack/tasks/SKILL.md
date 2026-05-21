---
name: tasks
description: Break plan into minimal verifiable tasks with 5-dimension verification metadata.
trigger: When plan.md exists and tasks.md does not.
inputs: [spec.md, plan.md]
outputs: [.agents-stack/<id>/tasks.md, .agents-stack/<id>/status.json]
boundaries: Task breakdown only. No implementation. No design changes.
---

# Tasks Worker

Decompose the plan into a strictly ordered sequence of verifiable tasks. Each task is a self-contained unit with embedded 5-dimension verification. This document is the execution script for the implement phase.

## Output Template: tasks.md

```markdown
# Tasks: [Brief Title]

**Workstream ID:** `<id>`
**Plan Referenced:** [date or version]
**Total Tasks:** `<N>`
**Execution Order:** Strictly sequential — each task depends on the prior.

---

## TASK-1: Scaffold Test Infrastructure

**Depends On:** None (first task)

### 1. Align Spec
- SPEC.md — overall quality bar: all ACs must be testable

### 2. Coverage Checklist
- [ ] Test framework configured and running
- [ ] Test database/seeding utilities in place
- [ ] CI-compatible test runner command exists (e.g., `npm test`)
- [ ] Fixture/mock helpers scaffolded for core entities

### 3. Deliverables
- Test configuration files — ensure test runner passes (even with no tests)
- Test utility helpers — factories, seeders, cleanup routines

### 4. Verification Checkpoints
- [ ] `npm test` runs and exits 0 (no tests is fine, no errors)
- [ ] Test DB can be created, migrated, seeded, and torn down
- [ ] Coverage tool configured and reporting

### 5. Definition of Done
- Coverage ≥ 80%, all checkpoints green
- Test infrastructure ready for TDD workflow

---

## TASK-N: [Task Name]

**Depends On:** TASK-(N-1)

### 1. Align Spec
- SPEC.md §X — [specific requirement reference]
- AC-00X — [acceptance criterion this task satisfies]

### 2. Coverage Checklist
- [ ] [Test scenario that must be covered]
- [ ] [Test scenario that must be covered]

### 3. Deliverables
- `path/to/file.ts` — [what this file adds/changes]
- `path/to/test.ts` — [corresponding test file]

### 4. Verification Checkpoints
- [ ] [Observable command or condition to verify]
- [ ] [Observable command or condition to verify]

### 5. Definition of Done
- Coverage ≥ 80% for files in this task
- All checkpoints green
- Task-N tests pass alongside all prior task tests (no regressions)
```

## Workflow

1. Read `spec.md` — understand user stories, edge cases, and acceptance criteria
2. Read `plan.md` — understand architecture, files to touch, and test strategy
3. Break the plan into strictly sequential tasks
4. Verify sequential dependencies — each task builds on the prior, no parallel tasks
5. For every task, complete all five dimensions of verification:
   - **1. Align Spec** — trace to specific ACs and spec sections
   - **2. Coverage Checklist** — what test scenarios are required
   - **3. Deliverables** — exact file paths from plan.md impact analysis
   - **4. Verification Checkpoints** — observable pass/fail commands
   - **5. Definition of Done** — coverage threshold ≥ 80%, all checkpoints green
6. Write `tasks.md` to `.agents-stack/<id>/tasks.md`
7. Update `status.json`: set `phase: "tasks"`

## Quality Bar

- Tasks are strictly sequential — no two tasks can run in parallel
- Each task is small enough to complete in one AI session
- TASK-1 is always scaffold test infrastructure
- Every task has all five verification dimensions filled in
- Coverage checklist maps to test strategy from plan.md
- If a task cannot be made verifiable, the plan is insufficient — flag it

## Done

`tasks.md` exists with strictly sequential tasks, each having complete 5-dimension verification metadata. First task is scaffold test infrastructure. `status.json` reflects tasks phase.
