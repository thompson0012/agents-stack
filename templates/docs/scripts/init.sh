#!/usr/bin/env sh
set -eu

# Fresh scaffold invariants:
# - new projects start with no active or parked sprint and no archive history
# - `.harness/` and `docs/archive/` stay empty until real work creates artifacts
# - the files written below are the canonical blank defaults for copied scaffolds
# - keep `templates/docs/live/*` and `templates/docs/reference/*` aligned with these defaults

ensure_dir() {
  dir="$1"
  if [ ! -d "$dir" ]; then
    mkdir -p "$dir"
    printf 'created %s\n' "$dir"
  fi
}

write_file_if_missing() {
  path="$1"
  content="$2"

  if [ -e "$path" ]; then
    printf 'kept %s\n' "$path"
    return
  fi

  parent=$(dirname "$path")
  ensure_dir "$parent"
  printf '%s' "$content" > "$path"
  printf 'created %s\n' "$path"
}

ensure_dir ".agents/skills/using-agents-stack"
ensure_dir ".harness"
ensure_dir "docs/archive"
ensure_dir "docs/live"
ensure_dir "docs/records"
ensure_dir "docs/reference"
ensure_dir "docs/scripts"

write_file_if_missing "docs/live/tracked-work.json" '{
  "project": "Replace with project name",
  "idea_backlog_path": "docs/live/ideas.md",
  "current_focus_path": "docs/live/current-focus.md",
  "roadmap_path": "docs/live/roadmap.md",
  "records_root_path": "docs/records/",
  "single_runnable_active_sprint": true,
  "runnable_active_sprint_id": null,
  "parked_sprint_ids": [],
  "compound_pending_feature_ids": [],
  "backlog": []
}'

write_file_if_missing "docs/live/ideas.md" '# Live Idea Backlog

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
'

write_file_if_missing "docs/live/current-focus.md" '# Current Focus

This file is a live resume anchor. It is not a second contract.

- Current objective: Establish the first truthful source goal, roadmap, and backlog state for this repo.
- Source-goal lineage: No durable source goal is recorded yet.
- Current roadmap phase: Unset. Record the real source goal in `docs/live/roadmap.md` before proposing sprint work.
- Next owner: `project-initializer`, or the next human or agent establishing durable state.
- Next file to open: `docs/live/roadmap.md`
- Contract truth: If a sprint is later opened, `.harness/<feature-id>/contract.md` becomes the only runnable sprint contract.
'

write_file_if_missing "docs/live/roadmap.md" '# Initiative Roadmap

This file is the non-runnable roadmap for broader goals. It does not select the runnable sprint; `docs/live/tracked-work.json` still does that.

- Source goal: Not recorded yet. Replace this line with the real user or repo objective.
- Current slice: None selected yet.
- Ordered remaining slices/phases:
  1. Record the source goal and any real constraints.
  2. Add the first bounded backlog item to `docs/live/tracked-work.json` when one is justified.
  3. Open proposal work only after one dependency-ready item is honestly `pending`.
- Stop or re-authorization condition: Stop when no bounded next slice is justified from repo facts or user direction. Re-authorize before inventing more roadmap.
- Visible remaining-work summary: No runnable sprint is selected, no parked sprint is recorded, and the backlog is empty until real tracked work exists.
'

write_file_if_missing "docs/live/progress.md" '# Project Progress Ledger

Record dated sprint outcomes here. Append new entries; do not rewrite history.

Use this ledger for durable audit events, not as a second registry. `docs/live/tracked-work.json` remains the tracked-work source of truth.

Record transitions such as:
- sprint start, pause, escalation, build failure, review failure, PASS archive cutover, and next-action decisions
- record creation in `docs/records/*`
- record promotion into `docs/reference/*`
- record supersession or expiry, with replacement path when one exists

When a record event is tied to tracked work, name the workstream id, record path, and evidence path that justifies it.

## Entry template
- YYYY-MM-DD - EVENT - Workstream: WORKSTREAM-### | none - Paths: `docs/records/...`, `docs/reference/...`, `.harness/...`, or `docs/archive/...` - Notes: brief factual summary
'

write_file_if_missing "docs/records/README.md" '# Durable Records

Use this folder for durable feature or decision pages created from a sprint, review, or scoped discussion when the material should survive chat loss but is not the active contract, not immutable archive evidence, and not stable project-wide reference truth.

## What belongs here
- feature-local decision notes, investigation summaries, tradeoff writeups, or handoff context that remain useful after the sprint
- sprint or discussion output that needs durable traceability but is too situational for `docs/reference/*` and too interpreted for `docs/archive/*`
- pages tied to a tracked workstream id and registered from that feature entry through `record_paths`

## What does not belong here
- active sprint contracts, proposals, runtime logs, reviews, or status files
- copied archive evidence from `.harness/<WORKSTREAM-ID>/` or `docs/archive/<WORKSTREAM-ID>_<timestamp>/`
- current project-wide truth that belongs in `docs/reference/*`
- untracked ideas; keep those in `docs/live/ideas.md` until a feature id exists

## Page metadata and backlinks
At the top of each record, include:
- `feature_id`: owning tracked feature, when one exists
- `scope`: what question, slice, or discussion window this page covers
- `status`: current validity such as `informative`, `promoted`, `superseded`, or `expired`
- `superseded_by`: replacement record or reference path, if any
- `idea_ref`: originating idea section or durable discussion pointer, if any
- `evidence_path`: one canonical evidence path for the current supporting sprint evidence
- `reference_paths`: stable reference pages that absorbed durable truth from this record
- `sprint_contributions`: sprint folders or feature ids that materially informed the page
- `archive_contributions`: archive folders that preserve cited PASS evidence

Backlink rules:
- register the page path under the owning feature entry `record_paths`
- link back to the current `evidence_path` for the supporting sprint
- when content becomes stable current truth, promote that truth into `docs/reference/*`, update `reference_paths`, and leave this record as provenance
- when content is replaced or no longer valid, update `status` and `superseded_by` instead of deleting history
'

write_file_if_missing "docs/live/memory.md" '# Durable Project Memory

Capture stable repo truths, environment quirks, and lessons future agents should reuse.
'

write_file_if_missing "docs/reference/architecture.md" '# Architecture Reference

Describe the project-specific runtime, entrypoints, major subsystem boundaries, integration boundaries, and orchestration rules.
'

write_file_if_missing "docs/reference/design.md" '# Design Reference

Describe the project-specific product intent, interaction model, visual system, and notable constraints.
'