---
name: delivery-control
description: Use when a software feature request needs delivery-control orchestration, multi-session loop design, or independent frontend QA. For greenfield product definition (strategy, PRDs, v1 architecture), use labs21-product-suite instead.
---

# Delivery Control

Use this router to enforce delivery governance and execution honesty on feature work that is already defined.

For net-new product creation, raw ideas, comprehensive PRDs, or system architecture from scratch, use `labs21-product-suite` instead.

Do not perform the stage work here. Choose the narrowest next skill, then hand off.

## Core Contract

- Defer greenfield product definition (Strategy, MVP, PRDs, System Architecture) to `labs21-product-suite`. `delivery-control` governs how to deliver; `labs21-product-suite` defines what to build.
- Choose exactly one primary route or decide that no delivery-control route fits.
- Use `references/children.json` as the source of truth for child boundaries.

## Decision Order

Apply these checks in order.

### 0. Is this a net-new product or greenfield initiative?
Route to `labs21-product-suite` if the user is starting from a raw idea, needs a strategic blueprint, a comprehensive PRD, or a baseline system architecture.

### 1. Is the main need cross-session delivery control or harness design?
Route to `delivery-control/harness-design` when the work needs explicit control over single-session vs compacted continuation vs planner/generator/evaluator loops, plus the handoff artifacts and pass/fail boundaries that keep multi-session execution honest.

Use this lane for orchestration and control. Do not use it for ordinary single-session work.

### 2. Is the main need independent browser-facing acceptance?
Route to `delivery-control/frontend-evaluator` when browser-facing work already exists and the user wants a skeptical pass/fail QA gate with evidence, defects, and retry guidance.

This lane verifies; it does not implement or fix.

### 3. No delivery-control route
If none of the above fits cleanly, do not force this family. Answer directly or let the agent fall back to generic repo implementation skills.

## Router Output

Return one of these forms and then invoke the selected skill if needed:

- `Route to labs21-product-suite.`
- `Route to delivery-control/harness-design.`
- `Route to delivery-control/frontend-evaluator.`
- `No delivery-control route fits; answer directly.`

Add one sentence explaining why the selected route is the narrowest correct fit.

## References

- `references/children.json`

## Failure Modes to Avoid

- routing to `delivery-control` for greenfield product definition, v1.0 PRDs, or baseline system architecture instead of `labs21-product-suite`
- routing `delivery-control/harness-design` for ordinary single-session stage selection instead of true cross-session delivery control
