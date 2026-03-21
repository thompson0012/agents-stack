# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

Task 35 is now complete. The base template skill suite gained a few portable methodology upgrades without changing the repo's philosophy: `self-cognitive` and `feature-spec` now include an adversarial preflight challenge, router-creation guidance now treats `recommends` as honest next-step metadata instead of a wish list, `website-building/shared/09-technical.md` now suggests low-fidelity flow sketches for non-trivial web work, and the base-template audit now scans router `references/children.json` files for stale paths, vendor strings, and template placeholders. The next likely step is to resume the targeted methodology refinement pass across the finance, research, and webapp docs that were already flagged as promising follow-up work.

## Latest Completed Work

Added portable methodology guidance in `templates/base/.agents/skills/self-cognitive/SKILL.md`, `templates/base/.agents/skills/feature-spec/SKILL.md`, `templates/base/.agents/skills/website-building/shared/09-technical.md`, and the `create-router-skill` docs so preflight challenge, optional flow-sketching, and honest companion recommendations are explicit. Extended `scripts/audit_base_template_skills.py` plus `scripts/tests/test_audit_base_template_skills.py` so router metadata JSON is audited for the same stale-path, vendor-string, and placeholder drift already checked in markdown and targeted template assets.

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Resume the methodology refinement pass in the finance, research, and website-building/webapp docs that were already identified as likely follow-up targets, reusing the new preflight-challenge and honest-companion patterns only where they genuinely improve the skill.

## Touched Files

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

- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/self-cognitive --strict`
- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/feature-spec --strict`
- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/create-router-skill --strict`
- `python3 templates/base/.agents/skills/create-router-skill/scripts/validate_router.py templates/base/.agents/skills/website-building --strict`
- `python3 -m unittest scripts.tests.test_audit_base_template_skills scripts.tests.test_vendor_agnostic_naming -v`
- `python3 -m py_compile scripts/audit_base_template_skills.py scripts/tests/test_audit_base_template_skills.py scripts/tests/test_vendor_agnostic_naming.py`
- `python3 scripts/audit_base_template_skills.py`
- `git diff --check` returned no output
- readback review confirmed the new preflight-challenge guidance in `self-cognitive` and `feature-spec`, the optional flow-sketch step in `website-building/shared/09-technical.md`, and the clarified `recommends` semantics in the `create-router-skill` docs

## Hand-off Note

Portable methodology tightening now covers three new patterns worth reusing carefully: adversarial preflight challenge before execution, honest router-level companion recommendations via `recommends`, and optional low-fidelity state/flow sketches before non-trivial web implementation. The base-template audit also now scans router `references/children.json` files, so metadata drift is checked alongside markdown and targeted template assets.