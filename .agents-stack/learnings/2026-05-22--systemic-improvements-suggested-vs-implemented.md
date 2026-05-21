---
title: Systemic improvements — five suggestions, two implemented, three deferred
type: insight
source: agents-stack-improvement-session
trigger: When proposing workflow/process improvements, always track which suggestions were accepted, which were deferred, and why. The gap between "suggested" and "implemented" is itself a learning.
---

## What happened

In a single improvement session, five systemic changes to agents-stack were proposed to solve the recurring "parallel efficiency over pipeline discipline" problem:

| # | Suggestion | Implemented? | Where |
|---|-----------|-------------|-------|
| 1 | **Baseline before parallel** — ranking rule in Core Contract | ✅ | `using-agents-stack/SKILL.md` |
| 2 | **@fixer job prompt template** — mandatory RED/GREEN/VERIFY steps in spawn template | ❌ Deferred | — |
| 3 | **Integration gate** — zero-caller scan + cross-module wiring check between implement and qa | ✅ | `implement/SKILL.md` + `qa/SKILL.md` |
| 4 | **Success metric change** — "tests passing, E2E running, ACs verified" not "files written" | ❌ Deferred | — |
| 5 | **Work classification** — Greenfield / Iteration / Bug fix with different pipeline requirements | ❌ Deferred | — |

Additionally, the 0.1% rule was added (not in the original 5) as a parallel to superpowers' 1% rule.

## Root cause

Three patterns explain the gap:

1. **Effort/reward heuristic**: #1 (one-line rule) and #3 (add section to existing SKILL.md) were cheap. #2 (fixer prompt template) and #5 (classification logic) require deeper changes to agent dispatch mechanics. #4 (success metric) touches status.json schema, which has downstream effects.

2. **Patch bias**: The agent naturally implements what's quickest and most visible. The harder changes (#2, #5) require tooling changes outside SKILL.md files, which have higher activation energy.

3. **No explicit tracking of deferred items**: Suggestions #2, #4, #5 were acknowledged as valuable but never recorded as pending work. They exist only in conversation memory — which violates agents-stack invariant #1 (files beat chat memory).

## Prevention rule

When proposing a set of improvements, explicitly track the disposition of each item:

```
| Suggestion | Priority | Effort | Status |
|------------|----------|--------|--------|
| ... | high/med/low | small/med/large | ✅ implemented / ⏳ deferred / ❌ rejected |
```

Deferred items must be recorded somewhere durable — either as a `.agents-stack/learnings/` entry, a tracked-work.json backlog item, or a TASK-0 in the next workstream. Conversation memory is not durable state.

## Related

- `2026-05-22--parallel-efficiency-vs-pipeline-discipline.md`
- `2026-05-22--patch-templates-not-just-local-copies.md`
- `using-agents-stack/SKILL.md`
- `using-agents-stack/implement/SKILL.md`
- `using-agents-stack/qa/SKILL.md`
