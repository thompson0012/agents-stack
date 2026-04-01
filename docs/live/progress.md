# Progress

Read after `current-focus.md` to recover the latest state and hand-off details. Keep each section concise.

## Current State

Template cutover batch is in progress. Phases 1-3 are complete; Phase 4 verification is active.

See `roadmap.md` for the full phase ledger and goal lineage.

## Latest Completed Work

- Recast root live docs (`current-focus.md`, `progress.md`, `todo.md`, `roadmap.md`) to describe the template-cutover objective.
- Aligned `templates/base/docs/live/` scaffolds to mirror the root standard while staying inert.
- Aligned `templates/base/docs/reference/` scaffolds to mirror the root standard while staying inert.
- Updated `templates/base/AGENTS.md` and root `AGENTS.md` to remove `software-delivery` wording and align with `delivery-control`.
- Prior batch (complete): root docs control-plane cutover — split README/AGENTS, aligned live docs, replaced reference placeholders, deduplicated router prose.

## Blockers

None.

## Touched Files

- `docs/live/{current-focus,progress,todo,roadmap}.md`
- `AGENTS.md`
- `templates/base/AGENTS.md`
- `templates/base/docs/live/{current-focus,progress,todo,roadmap}.md`
- `templates/base/docs/reference/{codemap,architecture,memory}.md`

## Verification

- `git diff --check` passed.
- Confirmed no `software-delivery` remains in root or template AGENTS.
- Confirmed the template live docs mirror the root standard while remaining inert.
- Confirmed the template reference scaffolds are structural only, not seeded project truth.

## Next Recommended Action

- Complete Phase 4: cross-surface verification of the root and template contract surfaces, then decide whether to add any follow-up hardening notes to `docs/reference/lessons.md`.
