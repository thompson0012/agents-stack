---
title: Patch templates, not just local project copies — systemic fix over local fix
type: correction
source: agents-stack-improvement-session
trigger: When improving agents-stack workflow rules, gates, or skills. Before modifying any skill file, check whether it exists in agents-stack/templates/ and patch that instead.
---

## What happened

After identifying three systemic improvements to agents-stack (baseline-before-parallel rule, integration gate, fresh session requirement), I applied all patches to arc's local `.agents/skills/using-agents-stack/` copies. The user corrected me: "你應該改agents-stack的templates."

The templates at `agents-stack/templates/` are the source that `init.sh` copies into new projects. By patching only arc's copies, I fixed the symptom for one project but left the root cause — stale templates — untouched for all future projects.

## Root cause

Two factors:

1. **Optimized for the immediate context**: I was working inside arc's directory, so arc's skill files were the natural target. I didn't zoom out to ask "where does this ultimately come from?"

2. **Same pattern as the original error**: The parallel-fixers-over-discipline problem repeats at a meta level — quick local fix over systemic fix. The agent's efficiency bias prioritizes the visible problem (arc's broken process) over the invisible one (stale templates).

## Prevention rule

Before modifying any agents-stack skill file, always check three locations and patch all that need updating:

| Priority | Location | Why |
|----------|----------|-----|
| 1 | `agents-stack/.agents/skills/using-agents-stack/` (live) | Used by agents-stack itself when routing |
| 2 | `agents-stack/templates/.agents/skills/using-agents-stack/` (templates) | Propagates to all new projects via init.sh |
| 3 | `<project>/.agents/skills/using-agents-stack/` (project copies) | Needed if project was initialized before the template was updated |

The question to ask before any patch: **"Does this fix the source, or just one symptom?"**

## Related

- `2026-05-22--parallel-efficiency-vs-pipeline-discipline.md`
- `agents-stack/templates/.agents/skills/using-agents-stack/`
