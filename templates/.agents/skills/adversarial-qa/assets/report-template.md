# Adversarial QA Report

## Scope

<!-- What was attacked, what was excluded, why -->

**Feature / System**: [name]
**Attack Date**: [date]
**Attack Domains**: [spec | design | backend | frontend | data]

## Risk Summary

<!--
Highest-risk findings and overall stability assessment.
One paragraph: "This system is [safe / moderate risk / high risk] because..."
-->

## Findings

### F-001: [Title]

- **Domain**: [Spec | Design | Backend | Frontend | Data]
- **Severity**: [P0 | P1 | P2 | P3]
- **Attack Path**:
  ```
  1. [Step 1]
  2. [Step 2]
  3. [Observed result]
  ```
- **Evidence**: [Logs, output, screenshots, or description of what was observed]
- **Impact**: [What happens if this is exploited or triggered in production]
- **Recommendation**: [What to fix or mitigate]
- **Compounds With**: [F-00X, F-00Y — if any]

---

### F-002: [Title]

...

## Survived Attacks

<!--
Attack patterns that were tried but the system held.
Equally important as findings — documents what was tested and passed.
-->

| Domain | Attack Attempted | Result |
|--------|-----------------|--------|
| Backend | Concurrent writes to same record | Correctly rejected — optimistic locking in place |
| Frontend | Empty state with null data | Shows graceful empty state |
| ... | ... | ... |

## Risk Assessment

<!-- Overall assessment -->

| Dimension | Assessment | Evidence |
|-----------|-----------|----------|
| **Spec completeness** | [Adequate / Gaps found / Major gaps] | [Ref to findings] |
| **Design robustness** | [Robust / Minor concerns / Fragile] | [Ref to findings] |
| **Backend resilience** | [Resilient / Moderate / Brittle] | [Ref to findings] |
| **Frontend robustness** | [Robust / Moderate / Brittle] | [Ref to findings] |
| **Data integrity** | [Integrity verified / Issues found / Critical findings] | [Ref to findings] |

**Overall Verdict**: [Ship / Ship with mitigations / Fix before ship / Do not ship]

## Recommended Follow-Up

| Priority | Action | Owner |
|---------|--------|-------|
| P0 | [Critical fix needed] | [implement / plan / spec] |
| P1 | [Important fix] | [implement / plan] |
| P2 | [Should fix soon] | [implement] |
| P3 | [Watch / document] | [spec] |

## Appendix: Attack Log

<!-- What was attempted, in what order, what was abandoned -->

| Time | Domain | Action | Outcome |
|------|--------|--------|---------|
| T+0 | Spec | Assumption scan | Found 3 implicit assumptions |
| T+15 | Backend | Input fuzzing | 2 endpoints crashed on malformed JSON |
| ... | ... | ... | ... |
