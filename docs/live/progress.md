# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

Task 34 is complete and the follow-up vendor-agnostic rename sweep also landed: the known legacy vendor residue has been removed from shared website assets, helper scripts, audit coverage, and document-script defaults. The next likely step is still a capability-based methodology refinement pass across the finance, research, and webapp docs that were already flagged as promising follow-up targets.

## Latest Completed Work

Renamed the remaining legacy vendor file and symbol names to vendor-agnostic alternatives (`provenance_metadata.html`, `OptionalAttribution.tsx`), generalized the audit patterns and tests, changed DOCX comment defaults to `Agent` / `AG`, and replaced the media-helper private SDK coupling with a provider-agnostic `media_client.py` adapter contract plus updated docs. Fresh unittest, py_compile, audit, and repo-wide grep verification all passed with no remaining legacy vendor name matches.

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Review the identified methodology-heavy docs in finance, research, and website-building/webapp, then tighten their capability-based guidance without reintroducing stale or vendor-specific surface assumptions.

## Touched Files

- `scripts/audit_base_template_skills.py`
- `scripts/tests/test_audit_base_template_skills.py`
- `scripts/tests/test_vendor_agnostic_naming.py`
- `.github/workflows/base-template-skill-audit.yml`
- `templates/base/.agents/skills/{coding-and-data,design-foundations,feature-spec,generating-design-tokens,media,meta-prompting,self-cognitive,startup-pressure-test,visualization}/SKILL.md`
- `templates/base/.agents/skills/startup-pressure-test/evals/{evals.json,trigger-evals.json}`
- `templates/base/.agents/skills/using-agent-practices/{SKILL.md,evals/**,references/category-map.md}`
- `templates/base/.agents/skills/using-{documents,finance,research,reasoning,legal,marketing,sales}/**`
- `templates/base/.agents/skills/website-building/{SKILL.md,game/**,informational/**,shared/**,webapp/**}`
- `docs/live/current-focus.md`
- `docs/live/progress.md`
- `docs/live/todo.md`
- deleted `.DS_Store` artifacts under repo root, `.git/`, and `templates/base/.agents/**`

## Verification Status

Observed success for:

- `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/using-agent-practices --strict`
- `python3 templates/base/.agents/skills/using-documents/scripts/validate_router.py templates/base/.agents/skills/using-documents`
- `python3 templates/base/.agents/skills/using-reasoning/scripts/validate_router.py templates/base/.agents/skills/using-reasoning`
- `python3 -m unittest scripts.tests.test_audit_base_template_skills scripts.tests.test_vendor_agnostic_naming -v`
- `python3 -m py_compile scripts/audit_base_template_skills.py scripts/tests/test_audit_base_template_skills.py scripts/tests/test_vendor_agnostic_naming.py templates/base/.agents/skills/using-documents/docx/scripts/comment.py templates/base/.agents/skills/website-building/shared/llm-api/media_client.py templates/base/.agents/skills/website-building/shared/llm-api/generate_image.py templates/base/.agents/skills/website-building/shared/llm-api/generate_video.py templates/base/.agents/skills/website-building/shared/llm-api/generate_audio.py templates/base/.agents/skills/website-building/shared/llm-api/transcribe_audio.py`
- `python3 scripts/audit_base_template_skills.py`
- repo-wide grep for the removed vendor-name patterns returned no matches

## Hand-off Note

The audit script is now the truth source for portability drift across both markdown skill docs and the currently targeted non-markdown website-building assets. Keep the scan explicit for now: the concrete website-building files were enough to catch real residue, and broader non-markdown scanning should wait for evidence that more template assets are drifting.