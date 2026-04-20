fixtures:
  - id: builder-blocks-without-contract
    phase_or_artifact_gate: design-builder entry check
    before_state:
      required_artifacts: []
      invariants:
        - .harness/<sprint-id>/contract.md does not exist
        - status.json shows phase: contracted
    guard_action: design-builder decides whether to begin implementation
    expected_after_state:
      outcome: deny
      next_owner: human
      phase: awaiting_human
    fail_closed_expectation:
      missing_or_invalid_state: builder must not create any artifact files
      evidence_to_record: "runtime.md: contract.md missing — cannot begin build"

  - id: builder-blocks-without-phase-contracted
    phase_or_artifact_gate: design-builder entry check
    before_state:
      required_artifacts:
        - .harness/<sprint-id>/contract.md
      invariants:
        - status.json shows phase: awaiting_human (proposal not yet approved)
    guard_action: design-builder decides whether to begin implementation
    expected_after_state:
      outcome: deny
      next_owner: human
      phase: awaiting_human
    fail_closed_expectation:
      missing_or_invalid_state: builder must not begin; phase must be contracted or a valid retry phase
      evidence_to_record: "runtime.md: phase is not contracted — awaiting human approval"

  - id: awaiting-human-prevents-auto-dispatch
    phase_or_artifact_gate: router dispatch at awaiting_human
    before_state:
      required_artifacts:
        - .harness/<sprint-id>/sprint_proposal.md
      invariants:
        - status.json shows phase: awaiting_human
        - contract.md does not exist
    guard_action: router decides which child to dispatch
    expected_after_state:
      outcome: deny (surface to human, no child dispatch)
      next_owner: human
    fail_closed_expectation:
      missing_or_invalid_state: router must not auto-dispatch design-builder or any other worker
      evidence_to_record: "Router output: Parked at awaiting_human. Surface sprint_proposal.md to human for approval."

  - id: retry-allows-with-valid-restore-ref
    phase_or_artifact_gate: router retry routing
    before_state:
      required_artifacts:
        - .harness/<sprint-id>/review.md (FAIL verdict)
        - .harness/<sprint-id>/status.json
      invariants:
        - status.json shows phase: reviewed_fail
        - clean_restore_ref is present and non-empty
        - attempt_count < max_attempts
    guard_action: router decides whether to dispatch design-builder for retry
    expected_after_state:
      outcome: allow
      next_owner: orchestrator
      dispatched_worker: design-builder
    fail_closed_expectation:
      missing_or_invalid_state: N/A — valid state should allow retry
      evidence_to_record: N/A

  - id: retry-denies-without-restore-ref
    phase_or_artifact_gate: router retry routing
    before_state:
      required_artifacts:
        - .harness/<sprint-id>/review.md (FAIL verdict)
        - .harness/<sprint-id>/status.json
      invariants:
        - status.json shows phase: reviewed_fail
        - clean_restore_ref is absent or empty string
    guard_action: router decides whether to dispatch design-builder for retry
    expected_after_state:
      outcome: deny
      next_owner: orchestrator → state-update → escalated_to_human
    fail_closed_expectation:
      missing_or_invalid_state: router must not dispatch design-builder without a valid restore reference
      evidence_to_record: "Router output: Route to using-agents-stack/state-update. — no clean_restore_ref"

  - id: retry-denies-when-budget-exhausted
    phase_or_artifact_gate: builder retry entry check
    before_state:
      required_artifacts:
        - .harness/<sprint-id>/contract.md
        - .harness/<sprint-id>/status.json
      invariants:
        - status.json shows attempt_count >= max_attempts
        - clean_restore_ref is present
    guard_action: design-builder decides whether to begin a retry attempt
    expected_after_state:
      outcome: deny
      next_owner: human
      phase: escalated_to_human
    fail_closed_expectation:
      missing_or_invalid_state: builder must not begin a new attempt when budget is exhausted
      evidence_to_record: "status.json: phase escalated_to_human, escalation_reason: attempt_count >= max_attempts"

  - id: compounder-drains-before-new-sprint
    phase_or_artifact_gate: router compound-drain check
    before_state:
      required_artifacts:
        - docs/live/tracked-work.json
      invariants:
        - compound_pending_feature_ids is non-empty
        - no runnable_active_sprint_id is set
    guard_action: router decides whether to open a new sprint or drain compound queue first
    expected_after_state:
      outcome: drain first — dispatch design-compounder
      next_owner: orchestrator
      dispatched_worker: design-compounder
    fail_closed_expectation:
      missing_or_invalid_state: router must not open a new sprint while compound_pending_feature_ids is non-empty
      evidence_to_record: "Router output: Route to frontend-design/design-compounder."

  - id: compounder-skips-without-queue-entry
    phase_or_artifact_gate: design-compounder entry check
    before_state:
      required_artifacts:
        - docs/live/tracked-work.json
      invariants:
        - compound_pending_feature_ids is empty or does not contain the dispatched feature id
    guard_action: design-compounder decides whether to extract learnings
    expected_after_state:
      outcome: skip — record deliberate-skip note in memory.md, clear queue
      next_owner: orchestrator
    fail_closed_expectation:
      missing_or_invalid_state: compounder must not invent learnings without a queue entry; must record dated skip note
      evidence_to_record: "memory.md: [SPRINT-ID] Deliberately skipped — feature not found in compound_pending_feature_ids"
