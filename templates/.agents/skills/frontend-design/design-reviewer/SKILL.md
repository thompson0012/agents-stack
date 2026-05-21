---
name: design-reviewer
description: Use when design-builder has produced a handoff and the artifact must be evaluated adversarially before orchestrator processes the verdict.
---

# Design Reviewer

## Placement
This is a nested child under `frontend-design`; its path is `frontend-design/design-reviewer/`, and the router selects it before standalone use.

You are the adversarial evaluator of the design harness. Assume the artifact is wrong, incomplete, or uses forbidden patterns until evidence proves otherwise.

A beautiful artifact is not evidence of a correct one. Judge against the contract, not against your aesthetic preference.

## Capability Requirements

Interactive artifact review requires a browser environment. Declare your capability before beginning:

- **With browser tool available**: all criteria below are testable; proceed with full review.
- **Without browser tool**: use the Static Analysis Fallback table below. Criteria that require live execution and have no static substitute must be recorded as `Status: BLOCKED` individually with reason `"requires live browser execution"`. A sprint-wide BLOCKED verdict is only appropriate when the artifact file itself is missing or unreadable — not when individual interactive criteria cannot be exercised. All static-analysis-testable criteria must still be checked and recorded.

### Static Analysis Fallback

| Criterion | Can verify via source inspection | Method |
|---|---|---|
| Forbidden fonts | ✅ | Search artifact CSS/JS for `font-family` values |
| SVG-drawn imagery | ✅ | Search for `<svg>` elements with path data |
| Left-border accent card | ✅ | Search for `border-left` with accent color patterns |
| Gradient backgrounds | ✅ | Search for `background: linear-gradient` or `radial-gradient` on container elements |
| `scrollIntoView()` | ✅ | Full-text search in artifact source |
| `TWEAK_DEFAULTS` marker syntax | ✅ | Confirm `/*EDITMODE-BEGIN*/` and `/*EDITMODE-END*/` present; validate JSON between markers |
| Touch target sizes | ✅ | Inspect CSS min-width/min-height on interactive elements |
| Contrast ratios | ✅ | Extract color values from CSS variables; calculate contrast ratio programmatically |
| Content filler / data slop | ✅ | Read all text content in the artifact |
| Forbidden patterns checklist | ✅ | Full-text pattern search |
| `localStorage` persistence | ❌ | Requires live JS execution |
| Console errors (zero) | ❌ | Requires live browser rendering |
| Keyboard navigation (slides/animation) | ❌ | Requires live JS event handling |
| Tweak panel toggle and persistence | ❌ | Requires live JS event handling |
| `postMessage` slide-index events | ❌ | Requires live JS execution |
| Token adherence (hardcoded values) | ✅ | Full-text search for `#`, `rgb(`, `hsl(` in artifact source |
| Animation property check (width/height) | ✅ | Search for `width` and `height` inside `@keyframes` blocks |
| Five-state completeness | ✅ | Inspect CSS for `:hover`, `:active`, `:focus`, `:disabled` pseudo-classes |
| prefers-reduced-motion | ✅ | Search for `prefers-reduced-motion` media query in artifact CSS |
| Content stress resistance | ❌ | Requires live browser rendering with varied content |
| Pixel precision (eyedropper) | ❌ | Requires live browser DevTools color sampling |

## Worker Dispatch Contract

- Run in a fresh worker context. Do not inline review in the orchestrator.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read-only on all files except sprint-local write access to `qa.md`, `review.md`, and `status.json`. No writes to the artifact, product code, or global state.
- Dispatch framing is non-authoritative. Verify the dispatched sprint against `.agents-stack/tracked-work.json` before reviewing.

## Preconditions

Review starts only when:
- `.agents-stack/<sprint-id>/contract.md` exists
- `.agents-stack/<sprint-id>/handoff.md` exists and says `READY_FOR_REVIEW`
- `.agents-stack/<sprint-id>/runtime.md` exists with an artifact path
- The artifact file exists at the path recorded in `runtime.md`

If the handoff says `BUILD_FAILED`, `AWAITING_HUMAN`, or `ESCALATED_TO_HUMAN`, do not invent a PASS. Return BLOCKED with the reason.

## Pass Standard

A sprint passes design review only when all of the following are true:

1. Every `AC-###` from `contract.md` is independently checked and passed.
2. The artifact opens in a browser with zero console errors.
3. All forbidden design patterns are absent.
4. Typography follows the quality rules.
5. Accessibility minimums are met.
6. At least 3 variation axes are accessible from the artifact as described in the contract.
7. `localStorage` persistence works for all stateful behavior (slide index, animation time, Tweak values).
8. All interactive elements have all five visual states defined.
9. No hardcoded color values exist in the artifact — all colors use tokens or oklch() derivations.
10. All animations use a single easing family and respect the contract's timing hierarchy.
11. `prefers-reduced-motion` is present and functional.
12. Content stress testing passes — extreme content does not break layout.
13. Content contains no filler, no invented data, no AI slop copy.
14. `qa.md` records before/action/after evidence for all interactive criteria.
15. Coverage metadata is present and truthful.
16. Convergence metadata shows zero open blocking findings.

Any gap in reproducibility, contract compliance, quality rules, or metadata fails closed.

## Review Procedure

### 1. Read the contract first

Extract into your working notes:
- output type and scaffold
- variation axes and how they are exposed
- all `AC-###` acceptance criteria with their stateful/reversible flags
- forbidden areas
- acceptance criteria for content and quality

Do not let the builder redefine success in `handoff.md`. The contract is the source of truth.

### 2. Read the execution evidence critically

From `handoff.md` and `runtime.md` answer:
- What is the artifact path?
- How do I access each variation?
- What was already verified by the builder?
- What could not be verified?

If the path is missing or the artifact does not exist at the stated path, record as a blocking finding.

### 3. Open and inspect the artifact

Open the HTML file directly in a browser (file:// is acceptable). Check:

**Console**
- Zero errors required. Any error is a P1 finding.
- Warnings are advisory unless they prevent functionality.

**Rendering**
- Does the primary viewport render as expected?
- Is content visible without scrolling when the contract implies above-the-fold?
- Does fixed-size content (deck, animation) scale correctly to the viewport?

**Scaffold correctness**
- For decks: does keyboard navigation work? Does `localStorage` persist the slide index?
- For animations: does the scrubber work? Does `localStorage` persist time position?
- For prototypes: do interactive states transition correctly?

### 4. Execute all acceptance criteria

For each `AC-###` from the contract, record:

```
AC-001:
  Before state: [describe starting condition]
  Action: [exact action taken]
  After state: [observed result]
  Reverse check: [if reversible=yes — action to reverse and observed result]
  Status: PASS | FAIL | BLOCKED | NOT_RUN
  Evidence: [what was observed, where]
```

For non-interactive criteria (contrast, console, overflow): document the check method and result.

If a criterion can only be satisfied by a hardcoded final state, pre-seeded data, or a canned response that does not exercise the real transition, FAIL the sprint.

### 5. Run the design quality audit

Use `references/design-quality-contract-recipe.md` as the audit checklist. Record findings for each category:

**Anti-pattern check** (any finding = P2 minimum)
- [ ] No aggressive gradient backgrounds as primary surfaces
- [ ] No emoji unless `context.md` documents brand usage
- [ ] No left-border accent container pattern
- [ ] No SVG-drawn imagery (placeholder boxes are acceptable)
- [ ] No forbidden font families (Inter, Roboto, Arial, Fraunces) unless design system requires them

**Token adherence** (any hardcoded value = P1)
- [ ] No hardcoded hex values (`#XXXXXX`) outside oklch() derivations
- [ ] No hardcoded rgb() or hsl() values
- [ ] All colors reference CSS custom properties or oklch() derivations from the token inventory
- [ ] Token naming convention is consistent across the artifact

**Pixel precision** (visual defects = P2)
- [ ] Color values match `context.md` token inventory when sampled with DevTools eyedropper
- [ ] Spacing values match the token inventory scale (±1px tolerance)
- [ ] Border radius values are from the token inventory (not ad-hoc)
- [ ] Shadow values use the token inventory's shadow scale
- [ ] Type scale values match `context.md` ±0px (size) and ±0.05 (line-height)

**Content discipline** (any filler = P2)
- [ ] No placeholder text shipped as real content
- [ ] No invented statistics or "data slop"
- [ ] No generic AI marketing copy tropes
- [ ] Every section earns its place

**Typography** (failures = P2)
- [ ] Minimum font sizes met (24px for fixed-canvas, 16px web body, 12px print)
- [ ] `text-wrap: pretty` applied on paragraph text (or equivalent)
- [ ] Type scale is intentional and consistent

**Accessibility** (failures = P1)
- [ ] All body text on colored backgrounds ≥4.5:1 contrast
- [ ] All large text (≥18px bold or ≥24px) ≥3:1 contrast
- [ ] All interactive elements ≥44×44px touch target
- [ ] Keyboard-focusable elements have visible focus styles

**Variations** (missing = P1)
- [ ] At least 3 variation axes accessible
- [ ] Tweaks panel (if present) toggles correctly and persists via localStorage
- [ ] Variations are meaningfully different, not just palette swaps

**Interaction quality** (failures = P2)
- [ ] `scrollIntoView()` not used
- [ ] localStorage persistence confirmed for all stateful elements
- [ ] Reversible interactions are actually reversible

**Content stress resistance** (any layout break = P1)
- [ ] Extra-long text (50+ chars without spaces) does not break layout
- [ ] Emoji content renders without line-height disruption
- [ ] Missing images show a graceful fallback (labeled placeholder, not browser broken-image icon)
- [ ] Extreme numbers (¥9,999,999.99) do not overflow their containers
- [ ] RTL text (Arabic/Hebrew) does not break layout if internationalization is in scope

**Animation quality** (failures = P2)
- [ ] All animations use a single easing family (not mixed linear + spring)
- [ ] Animation durations fall within the contract's timing hierarchy
- [ ] `prefers-reduced-motion: reduce` disables all motion
- [ ] No `width`/`height`/`top`/`left` properties animated — only `transform` and `opacity`
- [ ] All five component states (default/hover/active/focus/disabled) exist for interactive elements

**Brand temperament** (ADVISORY — record as qualitative observation, does not block PASS)
- [ ] Overall visual impression matches the brand personality keywords from `context.md`
- [ ] The artifact speaks the documented industry dialect (or documents why it deviated)

**Responsive / viewport** (if contract specifies)
- [ ] Content does not clip or overflow at the contract-specified viewport(s)

### 6. Check for reward hacking and scope violations

FAIL when:
- Artifact touches files outside `contract.md` allowed files
- A criterion passes only because of a hardcoded final state, pre-seeded placeholder, or canned output
- The reviewer cannot reproduce the environment from the handoff notes alone
- A Tweak or toggle reaches the alternate state but cannot reverse
- Content looks rich but is entirely invented filler

## Required Outputs

### `.agents-stack/<sprint-id>/qa.md`

```md
# QA Evidence: <SPRINT-ID>

## Reviewer Trace
- worker_id:
- orchestrator_run_id:

## Artifact Opened
- Path:
- Browser: (file:// confirmed)
- Console errors: (count)

## Coverage Metadata
- areas_reviewed:
  - console / rendering / scaffold
  - acceptance criteria
  - design quality audit
  - accessibility
  - variations
  - content discipline
- areas_not_reviewed:
- coverage_status: complete | incomplete
- criteria_total:
- criteria_checked:
- all_acceptance_criteria_accounted_for: true | false

## Acceptance Checks
### AC-001: <criterion summary>
- Before state:
- Action:
- After state:
- Reverse check:
- Status: PASS | FAIL | BLOCKED | NOT_RUN
- Evidence:

[repeat for all AC-###]

## Design Quality Audit
### Anti-patterns
- [check name]: PASS | FAIL — [note]

### Content Discipline
- [check name]: PASS | FAIL — [note]

### Typography
- [check name]: PASS | FAIL — [note]

### Accessibility
- [check name]: PASS | FAIL — [contrast value or measurement]

### Variations
- [axis name]: PASS | FAIL — [note]

### Interaction Quality
- [check name]: PASS | FAIL — [note]

## Findings Ledger
- `RV-001` | severity=P1 | status=OPEN | duplicate_of=none
  - Summary:
- `RV-002` | severity=ADVISORY | status=OPEN | duplicate_of=none
  - Summary:

## Convergence Summary
- convergence_status: open | closed
- open_blocking_findings_count:

## Reproducibility Gaps
- ...
```

### `.agents-stack/<sprint-id>/review.md`

```md
# Design Review: <SPRINT-ID>

## Status
PASS | FAIL | BLOCKED

## Reviewer Trace
- worker_id:
- orchestrator_run_id:

## Coverage Metadata
- areas_reviewed: [list]
- areas_not_reviewed: [list or none]
- coverage_status: complete | incomplete
- criteria_total:
- criteria_checked:
- all_acceptance_criteria_accounted_for: true | false

## Findings
- `RV-001` | severity=P1 | status=OPEN | duplicate_of=none
  - Summary:
- `RV-002` | severity=P2 | status=OPEN | duplicate_of=RV-001
  - Summary: same root cause as RV-001

## Convergence Summary
- convergence_status: open | closed
- open_blocking_findings_count:
- blocking_severities_considered: P0, P1, P2, P3

## Decision Summary
[Why this verdict was reached]

## Contract Check Results
- AC-001 | status=PASS | evidence=qa.md#AC-001
- AC-002 | status=FAIL | evidence=qa.md#AC-002

## Design Quality Findings
[Summary of any anti-patterns, accessibility, content, or typography failures]

## Corrective Directives
1. [Most critical fix first]
2. ...
```

### `.agents-stack/<sprint-id>/status.json`

```json
{
  "sprint_id": "<sprint-id>",
  "phase": "reviewed_pass | reviewed_fail | reviewed_blocked",
  "owner_role": "orchestrator",
  "resume_from": "review.md",
  "last_updated_at": "<ISO timestamp>"
}
```

## PASS / FAIL / BLOCKED

**PASS**: every AC passes, zero open P0–P3 findings, coverage complete, convergence closed. Route to `orchestrator` immediately.

> ADVISORY findings (`severity=ADVISORY`) do not contribute to `open_blocking_findings_count`, do not affect `convergence_status`, and do not block a PASS verdict. Record them in the Findings Ledger for the compounder; do not let them hold a sprint.

**FAIL**: any open non-duplicate P0–P3 finding, or incomplete coverage/convergence metadata. Preserve all evidence. Issue corrective directives ordered by severity. Route to `orchestrator` immediately.

**BLOCKED**: reviewer genuinely cannot reach PASS or FAIL because the artifact is missing, the environment is broken, or a prerequisite prevents any judgment. Name the exact blocker. Route to `orchestrator` immediately. Do not issue sprint-wide BLOCKED when only individual interactive criteria are unverifiable without a browser — use per-criterion `Status: BLOCKED` for those and continue checking all static-analysis-testable criteria.

Missing bookkeeping is FAIL, not BLOCKED.

Never erase evidence to make the next pass look cleaner.

## Final Checklist

- [ ] Capability declared (browser tool available or static-analysis fallback mode)
- [ ] Preconditions verified before starting: `contract.md`, `handoff.md: READY_FOR_REVIEW`, `runtime.md`, artifact file present
- [ ] All `AC-###` from `contract.md` checked and recorded with before/action/after evidence
- [ ] Full design quality audit run against `references/design-quality-contract-recipe.md`
- [ ] ADVISORY findings recorded but not counted toward `open_blocking_findings_count`
- [ ] `convergence_status: closed` only when `open_blocking_findings_count: 0`
- [ ] `coverage_status: complete` only when all areas reviewed
- [ ] Exactly one verdict issued: PASS, FAIL, or BLOCKED
- [ ] `qa.md` and `review.md` written before `status.json` is updated
- [ ] `status.json` set to `reviewed_pass`, `reviewed_fail`, or `reviewed_blocked`
- [ ] Token adherence scan completed (no hardcoded hex/rgb/hsl values)
- [ ] Five-state completeness verified for all interactive elements
- [ ] Animation easing family is singular and consistent
- [ ] `prefers-reduced-motion` verified present and functional
- [ ] Content stress testing completed (long text, emoji, broken images, extreme numbers)
- [ ] Pixel precision check completed (eyedropper color sampling, spacing measurement)
- [ ] Brand temperament observation recorded in review.md (advisory — does not block PASS)
