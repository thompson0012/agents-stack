---
name: project-initializer
purpose: Bootstrap the durable global state for a repo that is entering the agents-stack harness for the first time.
trigger: Use when `docs/live/features.json` is missing, empty, or otherwise not yet trustworthy as project state.
inputs:
  - AGENTS.md
  - existing repository structure and source files
  - docs/live/* if present
  - docs/reference/* if present
outputs:
  - docs/live/features.json
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/architecture.md
  - docs/reference/design.md
boundaries:
  - Do not invent completed work, fake backlog history, or archived sprints.
  - Do not start implementation or open an active sprint folder.
  - Do not mark any feature `in_progress` unless the human explicitly selected it.
next_skills:
  - generator-proposal
---

# Project Initializer

## Mission
Create the minimum durable state needed for the harness to operate truthfully.

This phase establishes the repo's current facts, not a fictional project narrative. Its job is to make future planning resumable from files alone.

## Worker Dispatch Contract

- Run this phase in a fresh worker context selected by the orchestrator, not by loading initialization into the orchestrator's own window.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: repository discovery plus writes to `docs/live/*` and `docs/reference/*` only. No product-code edits, no `.harness/<feature-id>/` execution work, no archive writes.
- Durable return contract: `docs/live/features.json`, `docs/live/progress.md`, `docs/live/memory.md`, `docs/reference/architecture.md`, and `docs/reference/design.md`. If the host provides worker metadata, record `worker_id` / `orchestrator_run_id` in the initialization ledger entry or equivalent durable note.

## Required Reads
Read these before writing anything:

1. `AGENTS.md`
2. Existing `docs/live/*` and `docs/reference/*` files, if present
3. Repository manifests and entrypoints that reveal actual architecture
4. Any existing tests, scripts, or app shells that define how the project runs

If the repo already contains trustworthy state files, update them in place instead of replacing them with a generic template.

## Expected Outputs
Produce or repair these durable global files:

### `docs/live/features.json`
A truthful backlog snapshot.
- If the human already named features, record them.
- If no backlog is known yet, write an empty backlog or a clearly minimal seed set derived from explicit user goals only.
- Never fabricate completed items or pretend a feature has already been selected.

### `docs/live/progress.md`
A ledger of known project progress.
- It may begin with a single initialization entry.
- It must not imply prior sprints happened if they did not.
- If history is unknown, say so plainly.

### `docs/live/memory.md`
A concise durable summary of facts future agents should not rediscover every session.
- Record actual repo topology, major frameworks, critical run commands if observed, and known constraints.
- Record uncertainty explicitly instead of guessing.

### `docs/reference/architecture.md`
A short description of the current system shape.
- Note main runtime, entrypoints, important subsystems, and integration boundaries.
- Mark gaps as unknown where the repo does not reveal them.

### `docs/reference/design.md`
A short description of the current product or UI intent.
- Capture existing visual system, interaction model, and notable UX constraints.
- If the repo is not UI-heavy, say that directly.

## Workflow

### 1. Establish whether initialization is actually needed
- If durable state already exists and is coherent, stop and hand off to the next phase.
- Only initialize missing, empty, or untrustworthy state.

### 2. Read the repo, not your assumptions
- Inspect real files to identify the app type, runtime, entrypoints, and major feature areas.
- Derive architecture notes from code and configuration, not from naming vibes.
- Prefer explicit uncertainty over plausible fiction.

### 3. Create truthful global state
- Write `features.json` from explicit user goals or verified backlog items only.
- If there is not enough information to define backlog priorities responsibly, leave the backlog small and honest.
- Record the current baseline in `progress.md` without backfilling fake history.

### 4. Capture durable references for future agents
- Summarize architecture and design in the reference docs.
- Record repo-specific gotchas, conventions, or operational constraints in `memory.md`.
- Keep these documents concise enough to stay maintained.

### 5. Verify the initialized state is usable
Confirm a future planner could answer all of the following from files alone:
- What project is this?
- What features are candidates for work?
- What is already known about architecture and design?
- What is still unknown and must be discovered later?

## File Write Expectations
- Write only global durable state in this phase.
- Do not create `.harness/<feature-id>/` yet unless the user explicitly instructed you to open a sprint immediately.
- Do not create anything under `docs/archive/` during initialization.
- When updating existing files, preserve observed facts and replace only stale boilerplate.

## Refusal and Stop Conditions
Stop and report the gap instead of inventing content when:
- The repo contents are too sparse to infer architecture truthfully.
- The user goal is too vague to seed even a minimal backlog.
- Existing state files contradict the codebase and you cannot resolve which is authoritative.
- Initialization would require selecting a feature or architecture direction the human has not chosen.

In those cases, write the uncertainty into the durable files if appropriate; do not disguise it.

## Quality Bar
A good initialization pass:
- tells the truth about what is known vs unknown
- creates no fake project history
- leaves the backlog usable for planning without overcommitting
- reflects the real repo topology and current architecture
- gives the next agent enough durable context to start proposal work without chat history

## Done Definition
This skill is done when the repo has coherent global state, no active sprint has been fabricated, and the next phase can select a real feature from durable files.