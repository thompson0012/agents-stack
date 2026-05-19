# AGENTS.md

This repository uses the agents-stack harness — a stateful, resumable, adversarial framework.

## Key Paths

- `.harness/<ID>/` — workstream artifacts (thesis.md, challenge.md, response.md, synthesis.md, contract.md, handoff.md, audit.md, status.json)
- `docs/live/plan.md` — resume anchor: Why, What, Next, cross-workstream Lessons
- `docs/live/tracked-work.json` — active/parked workstream registry
- `.agents/skills/using-agents-stack/` — router SKILL.md, phase SKILL.md files, references

## Three Layers

| Layer | Question | Phases | Output |
|-------|----------|--------|--------|
| **Direction** | What are we understanding? | thesis → challenge | thesis.md, challenge.md |
| **Method** | How do we respond to gaps? | response → synthesis | response.md, synthesis.md |
| **Action** | What do we build to verify? | contract → build → audit | contract.md, handoff.md, audit.md |

Layers proceed sequentially. Action layer may trigger a spiral turn back to Direction at greater depth.

## Core Invariants

1. **Files beat chat memory.** Durable artifacts are state. Conversation is not.
2. **One active workstream.** At most one workstream is non-parked at any time.
3. **Generator ≠ Auditor.** Build and audit must be separate agent instances.
4. **Artifact precedence.** `audit.md > handoff.md > contract.md > phase artifacts > status.json > tracked-work.json > plan.md`
5. **Depth and attempt are independent.** `depth` tracks understanding layers. `attempt` tracks execution retries.
6. **Cold start must work.** A new agent must recover full state from files alone.

## State

- `docs/live/plan.md` — resume anchor: Why, What, Next, and cross-workstream Lessons.
- `docs/live/tracked-work.json` — workstream registry: active, parked, per-workstream metadata.
- `.harness/<ID>/status.json` — per-workstream checkpoint: depth, layer, phase, attempt, max, blocked_reason.

## Orchestrator-Worker Model

- The root router (`using-agents-stack`) is the only orchestrator. It reads state, routes, dispatches workers, merges results.
- Workers run one phase each, in their own context. Workers must not spawn nested workers.
- Dispatch: provide worker with SKILL.md path + workstream ID + artifact paths. No elaborate formalism.
- **Generator ≠ Auditor pre-dispatch check:** Build and audit must be dispatched to separate worker instances. Same instance for both roles is always a violation.

## Routing Overview

Routes are layer-internal, layer-to-layer, or spiral-turn. The orchestrator checks which artifacts exist to decide the next phase. Detailed routing table: `.agents/skills/using-agents-stack/SKILL.md` (Decision Order section) and `.agents/skills/using-agents-stack/references/state-machine.md`.

## Quick Resume

1. Read `AGENTS.md`, `docs/live/plan.md`, `docs/live/tracked-work.json`
2. Read `.harness/<ID>/status.json` and the strongest artifact (by precedence)
3. Verify checkpoint matches disk state, continue from strongest valid checkpoint

## Success Condition

The harness is healthy when a cold-start agent can read the files above and continue safely without any chat history.
