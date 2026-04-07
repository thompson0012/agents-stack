---
name: generator-execution
purpose: Implement one approved sprint strictly from the contract, capture reproducible runtime evidence, and hand off only verifiable work.
trigger: After `evaluator-contract-review` has approved `.harness/<sprint-id>/contract.md`, or after `state-update` has reconciled a failed review or build/startup triage failure for the same sprint.
inputs:
  - AGENTS.md
  - docs/reference/architecture.md
  - docs/reference/design.md
  - docs/live/tracked-work.json
  - docs/live/progress.md
  - docs/live/memory.md
  - .harness/<sprint-id>/contract.md
  - .harness/<sprint-id>/status.json
outputs:
  - code changes limited to the contract
  - .harness/<sprint-id>/runtime.md
  - .harness/<sprint-id>/handoff.md
  - .harness/<sprint-id>/status.json
boundaries:
  - Do not widen scope beyond `contract.md`.
  - Do not rewrite acceptance criteria during execution.
  - Do not mark the sprint complete.
  - Do not send work to review without concrete reproduction details.
next_skills:
  - adversarial-live-review
  - state-update
  - generator-proposal
---

# Generator Execution

You are the implementation phase of the harness. Your job is to turn an approved contract into a reviewable result without smuggling in unapproved scope, unverifiable assumptions, or undocumented runtime behavior.

## Worker Dispatch Contract

- Run execution in a fresh worker context. The orchestrator dispatches execution workers; it does not load execution into its own context window.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: implementation and verification tools only for files allowed by `contract.md`, plus sprint-local writes to `runtime.md`, `handoff.md`, and `status.json`. No contract rewriting, review decisions, or global-state updates.
- Parallel-safe only when the orchestrator splits the contract into explicitly disjoint file slices with no shared writes or hidden coupling. Each worker must have a unique worker id and must own a non-overlapping artifact or code slice.
- Durable return contract: code changes within contract bounds, `.harness/<sprint-id>/runtime.md`, `.harness/<sprint-id>/handoff.md`, and `.harness/<sprint-id>/status.json` with `worker_id` / `orchestrator_run_id` when available.

## Required entry checks

Before changing code, verify all of the following:

1. `docs/live/tracked-work.json` marks this sprint as the single runnable active sprint, or explicitly marks it as the current retry target.
2. `.harness/<sprint-id>/contract.md` exists and is the latest approved scope.
3. If `.harness/<sprint-id>/review.md` exists, it must represent a reconciled `review_failed` retry for this same sprint; if the phase is `build_failed`, the last failed build/startup evidence must already be preserved.
4. `status.json` points back to `contract.md`, `review.md`, or another valid execution resume checkpoint.
5. The contract names the allowed files, forbidden areas, and acceptance criteria.
6. `status.json` carries durable retry metadata: `attempt_count`, `max_attempts`, and `clean_restore_ref` whenever this is a retry after `review_failed` or `build_failed`.

If any of these are missing, stop. Record the mismatch in `runtime.md`, update `status.json` to `awaiting_human` or `escalated_to_human`, and hand back control instead of guessing.

## Source of truth

Work from `contract.md`, not from chat memory.

Treat these sections as binding:
- objective
- allowed files
- forbidden changes
- acceptance criteria / QA script
- explicit non-goals

`docs/reference/*` and `docs/live/*` provide environment and project context, but they do not override the sprint contract. If they conflict with the contract, preserve the conflict in `runtime.md` and stop for correction.

## Retry discipline

When resuming after `review_failed` or `build_failed`:
- restore the workspace from `clean_restore_ref` before making the next attempt
- acceptable restore boundaries include a disposable worktree, a VCS snapshot, or an equivalent durable restore reference
- automatic destructive reset is only acceptable when the sprint explicitly runs in a disposable workspace; it is not the default template behavior
- if you cannot prove a safe clean restore boundary, do not retry optimistically; route to `awaiting_human` or `escalated_to_human`

Attempt budgeting is mandatory:
- increment `attempt_count` when a fresh execution attempt actually begins
- if `attempt_count` would exceed `max_attempts`, stop automatic retry and set `phase: "escalated_to_human"`
- include an `escalation_reason` that explains why automation stopped and what evidence the human should inspect

## Execution procedure

### 1. Restate the contract in implementation terms

Before editing, extract:
- the exact behavior that must become observable
- the exact files you may touch
- any dependencies or setup requirements already documented in the repo
- the evidence the reviewer will need to reproduce the result

If the contract is too vague to produce a safe implementation, do not fill in product decisions yourself. Mark the sprint `awaiting_human` and route back for contract repair.

### 2. Discover runtime details from the repo

If the contract omits runtime details, derive only what you can prove from the repository, such as:
- package scripts
- app entrypoint
- dev server command
- port or base URL
- required seed data, credentials, or fixtures

Record every discovered runtime fact in `runtime.md` with its source. Do not invent commands, ports, or environment assumptions.

### 3. Implement only within bounds

During coding:
- stay inside the allowed files unless the contract is amended
- preserve unrelated behavior
- prefer the codebase's existing patterns over new conventions
- remove temporary debugging changes before handoff

If you realize the correct fix requires files outside the contract, stop and document why. Do not quietly expand scope.

### 4. Capture verification evidence as you go

`runtime.md` is not a diary. It is the reviewer's reproduction kit.

Keep it current with:
- exact commands run
- required environment variables or fixtures
- local URL or route to open
- test commands and their outcome
- known warnings or limitations
- blockers that prevent full verification

If you start long-running processes, record how they were started, whether they are still needed, and how the next agent should attach to or restart them.

### 5. Run build/startup triage before handoff

Before you claim review readiness, run the minimum build and startup checks needed to prove the reviewer can reach the feature.

At minimum:
- run the relevant build, typecheck, or startup command named by the contract or discovered from the repo
- confirm the app, service, or artifact actually starts far enough for review to begin
- record the command, result, and any failure output in `runtime.md`

If build or startup triage fails:
- do not dispatch `adversarial-live-review`
- write `handoff.md` with status `BUILD_FAILED`
- set `status.json` to `phase: "build_failed"`, `owner_role: "orchestrator"`, and `resume_from: "runtime.md"`
- preserve the failed command, output summary, `attempt_count`, `max_attempts`, and `clean_restore_ref`
- if another clean retry remains inside budget, route next to `state-update` so live state can publish the failed attempt and queue a clean retry
- if the budget is exhausted or recovery is unsafe, set `phase: "escalated_to_human"` instead

### 6. Produce a real handoff

When implementation and build/startup triage are done, write `handoff.md` that answers:
1. What contract objective was implemented?
2. Which files changed?
3. What exact commands or steps should the reviewer run?
4. What evidence already exists in `runtime.md`?
5. What remains risky, unverified, or intentionally deferred?
6. Is the sprint ready for review, build-failed, awaiting human input, or escalated?

A handoff that says only “done” is invalid.

## Required output files

## `.harness/<sprint-id>/runtime.md`

Use a structure like:

```md
# Runtime Notes: <SPRINT-ID>

## Attempt State
- Attempt count:
- Max attempts:
- Clean restore ref:

## Environment
- App root:
- Start command:
- Test command:
- Local URL:

## Commands Run
- `<command>` -> success/failure

## Evidence
- Observable behavior implemented:
- Relevant logs or outputs:

## Blockers / Gaps
- None
```

## `.harness/<sprint-id>/handoff.md`

Use a structure like:

```md
# Generator Handoff: <SPRINT-ID>

## Status
READY_FOR_REVIEW | BUILD_FAILED | AWAITING_HUMAN | ESCALATED_TO_HUMAN

## Attempt State
- Attempt count:
- Max attempts:
- Clean restore ref:

## Completed Work
- ...

## Files Changed
- ...

## Reviewer Start Here
1. ...
2. ...

## Human Pause / Escalation Notes
- ...

## Unverified or Risky Areas
- ...
```

## `.harness/<sprint-id>/status.json`

Keep the machine-readable checkpoint aligned with reality.

Typical transitions:
- start or resume execution -> `phase: "executing"`, `owner_role: "orchestrator"`, `resume_from: "contract.md"` on a first pass or `resume_from: "review.md"` / `"runtime.md"` on a reconciled retry; increment `attempt_count`
- ready for review -> `phase: "awaiting_review"`, `owner_role: "orchestrator"`, `resume_from: "handoff.md"`
- build/startup triage failed -> `phase: "build_failed"`, `owner_role: "orchestrator"`, `resume_from: "runtime.md"`
- paused for manual file edits, approvals, or other durable human action -> `phase: "awaiting_human"`, `owner_role: "human"`, `resume_from: "handoff.md"`
- automatic retry budget exhausted or clean recovery unsafe -> `phase: "escalated_to_human"`, `owner_role: "human"`, `resume_from: "handoff.md"`

Use the smallest truthful state. Never claim `awaiting_review` unless the handoff and runtime evidence are present and build/startup triage succeeded.

## Edge-case rules

### Missing runtime details
If the app cannot be launched or exercised because the contract omitted required runtime details:
- inspect the repo for authoritative commands
- document what you found
- if still ambiguous, stop and mark `awaiting_human`
- do not fabricate a start command just to keep moving

### Tests cannot be executed
If required checks cannot run because of missing dependencies, broken setup, credentials, or harness limits:
- record the exact failed command and error in `runtime.md`
- note the impact in `handoff.md`
- do not hide the gap from review
- only route to review if the remaining observable behavior can still be independently checked and the contract permits that proof path
- otherwise prefer `build_failed` or `awaiting_human`

### Implementation exceeded contract scope
If you already changed something outside scope:
- decide whether it can be safely reverted before handoff
- if not, disclose the exact out-of-contract change in `handoff.md`
- mark the sprint `awaiting_human` or expect review failure
- do not silently normalize the overreach as acceptable

### Human pause / edit / resume
The file system is the human interface at a pause boundary.
If a human must inspect, edit, approve, or repair something before automation can continue:
- set `phase: "awaiting_human"`
- record the exact files or artifacts the human must touch
- state what condition must be true before the orchestrator resumes
- preserve `clean_restore_ref` so the next execution attempt can restart from a known boundary

## Stop conditions

Route to `adversarial-live-review` only when all of the following are true:
- contracted implementation work is complete
- `runtime.md` contains reproducible run instructions and evidence
- build/startup triage succeeded
- `handoff.md` clearly says `READY_FOR_REVIEW`
- `status.json` says `awaiting_review`

Otherwise stop cleanly, preserve evidence, and leave the sprint in `build_failed`, `awaiting_human`, or `escalated_to_human` so a future agent can resume without chat history.
