# agents-stack state machine

This reference defines the durable phase model for the starter-pack harness. The orchestrator reads these rules to decide which child skill owns the next action, then dispatches that child as a fresh worker. State comes from files, not chat memory.

## Core invariants

- Exactly one sprint may be runnable at a time.
- A selected planning workstream may also keep a local `.harness/<workstream-id>/status.json` checkpoint in `needs_brainstorm` or `pending` without claiming the runnable active sprint slot.
- Additional non-terminal sprint folders may remain in `.harness/` when they are the selected planning lane or are explicitly parked in `awaiting_human` or `escalated_to_human`.
- Parked and planning-local workspaces stay visible in durable state, but they do not count as the runnable active sprint.
- Global state in `docs/live/*` tracks project-level priority, dependencies, parked visibility, history, the live resume anchor, and the durable initiative roadmap. `docs/live/tracked-work.json` remains the only tracked-work registry and stores per-feature links such as `idea_ref`, `evidence_path`, `record_paths`, and `reference_paths`.
- Local state in `.harness/<workstream-id>/*` tracks one workstream's current planning or sprint checkpoint, retry budget, and human handoff boundary.
- Scoped durable records in `docs/records/*` may preserve discussion or sprint outputs that are not the active contract, immutable archive evidence, or current reference truth.
- Archived state in `docs/archive/<workstream-id>_<timestamp>/` preserves archived sprint artifacts after PASS archive cutover.
- A sprint is not terminal when code exists. It becomes archived only after review passes, state is updated, and the archive cutover is recorded.
- If state files disagree, later-phase artifact evidence wins over stale status declarations.
- The orchestrator routes and dispatches; each phase runs in a fresh worker with phase-scoped tools.
- Workers do not spawn other workers. If more delegation is needed, control returns to the lead orchestrator.

Evidence precedence for routing:

1. `review.md`
2. `handoff.md`
3. `runtime.md`
4. `contract.md`
5. `sprint_proposal.md`
6. `status.json`
7. `docs/live/tracked-work.json`
8. `docs/live/current-focus.md` and `docs/live/roadmap.md`
9. `docs/live/progress.md` and `docs/live/memory.md`
10. `docs/reference/*`
11. `docs/records/*`
12. `docs/archive/*` as historical evidence only

## Canonical dispatcher decision ladder

The root router keeps family-trigger judgment, broad goal-lineage interpretation, and semantic ambiguity handling. Only after that may it use `scripts/dispatch_phase.py` as the deterministic fast path for closed-world file-state routing.

1. If required live files are missing, unusable, or otherwise fail closed, route `project-initializer`.
2. If durable contradictions prevent a truthful single-lane decision, route `state-update` rather than inventing a winner.
3. If `compound_pending_feature_ids` is non-empty, route `compound-capture` before any runnable sprint resume or new backlog selection.
4. If `review.md` exists and the verdict has not yet been reconciled into local and live state, route `state-update`.
5. If exactly one runnable sprint exists, route from the strongest local artifact in precedence order: reconciled `review.md` plus `review_failed` state -> retry path candidate; `handoff.md` -> `adversarial-live-review`; `runtime.md` plus `build_failed` evidence -> retry path candidate; `contract.md` or active execution evidence -> `generator-execution`; `sprint_proposal.md` -> `evaluator-contract-review`.
6. If no runnable sprint exists but exactly one local planning workspace exists in `.harness/` with phase `needs_brainstorm` or `pending`, route from that local planning checkpoint instead of inventing a different backlog winner.
7. If the strongest durable truth is a parked `awaiting_human` or `escalated_to_human` gate with no new human edits, do not blur it into runnable work. Return `no_family_child` and surface the human boundary.
8. If no runnable sprint exists and no selected planning workspace exists, choose the highest-priority dependency-ready `needs_brainstorm` item, then the highest-priority dependency-ready `pending` item, else surface parked or dependency blockers honestly.
9. After a retry-route candidate is found, retry eligibility is still decided separately by `scripts/verify_retry_guard.py`; the dispatcher does not author that verdict.
10. After a PASS-route candidate is found, publishability is still decided separately by `state-update` plus review-convergence evidence; the dispatcher does not publish PASS.
8. After a retry-route candidate is found, retry eligibility is still decided separately by `scripts/verify_retry_guard.py`; the dispatcher does not author that verdict.
9. After a PASS-route candidate is found, publishability is still decided separately by `state-update` plus review-convergence evidence; the dispatcher does not publish PASS.
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
- Independent work may run in parallel only when the lead orchestrator starts sibling workers with non-overlapping ownership, assigns stable worker IDs, awaits every sibling return, and merges those returns into sprint-local state through a merged result ledger before phase synthesis.
- Retries do not reuse old context windows. They start a new worker and keep prior evidence on disk.
- Structured worker returns should name the stable worker ID, phase, artifact paths, blockers, and next owner when useful.

## Roadmap publication and revision

- `docs/live/tracked-work.json` still decides runnable and backlog truth, remains the only tracked-work registry, and carries durable links to ideas, scoped records, current reference docs, and each feature's single canonical `evidence_path`. `docs/live/current-focus.md` is the live resume anchor, and `docs/live/roadmap.md` is the initiative ledger for source goals, remaining slices, and re-authorization boundaries.
- Publish or revise `docs/live/roadmap.md` whenever initialization, planning, or state reconciliation turns a broad user goal into durable tracked work or changes which slices remain.
- Refresh `docs/live/current-focus.md` whenever the next owner, active lane, or strongest artifact changes.
- Neither live file becomes a second runnable contract. If a sprint is active, `.harness/<workstream-id>/contract.md` remains the slice truth. Records and reference docs stay linked through `tracked-work.json`; they do not become a second registry or a second execution contract.

## Durable records and reference links

- `docs/records/*` is for durable, traceable, scoped records from discussion or sprint work. These pages are optional and may later be promoted, superseded, or expired.
- Each record page must carry page-local provenance and validity metadata such as `scope`, `status`, `superseded_by`, and the sprint or archive contributions it summarizes.
- `docs/reference/*` remains current stable truth only. Promote record content there only when it is broadly current, then keep `tracked-work.json` traceability pointers up to date instead of inventing a second registry.
- `docs/live/progress.md` may log record creation, promotion, supersession, expiry, and archive cutover events, but it remains an append-only audit trail rather than a tracked-work index.
- Not every sprint must create a record. The absence of a record is not a state defect when `tracked-work.json`, local evidence, and archive history already tell the truth.

## Phase model

| Phase | Durable evidence | Owner skill | Meaning | Normal next step |
| --- | --- | --- | --- | --- |
| `uninitialized` | `docs/live/tracked-work.json` missing, empty, or unusable | `project-initializer` worker | Repo is not ready for sprint routing yet. | Seed durable live state, including initial focus and roadmap truth. |
| `needs_brainstorm` | `docs/live/tracked-work.json` tracks a dependency-ready item as `needs_brainstorm`, optionally with supporting notes in `docs/live/ideas.md`, and `.harness/<workstream-id>/status.json` when the item is the currently selected planning lane | `generator-brainstorm` worker | The candidate is real enough to track, but still too vague for honest proposal work. | Refine or promote it to `pending`. |
| `proposal_needed` | No runnable active sprint and at least one dependency-ready pending feature; a selected proposal lane may already have `.harness/<workstream-id>/status.json` | `generator-proposal` worker | A ready backlog item exists but no local sprint has been proposed yet. | Cut one runnable slice from the roadmap into `.harness/<feature>/sprint_proposal.md`. |
| `proposal_ready` | `sprint_proposal.md` exists | `evaluator-contract-review` worker | Proposed scope exists and needs adversarial contract review. | Approve into `contract.md` or reject with revisions. |
| `contracted` | `contract.md` exists and no later artifact exists | `generator-execution` worker | Boundaries and QA criteria are approved; implementation can begin. | Execute or resume work. |
| `executing` | `status.json` shows active execution, no later artifact exists | `generator-execution` worker | Work is underway. | Finish implementation, or record an execution-time failure honestly. |
| `build_failed` | `status.json.phase = build_failed` plus execution notes in `runtime.md` or `handoff.md` | `state-update` worker, then `compound-capture`, then orchestrator | Build, startup, or smoke-triage failed during execution, so the sprint must reconcile, compound, and then retry or escalate. | Clean-restore and retry, park for human input, or escalate. |
| `paused_by_timeout` | `status.json.phase = paused_by_timeout` | Route by `resume_from`, usually a fresh phase worker | Prior session stopped without a clean finish. | Resume from the last trustworthy checkpoint. |
| `awaiting_review` | `handoff.md` exists and `review.md` does not | `adversarial-live-review` worker | Execution claims completion and is waiting for independent review. | Review observable behavior, state transitions, and convergence metadata. |
| `review_recorded` | `review.md` exists with findings, coverage metadata, and convergence metadata | `state-update` worker | Review outcome exists and must be synchronized into durable state. PASS publishes only when convergence is closed. | Mark archived on converged PASS, reopen on FAIL or open convergence, or park/escalate on BLOCKED. |
| `review_failed` | `review.md` remains on disk; `status.json.phase = review_failed` after `state-update` reconciles a FAIL review | `state-update` worker, then `compound-capture`, then orchestrator | The failure is durable, the evidence stays attached, and the next execution loop owns the sprint only after compounding and retry gates are satisfied. | Clean-restore and retry, park for human input, or escalate. |
| `awaiting_human` | `status.json.phase = awaiting_human` plus explicit human action fields | no automatic child until human input changes files | Automation is paused at a durable file boundary for human edits, approvals, or environment intervention. | Wait for human edits, then resume from `resume_from`. |
| `escalated_to_human` | `status.json.phase = escalated_to_human` plus escalation reason | no automatic child until human decision changes files | Automatic retry must stop because attempt budget is exhausted or recovery is unsafe. | Human decides whether to reset, cancel, or re-scope. |
| `compound_pending` | `docs/live/tracked-work.json` lists the feature id in `compound_pending_feature_ids` | `compound-capture` worker | Explicit durable-learning capture must run before new work selection or runnable resume. | Capture the durable lesson or clear the queue truthfully. |
| `archived` | Artifacts moved or copied to `docs/archive/...`, live state updated, and `evidence_path` cut over | `generator-brainstorm` or `generator-proposal` worker for the next item | Sprint is archived, no longer active, and traceable through `tracked-work.json` pointers instead of a second registry. | Select the next dependency-ready `needs_brainstorm` or `pending` feature. |

## Transition rules

### Initialization, brainstorm, and proposal

- `uninitialized` -> `needs_brainstorm` or `proposal_needed`
  - Trigger: `project-initializer` worker seeds `docs/live/tracked-work.json`, `docs/live/ideas.md`, `docs/live/current-focus.md`, `docs/live/roadmap.md`, `progress.md`, and related live files truthfully.
- `needs_brainstorm` -> `proposal_needed`
  - Trigger: `generator-brainstorm` worker clarifies the candidate enough to promote it into `pending` backlog state, writes or refreshes `.harness/<workstream-id>/status.json` when the planning lane is selected, and, when needed, sharpens the roadmap slice it belongs to.
- `needs_brainstorm` -> `needs_brainstorm`
  - Trigger: the idea is still too vague for honest proposal work, so brainstorming leaves it tracked but non-runnable and preserves the planning checkpoint in `.harness/<workstream-id>/status.json` when one exists.
- `proposal_needed` -> `proposal_ready`
  - Trigger: `generator-proposal` worker advances the selected planning workspace by creating `.harness/<workstream-id>/sprint_proposal.md` and marking the sprint as proposed.
- `proposal_needed` -> `needs_brainstorm`
  - Trigger: proposal discovery proves the candidate is still too vague or forked, so it is explicitly returned to brainstorming instead of getting a mushy proposal.
- `proposal_needed` -> `proposal_needed`
  - Trigger: the highest-priority pending feature is not dependency-ready, so backlog traversal continues until a ready item is found or the queue is exhausted.

### Roadmap, focus, and drift control

- If a broad user goal or decisive outcome is not yet reflected in `docs/live/current-focus.md` plus `docs/live/roadmap.md`, publish or refresh those files before continuing serial sprint chaining.
- If `docs/live/current-focus.md`, `docs/live/roadmap.md`, or stronger evidence shows goal-lineage drift, preserve the current sprint evidence, refresh the focus anchor, revise the roadmap, and route back to `generator-brainstorm` or `generator-proposal` instead of stretching the current sprint.
- This does not create a second runnable contract or a second runnable sprint. `docs/live/tracked-work.json` still selects runnable truth, and `.harness/<workstream-id>/contract.md` remains the active slice contract.

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
  - Trigger: `adversarial-live-review` worker writes `review.md` with explicit PASS, FAIL, or BLOCKED plus findings severity labels, explicit `duplicate_of` fields, `areas_reviewed`, `areas_not_reviewed`, `coverage_status`, `convergence_status`, and `open_blocking_count`.
- `review_recorded` -> `archived`
  - Trigger: `state-update` worker processes a PASS review only after convergence is closed: `coverage_status = complete`, `convergence_status = closed`, and open non-duplicate P0 / P1 / P2 / P3 findings are zero. It then updates `docs/live/*`, cuts the feature's canonical `evidence_path` over to `docs/archive/<workstream-id>_<timestamp>/`, and archives the sprint.
- `review_recorded` -> `review_failed`
  - Trigger: `state-update` worker processes a FAIL review, or any review whose open non-duplicate P0 / P1 / P2 / P3 findings are non-zero, missing, or contradictory, increments retry metadata, preserves the evidence, and records the retry checkpoint.
- `review_recorded` -> `awaiting_human`
  - Trigger: `state-update` worker processes a BLOCKED review that requires human edits, approvals, credentials, or other intervention at a file-described pause boundary.
- `review_recorded` -> `escalated_to_human`
  - Trigger: `state-update` worker processes a BLOCKED review that cannot be retried safely or honestly by automation.
- `build_failed` -> `compound_pending`
  - Trigger: `state-update` worker publishes the failed build/startup attempt into durable live state, records retry metadata or a human gate, and queues the feature id in `compound_pending_feature_ids` before any retry is reconsidered.
- `archived`, `review_failed`, `awaiting_human`, or `escalated_to_human` -> `compound_pending`
  - Trigger: `state-update` queues the feature id in `compound_pending_feature_ids` after reconciling the decisive outcome.

### Retry, pause, escalation, and post-compound routing

Automatic retry never resumes directly from raw `build_failed` or `review_failed`. `state-update` must publish the failure first, `compound-capture` must drain any queued learning work, and only then may `generator-execution` retry.

- `compound_pending` -> `executing`
  - Trigger: the queue entry is cleared, the same sprint still remains the single runnable active sprint, the strongest durable evidence now reflects a reconciled `build_failed` or `review_failed` retry gate, and `scripts/verify_retry_guard.py` allows the retry from durable state.
- `scripts/verify_retry_guard.py` is the bounded checkable gate for these retry triggers. It reads durable retry state, returns allow/deny plus reason codes, and does not choose the next child.
- `build_failed` -> `awaiting_human`
  - Trigger: `state-update` determines retry is not yet safe because a human must edit files, repair the environment, or confirm the restore boundary, but escalation is not yet required.
- `review_failed` -> `awaiting_human`
  - Trigger: `state-update` determines fixing the failed review requires explicit human edits or approvals before another clean retry.
- `build_failed` -> `escalated_to_human`
  - Trigger: `state-update` determines `attempt_count` has reached `max_attempts` or no safe clean restore boundary exists.
- `review_failed` -> `escalated_to_human`
  - Trigger: `state-update` determines `attempt_count` has reached `max_attempts` or no safe clean restore boundary exists.
- `awaiting_human` -> route by `resume_from`
  - Trigger: a human changes the named files, updates the pause metadata, or otherwise records that the durable gate is cleared.
- `escalated_to_human` -> route by explicit human decision
  - Trigger: a human records a reset, cancellation, rescope, or new restore boundary in the files.
- `compound_pending` -> `needs_brainstorm` or `proposal_needed`
  - Trigger: the queue entry is cleared and no runnable sprint remains, so the orchestrator returns to dependency-ready backlog selection.

## PASS / BUILD_FAILED / FAIL / BLOCKED routing

### PASS path

1. `adversarial-live-review` worker writes `review.md` with PASS only after the review loop converges: `coverage_status = complete`, `convergence_status = closed`, and `open_blocking_count = 0`.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - validates the preserved convergence summary before publishing PASS
   - updates `docs/live/tracked-work.json`
   - refreshes `docs/live/current-focus.md` and `docs/live/roadmap.md` for the next authorized slice or pause boundary
   - appends outcome to `docs/live/progress.md`, including archive cutover and any record lifecycle events
   - archives the sprint to `docs/archive/<workstream-id>_<timestamp>/`
   - switches the feature's canonical `evidence_path` from `.harness/<workstream-id>/` to the archive path
   - clears runnable active-sprint status
   - queues the feature id in `compound_pending_feature_ids`
4. The next router pass selects `compound-capture`. Only after the queue is drained may the harness select new proposal work or another runnable sprint.

### BUILD_FAILED path

1. `generator-execution` worker records build/startup failure evidence in `runtime.md` or `handoff.md` and sets `status.json.phase = build_failed`.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - keeps the sprint visible in `.harness/`
   - records `build_failed` in durable live state
   - increments or validates `attempt_count` and confirms `max_attempts` for the next clean attempt
   - records or validates `clean_restore_ref` before any automatic retry
   - refreshes `docs/live/current-focus.md` and `docs/live/roadmap.md` when recovery ownership or re-authorization boundaries change
   - queues the feature id in `compound_pending_feature_ids`
   - leaves `runtime.md` on disk as evidence for the retry or escalation
   - updates global progress so the failure is visible outside the sprint folder
4. The next router pass selects `compound-capture` first. After the queue is drained, it selects `generator-execution` only if the retry is reconciled, attempts remain, and the restore boundary is safe. Otherwise the sprint moves to `awaiting_human` or `escalated_to_human`.

### FAIL path

1. `adversarial-live-review` worker writes `review.md` with FAIL and concrete directives. FAIL is mandatory whenever any open non-duplicate P0 / P1 / P2 / P3 finding remains or the required convergence metadata is missing / contradictory.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - keeps the sprint active or parks it honestly
   - records `review_failed` in durable state
   - preserves the convergence summary and open blocking findings so they remain visible until the next review loop closes them
   - increments `attempt_count` and confirms `max_attempts`
   - preserves directives and evidence
   - records or validates `clean_restore_ref` before any automatic retry
   - refreshes `docs/live/current-focus.md` and `docs/live/roadmap.md` when the remaining plan or re-authorization boundary changes
   - queues the feature id in `compound_pending_feature_ids`
   - leaves `review.md` on disk as evidence for the retry
   - updates global progress so the failure is visible outside the sprint folder
4. The next router pass selects `compound-capture` first. After the queue is drained, it selects `generator-execution` only if the retry is reconciled, attempts remain, and the restore boundary is safe. Otherwise the sprint moves to `awaiting_human` or `escalated_to_human`.

FAIL is not terminal. The review loop stays open until the preserved blockers are fixed and a later review closes convergence honestly.

### BLOCKED path

1. `adversarial-live-review` worker writes `review.md` with BLOCKED and concrete recovery steps.
2. The orchestrator selects `state-update` and dispatches a fresh worker.
3. `state-update` worker:
   - keeps the sprint visible in `.harness/`
   - records the blocker in durable state
   - decides between `awaiting_human` and `escalated_to_human`
   - refreshes `docs/live/current-focus.md` and `docs/live/roadmap.md` when the blocker changes the next authorized slice or handoff boundary
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
- `handoff.md` exists but the feature still shows `pending` in `docs/live/tracked-work.json`
- two runnable features are marked active at once
- `.harness/WORKSTREAM-001/` is parked in `awaiting_human`, but live state still treats it as the runnable active sprint
- `.harness/WORKSTREAM-002/` is `review_failed` with `attempt_count >= max_attempts`, but routing still points to execution

Handling rules:

1. Route from strongest artifact evidence, not the optimistic status field.
2. Treat contradiction as a state integrity problem, not silent success.
3. Send contradictions that require reconciliation to `state-update`.
4. If contradiction prevents choosing a single runnable sprint, `state-update` must preserve evidence and surface the conflict for human resolution rather than inventing a winner.

## Terminal state definition

A sprint is terminal only when all of the following are true:

- review passed with `coverage_status = complete`, `convergence_status = closed`, and zero open non-duplicate P0 / P1 / P2 / P3 findings
- global live state reflects the outcome and points the feature's canonical `evidence_path` at `docs/archive/<workstream-id>_<timestamp>/`
- the sprint is archived under `docs/archive/<workstream-id>_<timestamp>/`
- no runnable active status remains for that sprint in `.harness/`

Anything short of that is an open review loop, resumable work, or parked work, not an archived terminal outcome.
