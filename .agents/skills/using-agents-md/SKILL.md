---
name: using-agents-md
description: Use when adding, removing, moving, or updating repo guidance boundaries and you need to decide whether `AGENTS.md`, `docs/reference/*`, `docs/live/*`, or a repo-local skill should change.
---

# Using AGENTS.md

## Overview
`AGENTS.md` defines operating rules for a durable boundary. It is not a progress log, design spec, or memory dump.

## Quick Reference

| Change | Update |
| --- | --- |
| New subtree with durable, non-obvious local rules | Add a local `AGENTS.md` in that folder |
| Existing boundary, read order, or local rules changed | Update the owning `AGENTS.md` |
| Durable truth, policy, path, invariant, or lesson changed | Update `docs/reference/*` |
| Session objective, progress, todo, blocker, or verification changed | Update `docs/live/*` |
| Repeatable procedure is needed beyond static repo policy | Add or update a skill package |

## Add a Local `AGENTS.md` Only When the Boundary Earns It
Add a new local `AGENTS.md` only if all of these are true:
- multiple files in the subtree share the same local operating rules
- those rules differ materially from the parent guidance
- the subtree is a durable boundary another agent will re-enter later

Do not add a local `AGENTS.md` for a single file, a transient task folder, or a leaf that has no distinct long-lived contract.

## Workflow
1. Read the root `AGENTS.md`, then the nearest existing local `AGENTS.md` files for the subtree you are touching.
2. Decide whether the change affects boundary rules or only durable truth/session state.
3. If the boundary changed, update the owning `AGENTS.md`. If you created a new durable boundary, add a local `AGENTS.md` there.
4. In the same change, update the nearest parent discovery/index surface. If the startup path or a high-value repo entrypoint changed, update the root `AGENTS.md` and `docs/reference/codemap.md` too.
5. Run the reference writeback gate:
   - `architecture.md` for boundaries and invariants
   - `codemap.md` for high-value paths and entrypoints
   - `memory.md` for durable decisions and policy
   - `lessons.md` for reusable mistakes or anti-patterns
6. If the durable rule changed and the repeatable procedure changed, update both the relevant `docs/reference/*` file and the skill package in the same change.
7. If no `AGENTS.md` or `docs/reference/*` update is needed, say so explicitly before yielding.

## Common Mistakes
- putting progress, blockers, or hand-off notes in `AGENTS.md`
- adding leaf `AGENTS.md` files that do not own a real boundary
- changing local guidance without updating the nearest parent discovery/index surface, and the root entrypoints when the startup path changed
- updating only `memory.md` or only the skill when the durable rule and the repeatable procedure both changed
- duplicating durable reference-doc content or live-doc state inside `AGENTS.md`
- creating a new skill when the rule belongs in `AGENTS.md` or `docs/reference/*` instead
