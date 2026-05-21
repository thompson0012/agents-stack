---
name: design-builder
description: Use when design.md is in design_contracted phase and the design artifact must be implemented.
---

# Design Builder

## Placement
This is a nested child under `frontend-design`; its path is `frontend-design/design-builder/`, and the router selects it before standalone use.

You are the implementation phase of the design harness. Your job is to produce a high-quality, verifiable HTML artifact that exactly matches the approved contract in `design.md` — nothing more, nothing less.

Producing a beautiful artifact that violates the contract is still a failure. Producing a correct artifact that uses AI slop patterns is still a failure.

## Worker Dispatch Contract

- Run in a fresh worker context. The orchestrator dispatches; it does not inline building.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: write access to `.agents-stack/<sprint-id>/artifact/`, `.agents-stack/<sprint-id>/design-handoff.md`, `.agents-stack/<sprint-id>/status.json`. No edits to product code, .agents-stack/*, or .agents-stack/reference/*.
- Dispatch framing is non-authoritative. Verify against `design.md` and `.agents-stack/tracked-work.json` before writing.

## Required Entry Checks

Before writing any code:
1. `design.md` exists and all `[human must clarify]` fields are resolved.
2. `design.md` contains at minimum: output type, visual vocabulary reference, and token inventory reference.
3. `status.json` shows `phase: "design_contracted"` or a valid retry phase with `clean_restore_ref`.
4. If this is a retry: confirm `attempt_count < max_attempts` and `clean_restore_ref` names a valid restore point.

If any check fails, stop. Record the gap in `design-handoff.md`, set `phase: "awaiting_human"`, and return.

## Source of Truth

Work from `design.md`, not from the conversation.

Binding sections:
- objective
- output type
- allowed files
- forbidden areas
- acceptance criteria (all `AC-###` ids)
- variation axes

`.agents-stack/reference/design/vocabulary.md` and `.agents-stack/reference/design/tokens.json` provide the design vocabulary; they do not override the contract. If they conflict, preserve the conflict in `design-handoff.md` and stop.

## Retry Discipline

When resuming after `qa_fail` or `build_error`:
- restore from `clean_restore_ref` before beginning the next attempt
- increment `attempt_count` at the start of the attempt, not at the end
- if `attempt_count` would exceed `max_attempts`, set `phase: "escalated_to_human"` immediately

### clean_restore_ref Convention

`clean_restore_ref` identifies the restore point for the sprint's artifact directory.

**Format:** use the sprint-id string (e.g., `"DESIGN-001"`). Restoring means deleting all contents of `.agents-stack/<sprint-id>/artifact/` and rebuilding from `design.md` and reference files — these source files are never modified by the builder and always remain valid as the restore baseline.

**When to set it:** on the very first build attempt, before writing any artifact files, set `clean_restore_ref: "<sprint-id>"` in the `building` status.json. This ensures a restore point exists before any failure can occur.

**If git is available** and the `.agents-stack/` folder is tracked, prefer using the git SHA of the pre-build commit: `clean_restore_ref: "<git-sha>"`. Restoring then means `git checkout <sha> -- .agents-stack/<sprint-id>/artifact/`.

A sprint that reaches `build_error` or `qa_fail` without a `clean_restore_ref` in status.json cannot be retried — the router will escalate to human immediately.

## Build Procedure

### 0. Layered Implementation Order (MANDATORY)

Build in three layers, verifying each before moving to the next:

**Layer 1: Static Restoration**
- Nail typography, colors, spacing, and layout first — no animations, no interactivity
- Verify against `reference/design/tokens.json` with DevTools
- Every color must be a CSS custom property sourced from the token inventory
- No hardcoded hex values; use `var(--token-name)` or oklch() derivations

**Layer 2: Responsive Skeleton**
- Add responsive behavior (Container Queries or breakpoints)
- Verify at 320px, 768px, 1440px, and 2560px — no content clips or overflows
- All interactive elements must have ≥44×44px touch targets at every breakpoint

**Layer 3: Animation Loading**
- Add animations in priority order:
  1. Essential feedback (button presses, form validation) — 100-150ms
  2. Scroll-triggered reveals — 200-300ms
  3. Decorative animations (background particles, cursor tracking) — only if contracted
- All animations must use the single easing family specified in the contract
- All animations must respect `prefers-reduced-motion: reduce`

### 1. Determine the scaffold

Select the scaffold pattern that matches the contract's output type:

**`html-prototype`**
- React/Babel inline JSX — use the pinned CDN versions below, no exceptions:
  ```html
  <script src="https://unpkg.com/react@18.3.1/umd/react.development.js"
          integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
          integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
          integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"
          crossorigin="anonymous"></script>
  ```
  > **Hash note:** verify SRI hashes at `https://unpkg.com/{package}/{path}` before first use and after any version bump. A wrong hash produces an integrity console error on every load, failing AC-001 (zero console errors).
- Vanilla HTML/CSS/JS — acceptable when React adds no value (static layouts, simple interactions).

**`slide-deck`**
- Fixed 1920×1080 canvas. JS scaling wrapper: `transform: scale()` centered on black background.
- Keyboard navigation (←/→ and arrow keys), slide-count overlay.
- `localStorage` persistence for current slide index.
- Slide elements labeled with `data-screen-label="01 Title"` (1-indexed, matching the visible slide counter).
- Speaker notes via `<script type="application/json" id="speaker-notes">` only when the contract explicitly requires them.

**`animation`**
- Timeline-based engine with scrubber and play/pause controls.
- `localStorage` persistence for current time position.
- `Stage` wrapper with auto-scaling.

**`wireframe`**
- Low-fi HTML/CSS. Labeled placeholder blocks with a clear visual hierarchy.
- No decorative styling, no color beyond grayscale + one accent, no real imagery.

**`ui-mockup`**
- Hi-fi HTML using tokens from `reference/design/tokens.json`.
- Use `oklch()` for any supplementary colors not in the token inventory, deriving from the existing palette.

### 2. Apply design vocabulary from reference files

Before writing component code:
- Set CSS custom properties from the token inventory in `:root` (sourced from `reference/design/tokens.json`)
- Use only font families found in `reference/design/tokens.json`; if none were found, pick one from the non-forbidden list (not Inter, not Roboto, not Arial, not Fraunces)
- Use spacing and radius values from the token inventory
- Match the visual vocabulary described in `reference/design/vocabulary.md` (density, corner style, shadow, icon style)

### 3. Implement variations

The contract names at least 3 variation axes. Expose them via one of:

**Tweaks Panel (preferred for interactive prototypes)**
Implement as a floating panel toggled by a `__activate_edit_mode` / `__deactivate_edit_mode` message listener. Register the listener before posting `__edit_mode_available` to the parent. Persist changes via `__edit_mode_set_keys`. Wrap defaults in:
```js
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#D97757",
  "darkMode": false
}/*EDITMODE-END*/;
```
The block between markers must be valid JSON with double-quoted keys.

**Labeled sections or slides (for decks and wireframes)**
Each variation is a separate section with a visible label. The reviewer can navigate between them.

### 4. Quality Rules — Non-Negotiable

Every artifact must follow these rules before handoff. Violation of any rule is a build defect.

#### Content discipline
- No filler content. Every text element, stat, icon, or section earns its place. If the contract does not specify content, use minimal representative placeholders labeled as such (`[Metric: TBD]` not `42,000 users`).
- No "data slop" — invented statistics, meaningless numbers, or decorative data.
- No AI slop copy tropes (excessive superlatives, generic marketing phrases).

#### Visual anti-patterns (forbidden)
- No aggressive gradient backgrounds as primary surfaces
- No emoji unless `reference/design/vocabulary.md` documents the brand uses them
- No containers styled with `border-left: 4px solid <accent>` + rounded corners as a card treatment
- No imagery drawn with inline SVG paths; use labeled placeholder boxes (`<div class="img-placeholder">` styled with a neutral fill) or reference actual project assets
- No AI-generated color palettes invented from scratch when token inventory exists

#### Token discipline
- No hardcoded hex, rgb(), or hsl() values anywhere in the artifact. Use CSS custom properties from the token inventory or oklch() derivations from the existing palette.
- Token naming must follow the project's convention. Never mix naming styles.
- If a needed color has no token, derive it via oklch(from var(--existing-token) ...) and document the derivation.

#### Component state completeness (MANDATORY for html-prototype, ui-mockup)
Every interactive element must define all five visual states:
- Default → Hover → Active/Pressed → Focus (keyboard) → Disabled
- Focus state must use a visible focus ring (never `outline: none` without replacement)
- Disabled state must be visually distinct (reduced opacity, muted colors) but still readable

#### Animation and motion (MANDATORY for animation, html-prototype)
- Use the timing hierarchy from the contract: micro (100-150ms), transition (200-300ms), narrative (400-600ms)
- Prefer spring physics (`spring()` in CSS or equivalent) over linear animations for UI feedback
- Never mix easing families — use one family across the entire artifact
- Add `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }` to the artifact CSS
- Never animate `width`, `height`, `top`, `left` properties — use `transform` and `opacity` only (prevents layout thrashing)

#### Visual proportion discipline (ADVISORY — record in design-handoff.md if violated)
- 60-30-10 rule: ~60% neutral surface, ~30% brand color, ~10% accent
- 80/20 rule: ~80% of elements should be visually "quiet" (neutral, standard), ~20% "speak" (brand color, large type, animation)

#### Typography
- Never use: Inter, Roboto, Arial, Fraunces, or generic `system-ui` unless the project's own design system requires them and `reference/design/tokens.json` confirms this
- Minimum font sizes: 24px for 1920×1080 fixed canvas; 12px for print; 16px for web body
- Apply `text-wrap: pretty` on paragraph text

#### Interaction
- Never use `scrollIntoView()` — use other DOM scroll methods when scrolling is needed
- `localStorage` persistence required for: current slide index, current animation time, and any Tweak values
- All interactive state changes must be reversible if the contract marks them reversible
- Never use `width` or `height` in animation keyframes — use `transform: scale()` instead

#### Accessibility
- All text on colored backgrounds: ≥4.5:1 contrast (body), ≥3:1 (large text ≥18px bold or ≥24px regular)
- All interactive touch targets: minimum 44×44px
- Focusable interactive elements must have visible focus styles
- `prefers-reduced-motion: reduce` must disable all animations and transitions

#### React/Babel rules
- Each `<script type="text/babel">` gets its own scope. To share components between files, export them to `window`:
  ```js
  Object.assign(window, { MyComponent, AnotherComponent });
  ```
- Never use `const styles = { ... }` — always use component-specific names: `const cardStyles = { ... }`
- Never use `type="module"` on script imports — it breaks Babel transpilation
- Keep individual files under 1000 lines; split into smaller components and import them

#### Fixed-size content scaling
```js
function scaleStage() {
  const stage = document.querySelector('.stage');
  const scaleX = window.innerWidth / 1920;
  const scaleY = window.innerHeight / 1080;
  const scale = Math.min(scaleX, scaleY);
  stage.style.transform = `translate(-50%, -50%) scale(${scale})`;
}
window.addEventListener('resize', scaleStage);
scaleStage();
```
Navigation controls (prev/next, scrubber) must be outside the scaled element.

### 5. Capture build evidence

Build evidence is the reviewer's reproduction kit, not a progress diary. It is recorded directly in `design-handoff.md` under the **Build Evidence** section.

Record:
- Exact file path(s) of the artifact
- How to open it: `file:///path/to/artifact.html` or equivalent
- Output type and scaffold used
- Variation axes exposed and how to access them
- For each `AC-###` from the contract: what was implemented and where the reviewer should look
- Any known gaps, warnings, or intentional deferrals

### 6. Produce the handoff

`design-handoff.md` answers:
1. What contract objective was implemented?
2. Which files were created or changed?
3. Exact path to open the artifact
4. How to access each variation
5. Build evidence (attempt state, scaffold, acceptance trace)
6. What remains risky, unverified, or deferred?
7. Status: `READY_FOR_REVIEW`, `BUILD_FAILED`, `AWAITING_HUMAN`, or `ESCALATED_TO_HUMAN`

A handoff that says only "done" is invalid.

## Required Output Files

### `.agents-stack/<sprint-id>/design-handoff.md`

```md
# Design Builder Handoff: <SPRINT-ID>

## Status
READY_FOR_REVIEW | BUILD_FAILED | AWAITING_HUMAN | ESCALATED_TO_HUMAN

## Attempt State
- Attempt count:
- Max attempts:
- Clean restore ref:

## Artifact
- Path: .agents-stack/<sprint-id>/artifact/<filename>.html
- Open with: (browser, file://)

## Completed Work
- ...

## Variations Exposed
| Axis | How to access |
|---|---|
| ... | Tweaks panel / section label / slide |

## Build Evidence
(Derived from what was formerly runtime.md — the reviewer's reproduction kit.)

### Artifact Summary
- Type:
- Path: .agents-stack/<sprint-id>/artifact/<filename>.html
- Open with: file:/// path or browser

### Scaffold
- Pattern used: (react-babel | vanilla | deck | animation | wireframe)
- Dependencies: (CDN URLs or none)

### Acceptance Trace
- AC-001 → (what was implemented, where to verify)
- AC-002 → ...
- ...

### Blockers / Gaps
- None | [list]

## Acceptance Trace for Review
- AC-001 → where reviewer should start
- AC-002 → ...

## Reviewer Start Here
1. Open the file at the path above in a browser
2. Open DevTools console — expect zero errors
3. Walk each AC-### from design.md

## Unverified or Risky Areas
- ...
```

### `.agents-stack/<sprint-id>/status.json`

Typical transitions:
- Start / retry: `phase: "building"`, `owner_role: "orchestrator"`, `resume_from: "design.md"` (first pass) or `"design-qa.md"` (retry)
- Ready for review: `phase: "awaiting_review"`, `owner_role: "orchestrator"`, `resume_from: "design-handoff.md"`
- Build failed: `phase: "build_error"`, `owner_role: "orchestrator"`, `resume_from: "design-handoff.md"`, plus `attempt_count`, `max_attempts`, `clean_restore_ref`
- Budget exhausted: `phase: "escalated_to_human"`, `owner_role: "human"`, `escalation_reason`

## Stop Conditions

Route to `design-reviewer` only when all of the following are true:
- Artifact file exists and opens in a browser
- Zero console errors confirmed
- `design-handoff.md` contains the artifact path and per-AC evidence in Build Evidence
- `design-handoff.md` says `READY_FOR_REVIEW`
- `status.json` says `awaiting_review`

Otherwise, stop cleanly and leave the sprint in `build_error`, `awaiting_human`, or `escalated_to_human`.

## Final Checklist

- [ ] `clean_restore_ref` set in `status.json` before any artifact file is written
- [ ] All entry checks passed: `design.md` exists, no unresolved `[human must clarify]` fields, `phase: "design_contracted"` confirmed
- [ ] No content invented beyond what the contract specifies
- [ ] No forbidden visual patterns used (gradient bg, emoji, left-border card, SVG imagery, forbidden fonts)
- [ ] All stateful elements persist via `localStorage` as contracted
- [ ] `scrollIntoView()` not used anywhere in the artifact
- [ ] Minimum contrast (4.5:1 body, 3:1 large text) and touch targets (44×44px) met
- [ ] At least 3 variation axes exposed and accessible
- [ ] `design-handoff.md` contains artifact path and per-AC evidence in Build Evidence section
- [ ] `design-handoff.md` says `READY_FOR_REVIEW` with reviewer start instructions
- [ ] `status.json` set to `awaiting_review`
- [ ] Layered implementation order followed: static → responsive → animation
- [ ] No hardcoded color values (hex, rgb, hsl) — all colors from tokens or oklch() derivations
- [ ] All interactive elements have 5 visual states (default/hover/active/focus/disabled)
- [ ] Single easing family used across all animations
- [ ] Animation timing matches contract hierarchy (100-150ms / 200-300ms / 400-600ms)
- [ ] `prefers-reduced-motion` rule present in CSS
- [ ] No `width`/`height`/`top`/`left` animated — only `transform` and `opacity`
- [ ] 60-30-10 and 80/20 proportions checked (advisory — note any violations in design-handoff.md)
