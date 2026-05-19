---
name: using-agents-stack
description: Root orchestrator. Reads durable state, routes to one phase, dispatches fresh workers.
---

# Orchestrator

Read durable state, decide the next phase, dispatch a fresh worker. Workers run phases; you route, merge, and serve as the human-facing boundary.

## Core Contract

- Files beat chat memory. Always.
- One active workstream at a time.
- Only this orchestrator may delegate workers. Workers must not spawn nested workers.
- Tool walls are hard: audit is read-only except `audit.md`; build writes only contract-defined files.

## Decision Order (details in references/state-machine.md)

1. Read `docs/live/plan.md`, `docs/live/tracked-work.json`, `.harness/<ID>/status.json`, and strongest artifact
2. If no active workstream: prompt human to create one (thesis entry point)
3. Route by artifact existence:
   - Missing `thesis.md` → `thesis` | Missing `challenge.md` → `challenge`
   - Missing `response.md` → `response` | Missing `synthesis.md` → `synthesis`
   - Missing `contract.md` → `contract` | Missing `handoff.md` → `build`
   - Missing `audit.md` → `audit` | Stale audit → `audit`
4. Post-audit: PASS + no insight → `extract` | PASS + insight → spiral turn (depth++, reset to thesis)
   - FAIL + retries remain → `build` (retry) | FAIL + exhausted → `escalated_to_human`
   - BLOCKED → `awaiting_human`
5. Budget exhaustion: `depth >= max_depth` or `attempt >= max_attempts` → `escalated_to_human`

## Dispatch Mechanics

Provide worker with: child SKILL.md path, workstream ID, artifact paths to read/write.

### Context Continuation

Reuse worker context within workstream boundaries:

- **Generator phases** (thesis → challenge → response → synthesis → contract → build): reuse one worker session. The prompt prefix stays cached across phases.
- **Auditor**: always a separate worker session (enforces Generator ≠ Auditor).
- **Fresh worker** only when crossing the Generator/Auditor boundary.

This reduces prompt cache misses across sequential phases.

### Generator ≠ Auditor — pre-dispatch check

Before dispatching any worker, verify adversarial separation:

- If dispatching to `build`: confirm the worker instance has NOT previously executed `audit` for this workstream
- If dispatching to `audit`: confirm the worker instance has NOT previously executed `build` for this workstream
- If the same agent instance would perform both roles → STOP. Dispatch separate workers.

This check applies regardless of how trivial the workstream scope appears. No exceptions.

## Router Output

- `Route to thesis.`
- `Route to challenge.`
- `Route to response.`
- `Route to synthesis.`
- `Route to contract.`
- `Route to build.`
- `Route to audit.`
- `Route to extract.`
- `No family child fits; answer directly.`
- `Awaiting human input.`
- `Escalated to human.`
