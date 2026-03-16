# Current Focus

Read after `AGENTS.md` when starting or resuming work. Keep this file limited to the current objective and the bounds for active work.

## Objective

Create a packaged three-skill reasoning system from the supplied PDF discussion and final conclusion: `problem-definition` for unclear problems, `dynamic-problem-solving` for clearly defined complicated problems, and `thinking-ground` for pre-analysis state calibration.

## Scope

- Add `templates/base/.agents/skills/problem-definition/SKILL.md`.
- Add `templates/base/.agents/skills/dynamic-problem-solving/SKILL.md` plus the minimal supporting references and quick-invoke asset the workflow needs.
- Add `templates/base/.agents/skills/thinking-ground/SKILL.md` plus a compact whole-system pocket card.
- Remove generated placeholder resource files from all three initialized skill directories.
- Package each completed skill into `dist/`.

## Constraints

- Keep skill frontmatter limited to `name` and `description`.
- Keep the skill bodies in English and optimize for reusable agent workflows, not raw transcript copy.
- `dynamic-problem-solving` must only apply to clearly defined, complicated problems and must route vague problems to `problem-definition`.
- `thinking-ground` must rely on observable signals and explicit limits, not unverifiable claims about inner state or consciousness.
- Do not commit from this task.

## Success Criteria

- The three skill directories exist under `templates/base/.agents/skills/` with coherent English workflows.
- Unneeded generated placeholder files are removed from all three skills.
- `templates/base/.agents/skills/skill-creator/scripts/package_skill.py` validates each skill and produces `dist/problem-definition.skill`, `dist/dynamic-problem-solving.skill`, and `dist/thinking-ground.skill`.
- The live docs record the completed work and verification state.
