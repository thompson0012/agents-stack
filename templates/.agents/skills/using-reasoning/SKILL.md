---
name: using-reasoning
description: Use when a request is analytical and could plausibly fit more than one reasoning child such as integrated reasoning, scenario planning, or hidden-rule survivability checks.
---

# Using Reasoning

Use this router when the task is analytical, strategic, or diagnostic and more than one reasoning skill could fit.

Do not analyze the problem fully here. Select the narrowest correct reasoning skill, then hand off.

Each child lives under `using-reasoning/<child-name>/`, and each child SKILL.md should say it is a nested reasoning child.

## Core Contract

- Choose exactly one primary reasoning child or decide that no reasoning skill is needed.
- Prefer the earliest boundary violation: distorted state or vague problem → `reasoning` (Phase 0-1); concrete external signal → `strategic-foresight`; hidden-rule survivability → `reality-check`.
- For integrated workflow (calibrate → frame → analyze → recommend → verify), route to `reasoning` with the needed phases specified.
- Allow only explicit child routes listed below.
- If the request does not benefit from a reasoning skill, say so and answer directly.
- Use `references/children.json` as the source of truth for child boundaries, nested targets, install hints, and companion recommendations.

## Decision Tree

Apply these checks in order.

### 1. Does the situation need state calibration, problem framing, analysis, advice, or verification?
Route to `using-reasoning/reasoning` when any of these apply. Specify which phases to run:
- Needs state calibration (distorted reasoning, attachment, urgency) → `reasoning` Phase 0
- Problem still vague or solution-contaminated → `reasoning` Phase 1
- Problem is clear and needs rigorous analysis with lenses → `reasoning` Phase 2
- Needs structured recommendation or decision memo → `reasoning` Phase 3
- Post-decision verification or pattern extraction → `reasoning` Phase 4
- Multiple needs → `reasoning` with phases [0-1], [0-2-3], [1-2-3], etc.

### 2. Is there a concrete external signal with uncertainty about implications?
Route to `using-reasoning/strategic-foresight` when both are true:
- a concrete signal, threshold, launch, policy move, pricing shift, hardware curve, or scientific result is present
- the user wants implications, scenarios, winners/losers, second-order effects, or indicators to watch

### 3. Is the user really asking what they are not seeing?
Route to `using-reasoning/reality-check` when one or more of these are true:
- the user asks for a blunt reality check or asks what they are not seeing
- the main uncertainty is hidden rules, gatekeepers, information asymmetry, or selection filters
- downside survivability, resource mismatch, or platform ceiling matters more than optimization
- the honest answer depends on whether the current bet survives real-world incentives rather than on building a full advisory memo

Boundary checks:
- If this is really startup survival, GTM, CAC, churn, runway, pricing, or unit-economics work, do not use this router child; use `greenfield-product/startup-pressure-test`.
- If the user mainly needs sourced evidence, market mapping, or external research, do not use this child; use the appropriate research skill instead.

### 4. No reasoning skill
If none of the above fits cleanly, do not force a reasoning skill.

## Allowed Handoffs

All handoffs within `using-reasoning/reasoning` are internal — phases run sequentially within the same worker.
- `using-reasoning/reality-check -> using-reasoning/reasoning` (Phase 2 or Phase 3 after survivability check)
- `using-reasoning/strategic-foresight -> using-reasoning/reasoning` (Phase 4 for verification after scenario planning)
- `using-reasoning/reasoning -> using-reasoning/reality-check` (Phase 0 or 1 reveals hidden-rule concern)

## Forbidden Defaults

- Do not route to `using-reasoning/reasoning` Phase 2 (analyze) before Phase 1 (frame) when the problem is vague.
- Do not route to `using-reasoning/reasoning` Phase 3 (recommend) before Phase 2 (analyze) — recommendations without analysis are opinions.
- Do not route to `using-reasoning/reality-check` when the user mainly needs startup viability math, source-heavy research, or a clearer problem statement.
- Do not route to `using-reasoning/strategic-foresight` without a concrete external signal.
- Do not run multiple primary reasoning skills in parallel for the same request.

## References

- `references/children.json`

## Router Output

Return one of these forms and then invoke the selected skill if needed:

- `Route to using-reasoning/reasoning with phases: [0], [1], [2], [3], [4], or a combination like [0,1,2] or [2,3,4].`
- `Route to using-reasoning/strategic-foresight.`
- `Route to using-reasoning/reality-check.`
- `Install <child-path>, then route to <child-path>.`
- `No reasoning skill needed; answer directly.`

Add one sentence explaining why the selected route is the narrowest correct fit.

## Failure Modes to Avoid

- Jumping to analysis or recommendation when the problem is still vague
- Confusing Phase 0 (calibrate) with Phase 4 (verify) — calibrate is pre-analysis, verify is post-decision
- routing startup viability or GTM teardown requests into `using-reasoning/reality-check` because they sound harsh
- turning hidden-rule patterns into invented facts instead of labeling uncertainty honestly
- choosing `strategic-foresight` without a concrete external signal
- choosing `reality-check` when the user mainly needs a clear problem statement first
