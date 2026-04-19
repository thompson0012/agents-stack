---
name: design-builder
description: Use when contract.md is approved and the design artifact must be implemented.
purpose: Produce the HTML artifact within the approved contract scope, record reproducible delivery evidence, and hand off only verifiable work.
trigger: After human has approved `.harness/<sprint-id>/contract.md` and `status.json` shows `phase: "contracted"`.
inputs:
  - AGENTS.md
  - .harness/<sprint-id>/contract.md
  - .harness/<sprint-id>/context.md
  - docs/reference/design.md
  - docs/live/memory.md
  - .harness/<sprint-id>/status.json
outputs:
  - .harness/<sprint-id>/artifact/<filename>.html (and supporting files)
  - .harness/<sprint-id>/runtime.md
  - .harness/<sprint-id>/handoff.md
  - .harness/<sprint-id>/status.json
boundaries:
  - Do not widen scope beyond contract.md.
  - Do not self-approve or write review.md.
  - Do not edit product source code or docs/live/*.
  - Do not ship filler content, placeholder text, or invented data.
  - Do not use forbidden design patterns (see Quality Rules below).
next_skills:
  - design-reviewer
  - state-update
---

# Design Builder

You are the implementation phase of the design harness. Your job is to produce a high-quality, verifiable HTML artifact that exactly matches the approved contract — nothing more, nothing less.

Producing a beautiful artifact that violates the contract is still a failure. Producing a correct artifact that uses AI slop patterns is still a failure.

## Worker Dispatch Contract

- Run in a fresh worker context. The orchestrator dispatches; it does not inline building.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: write access to `.harness/<sprint-id>/artifact/`, `.harness/<sprint-id>/runtime.md`, `.harness/<sprint-id>/handoff.md`, `.harness/<sprint-id>/status.json`. No edits to product code, docs/live/*, or docs/reference/*.
- Dispatch framing is non-authoritative. Verify against `contract.md` and `docs/live/tracked-work.json` before writing.

## Required Entry Checks

Before writing any code:
1. `contract.md` exists and all `[human must clarify]` fields are resolved.
2. `context.md` exists and contains at minimum: output type, visual vocabulary, and token inventory.
3. `status.json` shows `phase: "contracted"` or a valid retry phase with `clean_restore_ref`.
4. If this is a retry: confirm `attempt_count < max_attempts` and `clean_restore_ref` names a valid restore point.

If any check fails, stop. Record the gap in `runtime.md`, set `phase: "awaiting_human"`, and return.

## Source of Truth

Work from `contract.md`, not from the conversation.

Binding sections:
- objective
- output type
- allowed files
- forbidden areas
- acceptance criteria (all `AC-###` ids)
- variation axes

`context.md` provides the design vocabulary; it does not override the contract. If they conflict, preserve the conflict in `runtime.md` and stop.

## Retry Discipline

When resuming after `review_failed` or `build_failed`:
- restore from `clean_restore_ref` before beginning the next attempt
- increment `attempt_count` at the start of the attempt, not at the end
- if `attempt_count` would exceed `max_attempts`, set `phase: "escalated_to_human"` immediately

## Build Procedure

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
- Hi-fi HTML using tokens from `context.md`.
- Use `oklch()` for any supplementary colors not in the token inventory, deriving from the existing palette.

### 2. Apply design vocabulary from context.md

Before writing component code:
- Set CSS custom properties from the token inventory in `:root`
- Use only font families found in `context.md`; if none were found, pick one from the non-forbidden list (not Inter, not Roboto, not Arial, not Fraunces)
- Use spacing and radius values from the token inventory
- Match the visual vocabulary described in `context.md` (density, corner style, shadow, icon style)

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
- No emoji unless `context.md` documents the brand uses them
- No containers styled with `border-left: 4px solid <accent>` + rounded corners as a card treatment
- No imagery drawn with inline SVG paths; use labeled placeholder boxes (`<div class="img-placeholder">` styled with a neutral fill) or reference actual project assets
- No AI-generated color palettes invented from scratch when token inventory exists

#### Typography
- Never use: Inter, Roboto, Arial, Fraunces, or generic `system-ui` unless the project's own design system requires them and `context.md` confirms this
- Minimum font sizes: 24px for 1920×1080 fixed canvas; 12px for print; 16px for web body
- Apply `text-wrap: pretty` on paragraph text

#### Interaction
- Never use `scrollIntoView()` — use other DOM scroll methods when scrolling is needed
- `localStorage` persistence required for: current slide index, current animation time, and any Tweak values
- All interactive state changes must be reversible if the contract marks them reversible

#### Accessibility
- All text on colored backgrounds: ≥4.5:1 contrast (body), ≥3:1 (large text ≥18px bold or ≥24px regular)
- All interactive touch targets: minimum 44×44px
- Focusable interactive elements must have visible focus styles

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

`runtime.md` is the reviewer's reproduction kit, not a progress diary.

Record:
- Exact file path(s) of the artifact
- How to open it: `file:///path/to/artifact.html` or equivalent
- Output type and scaffold used
- Variation axes exposed and how to access them
- For each `AC-###` from the contract: what was implemented and where the reviewer should look
- Any known gaps, warnings, or intentional deferrals

### 6. Produce a real handoff

`handoff.md` answers:
1. What contract objective was implemented?
2. Which files were created or changed?
3. Exact path to open the artifact
4. How to access each variation
5. Evidence already captured in `runtime.md`
6. What remains risky, unverified, or deferred?
7. Status: `READY_FOR_REVIEW`, `BUILD_FAILED`, `AWAITING_HUMAN`, or `ESCALATED_TO_HUMAN`

A handoff that says only "done" is invalid.

## Required Output Files

### `.harness/<sprint-id>/runtime.md`

```md
# Runtime Notes: <SPRINT-ID>

## Attempt State
- Attempt count:
- Max attempts:
- Clean restore ref:

## Artifact
- Type:
- Path: .harness/<sprint-id>/artifact/<filename>.html
- Open with: file:/// path or browser

## Scaffold
- Pattern used: (react-babel | vanilla | deck | animation | wireframe)
- Dependencies: (CDN URLs or none)

## Variations
| Axis | How to access |
|---|---|
| ... | Tweaks panel / section label / slide |

## Acceptance Trace
- AC-001 → (what was implemented, where to verify)
- AC-002 → ...
- ...

## Blockers / Gaps
- None
```

### `.harness/<sprint-id>/handoff.md`

```md
# Design Builder Handoff: <SPRINT-ID>

## Status
READY_FOR_REVIEW | BUILD_FAILED | AWAITING_HUMAN | ESCALATED_TO_HUMAN

## Attempt State
- Attempt count:
- Max attempts:
- Clean restore ref:

## Artifact
- Path: .harness/<sprint-id>/artifact/<filename>.html
- Open with: (browser, file://)

## Completed Work
- ...

## Variations Exposed
- ...

## Acceptance Trace for Review
- AC-001 → where reviewer should start
- AC-002 → ...

## Reviewer Start Here
1. Open the file at the path above in a browser
2. Open DevTools console — expect zero errors
3. Walk each AC-### from contract.md

## Unverified or Risky Areas
- ...
```

### `.harness/<sprint-id>/status.json`

Typical transitions:
- Start / retry: `phase: "building"`, `owner_role: "orchestrator"`, `resume_from: "contract.md"` (first pass) or `"review.md"` (retry)
- Ready for review: `phase: "awaiting_review"`, `owner_role: "orchestrator"`, `resume_from: "handoff.md"`
- Build failed: `phase: "build_failed"`, `owner_role: "orchestrator"`, `resume_from: "runtime.md"`, plus `attempt_count`, `max_attempts`, `clean_restore_ref`
- Budget exhausted: `phase: "escalated_to_human"`, `owner_role: "human"`, `escalation_reason`

## Stop Conditions

Route to `design-reviewer` only when all of the following are true:
- Artifact file exists and opens in a browser
- Zero console errors confirmed
- `runtime.md` contains the artifact path and per-AC evidence
- `handoff.md` says `READY_FOR_REVIEW`
- `status.json` says `awaiting_review`

Otherwise, stop cleanly and leave the sprint in `build_failed`, `awaiting_human`, or `escalated_to_human`.
