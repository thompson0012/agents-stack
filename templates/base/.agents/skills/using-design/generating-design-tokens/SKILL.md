---
name: generating-design-tokens
description: Use when turning brand inputs or existing product docs into a portable design-token spec, brand system, or brand spec with traceable decisions and resolved visual conflicts.
---

# Generating Design Tokens

## Overview

Transforms brand discovery inputs into a conflict-free, specification-ready design token spec. Resolves input tensions (e.g., warm personality vs. restrained visual references), derives atomic design tokens, and records design principles — all traceable back to discovery sources.

**Primary output:** a design token spec document (for example `docs/reference/design.md` or a project-specific brand spec)
**Extended output:** `Brand_System_Architecture.md` (tokens + component inventory)

---

## When to Use

- Brand discovery answers exist (any of the 6 questions below)
- Need atomic design tokens (color, spacing, radius, typography, shadow, motion)
- Inputs contain potential conflicts (personality vs. visual references)
- Output target: a design token spec or `Brand_System_Architecture.md`

**Do NOT use for:**
- Pure copywriting with no visual output
- Code-level implementation → use `tailwind-design-system` or `ui-ux-pro-max`
- One-off component design without brand context

---

## Step 0: Source Discovery (Do This Before Asking Any Question)

**Before asking the user anything**, scan existing project documents for brand inputs. Many questions may already be answered.

```
Check in order:
1. docs/reference/design.md     → product intent, behavior, brand direction
2. docs/reference/memory.md     → durable decisions, brand notes
3. docs/ or product/ folders    → roadmap docs, vision docs, brand briefs
4. README.md                    → project purpose, audience
```

**Extraction map** — what to pull from existing docs:

| Discovery Question | Look For In Docs |
|---|---|
| Q1 Purpose & Worldview | Problem statement, mission, "why we exist" |
| Q2 Persona | User personas, target audience, Jobs to be Done |
| Q3 Only We | Differentiators, unique features, competitive advantage |
| Q4 Personality & Voice | Tone of voice, brand values, writing guidelines |
| Q5 Desired Perception | Brand success metrics, positioning goals |
| Q6 Visual References | Mood boards, design inspiration, "what we are/aren't" |

**Rule:** If a question is answered in docs, use it — label the source as `【From: filename.md】`. Only ask for what genuinely cannot be found.

**Missing info rule:** Ask up to 3 clarifying questions per round. If the user still can't provide them, proceed with labeled `【Assumption: ...】`.

---

## Discovery Framework v1.2 — The 6 Brand Questions

### Q1 — Purpose & Worldview *(Brand DNA foundation)*
> "Why does this brand exist beyond making money, and what change in the world are you obsessed with creating?"

**Collect:** 1–2 paragraphs. Must contain a clear enemy/problem and the better future it fights for. Emotional, not corporate.
**What it drives:** Overall visual tone — activist/bold vs. gentle/nurturing.
**Example:** "Most coffee apps are corporate loyalty schemes. We exist to help independent roasters build direct relationships with coffee lovers. We're fighting commoditized coffee and soulless chains."

---

### Q2 — Audience Empathy *(Persona)*
> "Describe your ideal customer as a real person — name, age, daily frustrations, dreams, and current belief about this category."

**Collect:** 150–300 word character sketch: name, age, job/lifestyle, top 3 fears, what success looks like, one quote in their voice.
**What it drives:** Component roundness, color saturation, icon style, density.
**Example:** "Lena, 29, freelance designer, Berlin. Hates subscription lock-ins. 'I never know if I'm supporting the roaster or just middlemen.'"

---

### Q3 — Positioning & Proof *("Only We" differentiation)*
> "Finish: 'Only we ______.' Then give me the single most credible piece of proof."

**Collect:** One ownable sentence + one concrete proof (feature, policy, or technology competitors can't easily copy).
**What it drives:** Hero component selection — the UI must prove this claim at first glance.
**Example:** "Only we show the exact farm→roast→doorstep journey per bag." Proof: live origin map + in-app roaster chat.

---

### Q4 — Personality & Voice *(Human layer — direct style driver)*
> "If your brand were a person at a bar, how would they speak? What would they never say?"

**Collect:** 3–5 personality adjectives + 3–5 phrases the brand would say + 2–3 it would never say.
**What it drives:** Color palette mood, typography weight, motion style, spacing rhythm, microcopy tone.
**Example:** Warm, craft-obsessed, transparent. Would say: "Harvested by Fatima in March." Would never say: "Limited drop — 48 hrs only!!"

---

### Q5 — Desired Perception *(Emotional north-star)*
> "In 12–24 months, what 3–5 words do you want users to describe this brand with? What 3 words would make you die inside?"

**Collect:** Positive list (3–5). Forbidden list (3–4).
**What it drives:** Final emotional target — every token must land in this territory.
**Example:** Want: "Authentic, thoughtful, craft-first." Forbidden: "Corporate, trendy, disposable."

---

### Q6 — Visual References & Taste *(Translation accelerator)*
> "Show me 4–6 brands (any industry) that feel like us, and 3–4 that are the opposite. One sentence love/hate per brand."

**Collect:** Brand names + one-sentence love/hate note each.
**What it drives:** Concrete color, type, and component decisions.
**Example:** Love: Are.na (quiet curation), Muji (restraint), Courier mag (craft warmth). Hate: Starbucks app (gamified loyalty), Goop (performative exclusivity).

---

## Phase 1: Strategic Synthesis (Internal — Run Before Any Output)

Resolve all conflicts silently. Never output tokens before completing all 5 checks.

### 1.1 Vibe Check (Q4 vs Q6)
- Do Personality adjectives match Visual References' aesthetic?
- **Conflict rule:** Visual References govern **physics** (layout, radius, shadow, density); Personality governs **voice** (microcopy, motion energy, empty states).

### 1.2 Emotional Territory Check (Q5 vs Q4/Q6)
- Do Q5 "forbidden words" describe any current direction?
- If yes → adjust palette or radius before output.

### 1.3 Component Rationalization (Q3)
- Does at least one planned component directly prove the "Only We" claim?
- If none → add a Hero Component and flag it.

### 1.4 Persona Compatibility Check (Q2)
- Does token density and radius suit the persona's world?
- Design-literate → moderate density, editorial radius. Consumer → more air, softer radius.

### 1.5 WCAG AA Pre-check
- Text on surface: minimum **4.5:1** body, **3:1** large text.
- Fail → adjust token before output. Never output a failing contrast.

---

## Phase 2: Output — Design Token Spec

Use the project's preferred docs location for the token spec. If the repo follows this kit, add the token guidance to `docs/reference/design.md` or create a clearly named brand spec alongside the reference docs.

Key rules when filling:
- Every **Rationale** block must cite its discovery source (Q1–Q6 or `【From: filename.md】`).
- Every **Design Principle** row must name a Token Impact.
- All color values: hex only (`#RRGGBB`). No RGB, no named colors.
- All token names: `--kebab-case` CSS custom properties.
- Append the **Validation Report** with every item checked before saving.

---

## Phase 3: Extended Output — Brand_System_Architecture.md

When a full spec (tokens + component inventory) is requested, extend the design token spec output with:

```csv
ID,Priority,Name,Rationale
C01,Critical,"[Hero Component]","Directly proves Q3 'Only We' claim: [restate briefly]."
C02,Critical,"[Nav Pattern]","Primary wayfinding for [Q2 Persona] — [reason]."
C03,Essential,"[Component]","[Why needed for the use case]."
C04,Essential,"[Component]","[Why needed for the use case]."
C05,Nice-to-have,"[Component]","[Enhancement, non-blocking for launch]."
```

Priority levels: `Critical` → `Essential` → `Nice-to-have`

---

## Quick Reference

| Rule | Behavior |
|---|---|
| Docs exist with brand info | Extract first — label `【From: filename】`; only ask what's missing |
| Q4 clashes with Q6 | Q6 governs physics; Q4 governs voice |
| Q5 forbidden words match current direction | Pivot palette or radius before output |
| No Hero Component for Q3 claim | Add one, flag it explicitly |
| WCAG fails | Adjust token; never output failing contrast |
| Missing Q1–Q6 after doc check | Ask max 3 questions; then `【Assumption: ...】` |
| Opening greetings | **Forbidden** — start with Design Principles table |
| RGB or named colors | **Forbidden** — hex only |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Asking all 6 questions when docs have answers | Run Step 0 first; only ask what's genuinely missing |
| Skipping Phase 1 synthesis | Phase 1 resolves conflicts that change token values — never skip |
| Token names not in CSS custom property format | `--kebab-case` only; never `tokenName` or `SCREAMING_SNAKE` |
| Rationale blocks with no discovery source citation | Every rationale must cite its Q source or doc source |
| Inventing contrast ratios | State "unverified — flag for review" if you cannot calculate |
| Forgetting Validation Report | Append it always, without exception |
| Generating tokens before Phase 1 | Phase 1 can pivot palette choices — always run first |
