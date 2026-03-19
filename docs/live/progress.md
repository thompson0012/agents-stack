# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

The base template skill suite now has a repo-level audit gate, a broad portability cleanup, and an upgraded `startup-pressure-test` skill that is easier to trigger, defaults to a complete one-pass viability teardown, and now branches its pressure logic by startup archetype and secondary drag when that changes the dominant failure mechanism. Prompt-pressure evaluation of the wider router suite is still pending.

## Latest Completed Work

Expanded `startup-pressure-test` with additional archetype branches for usage-based API businesses, services disguised as software, low-ticket ecommerce, creator/media businesses, and developer tools facing open-source competition. Added secondary-drag rules for overlapping archetypes and added router-level eval coverage in `using-agent-practices` so borderline startup viability requests are tested against generic reasoning and research routes.

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Resume Task 28: run prompt-pressure evaluations against the expanded router suite with `python3 scripts/audit_base_template_skills.py` kept green after each follow-up change.

## Touched Files

- `scripts/audit_base_template_skills.py`
- `.github/workflows/base-template-skill-audit.yml`
- `templates/base/.agents/skills/{coding-and-data,design-foundations,feature-spec,generating-design-tokens,media,meta-prompting,self-cognitive,startup-pressure-test,visualization}/SKILL.md`
- `templates/base/.agents/skills/startup-pressure-test/evals/{evals.json,trigger-evals.json}`
- `templates/base/.agents/skills/using-agent-practices/evals/{evals.json,trigger-evals.json}`
- `templates/base/.agents/skills/using-{documents,finance,research,reasoning,legal,marketing,sales}/**`
- `templates/base/.agents/skills/website-building/{SKILL.md,game/**,informational/**,shared/**,webapp/**}`
- `docs/live/current-focus.md`
- `docs/live/progress.md`
- `docs/live/todo.md`
- deleted `.DS_Store` artifacts under repo root, `.git/`, and `templates/base/.agents/**`

## Verification Status

Observed success for:

- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/startup-pressure-test --strict`
- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/using-agent-practices --strict`
- `python3 scripts/audit_base_template_skills.py`

## Hand-off Note

The new audit script is now the truth source for portability drift: it runs strict leaf/router validation and scans for stale `skills/` paths, unsupported tool names, vendor strings, and `.DS_Store` artifacts. Run it before claiming future skill-suite edits are complete.