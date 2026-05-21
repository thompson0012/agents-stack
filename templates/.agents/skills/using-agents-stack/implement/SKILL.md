---
name: implement
description: TDD implementation per task. Each task passes before next. Produces handoff.md with reproducible evidence.
trigger: When tasks.md exists and handoff.md does not, or retry after Layer 1 rework.
inputs: [CONSTITUTION.md, spec.md, plan.md, tasks.md]
outputs: [code within task boundaries, .agents-stack/<id>/handoff.md, .agents-stack/<id>/status.json]
boundaries: Only files in tasks.md deliverables. Must not self-approve. Must record reproducible evidence.
---

# Implement Worker

Implement tasks from TASKS.md one by one using TDD. Each task must pass all its Verification Checkpoints before the next task begins.

## Entry Checks

Before touching code:
1. `tasks.md` exists with defined tasks
2. This workstream is the active one in `tracked-work.json`
3. If retrying: `attempt < max_attempts` and clean state available
4. **Generator ≠ Auditor**: if you previously executed `qa` for this workstream, STOP. The orchestrator must dispatch implement and qa as separate workers.
5. If any check fails: stop, record in `status.json`, hand back to orchestrator

## Task Status States

Track task status in TASKS.md with these markers:

- `[ ] pending` — not started
- `[→] in_progress` — actively working
- `[✅] done` — passed all verification checkpoints
- `[↩] reworking` — Layer 1: code fix in progress
- `[⚠️] needs_plan` — Layer 2: architecture/plan must change, STOP
- `[🚨] needs_spec` — Layer 3: requirement/spec must change, STOP

## Workflow

For each task in TASKS.md order:

1. Read task description with its 5-dimension verification metadata
2. Write failing test(s) matching the Verification Checkpoints
3. Implement the code to pass the tests
4. Run all checkpoints — must all pass
5. Mark task `[✅] done`
6. Commit or save state
7. Proceed to next task

On failure:
- If code error only → mark task `[↩] reworking`, fix, re-run checkpoints
- If architecture blocker → mark task `[⚠️] needs_plan`, stop, update status.json with blocked_reason
- If spec gap → mark task `[🚨] needs_spec`, stop, update status.json with blocked_reason

## Output: handoff.md

```markdown
# Handoff

## Summary
[What was built — brief]

## Acceptance Trace

### TASK-01: [name]
- Status: [PASS | FAIL]
- Evidence: [observed result]

### TASK-02: [name]
...

## Build/Startup Verification
- Build: [pass/fail]
- Start: [pass/fail]
- Core path exercised: [pass/fail]

## Known Issues
- [Warnings, limitations the QA worker should know]

## Rework Notes (if applicable)
- Prior failure: [what failed]
- What changed: [fix applied]
```

## Build/Startup Triage

Before writing handoff:
1. Build the project — does it compile?
2. Start the system — does it boot?
3. Exercise one basic path — does the core feature work?
4. If any step fails: record `build_failed`, do not write handoff as if succeeded

## Retry Discipline

- Increment `attempt` in `status.json` when starting a fresh attempt
- Restore clean state before re-implementing
- If `attempt >= max_attempts`: stop, set `phase: "escalated_to_human"`
- If build/startup fails: set `phase: "build_failed"`, preserve evidence

## Done

All tasks marked `[✅] done`. `handoff.md` exists with reproducible evidence. System builds, runs, and core path works.
