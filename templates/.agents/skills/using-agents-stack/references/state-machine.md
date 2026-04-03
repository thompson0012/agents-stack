# agents-stack state machine

This reference defines the durable phase model for the starter-pack harness. The orchestrator reads these rules to decide which child skill owns the next action, then dispatches that child as a fresh worker. State comes from files, not chat memory.

## Core invariants

- Exactly one sprint may be runnable at a time.
- Additional non-terminal sprint folders may remain in `.harness/` only when they are explicitly parked in `awaiting_human` or `escalated_to_human`.
- Parked sprints stay visible in durable state, but they do not count as the runnable active sprint.
- Global state in `docs/live/*` tracks project-level priority, dependencies, parked visibility, and history.
- Local state in `.harness/<feature-id>/*` tracks one sprint's current checkpoint, retry budget, and human handoff boundary.
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

## Scheduling order when no runnable sprint exists

When no runnable active sprint exists, the orchestrator chooses the next non-runnable or backlog phase in this order:

1. drain `compound_pending_feature_ids` via `compound-capture`
2. choose the highest-priority dependency-ready `needs_brainstorm` item
3. choose the highest-priority dependency-ready `pending` item
4. otherwise surface parked or dependency blockers honestly

This lets explicit compounding run before new work and lets the backlog advance around parked work without pretending the parked sprint is complete.

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
| `needs_brainstorm` | `docs/live/features.json` tracks a dependency-ready item as `needs_brainstorm`, optionally with supporting notes in `docs/live/ideas.md` | `generator-brainstorm` worker | The candidate is real enough to track, but still too vague for honest proposal work. | Refine or promote it to `pending`. |
| `proposal_needed` | No runnable active sprint and at least one dependency-ready pending feature | `generator-proposal` worker | A ready backlog item exists but no local sprint has been proposed. | Create `.harness/<feature>/sprint_proposal.md`. |
| `proposal_ready` | `sprint_proposal.md` exists | `evaluator-contract-review` worker | Proposed scope exists and needs adversarial contract review. | Approve into `contract.md` or reject with revisions. |
| `contracted` | `contract.md` exists and no later artifact exists | `generator-execution` worker | Boundaries and QA criteria are approved; implementation can begin. | Execute or resume work. |
| `executing` | `status.json` shows active execution, no later artifact exists | `generator-execution` worker | Work is underway. | Finish implementation, or record an execution-time failure honestly. |
| `build_failed` | `status.json.phase = build_failed` plus execution notes in `runtime.md` or `handoff.md` | `state-update` worker, then `compound-capture`, then orchestrator | Build, startup, or smoke-triage failed during execution, so the sprint must reconcile, compound, and then retry or escalate. | Clean-restore and retry, park for human input, or escalate. |
| `paused_by_timeout` | `status.json.phase = paused_by_timeout` | Route by `resume_from`, usually a fresh phase worker | Prior session stopped without a clean finish. | Resume from the last trustworthy checkpoint. |
| `awaiting_review` | `handoff.md` exists and `review.md` does not | `adversarial-live-review` worker | Execution claims completion and is waiting for independent review. | Review observable behavior and state transitions. |
| `review_recorded` | `review.md` exists | `state-update` worker | Review outcome exists and must be synchronized into durable state. | Archive on PASS, reopen on FAIL, or park/escalate on BLOCKED. |
| `review_failed` | `review.md` remains on disk; `status.json.phase = review_failed` after `state-update` reconciles a FAIL review | `state-update` worker, then `compound-capture`, then orchestrator | The failure is durable, the evidence stays attached, and the next execution loop owns the sprint only after compounding and retry gates are satisfied. | Clean-restore and retry, park for human input, or escalate. |
| `awaiting_human` | `status.json.phase = awaiting_human` plus explicit human action fields | no automatic child until human input changes files | Automation is paused at a durable file boundary for human edits, approvals, or environment intervention. | Wait for human edits, then resume from `resume_from`. |
| `escalated_to_human` | `status.json.phase = escalated_to_human` plus escalation reason | no automatic child until human decision changes files | Automatic retry must stop because attempt budget is exhausted or recovery is unsafe. | Human decides whether to reset, cancel, or re-scope. |
| `compound_pending` | `docs/live/features.json` lists the feature id in `compound_pending_feature_ids` | `compound-capture` worker | Explicit durable-learning capture must run before new work selection or runnable resume. | Capture the durable lesson or clear the queue truthfully. |
| `archived` | Artifacts moved or copied to `docs/archive/...` and live state updated | `generator-brainstorm` or `generator-proposal` worker for the next item | Sprint is complete and no longer active. | Select the next dependency-ready `needs_brainstorm` or `pending` feature. |

## Transition rules

### Initialization, brainstorm, and proposal

- `uninitialized` -> `needs_brainstorm` or `proposal_needed`
  - Trigger: `project-initializer` worker seeds `docs/live/features.json`, `docs/live/ideas.md`, `progress.md`, and related live files truthfully.
- `needs_brainstorm` -> `proposal_needed`
  - Trigger: `generator-brainstorm` worker clarifies the candidate enough to promote it into `pending` backlog state.
- `needs_brainstorm` -> `needs_brainstorm`
  - Trigger: the idea is still too vague for honest proposal work, so brainstorming leaves it tracked but non-runnable.
- `proposal_needed` -> `proposal_ready`
  - Trigger: `generator-proposal` worker creates `.harness/<feature-id>/sprint_proposal.md` and marks the sprint as proposed.
- `proposal_needed` -> `needs_brainstorm`
  - Trigger: proposal discovery proves the candidate is still too vague or forked, so it is explicitly returned to brainstorming instead of getting a mushy proposal.
- `proposal_needed` -> `proposal_needed`
  - Trigger: the highest-priority pending feature is not dependency-ready, so backlog traversal continues until a ready item is found or the queue is exhausted.

### Execution loop

- `contracted` -> `executing`
  - Trigger: `generator-execution` worker starts work and updates `status.json`.
- `executing` -> `awaiting_review`
  - Trigger: execution completes the contracted scope, passes build/startup triage, and writes `handoff.md`.
- `executing` -> `build_failed`
  - Trigger: build, startup, or basic smoke verification fails before the sprint is ready for independent review.
- `executing` -> `awaiting_human`
  - Trigger: execution reaches a deliberate human pause/edit/resume boundary and records the required file-level action.
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

### Review, state update, and compounding

- `awaiting_review` -> `review_recorded`
  - Trigger: `adversarial-live-review` worker writes `review.md` with explicit PASS, FAIL, or BLOCKED.
- `review_recorded` -> `archived`
  - Trigger: `state-update` worker processes a PASS review, updates `docs/live/*`, and archives the sprint.
- `review_recorded` -> `review_failed`
  - Trigger: `state-update` worker processes a FAIL review, increments retry metadata, preserves the evidence, and records the retry checkpoint.
- `review_recorded` -> `awaiting_human`
  - Trigger: `state-update` worker processes a BLOCKED review that requires human edits, approvals, credentials, or other intervention at a file-described pause boundary.
- `review_recorded` -> `escalated_to_human`
  - Trigger: `state-update` worker processes a BLOCKED review that cannot be retried safely or honestly by automation.
- `archived`, `review_failed`, `awaiting_human`, or `escalated_to_human` -> `compound_pending`
  - Trigger: `state-update` queues the feature id in `compound_pending_feature_ids` after reconciling the decisive outcome.

### Retry, pause, escalation, and post-compound routing

- `build_failed` -> `executing`
  - Trigger: retry metadata is fully recorded, `attempt_count < max_attempts`, `clean_restore_ref` names a safe restore boundary, and any queued compounding has been drained.
- `review_failed` -> `executing`
  - Trigger: local and live state agree that the failure is reconciled, `attempt_count < max_attempts`, `clean_restore_ref` names a safe restore boundary, and any queued compounding has been drained.
- `build_failed` -> `awaiting_human`
  - Trigger: retry is not yet safe because a human must edit files, repair the environment, or confirm the restore boundary, but escalation is not yet required.
- `review_failed` -> `awaiting_human`
  - Trigger: fixing the review failure requires explicit human edits or approvals before another clean retry.
- `build_failed` -> `escalated_to_human`
  - Trigger: `attempt_count` reaches `max_attempts` or no safe clean restore boundary exists.
- `review_failed` -> `escalated_to_human`
  - Trigger: `attempt_count` reaches `max_attempts` or no safe clean restore boundary exists.
- `awaiting_human` -> route by `resume_from`
  - Trigger: a human changes the named files, updates the pause metadata, or otherwise records that the durable gate is cleared.
- `escalated_to_human` -> route by explicit human decision
  - Trigger: a human records a reset, cancellation, rescope, or new restore boundary in the files.
- `compound_pending` -> `executing`
  - Trigger: the queue entry is cleared and the same sprint still remains the single runnable active sprint.
- `compound_pending` -> `needs_brainstorm` or `proposal_needed`
  - Trigger: the queue entry is cleared and no runnable sprint remains, so the orchestrator returns to dependency-ready backlog selection.

## PASS / FAIL / BLOCKED routing

### PASS path

1. `adversarial-live-review` worker writes `review.md` with PASS.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - updates `docs/live/features.json`
   - appends outcome to `docs/live/progress.md`
   - archives the sprint to `docs/archive/<feature-id>_<timestamp>/`
   - clears runnable active-sprint status
   - queues the feature id in `compound_pending_feature_ids`
4. The next router pass selects `compound-capture`. Only after the queue is drained may the harness select new proposal work or another runnable sprint.

### FAIL path

1. `adversarial-live-review` worker writes `review.md` with FAIL and concrete directives.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - keeps the sprint active or parks it honestly
   - records `review_failed` in durable state
   - increments `attempt_count` and confirms `max_attempts`
   - preserves directives and evidence
   - records or validates `clean_restore_ref` before any automatic retry
   - queues the feature id in `compound_pending_feature_ids`
   - leaves `review.md` on disk as evidence for the retry
   - updates global progress so the failure is visible outside the sprint folder
4. The next router pass selects `compound-capture` first. After the queue is drained, it selects `generator-execution` only if the retry is reconciled, attempts remain, and the restore boundary is safe. Otherwise the sprint moves to `awaiting_human` or `escalated_to_human`.

FAIL is not terminal. It is a new execution loop with stricter evidence, and the retry is driven by durable state instead of deleting review evidence.

### BLOCKED path

1. `adversarial-live-review` worker writes `review.md` with BLOCKED and concrete recovery steps.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - keeps the sprint visible in `.harness/`
   - records the blocker in durable state
   - decides between `awaiting_human` and `escalated_to_human`
   - queues the feature id in `compound_pending_feature_ids` so durable lessons can be captured before future routing
   - leaves `review.md` on disk as evidence for the stalled checkpoint
   - updates global progress so the blocker is visible outside the sprint folder
4. The next router pass selects `compound-capture` first, then either waits on the human gate or routes around parked work through dependency-ready backlog selection.

## Build/startup triage rule

Execution must do a minimal truthful build/startup check before asking for live review. If build, startup, or the first reproducible smoke step fails, the sprint enters `build_failed` instead of `awaiting_review`. Review workers do not spend time rediscovering failures that execution already observed.

## State-transition verification rule

Interactive acceptance criteria and adversarial reviews must verify before/action/after state transitions, not only a final static state. Reject hardcoded "looks passed now" conditions that do not prove the contractually required transition occurred.

Examples:

- Verify the precondition or prior state first.
- Perform the user-visible action or reproduction step.
- Verify the postcondition and the absence of contradictory side effects.

## Contradictory state handling

Contradiction examples:

- `review.md` exists but `status.json.phase = contracted`
- `handoff.md` exists but the feature still shows `pending` in `docs/live/features.json`
- two runnable features are marked active at once
- `.harness/FEAT-001/` is parked in `awaiting_human`, but live state still treats it as the runnable active sprint
- `.harness/FEAT-002/` is `review_failed` with `attempt_count >= max_attempts`, but routing still points to execution

Handling rules:

1. Route from strongest artifact evidence, not the optimistic status field.
2. Treat contradiction as a state integrity problem, not silent success.
3. Send contradictions that require reconciliation to `state-update`.
4. If contradiction prevents choosing a single runnable sprint, `state-update` must preserve evidence and surface the conflict for human resolution rather than inventing a winner.

## Terminal state definition

A sprint is terminal only when all of the following are true:

- review passed
- global live state reflects the outcome
- the sprint is archived under `docs/archive/<feature-id>_<timestamp>/`
- no runnable active status remains for that sprint in `.harness/`

Anything short of that is resumable or parked work, not completion.
