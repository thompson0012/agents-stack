# Current Focus

Read after `AGENTS.md` when starting or resuming work. Keep this file limited to the current objective and the bounds for active work.

## Objective

Modernize `templates/base/.agents/skills/create-skill/` into a first-party skill-authoring package that teaches portable, LLM-agnostic skill creation instead of vendor-locked instructions.

## Scope

- Keep the work inside `templates/base/.agents/skills/create-skill/` plus the live docs updated for continuity.
- Retain the flat skill namespace and keep the existing `create-skill` identity.
- Provide a universal `SKILL.md`, bundled references, starter templates, and focused local scripts for scaffolding and validation.

## Constraints

- Do not encode Anthropic-, OpenAI-, or other vendor-specific runtime rules as the canonical core workflow.
- Keep the portable core aligned with suite conventions: `name` and `description` frontmatter by default.
- Use runtime-specific notes only as optional overlays, not the core design.
- Do not commit from this task.

## Success Criteria

- `create-skill/SKILL.md` teaches portable skill creation, validation, and evaluation.
- Bundled references cover patterns, portability, security, and anti-patterns.
- `scripts/scaffold.py` and `scripts/validate.py` succeed on positive cases and reject malformed input.
- Legacy vendor-specific guidance is removed from the active package.