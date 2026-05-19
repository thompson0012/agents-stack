---
name: challenge
description: Adversarially test a thesis by delegating to oracle or council specialists.
trigger: When thesis.md exists but challenge.md does not.
inputs: [AGENTS.md, plan.md, thesis.md]
outputs: [.harness/<id>/challenge.md, .harness/<id>/status.json]
boundaries: Read-only except challenge.md. MUST delegate architectural judgment — do not judge inline.
---

# Challenge Worker

Attack the thesis. The question is not "is this right?" — it is "under what conditions does this hold, and under what conditions does it fail?"

## Input

The orchestrator provides inline context digest covering: plan objective, thesis claim, harness rules. Read from disk only if the inline digest is insufficient.

### Required Reads (fallback)

- `docs/live/plan.md`
- `.harness/<id>/thesis.md`
- Any prior evidence from spiral turns

## Delegation Rule

You MUST delegate architectural judgment. You are the coordinator — the oracle or council produces the structured verdict. You write it into `challenge.md`.

- **oracle**: deep single-model architectural review. Use for well-scoped theses.
- **council**: multi-model consensus synthesis. Use for high-risk or ambiguous theses.

Dispatch the specialist with: thesis.md contents + instruction to produce a structured verdict.

## Output: challenge.md

```markdown
# Challenge

## Thesis Under Review
[Link or summary of thesis.md]

## Delegation
- Method: [oracle | council]
- Rationale: [why this method]

## Verdict
[Structured judgment from oracle/council]

### Where It Holds
[Conditions and contexts where the thesis is valid]

### Where It Breaks
[Irreducible differences — where the thesis fails]

### Category Assessment
[Conceptual vs production applicability]

### Blind Spots
[What the thesis does not address]

## Comprehension Gate
- translation_needed: [true | false]
- barrier_type: [abstraction_level | domain_knowledge | structural_complexity]
- suggested_form: [narrative | analogy | scenario_walkthrough]
```

## Comprehension Gate Assessment

After receiving the verdict, assess honestly:
- Is the judgment abstract enough that downstream (human or agent) may not grasp it?
- If yes: set `translation_needed: true`. The orchestrator will route a translation pass.
- If no: set `translation_needed: false`. Routing proceeds to response.

## Workflow

1. Read thesis.md deeply
2. Decide: oracle or council?
3. Dispatch specialist with thesis as input
4. Receive structured verdict
5. Write `challenge.md` with verdict + comprehension gate
6. Update `status.json`: `phase: "challenge"`

## Done

`challenge.md` exists with oracle/council verdict. Comprehension gate assessed.
