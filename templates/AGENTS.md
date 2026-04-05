# AGENTS.md

This repository uses agents-stack. The scaffold starts blank: no active sprint, no archive history, and no seeded backlog. Files are the source of truth.

## First-session read order
Read only these files first:
1. `README.md`
2. `AGENTS.md`
3. `docs/scripts/init.sh`

Stop there unless the task explicitly needs live state or deeper harness/reference docs.

## Read later if needed
- `docs/reference/harness.md` — routing, state precedence, retry safety, and publication rules.
- `docs/reference/architecture.md` — project runtime and subsystem boundaries.
- `docs/reference/design.md` — project product intent and UX constraints.
- `docs/live/*` — current durable project state.

## Operating summary
- The `using-agents-stack` root skill is the only orchestrator in this repository.
- Files beat chat memory.
- Exactly one sprint may be runnable at a time.
- Parked `awaiting_human` and `escalated_to_human` sprints remain visible, but they are not runnable.
- `docs/live/features.json` is the runnable selector and tracked-work ledger.
- `docs/scripts/init.sh` is the canonical blank-default generator.
- Do not scan the whole tree on a fresh start unless the task is explicitly a repo audit or scaffold repair.

## Constitutional guardrails
- Execution does not self-approve.
- Reviewers and evaluators stay independent and do not get broad product-code write access.
- Tool walls are hard boundaries. Do not mix brainstorming, proposal, execution, review, state-update, and compound work in one lane.
- Reviews and interactive acceptance must verify before-state, action, and after-state transitions, not only a final static snapshot.
- PASS archives only after `state-update` reconciles live state. FAIL and BLOCKED preserve sprint evidence in `.harness/<feature-id>/`.
- Retries after `build_failed` or `review_failed` require remaining attempt budget plus a durable `clean_restore_ref`.
- If local and global state disagree, or `review.md` exists but status is stale, open `docs/reference/harness.md` and reconcile before more execution.

## Copyable scaffold
`docs/live/*` and `docs/reference/architecture.md` / `docs/reference/design.md` are copied as empty, project-neutral placeholders. `docs/reference/harness.md` is the full harness constitution for routing, retry, resume, state disagreement, and archive rules. It is read after bootstrap, not skipped forever.