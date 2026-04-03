# Project Progress Ledger

Append reviewed outcomes here after `state-update` reconciles them: archived PASS results and any active FAIL, BUILD_FAILED, or parked-human states that materially change the next action. Routine execution chatter still belongs in `.harness/<feature-id>/` and the current backlog entry in `features.json`.

This ledger records the decisive outcome first. Any durable cross-sprint lesson is captured later by the explicit Compound phase in `docs/live/memory.md`; `progress.md` is not a substitute for memory.

## Entry format

Each reviewed or reconciled entry should record:

- the date and feature id,
- final or parked status,
- what materially shipped, failed, or blocked progress,
- where the archived or active sprint artifacts live,
- retry budget and clean restore requirements when another execution pass is possible,
- whether the outcome queued explicit compounding work,
- the next recommended action for the project.

## [2026-04-02] FEAT-000: Bootstrap Harness Starter

- **Status**: Archived after successful closeout
- **Outcome**: Established the initial harness skeleton, durable state files, and the first resumable sprint folder.
- **Artifacts**: `docs/archive/FEAT-000_timestamp/`
- **Evidence**: Final contract, handoff, review, and status snapshot were preserved with the archive.
- **Compound**: Any durable lesson from the archived evidence belongs to the explicit Compound phase, not to state reconciliation.
- **Next Action**: Start proposal work for `FEAT-001`, then continue that sprint until it reaches a reviewed outcome.

## [2026-04-02] FEAT-001: Dark Mode Toggle Polish

- **Status**: Review failed; sprint remains the single runnable active sprint
- **Outcome**: The toggle behavior is functional, but the adversarial review failed on dark-mode contrast and on the generic checkbox-style control.
- **Artifacts**: `.harness/FEAT-001/`
- **Evidence**: `review.md`, `qa.md`, `runtime.md`, `handoff.md`, and `status.json` keep the failed review evidence intact.
- **Retry Budget**: Attempt `1` of `3` is consumed.
- **Clean Restore**: The next execution pass must start from `disposable-worktree:feat-001-attempt-02-baseline`, or an equivalent durable restore boundary. Do not default to destructive reset unless the workspace is explicitly disposable.
- **Compound**: This reconciled review-failed outcome should be queued in `docs/live/features.json` for the explicit Compound phase; compounding captures durable lessons without changing FEAT-001's runnable status.
- **Next Action**: Run `compound-capture` on the reconciled FEAT-001 evidence, then restore FEAT-001 from the clean boundary, resume `generator-execution` from `.harness/FEAT-001/review.md`, rerun build/startup triage after the fix, and only then return to `adversarial-live-review`.

## Current focus convention

Do not add an entry for every execution checkpoint. While `FEAT-001` is active, its detailed source of truth is:

- `docs/live/features.json` for project-level priority, parked-vs-runnable state, retry budget, compound queue state, and next action,
- `.harness/FEAT-001/status.json` for phase, resume pointer, attempt counts, and clean-restore metadata,
- `.harness/FEAT-001/review.md` for corrective directives after adversarial review.

When `state-update` reconciles a decisive outcome, it updates this ledger first. If that same update queues explicit compounding, `compound-capture` runs after reconciliation and before any new brainstorm or proposal selection. A runnable retry already named in live state remains the next execution owner once compounding is clear.

If a sprint moves to `awaiting_human` or `escalated_to_human`, record that parked state here and in `features.json`, then run any queued compounding before choosing new work from dependency-ready backlog items.