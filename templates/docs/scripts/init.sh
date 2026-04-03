#!/usr/bin/env sh
set -eu

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
ensure_dir "docs/reference"
ensure_dir "docs/scripts"

write_file_if_missing "docs/live/features.json" '{
  "project": "Replace with project name",
  "idea_backlog_path": "docs/live/ideas.md",
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

`docs/live/features.json` remains the authoritative tracked-work ledger. Use that file to track backlog truth, runnable state, and the single runnable active sprint.

## Promotion guide
- create or update exactly one backlog entry in `docs/live/features.json`
- assign a stable `id`, `title`, `summary`, `priority`, and `dependencies`
- use `status: "needs_brainstorm"` when the item is tracked but still needs ideation before proposal
- use `status: "pending"` only when the item is ready for proposal
- add a pointer back to this file or section if the tracked-work schema supports it
- do not set `runnable_active_sprint_id`
- do not open `.harness/<feature-id>/`

## Idea entry template
### IDEA-TEMPLATE: Working title
- Related feature id: none yet | FEAT-000
- Current state: exploring | needs_brainstorm | ready_to_promote | parked | rejected
- Problem statement:
- Why now:
- Constraints and dependencies:
- Rejected or risky directions:
- Open questions:
- Promotion signal:
'

write_file_if_missing "docs/live/progress.md" '# Project Progress Ledger

Record dated sprint outcomes here. Append new entries; do not rewrite history.
'

write_file_if_missing "docs/live/memory.md" '# Durable Project Memory

Capture stable repo truths, environment quirks, and lessons future agents should reuse.
'

write_file_if_missing "docs/reference/architecture.md" '# Architecture Reference

Describe the current runtime, entrypoints, and major subsystem boundaries.
'

write_file_if_missing "docs/reference/design.md" '# Design Reference

Describe the current UX intent, visual system, and product constraints.
'