# Sprint Proposal: FEAT-000

## Title
Initialize the starter repository for the agents-stack harness

## Problem
The repository needs durable state before any execution sprint can be trusted. Without a canonical `AGENTS.md`, live ledgers, and reference docs, a future agent would have to infer topology and priorities from chat memory or placeholders.

## Objective
Create the minimum truthful starter state so the next sprint can begin from files alone:
- establish the canonical harness rules in `AGENTS.md`
- seed global live state in `docs/live/*`
- capture initial reference context in `docs/reference/*`
- leave FEAT-001 queued as the next feature instead of starting implementation prematurely

## In Scope
- write `AGENTS.md` for the harness lifecycle, state precedence, and role boundaries
- create `docs/live/features.json` with FEAT-001 queued and no runnable active sprint yet
- create `docs/live/progress.md` and `docs/live/memory.md`
- create `docs/reference/architecture.md` and `docs/reference/design.md`
- record any verified bootstrap caveats the next sprint must know

## Out of Scope
- implementing FEAT-001 dark mode behavior
- browser QA against the app itself
- creating `.harness/FEAT-001/` execution artifacts
- inventing project history that did not happen

## Allowed Files
- `AGENTS.md`
- `docs/live/features.json`
- `docs/live/progress.md`
- `docs/live/memory.md`
- `docs/reference/architecture.md`
- `docs/reference/design.md`

## Verification Plan
1. Confirm each required file exists and has non-placeholder content.
2. Parse `docs/live/features.json` successfully as JSON.
3. Read `AGENTS.md` and verify it defines topology, lifecycle, and state precedence.
4. Read `docs/live/progress.md` and `docs/live/memory.md` to verify they record the current baseline without fake history.
5. Confirm the next recommended action is FEAT-001, not immediate implementation.

## Risks and Open Questions
- Tailwind wiring is not proven by this sprint; FEAT-001 must verify styles actually load before relying on dark-mode classes.
- The backlog beyond FEAT-001 is intentionally unspecified until a human or planner adds real priorities.
- If existing repo docs disagree with the initialized files, the conflict must be corrected before opening a code-changing sprint.

## Exit Condition
This sprint is complete only when a new agent can enter cold, read the repository, and determine that FEAT-001 is the next bounded unit of work without consulting chat history.
