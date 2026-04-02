---
name: generator-proposal
purpose: Convert one selected backlog item into a single bounded sprint proposal that can be reviewed adversarially.
trigger: Use when exactly one feature is ready to be scoped and no approved contract exists yet.
inputs:
  - AGENTS.md
  - docs/live/features.json
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/*
  - existing implementation in the target area
  - .harness/<feature-id>/sprint_proposal.md if revising an existing proposal
outputs:
  - .harness/<feature-id>/sprint_proposal.md
  - .harness/<feature-id>/status.json
  - optional precise update to docs/live/features.json to reserve the active sprint
boundaries:
  - Scope exactly one bounded sprint.
  - Do not implement code during this phase.
  - Do not hide architecture changes inside an implementation plan.
  - Do not claim a file boundary you have not checked against the repo.
next_skills:
  - evaluator-contract-review
---

# Generator Proposal

## Mission
Turn a selected feature into a reviewable sprint proposal with explicit scope, observable outcomes, and hard boundaries.

A proposal is not a wish list. It is a contract candidate that should survive hostile review.

## Worker Dispatch Contract

- Run proposal drafting in a fresh worker context. The orchestrator dispatches this worker; it does not swap into proposal mode inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: repo discovery, sprint-local planning writes under `.harness/<feature-id>/`, and the narrow `docs/live/features.json` reservation update when needed. No product-code edits.
- Parallel-safe only for read-only research across clearly disjoint code areas. One worker owns `.harness/<feature-id>/sprint_proposal.md` and `status.json`; parallel helpers must not write those same files or overlap target areas.
- Durable return contract: `.harness/<feature-id>/sprint_proposal.md`, `.harness/<feature-id>/status.json`, and optional `docs/live/features.json`. Include `worker_id` and `orchestrator_run_id` in `status.json` when the host provides them.

## Required Reads
Read these before drafting:

1. `AGENTS.md`
2. `docs/live/features.json`
3. `docs/live/progress.md` and `docs/live/memory.md`
4. Relevant `docs/reference/*`
5. The current code in every area you expect to touch
6. Existing `.harness/<feature-id>/` files if this is a revision

Do not propose from backlog text alone. You must inspect the real code so the file boundaries and acceptance checks are believable.

## Expected Outputs

### `.harness/<feature-id>/sprint_proposal.md`
A concrete proposal containing at minimum:
- feature id and title
- problem statement in current-repo terms
- objective for this sprint only
- explicit in-scope work
- explicit out-of-scope work
- allowed files
- forbidden files or subsystem boundaries
- implementation approach at a high level
- observable acceptance outcomes
- verification plan with concrete commands or review steps
- risks, assumptions, and blockers
- questions that must be answered before contract approval

### `.harness/<feature-id>/status.json`
A machine-readable checkpoint for resume and routing.
It should make the proposal state obvious, for example:
- `sprint_id`
- `phase: "proposed"` or `"proposal_revision_required"`
- `owner_role`
- `resume_from`
- timestamps and active process state if relevant

### Optional `docs/live/features.json` update
If the repo tracks reservation in backlog state, mark the selected feature as the single active sprint.
Do this only if no other item is already `in_progress`.

## Workflow

### 1. Select or confirm exactly one feature
- Use the explicit human-selected feature when provided.
- Otherwise use the highest-priority pending item from `features.json`.
- Refuse to proceed if another sprint is already active.

### 2. Bound the sprint by reading the real implementation surface
- Inspect the code paths likely to change.
- Identify the smallest meaningful increment that can be implemented and reviewed in one sprint.
- Split large or cross-cutting ideas before proposing anything.

### 3. Define observable success
Every acceptance outcome must be externally checkable.
Good examples:
- a page renders a new control with a stable selector
- a command prints a specific state transition
- an API returns a documented field shape under known input

Bad examples:
- “clean architecture”
- “better UX” without observable checks
- “support future extensibility”

### 4. Draw hard file and subsystem boundaries
- List the exact files expected to change when possible.
- If exact files are not yet knowable, name the narrowest allowed directory and justify why.
- List forbidden files or subsystems so review can catch scope creep.
- Call out any architecture or dependency change explicitly; never bury it in prose.

### 5. Write the proposal as a review target
The proposal must let an evaluator answer:
- What will change?
- What will not change?
- How will we know it worked?
- What evidence will the generator need to provide?
- What must be deferred to later sprints?

### 6. Set durable state for resume
- Write or update `status.json` so the next agent can resume from `sprint_proposal.md`.
- If this is a revision, replace stale proposal content rather than accumulating contradictory plans.

## File Write Expectations
- Write inside `.harness/<feature-id>/` only for sprint-local state.
- Do not create `contract.md` in this phase.
- Do not touch `docs/archive/*`.
- Do not edit product code, tests, or app assets.
- Only update `docs/live/features.json` if needed to represent the single active sprint truthfully.

## Refusal and Stop Conditions
Reject the proposal phase and leave a truthful blocker when:
- the requested work is too large for one bounded sprint
- acceptance criteria cannot be made observable from the current repo and tooling
- file boundaries cannot be identified because the feature is still conceptually vague
- the change implies hidden architecture work not acknowledged in scope
- another sprint is already active
- the repo state and backlog state disagree about what feature is active

When blocked, write the blocking reason explicitly. Do not compensate with a mushy proposal.

## Quality Bar
A good proposal:
- can be approved or rejected without a meeting
- is narrow enough to finish and review in one sprint
- names concrete files or tightly bounded directories
- exposes architecture changes instead of smuggling them in
- defines outcomes that a reviewer can verify from behavior
- leaves obvious future work out of scope instead of pretending to solve everything now

## Done Definition
This skill is done when the selected feature has one durable, bounded, reviewable sprint proposal and the repo state makes the next step unambiguous: adversarial contract review.