# Progress

Read after `docs/live/current-focus.md` to recover the latest state, continuity, and hand-off details. Keep each section concise so the next session can resume quickly.

## Current State

The repo now has a repo-local AGENTS-governance skill at `.agents/skills/using-agents-md/SKILL.md`, and the root discovery pointer now truthfully routes AGENTS/doc-governance decisions to it.

## Latest Completed Work

- ran a read-only baseline pressure test that confirmed the repo lacked an explicit AGENTS-maintenance decision procedure and still pointed root startup guidance at a missing repo-local skill surface
- created `.agents/skills/using-agents-md/SKILL.md` as the narrow procedural guide for when to change `AGENTS.md`, `docs/reference/*`, `docs/live/*`, or a skill package
- updated root `AGENTS.md` so the project-local skills section points to `.agents/skills/using-agents-md/SKILL.md` instead of a stale missing path
- updated `docs/reference/{architecture,codemap,memory,lessons}.md` so the new skill path, durable policy split, and stale-root-pointer anti-pattern are preserved
- ran a post-skill verification task, fixed the only remaining ambiguity in the skill workflow (nearest-parent vs root discovery updates, plus rule-vs-procedure dual updates), and rechecked that the clarification passed
- verified whitespace cleanliness with `git diff --check`

## In Progress

None.

## Blockers

None.

## Next Recommended Action

Use `.agents/skills/using-agents-md/SKILL.md` for future repo AGENTS-hierarchy or doc-governance changes; no additional follow-up is required for this task.

## Touched Files

- `.agents/skills/using-agents-md/SKILL.md`
- `AGENTS.md`
- `docs/reference/architecture.md`
- `docs/reference/codemap.md`
- `docs/reference/memory.md`
- `docs/reference/lessons.md`
- `docs/live/progress.md`

## Verification Status

- baseline read-only pressure test (`task` subagent) found the missing AGENTS-governance procedure and stale root skill pointer before implementation
- post-skill verification (`task` subagent) confirmed the new discovery pointer and AGENTS/reference/live-doc split, then identified one workflow ambiguity that was fixed
- follow-up recheck (`quick_task` subagent) returned `pass` after the skill clarification
- `git diff --check`

## Hand-off Note

The repo-local AGENTS-governance surface is now in place and documented. No `docs/live/current-focus.md` update was needed because the active objective and scope did not change. No further reference-doc update is pending for this task.
