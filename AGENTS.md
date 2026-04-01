# Project Agent Guide

## Repo Purpose

This repository uses a minimal agent documentation structure for recall, progressive disclosure, and reliable hand-off in a single worktree.

## Task Execution Priority

**SKILLS TAKE PRECEDENCE OVER MODEL KNOWLEDGE.**

Before ANY response or action, answer this question aloud:

> **What skill should I activate for this task?**

Execution order:
1. **SKILLS FIRST** — If a skill exists for the task type, invoke it before doing anything else
2. **Project-Local Skills** — Check `.agents/skills/` for repository-specific guidance
3. **User Skills** — Check `~/.agents/skills/` for user-installed capabilities
4. **Model Knowledge** — Use as fallback only when no skill applies

### Skill Check Protocol

| Before | After |
|--------|-------|
| "I'll just implement this..." | STOP → "Which skill applies? What does it say?" |
| "This is straightforward..." | STOP → "Is there a skill that could improve the approach?" |
| "I know how to do this..." | STOP → "Does a skill mandate a specific workflow?" |
| "Let me read files first..." | STOP → "Does a skill tell me HOW to explore?" |

### Mandatory Skill Invocation

If you think there is even a **1% chance** a skill might apply, you **MUST** invoke it to check.

When a skill is invoked:
1. Announce: `"Using [skill-name] for [purpose]..."`
2. Read the skill content via the `skill` tool
3. Follow the skill's workflow exactly
4. Proceed with the skill's guidance as your primary method

### Red Flags

These thoughts indicate you are rationalizing away skill usage:

| Rationalization | Reality |
|-----------------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE gathering information. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Skills provide structure. Use them. |
| "This doesn't need a formal skill" | If a skill exists for it, use it. |
| "I remember this skill" | Skills evolve. Read the current version. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |

## Injected Context Contract

- Inject `AGENTS.md` at session start.
- Treat `AGENTS.md` as the only always-in-context index.
- Retrieve additional docs on demand from `docs/live/` and `docs/reference/`; do not preload the full docs set.

## Project-Local Skills

- **ALWAYS** check `.agents/skills/` FIRST when a task type might have repository-specific guidance.
- Read `.agents/skills/using-labs21-suite/SKILL.md` as the router index whenever the right project-local skill or family router is not obvious.
- Use the most specific relevant skill available; do not fall back to model knowledge when a skill exists.
- Read only the smallest relevant skill or subdirectory needed for the task; do not preload the entire project skill tree.

## Progressive Disclosure Rules

- Start here, then read only the smallest set of docs needed for the task.
- Read `docs/live/current-focus.md` for the active objective, scope, and constraints.
- Read `docs/live/progress.md` for session continuity, touched files, latest verification, and the next recommended action.
- Use `docs/live/progress.md`'s `Next Recommended Action` as the default resume pointer unless user direction or `docs/live/current-focus.md` overrides it.
- Use `docs/live/progress.md`'s `Verification Status` before claiming completion or resuming work in a previously touched area.
- Read `docs/live/todo.md` only when selecting or sequencing among multiple plausible next actions, or when `docs/live/progress.md` does not already make the next step clear.
- Read `docs/reference/codemap.md` when you need to find where to work, identify likely entrypoints, or map a subsystem.
- Read `docs/reference/architecture.md` when system boundaries, invariants, or component relationships matter.
- Read `docs/reference/implementation.md` only for technical execution details.
- Read `docs/reference/design.md` only for product intent, UX, or behavior rules.
- Read `docs/reference/memory.md` for durable decisions, policies, or truths that should survive beyond the current task.
- Read `docs/reference/lessons.md` after mistakes, failed attempts, or surprising outcomes worth reusing.

## Read Order by Task Type

- Start or resume work: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md`
- Pick the next task: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/live/todo.md` when prioritization is still needed
- Find where to work: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/codemap.md`
- Implement or change behavior: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/implementation.md`
- Adjust product or UX behavior: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/design.md`
- Understand system boundaries before changing behavior: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/architecture.md`
- Recover durable decisions or repo truths: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/memory.md`
- Learn from prior mistakes or failed attempts: `AGENTS.md` → `docs/live/current-focus.md` → `docs/live/progress.md` → `docs/reference/lessons.md`
- Cross-cutting work: read `docs/reference/architecture.md` first, then `docs/reference/implementation.md` and `docs/reference/design.md` as needed after the live docs.

## Pre-Implementation Alignment Check

Before writing code or creating files, answer these questions aloud:

1. **Objective Match**: Which line in `docs/live/current-focus.md` Objective defines this work?
2. **Scope Boundary**: Which "Explicitly Out of Scope" item prevents something I might otherwise do?
3. **Minimal Change**: What's the smallest change that achieves the objective?

If you cannot answer all three with specific references, read `docs/live/current-focus.md` again.

## Drift Detection During Implementation

If any of these occur, pause and re-read `docs/live/current-focus.md`:

- Implementation requires creating files not listed in Scope
- You're editing files outside the touched-files history in `docs/live/progress.md`
- A "small fix" has expanded to touch 3+ additional files
- You're adding "helpful" features not requested in the objective

State aloud: "This work [is|is not] in scope because [specific reason]."

## Update Rules After Meaningful Work

- Update `docs/live/current-focus.md` when the active objective, scope, constraints, or success criteria change.
- Update `docs/live/progress.md` after meaningful work with current state, completed work, blockers, touched files, verification, and next recommended action.
- Update `docs/live/todo.md` when priorities or next actions change.
- Update `docs/reference/architecture.md` when boundaries, invariants, or major component relationships change.
- Update `docs/reference/codemap.md` when high-value paths, entrypoints, or subsystem locations change materially.
- Update `docs/reference/memory.md` when a decision, policy, or truth should persist beyond the current session.
- Update `docs/reference/lessons.md` when a mistake, anti-pattern, failed attempt, or hard-won fix is worth preserving.
- Keep every update concise so the next session can recover state quickly.

## Reference Writeback Gate
- Before yielding after meaningful work, explicitly decide whether any `docs/reference/*` file must change; do not leave this to user prompting or memory.
- If the change introduces or revises a durable default, policy, packaging rule, routing rule, or repo truth, update `docs/reference/memory.md`.
- If the change introduces or revises a reusable mistake pattern, false start, migration regret, anti-pattern, or hard-won fix, update `docs/reference/lessons.md`.
- If the change alters system boundaries, family ownership, component relationships, or other invariants, update `docs/reference/architecture.md`.
- If the change alters high-value entrypoints, package locations, router locations, or where a subsystem lives, update `docs/reference/codemap.md`.
- If none of those files need changes, state that conclusion explicitly in your working notes before completion: `No reference-doc update needed because ...`.
- Path-based default: if you changed skill packages, router metadata, or package layout under `.agents/skills/`, assume a `docs/reference/*` review is required and write down why each relevant reference doc did or did not change.