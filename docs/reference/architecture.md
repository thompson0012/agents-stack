# Architecture Reference

Read when system shape, boundaries, or invariants matter. Keep this focused on stable structure.

## System Boundaries

- Inside scope: portable skill routing, including the `using-design`, `using-reasoning`, and `delivery-control` families, plus template live/reference docs that carry delivery state across sessions.
- Outside scope: product-specific implementations, runtime-specific harness code, and mandatory evaluator overhead for trivial one-shot tasks.
- Boundary note: `using-design` owns design-family selection when the design boundary itself is the hard problem, while ordinary hand-authored web implementation stays outside this template suite.
- Boundary note: `using-reasoning` owns reasoning-family selection for analytical requests, while `startup-pressure-test` stays separate for harsh commercial survivability work.
- Boundary note: `delivery-control` owns delivery-control routing and independent frontend acceptance selection for non-trivial software feature work.
- Boundary note: repo-local guidance for maintaining this repository's `AGENTS.md` hierarchy belongs in `.agents/skills/using-agents-md/`, while `AGENTS.md` files remain the canonical boundary rules and `docs/reference/*`/`docs/live/*` keep durable truth and session state.


## Invariants

- Invariant: `delivery-control/harness-design` is only for cross-session control, compaction rules, baton passing, and planner/generator/evaluator structure.
- Why it must hold: routing ordinary single-session execution into harness design would duplicate the base router and blur ownership.
- Failure signal: routine build or plan-review work is described as harness design without any explicit session-control problem.

- Invariant: independent browser signoff belongs to `delivery-control/frontend-evaluator`, and the template suite must not imply a separate shipped builder-QA family unless that family actually exists in `templates/base/.agents/skills/`.
- Why it must hold: deleted or external web-builder families cannot remain as ghost defaults without lying about what the template currently ships.
- Failure signal: `website-building` or another removed family is still described as an active shipped QA surface inside the template docs or router metadata.

- Invariant: `templates/base/docs/live/runtime.md` and `templates/base/docs/live/qa.md` are the canonical live docs when explicit delivery control or evaluator evidence exists.
- Why it must hold: baton state and acceptance evidence must survive session resets and role changes in one predictable place.
- Failure signal: runtime mode, baton owner, evidence, or verdict only live in chat transcripts or ad hoc files.

- Invariant: `using-labs21-suite` may claim only the currently shipped top-level families and direct leaves; deleted or moved families must disappear from the router in the same change.
- Why it must hold: a top-level suite router that advertises deleted or external families lies about what the template actually ships and produces bad first-hop routing.
- Failure signal: the category map, child inventory, or evals still mention removed families such as `project-founding`, or omit newly shipped families such as `using-design` or `using-reasoning`.

## Major Components

- Component: `.agents/skills/using-agents-md/`
- Responsibility: guides repo-local decisions about when changes belong in `AGENTS.md`, `docs/reference/*`, `docs/live/*`, or a skill package, and insists that discovery pointers move with AGENTS-boundary changes.
- Key dependency: root `AGENTS.md` plus the live/reference writeback surfaces it triages.

- Component: `templates/base/.agents/skills/delivery-control/`
- Responsibility: routes non-trivial software work across discovery, harness control, plan review, implementation handoff, independent frontend evaluation, and readiness reflection.
- Key dependency: `references/children.json` plus the nested `harness-design/` and `frontend-evaluator/` leaves.

- Component: `templates/base/.agents/skills/using-labs21-suite/`
- Responsibility: top-level discoverability router for the shipped Labs21 template suite; it routes only across the owned top-level skills and refuses to claim moved external families as part of the suite.
- Key dependency: `references/children.json` plus `references/category-map.md` for the current top-level suite inventory.

- Component: `templates/base/.agents/skills/labs21-product-suite/`
- Responsibility: stage-gated product-development router for raw ideas, validated blueprints, PRDs, and v1 architecture; it hands off to exactly one child skill and continues from that child's workflow.
- Key dependency: `references/children.json`, `references/router-metadata.md`, `references/relationship-types.md`, `assets/router-skill-template.md`, `assets/children-template.json`, and the nested `labs21-chief-architect`, `labs21-prd-writer`, and `labs21-system-architect` leaves.

- Component: `templates/base/.agents/skills/using-design/`
- Responsibility: routes design-family requests across design foundations, design-token generation, generative UI, and liquid-glass experimentation.
- Key dependency: `references/children.json` plus the shipped design child packages.

- Component: `templates/base/.agents/skills/using-reasoning/`
- Responsibility: routes analytical, strategic, and diagnostic requests across state calibration, problem framing, foresight, reality checks, advisory analysis, and multi-lens problem solving.
- Key dependency: `references/children.json` plus the shipped reasoning child packages.

- Component: `templates/base/docs/live/{current-focus.md,progress.md,todo.md,runtime.md,qa.md}`
- Responsibility: carries recovery state across normal continuation, explicit baton passes, and evaluator evidence collection.
- Key dependency: truthful updates from the active role before handoff.