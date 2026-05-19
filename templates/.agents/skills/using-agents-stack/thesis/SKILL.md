---
name: thesis
description: Form a falsifiable claim from the current understanding of the problem space.
trigger: When no thesis.md exists for the active workstream, or after a spiral turn resets to thesis.
inputs: [AGENTS.md, plan.md, tracked-work.json, prior synthesis.md or audit.md]
outputs: [.harness/<id>/thesis.md, .harness/<id>/status.json]
boundaries: Claim formation only. No implementation. No self-approval.
---

# Thesis Worker

Form a clear, falsifiable claim about the problem. A thesis is not "what should we build?" — it is "what do we believe is true about this space?"

## Input

The orchestrator provides inline context digest covering: plan objective, prior synthesis/audit findings (spiral turn evidence), harness rules. Read from disk only if the inline digest is insufficient.

### Required Reads (fallback)

- `docs/live/plan.md` and `docs/live/tracked-work.json`
- Any prior `synthesis.md` or `audit.md` (spiral turn evidence)
- Relevant `docs/reference/*`

## Output: thesis.md

```markdown
# Thesis

## Claim
[One clear, falsifiable statement]

## Premises
- [What must be true for the claim to hold]
- [Each premise should be independently checkable]

## Expected Outcomes
[If the claim is correct, what should we observe?]

## Boundaries
[Conditions under which the claim does NOT apply]

## Evidence Basis
[Prior artifacts or research that support this claim]
[From spiral turn: what prior synthesis/audit revealed]
```

## Quality Bar

A good thesis can be proven wrong:
- ✗ "The architecture should be clean"
- ✗ "We should use microservices"
- ✓ "Multi-agent delegation can be reduced to single-agent composition with artifact passing"

## Workflow

1. Ground in prior evidence — read plan.md, any prior synthesis/audit
2. Form the narrowest honest claim
3. Self-attack: can this be falsified? If not, it is not a thesis — refine it
4. Write `thesis.md`
5. Update `status.json`: `phase: "thesis"`, `layer: "direction"`

## Done

`thesis.md` exists with a falsifiable claim. `status.json` reflects thesis phase.
