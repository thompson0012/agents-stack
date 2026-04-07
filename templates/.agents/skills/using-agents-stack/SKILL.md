---
name: using-agents-stack
description: Use when a repository follows the agents-stack harness and the orchestrator must route work to one workflow phase child via a fresh worker.
---

# Using Agents Stack

Use this router when the hard problem is choosing the next harness phase in a repository that uses the agents-stack starter layout. If the repository does not use this harness family, or the request is ordinary implementation outside the harness workflow, no family child fits.

Do not perform the child workflow here. Prefer dispatching a fresh worker, sub-agent, Task agent, or useful parallel workers first when the route depends on ambiguous or evidence-heavy investigation, then merge the returned outputs here and decide the next dispatch. If delegation would not materially help, or durable state already makes the answer clear, keep the step direct. Do not load the child phase into the orchestrator's own context and continue inline.

## Core Contract

- Route to exactly one child or say no family child fits.
- Use `references/children.json` as the source of truth for child selection, prerequisites, install hints, and fallbacks.
- Use `references/state-machine.md`, `references/file-system-layout.md`, and `references/orchestrator-worker.md` for family-specific state, path, and delegation rules.
- Prefer the strongest durable evidence on disk over chat memory or optimistic status text.
- Treat `build_failed`, `review_failed`, `awaiting_human`, and `escalated_to_human` as distinct routing states. Do not collapse them into generic "blocked" or route them all back into execution.
- Retries after `build_failed` or reconciled `review_failed` require a recorded clean restore boundary such as a disposable worktree, VCS snapshot, or equivalent `clean_restore_ref`. Automatic destructive reset is valid only in disposable workspaces and is not the default expectation.
- Respect attempt budgets. When `attempt_count` reaches `max_attempts`, or no safe clean restore boundary exists, automatic retry stops and the sprint must park for human action or escalation.
- Parked sprints in `.harness/` with `awaiting_human` or `escalated_to_human` remain visible durable state, but they do not count as the single runnable active sprint.
- `docs/live/tracked-work.json` remains the authoritative tracked-work ledger and runnable/backlog selector.
- `docs/live/current-focus.md` is the live resume anchor; `docs/live/roadmap.md` is the durable initiative ledger for source goals, remaining slices, and re-authorization boundaries.
- When a user introduces or changes a broad goal, normalize it into `docs/live/current-focus.md` plus `docs/live/roadmap.md` before continuing sprint chaining. Do not let cross-sprint intent live only in chat memory.
- Brainstorm and Compound are explicit non-runnable phases. They may be the next router action, but they must not claim `runnable_active_sprint_id`.
- When no runnable active sprint exists, drain `compound_pending_feature_ids` first, then choose the highest-priority dependency-ready `needs_brainstorm` backlog item, then the highest-priority dependency-ready `pending` item.
- Protect the orchestrator context: it selects, merges worker evidence, dispatches, and waits for structured outputs; it does not implement, review, or rewrite state inline.
- If the best child is missing, say to install it rather than quietly doing weaker work under the wrong child.

## Decision Order

1. Check whether the repository belongs to this family at all: `AGENTS.md`, `docs/live/*`, `.harness/<WORKSTREAM-ID>/`, and the agents-stack role/lifecycle model.
2. Read `docs/live/tracked-work.json` to determine whether the repo is uninitialized, has queued compound work, has one runnable active sprint, has only parked sprints, or needs new backlog work.
3. Read `docs/live/current-focus.md` and `docs/live/roadmap.md` together to confirm the resume anchor, source-goal lineage, remaining slices, and any re-authorization boundary.
4. If the user's high-level goal is broader than the live files currently capture, route first to the phase that will publish or refresh that durable source-goal truth before continuing sprint chaining.
5. If `compound_pending_feature_ids` is non-empty, route `compound-capture` before resuming or opening any sprint work.
6. If a runnable active sprint exists, route from the strongest local durable artifact for that sprint.
7. If `review.md` exists but live and local state have not yet reconciled the verdict, route to `state-update` before any new execution or proposal work.
8. If the sprint is in `build_failed` or reconciled `review_failed`, route to `generator-execution` only when attempts remain and `clean_restore_ref` defines a safe restore boundary.
9. If the sprint is in `awaiting_human` or `escalated_to_human` and that parked state is already reflected durably, do not auto-dispatch execution. Surface the parked state unless new human edits have changed the checkpoint.
10. If no runnable active sprint exists, choose the highest-priority dependency-ready `needs_brainstorm` backlog item for `generator-brainstorm`.
11. If no dependency-ready `needs_brainstorm` item exists, choose the highest-priority dependency-ready `pending` backlog item for `generator-proposal`.
12. Pick the narrowest child that matches the strongest durable evidence.
13. If the selected child is missing, install it when possible or disclose the fallback.
14. Dispatch a fresh worker for the selected child with a stable worker ID, phase-appropriate tools, and explicit artifact return targets after any useful evidence-gathering workers have returned and been merged.

## Family Workflow Boundary

This router owns only the agents-stack workflow family:

- project initialization of durable state
- pre-sprint brainstorm capture
- sprint proposal
- adversarial contract review
- contract-bound execution
- independent live review
- state synchronization and archive closeout
- post-publication compound capture

This router does not replace ordinary feature implementation, generic project planning, or non-harness repository work. If the repository is not using the agents-stack state model, no family child fits.

## Router Output

Return one of these forms, then dispatch the selected child as a fresh worker if needed:

- `Route to using-agents-stack/project-initializer.`
- `Route to using-agents-stack/generator-brainstorm.`
- `Route to using-agents-stack/generator-proposal.`
- `Route to using-agents-stack/evaluator-contract-review.`
- `Route to using-agents-stack/generator-execution.`
- `Route to using-agents-stack/adversarial-live-review.`
- `Route to using-agents-stack/state-update.`
- `Route to using-agents-stack/compound-capture.`
- `Install using-agents-stack/<child>, then route to using-agents-stack/<child>.`
- `No family child fits; answer directly.`

Add one sentence explaining why the selected child is the narrowest correct fit. If a child is selected, continue by spawning a fresh worker with that child prompt rather than swapping personas inside the orchestrator.

When the durable truth is a fully reconciled `awaiting_human` or `escalated_to_human` sprint with no new human edits, the correct result is usually `No family child fits; answer directly.` plus an explanation that automation must wait on the file-based human handoff boundary.

## References

- `references/children.json`
- `references/state-machine.md`
- `references/file-system-layout.md`
- `references/orchestrator-worker.md`

## Final Checklist

- [ ] Router stays focused on selection and fresh-worker dispatch
- [ ] Child inventory is current in `references/children.json`
- [ ] Missing/install/fallback behavior is explicit
- [ ] Compound queue drains before runnable sprint resume or backlog selection
- [ ] Brainstorm stays pre-sprint and non-runnable
- [ ] Retry routing respects clean restore boundaries and attempt budgets
- [ ] Parked `awaiting_human` and `escalated_to_human` sprints do not auto-dispatch into execution
- [ ] No child work is performed inline in the orchestrator
- [ ] Validation completed
