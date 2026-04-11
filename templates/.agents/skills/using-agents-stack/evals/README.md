# evaluating the using-agents-stack skill package

This package should be evaluated as a router and durable-state interpreter, not as an implementation skill. The primary question is whether it sends a new agent to the correct child skill using only repository evidence and whether retry/parked-state gates fail closed when the files say automation must stop.

## Included evaluation scaffolding

- `scripts/validate_router.py`: structural validator for the router package and `references/children.json`
- `evals/evals.json`: file-grounded router regression cases for route selection, contradiction handling, parked-state behavior, retry truthfulness, and explicit `No family child fits` outcomes
- `evals/trigger-evals.json`: discovery-noise checks for when the router should load at all, including contradiction, parked, and no-family-child asks
- `guard-eval-fixtures.md`: temporal retry-gate fixtures that check before/action/after correctness and fail-closed behavior; these are not router route-selection checks
- `review-convergence-fixtures.md`: review/state-update publishability fixtures that check coverage closure, convergence closure, and PASS fail-closed behavior; these are not router route-selection or retry-eligibility checks

Run the structural validator first, then use the router eval files to regression-test route selection and trigger quality. Evaluate retry guards separately with the temporal fixture lane documented in [guard-eval-fixtures.md](./guard-eval-fixtures.md). Evaluate PASS publishability separately with the convergence fixture lane documented in [review-convergence-fixtures.md](./review-convergence-fixtures.md). Both fixture lanes verify fail-closed gating, not child selection.

Treat the eval corpus as regression input, not a second contract. `SKILL.md`, `references/children.json`, `references/state-machine.md`, and the other reference docs remain canonical.

## Advisory synthesis experiment

> `scripts/compile_guard_experiment.py` is an offline, advisory-only experiment.

Use it only through explicit manual invocation. It reads the current hand-authored retry guard sources and prints a report-style comparison/suggestion summary to stdout for human inspection. It does not write files, does not choose children, and loses to `references/children.json`, the existing reference docs, and `scripts/verify_retry_guard.py`.

## What to evaluate

### 1. Router selection from durable files

The root skill should select exactly one child skill from the eight allowed children, or explicitly say that no family child fits. Router evals in this directory verify route selection and durable-state fidelity only; they do not stand in for temporal retry gating.

Allowed children:

- `project-initializer`
- `generator-brainstorm`
- `generator-proposal`
- `evaluator-contract-review`
- `generator-execution`
- `adversarial-live-review`
- `state-update`
- `compound-capture`

Checks:

- missing or unusable `docs/live/tracked-work.json` routes to `project-initializer`
- non-empty `compound_pending_feature_ids` routes to `compound-capture` before runnable resume or backlog selection
- no runnable sprint and a dependency-ready `needs_brainstorm` item routes to `generator-brainstorm` even when another sprint is only parked
- no runnable sprint, no compound queue, and a dependency-ready `pending` item routes to `generator-proposal`
- `sprint_proposal.md` without `contract.md` routes to `evaluator-contract-review`
- `contract.md` without `handoff.md` routes to `generator-execution`
- `handoff.md` without `review.md` routes to `adversarial-live-review`
- `review.md` or any other reconciled-late artifact contradiction routes to `state-update`
- reconciled `review_failed` and `build_failed` only route back to `generator-execution` when retry metadata is truthful and compounding is already clear

### 2. Contradictions, parked state, and impossible routes

The router should fail safe when the state is contradictory or when automation is already at a durable human boundary. It must not declare success because one file looks plausible.

Checks:

- multiple runnable or active-vs-parked contradictions are treated as state integrity problems and routed to `state-update`
- a locally parked `awaiting_human` or `escalated_to_human` sprint is not silently treated as runnable just because stale live state says so
- parked sprints remain visible without blocking dependency-ready backlog work that can honestly proceed
- when the only remaining work is a fully reconciled parked sprint and no dependency-ready backlog item exists, the router says `No family child fits; answer directly.` instead of fabricating another child route
- impossible retry routes fail back to reconciliation rather than pretending execution is still safe

### 3. Trigger quality

`trigger-evals.json` checks whether the router should load at all.

Checks:

- explicit harness-phase selection, contradiction reconciliation, retry ownership, parked-state routing, and no-family-child questions should trigger the router
- ordinary implementation, generic planning, or routine PR-fix requests should not trigger the router just because the repository happens to use agents-stack

### 4. Temporal retry guards

Guard fixtures are separate because they answer a different question: not "which child owns the next step?" but "did the retry gate allow only the truthful transition and deny everything else?"

Checks:

- `review_failed` clean-resume eligibility is proven from durable `review.md`, `status.json`, and live tracked-work state
- `build_failed` clean-resume eligibility is proven from durable `runtime.md`, `status.json`, and live tracked-work state
- missing `clean_restore_ref`, exhausted attempt budgets, stale sprint ownership, and non-empty compound queues deny retry instead of being normalized away
- the fixture lane demands temporal evidence so a static end-state snapshot cannot reward-hack its way into a false allow

### 5. Review convergence and PASS publishability

Review-convergence fixtures are separate because they answer a different question: not "which child runs next?" and not "may a retry start?" but "may this PASS review publish and archive yet?"

Checks:

- PASS requires explicit review coverage metadata showing every acceptance criterion was accounted for
- PASS requires explicit convergence closure and zero open non-duplicate P0-P3 findings before `state-update` may publish or archive
- duplicate-linked findings marked `duplicate_of` do not double-count as blockers
- advisory-only findings below the blocking severity range do not block convergence
- missing coverage metadata or missing convergence metadata denies PASS and forces deny / re-review

## Suggested router case groups

- initialization and missing-live-state cases
- compound queue beats retry or backlog selection
- brainstorm-ready and proposal-ready backlog selection when no runnable sprint exists
- proposal, contract, execution, handoff, and review artifact-gate routing
- contradictory review/live-state cases that must reconcile through `state-update`
- parked-sprint cases that either route around the blocker honestly or return `No family child fits`
- retry cases split cleanly between allowed `review_failed`, allowed `build_failed`, and denied unsafe retries
- review convergence cases split cleanly between publishable PASS, open-blocker denial, and missing-metadata denial

## Pass criteria

The package passes evaluation when all of the following are true:

- the router can be followed without chat context
- every state transition has a single owning child skill or an explicit `No family child fits` result
- contradictory and parked state is surfaced instead of normalized away
- the package reinforces the single-runnable-sprint rule
- PASS reviews still archive via `state-update`, and FAIL/build-failed retries resume execution only after reconciliation, compounding, and truthful retry gating
- guard fixtures distinguish review-failed clean resume, build-failed clean resume, and deny paths instead of flattening them into one generic retry story
- review-convergence fixtures distinguish publishable PASS from deny / re-review based on complete coverage, explicit convergence closure, and zero open non-duplicate P0-P3 findings

## Failure criteria

The package fails evaluation if any of the following happen:

- the router performs implementation or review work instead of routing
- the package treats missing or contradictory state as success
- child skill selection depends on chat memory or unwritten assumptions
- parked human-owned sprints are auto-dispatched back into execution without a durable change to the checkpoint
- retry logic allows execution without the specific evidence required for that failed phase
- PASS or archive is allowed while open non-duplicate P0-P3 findings remain, or while coverage / convergence metadata is missing
- the same durable state could reasonably produce multiple different routes without additional rules