# QA Evidence: [FEATURE-###] [short title]

<!--
  Template: .agents/skills/using-agents-stack/references/templates/.harness/qa.md
  Owner: adversarial-live-review
  Optional detailed evidence log behind review.md.
  Archive with sprint evidence when present.
  Delete this comment block before use.
-->

## Reproduction Environment

- **Branch/commit**: [ref]
- **Runtime**: [version]
- **Date**: [ISO date]

## Detailed Checks

### AC-001: [description]

**Before-state**:
[Observed precondition. Screenshot ref, file state, or command output.]

**Action**:
[Exact reproduction steps.]

```
$ [command or interaction]
[output]
```

**After-state**:
[Observed postcondition. Must differ from before-state.]

**Verdict**: [PASS / FAIL]

---

### AC-002: [description]

**Before-state**:
[Observed precondition.]

**Action**:
[Exact reproduction steps.]

```
$ [command or interaction]
[output]
```

**After-state**:
[Observed postcondition.]

**Verdict**: [PASS / FAIL]

---

## Edge Cases Explored

- [edge case]: [observation]

## Reviewer Notes

[Anything the next reviewer or state-update should know.]
