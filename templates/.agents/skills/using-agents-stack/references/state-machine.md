# agents-stack state machine

This reference defines the durable phase model for the starter-pack harness. The orchestrator reads these rules to decide which child skill owns the next action, then dispatches that child as a fresh worker. State comes from files, not chat memory.

## Core invariants

- Exactly one sprint may be active at a time.
- Global state in `docs/live/*` tracks project-level priority and history.
- Local state in `.harness/<feature-id>/*` tracks one in-flight sprint.
- Archived state in `docs/archive/<feature-id>_<timestamp>/` preserves completed sprint artifacts.
- A sprint is not complete when code exists. It is complete only after review passes and state is updated.
- If state files disagree, later-phase artifact evidence wins over stale status declarations.
- The orchestrator routes and dispatches; each phase runs in a fresh worker with phase-scoped tools.
- Workers do not spawn other workers. If more delegation is needed, control returns to the lead orchestrator.

Evidence precedence for routing:

1. `review.md`
2. `handoff.md`
3. `contract.md`
4. `sprint_proposal.md`
5. `status.json`
6. `docs/live/features.json`

## Orchestrator-worker execution model

- The lead orchestrator chooses the next phase from durable state and starts a fresh worker through the host runtime's delegation primitive.
- The worker owns exactly one phase and writes that phase's canonical artifacts.
- Independent work may run in parallel only when the lead orchestrator starts sibling workers with non-overlapping ownership and merges their outputs back into sprint-local state.
- Retries do not reuse old context windows. They start a new worker and keep prior evidence on disk.
- Structured worker returns should name the worker ID, phase, artifact paths, blockers, and next owner when useful.

## Phase model

| Phase | Durable evidence | Owner skill | Meaning | Normal next step |
| --- | --- | --- | --- | --- |
| `uninitialized` | `docs/live/features.json` missing, empty, or unusable | `project-initializer` worker | Repo is not ready for sprint routing yet. | Seed durable live state. |
| `proposal_needed` | No active sprint and at least one pending feature | `generator-proposal` worker | A ready backlog item exists but no local sprint has been proposed. | Create `.harness/<feature>/sprint_proposal.md`. |
| `proposal_ready` | `sprint_proposal.md` exists | `evaluator-contract-review` worker | Proposed scope exists and needs adversarial contract review. | Approve into `contract.md` or reject with revisions. |
| `contracted` | `contract.md` exists and no later artifact exists | `generator-execution` worker | Boundaries and QA criteria are approved; implementation can begin. | Execute or resume work. |
| `executing` | `status.json` shows active execution, no later artifact exists | `generator-execution` worker | Work is underway. | Finish implementation and emit handoff. |
| `paused_by_timeout` | `status.json.phase = paused_by_timeout` | Route by `resume_from`, usually a fresh `generator-execution` worker | Prior session stopped without a clean finish. | Resume from the last trustworthy checkpoint. |
| `blocked` | `status.json.phase = blocked` with blocker notes | `state-update` worker | The sprint cannot safely continue without escalation or reprioritization. | Publish blocker into live state. |
| `awaiting_review` | `handoff.md` exists and `review.md` does not | `adversarial-live-review` worker | Execution claims completion and is waiting for independent review. | Review observable behavior. |
| `review_recorded` | `review.md` exists | `state-update` worker | Review outcome exists and must be synchronized into durable state. | Archive on PASS or reopen on FAIL. |
| `review_failed` | `review.md` remains on disk; `status.json.phase = review_failed` after `state-update` reconciles a FAIL review | `generator-execution` worker | The failure is durable, the evidence stays attached, and the next execution loop owns the sprint. | Implement fixes and produce a new handoff. |
| `archived` | Artifacts moved or copied to `docs/archive/...` and live state updated | `generator-proposal` worker for the next item | Sprint is complete and no longer active. | Select the next pending feature. |

## Transition rules

### Initialization and proposal

- `uninitialized` -> `proposal_needed`
  - Trigger: `project-initializer` worker seeds `docs/live/features.json`, `progress.md`, and related live files.
- `proposal_needed` -> `proposal_ready`
  - Trigger: `generator-proposal` worker creates `.harness/<feature-id>/sprint_proposal.md` and marks the sprint as proposed.

### Contract review

- `proposal_ready` -> `contracted`
  - Trigger: `evaluator-contract-review` worker approves scope and writes `contract.md`.
- `proposal_ready` -> `proposal_needed`
  - Trigger: proposal is rejected and explicitly reset for rewrite.
- `proposal_ready` -> `proposal_ready`
  - Trigger: proposal remains under revision, but no execution starts until a contract exists.

### Execution loop

- `contracted` -> `executing`
  - Trigger: `generator-execution` worker starts work and updates `status.json`.
- `executing` -> `awaiting_review`
  - Trigger: execution completes the contracted scope and writes `handoff.md`.
- `executing` -> `blocked`
  - Trigger: execution finds a real dependency, environment failure, or human decision blocker that cannot be solved safely inside the contract.
- `executing` -> `paused_by_timeout`
  - Trigger: watchdog or orchestrator detects an expired heartbeat or abandoned runtime.

### Timeout and resume

- `paused_by_timeout` -> route by `resume_from`
  - `resume_from = sprint_proposal.md` -> fresh `evaluator-contract-review` worker
  - `resume_from = contract.md` -> fresh `generator-execution` worker
  - `resume_from = handoff.md` -> fresh `adversarial-live-review` worker
  - `resume_from = review.md` -> fresh `state-update` worker
- If `resume_from` is missing or points to a nonexistent file, derive the phase from artifact precedence instead of trusting the stale field.
- Timeout does not discard work. The sprint remains active until state is reconciled.
- Preserve prior evidence across retries. A resume creates a new worker assignment; it does not delete the earlier handoff or review trail.

### Review and state update

- `awaiting_review` -> `review_recorded`
  - Trigger: `adversarial-live-review` worker writes `review.md` with explicit PASS, FAIL, or BLOCKED.
- `review_recorded` -> `archived`
  - Trigger: `state-update` worker processes a PASS review, updates `docs/live/*`, and archives the sprint.
- `review_recorded` -> `review_failed`
  - Trigger: `state-update` worker processes a FAIL review, keeps the sprint active, records the failure in durable state, and leaves `review.md` in place as evidence.
- `review_recorded` -> `blocked`
  - Trigger: `state-update` worker processes a BLOCKED review, keeps the sprint active, records the blocker in durable state, and waits for blocker resolution before another phase is dispatched.
- `review_failed` -> `executing`
  - Trigger: a fresh `generator-execution` worker resumes with directives from `review.md` after the failure has been reconciled in live state, producing a new `handoff.md` for another review cycle.

## PASS / FAIL / BLOCKED routing

### PASS path

1. `adversarial-live-review` worker writes `review.md` with PASS.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - updates `docs/live/features.json`
   - appends outcome to `docs/live/progress.md`
   - preserves learnings in `docs/live/memory.md` if needed
   - archives the sprint to `docs/archive/<feature-id>_<timestamp>/`
   - clears active-sprint status
4. The next router pass selects `generator-proposal` for the next pending feature, or `project-initializer` only if the repo was never properly initialized.

### FAIL path

1. `adversarial-live-review` worker writes `review.md` with FAIL and concrete directives.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - keeps the sprint active
   - records `review_failed` in durable state
   - preserves directives and evidence
   - leaves `review.md` on disk as evidence for the retry
   - updates global progress so the failure is visible outside the sprint folder
4. The next router pass selects `generator-execution` and dispatches a new execution worker.

FAIL is not terminal. It is a new execution loop with stricter evidence, and the retry is driven by durable state instead of deleting review evidence.

### BLOCKED path

1. `adversarial-live-review` worker writes `review.md` with BLOCKED and concrete recovery steps.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - keeps the sprint active
   - records the blocker in durable state
   - leaves `review.md` on disk as evidence for the stalled checkpoint
   - updates global progress so the blocker is visible outside the sprint folder
4. The orchestrator does not dispatch another phase worker until the blocker is resolved or a human changes the sprint decision.

## Contradictory state handling

Contradiction examples:

- `review.md` exists but `status.json.phase = contracted`
- `handoff.md` exists but the feature still shows `pending` in `docs/live/features.json`
- two features are marked active at once
- `.harness/FEAT-001/` exists with active artifacts, but live state says there is no active sprint

Handling rules:

1. Route from strongest artifact evidence, not the optimistic status field.
2. Treat contradiction as a state integrity problem, not silent success.
3. Send contradictions that require reconciliation to `state-update`.
4. If contradiction prevents choosing a single active sprint, `state-update` must preserve evidence and surface the conflict for human resolution rather than inventing a winner.

## Terminal state definition

A sprint is terminal only when all of the following are true:

- review passed
- global live state reflects the outcome
- the sprint is archived under `docs/archive/<feature-id>_<timestamp>/`
- no active status remains for that sprint in `.harness/`

Anything short of that is resumable work, not completion.
