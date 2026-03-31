# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

The template AGENTS hierarchy rollout is complete in this worktree: the hierarchy suite now asserts the reference-doc truth, the template reference docs encode the approved boundaries, and verification is green aside from the known pre-existing `delivery-control` audit blocker.

## Latest Completed Work

- extended `scripts/tests/test_template_agents_hierarchy.py` with a reference-doc truth assertion and ran it red before updating docs
- updated `templates/base/docs/reference/{architecture,codemap,memory,lessons}.md` so they record the approved hierarchy truth: constitutional root, approved local boundaries, root indexing duty, inert template live docs, shipped-vs-optional separation, and hierarchy anti-patterns
- reran the hierarchy suite and inert live-doc suite, then checked the base-template audit and confirmed it still reports only the known `delivery-control` blocker
- verified whitespace cleanliness with `git diff --check`

## In Progress

None.

## Blockers

- `python3 scripts/audit_base_template_skills.py` remains red only because of the pre-existing `templates/base/.agents/skills/delivery-control` eval-schema failure.

## Next Recommended Action

Review the committed hierarchy rollout in the context of the broader harness goal-lineage work; no further action is required for this task itself.

## Touched Files

- `scripts/tests/test_template_agents_hierarchy.py`
- `templates/base/docs/reference/architecture.md`
- `templates/base/docs/reference/codemap.md`
- `templates/base/docs/reference/memory.md`
- `templates/base/docs/reference/lessons.md`
- `docs/live/progress.md`

## Verification Status

- `python3 -m unittest scripts.tests.test_template_agents_hierarchy.TemplateAgentsHierarchyTests.test_reference_docs_encode_the_template_agents_hierarchy_truth` failed first, then passed after the reference-doc updates
- `python3 -m unittest scripts.tests.test_template_agents_hierarchy`
- `python3 -m unittest scripts.tests.test_goal_lineage_templates`
- `python3 scripts/audit_base_template_skills.py` (fails only for the known pre-existing `delivery-control` eval-schema blocker)
- `git diff --check`

## Hand-off Note

Task 3 is done in this worktree. Keep the `delivery-control` audit failure treated as pre-existing until that package is repaired in its own task.
