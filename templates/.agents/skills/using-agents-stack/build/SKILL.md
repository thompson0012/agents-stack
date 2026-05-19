---
name: build
description: Implement the approved contract, producing code changes and a handoff for independent audit.
trigger: When contract.md exists and handoff.md does not, or retry after build_failed/review_failed.
inputs: [AGENTS.md, plan.md, contract.md, tracked-work.json, docs/reference/*]
outputs: [code within contract bounds, .harness/<id>/handoff.md, .harness/<id>/status.json]
boundaries: Only files in contract.md. Must not self-approve. Must record reproducible evidence.
---

# Build Worker

Implement exactly what the contract specifies. No more, no less. Record evidence so an independent auditor can reproduce and verify.

## Entry Checks

Before touching code:
1. `contract.md` exists and defines allowed files
2. This workstream is the active one in `tracked-work.json`
3. If retrying: `attempt < max_attempts` and `clean_restore_ref` exists
4. Generator ≠ Auditor: if you previously executed `audit` for this workstream, STOP. The orchestrator must dispatch build and audit as separate workers.
5. If any check fails: stop, record in `status.json`, hand back to orchestrator

## Input

The orchestrator provides inline context digest covering: plan objective, contract scope and ACs, harness rules. Read from disk only if the inline digest is insufficient. Actual code must be read from disk — inline context cannot replace inspecting real source.

### Required Reads (fallback)

- `docs/live/plan.md`
- `.harness/<id>/contract.md`
- `docs/reference/*` for project context
- Actual code in all areas to be modified

## Output: handoff.md

```markdown
# Handoff

## Summary
[What was built — brief]

## Reproduction Steps
[Exact commands to build, start, and reach the feature]
```bash
# Build
npm run build

# Start
npm run dev

# Verify
curl http://localhost:3000/api/...
```

## Acceptance Trace

### AC-001
- Status: [PASS | FAIL]
- Evidence: [what was observed]
- [For stateful: before → action → after]

### AC-002
...

## Known Issues
- [Warnings, limitations the auditor should know]

## Retry Notes (if applicable)
- Prior failure: [what failed]
- What changed: [fix applied]
- Restore ref: [clean_restore_ref]
```

## Retry Discipline

- Increment `attempt` in `status.json` when starting a fresh attempt
- Restore from `clean_restore_ref` before implementing
- If `attempt >= max_attempts`: stop, set `phase: "escalated_to_human"`
- If build/startup fails: set `phase: "build_failed"`, preserve evidence

## Build/Startup Triage

Before writing handoff:
1. Build the project — does it compile?
2. Start the system — does it boot?
3. Exercise one basic path — does the core feature work?
4. If any step fails: record `build_failed`, do not write handoff as if succeeded

## Workflow

1. Verify contract and entry conditions
2. Restore clean workspace if retrying
3. Implement within allowed files only
4. Build/startup triage
5. Record all evidence in `handoff.md`
6. Update `status.json`: `phase: "build"` or `"build_failed"`

## Done

`handoff.md` exists with reproducible evidence. System builds, runs, and core path works.
