---
name: generator-proposal
description: Use when exactly one feature is ready to be scoped for proposal, including a candidate previously promoted from brainstorming, and no approved contract exists yet.
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
  - existing `.harness/<workstream-id>/status.json` or `.harness/<workstream-id>/sprint_proposal.md` when continuing a selected planning workspace
outputs:
  - .harness/<workstream-id>/sprint_proposal.md
  - .harness/<workstream-id>/status.json
  - optional scoped `docs/records/*` note when durable feature-linked discussion residue should survive outside the sprint contract
  - optional precise updates to docs/live/roadmap.md and docs/live/current-focus.md when broad-goal truth must be made durable before sprint reservation
  - optional precise update to docs/live/tracked-work.json to reserve the active sprint, keep canonical `.harness/<workstream-id>/` evidence truthful, and register any touched `record_paths`
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

## Placement
This is a nested child under `using-agents-stack`; its path is `using-agents-stack/generator-proposal/`, and the router selects it before standalone use.

## Mission
Turn a selected feature into a reviewable sprint proposal with explicit scope, observable outcomes, and hard boundaries.

A proposal is not a wish list. It is a contract candidate that should survive hostile review.

When the feature came from `docs/live/ideas.md`, carry forward only the parts that strengthen scope truth: the real problem, hard constraints, rejected directions, and open questions that still matter. Brainstorm is context, not permission to stay vague.

## Worker Dispatch Contract

- Run proposal drafting in a fresh worker context. The orchestrator dispatches this worker; it does not swap into proposal mode inline.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: repo discovery, sprint-local planning writes under `.harness/<workstream-id>/`, optional scoped `docs/records/*`, and the narrow live-state updates needed to make source-goal truth durable in `docs/live/roadmap.md`, `docs/live/current-focus.md`, and `docs/live/tracked-work.json`. Proposal work advances the selected planning workspace rather than inventing a parallel planning lane. No product-code edits.
- Parallel-safe only for read-only research across clearly disjoint code areas. One worker owns `.harness/<workstream-id>/sprint_proposal.md`, `status.json`, and any scoped record update for that feature; parallel helpers must not write those same files or overlap target areas.
- Copy `.harness/<workstream-id>/sprint_proposal.md` and `.harness/<workstream-id>/status.json` from the canonical templates at `references/templates/.harness/`. Fill placeholders; delete template comment blocks. Do not construct these files from memory.
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
9. Existing `.harness/<workstream-id>/` files if this is a revision, including `review_feedback.md` when resuming from `proposal_revision_required`

Do not propose from backlog text alone. You must inspect the real code so the file boundaries and acceptance checks are believable.

## Expected Outputs

### `.harness/<workstream-id>/sprint_proposal.md`
A concrete proposal containing at minimum:
- feature id and title
- **risk tier** (`T1` / `T2` / `T3`) — determined by the deterministic CLI: `scripts/classify_proposal_tier.py .harness/<workstream-id>/sprint_proposal.md`. T1: cosmetic/docs/config only. T2: standard change. T3: schema, auth, or data integrity change.
- problem statement in current-repo terms
- objective for this sprint only
- explicit in-scope work
- explicit deferred work for this sprint, with same-initiative deferrals named as later roadmap slices or re-authorization boundaries
- allowed files
- forbidden files or subsystem boundaries
- implementation approach at a high level
- observable acceptance criteria already shaped for contract review as stable `AC-###` entries
- verification plan with concrete commands or review steps
- risks, assumptions, and blockers, including hidden assumptions the sprint must not discover too late
- alternative directions or smaller cuts rejected because they would change the contract shape or hide the real goal
- questions that must be answered before contract approval
- when the work is likely to reach approval, acceptance criteria should already be close to the final contract shape, for example:
```md
- `AC-001` | stateful=no | reversible=no
  - Requirement: `POST /api/tasks` returns `201` for a valid payload.
  - Evidence: `curl` response plus persisted task record.
- `AC-002` | stateful=yes | reversible=yes
  - Requirement: Toggling the task filter updates the visible list and can be reversed.
  - Evidence: reviewer-visible selector or observable output.
  - Before state: all tasks are visible.
  - Action: enable the completed-only filter.
  - After state: only completed tasks remain visible.
  - Reverse check: disable the filter and confirm the full list returns.
```

- a structured **task decomposition** that breaks the sprint into bounded, independently-implementable units. Each task must declare:
  - `id` — unique task identifier
  - `symbols` — list of declared functions/types/interfaces, each with `name`, `kind` (function|method|type|interface), `signature`, and optional `file_hint`
  - `depends_on` — list of task ids this task requires (enables topological ordering)
  - `acceptance` — list of verifiable conditions specific to this task

The task decomposition must be provided as a fenced JSON block under `## Task Decomposition`:

```json
{
  "tasks": [
    {
      "id": "auth-module",
      "symbols": [
        {
          "name": "ValidateToken",
          "kind": "function",
          "signature": "func ValidateToken(token string) (*Claims, error)",
          "file_hint": "internal/auth/"
        }
      ],
      "depends_on": [],
      "acceptance": [
        "ValidateToken returns error on expired token",
        "ValidateToken returns Claims on valid token"
      ]
    }
  ]
}
```

This decomposition is machine-verifiable — `scripts/check_contract_symbols.py` will verify that every declared symbol exists in the code before review. Proposal approval is blocked if the task decomposition is missing, unparseable, or contains tasks that span multiple subsystems without explicit dependency declarations.
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
Reserve the feature in `docs/live/tracked-work.json` only after that lineage is durable and only if no other runnable item is already active (check `docs/live/tracked-work.json` for `runnable_active_sprint_id`). Keep the feature's canonical `evidence_path` pointed at `.harness/<workstream-id>/` while proposal work is still local.
Prefer the narrow control-plane helpers when the initializer has already seeded the live files and you know the required values: update `docs/live/roadmap.md` through `templates/docs/scripts/roadmap_ops.py`, refresh `docs/live/current-focus.md` through `templates/docs/scripts/render_current_focus.py`, then run `templates/docs/scripts/validate_live_control.py --repo-root <repo-root>` before reserving the sprint.
If those files do not exist yet because the repo is still in minimal bootstrap, stop and route through `project-initializer` instead of inventing a second control-plane shape from proposal work.
If the control files appear to drift from the committed bootstrap seeds rather than from current sprint truth, run `templates/docs/scripts/validate_bootstrap_alignment.py --repo-root <repo-root>` and hand control back to `project-initializer` instead of patching around the drift here.
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

### 3b. Classify the proposal's risk tier
After defining file boundaries and task decomposition, classify the proposal tier mechanically:

```bash
python scripts/classify_proposal_tier.py .harness/<workstream-id>/sprint_proposal.md
```

This returns the deterministic tier and the T3 signals that triggered it. Record the tier in `sprint_proposal.md` under `## Risk Tier`.
- If the tier is `T3`, the self-attack (step 4) must be especially thorough — this change touches critical infrastructure.
- If the tier is `T1`, you may note that the evaluator will use a lighter review, but do not skip the self-attack.

### 4. Attack the proposal before handoff
Before this proposal can move to review, try to break it yourself.

Force the draft to answer:
- what hidden assumptions would execution otherwise discover too late
- how the implementation could reward-hack each acceptance criterion with static state, canned output, skipped transitions, or omitted failure paths
- what contradictory or ambiguous states the wording still permits
- what plausible alternative direction or smaller cut was considered, and why this proposal is still the narrowest honest sprint

If the proposal cannot survive that self-challenge, revise it or send the feature back to brainstorming instead of handing review a happy-path draft.

### 5. Define observable success

Every acceptance outcome must be externally checkable and traceable by stable `AC-###` id.

For interactive behavior, prefer state-transition checks over static end states. A good interactive criterion names:
- the starting condition
- the exact action the reviewer performs
- the expected after-state
- the reverse or repeated action when the behavior should be reversible

Shape each criterion so contract review can promote it directly into `contract.md` without inventing a second format:
```md
- `AC-001` | stateful=no | reversible=no
  - Requirement: ...
  - Evidence: ...
- `AC-002` | stateful=yes | reversible=yes
  - Requirement: ...
  - Evidence: ...
  - Before state: ...
  - Action: ...
  - After state: ...
  - Reverse check: ...
```

For browser-visible UI work, each criterion must also name:
- the route, page, or component
- the viewport or device class when layout matters
- the selector, label, or visible text the reviewer should observe
- any fixture or input shape needed to reach the state

Consult the narrowest matching recipe before finalizing the proposal:
- `references/frontend-ui-contract-recipe.md` for browser-visible UI work
- `references/backend-api-contract-recipe.md` for backend endpoints, auth boundaries, and API-visible behavior
- `references/integration-contract-recipe.md` for third-party APIs, webhooks, storage providers, and other cross-system boundaries
- `references/async-worker-contract-recipe.md` for jobs, queues, schedulers, and other background execution
- `references/migration-contract-recipe.md` for schema, data backfills, and state transitions that must be proved across time

Good examples:
- a page renders a new control with a stable selector and criterion id `AC-001`
- before clicking the theme toggle the page is in light mode, after one click it is in dark mode, and a second click returns it to light mode
- at 390px wide, the card stack collapses to one column without overlap
- while the form is submitting, the button is disabled and a spinner is visible, and after success the form clears
- `POST /api/tasks` returns `201` with the expected JSON shape and creates exactly one durable record

Bad examples:
- “clean architecture”
- “better UX” without observable checks
- “support future extensibility”
- “screen shows dark mode” when the proposal never requires the reviewer to trigger the toggle
- any criterion that could pass from a static screenshot, hardcoded DOM, canned output, or pre-seeded final state without exercising the real path


### 6. Decompose into bounded, verifiable tasks

Translate the sprint scope into a structured task DAG:
- Identify the smallest independent units of work — each task should touch one subsystem, one concern.
- For each task, declare the exact symbols it must produce (function names, type names, interface names) with their signatures.
- Declare dependencies between tasks: if task B consumes task A's output, A must be listed in B's `depends_on`.
- Tasks with empty `depends_on` are leaf tasks and can be implemented first or in parallel.
- Tasks must not have circular dependencies.

Write the decomposition as a fenced JSON block under `## Task Decomposition` in the proposal. The format must match:
```json
{
  "tasks": [
    {
      "id": "<kebab-case-id>",
      "symbols": [
        {"name": "<SymbolName>", "kind": "function|method|type|interface",
         "signature": "<full signature>", "file_hint": "<subdirectory>/"}
      ],
      "depends_on": ["<other-task-id>"],
      "acceptance": ["<verifiable condition>"]
    }
  ]
}
```

This decomposition enables `scripts/check_contract_symbols.py` to mechanically verify that every declared symbol exists in the code before adversarial review. It also enables parallel execution of independent tasks.

If the sprint cannot be decomposed into bounded tasks with explicit symbol contracts, it is not ready for proposal. Stop and send it back to brainstorming or human clarification.

### 7. Draw hard file and subsystem boundaries

- List the exact files expected to change when possible.
- If exact files are not yet knowable, name the narrowest allowed directory and justify why.
- List forbidden files or subsystems so review can catch scope creep.
- Call out any architecture or dependency change explicitly; never bury it in prose.
- If finishing the stated source goal would require later sprints, name those as roadmap items or deferred work instead of smuggling them into this sprint.

### 8. Write the proposal as a review target
The proposal must let an evaluator answer:
- What will change?
- What will not change?
- How will we know it worked?
- What evidence will the generator need to provide?
- What hidden assumptions, reward-hack surfaces, or contradictory states has the proposal already attacked?
- For interactive or other stateful behavior, what before/action/after checks prevent a hardcoded fake pass?
- What must be deferred to later sprints?
- Does the proposal stay inside the currently authorized roadmap slice, or does it require re-authorization first?

### 8b. Handle revision feedback when resuming from rejection
When `.harness/<workstream-id>/review_feedback.md` exists (phase is `proposal_revision_required`):
- Read `review_feedback.md` and address every piece of feedback explicitly.
- Update `sprint_proposal.md` to fix the issues raised — tighten scope, add missing AC details, clarify assumptions, fix the task decomposition, etc.
- After all feedback is addressed, remove `review_feedback.md` (or rename it to `review_feedback.resolved.md` for audit trail).
- Update `status.json`: set phase back to `"proposed"`. Do NOT reset `proposal_revision_count` — it is managed by the evaluator and must accumulate across revision cycles for escalation to work.
- Do not skip feedback items or silently narrow the scope to avoid attack vectors — the reviewer will catch that on re-submission.

### 9. Set durable state for resume
- Write or update `status.json` so the next agent can resume from `sprint_proposal.md`.
- If this is a revision, replace stale proposal content rather than accumulating contradictory plans.
- If this workstream entered proposal from a local planning checkpoint, replace stale `needs_brainstorm` / `pending` phase state with truthful proposal state instead of leaving two competing local stories.
- Do not reserve or chain the sprint forward until `docs/live/roadmap.md` and `docs/live/current-focus.md` tell the same source-goal story as the proposal.

## File Write Expectations
- Write inside `.harness/<workstream-id>/` only for sprint-local state.
- Do not create `contract.md` in this phase.
- Do not touch `docs/archive/*`.
- Do not edit product code, tests, or app assets.
- Update `docs/live/roadmap.md` and `docs/live/current-focus.md` only when needed to make source-goal lineage and current authorization durable.
- Only update `docs/live/tracked-work.json` after that lineage is durable and only if needed to represent the single runnable active sprint truthfully, keep canonical `.harness/<workstream-id>/` evidence truthful, or register feature-linked `record_paths`.
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
- the sprint cannot be decomposed into bounded tasks with explicit symbol contracts (missing or circular dependencies, symbols without signatures, tasks that span unrelated subsystems)
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
- includes a structured task decomposition with explicit symbol contracts that can be mechanically verified

## Done Definition
This skill is done when the selected feature has one durable, bounded, reviewable sprint proposal with a structured, machine-verifiable task decomposition, any relevant brainstorm or record context has been distilled into explicit source-goal and roadmap truth, any optional `docs/records/*` update is linked back through the same feature entry in `docs/live/tracked-work.json`, and the repo state makes the next step unambiguous: adversarial contract review.

## Known Limitations

The task decomposition produced by this phase enforces **structural completeness** — every declared symbol must have a signature, dependencies must be acyclic, and tasks must be self-contained. This decomposition is machine-verifiable by downstream phases.

This phase DOES NOT guarantee:
- **Architectural quality** of the decomposition itself — the model decides how to partition the problem. A poor decomposition passes structural checks.
- **Correct dependency ordering** — the model declares dependencies; the harness checks they're acyclic and resolved, not that they reflect the true data flow.
- **Coverage of cross-cutting concerns** — if the model fails to include auth, audit, or error handling in the task decomposition, the harness cannot invent them.

The structured task decomposition is a **process artifact**, not an architectural review. For system-level design decisions, pair this phase with a stronger model or a human architecture review.
