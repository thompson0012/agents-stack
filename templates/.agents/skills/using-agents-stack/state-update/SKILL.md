---
name: state-update
purpose: Synchronize decisive sprint outcomes back into durable project state, preserving evidence and making the next phase explicit.
trigger: After `adversarial-live-review` has written a decisive review outcome, or after execution has written a decisive non-review state such as `build_failed`, `awaiting_human`, or `escalated_to_human`.
inputs:
  - AGENTS.md
  - docs/live/features.json
  - docs/live/progress.md
  - .harness/<sprint-id>/contract.md
  - .harness/<sprint-id>/runtime.md
  - .harness/<sprint-id>/handoff.md
  - .harness/<sprint-id>/qa.md
  - .harness/<sprint-id>/review.md
  - .harness/<sprint-id>/status.json
outputs:
  - updated docs/live/features.json
  - updated docs/live/progress.md
  - updated .harness/<sprint-id>/status.json or preserved sprint folder
  - docs/archive/<sprint-id>_<timestamp>/... on PASS
boundaries:
  - Do not mark completion without evidence.
  - Do not erase failed sprint artifacts.
  - Do not rewrite review findings to make them pass.
  - Do not capture durable cross-sprint learning here; queue explicit Compound work instead.
  - Do not start the next sprint's implementation yourself.
next_skills:
  - compound-capture
  - generator-execution
  - generator-brainstorm
  - generator-proposal
---

# State Update

You are the state reconciler. Your job is to make the repository tell the truth after a decisive sprint-local outcome.

That means:
- global state reflects the latest reviewed or execution-triage outcome
- local sprint state remains resumable or is archived truthfully
- archived artifacts remain auditable
- routing to the next phase is explicit
- parked human-owned sprints are visible without pretending they are still runnable
- durable learning capture is queued for the explicit Compound phase instead of being folded into reconciliation

## Worker Dispatch Contract

- Run state reconciliation in a fresh worker context. The orchestrator dispatches this worker after review or execution triage; it does not perform state-update inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: durable state and archive operations only: `docs/live/features.json`, `docs/live/progress.md`, `.harness/<sprint-id>/*`, and `docs/archive/*` as required by the outcome. No product-code edits, no proposal rewriting, no new implementation work, and no `docs/live/memory.md` edits.
- Not parallel-safe. This worker owns the single runnable active sprint's global reconciliation, archive decision, and compounding queue update; do not split or race writes across multiple workers.
- Durable return contract: updated `docs/live/features.json`, `docs/live/progress.md`, `.harness/<sprint-id>/status.json`, and PASS-path archive contents. Include `worker_id` / `orchestrator_run_id` in the updated status or ledger entry when the host provides them.

## Mandatory verification before any update

Before touching global state, identify which decisive phase actually happened.

### Review-driven outcomes
If `status.json` or `review.md` says the sprint was reviewed, confirm all of the following:
1. `.harness/<sprint-id>/review.md` exists.
2. `.harness/<sprint-id>/qa.md` exists or `review.md` explicitly embeds equivalent evidence.
3. The review decision is unambiguous: `PASS`, `FAIL`, or `BLOCKED`.
4. `status.json` points to the review checkpoint.
5. The reviewed sprint matches the backlog item recorded in `docs/live/features.json`.

### Execution-triage outcomes
If `status.json` says `build_failed`, `awaiting_human`, or `escalated_to_human`, confirm all of the following:
1. `.harness/<sprint-id>/runtime.md` exists.
2. `.harness/<sprint-id>/handoff.md` exists.
3. The failure, pause, or escalation reason is explicit.
4. `status.json` includes any relevant `attempt_count`, `max_attempts`, and `clean_restore_ref` fields.
5. The sprint matches the backlog item recorded in `docs/live/features.json`.

If the required evidence for the claimed phase is missing, stop. Do not mark the sprint complete, do not archive it, and do not advance the backlog. Missing evidence is a data-integrity problem.

## Sources of truth by decision type

- `review.md` decides PASS vs FAIL vs BLOCKED.
- `qa.md` proves what was actually checked during review.
- `contract.md` defines the scope that was supposed to be delivered.
- `runtime.md` and `handoff.md` explain how the result was produced, where triage failed, or how a human can resume.
- `status.json` carries the current local routing truth, including attempt budgeting and clean restore metadata.
- `docs/live/features.json` is the authoritative tracked-work ledger that must now be synchronized.
- `docs/live/progress.md` is the reviewed-outcome ledger that must record what changed.

## Update procedure

### 1. Validate the decisive outcome

Read the strongest local artifact for the current phase and extract:
- final status or parked phase
- satisfied or failed contract criteria
- corrective directives or human actions
- any explicit scope violations
- any unexecuted checks or unverifiable claims
- retry state: `attempt_count`, `max_attempts`, and `clean_restore_ref`

If local evidence and `status.json` disagree, preserve the sprint as active or parked and record the discrepancy in `progress.md` rather than pretending the outcome is settled.

### 2. Update `docs/live/features.json`

This file is the project-wide backlog state.
It must distinguish runnable active work from parked non-terminal work and from queued compounding work.

At minimum, publish truthfully:
- which sprint, if any, is the single runnable active sprint
- which sprint ids are parked in `awaiting_human` or `escalated_to_human`
- which feature ids are waiting in `compound_pending_feature_ids` for explicit Compound work
- each feature's phase, owner, attempt count, max attempts, clean restore reference, and next action when those fields exist locally

#### Queue compounding explicitly
After reconciling any decisive outcome, add the feature id to `compound_pending_feature_ids` unless it is already present.

Queueing compounding means:
- the outcome is now published and stable enough for learning capture
- the next durable learning pass belongs to `compound-capture`, not to `state-update`
- the queue does not claim `runnable_active_sprint_id`
- the queue does not reopen execution or review

#### On PASS
- mark the sprint feature as completed using the repository's chosen terminal status
- remove it from the runnable active slot and from any parked list
- preserve identifiers, priority, dependencies, and any useful completion metadata already used by the template
- keep the feature id in `compound_pending_feature_ids` until `compound-capture` finishes

#### On `review_failed` or `build_failed`
- keep the same feature as the runnable active sprint only if an automatic retry is still safe
- copy `attempt_count`, `max_attempts`, `clean_restore_ref`, and the failure phase into the backlog entry
- set `next_action` to a clean retry through `generator-execution`, never to live review directly
- if `attempt_count >= max_attempts` or no safe clean restore boundary exists, convert the live feature state to `escalated_to_human` instead of advertising an automatic retry
- keep the feature id queued in `compound_pending_feature_ids` so the explicit Compound phase can decide whether any durable lesson survives before the next proposal cycle

#### On `awaiting_human`
- keep the sprint in the backlog and `.harness/`, but do not count it as the runnable active sprint
- publish the required human action, affected artifacts, and resume condition
- add the sprint id to the parked list
- keep the feature id queued in `compound_pending_feature_ids` until compounding clears it

#### On `escalated_to_human`
- keep the sprint in the backlog and `.harness/`, but do not count it as the runnable active sprint
- publish the escalation reason, exhausted attempt budget or unsafe recovery condition, and the evidence path the human should inspect
- add the sprint id to the parked list
- keep the feature id queued in `compound_pending_feature_ids` until compounding clears it

Do not invent a new schema casually. Extend only when necessary and keep it consistent.

### 3. Update `docs/live/progress.md`

Append a dated ledger entry that includes:
- sprint id and title
- PASS, FAIL, BLOCKED, BUILD_FAILED, AWAITING_HUMAN, or ESCALATED_TO_HUMAN status
- concise summary of what changed, what failed, or what blocked progress
- path to the evidence (`.harness/...` while active or parked, `docs/archive/...` after archive)
- attempt count and max attempts when retry budgeting matters
- clean restore expectation when another execution pass is possible
- whether the feature was queued for explicit Compound work
- next recommended action

For `review_failed` or `build_failed`, the next action should point back to the same sprint, the corrective directives, and the required clean restore boundary.
For `awaiting_human`, the next action should point to the exact file edits, approval, or manual recovery the human must complete.
For `escalated_to_human`, the next action should halt automatic retry and name the evidence bundle the human should inspect before resuming.
For PASS, the next action should point to `compound-capture` first when `compound_pending_feature_ids` is non-empty, then to backlog selection once compounding is clear.

### 4. Preserve or archive sprint artifacts truthfully

## FAIL path: preserve, do not archive as completed

On `review_failed`:
- keep `.harness/<sprint-id>/` intact
- keep `contract.md`, `runtime.md`, `handoff.md`, `qa.md`, `review.md`, and `status.json`
- update `status.json` to reflect that the sprint remains active, for example:
  - `phase: "review_failed"`
  - `owner_role: "orchestrator"`
  - `resume_from: "review.md"`
- preserve `attempt_count`, `max_attempts`, and `clean_restore_ref`
- synchronize `docs/live/features.json` and `docs/live/progress.md` so the sprint stays open, the failure is visible, and the next action points to a clean retry through `generator-execution`
- queue explicit compounding instead of writing `docs/live/memory.md` here
- if retry budget is exhausted or recovery is unsafe, change the routed phase to `escalated_to_human` instead

A failed sprint is not dead history. It is active work with evidence attached.

## BUILD_FAILED path: preserve and retry only from a clean boundary

On `build_failed`:
- keep `.harness/<sprint-id>/` intact
- keep `contract.md`, `runtime.md`, `handoff.md`, and `status.json`
- preserve the failed build/startup command evidence
- keep or update `phase: "build_failed"`, `owner_role: "orchestrator"`, and `resume_from: "runtime.md"`
- preserve `attempt_count`, `max_attempts`, and `clean_restore_ref`
- route back to `generator-execution` only after live state records the clean restore requirement
- queue explicit compounding instead of writing `docs/live/memory.md` here
- if retry budget is exhausted or recovery is unsafe, change the routed phase to `escalated_to_human`

Build/startup failure is execution evidence, not review work. Do not pay for `adversarial-live-review` when the reviewer cannot even start from the handoff.

## BLOCKED review path: preserve and publish the blocker

On review `BLOCKED`:
- keep `.harness/<sprint-id>/` intact
- keep `contract.md`, `runtime.md`, `handoff.md`, `qa.md` when it exists, `review.md`, and `status.json`
- publish the blocker truthfully in live state
- if the blocker requires a human action, prefer `awaiting_human`
- if the blocker is purely environmental but a safe automated retry is still possible, route back through `generator-execution` with a clean restore requirement
- queue explicit compounding instead of writing `docs/live/memory.md` here

A blocked sprint is not completed work.

## Human-parked paths

On `awaiting_human`:
- keep `.harness/<sprint-id>/` intact
- keep all evidence and checkpoint files needed for a human to edit or approve work from disk alone
- update live state so the sprint is clearly parked and not counted as the runnable active sprint
- route the project either to wait for the named human action or, if dependencies allow, to the highest-priority dependency-ready brainstorm or proposal work after compounding is clear

On `escalated_to_human`:
- keep `.harness/<sprint-id>/` intact
- keep the exhausted-attempt or unsafe-recovery evidence intact
- update live state so the sprint is clearly parked and not counted as the runnable active sprint
- do not advertise another automatic retry
- if another dependency-ready feature exists, route toward backlog selection for that feature after compounding is clear; otherwise wait for human intervention

### Dependency-aware backlog traversal
When there is no runnable active sprint because the current non-terminal sprint is parked in `awaiting_human` or `escalated_to_human`:
- do not pretend the parked sprint is still runnable
- inspect backlog dependencies before selecting new work
- route to `compound-capture` first whenever `compound_pending_feature_ids` is non-empty
- once the compound queue is clear, only route to the highest-priority dependency-ready feature
- if every pending or `needs_brainstorm` feature depends on the parked sprint or another unresolved prerequisite, publish that no runnable work exists and wait for human resolution

## PASS path: archive after global state is updated

On PASS:
1. Verify the review evidence is complete.
2. Update `docs/live/*` first.
3. Archive the full sprint artifact set to `docs/archive/<sprint-id>_<timestamp>/`.
4. Ensure the archive contains, at minimum:
   - `sprint_proposal.md` if it exists
   - `contract.md`
   - `handoff.md`
   - `review.md`
   - `status.json`
   - `runtime.md` when execution produced runtime notes
   - `qa.md` when the review produced a separate QA evidence log
5. Update `status.json` to a terminal archived state, for example:
   - `phase: "archived_pass"`
   - `owner_role: "none"`
   - `resume_from: "docs/archive/<sprint-id>_<timestamp>/review.md"`
6. Remove or clear the active sprint workspace only after the archive copy is confirmed and the harness's single-runnable-sprint rule is preserved.
7. Leave the feature id queued in `compound_pending_feature_ids` until `compound-capture` processes the archived evidence.

Never archive a sprint as complete if review failed, build/startup triage failed, or evidence is missing.

## Routing rules

### After PASS
Route toward the explicit Compound stage first when work is queued:
- if `compound_pending_feature_ids` is non-empty, next skill is `compound-capture`
- once compounding is clear, if another dependency-ready `needs_brainstorm` feature exists, next skill is usually `generator-brainstorm`
- once compounding is clear, if another dependency-ready `pending` feature exists, next skill is usually `generator-proposal`
- if the harness requires re-initialization or backlog refresh, route accordingly from global state

The completed sprint should no longer be the active work packet.

### After `review_failed` or `build_failed`
- queue the feature for `compound-capture` as part of the decisive outcome publication
- after compounding clears, route back to `generator-execution` on the same sprint only when `attempt_count < max_attempts`, `clean_restore_ref` is present and credible, and live state makes the clean retry requirement explicit
- otherwise route to `escalated_to_human`

### After `awaiting_human` or `escalated_to_human`
Keep the sprint parked, preserve the blocker or escalation evidence, and stop automatic phase advancement on that sprint until the required human action is completed.

If compounding is pending, route to `compound-capture` before opening new brainstorm or proposal work. Compounding does not make the parked sprint runnable again.

## Edge-case rules

### Review evidence is missing
If `review.md` exists but no evidence supports it:
- do not mark PASS, FAIL, or BLOCKED into global state as final
- leave the sprint active
- record the inconsistency in `progress.md`
- route back for a proper review, not for fresh implementation

### Build/startup evidence is missing
If `status.json` says `build_failed` but `runtime.md` or `handoff.md` does not prove the failed attempt:
- do not publish an automatic retry as safe
- park the sprint in `awaiting_human` or `escalated_to_human`
- record the inconsistency in `progress.md`

### Tests could not be executed
If the reviewer recorded that required tests could not run:
- treat the sprint as FAIL unless the contract explicitly allowed an alternate proof path
- preserve the failure evidence
- keep the sprint open or parked according to the real blocker

### Implementation exceeded contract scope
If review flags scope overreach:
- do not complete the sprint even if the feature appears functional
- record the overreach in `progress.md` only if it affects future work; leave durable learning capture to `compound-capture`
- route back to `generator-execution` with the review directives intact, or to `awaiting_human` / `escalated_to_human` when automatic correction is unsafe

## Minimum truthful outcomes

Use this table when updating state:

| Local outcome | Live feature status | Local sprint | Archive | Next route |
| --- | --- | --- | --- | --- |
| PASS with evidence | completed / done | cleared after archive verification | create `docs/archive/<id>_<timestamp>/` | `compound-capture`, then backlog routing |
| `review_failed` with evidence and retry budget | still runnable | preserve `.harness/<id>/` | none | `compound-capture`, then `generator-execution` after clean restore |
| `build_failed` with evidence and retry budget | still runnable | preserve `.harness/<id>/` | none | `compound-capture`, then `generator-execution` after clean restore |
| `awaiting_human` | parked, non-runnable | preserve `.harness/<id>/` | none | `compound-capture`, then human action or dependency-ready work |
| `escalated_to_human` | parked, non-runnable | preserve `.harness/<id>/` | none | `compound-capture`, then human intervention or dependency-ready work |
| Missing evidence | active or parked, but unresolved | preserve `.harness/<id>/` | none | reconcile evidence first |

If you cannot make the repository tell a coherent story from the files on disk, stop and preserve the sprint rather than lying with state.