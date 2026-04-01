# Current Focus

Read after `AGENTS.md` when starting or resuming work. Keep this file limited to the current objective and the bounds for active work.

## Objective

Propagate the docs-control-plane standard into `templates/base/` so every generated repo ships the same live-doc, reference-scaffold, and agent/router conventions that the root repo now uses.

The root cutover established five surfaces with one job each (README, AGENTS, live docs, reference docs, router skills). Templates still carry the old shape: different scaffold fields, missing `roadmap.md` conventions, and `AGENTS.md` prose that references `software-delivery` instead of `delivery-control`.

## Scope

In scope:
- Align `templates/base/docs/live/` scaffolds to mirror the root standard: current-focus, progress, todo, roadmap — same headings, same field names, still inert (no seeded policy prose).
- Align `templates/base/docs/reference/` scaffolds to mirror the root standard: task-first headings, honest field names, no placeholder content pretending to be filled.
- Update `templates/base/AGENTS.md` to replace `software-delivery` references with `delivery-control` and align progressive-disclosure rules with the root contract.
- Update root `AGENTS.md` to remove any remaining `software-delivery` wording.
- Verify no overlap, no stale references, no contradictions between root and template surfaces.

Out of scope:
- Modifying product code, template generation logic, or validator scripts.
- Reopening the root docs cutover — that work is complete.
- Adding new router families, skill packages, or product-specific implementation work.
- Filling template scaffolds with real content — they must remain inert structure.

## Constraints

- One concept, one representation — no compatibility shims, no duplicate authorities.
- Live docs must be self-contained: an agent resumes from these files, not chat memory.
- Template live docs remain neutral scaffolds with no seeded prose.
- Root live docs describe the template-cutover work, not the finished root cutover.

## Success Criteria

- Root live docs reflect the template-cutover objective and roadmap.
- `templates/base/docs/live/` scaffolds mirror the root standard while staying blank/inert.
- `templates/base/AGENTS.md` and root `AGENTS.md` no longer mention `software-delivery`.
- Template reference scaffolds mirror the root standard and do not pretend to be filled content.
