---
name: contract
description: Convert architectural synthesis into a bounded, buildable execution contract.
trigger: When synthesis.md exists and contract.md does not.
inputs: [AGENTS.md, plan.md, synthesis.md]
outputs: [.harness/<id>/contract.md, .harness/<id>/status.json]
boundaries: Scope definition only. No code implementation. Must inspect real code for file boundaries.
---

# Contract Worker

Turn the synthesis framework into a buildable contract. Define: what files change, what does not change, how we verify success.

## Input

The orchestrator provides inline context digest covering: plan objective, synthesis framework, harness rules. Read from disk only if the inline digest is insufficient.

### Required Reads (fallback)

- `docs/live/plan.md`
- `.harness/<id>/synthesis.md`
- **Actual code** in areas to be touched — must inspect real files for file boundaries, not guess paths

## Output: contract.md

```markdown
# Contract

## Workstream
- ID: [WORKSTREAM-ID]
- Title: [title]

## Objective
[What this sprint builds — derived from synthesis]

## Scope

### Allowed Files
- `path/to/file1.ts`
- `path/to/directory/` (bounded)

### Forbidden Areas
- `path/to/do-not-touch/`
- [subsystems or files that must not change]

## Acceptance Criteria

### AC-001 | stateful=no | reversible=no
- Requirement: [what must be true]
- Evidence: [how to verify — command, selector, observable output]
- I/O examples:
  - Input: [concrete input value] → Expected: [concrete expected output]
  - Input: [edge case input] → Expected: [expected output]

### AC-002 | stateful=yes | reversible=yes
- Requirement: [interactive behavior]
- I/O examples:
  - Before state: [starting condition]
    Action: [exact step]
    After state: [expected result]
  - Before state: [alternate starting condition]
    Action: [alternate step]
    After state: [expected result]
- Reverse check: [how to undo and verify]

## Risks and Assumptions
- [What could go wrong]
- [Hidden assumptions to surface]

## Non-Goals
| # | Deferred Item | Reason (external constraint) |
|---|---|---|
| 1 | [what is deferred] | [why not now — tech limitation, deadline, dependency not ready] |
| 2 | [what is deferred] | [why not now] |
```

## Quality Bar

- Narrow enough to finish in one sprint
- Every AC is externally verifiable — someone reading this file can check it
- File boundaries are precise — actual paths, not "the auth module"
- Every AC includes concrete I/O examples — not just behavioral prose
- Each Non-Goal states an external constraint (tech limitation, deadline, dependency not ready) — not subjective preference
- Stateful ACs include before/action/after — no "looks correct now"

## Workflow

1. Read `synthesis.md` for what to build
2. Inspect actual code for file boundaries
3. Define contract with hard edges
4. Write `contract.md`
5. Update `status.json`: `phase: "contract"`, `layer: "action"`

## Done

`contract.md` exists with bounded, verifiable scope. Ready for build.
