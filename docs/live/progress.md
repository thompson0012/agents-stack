# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

`templates/base/.agents/skills/create-skill/` is now a portable skill-authoring package instead of a thin wrapper around vendor-specific guidance. The package has a rewritten `SKILL.md`, a focused references set, starter templates, and local scaffold/validate scripts.

## Latest Completed Work

Rewrote `templates/base/.agents/skills/create-skill/SKILL.md` around LLM-agnostic skill design, moved the stale `reference/src.md` content into a proper `references/` set, added `scripts/scaffold.py` and `scripts/validate.py`, and added `assets/skill-template.md` plus `assets/eval-template.md`. Removed the empty legacy `reference/` directory.

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Run a real ambiguous-prompt eval loop against `create-skill` itself, then use it on one existing first-party skill to see whether the new portability and evaluation guidance produces cleaner packages in practice.

## Touched Files

- `templates/base/.agents/skills/create-skill/SKILL.md`
- `templates/base/.agents/skills/create-skill/scripts/scaffold.py`
- `templates/base/.agents/skills/create-skill/scripts/validate.py`
- `templates/base/.agents/skills/create-skill/references/patterns.md`
- `templates/base/.agents/skills/create-skill/references/portability.md`
- `templates/base/.agents/skills/create-skill/references/security.md`
- `templates/base/.agents/skills/create-skill/references/anti-patterns.md`
- `templates/base/.agents/skills/create-skill/assets/skill-template.md`
- `templates/base/.agents/skills/create-skill/assets/eval-template.md`
- `docs/live/current-focus.md`
- `docs/live/progress.md`
- `docs/live/todo.md`

## Verification Status

Read back the rewritten `SKILL.md` plus both new Python scripts. Ran and observed success for:

- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/create-skill --strict`
- a temporary happy-path scaffold + validate flow using `scripts/scaffold.py` followed by `scripts/validate.py --strict`
- a temporary negative validation case showing `validate.py` rejects an extra frontmatter field and a description that does not start with `Use when`

## Hand-off Note

The package now teaches a conservative portable core first, with runtime overlays separated into a portability reference. The next leverage point is not more structure; it is prompt-pressure evaluation to confirm the new trigger wording and checklists actually guide another agent under ambiguity.