# Guard evaluation fixtures

Use this fixture lane for guard-like behavior that must prove temporal correctness. Router evals answer "which child should run next?" Guard fixtures answer "given this state boundary, did the guard allow only the correct transition and fail closed otherwise?"

Keep this separate from `evals.json`:
- `evals.json` models prompt-to-route expectations for the router
- guard fixtures model before/action/after state transitions and negative gating behavior
- mixing both concerns into one schema makes route selection and guard correctness harder to review honestly

## Portable schema

```yaml
fixtures:
  - id: unique-fixture-id
    phase_or_artifact_gate: contracted
    before_state:
      required_artifacts:
        - .harness/WORKSTREAM-001/contract.md
      required_fields:
        status.json.phase: contracted
      invariants:
        - runnable_active_sprint_id matches the sprint under test
    guard_action: Decide whether the next phase may begin
    expected_after_state:
      outcome: allow
      next_owner: generator-execution
      evidence:
        - runtime.md may be created
    fail_closed_expectation:
      when:
        - required artifact is missing
        - required fields contradict stronger evidence
      outcome: deny_or_escalate
      evidence:
        - record the exact missing or contradictory state
```

## Required fields

- `id`: stable fixture identifier
- `phase_or_artifact_gate`: the phase boundary, artifact gate, or control-plane checkpoint under evaluation
- `before_state`: the minimum state that must already be true before the guard acts
- `guard_action`: the decision point being exercised
- `expected_after_state`: what the system may do when the guard allows the transition
- `fail_closed_expectation`: the negative case describing how the system refuses, parks, or escalates when truth is missing, contradictory, or unsafe

## Positive example: retry is allowed only with clean restore metadata

```yaml
- id: review-failed-retry-allows-clean-resume
  phase_or_artifact_gate: review_failed retry gate
  before_state:
    required_artifacts:
      - .harness/WORKSTREAM-004/review.md
      - .harness/WORKSTREAM-004/status.json
    required_fields:
      status.json.phase: review_failed
      status.json.clean_restore_ref: refs/worktrees/ws004-clean
      status.json.attempt_count: 1
      status.json.max_attempts: 2
    invariants:
      - compound_pending_feature_ids is empty
      - attempt_count < max_attempts
  guard_action: Decide whether generator execution may retry the same sprint
  expected_after_state:
    outcome: allow
    next_owner: generator-execution
    evidence:
      - the retry may proceed from the named clean restore boundary
  fail_closed_expectation:
    when:
      - any required retry field is absent
      - attempt_count is already equal to max_attempts
    outcome: deny_or_escalate
    evidence:
      - preserve the sprint and record why automatic retry stopped
```

## Negative example: missing contract fails closed

```yaml
- id: execution-start-denies-missing-contract
  phase_or_artifact_gate: contracted execution-start gate
  before_state:
    required_artifacts:
      - .harness/WORKSTREAM-004/contract.md
      - .local/docs/live/tracked-work.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-004
    invariants:
      - contract.md must be the approved execution boundary
  guard_action: Decide whether generator execution may start work for the sprint
  expected_after_state:
    outcome: allow_only_if_contract_exists
    next_owner: generator-execution
    evidence:
      - implementation begins strictly from the approved contract
  fail_closed_expectation:
    when:
      - contract.md is missing
      - tracked work points at a different runnable sprint
      - stronger local evidence contradicts the dispatched phase
    outcome: deny
    evidence:
      - stop before editing code
      - hand control back for state repair or contract review
```

## How to use these fixtures

1. Choose the exact phase or artifact gate the guard owns.
2. Describe the required before-state in concrete artifacts, fields, and invariants.
3. Name the decision point in one sentence.
4. Record the allowed after-state or routing outcome.
5. Add at least one fail-closed case that proves the guard does not guess through missing or contradictory state.

Keep the format reusable. If your workflow is not agents-stack, replace the file paths and phase names with your own system's gates while preserving the same temporal structure.