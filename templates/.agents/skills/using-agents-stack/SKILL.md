---
name: using-agents-stack
description: Root orchestrator. Reads durable state, routes to one phase, dispatches fresh workers.
---

# Orchestrator — Goal-QA-Driven v3

Read durable state from .agents-stack/, decide the next phase, dispatch a fresh worker. Workers run phases; you route, merge, and serve as the human-facing boundary.

## Core Contract

- Files beat chat memory. Always.
- One active workstream at a time.
- Only this orchestrator may delegate workers. Workers must not spawn nested workers.
- Tool walls are hard: qa is read-only except qa-report.md; implement writes only task-defined files.

## Pacing Discipline

When guiding through phases, add exactly one structural dimension per round. Do not mix concerns within a single round:

| Round | Dimension | Output |
|-------|-----------|--------|
| 1 | **Alignment** — confirm understanding of the spec | Spec coverage checklist, boundary confirmation |
| 2 | **Structure** — order of work, dependency relationships | Phase ordering, dependency graph |
| 3 | **Contract** — verification terms, deliverables, checkpoints | 5-dimension task verification matrix |
| 4+ | **Execution** — implement one task at a time | Code, passing tests |

Never merge rounds. Round 1 must not produce architecture. Round 2 must not produce verification checkpoints. Round 3 must not produce code. This prevents the confusion that comes from addressing scope, order, quality, and implementation simultaneously.

## Decision Order (details in references/state-machine.md)

1. Read `.agents-stack/tracked-work.json`, `.agents-stack/<ID>/status.json`, and strongest artifact
2. If no active workstream: prompt human to create one (spec entry point)
3. Route by artifact existence:
   - Missing `spec.md` → `spec` | Missing `plan.md` → `plan`
   - Missing `tasks.md` → `tasks` | Missing `handoff.md` → `implement`
   - Missing `qa-report.md` → `qa` | QA_PASS → `release`
4. Post-QA:
   - PASS → `release`
   - FAIL + Layer 1 + attempts remain → `implement` (retry)
   - FAIL + Layer 2 → `plan` (re-plan)
   - FAIL + Layer 3 → `spec` (re-spec)
   - BLOCKED → `awaiting_human`
5. Budget exhaustion: `depth >= max_depth` or `attempt >= max_attempts` → `escalated_to_human`

## Dispatch Mechanics

Provide worker with: child SKILL.md path, workstream ID, artifact paths to read/write.

### Generator ≠ Auditor — pre-dispatch check

Before dispatching any worker, verify adversarial separation:
- If dispatching to `implement`: confirm the worker instance has NOT previously executed `qa` for this workstream
- If dispatching to `qa`: confirm the worker instance has NOT previously executed `implement` for this workstream
- If the same agent instance would perform both roles → STOP. Dispatch separate workers.

### Context Continuation

Reuse worker context within workstream boundaries:
- **Generator phases** (spec → plan → tasks → implement): reuse one worker session
- **Verifier** (qa): always a separate worker session
- **Release**: can reuse generator context since it's post-verification

## Three-Layer Rework Routing

When QA returns FAIL with layer assessment:
- L1: route to `implement` — same contract, mark affected task as [↩] reworking
- L2: route to `plan` — update plan.md, then regenerate tasks, then re-implement
- L3: route to `spec` — update spec.md, then re-plan, re-task, re-implement

## Router Output

- `Route to spec.`
- `Route to plan.`
- `Route to tasks.`
- `Route to implement.`
- `Route to qa.`
- `Route to release.`
- `Awaiting human input.`
- `Escalated to human.`
