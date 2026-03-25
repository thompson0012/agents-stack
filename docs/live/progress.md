# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

Task 39 remains complete, and the base template's design family now uses an honest nested router layout: `using-design` owns the family entrypoint and the four design leaves now live under that router as bundled child packages. `using-agent-practices` and cross-skill references now point at `using-design/<leaf>` paths, while normal site/app/game builds still stay with `website-building`. No unresolved validation blocker is currently recorded, so the default next move still returns to Task 35 once this router move is noted.

## Latest Completed Work

Completed the bundled design-family cutover:
- moved `design-foundations`, `generating-design-tokens`, `generative-ui`, and `liquid-glass-design` into `templates/base/.agents/skills/using-design/` as nested leaf skills
- updated `templates/base/.agents/skills/using-design/{SKILL.md,references/children.json,evals/*}` and `templates/base/.agents/skills/using-agent-practices/{SKILL.md,references/category-map.md,evals/*}` so direct and ambiguous routes use `using-design/<leaf>` consistently
- updated dependent references in document, visualization, website-building, and plan-review skills so no stale top-level design-leaf paths remain
- confirmed the existing router-validator duplication remains shared-by-copy across router packages; left abstraction unchanged to avoid repo-wide churn outside this requested stack addition
- recorded the follow-on lesson in `docs/reference/{lessons.md,memory.md}`: when a bundled router family is warranted, default to moving bundled leaves under the router in the same change rather than staging an external-child interim

## In Progress

None.

## Blockers

None recorded.

## Next Recommended Action

Resume Task 35: refine the capability-based methodology overlays in the finance, research, and webapp docs. Treat the nested `using-design/<leaf>` layout as landed unless a concrete validator failure or routing regression appears.

## Touched Files

- `templates/base/.agents/skills/using-design/`
- `templates/base/.agents/skills/using-agent-practices/`
- `templates/base/.agents/skills/using-documents/`
- `templates/base/.agents/skills/software-delivery/plan-design-review/`
- `templates/base/.agents/skills/visualization/`
- `templates/base/.agents/skills/website-building/`
- `templates/base/AGENTS.md`
- `templates/base/docs/live/{runtime.md,qa.md}`
- `templates/base/docs/reference/{architecture.md,codemap.md}`

## Verification Status

Validated `templates/base/.agents/skills/using-design/` with `python3 templates/base/.agents/skills/using-design/scripts/validate_router.py --strict templates/base/.agents/skills/using-design`, JSON-parsed the updated router/eval metadata, and grep-checked that stale top-level design-leaf route/path references were removed from the edited skill surfaces.

## Hand-off Note

`using-design` is now both the family router and the physical package boundary for the bundled design leaves: `using-design/design-foundations`, `using-design/generating-design-tokens`, `using-design/generative-ui`, and `using-design/liquid-glass-design`. Keep direct leaf routing on those nested identifiers, and keep normal site/app/game builds under `website-building`. Unless a concrete regression appears, resume from Task 35.