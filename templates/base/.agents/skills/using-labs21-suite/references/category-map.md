# Labs21 Suite Category Map

This template's shipped Labs21 suite under `.agents/skills/` currently contains only these top-level skills and family routers.

## Suite Router

- `using-labs21-suite` — top-level discoverability router for the shipped Labs21 template skill surface when the right top-level entrypoint is not obvious yet

## Orchestration and Reflection

- `context-compaction` — compact session state for handoff or continuation
- `self-cognitive` — run confidence checks, retrospectives, and repeatable-workflow extraction

## Prompt Work

- `meta-prompting` — design or evaluate a prompt artifact such as a system prompt, prompt template, prompt architecture, rubric, or eval plan
- `prompt-augmentation` — enrich a sparse prompt or generate prompt variants for text, image, or video generation while preserving the user's core subject

## Skill Package Authoring

- `create-skill` — create or upgrade a reusable leaf skill package, scaffold a portable skill directory, or rewrite skill guidance into a reusable package
- `create-router-skill` — create or upgrade a discoverable router skill whose main job is selecting among child skills, carrying explicit child metadata, and handling install-or-fallback behavior honestly

Use `create-skill` when the package's job is one repeatable workflow. Use `create-router-skill` only when the package's job is family routing.

## Design Workflow Routing

Route through `using-design` when the request is about design-family selection and the right design lane is not obvious yet.

- `using-design/design-foundations` — choose colors, typography, spacing, chart styling, and general visual-system defaults when no project-specific system already governs the work
- `using-design/generating-design-tokens` — turn brand inputs into a design token spec or brand system
- `using-design/generative-ui` — build or evaluate model-generated browser UI with sandboxed HTML, typed component schemas, or streamed UI
- `using-design/liquid-glass-design` — implement or evaluate experimental liquid-glass UI effects in the browser

## Software Delivery Routing

Route through `delivery-control` when the request is non-trivial software feature work and the user needs help choosing the next delivery stage.

- `delivery-control/feature-discovery` — turn a fuzzy feature idea or change request into a clear problem statement and next-step recommendation
- `delivery-control/harness-design` — choose the honest delivery-control mode across single-session work, compacted continuation, or planner/generator/evaluator execution with explicit handoffs
- `delivery-control/plan-product-review` — challenge a plan on user value, scope, sequencing, and MVP shape before implementation
- `delivery-control/plan-engineering-review` — challenge a plan on architecture, failure modes, rollback, tests, and observability before implementation
- `delivery-control/plan-design-review` — challenge a plan on UX flows, states, accessibility, and interface clarity before implementation
- `delivery-control/frontend-evaluator` — provide strict independent browser-facing acceptance with evidence, defects, and retry guidance after implementation exists

## Commercial Reality Testing

- `startup-pressure-test` — pressure-test a startup, launch thesis, or business model with realistic acquisition, retention, monetization, burn, and runway pressure

## Reasoning Workflow Routing

Route through `using-reasoning` when the task is analytical and the right reasoning lane is not obvious yet.

- `using-reasoning/thinking-ground` — calibrate reasoning state before analysis
- `using-reasoning/problem-definition` — turn a messy situation into one clean problem statement
- `using-reasoning/strategic-foresight` — run scenarios around a concrete external signal or threshold
- `using-reasoning/reality-check` — surface hidden rules, survivability traps, resource mismatch, or platform ceilings
- `using-reasoning/domain-expert-consultation` — produce a structured advisory memo or expert recommendation
- `using-reasoning/dynamic-problem-solving` — analyze a clearly defined complicated problem through multiple lenses

## Outside the Shipped Labs21 Suite

The template no longer ships older router targets such as `project-founding`, `website-building`, `using-documents`, `using-legal`, `using-sales`, `using-marketing`, `using-research`, `using-finance`, `media`, `coding-and-data`, `data-exploration`, `visualization`, or `cx-ticket-triage`.

Do not route to those from `using-labs21-suite`. If the user needs one of those moved or external workflows, say that no Labs21 suite skill fits and continue with the appropriate non-suite workflow instead of pretending the template still owns that path.
