# Current Focus

Read after `AGENTS.md` when starting or resuming work. Keep this file limited to the current objective and the bounds for active work.

## Objective

Extend `templates/base/.agents/skills/create-skill/` with the best specialist capabilities from `skill-creator` while keeping the package portable, LLM-agnostic, and aligned with first-party suite conventions.

## Scope

- Keep the work inside `templates/base/.agents/skills/create-skill/` plus the live docs updated for continuity.
- Retain the flat skill namespace and keep the existing `create-skill` identity.
- Add portable versions of structured eval support, packaging guidance, and supporting assets/scripts without reintroducing vendor lock-in.

## Constraints

- Do not encode Anthropic-, OpenAI-, or other vendor-specific runtime rules as the canonical core workflow.
- Keep the portable core aligned with suite conventions: `name` and `description` frontmatter by default.
- Runtime overlays may exist, but the validator and package shape must remain useful without one specific platform.
- Do not commit from this task.

## Success Criteria

- `create-skill/SKILL.md` teaches portable skill creation, structured evaluation, and packaging.
- Bundled references cover patterns, evaluation, schemas, portability, security, and anti-patterns.
- `scripts/scaffold.py`, `scripts/validate.py`, and `scripts/package_skill.py` succeed on positive cases and reject malformed input.
- Extracted specialist features improve the package without reintroducing vendor-specific core guidance.