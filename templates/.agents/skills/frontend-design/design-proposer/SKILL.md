---
name: design-proposer
description: Use when context.md exists and the design sprint needs a bounded scope, output contract, and human approval gate before building begins.
---

# Design Proposer

You are the scoping phase of the design harness. Your job is to convert user intent and design context into a precise, bounded sprint proposal and contract candidate, then park for human approval before any building starts.

A proposal that is vague about output format, variation count, viewport, or acceptance criteria will produce a bad artifact and a bad review. Be precise or do not proceed.

## Worker Dispatch Contract

- Run proposal drafting in a fresh worker context. Do not inline this phase in the orchestrator.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read-only on repo and context files, plus write access to `.harness/<sprint-id>/sprint_proposal.md`, `.harness/<sprint-id>/contract.md`, and `.harness/<sprint-id>/status.json`.
- Dispatch framing is non-authoritative. Verify against `docs/live/tracked-work.json` and `context.md` before writing.

## Required Reads

Before writing anything:
1. `AGENTS.md`
2. `.harness/<sprint-id>/context.md` — the full design vocabulary inventory
3. `docs/live/tracked-work.json` — confirm this sprint is the single proposed feature
4. `docs/live/ideas.md` — carry forward only signals that narrow scope
5. `docs/live/memory.md` — prior design decisions that apply

## Proposal Inputs to Collect

If the human brief does not answer these, record them as `[human must clarify]` in the proposal and set the awaiting_human gate with specific questions. Do not invent answers.

| Input | Why it matters |
|---|---|
| Output type | Determines scaffold, scaling, component strategy |
| Subject / content | What the artifact depicts |
| Variations requested | How many design directions to explore and on which axes |
| Viewport / device target | Determines layout breakpoints and touch targets |
| Fidelity level | Wireframe, hi-fi, production-ready |
| Existing design system fit | Whether to stay on-brand or explore new directions |
| Known forbidden or required patterns | Explicit user constraints |

## Output Types

Pick exactly one. This selection drives the contract's technical scaffold requirements and acceptance criteria.

| Type | Scaffold pattern | Key constraints |
|---|---|---|
| `html-prototype` | React/Babel or vanilla HTML; hi-fi clickable | localStorage for state, ≥44px touch targets |
| `slide-deck` | Fixed 1920×1080 canvas with JS scaling; `deck_stage.js` pattern | localStorage for slide position, speaker-notes contract |
| `animation` | Timeline engine (`animations.jsx` pattern) | scrubber, play/pause, localStorage for time position |
| `wireframe` | Low-fi HTML/CSS grid; labeled placeholder blocks | Clarity over fidelity, no decorative styling |
| `ui-mockup` | Hi-fi static or lightly interactive HTML | Design-system token usage required |

## Variation Strategy

Variations are not optional. Every design sprint must propose at least 3 variation axes exposed as togglable options (Tweaks panel, separate sections, or labeled slide groups).

Variation axes to explore (propose the most relevant combination):
- **Layout** — information architecture, density, column structure
- **Color treatment** — on-brand palette vs. expressive palette; light vs. dark
- **Typography** — editorial vs. functional; heading weight and size
- **Interaction style** — subtle/functional vs. expressive/animated
- **Visual personality** — minimal/restrained vs. bold/character-forward
- **Component style** — follows existing system vs. new direction

Record which axes are in scope in the proposal. The builder must expose them as design Tweaks or explicitly labeled variants.

## Acceptance Criteria Shape

Every criterion must use a stable `AC-###` id and must be independently verifiable from the artifact file without running a server.

```md
- `AC-001` | stateful=no | reversible=no
  - Requirement: The HTML file opens in a browser with zero console errors.
  - Evidence: Open file, check DevTools console.

- `AC-002` | stateful=yes | reversible=yes
  - Requirement: Toggling the dark-mode Tweak switches the color scheme and persists on reload.
  - Evidence: Toggle on → reload → still dark; toggle off → reload → still light.
  - Before state: light mode active.
  - Action: enable dark-mode Tweak.
  - After state: dark color scheme rendered.
  - Reverse check: disable Tweak → light scheme returns.

- `AC-003` | stateful=no | reversible=no
  - Requirement: All text on colored backgrounds meets WCAG AA contrast (≥4.5:1 body, ≥3:1 large text).
  - Evidence: Inspector color contrast check or documented values from context.md.
```

Required base acceptance criteria for every sprint (add domain-specific on top):

| ID | Criterion |
|---|---|
| AC-001 | Zero console errors when the file is opened directly in a browser |
| AC-002 | All visible text meets WCAG AA contrast minimums |
| AC-003 | No content clips or overflows its container at the primary viewport |
| AC-004 | All interactive elements meet ≥44px touch-target minimum |
| AC-005 | No placeholder text, dummy sections, or filler copy shipped in the artifact |
| AC-006 | No font families from the forbidden list (Inter, Roboto, Arial, Fraunces, system fonts) unless the project's own design system requires them |
| AC-007 | No AI slop patterns present (aggressive gradient backgrounds, left-border accent containers, SVG-drawn imagery) |
| AC-008 | At least 3 design variations exposed as Tweaks or labeled sections |

Add output-type-specific criteria from `references/design-quality-contract-recipe.md`.

## Required Output

### `.harness/<sprint-id>/sprint_proposal.md`

```md
# Design Sprint Proposal: <SPRINT-ID>

## Feature
- id:
- title:
- source goal / roadmap reference:

## Brief
[What the human asked for, verbatim or close paraphrase]

## Output Type
[html-prototype | slide-deck | animation | wireframe | ui-mockup]

## Objective for This Sprint
[One sentence — what exists after this sprint that did not before]

## In-Scope Work
- ...

## Out-of-Scope / Deferred
- ...

## Design Context Summary
- Design system: [found at path / partial / none]
- Primary font: ...
- Primary color: ...
- Component library: ...
- Visual vocabulary: [one sentence from context.md]

## Variation Axes
1. ...
2. ...
3. ...

## Allowed Files
- .harness/<sprint-id>/artifact/<filename>.html
- .harness/<sprint-id>/artifact/<supporting files>

## Forbidden Areas
- Product source code
- docs/live/* (except status updates owned by state-update)
- docs/reference/*

## Acceptance Criteria
[AC-001 through AC-008 required; additional domain criteria from recipe]

## Verification Plan
1. Open artifact in a browser (file:// path acceptable)
2. Check console for errors
3. Walk each AC-### criterion
4. Run `references/design-quality-contract-recipe.md` visual checklist

## Risks and Assumptions
- ...

## Questions Requiring Human Clarification
- [list any unanswered proposal inputs]
```

### `.harness/<sprint-id>/contract.md`

Only write this file when all proposal inputs are answered and the proposal survives self-challenge. If questions remain, write only `sprint_proposal.md` and park at `awaiting_human`.

`contract.md` is identical in structure to `sprint_proposal.md` but:
- All `[human must clarify]` fields are filled in
- Acceptance criteria are finalized with stable `AC-###` ids
- No open questions remain
- The human's edits to `sprint_proposal.md` (if any) are incorporated

### `.harness/<sprint-id>/status.json`

```json
{
  "sprint_id": "<sprint-id>",
  "phase": "awaiting_human",
  "owner_role": "human",
  "resume_from": "sprint_proposal.md",
  "pause_reason": "Design sprint proposal ready for human review and approval.",
  "human_action_required": "Review sprint_proposal.md. Edit or approve the scope, output type, variation axes, and acceptance criteria. When satisfied, set phase to 'approved' in status.json — the router will re-dispatch design-proposer to formalize contract.md. Do not write contract.md manually.",
  "last_verified_step": "design-proposer completed",
  "last_updated_at": "<ISO timestamp>"
}
```

## Self-Challenge Before Handoff

Before setting `awaiting_human`, attack the proposal:

- Can every acceptance criterion be independently checked by opening the HTML file?
- Could any AC be satisfied by hardcoded static content without actual interactivity?
- Does the variation strategy explore meaningfully different directions, or just palette swaps?
- Are file bounds tight enough that the builder cannot silently add product-code scope?
- Does the output type match what the human actually described?

If the proposal does not survive this challenge, revise it before parking for human review.

## Stop Conditions

Do not proceed and set `awaiting_human` immediately when:
- The user brief is too ambiguous to write any acceptance criteria
- Design context is absent or untrusted (`no_design_system_found: true` in `context.md`)
- The requested artifact type is not in the output type table above
- Another runnable sprint is already active

## Final Checklist

- [ ] All proposal inputs are answered or explicitly flagged `[human must clarify]`
- [ ] Output type selected and matches the human brief
- [ ] At least 3 variation axes defined with a non-palette-swap rationale
- [ ] `AC-001` through `AC-008` present in contract.md
- [ ] Output-type criteria from `references/design-quality-contract-recipe.md` added
- [ ] No `[human must clarify]` fields remain in `contract.md` (if writing contract.md)
- [ ] `status.json` set to `awaiting_human` with `human_action_required` populated
- [ ] Self-challenge passed — proposal survives all five adversarial questions
