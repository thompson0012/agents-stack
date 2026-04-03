# Architecture Reference

This starter uses a file-backed orchestrator-worker harness. Repository files are durable state. Chat context, inline persona swaps, and script memory are disposable.

## Canonical topology

- `AGENTS.md`: operating contract for the whole repo.
- `docs/reference/architecture.md`: stable technical boundaries and orchestration rules.
- `docs/reference/design.md`: stable UI quality bar and review expectations.
- `docs/live/features.json`: machine-readable backlog, dependency graph, idea backlog pointer, compound queue, and runnable active sprint pointer.
- `docs/live/ideas.md`: pre-sprint ideation backlog. It stores exploration detail, candidate framing, and brainstorm notes, but it is not the authoritative runnable schedule.
- `docs/live/progress.md`: append-only ledger of shipped, failed, paused, escalated, and compounded outcomes.
- `docs/live/memory.md`: durable learnings captured after publication by the compound phase.
- `.harness/<feature-id>/`: the only place for sprint-local execution state while the sprint is runnable or human-gated.
- `docs/archive/<feature-id>_timestamp/`: immutable historical sprint artifacts after PASS, state publication, and compound queueing.
- `docs/scripts/*`: optional helpers; never the source of truth for state.

## Phase chain

The harness lifecycle is explicit:

`Brainstorm -> Plan -> Work -> Review -> State Update -> Compound -> Repeat`

- **Brainstorm** is pre-sprint and non-runnable. It deepens `needs_brainstorm` backlog items in `docs/live/ideas.md` and may promote a candidate into proposal-ready backlog state, but it must not claim `runnable_active_sprint_id`.
- **Plan** is `generator-proposal` plus `evaluator-contract-review`.
- **Work** is contract-bound execution with build/startup triage before review.
- **Review** is independent adversarial verification.
- **State Update** reconciles review truth into `docs/live/features.json` and `docs/live/progress.md`, archives PASS results, and queues compounding in `compound_pending_feature_ids`.
- **Compound** is post-publication and non-runnable. `compound-capture` records durable learnings in `docs/live/memory.md`, updates reference docs when warranted, and clears the queue.

## Orchestrator-worker model

The `using-agents-stack` router is an orchestrator, not a phase worker.

- The orchestrator reads durable state, selects the next phase, and dispatches a fresh worker with a clean context window.
- If the host runtime does not expose a literal `spawn_subagent` API, use its delegation primitive instead: sub-agent, Task agent, parallel worker, or equivalent.
- The orchestrator never performs child phase work inline. Brainstorm, proposal, execution, review, state publication, and compound capture each run in their own fresh worker.
- Workers return structured results through durable artifacts in `.harness/<feature-id>/` and `docs/live/*`; those files remain the source of truth.
- Only the orchestrator may delegate. Workers must not spawn nested workers.
- Every worker dispatch should be traceable in state with a worker id, subject, tool-scope profile, and spawn depth when those fields matter.

## Tool-scope lanes

Tool access is a hard boundary, not a suggestion.

- The orchestrator gets state inspection and delegation tools only.
- `project-initializer`, `generator-brainstorm`, `generator-proposal`, `generator-execution`, `state-update`, and `compound-capture` get only the write surface needed for the files they own.
- `evaluator-contract-review` and `adversarial-live-review` are evaluators. They must not receive general write access to product code or global state; if they need to return an artifact, the path must be narrowed to that artifact only.
- Workers do not widen their own scope, reach across phase boundaries, or keep hidden state outside the file handoff.

## Parallel work rules

Parallel workers are allowed only when the work is independent and non-overlapping.

- File ownership must not overlap unless the orchestrator can merge outputs without ambiguity.
- Parallel review or evaluation is safe only when each worker writes to its own artifact or returns structured findings for the orchestrator to reconcile.
- Do not use parallel workers to simulate nested delegation inside a worker. Parallelism still starts at the orchestrator.

## State locations and precedence

1. Human edits and explicit user instructions.
2. Active sprint-local state in `.harness/<active-feature>/`, especially `contract.md`, `runtime.md`, `handoff.md`, `review.md`, and `status.json`.
3. Global live state in `docs/live/features.json`, `docs/live/ideas.md`, `docs/live/progress.md`, and `docs/live/memory.md`.
4. Stable reference intent in `docs/reference/*`.
5. Derived outputs from `docs/scripts/*` or ad hoc tooling.

Use local state to decide how to continue the runnable sprint. Use global state to decide what the project should work on next and whether non-runnable brainstorm or compound work is queued. If they disagree, resolve the conflict explicitly; do not silently invent a merge.

## Runnable versus non-runnable semantics

Exactly one sprint may be runnable at a time.

- Runnable phases are the phases automation may continue immediately for one sprint, such as `proposed`, `contracted`, `in_progress`, `build_failed`, `in_review`, or `review_failed` once the retry preconditions are met.
- Parked phases are `awaiting_human` and `escalated_to_human`. These sprints remain in `.harness/`, but they do not count as the runnable active sprint.
- Brainstorm and Compound are explicit non-runnable phases. They may be the router's next action, but they must not claim `runnable_active_sprint_id` or open a second sprint.
- A parked sprint must include durable pause or escalation metadata explaining what changed, what the human must do, and which phase resumes next.
- When no sprint is runnable, the orchestrator drains `compound_pending_feature_ids` first, then selects the highest-priority dependency-ready `needs_brainstorm` item, then the highest-priority dependency-ready `pending` item.

## Retry safety and clean restore boundaries

Retries after `review_failed` or `build_failed` must start from a named clean restore boundary.

- Store that boundary in durable state such as `clean_restore_ref`.
- The boundary may be a disposable worktree, VCS snapshot, or another truthful restore reference.
- Do not rely on an unconditional `git reset --hard` as default starter behavior. Destructive reset is only appropriate in disposable workspaces where the restore boundary is explicit.
- Retry metadata must also include `attempt_count` and `max_attempts` so the orchestrator can stop before looping indefinitely.
- If the clean restore boundary is missing or the attempt budget is exhausted, automation must halt and the sprint moves to `awaiting_human` or `escalated_to_human`.

## Build triage before live review

Execution is responsible for proving the sprint is reviewable before the review worker is dispatched.

- If the implementation cannot build, boot, or reach the declared startup checkpoint, record `build_failed` in sprint-local state.
- A `build_failed` sprint goes back to execution after the clean restore preconditions are satisfied.
- Do not pay for an adversarial live review worker when the product never reached a reviewable state.

## Resume, publication, and archive procedure

- Resume by reading `docs/live/features.json`, then `.harness/<feature-id>/status.json`, then the strongest local artifact named by `resume_from`.
- Treat `status.json` as dispatch metadata for the next fresh worker, not as permission for the orchestrator to do that worker's phase inline.
- Keep implementation notes, build triage, handoff context, worker trace metadata, and review findings inside the active sprint folder while work is live.
- Human pause/edit/resume happens through durable artifacts. `awaiting_human` means the file system is the handoff boundary: a human edits or approves the named artifact, then the next worker resumes from the updated checkpoint.
- `escalated_to_human` means automation must stop until a human changes the plan, replaces the restore boundary, resets the attempt budget, or closes the sprint.
- After a sprint passes review, `state-update` updates `docs/live/features.json`, appends `docs/live/progress.md`, archives or snapshots the sprint to `docs/archive/<feature-id>_<timestamp>/`, clears the runnable active sprint, and queues the feature id in `compound_pending_feature_ids`.
- `compound-capture` consumes that queue, writes durable learnings to `docs/live/memory.md`, updates reference docs when they changed materially, and clears the processed queue entries.
- Never mix archived artifacts back into `.harness/`; active and historical state must stay separate.

## Dependency-aware backlog selection

When there is no runnable active sprint and no compound queue, the orchestrator chooses the next backlog item from `docs/live/features.json` by dependency readiness, not by naive list order.

- Consider `needs_brainstorm` items first.
- If no dependency-ready `needs_brainstorm` item exists, consider dependency-ready `pending` items.
- A candidate is ready only when every declared dependency is already complete, archived, or otherwise marked satisfied in durable backlog state.
- Among dependency-ready items of the same status, choose the highest-priority candidate according to the backlog's durable ordering fields.
- If dependency data is missing, malformed, or contradictory, surface that clearly and stop. The helper must not invent a feature choice.

## Review truthfulness requirements

Reviewers verify state transitions, not static screenshots of the end state.

- Acceptance checks must capture before/action/after evidence.
- Reviews must reject hardcoded pass conditions, mock-only success signals, or assertions that can pass without exercising the real behavior.
- `BLOCKED` is a review verdict. `state-update` must translate it into `awaiting_human` or `escalated_to_human` so later agents know whether the sprint is resumable or halted.
