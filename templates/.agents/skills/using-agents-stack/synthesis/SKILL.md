---
name: synthesis
description: Synthesize tactical responses into a unified, self-consistent architectural framework.
trigger: When response.md exists and synthesis.md does not. Response MUST complete before synthesis.
inputs: [AGENTS.md, plan.md, thesis.md, challenge.md, response.md]
outputs: [.harness/<id>/synthesis.md, .harness/<id>/status.json]
boundaries: Synthesis only. May optionally delegate to oracle to verify self-consistency.
---

# Synthesis Worker

Extract common patterns from dispersed tactical solutions and form them into a unified framework. This is where "what we designed" becomes "why we designed it this way."

## Critical Rule

`response.md` MUST exist and be complete before synthesis begins. This order is enforced by the orchestrator. If `response.md` is missing, stop and report the violation.

## Input

The orchestrator provides inline context digest covering: plan objective, thesis claim, challenge gaps, all response designs, harness rules. Read from disk only if the inline digest is insufficient.

### Required Reads (fallback)

- `docs/live/plan.md`
- `.harness/<id>/thesis.md`, `challenge.md`, `response.md`

## Output: synthesis.md

```markdown
# Synthesis

## Design Philosophy
[2-4 principles that guided the synthesis]
1. 
2. 

## Core Primitives
[Named concepts and their relationships]
- **Primitive A**: [definition, role, relationships]
- **Primitive B**: [definition, role, relationships]

## Key Flows

### Normal Path
[How the system operates under normal conditions]

### Failure Recovery
[How the system handles each failure mode]

## Cross-Cutting Concerns
- **Security**: [injection points, boundaries]
- **Cost**: [budget model, thresholds]
- **Observability**: [what to monitor, what signals matter]
- **Recoverability**: [how state survives failure]

## Self-Consistency Check
[Does any part of this framework contradict another?]
- [If contradictions found: list them and state whether resolved]
```

## Optional Oracle Verification

If the framework is complex, dispatch oracle to verify internal consistency:
- Provide synthesis.md to oracle
- Ask: "Does any part of this framework contradict another? Are there hidden assumptions?"
- If oracle finds minor issues → fix in synthesis.md
- If oracle finds fundamental contradictions → mark synthesis incomplete and report for spiral turn

## Workflow

1. Read all prior artifacts (thesis → challenge → response)
2. Pattern-extract across responses: what repeats? what is the common shape?
3. Form design philosophy from patterns
4. Define primitives, flows, cross-cutting concerns
5. Self-consistency check (optional oracle verification)
6. Write `synthesis.md`
7. Update `status.json`: `phase: "synthesis"`

## Termination

- Framework self-consistent → synthesis complete, route to contract
- Fundamental contradictions → mark incomplete, orchestrator triggers spiral turn

## Done

`synthesis.md` exists with self-consistent framework.
