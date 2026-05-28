---
name: using-reasoning
description: Use when a request is analytical and could plausibly benefit from integrated reasoning, reality-check, or scenario-planning templates.
---

# Using Reasoning

Use this router when the task is analytical, strategic, or diagnostic and more than one reasoning skill could fit.

Do not analyze the problem fully here. Select the narrowest correct reasoning skill, then hand off.

Each child lives under `using-reasoning/<child-name>/`, and each child SKILL.md should say it is a nested reasoning child.

## Core Contract

- Choose exactly one primary reasoning child or decide that no reasoning skill is needed.
- Prefer the earliest boundary violation: distorted state or vague problem → `reasoning` (Phase 0-1); clear reality-check or scenario-planning pattern → `reasoning` with quick-start template.
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

### 2. Does the situation need a quick-start template?
When the request is a clear reality check or scenario planning need, route to `using-reasoning/reasoning` and apply the appropriate quick-start template:
- Survivability audit / hidden-rule check → use the **Reality Check** template from `reasoning/references/archetypes.md`
- External signal or scenario planning → use the **Strategic Foresight** template from `reasoning/references/scenarios.md`

Boundary checks:
- If this is really startup survival, GTM, CAC, churn, runway, pricing, or unit-economics work, do not use this router child; use `greenfield-product/startup-pressure-test`.
- If the user mainly needs sourced evidence, market mapping, or external research, do not use this child; use the appropriate research skill instead.

### 3. No reasoning skill
If none of the above fits cleanly, do not force a reasoning skill.

## Allowed Handoffs

All handoffs within `using-reasoning/reasoning` are internal — phases run sequentially within the same worker.
The reality-check and scenario-planning quick-start templates are reference files within reasoning, not separate children.

## Forbidden Defaults

- Do not route to `using-reasoning/reasoning` Phase 2 (analyze) before Phase 1 (frame) when the problem is vague.
- Do not route to `using-reasoning/reasoning` Phase 3 (recommend) before Phase 2 (analyze) — recommendations without analysis are opinions.
- Do not run multiple primary reasoning skills in parallel for the same request.

## References

- `references/children.json`

## Router Output

Return one of these forms and then invoke the selected skill if needed:

- `Route to using-reasoning/reasoning with phases: [0], [1], [2], [3], [4], or a combination like [0,1,2] or [2,3,4].`
- `Route to using-reasoning/reasoning with the Reality Check quick-start template (references/archetypes.md).`
- `Route to using-reasoning/reasoning with the Strategic Foresight quick-start template (references/scenarios.md).`
- `Install using-reasoning/reasoning, then route to using-reasoning/reasoning.`
- `No reasoning skill needed; answer directly.`

Add one sentence explaining why the selected route is the narrowest correct fit.

## Failure Modes to Avoid

- Jumping to analysis or recommendation when the problem is still vague
- Confusing Phase 0 (calibrate) with Phase 4 (verify) — calibrate is pre-analysis, verify is post-decision
- Routing startup viability or GTM teardown requests into `using-reasoning/reasoning` because they sound analytical
- Turning hidden-rule patterns into invented facts instead of labeling uncertainty honestly
- Using scenario planning without a concrete external signal
- Skipping problem framing when the user mainly needs a clear problem statement first
