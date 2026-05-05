# Review: [FEATURE-###] [short title]

<!--
  Template: .agents/skills/using-agents-stack/references/templates/.harness/review.md
  Owner: adversarial-live-review
  Write exactly one verdict: PASS, FAIL, or BLOCKED.
  Every verdict must be backed by before/action/after evidence.
  Delete this comment block before use.
-->

## Verdict

**[PASS / FAIL / BLOCKED]**

## Evidence Checked

- [artifact path] — [what was checked]
- [artifact path] — [what was checked]

## Contract Criteria

| AC | Before-State | Action | After-State | Result |
|---|---|---|---|---|
| AC-001 | [observed before] | [reproduction step] | [observed after] | [PASS / FAIL] |
| AC-002 | [observed before] | [reproduction step] | [observed after] | [PASS / FAIL] |

## Defects (if FAIL)

- **[D-001]** [severity: P0/P1/P2]: [description, evidence, file:line]
- **[D-002]** [severity: P0/P1/P2]: [description, evidence, file:line]

## Blockers (if BLOCKED)

- [blocker]: [why it prevented honest PASS/FAIL, what must change]

## Next Owner

[state-update / generator-execution / awaiting_human / escalated_to_human]

## Retry / Recovery Instructions

[If FAIL: clean_restore_ref, which defects to fix first, remaining attempt budget.]
[If BLOCKED: what must be unblocked, who owns it, how to verify it's cleared.]
