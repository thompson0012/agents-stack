# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

`templates/base/.agents/skills/create-skill/` is now a stronger portable skill-authoring package: it still teaches LLM-agnostic skill design, and now also includes structured eval guidance, eval schemas/templates, a generic packager, and validator support for optional eval files and runtime-overlay metadata.

## Latest Completed Work

Extended `create-skill` with specialist capabilities extracted from `skill-creator` without importing its Claude-specific assumptions. Rewrote `SKILL.md` to add baseline-oriented evaluation and packaging phases, added `references/evaluation.md` plus `references/eval-schemas.md`, added starter eval/review assets, upgraded `scripts/scaffold.py` to create `evals/`, upgraded `scripts/validate.py` to parse optional nested metadata and validate `evals/*.json`, and added `scripts/package_skill.py` for generic ZIP packaging.

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Run a real prompt-pressure loop against `create-skill` using the new `evals/` structure, then decide whether the next extraction should be a separate specialist skill for benchmark aggregation or blind comparison rather than adding more weight to the canonical authoring skill.

## Touched Files

- `templates/base/.agents/skills/create-skill/SKILL.md`
- `templates/base/.agents/skills/create-skill/references/evaluation.md`
- `templates/base/.agents/skills/create-skill/references/eval-schemas.md`
- `templates/base/.agents/skills/create-skill/references/anti-patterns.md`
- `templates/base/.agents/skills/create-skill/assets/skill-template.md`
- `templates/base/.agents/skills/create-skill/assets/evals-template.json`
- `templates/base/.agents/skills/create-skill/assets/trigger-evals-template.json`
- `templates/base/.agents/skills/create-skill/assets/review-template.md`
- `templates/base/.agents/skills/create-skill/scripts/scaffold.py`
- `templates/base/.agents/skills/create-skill/scripts/validate.py`
- `templates/base/.agents/skills/create-skill/scripts/package_skill.py`
- `docs/live/current-focus.md`
- `docs/live/progress.md`
- `docs/live/todo.md`

## Verification Status

Read back the rewritten `SKILL.md`, validator, and packager. Ran and observed success for:

- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/create-skill --strict`
- a temporary scaffold + strict validate happy path using the upgraded `scripts/scaffold.py`
- a temporary negative case showing `validate.py` now rejects malformed `evals/evals.json` content
- a temporary positive case showing `validate.py` accepts optional overlay-style frontmatter and warns, rather than errors, on a non-portable extra field
- a temporary package flow showing `scripts/package_skill.py` creates a ZIP archive after validation
- a vendor-name grep over `templates/base/.agents/skills/create-skill/` showing no vendor-branded core guidance remains

## Hand-off Note

`create-skill` is now the canonical portable authoring skill plus a light specialist layer for eval design and packaging. The next design decision should be about boundaries: benchmark aggregation and richer blind-comparison tooling likely belong in a separate optional specialist skill, not in the canonical portable core.