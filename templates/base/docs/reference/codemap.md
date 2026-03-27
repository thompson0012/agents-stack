# Code Map

Read when you need to find where to work. Prefer only high-value paths.

## Key Paths

- Path: `templates/base/docs/live/`
- Purpose: live handoff surface for current objective, runtime control, continuity, QA evidence, and task selection.
- Update when: a live-doc path, handoff contract, or evaluation artifact changes.

- Path: `templates/base/docs/live/roadmap.md`
- Purpose: persistent source-goal / plan-goal / phase-goal ledger for roadmap-driven work.
- Update when: a plan is created, a phase changes, or the user explicitly changes direction.

- Path: `templates/base/docs/reference/`
- Purpose: stable reference docs for architecture, codemap, implementation, design, memory, and lessons.
- Update when: boundaries, high-value paths, or stable repo guidance changes.

- Path: `templates/base/.agents/skills/software-delivery/`
- Purpose: router family for feature discovery, harness control, plan reviews, and independent frontend evaluation.
- Update when: a software-delivery leaf is added, removed, renamed, or materially repurposed.

- Path: `templates/base/.agents/skills/using-reasoning/`
- Purpose: router family for analytical requests across state calibration, problem framing, strategic foresight, hidden-rule reality checks, structured advisory, and multi-lens analysis.
- Update when: a reasoning leaf is added, removed, renamed, or materially repurposed.

- Path: `templates/base/.agents/skills/using-agent-practices/references/category-map.md`
- Purpose: top-level discoverability for first-party skill families and standalone specialist skills.
- Update when: category routing or skill inventory changes.

## Entrypoints

- Entrypoint: `templates/base/AGENTS.md`
- Consumer: any agent starting or resuming work in the template
- Notes: root read order; points into the live docs and reference docs.

- Entrypoint: `templates/base/.agents/skills/using-agent-practices/SKILL.md`
- Consumer: agents choosing the narrowest first-party skill when the right route is not obvious yet
- Notes: top-level router across standalone specialist skills and family routers; keeps the category-map inventory honest.


- Entrypoint: `templates/base/.agents/skills/software-delivery/SKILL.md`
- Consumer: agents choosing the right software-delivery lane
- Notes: routes to `feature-discovery`, `harness-design`, `plan-product-review`, `plan-engineering-review`, `plan-design-review`, or `frontend-evaluator`.

- Entrypoint: `templates/base/.agents/skills/using-reasoning/SKILL.md`
- Consumer: agents choosing the right reasoning lane for analytical, strategic, or diagnostic requests
- Notes: routes to `thinking-ground`, `problem-definition`, `strategic-foresight`, `reality-check`, `domain-expert-consultation`, or `dynamic-problem-solving`.


- Entrypoint: `templates/base/docs/live/runtime.md`
- Consumer: planner, generator, or evaluator working under explicit delivery control
- Notes: records the active mode and baton rules; skip for trivial work that stays in one obvious session.

- Entrypoint: `templates/base/docs/live/qa.md`
- Consumer: independent evaluator or any role auditing acceptance evidence
- Notes: canonical markdown artifact for evaluator evidence, verdict, and retry contract when independent acceptance exists.

## High-Value Files

- File: `templates/base/docs/live/current-focus.md`
- Why it matters: defines the active boundary and next-owner instruction.
- Read after: `templates/base/AGENTS.md`

- File: `templates/base/docs/live/roadmap.md`
- Why it matters: preserves goal lineage so phased work can survive compaction and resume honestly.
- Read after: `templates/base/docs/live/current-focus.md`

- File: `templates/base/docs/live/todo.md`
- Why it matters: records the queued work so the active baton owner and next owner can see what remains and what is already done.
- Read after: `templates/base/docs/live/current-focus.md`

- File: `templates/base/docs/live/runtime.md`
- Why it matters: tells whether the work is `single-session`, `compacted-continuation`, or `planner-generator-evaluator`, and who owns the baton now.
- Read after: `templates/base/docs/live/current-focus.md`

- File: `templates/base/docs/live/progress.md`
- Why it matters: preserves continuity, touched files, blockers, and verification truth.
- Read after: `templates/base/docs/live/current-focus.md`

- File: `templates/base/docs/live/qa.md`
- Why it matters: carries audit-friendly QA evidence plus `pass`, `fail`, or `blocked` when independent evaluation exists.
- Read after: `templates/base/docs/live/runtime.md`

- File: `templates/base/.agents/skills/using-reasoning/reality-check/SKILL.md`
- Why it matters: defines the hidden-rule and survivability boundary for blunt “what am I missing?” requests.
- Read after: `templates/base/.agents/skills/using-reasoning/SKILL.md`


- File: `templates/base/.agents/skills/software-delivery/feature-discovery/SKILL.md`
- Why it matters: starts the delivery family when the feature or change request is still fuzzy.
- Read after: `templates/base/.agents/skills/software-delivery/SKILL.md`

- File: `templates/base/.agents/skills/software-delivery/harness-design/SKILL.md`
- Why it matters: defines mode selection, baton rules, and the live-doc artifact contract.
- Read after: `templates/base/.agents/skills/software-delivery/SKILL.md`

- File: `templates/base/.agents/skills/software-delivery/plan-product-review/SKILL.md`
- Why it matters: reviews value, scope, sequencing, and MVP cuts before build.
- Read after: `templates/base/.agents/skills/software-delivery/SKILL.md`

- File: `templates/base/.agents/skills/software-delivery/plan-engineering-review/SKILL.md`
- Why it matters: reviews architecture, failure modes, tests, and rollout risk before build.
- Read after: `templates/base/.agents/skills/software-delivery/SKILL.md`

- File: `templates/base/.agents/skills/software-delivery/plan-design-review/SKILL.md`
- Why it matters: reviews UX flows, states, accessibility, and interface clarity before build.
- Read after: `templates/base/.agents/skills/software-delivery/SKILL.md`

- File: `templates/base/.agents/skills/software-delivery/frontend-evaluator/SKILL.md`
- Why it matters: defines evidence, verdict, defect, and retry expectations for browser-facing signoff.
- Read after: `templates/base/.agents/skills/software-delivery/SKILL.md`
