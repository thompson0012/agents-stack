---
name: generator-brainstorm
description: Use when no runnable active sprint should start yet and a dependency-ready item still needs ideation before proposal, or when the human explicitly asks for backlog brainstorming.
purpose: Explore pre-proposal work in durable idea artifacts, refine candidate directions, and promote at most one idea into tracked backlog state when it is ready for proposal.
trigger: Use when no runnable active sprint should start yet and a dependency-ready item still needs ideation before proposal, or when the human explicitly asks for backlog brainstorming.
inputs:
  - AGENTS.md
  - docs/live/tracked-work.json
  - docs/live/ideas.md
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/*
  - linked docs/records/* for the selected tracked feature when present
outputs:
  - updated docs/live/ideas.md
  - optional scoped `docs/records/*` note for an already-tracked feature or initiative
  - optional precise update to docs/live/tracked-work.json
  - `.harness/<workstream-id>/status.json` when the selected item is already a tracked workstream
boundaries:
  - Operate only on durable idea, record, backlog, and selected-workstream planning artifacts.
  - Do not edit product code, tests, app assets, or later-phase `.harness/<workstream-id>/` execution/review files.
  - Do not claim `runnable_active_sprint_id` or otherwise mark a runnable active sprint.
  - Do not turn brainstorming notes into an implementation plan disguised as a proposal.
  - Do not create a record for untracked ideation or let `docs/records/*` become a second registry, contract, or archive.
next_skills:
  - generator-proposal
---

# Generator Brainstorm

## Mission
Turn vague, premature, or competing backlog thoughts into durable exploration that future workers can trust.

This phase exists before proposal work. Its job is to clarify problems, constraints, and candidate directions without pretending that implementation scope is already known.

A good brainstorm output makes one of two truths obvious:
- this candidate still needs more thinking, so it stays in `docs/live/ideas.md` and may remain `needs_brainstorm`
- this candidate is now concrete enough to promote into `docs/live/tracked-work.json` for bounded proposal work

Brainstorm never claims the single runnable active sprint slot. It prepares work for later selection; when the item is already tracked, it may refresh `.harness/<workstream-id>/status.json` as the canonical planning checkpoint, but it does not start execution.

## Worker Dispatch Contract

- Run brainstorming in a fresh worker context. The orchestrator dispatches this worker; it does not brainstorm inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: durable backlog state plus the selected workstream's planning checkpoint. Reads across `docs/live/*`, `docs/reference/*`, `docs/records/*` when linked, `AGENTS.md`, and existing `.harness/<workstream-id>/status.json` when present; writes to `docs/live/ideas.md`, optional scoped `docs/records/*`, the narrow `docs/live/tracked-work.json` updates needed to promote or restate candidate backlog truth, and `.harness/<workstream-id>/status.json` for the selected tracked workstream.
- Not parallel-safe for writes. This worker owns `docs/live/ideas.md`, any scoped record page it creates or updates for the selected tracked feature, any related `tracked-work.json` update during its run, and the selected workstream's `.harness/<workstream-id>/status.json` when that file exists or must be created.
- Durable return contract: an updated `docs/live/ideas.md` plus optional truthful `docs/records/*`, `docs/live/tracked-work.json`, and `.harness/<workstream-id>/status.json` updates. Include `worker_id` and `orchestrator_run_id` in durable notes only if the host already provides them.
- Dispatch framing is non-authoritative. Before acting, verify that the dispatched feature still matches `docs/live/tracked-work.json`, that the claimed phase still matches the strongest local/live artifact on disk, and that stronger evidence in the `AGENTS.md` precedence chain beats any dispatch summary, stale resume hint, or copied orchestrator context.
- If those checks disagree with the dispatch frame, stop before writing, preserve the existing truthful files, and hand control back to the orchestrator for correct-lane dispatch.

## Required Reads
Read these before changing anything:

1. `AGENTS.md`
2. `docs/live/tracked-work.json`
3. `docs/live/ideas.md`
4. `docs/live/progress.md` and `docs/live/memory.md`
5. Relevant `docs/reference/*` that constrain the idea space
6. Any existing `docs/records/*` already linked from the selected tracked feature or initiative
7. Existing `.harness/<workstream-id>/status.json` when the selected tracked workstream already has a local planning checkpoint

If `docs/live/ideas.md` is missing or obviously boilerplate, repair it first instead of inventing ephemeral brainstorm context in chat.

## Expected Outputs

### `docs/live/ideas.md`
A durable exploration record that keeps ideation legible across sessions. For the idea or backlog item you touch, capture at minimum:
- working title or linked feature id
- current state such as exploring, promoted, parked, or rejected
- problem statement in current-repo terms
- why the idea matters now, if known
- dependencies, constraints, and assumptions
- hidden assumptions, reward-hackable shortcuts, or happy-path framing that must be challenged before promotion
- rejected or risky directions worth remembering
- open questions blocking proposal-quality scoping
- the promotion signal that would justify moving the item into `tracked-work.json`

### Optional `docs/records/*` update
Use this only when the brainstorm produced durable discussion residue that is too large, too nuanced, or too likely to be revisited for `docs/live/ideas.md` alone.

Valid cases:
- the candidate already exists as a tracked feature or initiative in `docs/live/tracked-work.json`
- the record captures scoped rationale, option analysis, research residue, or decision context that should survive across sessions but is not stable reference truth
- `docs/live/tracked-work.json` is updated in the same pass so the feature's `record_paths` point back to the record
- `docs/live/ideas.md` keeps a concise summary and promotion signal instead of duplicating the whole record

Invalid cases:
- using a record to bypass creating or updating the tracked feature entry in `docs/live/tracked-work.json`
- storing untracked ideation that still belongs in `docs/live/ideas.md`
- turning a record into a hidden proposal, sprint contract, or second archive
- creating record pages for generic brainstorming with no tracked feature anchor

## Workflow

### 1. Confirm that brainstorming is the correct phase
Use this phase when the next work item is not yet proposal-ready.

Typical triggers:
- a tracked backlog item says `status: "needs_brainstorm"`
- a promising idea exists only in rough notes and needs durable refinement
- multiple candidate directions exist and the repo needs a durable recommendation before proposal

If the candidate is already bounded enough for proposal review, stop ideating and hand off to `generator-proposal` instead of reopening the question.

### 2. Ground the idea in durable repo truth
Read the live ledger and reference docs before refining anything.

Carry forward only facts you can defend from the repository state:
- known dependencies
- known architectural constraints
- already failed or rejected directions recorded in memory or progress
- current backlog ordering and human decisions

Do not pretend an idea is novel if durable state already records why it was deferred, rejected, or blocked.

### 3. Refine the idea backlog, not the implementation
Update `docs/live/ideas.md` so the next worker can understand:
- what problem is being explored
- what is still uncertain
- which options were considered and why some are weaker
- what evidence would make the idea proposal-ready

Stay at the backlog and product-decision level. Brainstorm is not the place to write sprint file lists, implementation steps, or execution instructions.

### 3a. Create a scoped record only when the tracked feature already exists
If the selected item is already tracked in `docs/live/tracked-work.json` and the durable discussion is too large or nuanced for `docs/live/ideas.md`, create or update one scoped page under `docs/records/*` in the same pass instead of deferring the residue to chat. Keep the record page-local: note its scope, current status, any supersession relationship, and the sprint or archive evidence it draws from when known.

When you do this:
- keep `docs/live/ideas.md` as the concise idea ledger
- update the feature entry's `record_paths` in `docs/live/tracked-work.json` in the same pass
- do not create a second registry or a hidden contract; the record is supporting residue, not runnable authority
- leave untracked ideation in `docs/live/ideas.md` rather than spawning a record page

### 3b. Attack the idea before promotion
Before you promote anything, challenge the brainstorm as if the next worker will overfit to the easiest happy path.

Record at minimum:
- the hidden assumptions that could make the proposal dishonest later
- what a reward-hacked sprint would look like for this idea
- at least one plausible alternative direction or smaller cut, and why it is weaker or not yet justified
- the repo fact or durable evidence that keeps the promoted direction honest

If you cannot write that down clearly, the idea is not proposal-ready yet. Keep it in brainstorming instead of promoting a false sense of readiness.

### 4. Promote at most one candidate when it becomes proposal-ready
Promotion means the idea is now specific enough to deserve tracked proposal work.

Promote only after the blind-spot check in step 3b is recorded and the remaining open questions are narrow enough for adversarial proposal review.

When promoting:
- keep the backlog entry narrow and truthful
- preserve dependency information and priority
- leave `runnable_active_sprint_id` unchanged
- use `pending` only when the candidate is ready for bounded proposal work
- use `needs_brainstorm` when the item should stay tracked but still needs ideation

If two ideas become attractive at once, rank them in `ideas.md` and promote only the one that is actually ready. Do not create hidden parallel runnable work.

### 5. Leave the next step explicit
When you finish, the durable state should clearly answer one question: does this candidate need more brainstorming, or is it ready for proposal?

If the answer is still unclear, that is a failure to refine the idea enough. Fix the ambiguity in `ideas.md` before you stop.

## File Write Expectations
- `docs/live/ideas.md` is the primary artifact for this phase.
- `docs/live/tracked-work.json` may change only to truthfully track brainstorm-needed or proposal-ready backlog state and to register any linked `record_paths` for the touched feature.
- Scoped `docs/records/*` pages are optional supporting artifacts only for already-tracked features; they must never replace `ideas.md`, `tracked-work.json`, or later sprint-local contracts.
- When the item is already a tracked workstream, create or update `.harness/<workstream-id>/status.json` so the selected planning lane has a canonical local checkpoint without claiming runnable status.
- Do not edit `docs/archive/*` during this phase.
- Do not touch product code, tests, or runtime assets.

## Refusal and Stop Conditions
Stop and record the blocker truthfully when:
- another runnable sprint is already active and the request tries to use brainstorming to bypass it
- the candidate is so vague that even the problem statement cannot be grounded in repo reality
- the requested output is actually a proposal, contract, or implementation plan
- backlog truth would become ambiguous because promotion would imply multiple runnable next steps
- the repository already contains a better, more current durable explanation than the new brainstorm would add

When blocked, write the uncertainty down. Do not pad `ideas.md` with fake confidence.

## Quality Bar
A good brainstorm pass:
- makes open questions explicit instead of hiding them
- captures durable reasons, constraints, rejected options, and challenged assumptions
- uses `docs/records/*` only for scoped, feature-linked residue that would otherwise overload `ideas.md`
- promotes at most one candidate only when proposal work is justified
- keeps `docs/live/tracked-work.json` authoritative for tracked work and record linkage
- preserves the single-runnable-sprint rule by staying pre-sprint and non-runnable

## Done Definition
This skill is done when `docs/live/ideas.md` truthfully captures the explored candidate, any related backlog item in `docs/live/tracked-work.json` accurately says `needs_brainstorm` or `pending`, any optional record is feature-linked through `record_paths` instead of becoming a second registry, any selected tracked workstream has a truthful `.harness/<workstream-id>/status.json` planning checkpoint, and no runnable sprint slot has been claimed.