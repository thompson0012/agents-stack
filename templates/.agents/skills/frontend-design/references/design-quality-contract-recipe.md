# Design Quality Contract Recipe

Domain-specific acceptance criteria shapes and review checklist for `frontend-design` sprint contracts and reviews. Use this alongside the base `AC-001` through `AC-008` criteria required by every design sprint.

---

## Output-Type Criteria

Add the criteria for the contract's output type to the base set in `sprint_proposal.md` and `contract.md`.

### html-prototype

```md
- `AC-T01` | stateful=yes | reversible=yes
  - Requirement: All interactive state transitions are reversible when the contract marks them reversible (e.g. toggles, filters, modal open/close).
  - Evidence: Reviewer triggers each interactive element, confirms the after-state, then reverses and confirms the before-state returns.
  - Before state: initial load state.
  - Action: trigger the interaction.
  - After state: expected changed state.
  - Reverse check: trigger reversal, confirm initial state returns.

- `AC-T02` | stateful=yes | reversible=no
  - Requirement: All Tweak values persist across page reload via localStorage.
  - Evidence: Set a Tweak value, reload the page (Cmd+R / F5), confirm the value is restored.
  - Before state: default Tweak values.
  - Action: change a Tweak value, reload.
  - After state: changed value persists.

- `AC-T03` | stateful=no | reversible=no
  - Requirement: No `scrollIntoView()` calls exist in the artifact.
  - Evidence: Search artifact source for `scrollIntoView`.
```

### slide-deck

```md
- `AC-D01` | stateful=yes | reversible=yes
  - Requirement: Keyboard navigation (← / →) advances and retreats slides.
  - Evidence: Open the deck, press → three times (slides advance), press ← three times (slides retreat to start).
  - Before state: slide 1 displayed.
  - Action: press → three times.
  - After state: slide 4 displayed.
  - Reverse check: press ← three times, slide 1 displayed.

- `AC-D02` | stateful=yes | reversible=no
  - Requirement: Current slide index persists across page reload.
  - Evidence: Navigate to slide 5, reload, confirm slide 5 opens.
  - Before state: default (slide 1).
  - Action: navigate to slide 5, reload.
  - After state: slide 5 displayed.

- `AC-D03` | stateful=no | reversible=no
  - Requirement: Fixed canvas scales correctly at the reviewer's viewport; no content clips.
  - Evidence: Resize window to 1280×720, confirm content is visible and unclipped. Resize to 2560×1440 and confirm.

- `AC-D04` | stateful=no | reversible=no
  - Requirement: Slide elements carry `data-screen-label` attributes matching the visible slide counter (1-indexed).
  - Evidence: Inspect DOM — slide 1 element has `data-screen-label="01 <title>"`, slide 5 has `data-screen-label="05 <title>"`.

- `AC-D05` | stateful=no | reversible=no (only when speaker notes are contracted)
  - Requirement: `window.postMessage({slideIndexChanged: N})` is fired on init and on every slide change.
  - Evidence: Open the browser console, navigate slides, confirm postMessage calls appear.
```

### animation

```md
- `AC-A01` | stateful=yes | reversible=yes
  - Requirement: Play/pause controls start and stop the animation.
  - Evidence: Click play, confirm animation runs. Click pause, confirm animation freezes. Click play again, animation resumes from the paused position.
  - Before state: paused at 0s.
  - Action: click play.
  - After state: animation running.
  - Reverse check: click pause, animation freezes.

- `AC-A02` | stateful=yes | reversible=yes
  - Requirement: Scrubber changes the animation time position.
  - Evidence: Drag scrubber to 50%, confirm animation shows mid-point state. Drag back to 0%, confirm start state.

- `AC-A03` | stateful=yes | reversible=no
  - Requirement: Last time position persists across page reload.
  - Evidence: Scrub to 30s, reload, confirm animation opens at ~30s.

- `AC-A04` | stateful=no | reversible=no
  - Requirement: Fixed canvas scales correctly at the reviewer's viewport.
  - Evidence: Resize to 1280×720 and confirm unclipped scaling.
```

### wireframe

```md
- `AC-W01` | stateful=no | reversible=no
  - Requirement: All placeholder blocks are visually distinct from real content and labeled.
  - Evidence: Every unfilled image, icon, or content area uses a neutral placeholder style with a visible label (e.g. "[Hero Image]").

- `AC-W02` | stateful=no | reversible=no
  - Requirement: Visual hierarchy is clear at a glance — headings, body, and UI regions are distinguishable without color.
  - Evidence: Screenshot the page and view in grayscale; structural hierarchy is still apparent.
```

### ui-mockup

```md
- `AC-M01` | stateful=no | reversible=no
  - Requirement: All color values are sourced from the project token inventory in context.md, or derived using oklch from that palette.
  - Evidence: Inspect the artifact CSS; no color values outside the token inventory appear without oklch derivation notation.

- `AC-M02` | stateful=no | reversible=no
  - Requirement: Spacing, radius, and shadow values match the project token scale in context.md.
  - Evidence: Compare pixel values in DevTools against the token inventory.
```

---

## Design Quality Review Checklist

Use this checklist in the reviewer's audit pass. Each category maps to severity levels when failed.

### Forbidden Pattern Check (P2 minimum per violation)

| Check | Pass condition | Fail condition |
|---|---|---|
| Gradient backgrounds | No gradient used as a primary surface background | Any full-bleed gradient used as a primary background |
| Emoji usage | No emoji, OR `context.md` documents brand uses emoji | Emoji present without documented brand policy |
| Left-border accent card | No container uses the `border-left: 4px + accent color + rounded corners` pattern | This pattern used as a component card style |
| SVG-drawn imagery | No image content drawn with inline SVG paths | Inline SVG used to depict illustrations, photos, or icons |
| Forbidden fonts | No Inter, Roboto, Arial, Fraunces, or system-ui used unless `context.md` confirms the design system requires them | Any of these font families present without design system justification |

### Content Discipline (P2 minimum per violation)

| Check | Pass condition | Fail condition |
|---|---|---|
| No filler | Every text, stat, and section was specified in the contract or uses an explicitly labeled placeholder | Generic placeholder text ("Lorem ipsum", "Sample data") shipped as-is |
| No data slop | No invented statistics, meaningless metrics, or decorative numbers | Numbers like "12,400 users" or "94% satisfaction" appear without being in the brief |
| No AI copy tropes | Copy is direct, specific, and matches the project voice | Copy uses superlatives, vague corporate claims, or generic marketing language |
| Earned elements | Each UI element serves a specific function from the contract | Decorative sections, stock-photo placeholders, or extra features added without contract scope |

### Typography (P2 per violation)

| Check | Pass condition | Fail condition |
|---|---|---|
| Minimum sizes | 24px+ for 1920×1080 fixed canvas; 16px+ for web body; 12px+ for print | Any visible body text below the minimum |
| Non-forbidden family | Font family is from the token inventory or a design-appropriate choice | Forbidden family used without design system justification |
| text-wrap: pretty | Paragraph text has `text-wrap: pretty` or equivalent | Long-form text without widow/orphan control |
| Consistent scale | Heading and body sizes follow a discernible ratio from the token inventory | Ad-hoc sizes with no relationship to the design system |

### Accessibility (P1 per violation)

| Check | Pass condition | Fail condition |
|---|---|---|
| Body text contrast | All body text on colored backgrounds ≥4.5:1 | Any body text below 4.5:1 |
| Large text contrast | All text ≥18px bold or ≥24px regular on colored backgrounds ≥3:1 | Any large text below 3:1 |
| Touch targets | All interactive elements ≥44×44px | Any interactive element with a tap area below 44×44px |
| Focus styles | All keyboard-focusable elements have a visible focus ring | Any focusable element with invisible or removed focus style |

### Variations (P1 if fewer than 3 axes)

| Check | Pass condition | Fail condition |
|---|---|---|
| Variation count | ≥3 axes accessible in the artifact | Fewer than 3 distinct variation axes |
| Meaningful differences | Axes explore layout, interaction, or visual personality differences | All axes are palette-only swaps |
| Tweak persistence | All Tweak values persist via localStorage on reload | A Tweak value resets to default on reload |
| Tweak listener order | Listener registered before `__edit_mode_available` posted | `__edit_mode_available` posted before listener attached (breaks toggle) |

### Interaction Quality (P2 per violation)

| Check | Pass condition | Fail condition |
|---|---|---|
| No scrollIntoView | Artifact source does not contain `scrollIntoView` | `scrollIntoView` found in artifact |
| localStorage state | All stateful behavior persists as contracted | Any stateful element resets on reload when persistence was contracted |
| Reversible transitions | Every reversible interaction returns to the before-state | A reversible interaction cannot be undone |

---

## Severity Reference

| Level | Meaning |
|---|---|
| P0 | Security or data-destruction risk — rare in design artifacts |
| P1 | Sprint fails. Accessibility violation, missing required variations, missing console-error check, reproduction blocked |
| P2 | Sprint fails. Forbidden pattern, content discipline violation, typography violation, interaction quality violation |
| P3 | Sprint fails if it was an explicit contract requirement; otherwise advisory |
| ADVISORY | Non-blocking. Noted for the compounder and future sprints |
