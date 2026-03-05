# DESIGN_TOKEN.md

> **Status**: TEMPLATE
> **Brand:** [Brand Name]
> **Version:** 1.0
> **Generated:** [YYYY-MM-DD]
> **Source Skill:** generating-design-tokens v1.2

---

## Brand Discovery Summary

> Fill from project docs (PRD.md, MEMORY.md, product brief) first. Only leave blank if genuinely unknown.

| Question | Answer |
|---|---|
| **Q1 Purpose** | [Why this brand exists — the enemy it fights and the future it creates] |
| **Q2 Persona** | [Name, age, context, key frustration, one quote in their voice] |
| **Q3 Only We** | ["Only we ______." + the single most credible proof] |
| **Q4 Personality** | [3–5 adjectives + would say / would never say examples] |
| **Q5 Desired Perception** | [Want: X, Y, Z — Forbidden: A, B, C] |
| **Q6 Visual References** | [Love: Brand (why). Hate: Brand (why).] |

---

## Phase 1: Conflict Resolution Log

> Record all synthesis decisions here before generating tokens.

| Check | Finding | Resolution |
|---|---|---|
| **1.1 Vibe Check (Q4 vs Q6)** | [Conflict or alignment noted] | [Which governs physics, which governs voice] |
| **1.2 Emotional Territory (Q5 vs Q4/Q6)** | [Any forbidden-word collisions] | [Adjustments made] |
| **1.3 Component Rationalization (Q3)** | [Hero component identified or missing] | [Added / flagged] |
| **1.4 Persona Compatibility (Q2)** | [Density and radius match persona?] | [Adjustments made] |
| **1.5 WCAG Pre-check** | [Text/surface contrast ratio] | [Pass / adjusted to pass] |

---

## Design Principles

> Derived from brand discovery. Every token decision is constrained by at least one principle.

| # | Principle | Source | Token Impact |
|---|-----------|--------|--------------|
| P1 | [e.g., "Craft over convenience"] | Q1 Purpose | [e.g., Muted palette, unhurried spacing] |
| P2 | [e.g., "Radical transparency"] | Q3 Only We | [e.g., No hidden states, no urgency colors] |
| P3 | [e.g., "Human, never corporate"] | Q4 Personality | [e.g., Warm neutrals, soft radius] |
| P4 | [e.g., "Native to [Persona]'s world"] | Q2 Persona | [e.g., Editorial density, no gamification] |
| P5 | [e.g., "[Adjective from Q6 love brand]"] | Q6 References | [e.g., Restraint in shadow and color count] |

---

## Color Tokens

### Palette Rationale

> 2–3 sentences citing Q4 Personality and Q5 Desired Perception. Explain what was rejected and why.

[Replace this with rationale before use.]

```css
/* ─── Core Brand ─────────────────────────────────────────── */
--color-primary:           [hex];   /* [usage note — main CTAs, active states] */
--color-primary-light:     [hex];   /* Hover / focus ring */
--color-primary-dark:      [hex];   /* Pressed state */

/* ─── Surface Stack ──────────────────────────────────────── */
--color-surface-base:      [hex];   /* Page background */
--color-surface-raised:    [hex];   /* Cards, panels */
--color-surface-overlay:   [hex];   /* Modals, drawers */
--color-surface-invert:    [hex];   /* Dark surface for reversed sections */

/* ─── Text Stack ─────────────────────────────────────────── */
--color-text-primary:      [hex];   /* Body — [X.X:1 on surface-base] ✓ WCAG AA */
--color-text-secondary:    [hex];   /* Labels, captions — [X.X:1] ✓ */
--color-text-tertiary:     [hex];   /* Metadata — decorative; not for body copy */
--color-text-disabled:     [hex];   /* Disabled — decorative only */
--color-text-invert:       [hex];   /* Text on invert surfaces */

/* ─── Brand Accent ───────────────────────────────────────── */
--color-accent-[name]:     [hex];   /* [usage — sparingly, hero moments] */

/* ─── Semantic ───────────────────────────────────────────── */
--color-success:           [hex];
--color-warning:           [hex];
--color-error:             [hex];
--color-info:              [hex];

/* ─── Border ─────────────────────────────────────────────── */
--color-border-default:    [hex];   /* Subtle dividers */
--color-border-strong:     [hex];   /* Focused inputs, emphasized borders */
```

---

## Spacing Tokens

> Base unit: **[X]px** — state rationale for base unit choice (4px grid vs. 5px editorial, etc.)

```css
--space-1:   [px];    /* Icon gaps, tight inline */
--space-2:   [px];    /* Chip / badge inner padding */
--space-3:   [px];    /* Form field inner padding */
--space-4:   [px];    /* Card inner padding (default) */
--space-5:   [px];    /* Component-to-component gap */
--space-6:   [px];    /* Section inner padding */
--space-8:   [px];    /* Large section gap */
--space-10:  [px];    /* Content container vertical rhythm */
--space-12:  [px];    /* Section breaks */
--space-16:  [px];    /* Page-level breathing room */
--space-24:  [px];    /* Hero sections */
```

---

## Typography Tokens

### Typeface Rationale

> 1–2 sentences connecting heading and body font choices to Q4 Personality and Q6 Visual References.

[Replace this with rationale before use.]

```css
/* ─── Typefaces ──────────────────────────────────────────── */
--font-family-heading: '[Font]', [fallback], [generic];
--font-family-body:    '[Font]', [fallback], [generic];
--font-family-mono:    '[Font]', [fallback], monospace;

/* ─── Type Scale (state ratio used, e.g. 1.25 Major Third) ─ */
--font-size-xs:   [rem];   /* ~[px] — caption, legal */
--font-size-sm:   [rem];   /* ~[px] — labels, metadata */
--font-size-base: [rem];   /* ~[px] — body copy */
--font-size-md:   [rem];   /* ~[px] — subheadings */
--font-size-lg:   [rem];   /* ~[px] — section headings */
--font-size-xl:   [rem];   /* ~[px] — page titles */
--font-size-2xl:  [rem];   /* ~[px] — hero headings */
--font-size-3xl:  [rem];   /* ~[px] — display / marketing */

/* ─── Weight ─────────────────────────────────────────────── */
--font-weight-light:    300;
--font-weight-regular:  400;
--font-weight-medium:   500;
--font-weight-semibold: 600;
--font-weight-bold:     700;

/* ─── Line Height ────────────────────────────────────────── */
--line-height-tight:    1.2;    /* Headings */
--line-height-snug:     1.35;   /* Subheadings */
--line-height-base:     1.5;    /* Body copy */
--line-height-relaxed:  1.7;    /* Long-form content */
--line-height-loose:    2.0;    /* Intentional open passages */

/* ─── Letter Spacing ─────────────────────────────────────── */
--tracking-tight:   -0.02em;   /* Large display / hero headings */
--tracking-normal:   0em;      /* Body text */
--tracking-wide:     0.05em;   /* Uppercase UI labels */
--tracking-widest:   0.12em;   /* Small caps, metadata badges */
```

---

## Radius Tokens

### Radius Rationale

> 1 sentence connecting radius strategy to Q4 Personality. (e.g., "Soft 8px radius reflects warmth without feeling playful-DTC.")

[Replace this with rationale before use.]

```css
--radius-none:   0px;      /* Tables, data cells, code blocks */
--radius-xs:     [px];     /* Inline tags, small chips */
--radius-sm:     [px];     /* Input fields, secondary buttons */
--radius-md:     [px];     /* Primary buttons, cards */
--radius-lg:     [px];     /* Modals, drawers, feature cards */
--radius-xl:     [px];     /* Hero panels, large surface insets */
--radius-full:   9999px;   /* Avatars, status dots, badges only */
```

---

## Shadow / Depth Tokens

### Depth Rationale

> 1 sentence connecting depth strategy to Q6 Visual References. (e.g., "Border-first, Are.na-inspired — shadows signal interactivity only.")

[Replace this with rationale before use.]

```css
--shadow-none:  none;

--shadow-xs:    [css value];   /* Subtle — input focus alternative */
--shadow-sm:    [css value];   /* Cards at rest */
--shadow-md:    [css value];   /* Cards on hover, elevated panels */
--shadow-lg:    [css value];   /* Modals, bottom sheets */
--shadow-xl:    [css value];   /* Sticky navs, floating toasts */
```

---

## Motion Tokens

> State the motion personality in 1 sentence (e.g., "Unhurried and considered — no bounce, no urgency.").

[Replace this with rationale before use.]

```css
/* ─── Duration ───────────────────────────────────────────── */
--duration-instant:  0ms;
--duration-fast:     [ms];   /* Hover, focus ring */
--duration-base:     [ms];   /* Button state, chip toggle */
--duration-moderate: [ms];   /* Card expand, panel slide */
--duration-slow:     [ms];   /* Modal enter, page transition */
--duration-crawl:    [ms];   /* Signature animations, hero reveals */

/* ─── Easing ─────────────────────────────────────────────── */
--easing-standard:  cubic-bezier(0.4, 0, 0.2, 1);    /* Default */
--easing-enter:     cubic-bezier(0.0, 0.0, 0.2, 1);  /* Decelerate in */
--easing-exit:      cubic-bezier(0.4, 0, 1.0, 1);    /* Accelerate out */
--easing-craft:     cubic-bezier(0.25, 0.1, 0.25, 1);/* Refined hero transitions */
/* Add --easing-spring only if Q4 personality explicitly warrants playfulness */
```

---

## Validation Report

> Check every item before marking this document complete.

- [ ] **Consistency:** Radius tokens match Radius Rationale direction (sharp/rounded).
- [ ] **WCAG AA:** `--color-text-primary` contrast ratio stated and ≥ 4.5:1 on `--color-surface-base`.
- [ ] **Principles Traceable:** Every Design Principle row has a named Token Impact, and at least one token implements it.
- [ ] **Persona Fit:** Token density and radius suit the Q2 persona's cognitive and aesthetic expectations.
- [ ] **No Forbidden Patterns:** Q5 forbidden words do not describe any token choice.
- [ ] **Hero Component:** At least one component (if inventory included) directly proves the Q3 "Only We" claim.
- [ ] **Conflict Resolution:** All Phase 1 conflicts resolved and logged.

**Conflict Notes:** [Describe resolved tensions, or "None detected."]
