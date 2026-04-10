# Guard evaluation fixtures

Use this fixture lane for guard-like behavior that must prove temporal correctness. Router evals answer "which child should run next?" Guard fixtures answer "given this state boundary, did the guard allow only the correct transition and fail closed otherwise?"

Keep this separate from `evals.json`:
- `evals.json` models prompt-to-route expectations for the router
- guard fixtures model before/action/after state transitions, retry eligibility, and negative gating behavior
- mixing both concerns into one schema makes route selection, retry truthfulness, and fail-closed behavior harder to review honestly
- these fixtures are regression inputs for guard logic, not a second contract for the router or state machine

Use temporal fixtures to prevent reward-hackable proofs. A guard should not accept a plausible end state unless the required before-state, evidence, and deny conditions are all explicit.

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

## Positive example: reconciled `review_failed` may retry only with clean restore metadata

```yaml
- id: review-failed-retry-allows-clean-resume
  phase_or_artifact_gate: review_failed retry gate
  before_state:
    required_artifacts:
      - docs/live/tracked-work.json
      - .harness/WORKSTREAM-004/review.md
      - .harness/WORKSTREAM-004/status.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-004
      tracked-work.json.backlog[FEATURE-004].status: review_failed
      status.json.phase: review_failed
      status.json.clean_restore_ref: refs/worktrees/ws004-clean
      status.json.attempt_count: 1
      status.json.max_attempts: 3
    invariants:
      - compound_pending_feature_ids is empty
      - attempt_count < max_attempts
      - failed review evidence remains on disk for the same sprint
  guard_action: Decide whether generator execution may retry the same sprint after a reconciled FAIL review
  expected_after_state:
    outcome: allow
    next_owner: generator-execution
    evidence:
      - the retry may proceed from the named clean restore boundary
      - review evidence stays attached to the sprint instead of being deleted
  fail_closed_expectation:
    when:
      - review.md is missing or empty
      - any required retry field is absent
      - compound_pending_feature_ids is not empty
      - attempt_count is already equal to max_attempts
    outcome: deny
    evidence:
      - preserve the sprint and record why automatic retry stopped
      - do not silently convert the failed review into a runnable execution pass
```

## Positive example: reconciled `build_failed` may retry only with clean restore metadata

```yaml
- id: build-failed-retry-allows-clean-resume
  phase_or_artifact_gate: build_failed retry gate
  before_state:
    required_artifacts:
      - docs/live/tracked-work.json
      - .harness/WORKSTREAM-005/runtime.md
      - .harness/WORKSTREAM-005/status.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-005
      tracked-work.json.backlog[FEATURE-005].status: build_failed
      status.json.phase: build_failed
      status.json.clean_restore_ref: refs/worktrees/ws005-clean
      status.json.attempt_count: 0
      status.json.max_attempts: 2
    invariants:
      - compound_pending_feature_ids is empty
      - attempt_count < max_attempts
      - runtime.md records the failed build/startup checkpoint for the same sprint
  guard_action: Decide whether generator execution may retry the same sprint after build/startup triage failed
  expected_after_state:
    outcome: allow
    next_owner: generator-execution
    evidence:
      - the retry may proceed from the named clean restore boundary
      - build/startup failure evidence stays attached to the sprint instead of being flattened into a generic blocked state
  fail_closed_expectation:
    when:
      - runtime.md is missing or empty
      - clean_restore_ref is absent
      - tracked work does not still point at the same sprint
      - attempt_count is already equal to max_attempts
    outcome: deny
    evidence:
      - preserve the sprint and surface the exact retry blocker
      - do not let build_failed masquerade as a clean execution restart
```

## Negative example: `review_failed` retry denies unsafe resume

```yaml
- id: review-failed-retry-denies-missing-clean-restore
  phase_or_artifact_gate: review_failed retry gate
  before_state:
    required_artifacts:
      - docs/live/tracked-work.json
      - .harness/WORKSTREAM-006/review.md
      - .harness/WORKSTREAM-006/status.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-006
      tracked-work.json.backlog[FEATURE-006].status: review_failed
      status.json.phase: review_failed
      status.json.attempt_count: 1
      status.json.max_attempts: 3
    invariants:
      - compound_pending_feature_ids is empty
      - review evidence exists for the same sprint
  guard_action: Decide whether generator execution may retry after review failure when restore metadata is incomplete
  expected_after_state:
    outcome: deny
    evidence:
      - no execution retry starts
      - the guard reports missing_clean_restore_ref or an equivalent explicit reason code
  fail_closed_expectation:
    when:
      - clean_restore_ref is missing
      - stronger evidence shows a different sprint owns the failure
    outcome: deny
    evidence:
      - hand control back for reconciliation or human gating instead of guessing through the missing restore boundary
```

## Negative example: `build_failed` retry denies exhausted budget

```yaml
- id: build-failed-retry-denies-exhausted-budget
  phase_or_artifact_gate: build_failed retry gate
  before_state:
    required_artifacts:
      - docs/live/tracked-work.json
      - .harness/WORKSTREAM-007/runtime.md
      - .harness/WORKSTREAM-007/status.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-007
      tracked-work.json.backlog[FEATURE-007].status: build_failed
      status.json.phase: build_failed
      status.json.clean_restore_ref: refs/worktrees/ws007-clean
      status.json.attempt_count: 2
      status.json.max_attempts: 2
    invariants:
      - compound_pending_feature_ids is empty
      - runtime evidence exists for the failed checkpoint
  guard_action: Decide whether generator execution may retry after build failure when the attempt budget is exhausted
  expected_after_state:
    outcome: deny
    evidence:
      - no execution retry starts
      - the guard reports attempt_budget_exhausted or an equivalent explicit reason code
  fail_closed_expectation:
    when:
      - attempt_count >= max_attempts
      - max_attempts is invalid or missing
    outcome: deny_or_escalate
    evidence:
      - automatic retry stops without deleting the failed sprint evidence
      - the next step remains reconciliation or human escalation, not a fabricated clean rerun
```

## How to use these fixtures

1. Choose the exact phase or artifact gate the guard owns.
2. Describe the required before-state in concrete artifacts, fields, and invariants.
3. Name the decision point in one sentence.
4. Record the allowed after-state or denial outcome explicitly.
5. Add fail-closed cases that prove the guard does not guess through missing, contradictory, unsafe, or reward-hackable state.

Keep the format reusable. If your workflow is not agents-stack, replace the file paths and phase names with your own system's gates while preserving the same temporal structure.