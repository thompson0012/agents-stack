---
name: project-initializer
purpose: Bootstrap the durable global state for a repo that is entering the agents-stack harness for the first time.
trigger: Use when `docs/live/tracked-work.json` is missing, empty, or otherwise not yet trustworthy as project state.
inputs:
  - AGENTS.md
  - existing repository structure and source files
  - docs/live/* if present
  - docs/reference/* if present
  - docs/records/* if present
outputs:
  - docs/live/tracked-work.json
  - docs/live/current-focus.md
  - docs/live/roadmap.md
  - docs/live/ideas.md
  - docs/live/progress.md
  - docs/live/memory.md
  - docs/reference/architecture.md
  - docs/reference/design.md
boundaries:
  - Do not invent completed work, fake backlog history, archived sprints, or synthetic record pages.
  - Do not start implementation or open an active sprint folder.
  - Do not mark any feature `in_progress` unless the human explicitly selected it.
next_skills:
  - generator-proposal
---

# Project Initializer

## Mission
Create the minimum durable state needed for the harness to operate truthfully.

This phase establishes the repo's current facts, not a fictional project narrative. Its job is to make future planning resumable from files alone.

That durable state now sits inside a broader durable-doc topology:
- `docs/live/tracked-work.json` for authoritative tracked work, runnable truth, and live file pointers
- `docs/live/current-focus.md` for the current objective, goal lineage, next owner, and next file to open
- `docs/live/roadmap.md` for the non-runnable source-goal roadmap across slices or phases
- `docs/live/ideas.md` for open exploration, rough candidates, and pre-proposal refinement that must survive across sessions

Alongside those live artifacts, the harness preserves distinct durable lanes: `docs/reference/*` for current stable truth, `docs/records/*` for feature-linked durable records with page-local provenance, and `docs/archive/*` for PASS-history evidence. Initialization should recognize that topology, preserve existing records when present, and avoid inventing record content just to fill the tree.

## Worker Dispatch Contract

- Run this phase in a fresh worker context selected by the orchestrator, not by loading initialization into the orchestrator's own window.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: repository discovery plus writes to `docs/live/*` and `docs/reference/*` only. Read existing `docs/records/*` when they already exist so backlog traceability stays coherent, but do not author new record pages during bootstrap. No product-code edits, no `.harness/<feature-id>/` execution work, no archive writes.
- Durable return contract: `docs/live/tracked-work.json`, `docs/live/current-focus.md`, `docs/live/roadmap.md`, `docs/live/ideas.md`, `docs/live/progress.md`, `docs/live/memory.md`, `docs/reference/architecture.md`, and `docs/reference/design.md`. If the host provides worker metadata, record `worker_id` / `orchestrator_run_id` in the initialization ledger entry or equivalent durable note.
- Dispatch framing is non-authoritative. Before acting, verify that the dispatched repo state still matches durable files: `docs/live/tracked-work.json` for live tracked-work truth, the strongest existing local/live artifact for the claimed phase, and any stronger evidence identified by the `AGENTS.md` precedence chain.
- If the dispatch frame conflicts with stronger durable evidence, stop before writing, preserve the existing truthful files, and hand control back to the orchestrator for correct-lane dispatch.

## Required Reads
Read these before writing anything:

1. `AGENTS.md`
2. Existing `docs/live/*`, `docs/reference/*`, and `docs/records/*` files, if present
3. Repository manifests and entrypoints that reveal actual architecture
4. Any existing tests, scripts, or app shells that define how the project runs

If the repo already contains trustworthy state files, update them in place instead of replacing them with a generic template.

## Expected Outputs
Produce or repair these durable global files:

### `docs/live/tracked-work.json`
A truthful backlog snapshot and runnable selector.
- If the human already named features, record them.
- If no backlog is known yet, write an empty backlog or a clearly minimal seed set derived from explicit user goals only.
- Preserve the runnable backlog fields and compound queue while adding live control-plane pointers such as `current_focus_path` and `roadmap_path`.
- When existing tracked items already have durable traceability, preserve truthful pointers such as `idea_ref`, `record_paths`, `reference_paths`, and the feature's single canonical `evidence_path` instead of dropping them during bootstrap.
- Never fabricate archived items, record links, or pretend a feature has already been selected.
- Use `status: "needs_brainstorm"` when a tracked item is real enough to keep visible but not yet ready for proposal.

### `docs/live/current-focus.md`
A concise live resume anchor.
- State the current objective, source-goal lineage, current roadmap phase, next owner, and next file to open.
- Say explicitly that it is not a second contract.
- If a runnable or parked sprint exists, point back to the strongest local sprint artifact for slice truth instead of duplicating the sprint contract.
- If no meaningful work is active yet, keep the file minimal and honest rather than inventing a fake active lane.

### `docs/live/roadmap.md`
A non-runnable initiative roadmap.
- Record the source goal, current slice, ordered remaining slices or phases, the stop or re-authorization condition, and a visible remaining-work summary.
- Keep it at initiative level. It must not become the runnable sprint selector or a hidden contract.
- If the repo has no meaningful backlog yet, keep the roadmap minimal and honest instead of inventing fake slices.

### `docs/live/ideas.md`
A durable exploration ledger for pre-proposal thinking.
- Put rough ideas, candidate refinements, constraints, rejected directions, and open questions here.
- This file is not the runnable sprint selector; it does not claim `runnable_active_sprint_id`.
- If the repo has known ideas that are not ready for proposal, seed them here instead of overstuffing `tracked-work.json`.
- If there are no concrete ideas yet, create the structure and usage guidance without inventing fake candidate work.

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
- Write `tracked-work.json` from explicit user goals or verified backlog items only.
- If there is not enough information to define backlog priorities responsibly, leave the backlog small and honest.
- Write `current-focus.md` as a resume pointer, not as a second contract.
- Write `roadmap.md` from verified source goals and visible remaining work only.
- Create `ideas.md` as the durable home for open exploration and raw candidates that are not ready for proposal.
- Use `needs_brainstorm` for tracked items that still require ideation before proposal; use `pending` only when proposal work is the next honest step.
- Record the current baseline in `progress.md` without backfilling fake history.

### 4. Capture durable references for future agents
- Summarize architecture and design in the reference docs.
- Record repo-specific gotchas, conventions, or operational constraints in `memory.md`.
- Keep these documents concise enough to stay maintained.

### 5. Verify the initialized state is usable
Confirm a future planner could answer all of the following from files alone:
- What project is this?
- What source goal and roadmap phase are currently active?
- What features are candidates for work?
- Which items still need brainstorm versus proposal?
- What is already known about architecture and design?
- What is still unknown and must be discovered later?

## File Write Expectations
- Write only global durable state in this phase.
- `docs/live/tracked-work.json` remains the authoritative tracked-work ledger and runnable selector.
- `docs/live/current-focus.md` is a live resume aid. It must stay concise and must not become a second contract.
- `docs/live/roadmap.md` is the non-runnable initiative roadmap. It does not choose the active sprint.
- `docs/live/ideas.md` stores exploration detail and idea refinement, not runnable sprint selection.
- Respect the broader durable-doc topology: preserve existing `docs/records/*` links in live state when they already exist, but do not seed new record pages or treat records as a second registry.
- Do not create `.harness/<feature-id>/` yet unless the user explicitly instructed you to open a sprint immediately.
- Do not create anything under `docs/archive/` during initialization.
- When updating existing files, preserve observed facts and replace only stale boilerplate.

## Refusal and Stop Conditions
Stop and report the gap instead of inventing content when:
- The repo contents are too sparse to infer architecture truthfully.
- The user goal is too vague to seed even a minimal backlog or idea ledger.
- Existing state files contradict the codebase and you cannot resolve which is authoritative.
- Initialization would require selecting a feature or architecture direction the human has not chosen.

In those cases, write the uncertainty into the durable files if appropriate; do not disguise it.

## Quality Bar
A good initialization pass:
- tells the truth about what is known vs unknown
- creates no fake project history
- leaves the backlog usable for brainstorm or proposal without overcommitting
- makes the source goal, roadmap phase, and next owner visible from files alone
- reflects the real repo topology and current architecture
- gives the next agent enough durable context to start the correct pre-sprint phase without chat history

## Done Definition
This skill is done when the repo has coherent global state, `docs/live/current-focus.md` and `docs/live/roadmap.md` exist as first-class live control artifacts, `docs/live/ideas.md` exists as durable exploration state, no runnable active sprint has been fabricated, and the next phase can truthfully choose initialization follow-up, brainstorm, or proposal from files alone.