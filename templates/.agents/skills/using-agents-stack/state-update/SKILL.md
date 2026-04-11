---
name: state-update
purpose: Synchronize decisive sprint outcomes back into durable project state, preserving evidence and making the next phase explicit.
trigger: After `adversarial-live-review` has written a decisive review outcome, or after execution has written a decisive non-review state such as `build_failed`, `awaiting_human`, or `escalated_to_human`.
inputs:
  - AGENTS.md
  - docs/live/tracked-work.json
  - docs/live/current-focus.md
  - docs/live/roadmap.md
  - docs/live/progress.md
  - .harness/<sprint-id>/contract.md
  - .harness/<sprint-id>/runtime.md
  - .harness/<sprint-id>/handoff.md
  - .harness/<sprint-id>/qa.md
  - .harness/<sprint-id>/review.md
  - .harness/<sprint-id>/status.json
outputs:
  - updated docs/live/tracked-work.json
  - updated docs/live/current-focus.md
  - updated docs/live/roadmap.md
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
  - evaluator-contract-review
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
- each feature entry keeps one canonical `evidence_path`, plus truthful `record_paths` and `reference_paths`, inside `docs/live/tracked-work.json` rather than scattering registry state elsewhere

## Worker Dispatch Contract

- Run state reconciliation in a fresh worker context. The orchestrator dispatches this worker after review or execution triage; it does not perform state-update inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: durable state and archive operations only: `docs/live/tracked-work.json`, `docs/live/current-focus.md`, `docs/live/roadmap.md`, `docs/live/progress.md`, `.harness/<sprint-id>/*`, and `docs/archive/*` as required by the outcome. No product-code edits, no proposal rewriting, no new implementation work, and no `docs/live/memory.md` edits.
- Not parallel-safe. This worker owns the single runnable active sprint's global reconciliation, archive decision, compounding queue update, roadmap truth, and focus-anchor refresh; do not split or race writes across multiple workers.
- Before publishing tracked-work or progress mutations from a review outcome, run `templates/.agents/skills/using-agents-stack/scripts/validate_state_update.py` against the durable files. Trust the merged review convergence summary only after the reviewer await-all synthesis barrier has produced one decisive record and merged result ledger.
- Durable return contract: updated `docs/live/tracked-work.json`, `docs/live/current-focus.md`, `docs/live/roadmap.md`, `docs/live/progress.md`, `.harness/<sprint-id>/status.json`, and PASS-path archive contents. Include stable `worker_id` / `orchestrator_run_id` in the updated status or ledger entry when the host provides them, and preserve review convergence data instead of recomputing it from chat summaries.
- Dispatch framing is non-authoritative. Before reconciling state, verify that the dispatched sprint still matches `docs/live/tracked-work.json`, that the claimed decisive phase still matches the strongest local artifact on disk, and that stronger evidence in the `AGENTS.md` precedence chain beats any dispatch summary, stale resume hint, or copied orchestrator context.
- If those checks disagree with the dispatch frame, stop before writing live or sprint state, preserve the existing truthful files, and hand control back to the orchestrator for correct-lane dispatch.

## Mandatory verification before any update

Before touching global state, identify which decisive phase actually happened.

### Review-driven outcomes
If `status.json` or `review.md` says the sprint was reviewed, confirm all of the following:
1. `.harness/<sprint-id>/review.md` exists.
2. `.harness/<sprint-id>/qa.md` exists or `review.md` explicitly embeds equivalent evidence.
3. The review decision is unambiguous: `PASS`, `FAIL`, or `BLOCKED`.
4. The review findings list is present, every finding has a severity label, and every finding carries an explicit `duplicate_of` value.
5. Coverage metadata is present: `areas_reviewed`, `areas_not_reviewed`, and `coverage_status`.
6. Convergence metadata is present: `convergence_status` and `open_blocking_count`.
7. `templates/.agents/skills/using-agents-stack/scripts/validate_state_update.py` returns `allow` for any PASS publication and explains any denial with reason codes.
8. `status.json` points to the review checkpoint.
9. The reviewed sprint matches the backlog item recorded in `docs/live/tracked-work.json`.

### Execution-triage outcomes
If `status.json` says `build_failed`, `awaiting_human`, or `escalated_to_human`, confirm all of the following:
1. `.harness/<sprint-id>/runtime.md` exists.
2. `.harness/<sprint-id>/handoff.md` exists.
3. The failure, pause, or escalation reason is explicit.
4. `status.json` includes any relevant `attempt_count`, `max_attempts`, and `clean_restore_ref` fields.
5. The sprint matches the backlog item recorded in `docs/live/tracked-work.json`.

If the required evidence for the claimed phase is missing, stop. Do not mark the sprint complete, do not archive it, and do not advance the backlog. Missing evidence is a data-integrity problem.

## Sources of truth by decision type

- `review.md` decides PASS vs FAIL vs BLOCKED.
- `qa.md` proves what was actually checked during review.
- `contract.md` defines the scope that was supposed to be delivered.
- `runtime.md` and `handoff.md` explain how the result was produced, where triage failed, or how a human can resume.
- `status.json` carries the current local routing truth, including attempt budgeting and clean restore metadata.
- `docs/live/tracked-work.json` is the authoritative tracked-work ledger that must now be synchronized.
- `docs/live/progress.md` is the reviewed-outcome ledger that must record what changed.
- The review convergence summary decides whether PASS may be published: `coverage_status` must be `complete`, `convergence_status` must be `closed`, and `open_blocking_count` must be zero.
- If review metadata is missing, contradictory, or denied by `validate_state_update.py`, fail closed. Preserve the sprint and publish the inconsistency instead of archiving optimistically.

## Failure-owner classification

Before publishing `next_action` or refreshing `docs/live/current-focus.md` / `docs/live/roadmap.md`, classify the decisive issue truthfully:

- Implementation defect: the approved slice still stands, but execution or review proved the implementation inside it is wrong. Next owner: `generator-execution` after reconciliation and explicit compounding.
- Slice-contract defect: the strongest evidence shows the slice, file bounds, or acceptance criteria were wrong or incomplete. Next owner: `evaluator-contract-review` for contract repair, or `generator-proposal` when the slice itself must be re-cut.
- Orchestration/state defect: local artifacts, `status.json`, `tracked-work.json`, `current-focus.md`, or `roadmap.md` disagree, or the resume checkpoint is missing. Next owner: `state-update`, or `project-initializer` when the live state model itself is untrustworthy.
- Environment blocker: runtime, credential, dependency, or operator conditions prevented an honest PASS/FAIL. Next owner: human unless a named clean recovery path already makes `generator-execution` responsible for the retry.
- Goal-lineage drift: the strongest evidence, `docs/live/current-focus.md`, or `docs/live/roadmap.md` shows the sprint is no longer the right slice for the active source goal. Next owner: `generator-brainstorm` or `generator-proposal` only after the roadmap and focus anchor are refreshed and any further sprint chaining is paused pending re-authorization.


## Update procedure

### 1. Validate the decisive outcome

Read the strongest local artifact for the current phase and extract:
- final status or parked phase
- satisfied or failed contract criteria
- corrective directives or human actions
- any explicit scope violations
- any unexecuted checks or unverifiable claims
- review coverage metadata: `areas_reviewed`, `areas_not_reviewed`, and `coverage_status` when review drove the outcome
- review convergence metadata: `convergence_status`, `open_blocking_count`, and the canonical open non-duplicate P0 / P1 / P2 / P3 finding ids when review drove the outcome
- retry state: `attempt_count`, `max_attempts`, and `clean_restore_ref`

If local evidence and `status.json` disagree, preserve the sprint as active or parked and record the discrepancy in `progress.md` rather than pretending the outcome is settled.

### 2. Update `docs/live/tracked-work.json`

This file is the project-wide backlog state.
It must distinguish runnable active work from parked non-terminal work and from queued compounding work.
It is not the place to hide non-runnable initiative decomposition; that belongs in `docs/live/roadmap.md`.

At minimum, publish truthfully:
- which sprint, if any, is the single runnable active sprint
- which sprint ids are parked in `awaiting_human` or `escalated_to_human`
- which feature ids are waiting in `compound_pending_feature_ids` for explicit Compound work
- each touched feature's terminal or non-terminal status, owner, attempt count, max attempts, clean restore reference, and next action when those fields exist locally
- when review drove the outcome, the preserved convergence summary that explains whether PASS is closed or which open P0 / P1 / P2 / P3 findings still block completion
- the feature's one canonical `evidence_path`: `.harness/<sprint-id>/...` while active or parked, `docs/archive/<sprint-id>_<timestamp>/...` after PASS archive cutover
- any truthful `idea_ref`, `record_paths`, and `reference_paths` already attached to that feature so live state remains the single registry for durable traceability

#### Queue compounding explicitly
After reconciling any decisive outcome, add the feature id to `compound_pending_feature_ids` unless it is already present.

Queueing compounding means:
- the outcome is now published and stable enough for learning capture
- the next durable learning pass belongs to `compound-capture`, not to `state-update`
- the queue does not claim `runnable_active_sprint_id`
- the queue does not reopen execution or review

#### On PASS
- publish PASS only when the review verdict is PASS, `templates/.agents/skills/using-agents-stack/scripts/validate_state_update.py` returns `allow`, `coverage_status` is `complete`, `convergence_status` is `closed`, and `open_blocking_count` is `0`
- mark the sprint feature with the repository's terminal status name `archived` after the PASS archive cutover completes
- remove it from the runnable active slot and from any parked list
- switch the feature's canonical `evidence_path` from `.harness/<sprint-id>/...` to the resulting `docs/archive/<sprint-id>_<timestamp>/...` bundle
- preserve identifiers, priority, dependencies, `idea_ref`, `record_paths`, `reference_paths`, and any useful completion metadata already used by the template
- keep the feature id in `compound_pending_feature_ids` until `compound-capture` finishes

#### On `review_failed` or `build_failed`
- keep the same feature as the runnable active sprint only if an automatic retry is still safe
- copy `attempt_count`, `max_attempts`, `clean_restore_ref`, and the failure phase into the backlog entry
- when the failure came from review, preserve `coverage_status`, `convergence_status`, `open_blocking_count`, and the canonical open non-duplicate P0 / P1 / P2 / P3 finding ids so those blockers keep the sprint active until the next review loop closes them
- set `next_action` to a clean retry through `generator-execution`, never to live review directly
- if review metadata is missing or `validate_state_update.py` denies PASS publication, fail closed: preserve the sprint, publish the denial reason codes, and do not archive
- if `attempt_count >= max_attempts` or no safe clean restore boundary exists, convert the live feature state to `escalated_to_human` instead of advertising an automatic retry
- `scripts/verify_retry_guard.py` is the bounded retry-eligibility check for this handoff back to execution. If it denies, keep the sprint in reconciliation or human-gated state instead of advertising an automatic retry
- keep the feature id queued in `compound_pending_feature_ids` so the explicit Compound phase can decide whether any durable lesson survives before the next proposal cycle

#### On `awaiting_human`
- keep the sprint in the backlog and `.harness/`, but do not count it as the runnable active sprint
- publish the required human action, affected artifacts, and resume condition
- keep the feature's canonical `evidence_path` pointed at `.harness/<sprint-id>/...`
- add the sprint id to the parked list
- keep the feature id queued in `compound_pending_feature_ids` until compounding clears it

#### On `escalated_to_human`
- keep the sprint in the backlog and `.harness/`, but do not count it as the runnable active sprint
- publish the escalation reason, exhausted attempt budget or unsafe recovery condition, and the evidence path the human should inspect
- keep the feature's canonical `evidence_path` pointed at `.harness/<sprint-id>/...`
- add the sprint id to the parked list
- keep the feature id queued in `compound_pending_feature_ids` until compounding clears it

Do not invent a new schema casually. Extend only when necessary and keep it consistent.

### 3. Refresh `docs/live/roadmap.md` when goal truth changed

> Treat this file as the non-runnable initiative control plane, not as the sprint selector.

Refresh it whenever the decisive outcome changes what the repository can honestly say about the source goal, authorized initiative slice, or deferred follow-on work.

At minimum, make explicit:
- the source goal or user-request lineage the current sprint belongs to
- the currently authorized initiative or slice
- deferred later work that remains outside the current sprint
- any newly discovered scope that requires re-authorization before another sprint can be reserved or chained forward
- the evidence path that justified the roadmap change

If late scope discovery or goal-lineage drift appears after execution or review started, pause further sprint chaining. Update the roadmap to show the new boundary first, then route back to `generator-proposal` or `generator-brainstorm` instead of silently appending follow-on work.

### 4. Refresh `docs/live/current-focus.md`

> Treat this file as a live resume aid, not a second contract.

Rewrite or refresh a concise anchor that states:
- the current objective and why it is the objective now
- the goal lineage from source goal to authorized roadmap slice to active or parked sprint, or to the next backlog lane when no sprint is runnable
- the decisive artifact path a cold-start agent should open next
- the next owner and exact resume lane, using the failure-owner classification above when applicable

Keep the focus note complementary:

- `docs/live/tracked-work.json` still owns backlog truth, runnable ownership, parked state, and compound queue state
- `docs/live/roadmap.md` owns the non-runnable initiative decomposition and re-authorization boundaries
- `docs/live/progress.md` still owns the outcome ledger
- `.harness/<sprint-id>/contract.md` still owns active-sprint execution scope
- `docs/live/memory.md` still owns cross-sprint learning written by explicit compounding

For active or parked sprints, point back to `.harness/<sprint-id>/contract.md`, `review.md`, `handoff.md`, or `runtime.md` instead of restating the full contract. If no sprint is runnable, make the next backlog lane or parked blocker explicit without inventing a second control plane.

### 5. Update `docs/live/progress.md`

> The progress ledger records what happened; the focus anchor records what matters next.

Append a dated ledger entry that includes:
- sprint id and title
- PASS, FAIL, BLOCKED, BUILD_FAILED, AWAITING_HUMAN, or ESCALATED_TO_HUMAN status
- concise summary of what changed, what failed, or what blocked progress
- the same canonical evidence path published in `docs/live/tracked-work.json` (`.harness/...` while active or parked, `docs/archive/...` after archive)
- attempt count and max attempts when retry budgeting matters
- clean restore expectation when another execution pass is possible
- when review drove the outcome, `coverage_status`, `convergence_status`, `open_blocking_count`, and the canonical open blocker ids or denial reason codes that explain why PASS is still blocked
- whether the feature was queued for explicit Compound work
- next recommended action

For `review_failed` or `build_failed`, the next action should point back to the same sprint, the corrective directives, the required clean restore boundary, and any still-open blocking findings that must be cleared before rerunning review.
For `awaiting_human`, the next action should point to the exact file edits, approval, or manual recovery the human must complete.
For `escalated_to_human`, the next action should halt automatic retry and name the evidence bundle the human should inspect before resuming.
For PASS, the next action should point to `compound-capture` first when `compound_pending_feature_ids` is non-empty, then to backlog selection once compounding is clear. `progress.md` stays the append-only outcome ledger, not a second registry for record or reference links.

### 6. Preserve or archive sprint artifacts truthfully

## FAIL path: preserve, do not archive on FAIL

On `review_failed`:
- keep `.harness/<sprint-id>/` intact
- keep `contract.md`, `runtime.md`, `handoff.md`, `qa.md`, `review.md`, and `status.json`
- update `status.json` to reflect that the sprint remains active, for example:
  - `phase: "review_failed"`
  - `owner_role: "orchestrator"`
  - `resume_from: "review.md"`
- preserve `attempt_count`, `max_attempts`, and `clean_restore_ref`
- preserve the review convergence summary and any open non-duplicate P0 / P1 / P2 / P3 blockers so they remain visible in live state and progress until the next review loop closes them
- synchronize `docs/live/tracked-work.json` and `docs/live/progress.md` so the sprint stays open, the failure is visible, and the next action points to a clean retry through `generator-execution`
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

A blocked sprint is not archived work.

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
1. Run `templates/.agents/skills/using-agents-stack/scripts/validate_state_update.py <sprint-id> --repo-root <repo-root>` and continue only when it returns `allow`.
2. Verify the review evidence is complete and that the preserved convergence summary still says `coverage_status: complete`, `convergence_status: closed`, and `open_blocking_count: 0`.
3. Update `docs/live/*` first, including the feature's `archived` terminal status and the archive-bound `evidence_path`.
4. Archive the full sprint artifact set to `docs/archive/<sprint-id>_<timestamp>/`.
5. Ensure the archive contains, at minimum:
   - `sprint_proposal.md` if it exists
   - `contract.md`
   - `handoff.md`
   - `review.md`
   - `status.json`
   - `runtime.md` when execution produced runtime notes
   - `qa.md` when the review produced a separate QA evidence log
6. Update `status.json` to a terminal archived state, for example:
   - `phase: "archived"`
   - `owner_role: "none"`
   - `resume_from: "docs/archive/<sprint-id>_<timestamp>/review.md"`
7. Remove or clear the active sprint workspace only after the archive copy is confirmed and the harness's single-runnable-sprint rule is preserved.
8. Leave the feature id queued in `compound_pending_feature_ids` until `compound-capture` processes the archived evidence.
9. Keep any existing `record_paths` and `reference_paths` registered on the feature entry; state-update moves the evidence pointer, it does not create a second registry.

Never archive a sprint if review failed, build/startup triage failed, review convergence is still open, or evidence is missing.

## Routing rules

### After PASS
Route toward the explicit Compound stage first when work is queued:
- if `compound_pending_feature_ids` is non-empty, next skill is `compound-capture`
- once compounding is clear, if another dependency-ready `needs_brainstorm` feature exists, next skill is usually `generator-brainstorm`
- once compounding is clear, if another dependency-ready `pending` feature exists, next skill is usually `generator-proposal`
- if the harness requires re-initialization or backlog refresh, route accordingly from global state

The archived sprint should no longer be the active work packet.

### After `review_failed` or `build_failed`
- queue the feature for `compound-capture` as part of the decisive outcome publication
- after compounding clears, route back to `generator-execution` on the same sprint only when `attempt_count < max_attempts`, `clean_restore_ref` is present and credible, live state makes the clean retry requirement explicit, and any preserved open blockers still point at implementation work rather than contract or state defects
- otherwise route to `escalated_to_human`

### After `awaiting_human` or `escalated_to_human`
Keep the sprint parked, preserve the blocker or escalation evidence, and stop automatic phase advancement on that sprint until the required human action is completed.

If compounding is pending, route to `compound-capture` before opening new brainstorm or proposal work. Compounding does not make the parked sprint runnable again.

## Edge-case rules

### Review evidence is missing
If `review.md` exists but no evidence supports it, or the required coverage / convergence metadata is missing:
- do not mark PASS, FAIL, or BLOCKED into global state as final
- leave the sprint active
- record the inconsistency and any `validate_state_update.py` denial reason codes in `progress.md`
- route back for a proper review, not for fresh implementation

### Build/startup evidence is missing
If `status.json` says `build_failed` but `runtime.md` or `handoff.md` does not prove the failed attempt:
- do not publish an automatic retry as safe
- park the sprint in `awaiting_human` or `escalated_to_human`
- record the inconsistency in `progress.md`

### Late scope discovery changed the roadmap
If review or execution proves the current sprint no longer matches the authorized roadmap slice:
- refresh `docs/live/roadmap.md` and `docs/live/current-focus.md` before advertising any next sprint
- clear any implied sprint chaining that depended on the old boundary
- keep the current sprint active, parked, or failed according to the real evidence; do not relabel it as a clean success
- route back to `generator-proposal` or `generator-brainstorm` when a new slice must be authorized, or to `evaluator-contract-review` when only the contract needs repair

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
| PASS with closed convergence evidence | archived | cleared after archive verification | create `docs/archive/<id>_<timestamp>/` and switch `evidence_path` there | `compound-capture`, then backlog routing |
| `review_failed` with evidence and retry budget | still runnable | preserve `.harness/<id>/` and keep `evidence_path` there | none | `compound-capture`, then `generator-execution` after clean restore and blocker preservation |
| `build_failed` with evidence and retry budget | still runnable | preserve `.harness/<id>/` and keep `evidence_path` there | none | `compound-capture`, then `generator-execution` after clean restore |
| `awaiting_human` | parked, non-runnable | preserve `.harness/<id>/` and keep `evidence_path` there | none | `compound-capture`, then human action or dependency-ready work |
| `escalated_to_human` | parked, non-runnable | preserve `.harness/<id>/` and keep `evidence_path` there | none | `compound-capture`, then human intervention or dependency-ready work |
| Missing evidence or open convergence | active or parked, but unresolved | preserve `.harness/<id>/` and keep `evidence_path` there | none | reconcile evidence first |

If you cannot make the repository tell a coherent story from the files on disk, stop and preserve the sprint rather than lying with state.