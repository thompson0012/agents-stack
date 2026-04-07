---
name: context-compaction
description: Use when the same role must continue the same work after a reset, long session, or context-pressure event and needs a compact continuation snapshot anchored to durable files.
---

# Context Compaction

Use this leaf skill to produce a compact continuation snapshot for the same owner after a reset. It preserves the minimum truthful state needed to resume work without pretending to redesign the workflow, change owners, or replace the repo's durable artifacts.

## Boundary

Use this skill when:
- the same role should continue after a reset, reconnect, or context-window pressure event
- most truth already lives in durable files, but the next session needs a compact resume anchor
- the main problem is carrying forward active state, not choosing a new owner or control model

Do not use this skill when:
- the real question is whether the work should stay `single-session`, become `compacted-continuation`, or move into a multi-role loop — that belongs to `delivery-control/harness-design` or the template orchestrator
- ownership is changing across planner / generator / evaluator / reviewer lanes
- the next step is contract approval, scope repair, or orchestration repair
- a vague narrative summary would hide the stronger truth already present in files

## Core Contract

- Produce exactly one continuation snapshot for the same owner.
- Preserve final state, not the history of how the state changed.
- Point back to durable files instead of inlining their contents.
- Carry forward only active session or task constraints that are not already recoverable from standing repo rules.
- Keep the original objective and the current focus separate when they drifted.
- Name the strongest artifacts to re-read on resume.
- State the next action concretely enough that a cold-start session can continue without guessing.
- Do not choose a new owner, invent a baton protocol, or approve the contract. If those decisions are still open, this skill is the wrong tool.

## Read Before Compacting

Read the strongest durable artifacts first. In a harnessed repo, this usually means:
- repo constitution: `AGENTS.md` or `templates/AGENTS.md`
- current sprint truth: the strongest local artifact such as `.harness/<WORKSTREAM-ID>/review.md`, `handoff.md`, `runtime.md`, or `contract.md`
- current live selectors: `docs/live/current-focus.md` and `docs/live/tracked-work.json`
- any modified outputs that exist only in chat, scratch notes, or unstored tool output

If a stronger durable artifact disagrees with chat memory, compact the file truth.

## Output Shape

Return a compact markdown snapshot with these sections:

1. `Original objective`
2. `Current focus`
3. `Resume owner` — always state that the same owner continues
4. `Re-read first` — 3 to 6 highest-value file paths
5. `Active constraints` — only session/task constraints not already covered by standing docs
6. `Final decisions`
7. `File state` — modified / created / pending with short notes
8. `Open tasks and blockers`
9. `Last action`
10. `Next action`

Use this template:

```markdown
# Compacted Continuation Snapshot

## Original objective
- ...

## Current focus
- ...
- Drift from original objective: none / [brief reason]

## Resume owner
- Same owner continues. This snapshot does not reassign ownership.

## Re-read first
- `path/to/highest-value-file`
- `path/to/next-file`
- `path/to/another-file`

## Active constraints
- ...
- If none: `No active session-specific constraints.`

## Final decisions
- Topic -> final decision

## File state
- `path/to/file` — modified / created / pending — short note

## Open tasks and blockers
- [ ] ...
- Blockers: none / ...

## Last action
- ...

## Next action
- ...
```

## Pruning Rules

Keep:
- strongest file paths to re-read
- final decisions still in force
- active constraints that would be lost across reset
- touched files and the concrete next step

Drop:
- raw tool logs
- repeated standing `AGENTS.md` rules
- abandoned alternatives and superseded tactics
- full file contents that can be re-read directly
- baton, reviewer, or multi-owner routing decisions owned elsewhere

## Failure Modes to Avoid

- Calling a loose summary a compaction artifact.
- Copying standing repo rules instead of referencing the file that already owns them.
- Inlining large file contents instead of naming the file paths.
- Mixing expired tactics with active constraints.
- Using this skill to decide ownership, approval, or orchestration mode.
- Producing a snapshot that leaves the next action vague or unstated.