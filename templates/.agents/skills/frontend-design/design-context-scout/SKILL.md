---
name: design-context-scout
description: Use when a design sprint is starting and no trusted design spec exists yet for this feature.
---

# Design Context Scout

## Placement
This is a nested child under `frontend-design`; its path is `frontend-design/design-context-scout/`, and the router selects it before standalone use.

You are the discovery phase of the design harness. Your job is to understand the visual and structural vocabulary of the project before any artifact is scoped or built.

Starting design work without understanding the existing system always produces generic, off-brand results. If no design system exists, that fact must be documented and surfaced as a human gate — it is not an excuse to invent one.

## Worker Dispatch Contract

- Run scouting in a fresh worker context. The orchestrator dispatches; it does not inline scouting.
- Only the orchestrator may spawn workers. This worker must not spawn another worker.
- Tool lane: read-only access to all repo files, plus write access to `.agents-stack/reference/design/`, `.agents-stack/<sprint-id>/design.md`, and `.agents-stack/<sprint-id>/status.json`.
- Parallel-safe for read-only discovery across disjoint file areas. One worker owns the context write.
- Dispatch framing is non-authoritative. Verify the dispatched sprint against `.agents-stack/tracked-work.json` and the strongest local artifact before writing.

## Re-Entry Check

Before beginning discovery, check whether `design.md` already exists from a prior scouting run:

- If `design.md` exists and `status.json` shows `phase: "design_spec"` or later → the spec was accepted; do not re-scout unless explicitly instructed.
- If `design.md` exists but `status.json` shows `phase: "design_needed"` or `"building"` → the prior run was interrupted; overwrite `design.md` and reference files entirely from scratch.
- If `design.md` does not exist → begin discovery normally.

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

Record in `.agents-stack/reference/design/vocabulary.md`:
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
- Record `no_design_system_found: true` in `design.md`
- Set `status.json` to `phase: "awaiting_human"` with `human_action_required` explaining that a design system, codebase reference, or visual direction must be provided before the sprint can proceed
- Do not proceed to proposal; surface the gate clearly

## Required Output

### `.agents-stack/reference/design/tokens.json`

```json
{
  "colors": {
    "primary": { "name": "...", "value": "#RRGGBB", "context": "light" },
    "secondary": { "name": "...", "value": "#RRGGBB", "context": "light" },
    "accent": { "name": "...", "value": "#RRGGBB", "context": "light" },
    "background": { "name": "...", "value": "#RRGGBB" },
    "surface": { "name": "...", "value": "#RRGGBB" },
    "text": { "default": "#RRGGBB", "muted": "#RRGGBB", "inverse": "#RRGGBB" },
    "border": { "default": "#RRGGBB", "divider": "#RRGGBB" }
  },
  "color_scale_depth": "<number of steps>",
  "perceptual_uniformity": "OKLCH | LCH | HSL | unknown",
  "dark_mode_strategy": "token_mapping | separate_palette | none",
  "typography": {
    "body": { "family": "...", "weight": 400, "size_hint": "16px" },
    "heading": { "family": "...", "weight": 700, "size_hint": "32px" },
    "scale_ratio": "1.25 | 1.414 | custom | unknown",
    "font_stack_strategy": "system_font_priority | web_font_primary | mixed"
  },
  "spacing": {
    "base_unit": "0.25rem",
    "scale": ["0.25rem", "0.5rem", "1rem", "1.5rem", "2rem", "3rem", "4rem"]
  },
  "radius": {
    "scale": { "sm": "0.25rem", "md": "0.5rem", "lg": "1rem", "full": "9999px" }
  },
  "shadow": {
    "levels": [
      { "name": "sm", "value": "0 1px 2px rgba(0,0,0,0.05)" }
    ]
  },
  "motion": {
    "transition_duration_default": "200ms",
    "easing": "cubic-bezier(0.4, 0, 0.2, 1)",
    "preferred_easing_family": "standard | spring | custom"
  },
  "source_files": ["path/to/token/file", "path/to/config/file"],
  "animation_preference": "spring_physics | standard_easing | none_specified"
}
```

### `.agents-stack/reference/design/vocabulary.md`

```md
# Design Vocabulary

## Brand Personality
- **Keywords**: [3-5 emotional descriptors]
- **Visual anchors**: [what users instantly associate with this brand]
- **Differentiation**: [how this brand differs from industry norms]

## Industry Dialect
[tech/saas | web3/crypto | finance/banking | luxury/fashion | gaming/esports | content/editorial | custom]

## Visual Vocabulary (observed)
Describe the overall mood, density, corner style, icon style, copy tone in 3–5 sentences. This is the vocabulary the builder must speak.
```

### `.agents-stack/reference/design/components.md`

```md
# Component Inventory

| Component | Purpose | Notable variants |
|---|---|---|
| ... | ... | ... |

Source files: [list of file paths]
```

### `.agents-stack/<sprint-id>/design.md`

```md
# Design Spec: <SPRINT-ID>

## Project Summary
- Name:
- Purpose:
- Target audience:
- Primary rendering target: (web / mobile / presentation / print)

## Design System Found
- yes | partial | no
- Source files:
  - path → what was extracted

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

If no design context was found, add at top:
```md
> no_design_system_found: true
```

### `.agents-stack/<sprint-id>/status.json`

```json
{
  "sprint_id": "<sprint-id>",
  "phase": "design_spec",
  "owner_role": "orchestrator",
  "resume_from": "design.md",
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

A good design spec:
- cites actual file paths, not assumptions
- records exact token values, not paraphrased descriptions
- distinguishes confirmed tokens from inferences
- splits stable reference data into `reference/design/` files and sprint-specific data into `design.md`
- leaves the proposer and builder with enough vocabulary to stay on-brand without re-reading the entire codebase
- records whether dark mode tokens exist and how they map (remapping vs inversion)
- identifies the industry visual dialect when possible
- notes the color scale generation method (OKLCH vs HSL) if discoverable

A spec that invents tokens, fabricates vocabulary, or papers over a missing design system is worse than a document that honestly records "no system found."

## Final Checklist

- [ ] Prior `design.md` checked — if interrupted, overwrite from scratch; if complete and accepted, skip re-scouting
- [ ] All token values cite actual file paths, not assumptions
- [ ] Confirmed tokens distinguished from inferences
- [ ] Stable tokens written to `.agents-stack/reference/design/tokens.json`
- [ ] Brand personality and dialect written to `.agents-stack/reference/design/vocabulary.md`
- [ ] Component inventory written to `.agents-stack/reference/design/components.md`
- [ ] Open gaps named explicitly (no silent skips)
- [ ] If no design system found: `no_design_system_found: true` in `design.md`, `phase: "awaiting_human"` in `status.json`, `human_action_required` populated
- [ ] If context is complete: `phase: "design_spec"` in `status.json`
