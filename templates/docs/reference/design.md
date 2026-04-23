# Design Reference

Current stable truth for product intent, visual system, interaction model, and design constraints.

Updated only when a lesson becomes broadly current truth. For sprint-level observations, use `docs/live/memory.md` or `docs/records/*` instead.

---

## Product Intent

### Purpose & Worldview
Why does this product exist beyond making money, and what change is it obsessed with creating?

- **Enemy / Problem:**
- **Better future it fights for:**
- **One-sentence purpose:**

### Target Audience
Describe the ideal user as a real person.

- **Name / Archetype:**
- **Age / Lifestyle:**
- **Top 3 frustrations:**
- **What success looks like:**
- **One quote in their voice:**

### "Only We"
Finish: "Only we ______."

- **Ownable claim:**
- **Single most credible proof:**

---

## Visual System

### Color Palette
All values in hex (`#RRGGBB`). Rationale must cite a discovery source.

| Role | Token | Value | Rationale |
|------|-------|-------|-----------|
| Primary | `--color-primary` | | |
| Primary Hover | `--color-primary-hover` | | |
| Secondary | `--color-secondary` | | |
| Accent | `--color-accent` | | |
| Background | `--color-bg` | | |
| Surface | `--color-surface` | | |
| Text Default | `--color-text` | | |
| Text Muted | `--color-text-muted` | | |
| Text Inverse | `--color-text-inverse` | | |
| Border | `--color-border` | | |
| Error | `--color-error` | | |
| Success | `--color-success` | | |
| Warning | `--color-warning` | | |

### Typography
| Role | Family | Weight | Size Scale | Usage |
|------|--------|--------|------------|-------|
| Display | | | | Hero, largest headings |
| Heading | | | | Section headings |
| Body | | | | Paragraphs, descriptions |
| Label | | | | Buttons, inputs, captions |
| Mono | | | | Code, data, timestamps |

### Spacing & Radius
- **Base spacing unit:**
- **Spacing scale:** (e.g. 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64)
- **Border radius scale:** (sm / md / lg / full values)

### Shadow / Elevation
| Level | Token | Value | Usage |
|-------|-------|-------|-------|
| 1 (subtle) | `--shadow-sm` | | Cards at rest |
| 2 (raised) | `--shadow-md` | | Hover, dropdowns |
| 3 (floating) | `--shadow-lg` | | Modals, toasts |

### Motion
- **Default transition duration:**
- **Default easing:**
- **Reduced-motion fallback:**

---

## Brand Voice

### Personality Adjectives
(3-5 words)

### What We Would Say
(3-5 example phrases)

### What We Would Never Say
(2-3 example phrases)

### Desired Perception
- **Want users to describe us as:**
- **Forbidden words that would make us die inside:**

---

## Design Principles

Every principle must name a Token Impact.

| Principle | Rationale | Token Impact |
|-----------|-----------|--------------|
| | | |

---

## Interaction Model

### Primary Flows
| Flow | Entry Point | Key States | Exit Criteria |
|------|-------------|------------|---------------|
| | | | |

### Key Patterns
- **Navigation:**
- **Feedback:**
- **Error Recovery:**
- **Loading:**

---

## Constraints

### Tech Stack
- Rendering target: (web / mobile / desktop / presentation / print)
- Framework constraints:
- Supported browsers / platforms:

### Accessibility Baseline
- Target standard: (WCAG 2.1 AA / AAA / unknown)
- Minimum contrast: body 4.5:1, large text 3:1
- Keyboard navigation: (full / partial / none)
- Screen reader testing: (required / optional / unknown)

### Forbidden Patterns
Explicitly list patterns the brand must avoid.

- Gradient-heavy backgrounds
- Left-border accent cards
- (Add project-specific forbidden patterns as discovered)

### Emoji Policy
(brand uses / brand does not use / unknown)

---

## Durable Decisions

Record provenance-linked design decisions that are now stable truth.

Format:

```
YYYY-MM-DD — Decision summary
- Source: sprint-id, record, or artifact path
- Reason: why this decision was made
- Scope: what it affects
```

---

## Validation Report

Append a brief checklist before saving changes to this file.

- [ ] Every color value is hex only (`#RRGGBB`)
- [ ] Every rationale cites a discovery source
- [ ] Every design principle names a Token Impact
- [ ] Contrast ratios pass WCAG AA (or flagged as unverified)
- [ ] No RGB, no named colors, no `tokenName` or `SCREAMING_SNAKE`
