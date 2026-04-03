---
name: compound-capture
description: Capture durable cross-sprint learnings after state reconciliation has queued explicit compounding work.
trigger: After `state-update` has reconciled a decisive sprint outcome and queued the feature id in `docs/live/features.json` under `compound_pending_feature_ids`.
inputs:
  - AGENTS.md
  - docs/live/features.json
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/architecture.md
  - docs/reference/design.md
  - .harness/<feature-id>/* when the sprint still lives locally
  - docs/archive/<feature-id>_<timestamp>/* when the sprint has already been archived
outputs:
  - updated docs/live/memory.md when durable learning survives
  - unchanged docs/live/memory.md when extraction is deliberately skipped because no durable lesson survived
  - optional precise update to docs/reference/architecture.md or docs/reference/design.md when the lesson is now stable reference truth
  - updated docs/live/features.json with the processed feature id removed from `compound_pending_feature_ids`
boundaries:
  - Do not reopen proposal, execution, review, or state reconciliation.
  - Do not make backlog publication, archive, or runnable-sprint decisions; those belong to `state-update`.
  - Do not invent durable lessons from a single noisy artifact.
  - Do not claim or change `runnable_active_sprint_id`.
next_skills:
  - generator-execution
  - generator-brainstorm
  - generator-proposal
---

# Compound Capture

## Mission
Capture only the durable learning that should survive beyond the just-reconciled sprint outcome.

This phase exists because state reconciliation and learning capture are different jobs:
- `state-update` makes the repository tell the truth about outcome, archive state, retry state, and backlog visibility.
- `compound-capture` decides whether any of that evidence becomes cross-sprint memory or stable reference guidance.

Compounding is explicit, non-runnable phase work. It does not reopen execution or review, and it does not take or advertise the runnable active sprint slot.

## Worker Dispatch Contract

- Run compounding in a fresh worker context after `state-update`; do not fold it into reconciliation.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read the decisive evidence, write `docs/live/memory.md` only when durable residue survives, optionally patch stable reference docs, and clear the processed queue entry in `docs/live/features.json`. No product-code edits, no `.harness/<feature-id>/status.json` rewrites, no archive moves.
- Not parallel-safe against another worker touching `docs/live/memory.md`, the same reference doc, or `docs/live/features.json`. Process one queued feature id at a time.
- Durable return contract: truthful `docs/live/memory.md` when extraction happens, or a deliberate no-edit skip when no durable learning survives, plus `docs/live/features.json` with the processed feature removed from `compound_pending_feature_ids`.

## Required Reads
Read these before writing anything:

1. `AGENTS.md`
2. `docs/live/features.json`
3. `docs/live/progress.md`
4. `docs/live/memory.md`
5. Relevant `docs/reference/architecture.md` or `docs/reference/design.md` if the lesson may be reference-worthy
6. The decisive sprint evidence for the queued feature id:
   - prefer `.harness/<feature-id>/review.md`, `runtime.md`, `handoff.md`, and `status.json` when the sprint is still active or parked
   - prefer `docs/archive/<feature-id>_<timestamp>/review.md`, `runtime.md`, `handoff.md`, and `status.json` when the sprint has already been archived

Do not compound from backlog text alone. The learning must be grounded in durable evidence.

## What qualifies as a durable learning
Good candidates:
- environment or runtime quirks that future workers are likely to hit again
- recurring failure patterns that should tighten future proposals, contracts, or reviews
- architecture constraints or integration boundaries confirmed by the sprint evidence
- design-system or UX verification lessons that should change how future work is scoped or checked

Bad candidates:
- one-off logs or stack traces
- temporary blockers that live only in a single sprint handoff
- opinions that were not tested or reviewed
- paraphrases of the sprint outcome already recorded in `progress.md`
- speculative “best practices” not confirmed by repository evidence

A truthful outcome may be: no durable new learning survived. In that case, clear the queue and leave `docs/live/memory.md` unchanged.

## Workflow

### 1. Confirm the queue entry is real
- Verify the target feature id is already present in `docs/live/features.json` under `compound_pending_feature_ids`.
- Verify `state-update` has already reconciled the decisive outcome into live state and, when applicable, archived or preserved the sprint correctly.
- If the queue entry is missing, do not invent compounding work. Stop and preserve the current files.

### 2. Gather the strongest evidence bundle
Identify whether the decisive evidence lives in `.harness/<feature-id>/` or `docs/archive/<feature-id>_<timestamp>/`.

Use the strongest available artifacts in this order:
1. `review.md`
2. `runtime.md`
3. `handoff.md`
4. `status.json`
5. `contract.md`
6. `sprint_proposal.md`
7. the already-published outcome in `docs/live/progress.md`

Never write a durable lesson that contradicts the strongest artifact.

### 3. Distill candidate learnings
For each candidate lesson, ask:
- Will this matter outside the just-finished sprint?
- Is it supported by evidence, not just chat or intuition?
- Would a future worker make a worse decision without this note?
- Does it belong in `memory.md`, or is it stable enough for a reference doc?

If the answer is no, do not record it.

### 4. Extract durable residue or skip extraction
When a learning survives, append or refine a concise note in `docs/live/memory.md`. When no durable cross-sprint lesson survives, explicitly skip extraction: leave `docs/live/memory.md` unchanged and do not add placeholder text.

Write in project-truth terms when you do extract:
- what was learned
- why it matters for future work
- enough context to apply it without rereading the old sprint
- only the residue that survives beyond this sprint, not the whole sprint story

`progress.md` already owns the outcome ledger. `memory.md` should either gain durable residue or remain unchanged on purpose. Do not blur those roles.

### 5. Update reference docs only when the lesson is now stable

Examples:
- a verified integration boundary that future proposals must respect
- a design-system rule or interaction constraint that is now part of the product baseline

Do not patch reference docs for tentative lessons, retries, or one-off failures.

### 6. Clear the compound queue truthfully
After extracting durable learning, or after deliberately skipping extraction because none survives:
- remove the feature id from `compound_pending_feature_ids`
- leave `runnable_active_sprint_id` unchanged
- do not change the sprint phase, retry budget, archive state, or parked-state metadata

Clearing the queue is the durable record that the extract-or-skip decision for that feature is finished. It does not mean the sprint outcome changed.

## Stop Conditions
Stop and preserve the queue entry when:
- the feature id was not actually queued for compounding
- decisive evidence cannot be located in `.harness/<feature-id>/` or `docs/archive/<feature-id>_<timestamp>/`
- the evidence set contradicts the live outcome badly enough that reconciliation appears incomplete
- the only candidate notes are speculative or transient

If the evidence is thin but sufficient to conclude “no durable learning,” that is not a blocker. Clear the queue without fabricating a note.

## Quality Bar
A good compounding pass:
- leaves `progress.md` as the outcome ledger and `memory.md` as the cross-sprint residue
- keeps reference docs reserved for stable truths
- clears the queue entry so the orchestrator does not compound the same feature twice
- never steals ownership of execution, review, or backlog publication
- tells the truth even when the answer is to skip extraction because nothing durable survived

## Done Definition
This skill is done when the queued feature has been evaluated for durable learning, any real cross-sprint lesson has been captured in `docs/live/memory.md` and optional reference docs, or extraction has been deliberately skipped because no durable residue survived, and the feature id has been removed from `compound_pending_feature_ids` without altering runnable-sprint ownership or reopening prior phases.
