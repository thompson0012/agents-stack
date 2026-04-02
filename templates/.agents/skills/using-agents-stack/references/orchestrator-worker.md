# orchestrator-worker model

This family uses a lead orchestrator plus fresh workers. The orchestrator reads durable state, chooses the next child skill, dispatches a new worker through whatever delegation primitive the host runtime provides, and then waits for structured outputs. It does not swap personas inline and continue inside the same context window.

Use the runtime's native primitive if it is called `sub-agent`, `Task agent`, `parallel agent`, or something else. The rule is behavioral, not API-specific: once the phase is chosen, continue in a fresh worker context.

## Lead orchestrator protections

- Keep the orchestrator thin. Its job is route, dispatch, merge, and retry.
- Do not paste the full child phase prompt into the orchestrator and keep working there.
- Read durable state before dispatch. Workers should inherit the minimum exact context they need, not the entire session transcript.
- Preserve the file-based state model. The canonical outputs are still `sprint_proposal.md`, `contract.md`, `handoff.md`, `review.md`, `status.json`, and the live/archive files.

## Lane walls and tool scope

Workers get only the tools their phase needs.

- Proposal workers may inspect backlog and reference files, but they are not execution workers.
- Contract-review and live-review workers must stay independent and must not receive write access to implementation files.
- Execution workers may change only the approved contract scope and must not mark their own work approved.
- State-update workers reconcile state and archive history, but they do not silently redo proposal, execution, or review work.

Treat tool scope as part of the contract. If the runtime supports per-worker tool restrictions, use them. If it does not, the orchestrator must still instruct the worker to stay inside its lane and reject mixed-phase work.

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

Keep subjects narrow. A worker should know which sprint, which phase, which files, and which outputs it owns.

## No nested spawning

Workers do not spawn other workers.

- If more delegation is needed, control returns to the lead orchestrator.
- Child workers must not create grandchild workers for side quests, retries, or review.
- This keeps traceability flat, tool scope understandable, and resume behavior deterministic.

## Resume and archive behavior

Fresh-worker orchestration does not change the file contracts.

- Resume from the strongest durable artifact, not from remembered chat state.
- Retries keep the same sprint folder and preserve evidence already on disk.
- PASS still archives the full sprint record.
- FAIL or BLOCKED still preserves local evidence and routes back through the correct phase owner.

The worker model exists to protect context quality and role boundaries, not to replace the existing file-based state machine.
