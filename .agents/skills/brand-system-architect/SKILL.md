---
name: brand-system-architect
description: Use when synthesizing brand discovery inputs into a unified design system architecture or design token document. Triggers include "create a design system", "build a brand spec", "generate design tokens", "generate DESIGN_TOKEN.md", "generate Brand_System_Architecture.md", or when brand discovery answers (purpose, audience, differentiator, personality, perception, visual references) are provided and a conflict-free design spec is needed.
---

# Brand System Architect

## Overview

Acts as **Chief Design Officer** to transform raw brand discovery answers into a conflict-free, specification-ready design system. Resolves input tensions (e.g., warm personality vs. restrained visual references), produces atomic design tokens, and outputs a prioritized component inventory — all in one document.

**Primary output:** `DESIGN_TOKEN.md` (tokens) and/or `Brand_System_Architecture.md` (full spec).

## When to Use

- Brand discovery answers are provided (any of the 6 questions below)
- Inputs contain potential conflicts (personality vs. visual references)
- Need atomic design tokens (color, spacing, radius, typography, shadow)
- Need a component inventory tied to a "Only We" differentiator
- Output target: `DESIGN_TOKEN.md` or `Brand_System_Architecture.md`

**Do NOT use for:**
- Pure copywriting with no visual output
- Code-level implementation (use `tailwind-design-system` or `ui-ux-pro-max` for that)
- One-off component design without brand context

---

## Discovery Framework v1.2 — The 6 Brand Questions

These are the canonical inputs. Collect ALL before generating. Ask up to 3 clarifying questions if answers are missing; proceed with labeled `【Assumption: ...】` if the user cannot provide them.

### Q1 — Purpose & Worldview *(Brand DNA foundation)*
> "Why does this brand exist beyond making money, and what change in the world are you obsessed with creating?"

**Collect:** 1–2 paragraphs. Must contain a clear enemy/problem and the better future it fights for. Emotional, not corporate.

**What it drives:** Overall visual tone, whether the design feels activist/bold or gentle/nurturing.

**Example:** "Most coffee apps are corporate loyalty schemes or hipster review aggregators. We exist to help independent roasters build direct relationships with coffee lovers who care where their beans come from. We're fighting commoditized coffee and soulless chains."

---

### Q2 — Audience Empathy *(Persona)*
> "Describe your ideal customer as if they're a real person sitting next to us right now — name, age, daily frustrations, dreams, and current belief about this category."

**Collect:** 150–300 word character sketch. Include: name, age, job/lifestyle, top 3 fears, what success looks like, where they hang out, one quote in their own voice.

**What it drives:** Component roundness, color saturation, icon style, density — must feel native to this person's world.

**Example:** "Meet Lena, 29, freelance graphic designer in Berlin. Buys beans 2–3×/month, follows small roasters on Instagram, hates subscription lock-ins. 'I never know if I'm actually supporting the roaster or just middlemen.' Success = every bag puts money straight into the hands of growers and roasters."

---

### Q3 — Positioning & Proof *("Only We" differentiation)*
> "Finish this sentence: 'Only we ______.' Then give me the single most credible piece of proof."

**Collect:** One ownable sentence + one concrete proof (feature, policy, technology, or result competitors can't easily copy).

**What it drives:** Hero component selection — the UI must visually prove this claim at first glance.

**Example:** "Only we let customers message the roaster directly and see the exact farm→roast→doorstep journey for every bag." Proof: In-app chat with the actual roaster + live map tracing every batch from origin.

---

### Q4 — Personality & Voice *(Human layer — direct style driver)*
> "If your brand were a person at a bar, how would you describe their personality and speech? What would they never say?"

**Collect:** 3–5 personality adjectives + 3–5 phrases the brand would say + 2–3 it would never say.

**What it drives:** Color palette mood, typography weight, motion style, spacing rhythm, microcopy tone.

**Example:**
- Personality: Warm, craft-obsessed, transparent, slightly geeky, proud but never pretentious.
- Would say: "This Yemen lot was harvested by Fatima and her co-op in March — here's the video."
- Would never say: "Limited drop — 48 hours only!!" / "Coffee that slaps."

---

### Q5 — Desired Perception *(Emotional north-star)*
> "In 12–24 months, what exact 3–5 words do you want users to describe this brand with? And what 3 words would make you die inside?"

**Collect:** Positive list (3–5 adjectives). Forbidden list (3–4 words to avoid at all costs).

**What it drives:** Final emotional target — every token value must land inside this emotional territory.

**Example:**
- Want: "Authentic, thoughtful, craft-first, human."
- Would die: "Corporate, trendy, influencer-y, disposable."

---

### Q6 — Visual References & Taste *(Translation accelerator)*
> "Show me 4–6 brands (any industry) that feel spiritually like us, and 3–4 that are the complete opposite. For each, tell me exactly what you love or hate."

**Collect:** Brand names or links + one-sentence love/hate note per brand.

**What it drives:** Concrete color, type, and component decisions — translates DNA into pixels in hours not months.

**Example:**
- Love: Are.na (quiet curation), Muji digital (restraint), Courier magazine (craft warmth), Letterboxd (passionate, never try-hard).
- Hate: Starbucks app (gamified loyalty), DTC drops brands (fake scarcity), Goop (performative exclusivity).

---

## Phase 1: Strategic Synthesis (Internal — Do This Before Any Output)

Resolve all conflicts silently before writing a single token.

### 1.1 Vibe Check
- Cross-reference Q4 (Personality) against Q6 (Visual References).
- **Conflict rule:** If they clash → Visual References govern **physics** (layout, radius, shadow, density); Personality governs **voice** (microcopy, labels, empty states, motion energy).

### 1.2 Emotional Territory Check
- Cross-reference Q5 (Desired Perception) against Q4 (Personality) and Q6 (Visual References).
- If "authentic/human" is desired but visual refs are cold and corporate → warm the palette neutrals; keep structure disciplined.

### 1.3 Component Rationalization
- Identify the Q3 "Only We" claim.
- Confirm at least one **Hero Component** in the inventory directly proves it.
- If none exists → add one and flag it.

### 1.4 Persona Compatibility Check
- Cross-reference Q2 (Persona) against token density and radius decisions.
- A technically-literate persona tolerates higher density and sharper radii; a creative/lifestyle persona needs more air and softness.

### 1.5 WCAG AA Pre-check
- Minimum contrast: **4.5:1** body text on surface, **3:1** large text.
- Verify before writing any color token. If it fails, adjust before output.

---

## Phase 2A: Output — DESIGN_TOKEN.md

Use this structure when the primary output requested is design tokens.

```markdown
# DESIGN_TOKEN.md
> Brand: [Brand Name]  
> Version: 1.0  
> Generated: [Date]  
> Architect: Brand System Architect v1.2

---

## Design Principles

Derived from brand discovery. These principles constrain every token decision.

| # | Principle | Source | Token Impact |
|---|-----------|--------|--------------|
| P1 | [e.g., "Craft over convenience"] | Q1 Purpose | Muted palette, unhurried spacing |
| P2 | [e.g., "Radical transparency"] | Q3 Only We | Journey-tracker component; no hidden states |
| P3 | [e.g., "Human, never corporate"] | Q4 Personality | Warm neutrals, soft radius, personal typography |
| P4 | [e.g., "Lena's world — not a loyalty app"] | Q2 Persona | High readability, no gamification colors |

---

## Color Tokens

### Palette Rationale
[2–3 sentences explaining why these colors were chosen in terms of Q4 Personality and Q5 Desired Perception.]

```css
/* Core Palette */
--color-primary:        [hex];   /* [usage note] */
--color-primary-light:  [hex];   /* Hover / focus states */
--color-primary-dark:   [hex];   /* Pressed / active states */

/* Surface Stack */
--color-surface-base:   [hex];   /* Page background */
--color-surface-raised: [hex];   /* Cards, panels */
--color-surface-overlay:[hex];   /* Modals, drawers */

/* Text Stack */
--color-text-primary:   [hex];   /* Body — [X.X:1 on surface-base] WCAG AA ✓ */
--color-text-secondary: [hex];   /* Labels, captions — [X.X:1] */
--color-text-disabled:  [hex];   /* Disabled state — decorative only */

/* Semantic */
--color-success:        [hex];
--color-warning:        [hex];
--color-error:          [hex];
--color-info:           [hex];

/* Brand Accent */
--color-accent:         [hex];   /* Sparingly — hero moments only */
```

---

## Spacing Tokens

```css
/* Base unit: [Xpx] — all spacing is multiples */
--space-1:  [calc];   /* [Xpx]  — icon gaps, tight inline */
--space-2:  [calc];   /* [Xpx]  — form field padding */
--space-3:  [calc];   /* [Xpx]  — component inner padding */
--space-4:  [calc];   /* [Xpx]  — card padding */
--space-6:  [calc];   /* [Xpx]  — section gaps */
--space-8:  [calc];   /* [Xpx]  — large section breaks */
--space-12: [calc];   /* [Xpx]  — page-level breathing room */
--space-16: [calc];   /* [Xpx]  — hero spacing */
```

---

## Typography Tokens

### Typeface Rationale
[1–2 sentences connecting font choices to Q4 Personality and Q6 Visual References.]

```css
/* Typefaces */
--font-family-heading: '[Font]', [fallback stack];
--font-family-body:    '[Font]', [fallback stack];
--font-family-mono:    '[Font]', monospace;

/* Scale */
--font-size-xs:   [rem];   /* Caption, legal */
--font-size-sm:   [rem];   /* Labels, metadata */
--font-size-base: [rem];   /* Body copy */
--font-size-md:   [rem];   /* Subheadings */
--font-size-lg:   [rem];   /* Section titles */
--font-size-xl:   [rem];   /* Page headings */
--font-size-2xl:  [rem];   /* Hero headings */
--font-size-3xl:  [rem];   /* Display / marketing */

/* Weight */
--font-weight-regular: 400;
--font-weight-medium:  500;
--font-weight-bold:    700;

/* Line Height */
--line-height-tight:   1.2;   /* Headings */
--line-height-base:    1.5;   /* Body */
--line-height-loose:   1.75;  /* Long-form content */

/* Letter Spacing */
--tracking-tight:  -0.02em;  /* Large display text */
--tracking-normal:  0em;
--tracking-wide:    0.05em;  /* Uppercase labels */
```

---

## Radius Tokens

### Radius Rationale
[1 sentence connecting radius strategy to Q4 Personality.]

```css
--radius-none:   0px;
--radius-sm:     [px];   /* Inputs, inline chips */
--radius-md:     [px];   /* Buttons, cards */
--radius-lg:     [px];   /* Modals, panels */
--radius-xl:     [px];   /* Feature cards, hero sections */
--radius-full:   9999px; /* Pills, avatars, badges */
```

---

## Shadow / Depth Tokens

### Depth Rationale
[1 sentence connecting depth strategy to Q6 Visual References.]

```css
--shadow-none:    none;
--shadow-xs:      [css value];   /* Subtle lift — inputs on focus */
--shadow-sm:      [css value];   /* Cards at rest */
--shadow-md:      [css value];   /* Cards on hover */
--shadow-lg:      [css value];   /* Modals, dropdowns */
--shadow-xl:      [css value];   /* Sticky elements, toasts */
```

---

## Motion Tokens

```css
--duration-instant: 0ms;
--duration-fast:    [ms];   /* Micro-interactions (hover, focus) */
--duration-base:    [ms];   /* Component transitions */
--duration-slow:    [ms];   /* Page/modal enter/exit */

--easing-default:   cubic-bezier(0.4, 0, 0.2, 1);  /* Material standard */
--easing-enter:     cubic-bezier(0, 0, 0.2, 1);     /* Decelerate in */
--easing-exit:      cubic-bezier(0.4, 0, 1, 1);     /* Accelerate out */
--easing-spring:    cubic-bezier(0.34, 1.56, 0.64, 1); /* Playful bounce */
```

---

## Validation Report

- [ ] **Consistency:** Radius tokens match Radius Rationale direction (sharp/rounded).
- [ ] **WCAG AA:** `--color-text-primary` contrast ratio stated and ≥ 4.5:1 on `--color-surface-base`.
- [ ] **Principles Traceable:** Every Design Principle in the table has at least one token that implements it.
- [ ] **Persona Fit:** Token density and radius suit the Q2 persona's cognitive and aesthetic expectations.
- [ ] **Conflict Resolution:** Any Q4 vs Q6 clash resolved and noted below.

**Conflict Notes:** [Tensions resolved, or "None detected."]
```

---

## Phase 2B: Output — Brand_System_Architecture.md

Use this structure when a full spec (tokens + component inventory) is requested.

Extend Phase 2A output with:

### Section C: Component Inventory

```csv
ID,Priority,Name,Rationale
C01,Critical,"[Hero Component]","Directly proves the Q3 'Only We' claim: [restate claim briefly]."
C02,Critical,"[Nav Pattern]","Primary wayfinding for [Q2 Persona name] — [why they need it]."
C03,Essential,"[Component]","[Why needed for the primary use case]."
C04,Essential,"[Component]","[Why needed for the primary use case]."
C05,Nice-to-have,"[Component]","[Enhancement, non-blocking for launch]."
```

Priority levels: `Critical` → `Essential` → `Nice-to-have`

---

## Quick Reference

| Rule | Behavior |
|---|---|
| Q4 clashes with Q6 | Q6 governs physics (layout/radius/depth); Q4 governs voice (copy/motion energy) |
| Q5 "forbidden words" match current direction | Pivot the palette or radius before generating tokens |
| No Hero Component proves Q3 claim | Add one and flag it explicitly |
| WCAG fails before output | Adjust token; never output a failing contrast |
| Missing any Q1–Q6 answer | Ask up to 3 questions; then use labeled `【Assumption: ...】` |
| Opening greetings | **Forbidden** — start with Design Principles table immediately |
| RGB or named colors | **Forbidden** — hex only (`#RRGGBB` or `#RRGGBBAA`) |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping Phase 1 synthesis | Always run all 5 checks — Q5 forbidden words often catch palette errors |
| Token names not CSS custom property format | `--kebab-case` only; never `tokenName` or `SCREAMING_SNAKE` |
| Inventing contrast ratios | State "unverified — flag for review" if you cannot calculate |
| Design Principles table with no token impact column | Every principle must trace to at least one concrete token decision |
| Forgetting Validation Report | Append always, without exception |
| Generating tokens before Phase 1 | Phase 1 resolves conflicts that change token values — never skip |
