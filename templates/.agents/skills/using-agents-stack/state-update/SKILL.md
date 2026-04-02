---
name: state-update
purpose: Synchronize reviewed sprint outcomes back into durable project state, preserving evidence and routing the next correct action.
trigger: After `adversarial-live-review` has written `.harness/<sprint-id>/review.md` and updated the sprint status.
inputs:
  - AGENTS.md
  - docs/live/features.json
  - docs/live/progress.md
  - docs/live/memory.md
  - .harness/<sprint-id>/contract.md
  - .harness/<sprint-id>/runtime.md
  - .harness/<sprint-id>/handoff.md
  - .harness/<sprint-id>/qa.md
  - .harness/<sprint-id>/review.md
  - .harness/<sprint-id>/status.json
outputs:
  - updated docs/live/features.json
  - updated docs/live/progress.md
  - updated docs/live/memory.md
  - updated .harness/<sprint-id>/status.json or preserved sprint folder
  - docs/archive/<sprint-id>_<timestamp>/... on PASS
boundaries:
  - Do not mark completion without review evidence.
  - Do not erase failed sprint artifacts.
  - Do not rewrite review findings to make them pass.
  - Do not start the next sprint's implementation yourself.
next_skills:
  - generator-execution
  - generator-proposal
---

# State Update

You are the state manager. Your job is to make the repository tell the truth after review.

That means:
- global state reflects the latest reviewed outcome
- local sprint state remains resumable
- archived artifacts remain auditable
- routing to the next phase is explicit

## Worker Dispatch Contract

- Run state reconciliation in a fresh worker context. The orchestrator dispatches this worker after review; it does not perform state-update inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: durable state and archive operations only: `docs/live/*`, `.harness/<sprint-id>/*`, and `docs/archive/*` as required by the review outcome. No product-code edits, no proposal rewriting, no new implementation work.
- Not parallel-safe. This worker owns the single active sprint's global reconciliation and archive decision; do not split or race writes across multiple workers.
- Durable return contract: updated `docs/live/features.json`, `docs/live/progress.md`, `docs/live/memory.md`, `.harness/<sprint-id>/status.json`, and PASS-path archive contents. Include `worker_id` / `orchestrator_run_id` in the updated status or ledger entry when the host provides them.

## Mandatory verification before any update

Before touching global state, confirm all of the following:
1. `.harness/<sprint-id>/review.md` exists.
2. `.harness/<sprint-id>/qa.md` exists or `review.md` explicitly embeds equivalent evidence.
3. The review decision is unambiguous: `PASS`, `FAIL`, or `BLOCKED`.
4. `status.json` points to the review checkpoint.
5. The reviewed sprint matches the active feature recorded in `docs/live/features.json`.

If any of these fail, stop. Do not mark the sprint complete, do not archive it, and do not advance the backlog. Missing review evidence is a blocking data-integrity problem.

## Sources of truth by decision type

- `review.md` decides PASS vs FAIL vs BLOCKED.
- `qa.md` proves what was actually checked.
- `contract.md` defines the scope that was supposed to be delivered.
- `runtime.md` and `handoff.md` explain how the result was produced and how it can be resumed.
- `docs/live/*` is the durable global ledger that must now be synchronized.

## Update procedure

### 1. Validate the reviewed outcome

Read `review.md` and extract:
- final status
- satisfied or failed contract criteria
- corrective directives
- any explicit scope violations
- any unexecuted checks or unverifiable claims

If review evidence and review status disagree, preserve the sprint as active and record the discrepancy in `progress.md` rather than pretending the outcome is settled.

### 2. Update `docs/live/features.json`

This file is the project-wide backlog state.

#### On PASS
- mark the sprint feature as completed using the repository's chosen terminal status
- remove or clear any `in_progress` marker so there is no active sprint left behind
- preserve identifiers, priority, dependencies, and any useful completion metadata already used by the template

#### On FAIL
- keep the same feature active or explicitly mark it as failed-but-open according to the file's schema
- do not move to the next feature
- add any machine-readable review pointers or retry counts if the schema already supports them

Do not invent a new schema casually. Extend only when necessary and keep it consistent.

### 3. Update `docs/live/progress.md`

Append a dated ledger entry that includes:
- sprint id and title
- PASS, FAIL, or BLOCKED status
- concise summary of what changed, what failed, or what blocked progress
- path to the evidence (`.harness/...` while active, `docs/archive/...` after archive)
- next recommended action

For FAIL, the next action should point back to the active sprint and the corrective directives.
For PASS, the next action should point to backlog selection or the next pending feature.
For BLOCKED, the next action should point to the blocker owner, prerequisite, or human decision needed before another worker is dispatched.

### 4. Update `docs/live/memory.md`

Write only durable knowledge worth carrying forward, such as:
- runtime quirks the next sprint must remember
- architecture or environment lessons confirmed during review
- recurring failure patterns that should influence future contracts

Do not dump transient logs into memory. Memory is for durable project-level truths.

### 5. Preserve or archive sprint artifacts truthfully

## FAIL path: preserve, do not archive as completed

On FAIL:
- keep `.harness/<sprint-id>/` intact
- keep `contract.md`, `runtime.md`, `handoff.md`, `qa.md`, `review.md`, and `status.json`
- update `status.json` to reflect that the sprint remains active, for example:
  - `phase: "review_failed"`
  - `owner_role: "orchestrator"`
  - `resume_from: "review.md"`
- synchronize `docs/live/features.json` and `docs/live/progress.md` so the active sprint stays open, the failure is visible, and the next action points to `generator-execution`
- leave `review.md` untouched; the retry is driven by durable state, not by deleting evidence
- ensure the next generator can resume from the evidence without reconstructing context from chat

A failed sprint is not dead history. It is active work with evidence attached.

## BLOCKED path: preserve and publish the blocker

On BLOCKED:
- keep `.harness/<sprint-id>/` intact
- keep `contract.md`, `runtime.md`, `handoff.md`, `qa.md` when it exists, `review.md`, and `status.json`
- update `status.json` to reflect that the sprint remains active but cannot safely proceed yet, for example:
  - `phase: "blocked"`
  - `owner_role: "orchestrator"`
  - `resume_from: "review.md"`
- synchronize `docs/live/features.json` and `docs/live/progress.md` so the active sprint stays open and the blocker is visible
- leave `review.md` untouched; the blocker and recovery steps are durable evidence, not scratch notes

A blocked sprint is active work waiting on a prerequisite, not a hidden failure and not a completed sprint.

## PASS path: archive after global state is updated

On PASS:
1. Verify the review evidence is complete.
2. Update `docs/live/*` first.
3. Archive the full sprint artifact set to `docs/archive/<sprint-id>_<timestamp>/`.
4. Ensure the archive contains, at minimum:
   - `sprint_proposal.md` if it exists
   - `contract.md`
   - `handoff.md`
   - `review.md`
   - `status.json`
   - `runtime.md` when execution produced runtime notes
   - `qa.md` when the review produced a separate QA evidence log
5. Update `status.json` to a terminal archived state, for example:
   - `phase: "archived_pass"`
   - `owner_role: "none"`
   - `resume_from: "docs/archive/<sprint-id>_<timestamp>/review.md"`
6. Remove or clear the active sprint workspace only after the archive copy is confirmed and the harness's single-active-sprint rule is preserved.

Never archive a sprint as complete if review failed or evidence is missing.

## Routing rules

### After PASS
Route toward the next backlog decision:
- if another pending feature exists, next skill is usually `generator-proposal`
- if the harness requires re-initialization or backlog refresh, route accordingly from global state

The completed sprint should no longer be the active work packet.

### After FAIL
Route back to `generator-execution` on the same sprint once `status.json` and `docs/live/*` reflect `review_failed`.

The next generator should be able to open:
- `contract.md` for scope
- `runtime.md` for environment
- `qa.md` for raw evidence
- `review.md` for corrective directives

Do not wipe or rewrite these files to create a cleaner retry.

### After BLOCKED
Keep the sprint active, preserve the blocker evidence, and stop automatic phase advancement until the blocker is resolved.

The orchestrator should surface the blocker and wait for the named prerequisite or human decision. Do not silently dispatch a new execution or review worker while the blocker still stands.

## Edge-case rules

### Review evidence is missing
If `review.md` exists but no evidence supports it:
- do not mark PASS, FAIL, or BLOCKED into global state as final
- leave the sprint active
- record the inconsistency in `progress.md`
- route back for a proper review, not for fresh implementation

### Tests could not be executed
If the reviewer recorded that required tests could not run:
- treat the sprint as FAIL unless the contract explicitly allowed an alternate proof path
- preserve the failure evidence
- keep the sprint open

### Implementation exceeded contract scope
If review flags scope overreach:
- do not complete the sprint even if the feature appears functional
- record the overreach in `progress.md` and `memory.md` only if it affects future work
- route back to `generator-execution` with the review directives intact

## Minimum truthful outcomes

Use this table when updating state:

| Review result | Live feature status | Local sprint | Archive | Next route |
| --- | --- | --- | --- | --- |
| PASS with evidence | completed / done | cleared after archive verification | create `docs/archive/<id>_<timestamp>/` | `generator-proposal` |
| FAIL with evidence | still active / failed-open | preserve `.harness/<id>/` | none | `generator-execution` |
| BLOCKED with evidence | still active / blocked | preserve `.harness/<id>/` | none | orchestrator decision after blocker resolution |
| Missing evidence | still active | preserve `.harness/<id>/` | none | proper review |

If you cannot make the repository tell a coherent story from the files on disk, stop and preserve the sprint rather than lying with state.
