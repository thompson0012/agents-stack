---
name: frontend-qa
description: Use when validating frontend behavior in a real browser, including functional flows, visual quality, accessibility, responsive behavior, perceived performance, or adversarial edge cases.
---

# Frontend QA

## Overview

Frontend QA validates what users actually experience in the browser across seven independent layers. This is a self-contained skill — its framework is defined inline, not inherited from a shared QA core.

Signoff lens: **Utility × Usability × Craft** — does the feature solve the right job, stay understandable under real interaction, and feel intentional rather than merely unbroken?

## Seven-Layer QA Framework

Execute passes in order. Each layer builds on the previous. Record findings per layer before moving to the next.

### Layer 1: Visual QA
Validate pixel-level fidelity against the design source (Figma, design system, or reference screenshots).

- Color accuracy (eyedropper sampling vs. design tokens)
- Typography (font-size, font-weight, line-height, letter-spacing, font-family)
- Spacing (padding, margin, gap — ±1px tolerance)
- Shadows and elevation (x, y, blur, spread, color)
- Border radius consistency
- Gradient direction and color stops
- Dark mode — no white flash, correct token mapping
- Opacity and transparency consistency

[See `references/playbook.md#visual-qa` for detailed procedure]

### Layer 2: Interaction QA
Validate that every interactive element behaves correctly across all states and transitions.

- Five-state completeness: Default → Hover → Active/Pressed → Focus (keyboard) → Disabled
- Loading states — buttons show loading, prevent double-submit
- Empty states — graceful, not broken
- Error states — clear messaging, recovery path
- Reversible interactions — toggles, modals can be opened AND closed
- Navigation back/forward after state changes

[See `references/playbook.md#interaction-qa` for detailed procedure]

### Layer 3: Design System QA
Validate that the implementation faithfully uses the design system — not ad-hoc styling.

- Token adherence — no hardcoded hex, rgb(), hsl() values (search full source)
- Component library version consistency
- Icon consistency (same library, same stroke width)
- Breakpoint consistency (same breakpoints across all pages)
- Z-index management (no magic numbers like `z-index: 9999`)
- CSS custom property naming convention consistency

[See `references/playbook.md#design-system-qa` for detailed procedure]

### Layer 4: Accessibility QA
Validate that the feature is usable by everyone, including assistive technology users.

- Color contrast — body text ≥ 4.5:1, large text ≥ 3:1 (WCAG AA minimum). Use a contrast ladder: primary text ≥ 7:1, secondary ≥ 4.5:1, placeholder ≥ 3:1, disabled ≥ 2:1
- Keyboard navigation — all functionality reachable via Tab/Shift+Tab, logical focus order, visible focus ring
- Screen reader — correct heading hierarchy, labels on form fields, alt text on images, decorative images have `alt=""`
- Touch targets — minimum 44×44px (iOS) or 48×48dp (Material Design)
- Color independence — the UI must be usable in grayscale mode
- `prefers-reduced-motion` — all animations disabled when OS setting is on
- `prefers-color-scheme` — dark mode respects system preference
- ARIA — correct roles, states, and live regions

[See `references/playbook.md#accessibility-qa` for detailed procedure]

### Layer 5: Responsive QA
Validate behavior across all target viewports and devices.

- Full viewport range: 320px (iPhone SE) → 768px (tablet portrait) → 1024px (tablet landscape) → 1440px (desktop) → 2560px (4K)
- No horizontal overflow at any breakpoint
- Text wrapping under long content and real data
- Font scaling — browser text size set to "Very Large" or 200% zoom
- Landscape mode on mobile — no content clipped by notches or gesture bars
- Safe area handling — important controls not hidden behind system UI (notch, home indicator)
- Minimum touch target sizes maintained at all breakpoints

[See `references/playbook.md#responsive-qa` for detailed procedure]

### Layer 6: Content QA
Validate behavior with real-world, messy content — not just ideal design data.

- Extreme content length (50+ char usernames, multi-paragraph bios)
- Special characters and Emoji (line-height stability, no XSS)
- RTL text (Arabic, Hebrew) if internationalization is in scope
- Missing or broken images (graceful fallback, not browser broken-image icon)
- Mixed content (Chinese + English + numbers in one field)
- Number formatting (¥9,999,999.99, 1,000,000 users)
- Markdown/HTML injection prevention
- Empty, null, and partial data states

[See `references/playbook.md#content-qa` for detailed procedure]

### Layer 7: Performance QA
Validate that the feature feels fast and smooth — measured, not guessed.

- First Contentful Paint (FCP) < 1.8s
- Largest Contentful Paint (LCP) < 2.5s
- Cumulative Layout Shift (CLS) < 0.1
- Font loading — `font-display: swap`, no invisible text during load
- Image optimization — correct format (WebP/AVIF), responsive `srcset`, lazy loading
- Animation smoothness — 60fps, no layout thrashing (no animated width/height/top/left)
- Back/forward cache behavior
- Third-party script impact

[See `references/playbook.md#performance-qa` for detailed procedure]

## Severity Classification

Use three severity levels for all findings:

| Severity | Definition | Examples |
|---|---|---|
| **Blocker** | Release-stopping. Core journey broken or safety-critical failure. | Critical flow cannot complete; user data lost; UI unusable on required device/accessibility path |
| **Major** | High user impact with real cost, but not total release stop. | Confusing state in primary workflow; responsive breakage hiding important controls; severe accessibility regression |
| **Minor** | Real defect with limited blast radius or low urgency. | Non-critical visual inconsistency; secondary-state polish issue; copy/spacing problem not blocking comprehension |

## QA Inventory

Before any pass execution, build an inventory covering:
1. Core user journeys and workflows
2. Visible UI claims and design specifications
3. All interaction states and transitions
4. Risky failure modes
5. Target viewports and device classes
6. Edge cases likely to expose brittle behavior
7. Signoff claims to verify

## Evidence Rules

- Test the real path before signoff. A screenshot, DOM dump, or code inspection alone is not proof.
- Record evidence from the state where each claim is true.
- Include the interaction or request that produced the evidence.
- Quote visible text exactly when reporting copy, labels, or error states.
- Use screenshots or recordings when they clarify a visual or motion claim.
- Keep notes on what remains unverified so the report does not overclaim.
- Separate confirmed defects, contract gaps, environment issues, and product tradeoffs.

## Output Contract

Every QA execution produces:
1. **QA Inventory** — What was tested against
2. **Evidence Ledger** — Per-layer findings with reproduction steps
3. **Findings Report** — Labeled by severity, classification, and evidence basis
4. **Signoff Statement** — Evaluated through Utility × Usability × Craft lens
5. **Unverified Gaps** — Explicitly listed; never silently omitted

## Common QA Traps

| Trap | Consequence | Prevention |
|---|---|---|
| Testing only the homepage | Inner pages, error pages, empty states are uncontrolled | Build a page matrix; test at least one instance of every template |
| Testing only in Chrome | Safari/Firefox rendering differences in `backdrop-filter`, border-radius, font line-height | Test in Safari (WebKit) and Firefox (Gecko) minimum |
| Ignoring loading states | Users see white screen for 3s, assume site is broken | Test skeleton screens, loading spinners, progressive loading |
| Testing only the "ideal" screen | Admin sees perfect data; real users see chaos | Test with different roles, permissions, data states |
| Not back-syncing design files | Design files and code permanently diverge | After QA signoff, update Figma tokens to match code reality (reverse sync) |
| Calling a feature "passed" because code looks correct | Code is not behavior | Verify in browser, not in source |
| Counting one happy-path run as signoff | Most failures live in non-happy-path states | Minimum 10-state coverage: default, loading, empty, populated, success, error, partial, dense, disabled, unauthorized |

## Minimum State Coverage

Before signoff, touch as many of these states as the feature supports:
- default, loading, empty, populated, success, error, partial data, dense/maximum data, disabled/read-only, unauthorized/redirected

## QA Toolbox

| Purpose | Tools |
|---|---|
| Pixel comparison | PerfectPixel (Chrome), Figma Dev Mode |
| Color / contrast | Stark, Colour Contrast Analyser, APCA calculator |
| Accessibility | axe DevTools, WAVE, Lighthouse, macOS VoiceOver, Windows NVDA |
| Animation | DevTools Animations panel, Motion DevTools |
| Responsive | DevTools Device Mode, BrowserStack, real devices (iPhone + Android) |
| Performance | Lighthouse, WebPageTest, GTmetrix |
| Hardcoded values | grep for `#`, `rgb(`, `hsl(` in source |

## References

- [Framework](references/framework.md) — Utility × Usability × Craft in detail
- [Playbook](references/playbook.md) — Seven-layer pass execution guide
- [Reporting](references/reporting.md) — Findings format, severity classification, bug report template
