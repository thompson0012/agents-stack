# Harness Reference

This file is the durable operational constitution for agents-stack after bootstrap. Read it when routing, retrying, resuming, reconciling state, or deciding whether a sprint is truly complete.

## Constitutional invariants

1. Files beat chat memory.
   - Durable files are the state model.
   - Chat summaries, optimistic tool output, and stale status text do not overrule stronger file evidence.
2. Exactly one sprint may be runnable at a time.
   - `docs/live/features.json` is the runnable selector.
   - Parked sprints may remain visible in `.harness/`, but `awaiting_human` and `escalated_to_human` do not count as runnable.
3. Execution does not self-approve.
   - Execution may implement, verify reviewability, and hand off.
   - Execution may not declare PASS for its own work.
4. Tool walls are hard boundaries.
   - Brainstorm, proposal, execution, review, state-update, and compound lanes have different authority.
   - Do not blur phases because the same runtime technically allows wider access.
5. Reviewers and evaluators stay independent.
   - Contract review and live review must not receive broad implementation write access.
   - Their job is to judge evidence and return decisive artifacts, not patch product code.
6. Reviews verify state transitions, not static end-state snapshots.
   - Check before-state, perform the action or reproduction step, then check after-state.
   - Reject tests or review claims that would pass even if the intended transition never happened.
7. PASS only archives after reconciliation.
   - A sprint is complete only after review PASS, `state-update` reconciles live state, and the sprint is archived.
   - Before that, the sprint is active, resumable, or parked.
8. Active state and historical state stay separate.
   - `.harness/<feature-id>/` is sprint-local active or parked state.
   - `docs/archive/<feature-id>_<timestamp>/` is historical evidence after PASS.
9. The orchestrator routes and workers execute one phase each.
   - Use fresh workers for each phase or retry.
   - Workers do not spawn nested workers.

## State model and evidence precedence

### Global, local, and historical roles

- `docs/live/features.json`
  - authoritative backlog and single runnable-sprint selector
  - also carries parked visibility and `compound_pending_feature_ids`
- `docs/live/current-focus.md`
  - live resume anchor for the broader initiative and next owner
  - not a sprint contract
- `docs/live/roadmap.md`
  - durable initiative ledger for source goal, remaining slices, and re-authorization boundaries
  - not a sprint contract
- `.harness/<feature-id>/`
  - sprint-local proposal, contract, runtime, handoff, review, and status checkpoints
- `docs/archive/<feature-id>_<timestamp>/`
  - preserved PASS history, including the final `status.json` snapshot

### Evidence precedence when files disagree

Route from the strongest durable evidence, in this order:

1. explicit human edits or instructions
2. `review.md`
3. `handoff.md`
4. `runtime.md` when it records an execution-time failure or pause boundary
5. `contract.md`
6. `sprint_proposal.md`
7. `.harness/<feature-id>/status.json`
8. `docs/live/features.json`
9. `docs/live/roadmap.md`
10. `docs/live/current-focus.md`
11. `docs/live/progress.md` and `docs/live/memory.md`
12. `docs/reference/*`
13. `docs/archive/*`

Implications:

- Later-phase artifacts outrank stale `status.json` fields.
- Local sprint evidence outranks optimistic global status for the same sprint.
- Global live state still decides which sprint is supposed to be runnable when local files are ambiguous.
- Archive folders are evidence for history and learning, not active routing targets.

## Deterministic routing cascade

Apply this cascade in order. Do not treat it as an unordered checklist.

1. If the repository is missing usable live state, route to `project-initializer`.
   - Missing, empty, or contradictory `docs/live/features.json` means the harness is not ready for normal routing.
2. Read `docs/live/current-focus.md` and `docs/live/roadmap.md` before sprint chaining.
   - If the durable goal or next authorized slice is stale, refresh that source-goal truth before continuing.
3. If `compound_pending_feature_ids` is non-empty, route `compound-capture` first.
   - Compounding drains before runnable sprint resume or new backlog selection.
4. If multiple runnable sprints appear active, stop treating this as ordinary execution.
   - Route to reconciliation first. If the conflict cannot be resolved from file evidence, surface it for human action.
5. If exactly one runnable active sprint exists, route from the strongest local artifact for that sprint.
6. If `review.md` exists and live plus local state are not yet reconciled, route `state-update`.
   - Never jump straight from `review.md` back into execution or proposal.
7. If `handoff.md` exists and `review.md` does not, route `adversarial-live-review`.
8. If the sprint is `build_failed` or reconciled `review_failed`, retry only through `generator-execution`, and only when all retry gates pass.
   - `attempt_count < max_attempts`
   - `clean_restore_ref` exists and names a safe restore boundary
   - the failure has already been reconciled into durable state
   - any queued compounding has already been drained
9. If the sprint is `awaiting_human` or `escalated_to_human` and that parked state is already reflected durably, do not auto-dispatch execution.
   - Resume only after human edits or decisions change the checkpoint.
10. If `contract.md` exists and no later-phase artifact blocks it, route `generator-execution`.
11. If `sprint_proposal.md` exists without an approved `contract.md`, route `evaluator-contract-review`.
12. If no runnable sprint exists and the highest-priority dependency-ready backlog item is `needs_brainstorm`, route `generator-brainstorm`.
13. Otherwise, if no runnable sprint exists and the highest-priority dependency-ready backlog item is `pending`, route `generator-proposal`.
14. Otherwise surface the blocker honestly.
   - Missing dependencies, parked work, exhausted retries, or stale durable state are routing truths, not reasons to guess.

## Worker model and anti-nesting rules

### Orchestrator responsibilities

- Read durable state before dispatch.
- Choose one phase owner at a time.
- Dispatch a fresh worker with phase-appropriate tools and explicit artifact return targets.
- Merge worker evidence back into durable files before selecting the next phase.
- Stay thin: route, dispatch, merge, and reconcile. Do not secretly do child-phase work inline.

### Worker rules

- A worker owns exactly one phase.
- Workers do not spawn nested workers.
- Retries start a fresh execution worker. They do not reuse the old execution context.
- Parallel sibling workers are allowed only for truly independent, non-overlapping work with a clear merge owner.

### Lane walls

- Brainstorm writes idea exploration and narrow backlog promotion only.
- Proposal writes sprint-local planning plus any legitimate live planning refresh.
- Contract review evaluates scope and either approves into `contract.md` or rejects decisively.
- Execution changes only approved contract scope plus sprint-local runtime and handoff artifacts.
- Live review records review evidence and verdicts. It does not patch implementation.
- State-update reconciles local and global truth, appends progress, archives PASS outcomes, and queues compounding.
- Compound-capture writes durable lessons and clears processed queue entries. It does not reopen sprint state or claim the runnable slot.

If the runtime supports per-worker tool restrictions, use them. If it does not, the phase contract still applies.

## Resume and retry contract

### Where to read to resume

On a cold start:

1. read `README.md`
2. read `AGENTS.md`
3. read `docs/scripts/init.sh`
4. then open this file when routing, retry, reconciliation, or resume logic is needed

For active or parked work:

1. read `docs/live/features.json` to identify the active sprint, parked sprints, and compound queue
2. read `docs/live/current-focus.md` and `docs/live/roadmap.md` to understand the broader goal, next owner, and re-authorization boundary
3. read the strongest sprint-local artifact for the selected sprint
   - `review.md` if present
   - else `handoff.md`
   - else `runtime.md` when execution recorded a failure or pause
   - else `contract.md`
   - else `sprint_proposal.md`
4. read `.harness/<feature-id>/status.json` for machine-readable resume metadata

Use `status.json.resume_from` as a pointer, not as stronger evidence than later artifacts.

### `status.json` expectations

`status.json` is the machine-readable checkpoint for resume, retry, traceability, and parked-state truth.

Minimum durable fields for an active or parked sprint:

- `sprint_id`
- `phase`
- `resume_from`
- `last_updated_at`

Expected routing and traceability fields when they apply:

- `owner_role`
- `worker_id`
- `worker_kind`
- `expected_outputs`
- `blocked_on`

Required retry metadata for `build_failed` or `review_failed` retries:

- `attempt_count`
- `max_attempts`
- `clean_restore_ref`

Required parked-state metadata when automation is paused:

- `human_action_required` for `awaiting_human`
- `pause_reason` for `awaiting_human`
- `escalation_reason` for `escalated_to_human`
- `parked_at`

Rules:

- Preserve retry metadata across proposal revisions, retries, and state reconciliation unless the policy truthfully changes.
- Do not erase evidence fields when retrying or parking a sprint.
- If `resume_from` is stale or missing, derive the next step from artifact precedence instead of guessing.

### Retry rules

- Retries after `build_failed` or reconciled `review_failed` are explicit orchestration events.
- Do not retry until local and global state agree on the failure outcome.
- Do not retry unless `attempt_count < max_attempts`.
- Do not retry unless `clean_restore_ref` names a safe boundary such as a disposable worktree, VCS snapshot, or equivalent checkpoint.
- Automatic destructive reset is acceptable only in disposable workspaces with an explicit restore boundary. It is not the default assumption.
- If the retry is unsafe, out of budget, or blocked on a human decision, move to `awaiting_human` or `escalated_to_human` instead of looping.

## Review and publication rules

### Build and startup triage before review

Execution owns the first honest build or startup check.

- If the contract implies code, build, startup, or smoke verification, execution runs the minimal truthful check needed to prove reviewability.
- If that triage fails, record `build_failed` in `runtime.md` or `handoff.md` and update `status.json`.
- Do not send a sprint to live review just so review can rediscover an execution-time failure.

### Review must verify transitions

Contract review and live review must verify state transitions, not only static outputs.

1. prove the before-state
2. perform the user-visible action, reproduction step, or contractually required change
3. prove the after-state and check for contradictory side effects

A review that only proves a final static condition has not proved the contract.

### PASS, FAIL, and BLOCKED outcomes

PASS path:

1. `adversarial-live-review` writes PASS to `review.md`.
2. Route `state-update`.
3. `state-update` updates `docs/live/*`, appends progress, archives the sprint, clears runnable status, and queues the feature in `compound_pending_feature_ids`.
4. The next router pass drains `compound-capture` before selecting more work.

FAIL path:

1. `adversarial-live-review` writes FAIL with concrete directives.
2. Route `state-update`.
3. `state-update` preserves evidence, records `review_failed`, updates retry metadata, refreshes live planning when needed, and queues compounding.
4. Only after compounding is drained may the harness retry through fresh execution, and only if retry gates pass.

BLOCKED path:

1. `adversarial-live-review` writes BLOCKED with explicit recovery steps.
2. Route `state-update`.
3. `state-update` decides between `awaiting_human` and `escalated_to_human`, records the blocker durably, and queues compounding.
4. The harness does not auto-dispatch execution while the human gate remains unchanged.

### Archive rules

- Archive only after review PASS and `state-update` reconciliation.
- Never treat `.harness/<feature-id>/` as the archive itself.
- Archive naming should include the feature id and a timestamp or equivalent unique suffix.
- Preserve the final `status.json` snapshot in the archive so worker IDs, attempt counters, restore boundaries, and parked history remain auditable.
- FAIL, BLOCKED, `awaiting_human`, and `escalated_to_human` keep their evidence in `.harness/<feature-id>/`; they are not archived as completed work.

## State-disagreement worked examples

| Situation | Stronger truth | Correct action |
| --- | --- | --- |
| Local sprint is ahead of global state: `review.md` exists, but `docs/live/features.json` still says the sprint is active and unreconciled. | `review.md` outranks stale live state. | Route `state-update`. Do not resume execution yet. |
| Global state is ahead of local state: `docs/live/features.json` says no runnable sprint exists, but `.harness/FEAT-002/contract.md` still looks active. | Live state says the sprint was already reconciled or displaced, unless fresher local evidence proves otherwise. | Reconcile via `state-update` or surface a human conflict. Do not silently reopen the sprint. |
| Conflicting runnable features: two backlog items or sprint folders both look runnable. | This is a state-integrity failure, not an invitation to pick one arbitrarily. | Stop normal routing. Reconcile to one runnable sprint or park the conflict for human resolution. |
| Parked sprint missing gate metadata: `status.json.phase = awaiting_human`, but no `human_action_required`, `pause_reason`, or truthful `resume_from` is recorded. | The parked state is incomplete and not safely resumable. | Route to reconciliation or explicit human repair of the checkpoint. Do not guess what clears the gate. |
| Review exists but status is stale: `review.md` records FAIL, while `status.json.phase = contracted`. | `review.md` is stronger. | Route `state-update`, preserve the review evidence, record `review_failed`, then decide retry versus park or escalate. |
| `review_failed` or `build_failed` exists, but `clean_restore_ref` is missing or unsafe. | Retry safety invariants block automatic execution. | Do not launch a retry. Park in `awaiting_human` or `escalated_to_human` with explicit recovery instructions. |
| Parked local sprint still appears as the runnable active sprint globally. | Parked local evidence plus live mismatch means state disagreement. | Route `state-update` to remove runnable status or surface the conflict for human action. |

## Terminal state definition

A sprint is complete only when all of the following are true:

- review passed
- `state-update` reconciled the result into `docs/live/*`
- the sprint is archived under `docs/archive/<feature-id>_<timestamp>/`
- no runnable active status remains for that sprint
- any compounding that should happen is queued explicitly and can be drained on the next router pass

Anything short of that is active, resumable, parked, or contradictory work. It is not complete.