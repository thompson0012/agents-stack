---
name: design-context-scout
description: Use when a design sprint is starting and no trusted design context document exists yet for this feature.
purpose: Explore the repository and any provided design sources to produce a durable design context document that the proposer and builder can work from.
trigger: When `.harness/<sprint-id>/context.md` is absent or flagged stale, before `design-proposer` can begin scoping.
inputs:
  - AGENTS.md
  - docs/reference/design.md
  - docs/reference/architecture.md
  - docs/live/tracked-work.json
  - docs/live/ideas.md
  - docs/live/memory.md
  - codebase component and styling files (see Discovery Order below)
  - any attached screenshots, Figma links, or brand briefs provided by the human
outputs:
  - .harness/<sprint-id>/context.md
  - .harness/<sprint-id>/status.json
boundaries:
  - Do not produce a proposal, contract, or artifact.
  - Do not invent design tokens or vocabulary that are not grounded in actual repo evidence or explicit human input.
  - Do not bulk-copy design assets; reference and describe them.
  - Do not start building anything.
next_skills:
  - design-proposer
---

# Design Context Scout

You are the discovery phase of the design harness. Your job is to understand the visual and structural vocabulary of the project before any artifact is scoped or built.

Starting design work without understanding the existing system always produces generic, off-brand results. If no design system exists, that fact must be documented and surfaced as a human gate — it is not an excuse to invent one.

## Worker Dispatch Contract

- Run scouting in a fresh worker context. The orchestrator dispatches; it does not inline scouting.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read-only access to all repo files, plus write access to `.harness/<sprint-id>/context.md` and `.harness/<sprint-id>/status.json`.
- Parallel-safe for read-only discovery across disjoint file areas. One worker owns the context write.
- Dispatch framing is non-authoritative. Verify the dispatched sprint against `docs/live/tracked-work.json` and the strongest local artifact before writing.

## Discovery Order

Scout in this order. Stop and record what was found at each level before continuing.

### 1. Project-Level Design Reference
```
Check in order:
1. docs/reference/design.md          → product intent, brand, visual system
2. docs/reference/architecture.md    → tech stack, rendering targets, constraints
3. docs/live/memory.md               → prior design decisions with provenance
4. docs/live/ideas.md                → any design-related brainstorm notes
5. README.md                         → project purpose, audience, screenshot links
```

### 2. Design Token Sources
```
Look for:
- tailwind.config.{js,ts}           → color palette, spacing scale, font stack, radius, shadow
- tokens.css / _variables.scss / design-tokens.{js,ts,json}
- theme.{ts,js} / colors.{ts,js}    → semantic color system
- globals.css / base.css            → root-level CSS custom properties
```

For each token file found, extract:
- primary/secondary/accent color values (exact hex)
- background and surface colors
- text colors (default, muted, inverse)
- border/divider colors
- spacing scale if defined
- border-radius scale
- shadow/elevation levels
- font families and weight scale
- motion: transition duration, easing presets

### 3. Component Library Inventory
```
Look for:
- src/components/ or components/
- ui/, lib/ui/, design-system/
- stories/ or *.stories.{ts,tsx,js,jsx}  → component props and variants
- *.module.css / *.styled.{ts,tsx}       → component-scoped tokens
```

For each component found, extract:
- component name and primary purpose
- variant names (size, color, state)
- notable visual traits (rounded, bordered, shadow, icon-adjacent)
- any known interaction states (hover, active, disabled, loading)

### 4. Existing UI Screenshots or Live Pages
If the human attached screenshots, Figma links, or a URL:
- Describe the visual vocabulary observed: color mood, type treatment, density, radius, iconography style
- Note any patterns the new work must match

### 5. No Context Found
If steps 1–4 produce no usable design context:
- Record `no_design_system_found: true` in `context.md`
- Set `status.json` to `phase: "awaiting_human"` with `human_action_required` explaining that a design system, codebase reference, or visual direction must be provided before the sprint can proceed
- Do not proceed to proposal; surface the gate clearly

## Required Output

### `.harness/<sprint-id>/context.md`

```md
# Design Context: <SPRINT-ID>

## Project Summary
- Name:
- Purpose:
- Target audience:
- Primary rendering target: (web / mobile / presentation / print)

## Design System Found
- yes | partial | no
- Source files:
  - path → what was extracted

## Token Inventory

### Colors
| Role | Token name | Value |
|---|---|---|
| Primary | ... | #RRGGBB |
| ... | | |

### Typography
| Role | Family | Weight | Size hint |
|---|---|---|---|
| Body | ... | ... | ... |
| Heading | ... | ... | ... |

### Spacing & Radius
- Base spacing unit:
- Border radius scale: (sm / md / lg / full values)

### Shadow / Elevation
- ...

### Motion
- Transition duration default:
- Easing:

## Component Inventory
| Component | Purpose | Notable variants |
|---|---|---|
| ... | ... | ... |

## Visual Vocabulary (observed)
Describe the overall mood, density, corner style, icon style, copy tone in 3–5 sentences. This is the vocabulary the builder must speak.

## Design Constraints
- Fonts in use: (list actual families; flag if any are overused: Inter, Roboto, Arial, Fraunces)
- Emoji policy: (brand uses / brand does not use / unknown)
- Known forbidden patterns: (gradient-heavy backgrounds, left-border accent cards, etc. as found)
- Accessibility baseline: (WCAG AA / unknown)

## Open Questions for Human
- List any blocking ambiguities (e.g. no color tokens found, no brand brief available)

## Scout Evidence Log
- file paths read:
- tokens confirmed:
- components surveyed:
- gaps or inferences:
```

### `.harness/<sprint-id>/status.json`

```json
{
  "sprint_id": "<sprint-id>",
  "phase": "context_ready",
  "owner_role": "orchestrator",
  "resume_from": "context.md",
  "last_verified_step": "design-context-scout completed",
  "last_updated_at": "<ISO timestamp>"
}
```

If no design context was found, set `phase: "awaiting_human"` and add:
```json
{
  "pause_reason": "No design system or visual reference found in repo.",
  "human_action_required": "Attach design system files, screenshots, Figma link, or brand brief before scouting can complete."
}
```

## Quality Bar

A good context document:
- cites actual file paths, not assumptions
- records exact token values, not paraphrased descriptions
- distinguishes confirmed tokens from inferences
- names open gaps explicitly rather than silently skipping them
- leaves the proposer and builder with enough vocabulary to stay on-brand without re-reading the entire codebase

A context document that invents tokens, fabricates vocabulary, or papers over a missing design system is worse than a document that honestly records "no system found."
