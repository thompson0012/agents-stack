---
name: generator-brainstorm
purpose: Explore pre-proposal work in durable idea artifacts, refine candidate directions, and promote at most one idea into tracked backlog state when it is ready for proposal.
trigger: Use when no runnable active sprint should start yet and a dependency-ready item still needs ideation before proposal, or when the human explicitly asks for backlog brainstorming.
inputs:
  - AGENTS.md
  - docs/live/features.json
  - docs/live/ideas.md
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/*
outputs:
  - updated docs/live/ideas.md
  - optional precise update to docs/live/features.json
boundaries:
  - Operate only on durable idea and backlog artifacts.
  - Do not edit product code, tests, app assets, or `.harness/<feature-id>/` sprint files.
  - Do not claim `runnable_active_sprint_id` or otherwise mark a runnable active sprint.
  - Do not turn brainstorming notes into an implementation plan disguised as a proposal.
next_skills:
  - generator-proposal
---

# Generator Brainstorm

## Mission
Turn vague, premature, or competing backlog thoughts into durable exploration that future workers can trust.

This phase exists before proposal work. Its job is to clarify problems, constraints, and candidate directions without pretending that implementation scope is already known.

A good brainstorm output makes one of two truths obvious:
- this candidate still needs more thinking, so it stays in `docs/live/ideas.md` and may remain `needs_brainstorm`
- this candidate is now concrete enough to promote into `docs/live/features.json` for bounded proposal work

Brainstorm never claims the single runnable active sprint slot. It prepares work for later selection; it does not open `.harness/<feature-id>/` or start execution.

## Worker Dispatch Contract

- Run brainstorming in a fresh worker context. The orchestrator dispatches this worker; it does not brainstorm inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: durable backlog state only. Reads across `docs/live/*`, `docs/reference/*`, and `AGENTS.md`; writes only to `docs/live/ideas.md` and the narrow `docs/live/features.json` updates needed to promote or restate candidate backlog truth.
- Not parallel-safe for writes. This worker owns `docs/live/ideas.md` and any related `features.json` update for the selected candidate during its run.
- Durable return contract: an updated `docs/live/ideas.md` plus an optional truthful `docs/live/features.json` update. Include `worker_id` and `orchestrator_run_id` in any durable note only if the host already provides them.

## Required Reads
Read these before changing anything:

1. `AGENTS.md`
2. `docs/live/features.json`
3. `docs/live/ideas.md`
4. `docs/live/progress.md` and `docs/live/memory.md`
5. Relevant `docs/reference/*` that constrain the idea space

If `docs/live/ideas.md` is missing or obviously boilerplate, repair it first instead of inventing ephemeral brainstorm context in chat.

## Expected Outputs

### `docs/live/ideas.md`
A durable exploration record that keeps ideation legible across sessions. For the idea or backlog item you touch, capture at minimum:
- working title or linked feature id
- current state such as exploring, promoted, parked, or rejected
- problem statement in current-repo terms
- why the idea matters now, if known
- dependencies, constraints, and assumptions
- rejected or risky directions worth remembering
- open questions blocking proposal-quality scoping
- the promotion signal that would justify moving the item into `features.json`

### Optional `docs/live/features.json` update
Use this only when the brainstorm produced a truthful backlog change.

Valid cases:
- create or refine a backlog entry that should be tracked durably
- keep or set `status: "needs_brainstorm"` when ideation is still required before proposal
- promote one candidate to proposal-ready tracked work, usually by moving it to `pending`

Invalid cases:
- claiming `runnable_active_sprint_id`
- marking a feature `in_progress`, `contracted`, or otherwise runnable from brainstorming alone
- opening `.harness/<feature-id>/`

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

### 4. Promote at most one candidate when it becomes proposal-ready
Promotion means the idea is now specific enough to deserve tracked proposal work.

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
- `docs/live/features.json` may change only to truthfully track brainstorm-needed or proposal-ready backlog state.
- Do not create `.harness/<feature-id>/` from brainstorming.
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
- captures durable reasons, constraints, and rejected options
- promotes at most one candidate only when proposal work is justified
- keeps `docs/live/features.json` authoritative for tracked work
- preserves the single-runnable-sprint rule by staying pre-sprint and non-runnable

## Done Definition
This skill is done when `docs/live/ideas.md` truthfully captures the explored candidate, any related backlog item in `docs/live/features.json` accurately says `needs_brainstorm` or `pending`, and no runnable sprint slot has been claimed.