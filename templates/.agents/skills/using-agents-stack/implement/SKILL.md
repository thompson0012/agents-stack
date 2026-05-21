---
name: implement
description: RED-GREEN-REFACTOR implementation per task. Each task passes before next. Produces handoff.md with reproducible evidence.
trigger: When tasks.md exists and handoff.md does not, or retry after Layer 1 rework.
inputs: [CONSTITUTION.md, spec.md, plan.md, tasks.md]
outputs: [code within task boundaries, .agents-stack/<id>/handoff.md, .agents-stack/<id>/status.json]
boundaries: Only files in tasks.md deliverables. Must not self-approve. Must record reproducible evidence.
---

# Implement Worker

Implement tasks from TASKS.md one by one using the RED-GREEN-REFACTOR cycle. Each task must pass all its Verification Checkpoints before the next task begins.

## Entry Checks

Before touching ANY code, verify these gates. Each is a hard stop.

1. `tasks.md` exists with defined tasks
2. This workstream is the active one in `tracked-work.json`
3. If retrying: `attempt < max_attempts` and clean state available
4. **Generator ≠ Auditor**: if you previously executed `qa` for this workstream, STOP. The orchestrator must dispatch implement and qa as separate workers.
5. **Blocking gate check**: read `status.json.phase_gates.implement.entry_ok`. If not `true`:
   - Read `status.json.blocking_gate` to determine what's blocked
   - If the blocking gate is from an unfinished consistency check: run it now, clear gate if passed
   - If the blocking gate requires a prior phase rework (plan/spec): STOP, route back to orchestrator
   - You CANNOT start implementation while a blocking gate is set
6. **⛔ You are the IMPLEMENT WORKER, not the orchestrator.** If you are the orchestrator reading this (not a dispatched implementation agent), you must dispatch an implementation agent to do the implementation. See Routing Rules below.
8. **Test harness readiness**: Before starting the first implementation task (or after TASK-1 if it scaffolds infra), verify the test runner can execute and report results. Run `npm test -- --collect-only` or equivalent. If the test runner is broken, fix it before writing any implementation code. Do not write production code against a non-functional test runner.
9. **RED before GREEN per task**: Before writing implementation code for ANY task, the test file for that task must already exist with a *failing* test (RED phase). Verify by running the test — it must fail. No implementation code may be written before RED evidence exists. This is a hard gate per task, checked at each task's start.
10. If any check fails: stop, record in `status.json` with `blocking_gate` and `blocked_reason`, hand back to orchestrator

## Task Status States

Track task status in TASKS.md with these markers:

- `[ ] pending` — not started
- `[→] in_progress` — actively working
- `[✅] done` — passed all verification checkpoints
- `[↩] reworking` — Layer 1: code fix in progress
- `[⚠️] needs_plan` — Layer 2: architecture/plan must change, STOP
- `[🚨] needs_spec` — Layer 3: requirement/spec must change, STOP

## Routing Rules

**⛔ Orchestrator must not self-implement.** During the implement phase, the orchestrator's role is to dispatch and verify — not to write code. Follow this table without exception:

| Who | What they do | What they do NOT do |
|-----|-------------|---------------------|
| **Orchestrator** (you, if reading this) | Read `tasks.md` + `status.json`, dispatch implementation agent per task, dispatch review agent for review, update gates | Write implementation code, write tests, self-review |
| **Implementation agent** | Implement a single task: write test → write code → verify → handoff | Make architectural decisions, skip verification, modify scope |
| **Review agent** | Review handoff, verify execution path, produce review-verdict.md | Write code, modify tasks, skip adversarial analysis |

### When to dispatch implementation agent

Dispatch implementation agent when:
- A task is `pending` and its dependencies are met
- The task spec is well-defined by tasks.md (5-dimension verification is complete)
- You can give implementation agent: which task number, the full task definition from tasks.md, the files to read/write

Do NOT dispatch implementation agent when:
- The task spec is ambiguous (dispatch back to orchestrator → route to tasks phase)
- Multiple pending tasks share the same files (sequential dependency exists)
- You could do it in < 30 seconds (but ask: "Am about to violate my role?")

### When to dispatch review agent

Dispatch review agent when:
- A task's verification checkpoints are complete and you need adversarial review
- ALL tasks in a parallel group are `[✅] done` — before advancing to the next group
- The full implement phase is complete and handoff.md is drafted
- The previous implement attempt failed QA at L1 and you need root cause analysis

### When to dispatch yourself (orchestrator-as-doer)

Only when:
- Updating `status.json` gates
- Reading artifacts to determine next routing decision
- Consolidating results across workers
- The change is TRIVIAL: ≤ 5 lines, no branching, no new files, no test changes

## Workflow

Tasks execute ONE AT A TIME, in dependency order. No exceptions.

### Inter-Task Gate (Hard Stop)

**⛔ Before moving from task N to task N+1, ALL of these must be true:**

| Gate | Condition | How to verify |
|------|-----------|---------------|
| RED phase completed | Failing test written first, RED evidence recorded | `cat handoff.md` — task N section shows RED command + failing output |
| Task N tests pass | All tests for task N pass (RED→GREEN→REFACTOR complete) | `npm test` or equivalent |
| No regression | All prior task tests still pass | `npm test` (full suite) |
| 5-dimension verified | Import / unit / type / spec / edge — all checked | per task's Verification Checkpoints |
| handoff evidence | Task N's evidence recorded in handoff.md | handoff.md exists with task N section |
| status.json updated | `phase_gates.implement.current_task_verified` = true | read status.json |

If ANY gate is unmet, you CANNOT start task N+1. Fix the current task first.

If you attempt to start task N+1 with task N gates unmet, you are violating the process. Stop.

### Per-Group Execution

For each Parallel Group in dependency order:

1. Identify all tasks in the current group
2. Execute tasks within the group sequentially (one at a time — see Inter-Task Gate above):
   - For each task: read its 5-dimension verification metadata
   - For each task: write failing test(s) matching its Verification Checkpoints
   - For each task: implement the code to pass its tests
   - For each task: run all checkpoints — must all pass
   - For each task: gate check before next task
3. Once ALL tasks in the group pass and all inter-task gates are met: proceed to the next group

### Per-Task Within Group — RED-GREEN-REFACTOR Cycle

Each task follows exactly this 7-phase cycle. No phase can be skipped or merged. Each phase ends with a verifiable outcome.

#### Phase 1 — RED: Write a Failing Test
1. Read the task's 5-dimension verification metadata
2. Write test(s) that match the Verification Checkpoints
3. **Run the test(s) — they MUST fail.** If they pass, the test is invalid (either not testing the right thing, or the feature already exists)
4. If the test framework reports a runtime error (not a test failure), fix the test infrastructure first and repeat from step 2

#### Phase 2 — GREEN: Write Minimal Implementation
5. Write the minimum production code to make the failing test pass
   - Do NOT add code for edge cases not covered by tests
   - Do NOT add abstractions or patterns not required by current tests
   - Do NOT refactor during this phase — resist the urge
6. **Run the test(s) — they MUST pass.** If they fail, iterate on production code (not tests) and repeat step 6

#### Phase 3 — REFACTOR: Improve Without Changing Behavior
7. Refactor the implementation: improve naming, extract duplication, simplify logic
8. **Run ALL prior task tests + current task tests — they MUST all pass**
9. If any test breaks during refactoring, revert the refactoring attempt and retry with smaller, safer steps

#### Phase 4 — VERIFY: Run All Checkpoints (falsifiable)
10. Run every Verification Checkpoint from the task's metadata
11. Each checkpoint must produce observable evidence — not "looks correct" but actual command output, API response, or test result
12. If a checkpoint cannot produce falsifiable evidence (no way to make it fail), mark it as invalid and skip

#### Phase 5 — COMMIT: Lock the State
13. Mark task `[✅] done`
14. Commit or save state with a message referencing the task ID

#### Phase 6 — REGRESS: Verify No Regression
15. Run ALL completed task tests from this workstream (not just the current one)
16. All must pass — a regression means the current task broke prior work

#### Phase 7 — GATE: Lock the Inter-Task Gate
17. Update `status.json.phase_gates.implement.current_task` to the current task ID
18. Update `status.json.phase_gates.implement.current_task_verified` to `true`
19. Update `status.json.blocking_gate` to `null` (cleared — ready for next task)
20. **Only now may you start the next task**

#### Failure Handling at Each Phase

| Phase | Failure Mode | Action |
|-------|-------------|--------|
| RED step 3 | Test passes unexpectedly | The test is invalid — rewrite it to test the right condition |
| GREEN step 6 | Production code fails to pass | Iterate on production code only, do NOT modify the test |
| REFACTOR step 8-9 | Refactoring breaks existing tests | Revert refactoring — it was too aggressive |
| VERIFY step 11 | Checkpoint cannot produce evidence | Mark checkpoint as invalid, report to handoff's Known Issues |
| REGRESS step 16 | Prior task test fails | A prior task's behavior was broken — fix before continuing |
| Build/startup fails | Project doesn't compile or boot | Set `build_failed`, do NOT write handoff as passed |

Beyond code errors:
- **Architecture blocker** → mark task `[⚠️] needs_plan`, stop, update status.json with blocked_reason
- **Spec gap** → mark task `[🚨] needs_spec`, stop, update status.json with blocked_reason
- **Parallel group failure** → mark failed task `[↩] reworking`, fix it. Other tasks in the same group that depend on shared state unaffected by the failed task may continue. Tasks that share state with the failed task must pause and re-verify after the fix.

## Output: handoff.md

```markdown
# Handoff

## Summary
[What was built — brief]

## Acceptance Trace

### TASK-01: [name]
- Status: [PASS | FAIL]
- RED: [test command + output showing initial failure]
- GREEN: [test command + output showing pass after implementation]
- REFACTOR: [all prior + current tests pass output]
- REGRESS: [full suite test output]

### TASK-02: [name]
...

## Verification-Before-Completion Evidence

Each claim below is backed by a command executed in this session:

- Build: [exit code 0] — `npm run build` (or equivalent)
- All tests: [N passed, 0 failed] — `npm test`
- System start: [process alive, port listening] — `npm start` + `curl localhost:PORT`
- Core path: [end-to-end flow verified] — specific command + output
- Pre-handoff checklist: all items passed

## Known Issues
- [Warnings, limitations the QA worker should know]

## Deviations from Plan
- [What was done differently than plan.md specified, and why]

## Rework Notes (if applicable)
- Prior failure: [what failed]
- What changed: [fix applied]
```

## Verification-Before-Completion

You are about to claim the work is done. Before you write a single word of handoff.md, you must produce **evidence** — not assertions.

### Rules

1. **Evidence before assertion.** Every claim in handoff.md (task passed, build works, core path succeeds) must be backed by a command you actually ran in this session. Not "I could run it" — "I ran it and this is the output."
2. **Re-run, don't recall.** If you ran a test 10 minutes ago and made code changes since, re-run it now. Past results are invalidated by subsequent changes.
3. **No static claims.** "Build: pass" is not valid unless you just ran `npm run build` or equivalent. The exact command and its exit code are the evidence.
4. **Core path exercise is not optional.** If the system starts, you must verify at least one user-facing path end-to-end — not just that the server boots.
5. **If a checkpoint cannot be executed** (missing dependency, environment constraint), record it in Known Issues with the reason. Do not mark it as pass by assumption.

### Pre-Handoff Checklist

Before writing handoff.md, complete this checklist. Each item requires an actual command execution:

- [ ] `npm run build` (or equivalent) — exits 0
- [ ] `npm test` (or equivalent) — all tests pass
- [ ] System starts without crash — process stays alive
- [ ] Core feature path exercised — one end-to-end flow verified
- [ ] All task checkpoints re-verified with CURRENT state (not cached results)
- [ ] `decisions.md` updated with any deviations from plan

If any item fails: fix it first, re-run the chain, only then write handoff.

### Invalid Evidence (do not accept from yourself)

The following are NOT evidence:
- "I ran it earlier and it worked" — time decay invalidates this
- "It should work because X" — should is not evidence
- Static screenshots without before/action/after — could be hardcoded
- "All tests pass" without showing the actual test command and output
- Claims that cannot be falsified — "the system is stable" without defining what "unstable" looks like

## Integration Gate (Cross-Module Wiring Check)

Before dispatching the independent review agent, run a wiring integrity check against the plan.

### Why

Sequential phase plans naturally produce isolated modules that pass unit tests but are never connected. The most common failure pattern in multi-module workstreams is **zero production callers** — functions with full docstrings, type annotations, and passing unit tests that are never wired into the execution path.

### Gate: Call-Graph Scan

For every function or method that is part of the task's public API (defined in tasks.md deliverables), verify it has at least one production caller outside of tests:

```
# List all public API functions in the deliverables
# For each: check for non-test callers
rg "def ASSEMBLE_PROMPT\(" --type py          # identify the function
rg "assemble_prompt\(" --type py --glob '!tests/**'  # check production callers
```

| Condition | Action |
|-----------|--------|
| 0 production callers | **BLOCKED** — the function exists but is dead code. Add a wiring task or remove it. |
| 1+ production callers | PASS — continue |
| No public API to check (pure internal refactor) | SKIP — no wiring needed |

### Gate: Cross-Module Interface Check

For every cross-module interface declared in plan.md (imports, registrations, callbacks, dependency injections, data flow paths):

```
# Example: if plan says "agent.run calls guard.evaluate"
rg "from arc\.guard import" --type py  # verify the import exists
rg "evaluate\(" --type py --glob '!tests/**'  # verify the call happens in production
```

Cross-module interfaces include:
- Imports from one module into another
- Registration calls (hooks, tools, handlers)
- Callback functions passed across module boundaries
- Dependency injection wiring (if not using a DI framework, the explicit instantiation)

| Condition | Action |
|-----------|--------|
| All interfaces from plan have production code wiring | PASS |
| Any interface from plan has no production wiring | **BLOCKED** — create a task to wire it or update plan if intentionally removed |

### Results Go Into Handoff

Record the integration gate results in handoff.md under a dedicated section:

```markdown
## Integration Gate Results
- Zero-caller scan: [PASS | BLOCKED — list flagged functions]
- Cross-module interface check: [PASS | BLOCKED — list missing interfaces]
```

This ensures qa can see the wiring check was performed, even if it was skipped.

## Independent Review Gate (Before Handoff Finalization)

Before you write handoff.md as final, you must dispatch review agent for independent review.

### Why

- **Generator ≠ Auditor.** You cannot self-review your own implementation — you will only see what you already understand. The review agent will find gaps in execution paths, missing edge cases, and architectural drift that you miss.
- The 60% stub problem (code structure correct but execution paths incomplete) is invisible to self-review.

### Gate

- [ ] All tasks marked `[✅] done`
- [ ] All inter-task gates passed
- [ ] review agent dispatched with: full task list, current code state, handoff draft
- [ ] `review-verdict.md` exists with result
- [ ] review agent verdict is **PASS** — no P0/P1 gaps found
- [ ] If review agent found gaps: fix ALL gaps, re-run verification chain, re-dispatch review agent
- [ ] `status.json.phase_gates.implement.review_approved` = `true`
- [ ] `status.json.blocking_gate` = `null`

**You CANNOT finalize handoff.md without a PASS from review agent.** This is a hard gate.

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
- If build/startup fails: set `phase: "implement_failed"`, preserve evidence

## Done

All tasks marked `[✅] done`. `handoff.md` exists with reproducible evidence. System builds, runs, and core path works.

Before declaring implement phase complete, verify ALL gates:

| Gate | Condition | Status |
|------|-----------|--------|
| All tasks verified | Every task passed RED→GREEN→REFACTOR→VERIFY→REGRESS | ☐ |
| No blocking gate | `status.json.blocking_gate` is null | ☐ |
| Handoff written | `handoff.md` exists with reproducible evidence per task | ☐ |
| Review approved | `status.json.phase_gates.implement.review_approved` = true | ☐ |
| Phase gate updated | `status.json.phase_gates.implement.handoff_written` = true | ☐ |

If any gate is unmet, the implement phase is NOT done. Fix the gate before declaring completion.
