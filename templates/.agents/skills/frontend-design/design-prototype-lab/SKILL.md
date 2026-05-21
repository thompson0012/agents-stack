---
name: design-prototype-lab
description: Progressive design validation pipeline. Runs Token Lab → Component Theater → Page Slice to verify design vocabulary works in real browsers before full artifact build. Conditionally triggered when design.md specifies prototyping_required: true.
---

# Design Prototype Lab

## Placement
This is a nested child under `frontend-design`; its path is `frontend-design/design-prototype-lab/`, and the router selects it before standalone use.

You are the progressive validation phase of the design harness. Your job is to verify that the design vocabulary from `design.md` works correctly in real browsers before the full artifact build begins — catching token mismatches, component state gaps, and layout stress failures early, when they are cheap to fix.

A validated design vocabulary prevents rework. A skipped validation pipeline risks building on a broken foundation.

## Worker Dispatch Contract

- Run in a fresh worker context. The orchestrator dispatches; it does not inline validation.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read-only on repo and context files, plus write access to `.agents-stack/<sprint-id>/token-validation.md`, `.agents-stack/<sprint-id>/component-tests.md`, `.agents-stack/<sprint-id>/page-slice.md`, `.agents-stack/<sprint-id>/status.json`, and `.agents-stack/<sprint-id>/artifact/` (HTML test fixtures only). No edits to product code, .agents-stack/*, or .agents-stack/reference/*.
- Not parallel-safe. Only one prototype lab may run at a time. Do not dispatch a second lab while one is active.
- Dispatch framing is non-authoritative. Verify against `design.md` and `.agents-stack/tracked-work.json` before writing.

## Required Entry Checks

Before writing any test fixtures:

1. `design.md` exists with `prototyping_required: true`.
2. `design.md` exists with visual vocabulary, and `reference/design/tokens.json` has the token inventory (color palette, type scale, spacing, shadows).
3. `status.json` shows `phase: "design_contracted"`.
4. `design.md` identifies which design decisions are uncertain and need validation.

If any check fails, stop with the reason recorded in a new finding and set `phase: "awaiting_human"`. Do not skip levels.

## Skeleton-Based Token Injection

All three validation levels use pre-built skeleton HTML templates located in `references/`. The AI does **not** build HTML from scratch — it loads the skeleton and injects design tokens from `reference/design/tokens.json`.

### Token Injection Workflow

```
1. Read references/<skeleton>.html
2. Read reference/design/tokens.json
3. For each /*TOKEN:xxx*/ placeholder in the skeleton:
   → Find the matching token in reference/design/tokens.json (by semantic name, not literal string)
   → Replace placeholder with the actual CSS value (hex, px, font name, etc.)
4. If a token is not found in reference/design/tokens.json:
   → Leave /*TOKEN:xxx — NOT FOUND*/ as a visible marker for manual review
5. Save the filled HTML to .agents-stack/<sprint-id>/artifact/<filename>.html
6. Add @font-face or <link> for web fonts if design.md specifies external font sources
```

### Skeleton Templates

| Skeleton | Source | Output |
|---|---|---|
| Token Lab | `references/token-lab-skeleton.html` | `artifact/token-lab.html` |
| Component Theater | `references/component-theater-skeleton.html` | `artifact/component-theater.html` |
| Page Slice | `references/page-slice-skeleton.html` | `artifact/page-slice.html` |

Skeletons contain only structural HTML + the `:root` CSS block with `/*TOKEN:xxx*/` placeholders. They have **no decorative styling** — all visual identity comes from injected tokens.

### Progressive Validation Pipeline

### Level 1: Token Lab

**Purpose**: Validate that the color palette, type scale, spacing, and shadows from `reference/design/tokens.json` render correctly in a real browser.

**Procedure**:
1. Load `references/token-lab-skeleton.html`.
2. Inject tokens from `reference/design/tokens.json` into all `/*TOKEN:xxx*/` placeholders in the `:root` block.
3. Save the filled file to `.agents-stack/<sprint-id>/artifact/token-lab.html`.
4. The skeleton pre-builds these displays (all driven by injected tokens):
   - Full color palette side-by-side (primary, neutral, semantic — light mode + dark mode toggle)
   - Type scale specimen (all headings + body + caption, in both English and, if applicable, Chinese)
   - Spacing rhythm display (visual bars at each spacing scale step)
   - Shadow/elevation showcase (all shadow levels applied to sample cards)
   - Border radius showcase (all radius values applied to sample boxes)
5. Test on at least 2 real devices or browsers.
6. Record findings in `token-validation.md`:
   - Any color that renders differently than expected
   - Any font that fails to load or renders poorly
   - Any spacing that feels off
   - Any shadow that looks unnatural
   - Dark mode mapping correctness
   - Overall verdict: `TOKENS_VALID` | `TOKENS_NEEDS_ADJUSTMENT`

### Level 2: Component Theater

**Purpose**: Verify that key components render correctly with all five interaction states.

**Procedure**:
1. Load `references/component-theater-skeleton.html`.
2. Inject tokens from `reference/design/tokens.json` into all `/*TOKEN:xxx*/` placeholders.
3. The skeleton comes pre-built with 4 preset components (Button, Input Field, Card, Modal/Dialog) with state toggle UI. For each additional component in the contract's state matrix, copy the section pattern and add component markup.
4. For each component, the skeleton provides radio-button toggles for: Default, Hover, Active/Pressed, Focus (keyboard), and Disabled states.
5. Save the filled file to `.agents-stack/<sprint-id>/artifact/component-theater.html`.
6. Record findings in `component-tests.md`:
   - Per-component pass/fail with evidence
   - Any missing state
   - Any visual inconsistency between components
   - Overall verdict: `COMPONENTS_VALID` | `COMPONENTS_NEEDS_ADJUSTMENT`

### Level 3: Page Slice

**Purpose**: Test one representative section/page with real-world content stress.

**Procedure**:
1. Load `references/page-slice-skeleton.html`.
2. Inject tokens from `reference/design/tokens.json` into all `/*TOKEN:xxx*/` placeholders.
3. The skeleton provides a neutral page structure (header/nav, hero, card grid, content, footer). Apply the contract's layout pattern if the contract specifies one.
4. Save the filled file to `.agents-stack/<sprint-id>/artifact/page-slice.html`.
5. The skeleton has a built-in stress test toggle. When ON, content swaps to extreme variants:
   - 50-character strings without spaces (overflow test)
   - Long names (`"Mohammed bin Salman Al Saud"`)
   - Emoji-rich content (🚀💎🌙)
   - Missing images (broken `src`)
   - Extreme numbers (`¥9,999,999.99`)
6. The skeleton displays current viewport width and is responsive by default (card grid collapses below 768px).
7. Record findings in `page-slice.md`:
   - Layout behavior under stress
   - Text truncation/overflow
   - Image fallback behavior
   - Responsive behavior at extremes
   - Overall verdict: `SLICE_VALID` | `SLICE_NEEDS_ADJUSTMENT`

## Decision After Pipeline

After all three levels complete:

- **If ALL levels pass** (all verdicts are `*_VALID`): write `status.json` with `phase: "validated"`. The router will route to `design-builder` next.
- **If any level has critical findings** (any verdict is `*_NEEDS_ADJUSTMENT` with blocking issues): write `status.json` with `phase: "validating_failed"`. Escalate to human with specific findings and the affected test fixture paths.
- **If only advisory findings** (minor issues that do not block the build): write `status.json` with `phase: "validated"` but include advisory notes in each validation file for the builder to reference. Advisory findings do not block the `validated` phase.

## Required Output Files

### `.agents-stack/<sprint-id>/token-validation.md`

```md
# Token Validation: <SPRINT-ID>

## Test Environment
- Browser:
- Device:
- Viewport:

## Color Palette
| Token name | Expected hex/oklch | Rendered value | Match? | Notes |
|---|---|---|---|---|
| ... | ... | ... | PASS / FAIL | ... |

## Dark Mode Mapping
| Light token → Dark token | Expected behavior | Rendered behavior | Match? |
|---|---|---|---|
| ... | ... | ... | PASS / FAIL |

## Type Scale
| Level | Expected font | Rendered font | Size rendering | Notes |
|---|---|---|---|---|
| ... | ... | ... | PASS / FAIL | ... |

## Spacing Rhythm
| Token | Expected (px) | Rendered | Match? |
|---|---|---|---|
| ... | ... | ... | PASS / FAIL |

## Shadows / Elevation
| Level | Expected | Rendered appearance | Match? |
|---|---|---|---|
| ... | ... | ... | PASS / FAIL |

## Border Radius
| Token | Expected | Rendered | Match? |
|---|---|---|---|
| ... | ... | ... | PASS / FAIL |

## Findings Summary
- Total checks:
- Passed:
- Failed:
- Advisory:

## Verdict
TOKENS_VALID | TOKENS_NEEDS_ADJUSTMENT

## Evidence
- Test fixture: `.agents-stack/<sprint-id>/artifact/token-lab.html`
- Screenshots / measurements: (paths or inline descriptions)
```

### `.agents-stack/<sprint-id>/component-tests.md`

```md
# Component Tests: <SPRINT-ID>

## Test Environment
- Browser:
- Device:

## State Matrix Coverage
| Component | Default | Hover | Active/Pressed | Focus | Disabled | All states present? |
|---|---|---|---|---|---|---|
| Button (primary) | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | YES / NO |
| Button (secondary) | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | YES / NO |
| Input field | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | YES / NO |
| Card (interactive) | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | PASS / FAIL | YES / NO |
| [others] | ... | ... | ... | ... | ... | ... |

## Per-Component Findings
### Button (primary)
- Default: ...
- Hover: ...
- Active/Pressed: ...
- Focus: ...
- Disabled: ...
- Issues: ...

[repeat for each component]

## Cross-Component Consistency
- Color consistency: CONSISTENT | INCONSISTENT — [notes]
- Spacing consistency: CONSISTENT | INCONSISTENT — [notes]
- Interaction consistency: CONSISTENT | INCONSISTENT — [notes]

## Findings Summary
- Total components:
- Total states checked:
- Passed:
- Failed:
- Missing states:
- Advisory:

## Verdict
COMPONENTS_VALID | COMPONENTS_NEEDS_ADJUSTMENT

## Evidence
- Test fixture: `.agents-stack/<sprint-id>/artifact/component-theater.html`
```

### `.agents-stack/<sprint-id>/page-slice.md`

```md
# Page Slice Validation: <SPRINT-ID>

## Test Environment
- Browser:
- Device:
- Viewports tested:

## Section Implemented
- Screen / section name: (from design.md)
- Tokens used: ...
- Components used: ...

## Stress Content Results
| Stress case | Expected behavior | Observed behavior | Status |
|---|---|---|---|
| Long names | Text truncates or wraps gracefully | ... | PASS / FAIL |
| Emoji content | Renders without breaking layout | ... | PASS / FAIL |
| Missing images | Fallback placeholder displayed | ... | PASS / FAIL |
| Extreme numbers | Renders without overflow | ... | PASS / FAIL |
| 320px viewport | Content is usable, no horizontal scroll | ... | PASS / FAIL |

## Layout Behavior
- Container overflow: NONE | PRESENT — [details]
- Text truncation: HANDLED | UNHANDLED — [details]
- Image fallback: PRESENT | MISSING — [details]
- Responsive breakpoints: CORRECT | INCORRECT — [details]

## Findings Summary
- Total stress checks:
- Passed:
- Failed:
- Advisory:

## Verdict
SLICE_VALID | SLICE_NEEDS_ADJUSTMENT

## Evidence
- Test fixture: `.agents-stack/<sprint-id>/artifact/page-slice.html`
```

### `.agents-stack/<sprint-id>/status.json`

```json
{
  "sprint_id": "<sprint-id>",
  "phase": "validated | validating_failed",
  "owner_role": "orchestrator",
  "resume_from": "token-validation.md",
  "last_verified_step": "design-prototype-lab completed",
  "last_updated_at": "<ISO timestamp>"
}
```

For `validating_failed`, add:
```json
{
  "escalation_reason": "<summary of critical findings>",
  "affected_fixtures": [
    ".agents-stack/<sprint-id>/artifact/token-lab.html",
    ".agents-stack/<sprint-id>/artifact/component-theater.html",
    ".agents-stack/<sprint-id>/artifact/page-slice.html"
  ]
}
```

## Quality Bar

- All three HTML test fixtures open in a browser with zero console errors.
- Dark mode toggle works in `token-lab.html` — toggling switches the color scheme and all tokens update accordingly.
- Stress content in `page-slice.html` is realistic, not fabricated — use the exact long-name and emoji examples specified above.
- Record evidence, not opinions — screenshot, measure, or copy-paste actual rendered values. Do not describe from memory.
- Every finding must cite a specific observed value or behavior, not a vague impression.

## References

- [Token Lab Skeleton](references/token-lab-skeleton.html) — Color palette, typography, spacing, shadow, border-radius preview template
- [Component Theater Skeleton](references/component-theater-skeleton.html) — 5-state component preview template (Button, Input, Card, Modal preset)
- [Page Slice Skeleton](references/page-slice-skeleton.html) — Representative page layout with stress test toggle

## Stop Conditions

Do not proceed beyond the current level and set `phase: "validating_failed"` when:
- A token renders in a color that differs from the expected hex/oklch value by a visible margin
- A font in the type scale fails to load or renders in a fallback font
- A component is missing any of the five required states (default, hover, active/pressed, focus, disabled)
- The page slice breaks layout at 320px viewport width
- Any test fixture produces a console error when opened in a browser

## Final Checklist

- [ ] Entry checks passed: `design.md` has `prototyping_required: true`, `reference/design/tokens.json` has token inventory, `phase: "design_contracted"`
- [ ] `token-lab.html` generated from `references/token-lab-skeleton.html`, all `/*TOKEN:xxx*/` placeholders injected from `reference/design/tokens.json`, opens with zero console errors
- [ ] Dark mode toggle functional in `token-lab.html`
- [ ] `token-validation.md` written with per-token pass/fail evidence and overall verdict
- [ ] `component-theater.html` generated from `references/component-theater-skeleton.html`, all tokens injected, all five states functional for every contracted component
- [ ] `component-tests.md` written with per-component pass/fail evidence and overall verdict
- [ ] `page-slice.html` generated from `references/page-slice-skeleton.html`, all tokens injected, stress content covering long names, emoji, broken images, extreme numbers, and 320px viewport
- [ ] `page-slice.md` written with per-stress-case pass/fail evidence and overall verdict
- [ ] Decision executed: all three verdicts are `*_VALID` → `phase: "validated"`; any critical failure → `phase: "validating_failed"` with escalation reason
- [ ] `status.json` updated with correct phase and `last_updated_at` timestamp
- [ ] All findings cite evidence — observed values, measurements, or screenshots, not memory
