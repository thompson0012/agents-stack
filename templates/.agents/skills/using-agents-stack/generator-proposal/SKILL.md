---
name: generator-proposal
purpose: Convert one selected backlog item into a single bounded sprint proposal that can be reviewed adversarially.
trigger: Use when exactly one feature is ready to be scoped for proposal, including a candidate previously promoted from brainstorming, and no approved contract exists yet.
inputs:
  - AGENTS.md
  - docs/live/tracked-work.json
  - docs/live/current-focus.md
  - docs/live/roadmap.md
  - docs/live/ideas.md when the selected item was shaped by brainstorming or still carries idea-context worth preserving
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/*
  - linked docs/records/* for the selected feature when present
  - existing implementation in the target area
  - .harness/<workstream-id>/sprint_proposal.md if revising an existing proposal
outputs:
  - .harness/<workstream-id>/sprint_proposal.md
  - .harness/<workstream-id>/status.json
  - optional scoped `docs/records/*` note when durable feature-linked discussion residue should survive outside the sprint contract
  - optional precise updates to docs/live/roadmap.md and docs/live/current-focus.md when broad-goal truth must be made durable before sprint reservation
  - optional precise update to docs/live/tracked-work.json to reserve the active sprint and register any touched `record_paths`
boundaries:
  - Scope exactly one bounded sprint as a slice of the broader initiative, not a rewrite of it.
  - Do not implement code during this phase.
  - Do not hide architecture changes inside an implementation plan.
  - Do not claim a file boundary you have not checked against the repo.
  - Do not translate unresolved brainstorm notes into fake proposal certainty.
  - Do not invent source-goal intent or roadmap structure that the files and prompt cannot support.
  - Do not let `docs/records/*` become a second contract, second registry, or substitute for `.harness/<workstream-id>/sprint_proposal.md`.
next_skills:
  - evaluator-contract-review
---

# Generator Proposal

## Mission
Turn a selected feature into a reviewable sprint proposal with explicit scope, observable outcomes, and hard boundaries.

A proposal is not a wish list. It is a contract candidate that should survive hostile review.

When the feature came from `docs/live/ideas.md`, carry forward only the parts that strengthen scope truth: the real problem, hard constraints, rejected directions, and open questions that still matter. Brainstorm is context, not permission to stay vague.

## Worker Dispatch Contract

- Run proposal drafting in a fresh worker context. The orchestrator dispatches this worker; it does not swap into proposal mode inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: repo discovery, sprint-local planning writes under `.harness/<workstream-id>/`, optional scoped `docs/records/*`, and the narrow live-state updates needed to make source-goal truth durable in `docs/live/roadmap.md`, `docs/live/current-focus.md`, and `docs/live/tracked-work.json`. No product-code edits.
- Parallel-safe only for read-only research across clearly disjoint code areas. One worker owns `.harness/<workstream-id>/sprint_proposal.md`, `status.json`, and any scoped record update for that feature; parallel helpers must not write those same files or overlap target areas.
- Durable return contract: `.harness/<workstream-id>/sprint_proposal.md`, `.harness/<workstream-id>/status.json`, any optional `docs/records/*`, and any required `docs/live/roadmap.md` / `docs/live/current-focus.md` refresh before reservation, plus optional `docs/live/tracked-work.json`. Include `worker_id` and `orchestrator_run_id` in `status.json` when the host provides them.
- Dispatch framing is non-authoritative. Before acting, verify that the dispatched feature still matches `docs/live/tracked-work.json`, that the claimed phase still matches the strongest local/live artifact on disk, and that stronger evidence in the `AGENTS.md` precedence chain beats any dispatch summary, stale resume hint, or copied orchestrator context.
- If those checks disagree with the dispatch frame, stop before writing, preserve the existing truthful files, and hand control back to the orchestrator for correct-lane dispatch.

## Required Reads
Read these before drafting:

1. `AGENTS.md`
2. `docs/live/tracked-work.json`
3. `docs/live/current-focus.md` and `docs/live/roadmap.md`
4. `docs/live/progress.md` and `docs/live/memory.md`
5. `docs/live/ideas.md` when the selected backlog item came from brainstorming, references idea exploration, or still has open ideation context worth narrowing
6. Relevant `docs/reference/*`
7. Any linked `docs/records/*` for the selected feature when they contain durable rationale or prior decision residue
8. The current code in every area you expect to touch
9. Existing `.harness/<workstream-id>/` files if this is a revision

Do not propose from backlog text alone. You must inspect the real code so the file boundaries and acceptance checks are believable.

## Expected Outputs

### `.harness/<workstream-id>/sprint_proposal.md`
A concrete proposal containing at minimum:
- feature id and title
- problem statement in current-repo terms
- objective for this sprint only
- explicit in-scope work
- explicit deferred work for this sprint, with same-initiative deferrals named as later roadmap slices or re-authorization boundaries
- allowed files
- forbidden files or subsystem boundaries
- implementation approach at a high level
- observable acceptance outcomes
- verification plan with concrete commands or review steps
- risks, assumptions, and blockers, including hidden assumptions the sprint must not discover too late
- alternative directions or smaller cuts rejected because they would change the contract shape or hide the real goal
- questions that must be answered before contract approval

### `.harness/<workstream-id>/status.json`
A machine-readable checkpoint for resume and routing.
It should make the proposal state obvious, for example:
- `sprint_id`
- `phase: "proposed"` or `"proposal_revision_required"`
- `owner_role`
- `resume_from`
- timestamps and active process state if relevant

If the sprint already has retry metadata such as `attempt_count`, `max_attempts`, or `clean_restore_ref`, preserve it unless the proposal explicitly changes that policy. Proposal revision must not silently erase retry history.

### Optional live-state and record updates
If the selected work came from a broad user goal, first make the source-goal lineage explicit in `docs/live/roadmap.md` and `docs/live/current-focus.md`.
Reserve the feature in `docs/live/tracked-work.json` only after that lineage is durable and only if no other runnable item is already `in_progress`.
Do not use proposal work to pull a feature forward when the backlog still says `needs_brainstorm`; resolve that truth first. `tracked-work.json` remains the runnable/backlog selector and single registry, not the place to hide multi-sprint initiative intent.

If durable feature-linked discussion residue is too large or nuanced for `docs/live/ideas.md` but is not stable reference truth, you may create or refresh one scoped page under `docs/records/*` only when the feature already exists in `docs/live/tracked-work.json`. Register that path in the same feature entry's `record_paths`; do not let the record replace the proposal or become a shadow contract.
## Workflow

### 1. Select or confirm exactly one feature
- Use the explicit human-selected feature when provided.
- Otherwise use the highest-priority proposal-ready item from `tracked-work.json`.
- Refuse to proceed if another runnable sprint is already active.
- If the selected item is still `needs_brainstorm`, route back to brainstorming instead of writing a mushy proposal.

### 2. Pull forward only the brainstorm and record context that tightens the scope
- When an idea was promoted from `docs/live/ideas.md`, read the relevant section and extract only durable signals: problem framing, constraints, rejected directions, dependencies, and unresolved questions.
- When the selected feature already has linked `docs/records/*`, use them the same way: distill durable rationale into scope boundaries instead of copying exploratory bulk into the sprint.
- Convert that context into proposal boundaries. Do not copy open-ended exploration into the sprint as if it were approved scope.
- If the idea notes or linked records still contain competing directions that cannot fit one bounded sprint, split or return the item to brainstorming.

### 3. Distill the source goal into durable roadmap truth before reserving a sprint
- When a broad user prompt or brainstorm describes a broad initiative, write the durable source-goal, current authorized initiative, and explicit deferred lanes into `docs/live/roadmap.md`.
- Refresh `docs/live/current-focus.md` so a cold-start agent can see which roadmap slice is being turned into this sprint proposal and what artifact to open next.
- If the files do not support a clear single-sprint cut, first publish the broader initiative as a sequence of named roadmap slices and then write only the first bounded sprint; if a truthful slice decomposition still cannot be made, stop and send the work back to brainstorming or human clarification rather than reserving a runnable sprint.
- When you do cut a sprint, keep the broader initiative visible: the sprint objective is the first bounded slice of that initiative, not a new smaller project.
- Identify the smallest meaningful increment that can be implemented and reviewed in one sprint without discarding essential parts of the source goal.
- If choosing that increment would hide core requested work, surface the missing work as later roadmap slices and only proceed if the current slice still stands on its own; do not shrink the goal to fit.
- Split large or cross-cutting ideas into explicit later roadmap slices or re-authorization boundaries before proposing anything, and preserve the source-goal wording so the initiative itself is not rewritten into a smaller project.

### 4. Attack the proposal before handoff
Before this proposal can move to review, try to break it yourself.

Force the draft to answer:
- what hidden assumptions would execution otherwise discover too late
- how the implementation could reward-hack each acceptance criterion with static state, canned output, skipped transitions, or omitted failure paths
- what contradictory or ambiguous states the wording still permits
- what plausible alternative direction or smaller cut was considered, and why this proposal is still the narrowest honest sprint

If the proposal cannot survive that self-challenge, revise it or send the feature back to brainstorming instead of handing review a happy-path draft.

### 5. Define observable success

Every acceptance outcome must be externally checkable.

For interactive behavior, prefer state-transition checks over static end states. A good interactive criterion names:
- the starting condition
- the exact action the reviewer performs
- the expected after-state
- the reverse or repeated action when the behavior should be reversible

For browser-visible UI work, each criterion must also name:
- the route, page, or component
- the viewport or device class when layout matters
- the selector, label, or visible text the reviewer should observe
- any fixture or input shape needed to reach the state

For frontend UI work, consult `references/frontend-ui-contract-recipe.md` before finalizing the proposal. It keeps the prompt recipe and the proposal rubric aligned without turning the reference into a second contract.


Good examples:
- a page renders a new control with a stable selector
- before clicking the theme toggle the page is in light mode, after one click it is in dark mode, and a second click returns it to light mode
- at 390px wide, the card stack collapses to one column without overlap
- while the form is submitting, the button is disabled and a spinner is visible, and after success the form clears

Bad examples:
- “clean architecture”
- “better UX” without observable checks
- “support future extensibility”
- “screen shows dark mode” when the proposal never requires the reviewer to trigger the toggle
- any criterion that could pass from a static screenshot, hardcoded DOM, or canned output without exercising the browser path


### 6. Draw hard file and subsystem boundaries
- List the exact files expected to change when possible.
- If exact files are not yet knowable, name the narrowest allowed directory and justify why.
- List forbidden files or subsystems so review can catch scope creep.
- Call out any architecture or dependency change explicitly; never bury it in prose.
- If finishing the stated source goal would require later sprints, name those as roadmap items or deferred work instead of smuggling them into this sprint.

### 7. Write the proposal as a review target
The proposal must let an evaluator answer:
- What will change?
- What will not change?
- How will we know it worked?
- What evidence will the generator need to provide?
- What hidden assumptions, reward-hack surfaces, or contradictory states has the proposal already attacked?
- For interactive or other stateful behavior, what before/action/after checks prevent a hardcoded fake pass?
- What must be deferred to later sprints?
- Does the proposal stay inside the currently authorized roadmap slice, or does it require re-authorization first?

### 8. Set durable state for resume
- Write or update `status.json` so the next agent can resume from `sprint_proposal.md`.
- If this is a revision, replace stale proposal content rather than accumulating contradictory plans.
- Do not reserve or chain the sprint forward until `docs/live/roadmap.md` and `docs/live/current-focus.md` tell the same source-goal story as the proposal.

## File Write Expectations
- Write inside `.harness/<workstream-id>/` only for sprint-local state.
- Do not create `contract.md` in this phase.
- Do not touch `docs/archive/*`.
- Do not edit product code, tests, or app assets.
- Update `docs/live/roadmap.md` and `docs/live/current-focus.md` only when needed to make source-goal lineage and current authorization durable.
- Only update `docs/live/tracked-work.json` after that lineage is durable and only if needed to represent the single runnable active sprint truthfully or to register feature-linked `record_paths`.
- Read `docs/live/ideas.md` and any linked `docs/records/*` only when they materially narrow the selected feature; do not bloat the proposal with generic brainstorm notes or turn records into a shadow contract.

## Refusal and Stop Conditions
Reject the proposal phase and leave a truthful blocker when:
- the requested work cannot be truthfully partitioned into a first bounded sprint plus named later roadmap slices, or it would only fit after redefining the source goal into a smaller different project
- acceptance criteria cannot be made observable from the current repo and tooling
- an interactive or other stateful criterion can be satisfied by a static final screenshot, hardcoded final value, pre-seeded data, or canned output instead of a real transition
- hidden assumptions, contradictory states, or reward-hack surfaces remain implicit
- file boundaries cannot be identified because the feature is still conceptually vague
- the selected item still needs brainstorming before proposal
- the change implies hidden architecture work not acknowledged in scope
- the source goal or roadmap slice is still implicit, contradictory, or unsupported by the files
- late scope discovery shows that additional roadmap authorization is required before another sprint can be reserved or chained forward
- another runnable sprint is already active
- the repo state and backlog state disagree about what feature is active
When blocked, write the blocking reason explicitly. Do not compensate with a mushy proposal.

## Quality Bar
A good proposal:
- can be approved or rejected without a meeting
- is narrow enough to finish and review in one sprint
- names concrete files or tightly bounded directories
- exposes architecture changes instead of smuggling them in
- attacks hidden assumptions, reward-hack paths, and contradictory states before review sees the draft
- defines outcomes that a reviewer can verify from behavior and state transitions
- uses brainstorm or record context only to sharpen scope, not to excuse vagueness
- leaves obvious future work as named later roadmap slices instead of pretending to solve everything now

## Done Definition
This skill is done when the selected feature has one durable, bounded, reviewable sprint proposal, any relevant brainstorm or record context has been distilled into explicit source-goal and roadmap truth, any optional `docs/records/*` update is linked back through the same feature entry in `docs/live/tracked-work.json`, and the repo state makes the next step unambiguous: adversarial contract review.