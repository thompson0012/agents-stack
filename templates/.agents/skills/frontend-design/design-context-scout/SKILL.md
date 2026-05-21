---
name: design-context-scout
description: Use when a design sprint is starting and no trusted design context document exists yet for this feature.
---

# Design Context Scout

## Placement
This is a nested child under `frontend-design`; its path is `frontend-design/design-context-scout/`, and the router selects it before standalone use.

You are the discovery phase of the design harness. Your job is to understand the visual and structural vocabulary of the project before any artifact is scoped or built.

Starting design work without understanding the existing system always produces generic, off-brand results. If no design system exists, that fact must be documented and surfaced as a human gate — it is not an excuse to invent one.

## Worker Dispatch Contract

- Run scouting in a fresh worker context. The orchestrator dispatches; it does not inline scouting.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read-only access to all repo files, plus write access to `.agents-stack/<sprint-id>/context.md` and `.agents-stack/<sprint-id>/status.json`.
- Parallel-safe for read-only discovery across disjoint file areas. One worker owns the context write.
- Dispatch framing is non-authoritative. Verify the dispatched sprint against `.agents-stack/tracked-work.json` and the strongest local artifact before writing.

## Re-Entry Check

Before beginning discovery, check whether `context.md` already exists from a prior scouting run:

- If `context.md` exists and `status.json` shows `phase: "context_ready"` or later → the context was accepted; do not re-scout unless explicitly instructed.
- If `context.md` exists but `status.json` shows `phase: "context_needed"` or `"building"` → the prior run was interrupted; overwrite `context.md` entirely from scratch.
- If `context.md` does not exist → begin discovery normally.

## Discovery Order

Scout in this order. Stop and record what was found at each level before continuing.

### 0. Brand Personality Discovery

Before extracting tokens, define the brand's emotional DNA. This shapes which tokens matter and how the builder should use them.

Check for brand personality signals in:
```
├── .agents-stack/reference/design.md → brand section (if BIE output exists)
├── README.md → project purpose and audience
├── Any moodboard, brand brief, or visual reference files attached by the human
└── Ask: if this brand were a person, what 3-5 emotional keywords describe them? (e.g. "calm, precise, warm" vs "rebellious, fast, neon")
```

Record in context.md:
- **Brand Personality Keywords**: 3-5 emotional descriptors
- **Visual Identity Anchors**: What image or element would a user instantly associate with this brand?
- **Competitive Differentiation**: How does this brand visually differ from competitors in its space?
- **Industry Dialect**: Identify the visual dialect the brand speaks —
  - `tech/saas` → geometric sans-serif, strict grid, single accent, blue/indigo
  - `web3/crypto` → dark background, neon accents, bold wide type, asymmetry, glassmorphism
  - `finance/banking` → humanist sans-serif, symmetry, deep blue, gold/green accents
  - `luxury/fashion` → high-contrast serif, generous white space (60%+), earth tones or monochrome
  - `gaming/esports` → italic/bold display, slanted layouts, high-saturation, glitch/particle effects
  - `content/editorial` → F-pattern layout, reader-friendly type scale, minimal color, high information density

If the project fits none of these, record "custom" and describe the observed dialect in the Visual Vocabulary section.

### 1. Project-Level Design Reference
```
Check in order:
0. .agents-stack/reference/design.md           → brand identity + visual universe + design tokens + component specs + prompt methodology (BIE canonical output)
1. .agents-stack/reference/architecture.md     → tech stack, rendering targets, constraints
2. .agents-stack/insights/session-log.md                → prior design decisions with provenance
3. .agents-stack/ideas.md                 → any design-related brainstorm notes
4. README.md                          → project purpose, audience, screenshot links
```

When `.agents-stack/reference/design.md` is found, parse its structured sections into the Token Inventory:
- **## Visual System YAML block** → Parse the `color_policy`, `design_tokens` (color/spacing/radius/shadow/blur/motion/typography), `form_language`, `material_language`, `scene_density_rules`, `object_library`, `ui_translation`, `negative_prompt_policy`, `input_variables`, `application_presets`, `prompt_seed`, `rule_severity` keys
- **Colors** → `color_policy.dominant_colors`, `color_policy.accent_colors`, `color_policy.text_colors`, `color_policy.glass_colors`
  - If `design.md` contains a BIE Visual System YAML block, also record:
    - `color_policy.dominant_colors` and `color_policy.accent_colors`
    - Count of color scale steps (e.g., "5-step scale (100-500)" or "11-step scale (50-950)")
    - Whether a dark mode mapping exists
- **Typography** → `design_tokens.typography.family_display`, `design_tokens.typography.family_body`, `design_tokens.typography.scale`
- **Spacing & Radius** → `design_tokens.spacing`, `design_tokens.radius`
- **Shadow** → `design_tokens.shadow`
- **Motion** → `design_tokens.motion`
- **Component Inventory** → Prose sections: Component Specifications, Responsive Behaviour, Accessibility Implementation Guide
### 2. Design Token Sources
```
Look for:
- tailwind.config.{js,ts}           → color palette, spacing scale, font stack, radius, shadow
- tokens.css / _variables.scss / design-tokens.{js,ts,json}
- theme.{ts,js} / colors.{ts,js}    → semantic color system
- globals.css / base.css            → root-level CSS custom properties
- .agents-stack/reference/design.md             → BIE canonical output (already checked in Step 1 if found)
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

### `.agents-stack/<sprint-id>/context.md`

```md
# Design Context: <SPRINT-ID>

## Project Summary
- Name:
- Purpose:
- Target audience:
- Primary rendering target: (web / mobile / presentation / print)

## Brand Personality
- Keywords: [3-5 emotional descriptors]
- Visual anchors: [what users associate with this brand]
- Differentiation: [how it differs from industry norms]
- Industry dialect: [tech/saas | web3/crypto | finance/banking | luxury/fashion | gaming/esports | content/editorial | custom]

## Design System Found
- yes | partial | no
- Source files:
  - path → what was extracted

## Token Inventory

### Colors
| Role | Token name | Value | Context |
|---|---|---|---|
| Primary | ... | #RRGGBB | light |
| ... | | | |

- Color scale depth: [number of steps in primary color scale]
- Perceptual uniformity: [OKLCH | LCH | HSL | unknown] — how the color scale was generated
- Dark mode strategy: [token mapping | separate palette | none]

### Typography
| Role | Family | Weight | Size hint |
|---|---|---|---|
| Body | ... | ... | ... |
| Heading | ... | ... | ... |

- Type scale ratio: [modular scale used: 1.25 / 1.414 / custom / unknown]
- Font stack strategy: [system font priority | web font primary | mixed]

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
- Industry dialect constraints: [e.g., "web3: dark background required, neon accents expected"]
- Animation preference: [spring physics | standard easing | none specified]
- Preferred easing family: [cubic-bezier values if found in token files]

## Open Questions for Human
- List any blocking ambiguities (e.g. no color tokens found, no brand brief available)

## Scout Evidence Log
- file paths read:
- tokens confirmed:
- components surveyed:
- gaps or inferences:
```

### `.agents-stack/<sprint-id>/status.json`

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
- records whether dark mode tokens exist and how they map (remapping vs inversion)
- identifies the industry visual dialect when possible
- notes the color scale generation method (OKLCH vs HSL) if discoverable

A context document that invents tokens, fabricates vocabulary, or papers over a missing design system is worse than a document that honestly records "no system found."

## Final Checklist

- [ ] Prior `context.md` checked — if interrupted, overwrite from scratch; if complete and accepted, skip re-scouting
- [ ] All token values cite actual file paths, not assumptions
- [ ] Confirmed tokens distinguished from inferences
- [ ] Open gaps named explicitly (no silent skips)
- [ ] If no design system found: `no_design_system_found: true` in `context.md`, `phase: "awaiting_human"` in `status.json`, `human_action_required` populated
- [ ] If context is complete: `phase: "context_ready"` in `status.json`
