# Current Focus

Read after `AGENTS.md` when starting or resuming work. Keep this file limited to the current objective and the bounds for active work.

## Objective

Extract a separate `create-router-skill` package from the skill-authoring work so discoverable family routers can be built without overloading `create-skill` or breaking portable leaf-skill conventions.

## Scope

- Keep the work inside `templates/base/.agents/skills/create-router-skill/`, the touched `create-skill/` guidance, and the live docs updated for continuity.
- Preserve the portable core approach: router packages should remain useful without one runtime's loader or install model.
- Clarify the boundary between leaf skill creation and router/family-entrypoint creation.

## Constraints

- Do not encode Anthropic-, OpenAI-, or other vendor-specific runtime rules as the canonical router workflow.
- Keep the portable core aligned with suite conventions: `name` and `description` frontmatter by default, explicit metadata in bundled files only when justified.
- Router packages must keep selection, install, and fallback behavior truthful rather than relying on folder layout alone.
- Do not commit from this task.

## Success Criteria

- `create-router-skill/SKILL.md` teaches when and how to build a discoverable family router.
- Bundled references and assets define a reusable child-metadata model and typed relationship vocabulary.
- `scripts/validate_router.py` succeeds on a valid router package and rejects malformed router metadata.
- `create-skill` clearly redirects router-entrypoint work to `create-router-skill` instead of overloading leaf-skill guidance.