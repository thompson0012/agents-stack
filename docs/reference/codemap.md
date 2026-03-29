# Code Map

Read when you need to find where to work. Prefer only high-value paths.

## Key Paths

- Path: `templates/base/.agents/skills/using-labs21-suite/`
- Purpose: top-level router, child inventory, and category-map surface for the shipped Labs21 template suite, including `using-design`, `using-reasoning`, and `delivery-control` while excluding deleted or moved external families.
- Update when: the shipped suite boundary, first-hop routing, or category descriptions change.

- Path: `templates/base/.agents/skills/using-design/`
- Purpose: design-family router for visual-system guidance, design-token generation, generative browser UI, and liquid-glass experimentation.
- Update when: the design family boundary, child list, or install hints change.

- Path: `templates/base/.agents/skills/using-reasoning/`
- Purpose: reasoning-family router for analytical, strategic, and diagnostic requests across calibration, framing, foresight, reality checks, advisory analysis, and multi-lens problem solving.
- Update when: the reasoning family boundary, child list, or handoff rules change.

- Path: `templates/base/.agents/skills/delivery-control/`
- Purpose: router family for non-trivial software delivery, including `harness-design` and `frontend-evaluator`.
- Update when: the family boundary, child list, or eval coverage changes.

- Path: `templates/base/docs/live/`
- Purpose: continuity surface for repo work; `runtime.md` tracks baton state and `qa.md` stores evaluator evidence and verdicts.
- Update when: the live-doc contract or required handoff artifacts change.

## Entrypoints

- Entrypoint: `templates/base/.agents/skills/using-labs21-suite/SKILL.md`
- Consumer: agents choosing the right shipped top-level Labs21 skill or family router before any narrower handoff.
- Notes: enter here when the right top-level entrypoint is unclear.

- Entrypoint: `templates/base/.agents/skills/using-labs21-suite/references/children.json`
- Consumer: router authors and reviewers checking the current top-level suite boundary.
- Notes: source of truth for which shipped families and direct leaves belong to the suite router.

- Entrypoint: `templates/base/.agents/skills/using-design/SKILL.md`
- Consumer: agents deciding whether a design request belongs in foundations, token generation, generative UI, or liquid-glass work.
- Notes: enter here when the hard problem is the design-family boundary itself.

- Entrypoint: `templates/base/.agents/skills/using-design/references/children.json`
- Consumer: router authors and reviewers checking durable design-family boundaries.
- Notes: source of truth for shipped design children and install hints.

- Entrypoint: `templates/base/.agents/skills/using-reasoning/SKILL.md`
- Consumer: agents deciding whether an analytical request needs calibration, framing, foresight, reality checks, advisory analysis, or multi-lens reasoning.
- Notes: enter here when the hard problem is reasoning-family selection rather than a specific known child.

- Entrypoint: `templates/base/.agents/skills/using-reasoning/references/children.json`
- Consumer: router authors and reviewers checking durable reasoning-family boundaries.
- Notes: source of truth for shipped reasoning children and install hints.

- Entrypoint: `templates/base/.agents/skills/delivery-control/SKILL.md`
- Consumer: agents deciding whether work needs discovery, harness control, review, evaluator signoff, implementation, or readiness reflection.
- Notes: enter here before direct leaf selection when non-trivial software delivery is ambiguous.

- Entrypoint: `templates/base/.agents/skills/delivery-control/references/children.json`
- Consumer: router authors and reviewers checking durable delivery-family boundaries.
- Notes: source of truth for `harness-design`, `frontend-evaluator`, and the remaining delivery-control targets.

- Entrypoint: `templates/base/docs/live/runtime.md`
- Consumer: planner, generator, evaluator, or same-role continuation across resets.
- Notes: only required when explicit delivery control is in play.

- Entrypoint: `templates/base/docs/live/qa.md`
- Consumer: independent evaluator or anyone auditing acceptance evidence.
- Notes: records the evidence matrix, defect list, verdict, and retry contract.

## High-Value Files

- File: `templates/base/.agents/skills/delivery-control/harness-design/SKILL.md`
- Why it matters: defines when to stay single-session, compact, or use planner/generator/evaluator control.
- Read after: `templates/base/.agents/skills/delivery-control/SKILL.md`

- File: `templates/base/.agents/skills/delivery-control/frontend-evaluator/SKILL.md`
- Why it matters: defines independent browser QA output, evidence standards, and pass/fail/blocked semantics.
- Read after: `templates/base/.agents/skills/delivery-control/SKILL.md`

- File: `templates/base/.agents/skills/using-design/references/children.json`
- Why it matters: quickest way to see which shipped design children the top-level suite can honestly hand off to.
- Read after: `templates/base/.agents/skills/using-design/SKILL.md`

- File: `templates/base/.agents/skills/using-reasoning/references/children.json`
- Why it matters: quickest way to see which shipped reasoning children the top-level suite can honestly hand off to.
- Read after: `templates/base/.agents/skills/using-reasoning/SKILL.md`

- File: `templates/base/docs/live/runtime.md`
- Why it matters: quickest place to recover baton ownership and execution mode during multi-session work.
- Read after: `docs/live/current-focus.md`

- File: `templates/base/docs/live/qa.md`
- Why it matters: quickest place to audit evaluator evidence and the final verdict when independent signoff exists.
- Read after: `templates/base/docs/live/runtime.md`
