---
name: generator-execution
purpose: Implement one approved sprint strictly from the contract, capture reproducible runtime evidence, and hand off only verifiable work.
trigger: After `evaluator-contract-review` has approved `.harness/<sprint-id>/contract.md`, or after `state-update` has reconciled a failed review into `review_failed` for the same sprint.
inputs:
  - AGENTS.md
  - docs/reference/architecture.md
  - docs/reference/design.md
  - docs/live/features.json
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

1. `docs/live/features.json` marks exactly one feature as active for this sprint.
2. `.harness/<sprint-id>/contract.md` exists and is the latest approved scope.
3. If `.harness/<sprint-id>/review.md` exists, it must represent a reconciled `review_failed` retry for this same sprint; otherwise execution is not the correct next owner.
4. `status.json` points back to `contract.md`, `review.md`, or another valid execution resume checkpoint.
5. The contract names the allowed files, forbidden areas, and acceptance criteria.

If any of these are missing, stop. Record the mismatch in `runtime.md`, update `status.json` to a blocked or paused phase, and hand back control instead of guessing.

## Source of truth

Work from `contract.md`, not from chat memory.

Treat these sections as binding:
- objective
- allowed files
- forbidden changes
- acceptance criteria / QA script
- explicit non-goals

`docs/reference/*` and `docs/live/*` provide environment and project context, but they do not override the sprint contract. If they conflict with the contract, preserve the conflict in `runtime.md` and stop for correction.

## Execution procedure

### 1. Restate the contract in implementation terms

Before editing, extract:
- the exact behavior that must become observable
- the exact files you may touch
- any dependencies or setup requirements already documented in the repo
- the evidence the reviewer will need to reproduce the result

If the contract is too vague to produce a safe implementation, do not fill in product decisions yourself. Mark the sprint blocked and route back for contract repair.

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

### 5. Produce a real handoff

When implementation is done, write `handoff.md` that answers:
1. What contract objective was implemented?
2. Which files changed?
3. What exact commands or steps should the reviewer run?
4. What evidence already exists in `runtime.md`?
5. What remains risky, unverified, or intentionally deferred?
6. Is the sprint ready for review, or blocked?

A handoff that says only “done” is invalid.

## Required output files

## `.harness/<sprint-id>/runtime.md`

Use a structure like:

```md
# Runtime Notes: <SPRINT-ID>

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
READY_FOR_REVIEW | BLOCKED

## Completed Work
- ...

## Files Changed
- ...

## Reviewer Start Here
1. ...
2. ...

## Unverified or Risky Areas
- ...
```

## `.harness/<sprint-id>/status.json`

Keep the machine-readable checkpoint aligned with reality.

Typical transitions:
- start or resume execution -> `phase: "executing"`, `owner_role: "orchestrator"`, `resume_from: "contract.md"` on a first pass or `resume_from: "review.md"` on a reconciled retry
- ready for review -> `phase: "awaiting_review"`, `owner_role: "orchestrator"`, `resume_from: "handoff.md"`
- blocked during execution -> `phase: "blocked"`, `owner_role: "orchestrator"`, `resume_from: "runtime.md"`
- paused by interruption -> `phase: "paused_by_timeout"`, `owner_role: "orchestrator"`, `resume_from: "runtime.md"`

Use the smallest truthful state. Never claim `awaiting_review` unless the handoff and runtime evidence are present.

## Edge-case rules

### Missing runtime details
If the app cannot be launched or exercised because the contract omitted required runtime details:
- inspect the repo for authoritative commands
- document what you found
- if still ambiguous, stop and mark blocked
- do not fabricate a start command just to keep moving

### Tests cannot be executed
If required checks cannot run because of missing dependencies, broken setup, credentials, or harness limits:
- record the exact failed command and error in `runtime.md`
- note the impact in `handoff.md`
- do not hide the gap from review
- only route to review if the remaining observable behavior can still be independently checked

### Implementation exceeded contract scope
If you already changed something outside scope:
- decide whether it can be safely reverted before handoff
- if not, disclose the exact out-of-contract change in `handoff.md`
- mark the sprint blocked or expect review failure
- do not silently normalize the overreach as acceptable

## Stop conditions

Route to `adversarial-live-review` only when all of the following are true:
- contracted implementation work is complete
- `runtime.md` contains reproducible run instructions and evidence
- `handoff.md` clearly says `READY_FOR_REVIEW`
- `status.json` says `awaiting_review`

Otherwise stop cleanly, preserve evidence, and leave the sprint in a blocked or paused state that a future agent can resume without chat history.
