# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

Task 36 is now complete. In addition to the earlier portable methodology tightening, the repo now has a staged first-use path that lowers time-to-first-value without inventing a dishonest umbrella skill: `README.md` gives evaluators a short 'First useful run' sequence, and `templates/base/.agents/skills/using-agent-practices/SKILL.md` now mirrors that path as a router-level quick start. The next likely step is still to resume the targeted methodology refinement pass across the finance, research, and webapp docs that were already flagged as promising follow-up work.

## Latest Completed Work

Added a staged onboarding path in `README.md` and `templates/base/.agents/skills/using-agent-practices/{SKILL.md,references/category-map.md}` so users can match their situation to an existing skill quickly, stop after the first useful stage, and avoid a monolithic 'do everything' skill. The router and category map now both cover spec work via `feature-spec` and repo-backed coding/data work via `coding-and-data`, keeping the quick path honest and aligned with the installed skill inventory.

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Resume the methodology refinement pass in the finance, research, and website-building/webapp docs that were already identified as likely follow-up targets, and only add onboarding or quick-path language where the installed skill inventory already supports it honestly.

## Touched Files

- `README.md`
- `scripts/audit_base_template_skills.py`
- `scripts/tests/test_audit_base_template_skills.py`
- `scripts/tests/test_vendor_agnostic_naming.py`
- `.github/workflows/base-template-skill-audit.yml`
- `templates/base/.agents/skills/{coding-and-data,design-foundations,feature-spec,generating-design-tokens,media,meta-prompting,self-cognitive,startup-pressure-test,visualization}/SKILL.md`
- `templates/base/.agents/skills/create-router-skill/{SKILL.md,references/router-metadata.md}`
- `templates/base/.agents/skills/startup-pressure-test/evals/{evals.json,trigger-evals.json}`
- `templates/base/.agents/skills/using-agent-practices/{SKILL.md,evals/**,references/category-map.md}`
- `templates/base/.agents/skills/using-{documents,finance,research,reasoning,legal,marketing,sales}/**`
- `templates/base/.agents/skills/website-building/{SKILL.md,game/**,informational/**,shared/**,webapp/**}`
- `templates/base/AGENTS.md`
- `docs/live/current-focus.md`
- `docs/live/progress.md`
- `docs/live/todo.md`
- deleted stray `.DS_Store` artifacts under the repo root and `templates/` hierarchy

## Verification Status

Observed success for:

- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/using-agent-practices --strict`
- `git diff --check` returned no output
- readback review confirmed the new staged 'First useful run' section in `README.md`, the matching router-level quick path in `templates/base/.agents/skills/using-agent-practices/SKILL.md`, and the corresponding `feature-spec` / `coding-and-data` entries in `references/category-map.md`

## Hand-off Note

The repo now has one honest onboarding surface for 'where do I start?' without collapsing multiple lifecycle jobs into one skill: the public README gives a short staged first-use path, and `using-agent-practices` mirrors that path as a router-level quick start while still routing to narrow leaf or family skills.