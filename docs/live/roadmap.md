# Roadmap

Canonical carrier for phased-work goal lineage. Read after `current-focus.md` to understand where the current objective came from, what phases deliver it, and how to resume after compaction.

## Source Goal

- Source goal: Every generated repo should ship the same docs-control-plane standard that the root repo uses — live docs, reference scaffolds, and agent/router contracts — so agents resuming in any generated project find the same surfaces, same conventions, same progressive-disclosure contract.
- Origin: the root cutover established the standard (five surfaces, one job each, no overlap), but `templates/base/` still carries the old shape: different scaffold fields, missing conventions, and `AGENTS.md` prose referencing the obsolete `software-delivery` name.

## Plan Goal

- Plan goal: Single-batch cutover that aligns template scaffolds (live, reference), updates template and root `AGENTS.md` to remove `software-delivery`, and verifies cross-surface coherence — without filling scaffolds with real content.

## Phase Ledger

| Phase | Description | Status |
| --- | --- | --- |
| 0 | Recast root live docs to describe the template-cutover objective | Completed |
| 1 | Align `templates/base/docs/live/` scaffolds to the root standard | Not started |
| 2 | Align `templates/base/docs/reference/` scaffolds to the root standard | Not started |
| 3 | Update `templates/base/AGENTS.md` and root `AGENTS.md` — remove `software-delivery`, align contract | Not started |
| 4 | Cross-surface verification: no overlap, stale references, or contradictions | Not started |

## Goal Changes

| Date | Change | Reason |
| --- | --- | --- |
| 2026-04-01 | New batch: template cutover replaces completed root cutover as the active objective | Root cutover is done; templates still carry the old shape |

## Resume Rules

1. Read `current-focus.md` first for the active objective and constraints.
2. Read this file to locate the current phase and confirm the source goal has not changed.
3. Read `progress.md` for session-level state: what was just done, what to do next.
4. Read `todo.md` for the actionable queue.
5. Do not rely on chat memory. All resumable state lives in these four files.
6. When a phase completes, mark it `Completed` in the ledger above and update `progress.md` and `todo.md` accordingly.
7. When the source goal changes, record the change in the Goal Changes table with a date and reason.
