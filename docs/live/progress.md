# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

The root repository now has a lean AGENTS router with executable validation, and the portable `templates/base/` subtree now ships only clean root-relative startup assets: a manifest plus boundary guides, with no seeded repo-specific script or command text.

## Latest Completed Work

- changed the template hierarchy test first and watched it fail red until the portable template no longer shipped a seeded validator script or `templates/base/` path text
- kept `templates/base/.agents/router-manifest.json` inside the template as the portable machine-readable router artifact, but removed the seeded `templates/base/scripts/validate_agents_router.py` script
- cleaned `templates/base/AGENTS.md` so its Operational Commands section is startup-safe and command-free by default; downstream repos must localize their own real toolchain commands after copy
- removed remaining `templates/base/` path leakage from the copied template docs and references so the template now reads as root-relative after copy
- updated `templates/base/.agents/AGENTS.md` and `templates/base/docs/reference/{architecture,codemap,memory}.md` so the portable manifest and clean copied-root contract remain truthful
- reran the template hierarchy and goal-lineage tests and confirmed they pass after the cleanup
- verified with a grep sweep that no seeded `templates/base/`, repo test command, audit command, or copied-root validator command text remains anywhere under `templates/base/`
- verified whitespace cleanliness with `git diff --check`

## In Progress

None.

## Blockers

None for this cleanup task.

## Next Recommended Action

No further cleanup is required for `templates/base/` itself. If desired later, the separate pre-existing `delivery-control` audit issue can still be repaired in its own task.

## Touched Files

- `templates/base/AGENTS.md`
- `templates/base/.agents/AGENTS.md`
- `templates/base/.agents/router-manifest.json`
- `templates/base/.agents/skills/using-labs21-suite/references/category-map.md`
- `templates/base/docs/AGENTS.md`
- `templates/base/docs/reference/architecture.md`
- `templates/base/docs/reference/codemap.md`
- `templates/base/docs/reference/memory.md`
- `scripts/tests/test_template_agents_hierarchy.py`
- `docs/live/progress.md`

## Verification Status

- RED first: `python3 -m unittest scripts.tests.test_template_agents_hierarchy` failed because the template still shipped a seeded validator script and repo-specific path text
- GREEN: `python3 -m unittest scripts.tests.test_template_agents_hierarchy`
- GREEN: `python3 -m unittest scripts.tests.test_goal_lineage_templates`
- GREEN: grep sweep over `templates/base/` found no remaining `templates/base/`, repo test command, audit command, or copied-root validator-command text in `.md`, `.json`, or `.py` files
- GREEN: `git diff --check`

## Hand-off Note

`templates/base/` now behaves like a clean startup template: it ships root-relative guidance, inert live-doc scaffolds, and a portable manifest, but no seeded repo-specific validator script or maintenance command text. No `docs/live/current-focus.md` update was needed because the active objective and scope did not change. Reference docs were updated because the portable template contract changed durably.
