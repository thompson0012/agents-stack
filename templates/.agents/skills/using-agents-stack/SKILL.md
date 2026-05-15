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

## Decision Order

1. Read `docs/live/plan.md` and `docs/live/tracked-work.json`
2. If no active workstream exists: prompt human to create one (thesis is the entry point for new work)
3. If active workstream exists, read `.harness/<ID>/status.json` and strongest artifact

### Layer-internal routing

**Direction Layer:**
- No `thesis.md` → route `thesis`
- `thesis.md` exists, no `challenge.md` → route `challenge`
- `challenge.md` exists, translation needed → route translation (append to challenge.md)
- `challenge.md` exists, no translation needed → enter Method Layer

**Method Layer:**
- No `response.md` → route `response`
- `response.md` exists, no `synthesis.md` → route `synthesis`
- `synthesis.md` exists → enter Action Layer

**Action Layer:**
- No `contract.md` → route `contract`
- `contract.md` exists, no `handoff.md` → route `build`
- `handoff.md` exists, no `audit.md` → route `audit`
- `audit.md` exists → evaluate outcome

### Post-audit routing

- PASS + no deeper insight → route `extract`
- PASS + deeper insight → spiral turn: `depth++`, reset layer/phase to thesis
- FAIL + `attempt < max_attempts` + clean restore → route `build` (retry)
- FAIL + `attempt >= max_attempts` → `escalated_to_human`
- BLOCKED → `awaiting_human`

### Post-extract routing

After extract completes:
- `extract.md` exists → archive (update tracked-work.json + plan.md directly)

### Budget exhaustion

- `depth >= max_depth` → `escalated_to_human`
- `attempt >= max_attempts` → `escalated_to_human`

## Dispatch Mechanics

Provide worker with: child SKILL.md path, workstream ID, artifact paths to read/write. Fresh worker, clean context.

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
