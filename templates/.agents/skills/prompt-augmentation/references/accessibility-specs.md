# Accessibility Specs

Concise reference of accessibility terms for augmenting design prompts with inclusive patterns.

## WCAG Guidelines (POUR)

- **Perceivable** — Content presentable in ways all users can perceive (text alternatives, captions, adaptable presentation)
- **Operable** — UI components and navigation operable by all (keyboard, timing, seizure safety)
- **Understandable** — Information and UI operation understandable (readable, predictable, error-tolerant)
- **Robust** — Content compatible with current and future assistive technologies (valid markup, ARIA)

## Focus Indicators

- **Focus ring** — Visible outline on focused element; 2–3px offset ring in high-contrast color
- **Visible focus** — Never use `outline: none` without replacement; ensure 3:1 contrast ratio
- **Skip links** — Hidden link revealed on focus; jumps to main content, bypasses nav
- **Tab order** — Logical left-to-right, top-to-bottom; matches visual reading order
- **Logical flow** — Grouped controls in sequence; no focus traps, no orphan focus

## Screen Reader Cues

- **Semantic HTML** — Native elements (`<button>`, `<nav>`, `<main>`) carry implicit ARIA semantics
- **ARIA roles** — `role="alert"`, `role="dialog"`, `role="tablist"`; only when HTML alone insufficient
- **Labels** — `aria-label`, `aria-labelledby`, `aria-describedby`; every interactive element named
- **Live regions** — `aria-live="polite"/"assertive"`; announce dynamic content changes
- **Alt text patterns** — Descriptive for images, empty `alt=""` for decorative, long descriptions for complex

## Motion / Accessibility

- **prefers-reduced-motion** — OS-level setting; disable non-essential animations, keep state transitions
- **Parallax sensitivity** — Avoid large positional shifts; vestibular disorder risk
- **Auto-play** — Media must not auto-play more than 3 seconds without pause control
- **Flashing** — Max 3 flashes/second; seizure risk threshold (WCAG 2.3)

## Color Vision Considerations

- **Deuteranopia** — Green-blind (~5% male); avoid green-only signals in red-green spectrum
- **Protanopia** — Red-blind (~1% male); avoid red-only signals in red-green spectrum
- **Tritanopia** — Blue-yellow blind (rare); avoid blue-only differentiation
- **Achromatopsia safe palettes** — No color as sole indicator; pair with icons/patterns/text
- **Contrast ratios** — 4.5:1 normal text, 3:1 large text, 3:1 UI components (WCAG 2.1 AA)
- **Color + cue** — Always layer: hue + shape + position + label for multi-channel encoding