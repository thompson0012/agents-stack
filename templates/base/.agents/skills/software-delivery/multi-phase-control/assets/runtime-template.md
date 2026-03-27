# Runtime

<!-- Copy this into the consuming project's docs/live/runtime.md when needed -->

## Execution Mode
<!-- single-session | compacted-continuation | planner-generator-evaluator -->

## Baton Owner
<!-- planner | generator | evaluator — who owns the next action -->

## Role Boundaries

### Planner Owns
- Scope definition
- Contracts and acceptance gates
- What generator may change

### Generator Owns
- Implementation inside boundary
- Updating artifacts with actual changes
- Reporting implementation defects

### Evaluator Owns
- Checking against contract
- Reporting pass/fail with evidence
- Independent verification

## Transition Rules
<!-- When and how to transition between roles -->

## Compaction Checkpoints
<!-- Scheduled points for context compaction -->
- [ ] Before phase transition
- [ ] After significant decisions
- [ ] When context approaches limits

## Session Notes
<!-- Notes specific to this execution -->
