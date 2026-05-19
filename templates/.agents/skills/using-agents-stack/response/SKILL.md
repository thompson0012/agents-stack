---
name: response
description: Design tactical solutions for each gap identified in the challenge verdict.
trigger: When challenge.md exists with clear comprehension gate, and response.md does not exist.
inputs: [AGENTS.md, plan.md, thesis.md, challenge.md]
outputs: [.harness/<id>/response.md, .harness/<id>/status.json]
boundaries: Design only. No code implementation. One concrete solution per gap.
---

# Response Worker

For every gap the challenge verdict identified, produce a concrete design response. No hand-waving. Each response must have schema-level specificity.

## Input

The orchestrator provides inline context digest covering: plan objective, thesis claim, challenge gaps, harness rules. Read from disk only if the inline digest is insufficient.

### Required Reads (fallback)

- `docs/live/plan.md`
- `.harness/<id>/thesis.md` and `.harness/<id>/challenge.md`

## Output: response.md

```markdown
# Response

## Gaps Addressed
[List of gaps from challenge.md]

---

[For EACH gap:]

## Gap: [name]

### What Challenge Found
[The specific issue challenge identified]

### Design Response
[Concrete solution with schema/structure/signature]

### Contract
[What must be true for this solution to work]

### Edge Cases
[What could still go wrong]

### Dependencies
[Relations to other responses — conflicts or prerequisites]

---
```

## Principles

- One solution per gap, independently complete
- Concrete schema or bust — no "we should consider..."
- Solutions do not need to be unified yet (synthesis handles that)
- If a gap cannot be designed around with current understanding, flag it explicitly

## Workflow

1. Parse `challenge.md` for gap list
2. For each gap: design a concrete response
3. Self-check: is each response specific enough that someone could implement it?
4. Write `response.md`
5. Update `status.json`: `phase: "response"`, `layer: "method"`

## Done

`response.md` exists with all gaps addressed concretely.
