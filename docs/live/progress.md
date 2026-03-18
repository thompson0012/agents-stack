# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

`create-skill` remains the portable leaf-skill authoring package, and `templates/base/.agents/skills/create-router-skill/` now exists as the separate specialist package for discoverable family routers with explicit child metadata and install/fallback rules.

## Latest Completed Work

Created `create-router-skill/` as a dedicated package with a router-focused `SKILL.md`, `references/router-metadata.md`, `references/relationship-types.md`, starter assets for router bodies and child inventories, eval prompts, and `scripts/validate_router.py` for deterministic router-package validation. Updated `create-skill/SKILL.md` plus `references/anti-patterns.md` so router-entrypoint work now routes to `create-router-skill` instead of being forced into leaf-skill guidance.

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Run a real prompt-pressure loop against `create-router-skill`, then pilot the metadata model on one actual family router before deciding whether the suite should adopt nested family packages or stay flat with router indexes only.

## Touched Files

- `templates/base/.agents/skills/create-router-skill/SKILL.md`
- `templates/base/.agents/skills/create-router-skill/references/router-metadata.md`
- `templates/base/.agents/skills/create-router-skill/references/relationship-types.md`
- `templates/base/.agents/skills/create-router-skill/assets/router-skill-template.md`
- `templates/base/.agents/skills/create-router-skill/assets/children-template.json`
- `templates/base/.agents/skills/create-router-skill/evals/evals.json`
- `templates/base/.agents/skills/create-router-skill/evals/trigger-evals.json`
- `templates/base/.agents/skills/create-router-skill/scripts/validate_router.py`
- `templates/base/.agents/skills/create-skill/SKILL.md`
- `templates/base/.agents/skills/create-skill/references/anti-patterns.md`
- `docs/live/current-focus.md`
- `docs/live/progress.md`
- `docs/live/todo.md`

## Verification Status

Read back the new router package and updated `create-skill` guidance. Ran and observed success for:

- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/create-router-skill --strict`
- `python3 templates/base/.agents/skills/create-router-skill/scripts/validate_router.py tmp/router-skill-check --strict` against a valid temporary router fixture
- `python3 templates/base/.agents/skills/create-router-skill/scripts/validate_router.py tmp/router-skill-check-invalid --strict` failing on an unknown fallback target
- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/create-skill --strict` after integrating the new router boundary
- `python3 -m py_compile templates/base/.agents/skills/create-router-skill/scripts/validate_router.py`
- reviewer re-check on `create-router-skill` confirming the previous validator issues were resolved and no material issues remain

## Hand-off Note

The suite now has an explicit split: use `create-skill` for leaf execution packages and `create-router-skill` when the package's primary job is selection, handoff, and child metadata. The next decision should be exercised on a real router family before committing to a broader filesystem reorganization.