# Live Idea Backlog

Use this file for open exploration before proposal work. Capture rough problems, candidate directions, tradeoffs, dependencies, and the signals that would justify promotion into tracked backlog work.

This file is durable state. Update it in place so future agents can see what was considered, what was rejected, and what still needs thought.

## What belongs here
- ideas that are too early, too broad, or too uncertain for `generator-proposal`
- refinements to existing backlog items that still need ideation
- constraints, dependencies, and repo-specific risks worth remembering
- rejected directions, dead ends, and open questions that should survive chat context loss

## What does not belong here
- the runnable sprint selector
- approved sprint contracts
- implementation checklists or code-change plans
- claims that `.harness/<feature-id>/` should exist already

`docs/live/features.json` remains the authoritative tracked-work ledger. Use that file to track backlog truth, runnable state, and the single runnable active sprint. Use this file to make idea exploration durable.

## How to promote an idea into `features.json`
Promote an idea only when you can name:
1. the real repo problem or opportunity
2. the user or system outcome that matters
3. the likely dependencies or blockers
4. the next bounded planning step

When promoting:
- create or update exactly one backlog entry in `docs/live/features.json`
- assign a stable `id`, `title`, `summary`, `priority`, and `dependencies`
- use `status: "needs_brainstorm"` when the item should be tracked but still needs ideation before proposal
- use `status: "pending"` only when the item is ready for `generator-proposal`
- add a pointer back to this file or section if the tracked-work schema supports it
- do not set `runnable_active_sprint_id`
- do not open `.harness/<feature-id>/`

## Status guide
- `needs_brainstorm`: the item is promising enough to track, but the next honest step is still ideation
- `pending`: the item is already bounded enough for proposal work; details here may still provide context, but `features.json` now owns tracked backlog priority

## Idea entry template
Use one section per candidate so promotion and refinement stay traceable.

### IDEA-TEMPLATE: Working title
- Related feature id: none yet | FEAT-000
- Current state: exploring | needs_brainstorm | ready_to_promote | parked | rejected
- Problem statement:
- Why now:
- Constraints and dependencies:
- Rejected or risky directions:
- Open questions:
- Promotion signal:

## Active exploration lanes

### Needs brainstorm before proposal
Use this section for ideas that are important enough to keep visible but not yet ready for proposal.

### Ready to promote
Move an idea here only when the next honest step is to create or update a backlog entry in `docs/live/features.json` with `status: "pending"`.

### Parked or rejected
Keep short notes here for ideas that should not be rediscovered without context. Record why they were deferred, rejected, or superseded.