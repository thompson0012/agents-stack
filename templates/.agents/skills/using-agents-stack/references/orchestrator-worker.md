# orchestrator-worker model

This family uses a lead orchestrator plus fresh workers. The orchestrator reads durable state, chooses the next child skill, dispatches a new worker through whatever delegation primitive the host runtime provides, and then waits for structured outputs. It does not swap personas inline and continue inside the same context window.

Use the runtime's native primitive if it is called `sub-agent`, `Task agent`, `parallel agent`, or something else. The rule is behavioral, not API-specific: when delegation is useful, gather evidence in a fresh worker context and bring the results back to the orchestrator for the routing decision. If delegation would not materially help, or durable state already settles the answer, the orchestrator may keep the step direct.

## Delegation constitution

This file is the canonical portable delegation constitution for the harness. It defines the reliability-first default for routing and task delegation. Project-specific architecture belongs in `docs/reference/architecture.md`; harness delegation rules belong here.

Later sections in this file contain the operational details. Use this summary as the governing default:

1. Keep the control plane thin. The orchestrator reads durable state, routes, dispatches fresh workers, merges results, and does not perform child phase work inline.
2. Planning already exists. Use brainstorm and proposal phases to turn a high-level goal into scope, dependencies, acceptance criteria, and candidate subtasks instead of adding a separate runtime planning layer.
3. Decompose only when it materially lowers uncertainty, improves verification, enables safe parallelism, reduces failure blast radius, or creates clearer ownership boundaries.
4. Keep hierarchical task trees in planning, not as router-owned runtime truth. The router selects phases from durable evidence; workers consume bounded tasks.
5. Workers own leaf tasks and phase-bounded outputs. Each worker operates at one level of abstraction and must not spawn nested workers.
6. Parallelism is bounded. Use sibling workers only for genuinely independent work, await all of them, and merge their outputs into durable state before the next routing decision.
7. Evaluation, truth publication, and learning capture remain separate. Generators do not self-approve; reviewers verify; state-update reconciles truth; compound-capture records durable lessons.
8. Files are canonical. Durable truth belongs in the appropriate live, harness, record, reference, or archive file lane rather than in chat memory.
9. Escalate complexity only when evidence justifies it. This thin-orchestrator plus specialist-worker model is the template's default, not a universal optimum for every workload.
10. Avoid router-owned recursive task trees as canonical truth, nested worker spawning, decentralized swarm coordination as the core sprint lifecycle, and collapsing planning, execution, and review into one worker.

## Lead orchestrator protections

- Keep the orchestrator thin. Its job is route, dispatch, merge, and retry orchestration.
- Prefer delegation first when the decision is ambiguous, evidence-heavy, or otherwise benefits from independent investigation. Dispatch the narrowest fresh worker or parallel workers that can gather the missing evidence, then merge their outputs before choosing the next child.
- Do not paste the full child phase prompt into the orchestrator and keep working there.
- Read durable state before dispatch. Workers should inherit the minimum exact context they need, not the entire session transcript.
- For reviewer dispatch, send only raw artifact paths and the exact neutral review question. Do not preload a verdict, preferred answer, expected winner, version ranking, provenance summary, or authorship labels that would steer judgment. See `references/dispatch-packet-examples.md` for copyable packets.
- When the review is comparative or subjective, anonymize the artifacts as A/B/C in the dispatch packet, keep the identity map out of the worker context until the review is complete, and let the reviewer form its own conclusion from the artifacts.
- Dispatch packets are routing aids, not authority. A worker must verify the claimed sprint, phase, and summary against durable files on entry, apply the `AGENTS.md` precedence chain when evidence disagrees, and stop before writing if the dispatch frame loses to stronger evidence. `references/dispatch-packet-examples.md` also includes the expected mismatch-handling pattern.
- Preserve the file-based state model. The canonical outputs are still `sprint_proposal.md`, `contract.md`, `runtime.md`, `handoff.md`, `review.md`, `status.json`, and the live/archive files.
- Drain `compound_pending_feature_ids` before runnable sprint resume or new backlog selection. Compounding is explicit work, not background magic.
- Distinguish runnable active work from non-runnable brainstorm and parked work. `needs_brainstorm`, `pending`, `awaiting_human`, and `escalated_to_human` stay visible, but they must not be mistaken for the one runnable active sprint.
- When no runnable active sprint exists and the compound queue is empty, resume the selected local planning workspace first when one exists; otherwise choose the highest-priority dependency-ready `needs_brainstorm` item before ordinary `pending` proposal work.
- Treat `docs/live/current-focus.md` as the live resume anchor and `docs/live/roadmap.md` as the initiative ledger for source goals, remaining slices, and re-authorization boundaries. Neither file replaces `.harness/<workstream-id>/contract.md` for an active sprint.
- If a user's broad goal or direction change is not yet reflected durably, pause sprint chaining long enough to publish or refresh that source-goal truth in `current-focus.md` plus `roadmap.md` before selecting the next owner.


## Deterministic dispatcher fast path

`scripts/dispatch_phase.py` is an optional read-only helper for closed-world file-state routing after the root router has already decided that the repository belongs to this family and that no semantic ambiguity requires model judgment.

- Use it only after grounding against durable files. It is not the tool for deciding whether a request is really asking for agents-stack routing, whether broad goal drift needs roadmap publication first, or whether a parked human gate was materially cleared by new edits.
- The dispatcher consumes durable state plus, when relevant, the fully merged sprint-local result ledger from any sibling evidence-gathering workers. Do not hand it partial sibling notes or bypass the await-all barrier.
- The merged result ledger is the handoff boundary from evidence gathering into deterministic routing. Stable worker IDs, artifact paths, blockers, and next-owner hints must be merged first; the dispatcher reads that reconciled ledger or the orchestrator routes directly without it.
- The dispatcher returns fixed JSON for route selection only. The orchestrator still translates that result into the root router's text output contract and performs the actual fresh-worker dispatch.
- Keep route selection separate from other gates: retry eligibility still comes from `scripts/verify_retry_guard.py`, contract approval still comes from `scripts/validate_contract.py`, review-against-contract truth still comes from `scripts/validate_review_against_contract.py`, and PASS publishability still comes from `state-update` plus review-convergence evidence rather than the dispatcher.
## Lane walls and tool scope

Workers get only the tools their phase needs.

- Brainstorm workers may read `docs/live/*` and `docs/reference/*`, and write `docs/live/ideas.md`, the narrow `docs/live/tracked-work.json` update needed to track or promote the candidate, and `.harness/<workstream-id>/status.json` when the selected tracked workstream needs a canonical planning checkpoint.
- Proposal workers may inspect backlog, `docs/live/current-focus.md`, and `docs/live/roadmap.md` to cut one runnable sprint from a broader initiative, may refresh those live planning files when proposal work legitimately re-slices what comes next, and should advance the selected workstream's `.harness/<workstream-id>/` checkpoint rather than inventing a parallel planning lane.
- Contract-review and live-review workers must stay independent and must not receive write access to implementation files.
- Execution workers may change only the approved contract scope, must perform build/startup triage before requesting review, and must not mark their own work approved.
- State-update workers reconcile state and archive history, refresh `docs/live/current-focus.md` plus `docs/live/roadmap.md` when decisive outcomes change the remaining initiative path or re-authorization boundary, and do not silently redo proposal, execution, review, or durable learning capture.
- Compound workers may write `docs/live/memory.md`, optional stable reference docs, and the queue-clearing update in `docs/live/tracked-work.json`. They do not reopen sprint state or claim the runnable slot.

Treat tool scope as part of the contract. If the runtime supports per-worker tool restrictions, use them. If it does not, the orchestrator must still instruct the worker to stay inside its lane and reject mixed-phase work.

## Explicit non-runnable phase ordering

- `compound-capture` runs before runnable sprint resume or new backlog selection when `compound_pending_feature_ids` is non-empty.
- `generator-brainstorm` runs only when no runnable sprint exists and the selected local planning workspace or highest-priority dependency-ready candidate still says `needs_brainstorm`.
- Neither Brainstorm nor Compound may claim `runnable_active_sprint_id` or open a second runnable sprint; brainstorming may keep `.harness/<workstream-id>/status.json` as canonical planning evidence without making the lane runnable.

## Parallel-safe dispatch

The orchestrator may dispatch multiple sibling workers only when their work is truly independent.

- Parallelize read-only investigation freely.
- Parallelize execution only when file ownership and merge order are explicit and safe.
- Keep one phase owner per worker. Do not mix review and execution in the same worker.
- After any sibling dispatch, enter a hard await-all barrier. If any sibling worker is still pending, the orchestrator must not emit a completion message, final synthesis, next-owner decision, or dispatcher call.
- Merge sibling outputs only after every dispatched sibling has returned, then write one merged result ledger in sprint-local durable state before routing to the next phase or invoking the dispatcher fast path.
- Emit one synthesis for that worker batch only after the merged ledger is complete, and name the stable worker IDs, artifact paths, blockers, and next owner explicitly.

Parallelism is optional. Fresh-worker boundaries are not.

## Subject hygiene and traceability

Every worker should be identifiable from durable state.

- Assign a stable worker ID such as `proposal-001`, `review-001`, or `exec-002`.
- Record the worker's phase and delegation kind in sprint-local state when useful, typically in `status.json`.
- Require structured returns keyed by stable worker ID: verdict, artifact paths written, blockers, and next-owner hints.
- Record sibling worker returns in one merged durable ledger rather than scattered freeform summaries, typically as a structured `worker_results` block in sprint-local state such as `status.json`.
- The merged ledger is the orchestrator's basis for synthesis, retry decisions, and the next dispatch; freeform prose may explain it, but it does not replace the ledger.
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
- Use `scripts/verify_retry_guard.py` as the bounded allow/deny check for this retry gate. It reads durable retry state, returns verdict plus reason codes, and does not select the next child for you.

## Failure-owner shorthand

Use these classifications when choosing the next lane after a decisive outcome:

- Implementation defect: the approved slice stands, but execution or review proved the implementation inside it is wrong. Route through `state-update`, drain `compound-capture`, then retry with `generator-execution` from a clean restore boundary.
- Slice-contract defect: the slice, file bounds, or acceptance criteria were wrong or incomplete. Freeze the evidence, then route to `evaluator-contract-review` or `generator-proposal` instead of patching in execution.
- Orchestration/state defect: live state, local artifacts, or resume metadata disagree. Route to `state-update`; use `project-initializer` only when the live state model itself is untrustworthy.
- Environment blocker: external runtime, credential, dependency, or operator conditions prevented honest judgment. Park or escalate until a human or a named recovery path owns it.
- Goal-lineage drift: `docs/live/current-focus.md`, `docs/live/roadmap.md`, or stronger evidence shows the sprint is no longer the right slice for the active objective. Refresh the focus anchor, revise the roadmap, and route back to brainstorm or proposal rather than forcing execution to absorb the drift.


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

- Resume from the strongest durable artifact, using `docs/live/current-focus.md` as the resume pointer and `docs/live/roadmap.md` as the initiative ledger for what remains. Neither file replaces `.harness/<workstream-id>/contract.md` for active-sprint truth.
- Retries keep the same sprint folder and preserve evidence already on disk.
- PASS still archives the full sprint record, refreshes `docs/live/current-focus.md` and `docs/live/roadmap.md` as needed, then queues explicit compounding before the next work-selection pass.
- FAIL or BLOCKED still preserves local evidence, reconciles state first, refreshes `docs/live/current-focus.md` and `docs/live/roadmap.md` when the remaining path changes, and may queue compounding before the next retry or parked-state decision.
- Parked `awaiting_human` and `escalated_to_human` sprints remain non-terminal evidence until a human decision changes them.
- Clearing `compound_pending_feature_ids` is the durable signal that the Compound phase is finished. That may mean durable learning was extracted or that extraction was deliberately skipped because no durable lesson survived.

The worker model exists to protect context quality and role boundaries, not to replace the existing file-based state machine.
