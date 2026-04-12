---
name: compound-capture
description: Capture durable cross-sprint learnings after state reconciliation has queued explicit compounding work.
trigger: After `state-update` has reconciled a decisive sprint outcome and queued the feature id in `docs/live/tracked-work.json` under `compound_pending_feature_ids`.
inputs:
  - AGENTS.md
  - docs/live/tracked-work.json
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/architecture.md
  - docs/reference/design.md
  - linked docs/records/* for the queued feature when present
  - .harness/<workstream-id>/* when the sprint still lives locally
  - docs/archive/<workstream-id>_<timestamp>/* when the sprint has already been archived
outputs:
  - updated docs/live/memory.md when durable learning survives
  - unchanged docs/live/memory.md when extraction is deliberately skipped because no durable lesson survived or a tempting lesson lacked artifact-linked provenance
  - optional precise update to linked `docs/records/*` when record residue is promoted, superseded, or expired
  - optional precise update to docs/reference/architecture.md or docs/reference/design.md when the lesson is now stable reference truth
  - updated docs/live/tracked-work.json with the processed feature id removed from `compound_pending_feature_ids` and any touched `record_paths` / `reference_paths` kept truthful
boundaries:
  - Do not reopen proposal, execution, review, or state reconciliation.
  - Do not make backlog publication, archive, or runnable-sprint decisions; those belong to `state-update`.
  - Do not invent durable lessons from a single noisy artifact.
  - Do not persist raw chat transcripts, paraphrased conversation logs, or chat-only conclusions; only decisive repo evidence may become durable output.
  - Do not claim or change `runnable_active_sprint_id`.
  - Do not let `docs/records/*` become a second contract, second archive, or hidden registry outside `docs/live/tracked-work.json`.
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
- Tool lane: read the decisive evidence, write `docs/live/memory.md` only when durable residue survives and can cite decisive artifact path(s), optionally patch linked `docs/records/*` and stable reference docs only when those durable writes keep the same artifact-linked provenance, and clear the processed queue entry in `docs/live/tracked-work.json`. No product-code edits, no `.harness/<workstream-id>/status.json` rewrites, no archive moves.
- Not parallel-safe against another worker touching `docs/live/memory.md`, linked record pages, the same reference doc, or `docs/live/tracked-work.json`. Process one queued feature id at a time.
- Durable return contract: truthful `docs/live/memory.md` when extraction happens with artifact-linked provenance, or a deliberate no-edit/no-publish skip when no durable learning survives or a tempting lesson lacks provenance, plus any linked `docs/records/*` / `docs/reference/*` updates and `docs/live/tracked-work.json` with the processed feature removed from `compound_pending_feature_ids`.
- Dispatch framing is non-authoritative. Before extracting learning, verify that the dispatched feature still matches `docs/live/tracked-work.json`, that the claimed compound-ready phase still matches the strongest local/archive evidence on disk, and that stronger evidence in the `AGENTS.md` precedence chain beats any dispatch summary, stale resume hint, or copied orchestrator context.
- If those checks disagree with the dispatch frame, stop before writing durable learning or queue state, preserve the existing truthful files, and hand control back to the orchestrator for correct-lane dispatch.

## Required Reads
Read these before writing anything:

1. `AGENTS.md`
2. `docs/live/tracked-work.json`
3. `docs/live/progress.md`
4. `docs/live/memory.md`
5. Relevant `docs/reference/architecture.md` or `docs/reference/design.md` if the lesson may be reference-worthy
6. Any linked `docs/records/*` already registered on the queued feature
7. The decisive sprint evidence for the queued feature id:
   - prefer `.harness/<workstream-id>/review.md`, `runtime.md`, `handoff.md`, and `status.json` when the sprint is still active or parked
   - prefer `docs/archive/<workstream-id>_<timestamp>/review.md`, `runtime.md`, `handoff.md`, and `status.json` when the sprint has already been archived

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

A candidate qualifies for extraction only when all are true:
- it is reusable beyond this sprint rather than a one-off handoff note or chat-only conclusion
- it can point to decisive artifact path(s) in the evidence bundle
- it would change how a future worker scopes, routes, reviews, or validates similar work

If any test fails, skip extraction instead of publishing a plausible-sounding note.

## Workflow

### 1. Confirm the queue entry is real
- Verify the target feature id is already present in `docs/live/tracked-work.json` under `compound_pending_feature_ids`.
- Verify `state-update` has already reconciled the decisive outcome into live state and, when applicable, archived or preserved the sprint correctly.
- If the queue entry is missing, do not invent compounding work. Stop and preserve the current files.

### 2. Gather the strongest evidence bundle
Identify whether the decisive evidence lives in `.harness/<workstream-id>/` or `docs/archive/<workstream-id>_<timestamp>/`.

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
- Does it belong in `memory.md`, a linked record page, or is it stable enough for a reference doc?

If the answer is no, do not record it.

### 4. Extract durable residue or skip extraction
When a learning survives, publish it only if the durable output can cite at least one specific decisive artifact path from the evidence bundle. That provenance gate applies to `docs/live/memory.md`, linked `docs/records/*`, and `docs/reference/*`. For `memory.md`, a direct inline artifact-path citation is sufficient; do not require a separate record page just to carry provenance.

If a lesson seems useful but cannot be tied to a specific artifact path, treat that as a deliberate no-publish result: leave durable outputs unchanged and clear the queue. When no durable cross-sprint lesson survives at all, explicitly skip extraction and leave `docs/live/memory.md` unchanged. Do not defer capture to chat memory or a later manual copy step.

Write in project-truth terms when you do extract:
- what was learned
- why it matters for future work
- enough context to apply it without rereading the old sprint
- only the residue that survives beyond this sprint, not the whole sprint story

`progress.md` already owns the outcome ledger. `memory.md` should either gain durable residue or remain unchanged on purpose. Do not blur those roles.

### 5. Reconcile linked records before promoting reference truth
If the queued feature already has `record_paths`, inspect those pages against the decisive evidence bundle. If no linked record exists yet and the durable residue should survive, create one new scoped page for the same tracked feature in the same pass only when that page can preserve artifact-linked provenance back to the decisive sprint artifacts.

Use records deliberately:
- promote stable residue from a record into `docs/reference/*` only when the lesson is now current project truth and the promoted text still carries artifact-linked provenance
- keep feature-specific or still-contingent material in `docs/records/*` with page-local provenance such as scope, status, superseded_by, and the sprint or archive contributions it relies on
- when later evidence invalidates or replaces a record, update that record's status to something like superseded or expired instead of silently deleting traceability
- keep `docs/live/tracked-work.json` authoritative by preserving or updating the feature's `record_paths` and `reference_paths` in the same pass

Do not patch reference docs for tentative lessons, retries, or one-off failures.

### 6. Clear the compound queue truthfully
After extracting durable learning, or after deliberately skipping extraction because none survives or because a tempting lesson lacked artifact-linked provenance:
- remove the feature id from `compound_pending_feature_ids`
- leave `runnable_active_sprint_id` unchanged
- keep the feature's `record_paths`, `reference_paths`, and canonical `evidence_path` truthful in `docs/live/tracked-work.json`
- do not change the sprint phase, retry budget, archive state, or parked-state metadata

Clearing the queue is the durable record that the extract-or-skip decision for that feature is finished. It does not mean the sprint outcome changed.

## Stop Conditions
Stop and preserve the queue entry when:
- the feature id was not actually queued for compounding
- decisive evidence cannot be located in `.harness/<workstream-id>/` or `docs/archive/<workstream-id>_<timestamp>/`
- the evidence set contradicts the live outcome badly enough that reconciliation appears incomplete

If the evidence is thin but sufficient to conclude “no durable learning,” that is not a blocker. Clear the queue without fabricating a note.
If a tempting lesson lacks artifact-linked provenance, that is also not a blocker. Do not publish to `docs/live/memory.md`, `docs/records/*`, or `docs/reference/*`; clear the queue as an explicit no-publish result.

## Quality Bar
A good compounding pass:
- leaves `progress.md` as the outcome ledger and `memory.md` as the cross-sprint residue
- publishes durable learning only with artifact-linked provenance
- promotes only stable truths into reference docs
- updates linked records when they should stay as feature-scoped residue, or marks them superseded/expired when later evidence invalidates them
- keeps `docs/live/tracked-work.json` authoritative for record and reference linkage
- clears the queue entry so the orchestrator does not compound the same feature twice
- never steals ownership of execution, review, or backlog publication
- tells the truth even when the answer is to skip extraction because nothing durable survived or because provenance was insufficient

## Done Definition
This skill is done when the queued feature has been evaluated for durable learning, every durable write to `docs/live/memory.md`, linked `docs/records/*`, or `docs/reference/*` carries artifact-linked provenance to decisive evidence, any real cross-sprint lesson has been captured truthfully, any linked record has either stayed as scoped residue, been promoted into `docs/reference/*`, or been marked superseded/expired truthfully, and the feature id has been removed from `compound_pending_feature_ids` without altering runnable-sprint ownership or reopening prior phases.
