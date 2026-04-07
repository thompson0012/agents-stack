# Live Idea Backlog

Use this file for open exploration before proposal work. Capture rough problems, candidate directions, tradeoffs, dependencies, and the signals that would justify promotion into tracked backlog work.

This file is durable state. Update it in place so future agents can see what was considered, what was rejected, and what still needs thought.

## What belongs here
- ideas that are too early, too broad, or too uncertain for `generator-proposal`
- refinements to existing backlog items that still need ideation
- constraints, dependencies, and repo-specific risks worth remembering
- rejected directions and open questions that should survive chat context loss

## What does not belong here
- the runnable sprint selector
- approved sprint contracts
- implementation checklists or code-change plans
- claims that `.harness/<feature-id>/` should exist already

`docs/live/tracked-work.json` remains the authoritative tracked-work ledger. Use that file to track backlog truth, runnable state, and the single runnable active sprint.

## Promotion guide
- create or update exactly one backlog entry in `docs/live/tracked-work.json`
- assign a stable `id`, `title`, `summary`, `priority`, and `dependencies`
- use `status: "needs_brainstorm"` when the item is tracked but still needs ideation before proposal
- use `status: "pending"` only when the item is ready for proposal
- add a pointer back to this file or section if the tracked-work schema supports it
- do not set `runnable_active_sprint_id`
- do not open `.harness/<feature-id>/`

## Idea entry template
### IDEA-TEMPLATE: Working title
- Related workstream id: none yet | WORKSTREAM-###
- Current state: exploring | needs_brainstorm | ready_to_promote | parked | rejected
- Problem statement:
- Why now:
- Constraints and dependencies:
- Rejected or risky directions:
- Open questions:
- Promotion signal:
