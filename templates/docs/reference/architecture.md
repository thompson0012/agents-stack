# Architecture Reference

This starter uses a file-backed orchestrator-worker harness. Repository files are durable state. Chat context, inline persona swaps, and script memory are disposable.

## Canonical topology

- `AGENTS.md`: operating contract for the whole repo.
- `docs/reference/architecture.md`: stable technical boundaries and state precedence.
- `docs/reference/design.md`: stable UI quality bar and review expectations.
- `docs/live/features.json`: machine-readable backlog and active sprint pointer.
- `docs/live/progress.md`: append-only ledger of shipped or archived outcomes.
- `docs/live/memory.md`: durable learnings, environment quirks, and conventions.
- `.harness/<feature-id>/`: the only place for active sprint-local execution state.
- `docs/archive/<feature-id>_timestamp/`: immutable historical sprint artifacts after closure.
- `docs/scripts/*`: optional helpers; never the source of truth for state.

## Orchestrator-worker model

The `using-agents-stack` router is an orchestrator, not a phase worker.

- The orchestrator reads durable state, selects the next phase, and dispatches a fresh worker with a clean context window.
- If the host runtime does not expose a literal `spawn_subagent` API, use its delegation primitive instead: sub-agent, Task agent, parallel worker, or equivalent.
- The orchestrator never performs child phase work inline. Proposal, execution, review, and state publication each run in their own fresh worker.
- Workers return structured results through durable artifacts in `.harness/<feature-id>/` and `docs/live/*`; those files remain the source of truth.
- Only the orchestrator may delegate. Workers must not spawn nested workers.
- Every worker dispatch should be traceable in state with a worker id, subject, tool-scope profile, and spawn depth when those fields matter.

## Tool-scope lanes

Tool access is a hard boundary, not a suggestion.

- The orchestrator gets state inspection and delegation tools only.
- `project-initializer`, `generator-proposal`, `generator-execution`, and `state-update` get only the write surface needed for the files they own.
- `evaluator-contract-review` and `adversarial-live-review` are evaluators. They must not receive general write access to product code or global state; if they need to return an artifact, the path must be narrowed to that artifact only.
- Workers do not widen their own scope, reach across phase boundaries, or keep hidden state outside the file handoff.

## Parallel work rules

Parallel workers are allowed only when the work is independent and non-overlapping.

- File ownership must not overlap unless the orchestrator can merge outputs without ambiguity.
- Parallel review or evaluation is safe only when each worker writes to its own artifact or returns structured findings for the orchestrator to reconcile.
- Do not use parallel workers to simulate nested delegation inside a worker. Parallelism still starts at the orchestrator.

## State locations and precedence

1. Human edits and explicit user instructions.
2. Active sprint-local state in `.harness/<active-feature>/`, especially `contract.md`, `handoff.md`, `review.md`, and `status.json`.
3. Global live state in `docs/live/features.json`, `docs/live/progress.md`, and `docs/live/memory.md`.
4. Stable reference intent in `docs/reference/*`.
5. Derived outputs from `docs/scripts/*` or ad hoc tooling.

Use local state to decide how to continue the active sprint. Use global state to decide what the project should work on next. If they disagree, resolve the conflict explicitly; do not silently invent a merge.

## Single-active-sprint rule

Exactly one feature may be active in `.harness/` at a time. New work stays pending in `docs/live/features.json` until the active sprint is reviewed and either:

- passed, published to `docs/live/*`, then archived under `docs/archive/`, or
- failed/cancelled, preserved in place for resume with an updated next action.

## Resume and archive procedure

- Resume by reading `docs/live/features.json`, then `.harness/<feature-id>/status.json`, then the file named by `resume_from`.
- Treat `status.json` as dispatch metadata for the next fresh worker, not as permission for the orchestrator to do that worker's phase inline.
- Keep implementation notes, handoff context, worker trace metadata, and review findings inside the active sprint folder while work is live.
- After a sprint is complete and state is updated, copy or move the final local artifacts to `docs/archive/<feature-id>_timestamp/`.
- Never mix archived artifacts back into `.harness/`; active and historical state must stay separate.
