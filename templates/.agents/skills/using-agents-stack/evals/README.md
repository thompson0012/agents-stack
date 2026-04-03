# evaluating the using-agents-stack skill package

This package should be evaluated as a router and durable-state interpreter, not as an implementation skill. The primary question is whether it sends a new agent to the correct child skill using only repository evidence.

## Included evaluation scaffolding

- `scripts/validate_router.py`: structural validator for the router package and `references/children.json`
- `evals/evals.json`: direct routing cases, ambiguous cases, and failure-retry cases
- `evals/trigger-evals.json`: discovery-noise checks so the router triggers when family routing is actually needed

Run the structural validator first, then use the eval files to regression-test route selection and trigger quality.

## What to evaluate

### 1. Routing correctness

The root skill should select exactly one child skill from the eight allowed children:

- `project-initializer`
- `generator-brainstorm`
- `generator-proposal`
- `evaluator-contract-review`
- `generator-execution`
- `adversarial-live-review`
- `state-update`
- `compound-capture`

Checks:

- missing or empty `docs/live/features.json` routes to `project-initializer`
- non-empty `compound_pending_feature_ids` routes to `compound-capture` before runnable resume or backlog selection
- no runnable sprint and a dependency-ready `needs_brainstorm` item routes to `generator-brainstorm`
- no runnable sprint, no compound queue, and at least one dependency-ready `pending` feature routes to `generator-proposal`
- `sprint_proposal.md` without `contract.md` routes to `evaluator-contract-review`
- `contract.md` without `handoff.md` routes to `generator-execution`
- `handoff.md` without `review.md` routes to `adversarial-live-review`
- `review.md` routes to `state-update`
- `review_failed` routes back to `generator-execution` only after state has been updated and queued compounding has been drained
### 2. State-file fidelity

The router must read durable files in the documented order and respect file meaning.

Checks:

- `AGENTS.md` is treated as the operating contract
- `docs/live/*` is treated as global state
- `.harness/<feature-id>/*` is treated as local sprint state
- later-phase artifacts outrank stale `status.json` fields
- archive folders are treated as historical evidence, not active state
- router output explains which files drove the decision

### 3. Failure handling and contradictions

The router should fail safe when the state is contradictory. It must not declare success because one file looks plausible.

Checks:

- multiple active sprints are detected as illegal state
- `paused_by_timeout` uses `resume_from` when valid and artifact precedence when invalid
- `blocked` is handled explicitly and not mistaken for completion
- `review.md` plus stale `contracted` status still routes to `state-update`
- empty state is treated as initialization, not as "nothing to do"

## Suggested test cases

### Case A: fresh repo

- `docs/live/features.json` missing or empty
- Expected route: `project-initializer`

### Case B: queued compounding

- `docs/live/features.json` contains `compound_pending_feature_ids`
- a runnable sprint may still exist, but the queue is not empty
- Expected route: `compound-capture`

### Case C: brainstorm-ready backlog

- no runnable active sprint
- highest-priority dependency-ready backlog item has `status: needs_brainstorm`
- `docs/live/ideas.md` exists
- Expected route: `generator-brainstorm`

### Case D: ready backlog, no runnable active sprint

- `features.json` contains dependency-ready `pending` feature(s), none runnable
- `compound_pending_feature_ids` is empty
- no `.harness/<feature-id>/` folder yet
- Expected route: `generator-proposal`

### Case E: proposal awaiting approval

- active feature exists
- `sprint_proposal.md` exists
- `contract.md` absent
- Expected route: `evaluator-contract-review`

### Case F: contracted sprint in execution

- `contract.md` exists
- `handoff.md` absent
- status says `contracted` or `in_progress`
- Expected route: `generator-execution`

### Case G: ready for live review

- `handoff.md` exists
- `review.md` absent
- Expected route: `adversarial-live-review`

### Case H: review recorded but not yet reconciled

- `review.md` exists
- `status.json.phase` is still pre-update or contradictory
- Expected route: `state-update`

### Case I: failed review already reconciled

- `review.md` exists and records FAIL
- `status.json.phase = review_failed`
- `docs/live/features.json` still points at the same active sprint
- `compound_pending_feature_ids` is empty because compounding already drained
- Expected route: `generator-execution`

### Case J: contradictory evidence

- `review.md` exists
- `status.json.phase = contracted`
- `features.json` still says pending
- Expected route: `state-update`, with contradiction explicitly noted

### Case K: stale timeout

- `status.json.phase = paused_by_timeout`
- `resume_from = handoff.md`
- Expected route: `adversarial-live-review`
## Pass criteria

The package passes evaluation when all of the following are true:

- the router can be followed without chat context
- every state transition has a single owning child skill
- contradictory state is surfaced instead of normalized away
- the package reinforces the single-runnable-sprint rule
- PASS reviews still archive via state-update, and FAIL reviews resume execution only after state-update has reconciled them.

## Failure criteria

The package fails evaluation if any of the following happen:

- the router performs implementation or review work instead of routing
- the package treats missing state as success
- child skill selection depends on chat memory or unwritten assumptions
- contradictory state is ignored
- the same repo state could reasonably produce multiple different routes without additional rules