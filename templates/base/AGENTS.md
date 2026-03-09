# Project Agent Guide

## Repo Purpose

This repository uses a minimal agent documentation structure for recall, progressive disclosure, and reliable hand-off in a single worktree.

## Injected Context Contract

- Inject `AGENTS.md` at session start.
- Treat `AGENTS.md` as the only always-in-context index.
- Retrieve additional docs on demand from `docs/live/` and `docs/reference/`; do not preload the full docs set.

## Progressive Disclosure Rules

- Start here, then read only the smallest set of docs needed for the task.
- Read `docs/live/current-focus.md` for the active objective, scope, and constraints.
- Read `docs/live/progress.md` for session continuity, touched files, and latest verification.
- Read `docs/live/todo.md` only when selecting or sequencing next actions.
- Read `docs/reference/implementation.md` only for technical execution details.
- Read `docs/reference/design.md` only for product intent, UX, or behavior rules.

## Read Order by Task Type

- Start or resume work: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md`
- Pick the next task: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/live/todo.md`
- Implement or change behavior: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/implementation.md`
- Adjust product or UX behavior: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/design.md`
- Cross-cutting work: read both `docs/reference/implementation.md` and `docs/reference/design.md` after the live docs.

## Update Rules After Meaningful Work

- Update `docs/live/current-focus.md` when the active objective, scope, constraints, or success criteria change.
- Update `docs/live/progress.md` after meaningful work with current state, completed work, blockers, touched files, verification, and next recommended action.
- Update `docs/live/todo.md` when priorities or next actions change.
- Keep every update concise so the next session can recover state quickly.
