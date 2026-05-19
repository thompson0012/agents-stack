# agents-stack state machine

Durable phase model for the harness. The orchestrator reads these rules, decides the next phase, dispatches a fresh worker.

## Core Invariants

- Exactly one workstream active at a time. Additional workstreams must be parked.
- Parked workstreams (`awaiting_human`, `escalated_to_human`) remain visible but are not active.
- Files are state. Chat memory is not durable.
- Orchestrator routes and dispatches. Workers execute one phase each. Workers must not spawn other workers.
- Generator ≠ Auditor. Build and audit are independent workers.

## Artifact Precedence

1. `audit.md`
2. `handoff.md`
3. `contract.md`
4. `thesis.md` / `challenge.md` / `response.md` / `synthesis.md` (equal weight within layer)
5. `status.json`
6. `docs/live/tracked-work.json`
7. `docs/live/plan.md`

When files disagree, the higher-precedence artifact wins.

## Layer Model

| Layer | Phases | Purpose |
|-------|--------|---------|
| Direction | thesis, challenge | Understand the problem, form and test claims |
| Method | response, synthesis | Design solutions, unify into framework |
| Action | contract, build, audit | Define scope, implement, verify |

Layers proceed sequentially. The Action layer can trigger a spiral turn back to Direction at greater depth.

## Phase Table

| Phase | Evidence | Owner | Next Step |
|-------|----------|-------|-----------|
| `uninitialized` | Missing or empty `tracked-work.json` | Human + orchestrator | Create first workstream |
| `thesis` | `thesis.md` exists | thesis worker | Challenge the thesis |
| `challenge` | `challenge.md` exists | challenge worker | Translation gate or response |
| `translation` | Appended to `challenge.md` | orchestrator (or specialist) | Re-check comprehension gate |
| `response` | `response.md` exists | response worker | Synthesis |
| `synthesis` | `synthesis.md` exists | synthesis worker | Contract |
| `contract` | `contract.md` exists | contract worker | Build |
| `build` | `handoff.md` exists | build worker | Audit (or build_failed) |
| `audit` | `audit.md` exists | audit worker | Archive or spiral turn |
| `build_failed` | `handoff.md` or `status.json` records failure | orchestrator | Retry (if attempts remain) |
| `awaiting_human` | `status.json` with `blocked_reason` | Human | Resume after human action |
| `escalated_to_human` | `status.json` with `blocked_reason` | Human | Human decision required |
| `archived` | Evidence in `docs/archive/` | — | Next workstream |

## Transition Rules

### Direction Layer

- No thesis → route `thesis`
  - thesis worker reads plan.md, prior synthesis/audit (if spiral turn), forms a falsifiable claim
- thesis exists, no challenge → route `challenge`
  - challenge worker delegates to oracle (single) or council (multi-model) for architectural judgment
- challenge exists → check comprehension gate
  - if translation needed: append translation to challenge.md, re-check
  - if clear: route `response`

### Method Layer

- challenge clear, no response → route `response`
  - response worker designs one concrete solution per gap in challenge
- response exists, no synthesis → route `synthesis`
  - synthesis worker unifies responses into coherent framework
  - optional oracle verification of self-consistency
  - if contradictions are fundamental: mark incomplete (orchestrator triggers spiral turn)

### Action Layer

- synthesis exists, no contract → route `contract`
  - contract worker defines buildable scope with hard file boundaries
- contract exists, no handoff → route `build`
  - build worker implements contract, records reproducible evidence
  - build/startup triage required before handoff
  - if build/startup fails: `build_failed`
- handoff exists, no audit → route `audit`
  - audit worker independently reproduces and judges
  - verdict: PASS, FAIL, or BLOCKED
  - assess: does this reveal a deeper thesis flaw? (spiral turn trigger)
- handoff exists, audit exists but `last_audited_attempt < attempt` → route `audit` (stale audit)
- audit exists with `last_audited_attempt == attempt` → evaluate outcome

### Post-Audit

- PASS + no deeper insight → archive
  - orchestrator moves evidence to `docs/archive/`
  - updates `tracked-work.json` (clear active, update evidence_path)
  - appends lessons to `plan.md`
- PASS + deeper insight → spiral turn
  - `depth++`
  - reset layer to Direction, phase to thesis
  - prior synthesis + audit become evidence for new thesis
- FAIL + `attempt < max_attempts` + clean restore → route `build` (retry)
- FAIL + `attempt >= max_attempts` → `escalated_to_human`
- BLOCKED → `awaiting_human`

### Budget Exhaustion

- `depth >= max_depth` → `escalated_to_human`
- `attempt >= max_attempts` → `escalated_to_human`

## Comprehension Gate

After challenge produces a verdict:
- Assess: is the judgment understandable to downstream (human or agent)?
- If not: append a translation section to challenge.md (narrative, analogy, scenario walkthrough)
- Re-check. Repeat until clear.
- Translation changes form, not content.

## Spiral Turn vs Retry

| | Spiral Turn | Retry |
|---|---|---|
| Counter | `depth++` | `attempt++` |
| Scope | New thesis, new contract | Same contract |
| Trigger | Deeper assumption flaw found | Implementation/verification failure |
| Resets to | thesis (Direction layer) | build (Action layer, same contract) |

## Contradiction Handling

When files disagree:
- Trust the strongest artifact by precedence
- If contradiction prevents single routing decision → `awaiting_human`
- Never invent a winner when evidence is genuinely split
