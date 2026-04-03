# Sprint Contract: FEAT-000

## Objective
Initialize the repository's durable harness state so future work routes from files instead of chat memory.

## Allowed Files
- `AGENTS.md`
- `docs/live/features.json`
- `docs/live/progress.md`
- `docs/live/memory.md`
- `docs/reference/architecture.md`
- `docs/reference/design.md`

## Forbidden Changes
- Do not create or modify `.harness/FEAT-001/` in this sprint.
- Do not implement FEAT-001 or any app behavior.
- Do not fabricate completed backlog history.
- Do not mark any feature `in_progress`.

## Acceptance Criteria
1. `AGENTS.md` defines the canonical repository topology, state roles, single-runnable-sprint rule, lifecycle phases, and role responsibilities.
2. `docs/live/features.json` parses as valid JSON and records FEAT-001 as pending, with no runnable active sprint.
3. `docs/live/progress.md` records FEAT-000 as an initialization sprint and names FEAT-001 as the next action.
4. `docs/live/memory.md` preserves at least one durable operational truth the next sprint must remember: verify Tailwind is loaded before browser QA.
5. `docs/reference/architecture.md` and `docs/reference/design.md` describe the current starter state truthfully and concisely.

## Review Script
1. Run `python -m json.tool docs/live/features.json`.
2. Read `AGENTS.md` and confirm the topology and lifecycle sections are concrete rather than placeholder text.
3. Read `docs/live/progress.md` and verify it records FEAT-000 without pretending additional history exists.
4. Read `docs/live/memory.md` and verify the Tailwind caveat is preserved as durable guidance.
5. Read both reference docs and confirm they describe the current starter repository, not an imagined finished product.

## Non-goals
- No browser session is required for this sprint.
- No runtime process should be left running.
- No archive artifacts should be produced until review passes.
