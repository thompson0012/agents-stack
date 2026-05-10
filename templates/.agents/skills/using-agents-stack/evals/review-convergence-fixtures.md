# Review convergence evaluation fixtures

Use this fixture lane for review/state-update convergence behavior that must prove PASS publishability honestly. Router evals answer "which child should run next?" Retry guard fixtures answer "may a failed sprint retry cleanly?" Review-convergence fixtures answer "may this review actually publish PASS and archive now, or must it deny / re-review first?"

Keep this separate from `evals.json` and `guard-eval-fixtures.md`:
- `evals.json` models prompt-to-route expectations for the router
- `guard-eval-fixtures.md` models retry eligibility and temporal clean-resume truth
- review-convergence fixtures model PASS gating, review coverage closure, and whether `state-update` may truthfully publish archived state
- these fixtures are regression inputs for review/state-update publishability, not a second contract for router selection or retry ownership

Use convergence fixtures to prevent reward-hackable PASS decisions. A plausible PASS summary is not enough unless coverage metadata shows every acceptance criterion id was accounted for, convergence metadata explicitly closes the review loop, and no non-duplicate open P0-P3 findings remain.

## Portable schema

```yaml
fixtures:
  - id: unique-fixture-id
    phase_or_artifact_gate: review convergence PASS gate
    before_state:
      required_artifacts:
        - .harness/WORKSTREAM-010/contract.md
        - .harness/WORKSTREAM-010/qa.md
        - .harness/WORKSTREAM-010/review.md
        - .harness/WORKSTREAM-010/status.json
        - docs/live/tracked-work.json
      required_fields:
        status.json.phase: review_recorded
        review.md.status: PASS
        review.md.coverage_metadata.criteria_total: 5
        review.md.coverage_metadata.criteria_checked: 5
        review.md.coverage_metadata.all_acceptance_criteria_accounted_for: true
        review.md.convergence_summary.convergence_status: closed
        review.md.convergence_summary.open_blocking_findings_count: 0
      invariants:
        - every contract acceptance id has an explicit contract-check result in review.md
        - every contract acceptance id appears in qa.md acceptance evidence
        - every non-duplicate P0, P1, P2, or P3 finding is closed, resolved, or absent
        - advisory-only findings below P3 may remain open without blocking PASS
    guard_action: Decide whether `state-update` may publish PASS and archive the sprint
    expected_after_state:
      outcome: allow_pass_publish
      next_owner: state-update
      evidence:
        - PASS publishability is justified from explicit review coverage and explicit convergence closure
        - archive cutover may proceed only because open non-duplicate P0-P3 blockers are zero
    fail_closed_expectation:
      when:
        - any non-duplicate P0, P1, P2, or P3 finding remains open
        - coverage metadata is missing or incomplete
        - contract acceptance ids are missing from qa.md or review.md
        - convergence metadata is missing, contradictory, or not explicitly closed
      outcome: deny_or_rereview
      evidence:
        - keep the sprint unarchived and record the exact blocker or missing metadata
```

## Required fields

- `id`: stable fixture identifier
- `phase_or_artifact_gate`: the review/state-update publishability boundary under evaluation
- `before_state`: the minimum durable state that must already be true before PASS may publish
- `guard_action`: the review convergence decision being exercised
- `expected_after_state`: what `state-update` may publish only when convergence is honestly closed
- `fail_closed_expectation`: the denial or re-review path when blocking findings or required metadata are missing

## Positive example: PASS publishable after complete coverage and closed convergence

```yaml
- id: review-pass-allows-publish-when-convergence-closed
  phase_or_artifact_gate: review convergence PASS gate
  before_state:
    required_artifacts:
      - docs/live/tracked-work.json
      - .harness/WORKSTREAM-008/contract.md
      - .harness/WORKSTREAM-008/qa.md
      - .harness/WORKSTREAM-008/review.md
      - .harness/WORKSTREAM-008/status.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-008
      tracked-work.json.backlog[FEATURE-008].status: awaiting_review
      status.json.phase: review_recorded
      review.md.status: PASS
      review.md.coverage_metadata.criteria_total: 5
      review.md.coverage_metadata.criteria_checked: 5
      review.md.coverage_metadata.all_acceptance_criteria_accounted_for: true
      review.md.convergence_summary.convergence_status: closed
      review.md.convergence_summary.open_blocking_findings_count: 0
    invariants:
      - contract.md defines AC-001 through AC-005
      - qa.md includes AC-001 through AC-005 in Acceptance Checks
      - review.md includes AC-001 through AC-005 in Contract Check Results
      - RV-008-2 is marked duplicate_of RV-008-1 and does not increase blocker count
      - RV-008-3 is advisory-only and may remain open without blocking convergence
      - no non-duplicate open P0, P1, P2, or P3 findings remain
  guard_action: Decide whether `state-update` may publish PASS, cut archive evidence over, and clear the runnable slot
  expected_after_state:
    outcome: allow_pass_publish
    next_owner: state-update
    evidence:
      - PASS may be published because coverage is complete and convergence is explicitly closed
      - duplicate-linked findings remain recorded for traceability but do not double-count as blockers
      - advisory-only findings below the blocking range do not stop archive cutover
  fail_closed_expectation:
    when:
      - any contract acceptance id loses its review result or QA evidence entry
      - convergence status is not explicitly closed
      - a primary P0, P1, P2, or P3 finding reopens
    outcome: deny_or_rereview
    evidence:
      - PASS publication stops and the sprint remains unarchived until the review is truthful again
```

## Negative example: open blocking finding denies PASS even when duplicates exist

```yaml
- id: review-pass-denies-open-p2-even-with-duplicate-thread
  phase_or_artifact_gate: review convergence PASS gate
  before_state:
    required_artifacts:
      - docs/live/tracked-work.json
      - .harness/WORKSTREAM-009/contract.md
      - .harness/WORKSTREAM-009/qa.md
      - .harness/WORKSTREAM-009/review.md
      - .harness/WORKSTREAM-009/status.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-009
      tracked-work.json.backlog[FEATURE-009].status: awaiting_review
      status.json.phase: review_recorded
      review.md.status: PASS
      review.md.coverage_metadata.criteria_total: 3
      review.md.coverage_metadata.criteria_checked: 3
      review.md.coverage_metadata.all_acceptance_criteria_accounted_for: true
      review.md.convergence_summary.convergence_status: open
      review.md.convergence_summary.open_blocking_findings_count: 1
    invariants:
      - contract.md defines AC-001 through AC-003
      - review.md includes AC-001 through AC-003 in Contract Check Results
      - RV-009-1 is an open P2 finding
      - RV-009-2 is an open P2 finding with duplicate_of: RV-009-1
      - duplicate_of prevents double-counting, but it does not erase the primary open blocker
  guard_action: Decide whether a review claiming PASS may publish while a primary blocking finding is still open
  expected_after_state:
    outcome: deny_or_rereview
    evidence:
      - PASS is denied because one non-duplicate open P2 blocker remains
      - duplicate-linked findings do not inflate the blocker count above one, but the remaining blocker still prevents convergence closure
  fail_closed_expectation:
    when:
      - any primary P0, P1, P2, or P3 finding is open
      - blocker counts disagree with the underlying finding list
    outcome: deny_or_rereview
    evidence:
      - keep the sprint out of archive and force explicit re-review or corrective work instead of normalizing the open blocker away
```

## Negative example: fake PASS narrative without full acceptance traceability denies publish

```yaml
- id: review-pass-denies-missing-acceptance-traceability
  phase_or_artifact_gate: review convergence PASS gate
  before_state:
    required_artifacts:
      - docs/live/tracked-work.json
      - .harness/WORKSTREAM-010/contract.md
      - .harness/WORKSTREAM-010/qa.md
      - .harness/WORKSTREAM-010/review.md
      - .harness/WORKSTREAM-010/status.json
    required_fields:
      tracked-work.json.runnable_active_sprint_id: WORKSTREAM-010
      tracked-work.json.backlog[FEATURE-010].status: awaiting_review
      status.json.phase: review_recorded
      review.md.status: PASS
    invariants:
      - contract.md defines AC-001 through AC-004
      - qa evidence exists, but at least one contract acceptance id is missing from qa.md or review.md
      - review.md.coverage_metadata is missing `criteria_total`, `criteria_checked`, or `all_acceptance_criteria_accounted_for`
      - no implicit PASS may be inferred from a narrative summary alone
  guard_action: Decide whether `state-update` may publish PASS when the review narrative looks positive but traceability metadata is absent
  expected_after_state:
    outcome: deny_or_rereview
    evidence:
      - PASS is denied because publishability metadata is incomplete even if no blocker is named explicitly
      - state-update must not archive from a prose-only review summary
  fail_closed_expectation:
    when:
      - any contract acceptance id is absent from review coverage
      - coverage summary fields are absent or contradictory
      - open_blocking_findings_count is absent
    outcome: deny_or_rereview
    evidence:
      - record a missing_review_acceptance_traceability or missing_review_convergence_metadata reason instead of fabricating closure
```

## How to use these fixtures

1. Choose the exact review/state-update publishability gate under evaluation.
2. Describe the required before-state in concrete artifacts, coverage fields, and convergence invariants.
3. Name the decision point in one sentence.
4. Record the only allowed publishable PASS after-state, or the deny / re-review outcome.
5. Add fail-closed cases that prove open P0-P3 findings, duplicate-count mistakes, missing acceptance-id coverage, or missing coverage/convergence metadata cannot be normalized into archive-ready PASS.

Keep the format reusable. If your workflow is not agents-stack, replace the file paths and review-field names with your own system's publishability gate while preserving the same convergence structure.
