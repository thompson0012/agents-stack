# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

The next work item is harness goal-lineage hardening: keep template live docs inert, add a roadmap artifact that preserves source/plan/phase goals, and make phased execution rehydrate from stored truth after compaction instead of drifting from the original objective.

## Latest Completed Work

- captured the user requirement that `template/` must be a true template with no prefilled content
- identified the recurring failure mode where roadmap execution loses the source goal after phase 1 and compaction
- drafted `docs/superpowers/plans/2026-03-27-harness-goal-lineage-hardening.md` to harden template inertness, goal lineage, and resume behavior
- refreshed `using-labs21-suite` so the shipped top-level router now includes `using-design` and `using-reasoning`, and removes deleted `project-founding` claims from its child inventory, category map, and evals
- updated active reference docs so the template suite boundary matches the actual shipped skill tree instead of stale family history

## In Progress

Harness goal-lineage hardening plan drafted; implementation pending.
- goal-lineage hardening remains the main pending implementation track; the top-level suite router now matches the shipped `using-design`, `using-reasoning`, and `delivery-control` families

## Blockers

None recorded.

## Next Recommended Action

Review and execute `docs/superpowers/plans/2026-03-27-harness-goal-lineage-hardening.md`.

## Touched Files

- `docs/superpowers/plans/2026-03-27-harness-goal-lineage-hardening.md`
- `docs/live/current-focus.md`
- `docs/live/progress.md`
- `templates/base/.agents/skills/{using-labs21-suite,using-design,using-reasoning}/`
- `docs/live/progress.md`
- `docs/reference/{architecture.md,codemap.md,memory.md}`

## Verification Status

- `python3 templates/base/.agents/skills/create-router-skill/scripts/validate_router.py templates/base/.agents/skills/using-labs21-suite --strict`
- `python3 templates/base/.agents/skills/using-design/scripts/validate_router.py templates/base/.agents/skills/using-design --strict`
- `python3 templates/base/.agents/skills/using-reasoning/scripts/validate_router.py templates/base/.agents/skills/using-reasoning --strict`

## Hand-off Note

The next session should implement the harness goal-lineage hardening plan and keep the roadmap as the authoritative source for phased work. The shipped `using-labs21-suite` boundary now reflects `using-design`, `using-reasoning`, and `delivery-control`; deleted `project-founding` should not be reintroduced unless that family is deliberately restored.
