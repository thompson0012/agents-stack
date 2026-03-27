# Phase Gates

Detailed patterns for defining entry and exit criteria in multi-phase work.

## Why Gates Matter

Gates prevent:
- Premature phase transitions (started phase 2 before phase 1 is verified)
- Ambiguous completion (what does "done" mean without criteria?)
- Drift accumulation (small deviations compound across phases)
- Unclear ownership (who decides phase 1 is complete?)

## Entry Criteria Patterns

Entry criteria answer: "What must be true before starting this phase?"

### Good Entry Criteria

| Pattern | Example |
|---------|---------|
| Prior phase exit verified | "Phase 1 exit criteria: tests passing, docs updated" |
| Dependency resolved | "API contract finalized and documented" |
| Decision locked | "Architecture decision: use PostgreSQL (recorded in memory.md)" |
| Resource available | "Staging environment provisioned" |

### Bad Entry Criteria

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Vague readiness | "When we're ready" — no verification possible |
| Missing dependency | "Start phase 2" without phase 1 verification |
| Assume context | "Continue from previous" — assumes reader knows state |
| Scope hidden in gate | "Implement auth (includes OAuth, SAML, MFA)" — gate is actually scope |

## Exit Criteria Patterns

Exit criteria answer: "What must be verified before this phase is complete?"

### Good Exit Criteria

| Pattern | Example |
|---------|---------|
| Deliverable produced | "User can create account via API" |
| Test evidence | "All tests passing: `npm test` output link" |
| Doc updated | "API documented in docs/reference/api.md" |
| Decision recorded | "Auth approach: JWT with RS256 (decision in memory.md)" |
| Progress updated | "`progress.md` reflects current state" |

### Bad Exit Criteria

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Process not outcome | "Work on auth" — no completion definition |
| Unverifiable | "Make it good" — subjective, no evidence |
| Scope creep | "And handle edge cases" — undefined scope |
| No evidence link | "Tests passing" — where's the proof? |

## Gate Verification

For each gate, define:

1. **Verification method** — How to check the criteria
   - Automated: test suite, build pass, lint clean
   - Manual: review signoff, user acceptance
   - Hybrid: automated + human judgment

2. **Evidence location** — Where to find proof
   - Test output link
   - PR with CI status
   - Doc commit hash
   - `progress.md` verification table

3. **Owner** — Who decides pass/fail
   - Generator for implementation gates
   - Evaluator for acceptance gates (if planner-generator-evaluator mode)
   - User for subjective gates

## Phase Transition Checklist

Before moving from phase N to phase N+1:

- [ ] All exit criteria for phase N verified
- [ ] `progress.md` updated with phase N completion
- [ ] Drift log checked — any scope changes?
- [ ] Compaction checkpoint if context is large
- [ ] Entry criteria for phase N+1 confirmed met

## Common Failure Modes

| Mode | Symptom | Fix |
|------|---------|-----|
| Gate skipping | "Phase 1 was probably done" | Require evidence, not assumption |
| Scope hiding | "Just one more thing before phase 2" | Gate is scope creep, move to backlog |
| Forgotten gates | Context reset loses gate definitions | Gates live in `current-focus.md`, not memory |
| Owner confusion | "Who decides phase 1 is done?" | Explicit owner per gate |
| Evidence rot | Link to test output that no longer exists | Record commit hash or screenshot |