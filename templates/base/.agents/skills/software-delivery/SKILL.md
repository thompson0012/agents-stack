---
name: software-delivery
description: Use when a software feature request could plausibly need discovery, scope definition, delivery-control orchestration, plan review, independent frontend acceptance, implementation, web builder QA, or ship-readiness reflection and the agent must choose the narrowest next skill.
---

# Software Delivery

Use this router when the request is about delivering a non-trivial software feature and more than one delivery-stage or delivery-control skill could fit.

Do not perform the stage work here. Choose the narrowest next skill, then hand off.

## Core Contract

- Choose exactly one primary route or decide that no software-delivery route fits.
- Prefer the earliest unmet delivery need: discovery before spec, spec before cross-session delivery-control design, delivery-control design before plan review.
- Prefer `software-delivery/frontend-evaluator` over `website-building` when the main need is independent browser-facing acceptance rather than implementation or builder-side QA.
- Prefer `website-building` over generic implementation only when user-facing web behavior, browser implementation, builder-side browser QA, or web child routing is the main risk.
- Use `self-cognitive` only when ship-readiness, confidence checking, retrospective learning, or postmortem reflection is the main need.
- Use `references/children.json` as the source of truth for child boundaries, external targets, install hints, and honest next-step recommendations.
- External targets such as `feature-spec`, `coding-and-data`, `website-building`, and `self-cognitive` remain shared skills. This router may route to them, but it does not redefine them.

## Decision Order

Apply these checks in order.

### 1. Is the feature idea or problem still fuzzy?
Route to `software-delivery/feature-discovery` when the team is still sorting out the user problem, opportunity, constraints, or what should be built at all.

### 2. Is the main need a scoped artifact?
Route to `feature-spec` when the team wants a PRD, scope, non-goals, acceptance criteria, or another concrete requirements artifact.

### 3. Is the main need cross-session delivery control or harness design?
Route to `software-delivery/harness-design` when the work needs explicit control over single-session vs compacted continuation vs planner/generator/evaluator loops, plus the handoff artifacts and pass/fail boundaries that keep multi-session execution honest.

Use this lane for orchestration and control. Do not use it for ordinary single-session stage selection that the router already handles.

### 4. Is there already a plan that needs challenge before building?
Choose exactly one review lane based on the dominant risk:
- `software-delivery/plan-product-review` for value, scope, sequencing, user outcomes, and MVP cuts
- `software-delivery/plan-engineering-review` for architecture, edge cases, reversibility, tests, rollout, and observability
- `software-delivery/plan-design-review` for UX flows, states, accessibility, interaction clarity, and interface quality

### 5. Is the main need independent browser-facing acceptance?
Route to `software-delivery/frontend-evaluator` when browser-facing work already exists and the user wants a skeptical pass/fail QA gate with evidence, defects, and retry guidance.

This lane verifies; it does not implement or fix.

### 6. Is browser-facing web work the main implementation risk?
Route to `website-building` when the main need is building a user-facing web experience or doing builder-side browser QA, especially when browser behavior or web child routing matters more than generic repo mechanics.

### 7. Is the team ready for repo-backed implementation?
Route to `coding-and-data` when the plan is stable enough to implement in code, debug in an existing repo, add tests, or perform structured data work tied to delivery.

### 8. Is the main need confidence, readiness, or learning?
Route to `self-cognitive` for ship-readiness checks, risky commitments, retrospectives, postmortems, or explicit confidence calibration after planning or implementation.

### 9. No software-delivery route
If none of the above fits cleanly, do not force this family.

## Router Output

Return one of these forms and then invoke the selected skill if needed:

- `Route to software-delivery/feature-discovery.`
- `Route to feature-spec.`
- `Route to software-delivery/harness-design.`
- `Route to software-delivery/plan-product-review.`
- `Route to software-delivery/plan-engineering-review.`
- `Route to software-delivery/plan-design-review.`
- `Route to software-delivery/frontend-evaluator.`
- `Route to website-building.`
- `Route to coding-and-data.`
- `Route to self-cognitive.`
- `Install <child-path>, then route to <child-path>.`
- `No software-delivery route fits; answer directly.`

Add one sentence explaining why the selected route is the narrowest correct fit.

## References

- `references/children.json`

## Failure Modes to Avoid

- treating a fuzzy feature request as implementation work before the problem is stable
- routing to product review when the user actually needs a requirements artifact
- routing `software-delivery/harness-design` for ordinary single-session stage selection instead of true cross-session delivery control
- routing to engineering review when the dominant question is UI or UX quality
- routing to `website-building` when the main need is independent frontend acceptance rather than implementation with builder-side QA
- routing to `coding-and-data` when the main uncertainty is browser-facing web behavior and QA
- routing to `self-cognitive` before discovery, scoping, review, implementation, or independent acceptance work has actually happened
