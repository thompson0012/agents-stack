# orchestrator-worker model

This family uses a lead orchestrator plus fresh workers. The orchestrator reads durable state, chooses the next child skill, dispatches a new worker through whatever delegation primitive the host runtime provides, and then waits for structured outputs. It does not swap personas inline and continue inside the same context window.

Use the runtime's native primitive if it is called `sub-agent`, `Task agent`, `parallel agent`, or something else. The rule is behavioral, not API-specific: when delegation is useful, gather evidence in a fresh worker context and bring the results back to the orchestrator for the routing decision. If delegation would not materially help, or durable state already settles the answer, the orchestrator may keep the step direct.

## Lead orchestrator protections

- Keep the orchestrator thin. Its job is route, dispatch, merge, and retry orchestration.
- Prefer delegation first when the decision is ambiguous, evidence-heavy, or otherwise benefits from independent investigation. Dispatch the narrowest fresh worker or parallel workers that can gather the missing evidence, then merge their outputs before choosing the next child.
- Do not paste the full child phase prompt into the orchestrator and keep working there.
- Read durable state before dispatch. Workers should inherit the minimum exact context they need, not the entire session transcript.
- Preserve the file-based state model. The canonical outputs are still `sprint_proposal.md`, `contract.md`, `runtime.md`, `handoff.md`, `review.md`, `status.json`, and the live/archive files.
- Drain `compound_pending_feature_ids` before runnable sprint resume or new backlog selection. Compounding is explicit work, not background magic.
- Distinguish runnable active work from non-runnable brainstorm and parked work. `needs_brainstorm`, `awaiting_human`, and `escalated_to_human` stay visible, but they must not be mistaken for the one runnable active sprint.
- When no runnable active sprint exists and the compound queue is empty, choose the highest-priority dependency-ready `needs_brainstorm` item before ordinary `pending` proposal work.

## Lane walls and tool scope

Workers get only the tools their phase needs.

- Brainstorm workers may read `docs/live/*` and `docs/reference/*`, and write only `docs/live/ideas.md` plus the narrow `docs/live/features.json` update needed to track or promote the candidate.
- Proposal workers may inspect backlog and reference files, but they are not execution workers.
- Contract-review and live-review workers must stay independent and must not receive write access to implementation files.
- Execution workers may change only the approved contract scope, must perform build/startup triage before requesting review, and must not mark their own work approved.
- State-update workers reconcile state and archive history, but they do not silently redo proposal, execution, review, or durable learning capture.
- Compound workers may write `docs/live/memory.md`, optional stable reference docs, and the queue-clearing update in `docs/live/features.json`. They do not reopen sprint state or claim the runnable slot.

Treat tool scope as part of the contract. If the runtime supports per-worker tool restrictions, use them. If it does not, the orchestrator must still instruct the worker to stay inside its lane and reject mixed-phase work.

## Explicit non-runnable phase ordering

- `compound-capture` runs before runnable sprint resume or new backlog selection when `compound_pending_feature_ids` is non-empty.
- `generator-brainstorm` runs only when no runnable sprint exists and the highest-priority dependency-ready candidate still says `needs_brainstorm`.
- Neither Brainstorm nor Compound may claim `runnable_active_sprint_id` or open a second runnable sprint.

## Parallel-safe dispatch

The orchestrator may dispatch multiple sibling workers only when their work is truly independent.

- Parallelize read-only investigation freely.
- Parallelize execution only when file ownership and merge order are explicit and safe.
- Keep one phase owner per worker. Do not mix review and execution in the same worker.
- Merge sibling outputs back into the sprint's durable files before routing to the next phase.

Parallelism is optional. Fresh-worker boundaries are not.

## Subject hygiene and traceability

Every worker should be identifiable from durable state.

- Assign a stable worker ID such as `proposal-001`, `review-001`, or `exec-002`.
- Record the worker's phase and delegation kind in sprint-local state when useful, typically in `status.json`.
- Require structured returns: verdict, artifact paths written, blockers, and next-owner hints.
- Preserve prior worker evidence across retries. A retry gets a new worker ID; it does not erase the old `review.md`, `handoff.md`, or status trail.
- Record retry budgeting and restore context in durable state. `attempt_count`, `max_attempts`, and `clean_restore_ref` are part of the execution truth, not scratch notes.

Keep subjects narrow. A worker should know which sprint, which phase, which files, and which outputs it owns.

## Retry model

Retries after `build_failed` or reconciled `review_failed` are explicit orchestration events.

- Do not launch a retry until local and live state agree on the failed phase.
- Do not launch a retry unless `attempt_count < max_attempts`.
- Do not launch a retry unless `clean_restore_ref` names a safe restore boundary such as a disposable worktree, VCS snapshot, or equivalent checkpoint.
- Automatic `git reset --hard` is only acceptable in disposable workspaces and is not the default starter assumption.
- A clean retry starts a fresh execution worker. It does not reuse the previous worker context.
- If the retry is unsafe or out of budget, park the sprint in `awaiting_human` or `escalated_to_human` instead of looping.

## Build/startup triage before live review

Execution owns the first honest build/startup check.

- If the contract implies code, build, startup, or smoke verification, execution runs the minimal truthful check needed to prove the sprint is reviewable.
- If that triage fails, execution records `build_failed` with evidence in `runtime.md` or `handoff.md` and updates `status.json`.
- The orchestrator routes that failure through the execution retry path after reconciliation. It does not pay for an independent review worker just to rediscover an obvious execution-time failure.

## Human pause/edit/resume model

The file system is the human interface at pause boundaries.

- `awaiting_human` means automation has stopped at a durable checkpoint and the next change must come from a human or another explicitly human-directed edit.
- Record the human-facing truth in files, not hidden process memory: what needs editing, which files are authoritative, and where resume should begin.
- `status.json` should capture the pause reason, `resume_from`, and the exact human action required.
- `handoff.md` should explain the current state, the expected human edit or approval, and how the next agent can tell that the gate is cleared.
- Once a human changes the files, the next router pass resumes from the strongest updated artifact instead of assuming the old execution plan still applies.

## Escalation model

`escalated_to_human` is stricter than `awaiting_human`.

- Use it when retry budget is exhausted, the restore boundary is unsafe or missing, or automation cannot choose a truthful next step.
- Escalation halts automatic execution routing.
- The sprint stays visible in `.harness/` and in live state so humans can decide whether to reset, cancel, re-scope, or provide a new restore boundary.

## No nested spawning

Workers do not spawn other workers.

- If more delegation is needed, control returns to the lead orchestrator.
- Child workers must not create grandchild workers for side quests, retries, or review.
- This keeps traceability flat, tool scope understandable, and resume behavior deterministic.

## Review and contract anti-reward-hacking rule

Contract checks and independent reviews must verify state transitions, not just final snapshots.

- Validate the precondition or before-state.
- Perform the intended action or reproduction step.
- Validate the after-state and confirm the transition actually happened.
- Reject hardcoded success checks that would pass even if the action never occurred.

A worker that only proves a final static condition has not proved the contract.

## Resume and archive behavior

Fresh-worker orchestration does not change the file contracts.

- Resume from the strongest durable artifact, not from remembered chat state.
- Retries keep the same sprint folder and preserve evidence already on disk.
- PASS still archives the full sprint record, then queues explicit compounding before the next work-selection pass.
- FAIL or BLOCKED still preserves local evidence, reconciles state first, and may queue compounding before the next retry or parked-state decision.
- Parked `awaiting_human` and `escalated_to_human` sprints remain non-terminal evidence until a human decision changes them.
- Clearing `compound_pending_feature_ids` is the durable signal that the Compound phase is finished. It does not change runnable ownership by itself.

The worker model exists to protect context quality and role boundaries, not to replace the existing file-based state machine.
