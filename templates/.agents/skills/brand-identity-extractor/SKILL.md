---
name: brand-identity-extractor
description: Use when extracting a production-ready brand identity and design system from curated reference images, mood boards, or brand descriptions. Triggers include requests to "extract brand identity", "create brand design system", "define brand DNA", "generate design tokens from images", "build a brand from moodboard", "create AI image prompts from brand", "design AI prompt methodology for brand", or "systematize brand identity for front-end handoff". Also triggers when the user provides reference images and asks for a structured brand output or AI image generation prompts.
---

# Brand Identity Extractor

Extract a complete, production-ready Brand Design System + Front-end Handoff Kit + AI Image Generation Asset Kit + Prompt Design Methodology from curated reference images, text descriptions, or mood boards.

Three stages: **Define → Handoff → Generate**

## Core Contract

- Extract only what the inputs support — do not invent
- Produce all 3 stages — skipping any section is a failure
- Include both affirmative rules (DO) and negative constraints (DON'T)
- Output design tokens in copy-paste-ready JSON
- Translate brand into concrete AI image generation prompts, not just adjectives
- Produce a prompt design methodology that teaches how to design brand-consistent AI image prompts — the "how to think" layer above the templates

---

## Phase 0: Brand Discovery & Conflict Resolution

Before extraction begins, establish the brand's foundational context. Skip this phase only if all 6 Brand Questions are already answered in provided inputs, or if the user is extending an existing brand with a pre-validated `docs/reference/design.md`.

### 0.1 Source Discovery (Do This Before Asking Any Question)

Scan existing project documents for brand inputs before asking the user anything:

Check in order:
1. `docs/reference/design.md`     → product intent, behavior, brand direction
2. `docs/insights/session-log.md`          → durable decisions, brand notes
3. `docs/` or product/ folders    → roadmap docs, vision docs, brand briefs
4. `README.md`                    → project purpose, audience

| Discovery Question | Look For In Docs |
|---|---|
| Q1 Purpose & Worldview | Problem statement, mission, "why we exist" |
| Q2 Persona | User personas, target audience, Jobs to be Done |
| Q3 Only We | Differentiators, unique features, competitive advantage |
| Q4 Personality & Voice | Tone of voice, brand values, writing guidelines |
| Q5 Desired Perception | Brand success metrics, positioning goals |
| Q6 Visual References | Mood boards, design inspiration, "what we are/aren't" |

**Rule:** If a question is answered in docs, use it — label the source as `【From: filename.md】`. Only ask for what genuinely cannot be found. Ask up to 3 clarifying questions per round; if the user still cannot answer, proceed with labeled `【Assumption: ...】`.

### 0.2 The 6 Brand Questions

**Q1 — Purpose & Worldview** *(Brand DNA foundation)*
> "Why does this brand exist beyond making money, and what change in the world are you obsessed with creating?"

Collect: 1–2 paragraphs. Must contain a clear enemy/problem and the better future it fights for. Drives overall visual tone — activist/bold vs. gentle/nurturing.

**Q2 — Audience Empathy** *(Persona)*
> "Describe your ideal customer as a real person — name, age, daily frustrations, dreams."

Collect: 150–300 word character sketch. Drives component roundness, color saturation, icon style, density.

**Q3 — Positioning & Proof** *("Only We" differentiation)*
> "Finish: 'Only we ______.' Give me the single most credible piece of proof."

Collect: One ownable sentence + one concrete proof (feature, policy, or technology competitors can't easily copy). Drives Hero Component selection.

**Q4 — Personality & Voice** *(Direct style driver)*
> "If your brand were a person at a bar, how would they speak? What would they never say?"

Collect: 3–5 personality adjectives + 3–5 phrases they'd say + 2–3 they'd never say. Drives color mood, typography weight, motion style, microcopy tone.

**Q5 — Desired Perception** *(Emotional north-star)*
> "In 12–24 months, what 3–5 words do you want users to describe this brand with? What 3 words would make you die inside?"

Collect: Positive list (3–5). Forbidden list (3–4). Every token must land in this territory.

**Q6 — Visual References & Taste** *(Translation accelerator)*
> "Show me 4–6 brands (any industry) that feel like us, and 3–4 that are the opposite. One sentence love/hate per brand."

Collect: Brand names + one-sentence love/hate note each. Drives concrete color, type, and component decisions.

### 0.3 Conflict Resolution (Run Before Any Output)

Resolve all conflicts silently. Never output tokens before completing all 5 checks.

**Check 1 — Vibe Check (Q4 vs Q6):** Do Personality adjectives match Visual References' aesthetic? Conflict rule: Visual References govern **physics** (layout, radius, shadow, density); Personality governs **voice** (microcopy, motion energy, empty states).

**Check 2 — Emotional Territory Check (Q5 vs Q4/Q6):** Do Q5 "forbidden words" describe any current direction? If yes → adjust palette or radius before output.

**Check 3 — Component Rationalization (Q3):** Does at least one planned component directly prove the "Only We" claim? If none → add a Hero Component and flag it.

**Check 4 — Persona Compatibility Check (Q2):** Does token density and radius suit the persona's world? Design-literate → moderate density, editorial radius. Consumer → more air, softer radius.

**Check 5 — WCAG AA Pre-check:** Text on surface: minimum **4.5:1** body, **3:1** large text. Fail → adjust token before output. Never output a failing contrast.

---

## Workflow

### Step 1: Gather Inputs

The user provides one or more of:
- 1–10 curated reference images (Pinterest, Behance, Dribbble, AI-generated)
- Brand manifesto, vision statement, or personality keywords
- Competitor references (what to absorb / what to avoid)
- Mood descriptors (industry, audience, desired feeling)

Image curation sources to suggest:
- Pinterest: search `[industry/mood] + "aesthetic"`
- Behance: browse industry portfolios
- Dribbble: UI trends in the target space
- AI generation: Midjourney, DALL-E, Stable Diffusion

If no images are given, rely on textual input. Ask clarifying questions only when too vague.

Phase 0 handles all brand discovery and conflict resolution. If inputs are already complete with answers to all 6 Brand Questions, Phase 0 auto-detects this and skips to extraction.

### Step 2: Run the Brand Extract Meta-Prompt

Copy the meta-prompt from [brand-extract-meta-prompt.md](assets/brand-extract-meta-prompt.md) and paste it into a reasoning model (O1, DeepSeek, Claude) with the user's inputs. The meta-prompt produces all 3 stages in one pass.

### Step 3: Validate Completeness

After receiving the output, verify all 10 output sections are present:

**Stage 1 — Brand Definition:**
1. Brand Soul
2. Visual Universe (Color, Form, Material, Composition, Object Library)
3. Typography & Voice
4. Brand Rulebook

**Stage 2 — Design System & Front-end Handoff:**
5. Core Design Tokens (JSON)
6. Component Specifications (all states table)
7. Responsive Behaviour (breakpoints)
8. Motion & Interaction Design
9. Accessibility Implementation Guide
10. Code Configuration (CSS/Tailwind/Figma)

**Stage 3 — AI Image Generation:**
11. Core Style Prompt + Negative Prompt Bank
12. Prompt Templates (5 copy-paste templates)
13. Image Consistency Validation Checklist

14. Prompt Design Technique Methodology

If any section is missing or sparse, prompt the model again with specific gaps.

### Step 4: Cross-check Token Validity

For extracted hex values and numeric tokens, verify against [design-standards](references/design-standards.md):
- Body text ≥ 16px
- Button/input height ≥ 44px (tap target)
- Contrast ratios (4.5:1 normal text, 3:1 large text)
- Spacing scale (systematic, not arbitrary)
- AI prompt negative keywords match Stage 1 forbidden lists

### Step 5: Write to `docs/reference/design.md`

`design.md` is the **single canonical design reference** for the project (per `AGENTS.md`). All brand identity content goes here. External artifacts are referenced from it — never duplicated.

**Write the Visual Universe as a YAML block under `## Visual System`:**
Stage 1 B.1–B.5 (Color Philosophy, Form Language, Material Library, Composition DNA, Object Library) must be written as a single structured YAML block inside `## Visual System`, following the v2.0 brand identity schema. The YAML block must include: `color_policy`, `design_tokens` (spacing, radius, shadow, blur, motion, typography), `form_language`, `material_language`, `scene_density_rules`, `object_library`, `ui_translation`, `negative_prompt_policy`, `input_variables`, `application_presets`, `prompt_seed`, and `rule_severity`. See `docs/reference/design.md` for the canonical schema structure.

**Write inline to `design.md` (prose sections):**
- Stage 1: Brand Soul, Typography & Voice, Brand Rulebook
- Stage 2: Component Specifications, Responsive Behaviour, Motion & Interaction Design, Accessibility Implementation Guide, Design QA Checklist
- Stage 3: Core Style Prompt, Negative Prompt Bank, Prompt Design Technique Methodology, Image Consistency Validation Checklist

**Write to external files under `docs/records/design/`, reference from `design.md` with a relative link:**
- Design Tokens → `docs/records/design/design-tokens.json` (JSON block from Stage 2.1)
- CSS Custom Properties → `docs/records/design/design-tokens.css` (from Stage 2.7)
- Tailwind Config → project Tailwind config file (extension snippet from Stage 2.7)
- Figma Variables → `docs/records/design/figma-variables.json` (from Stage 2.7)
- Prompt Templates → `docs/records/design/ai-prompt-templates.md` (5 templates from Stage 3.4)
- Tool-Specific Parameters → `docs/records/design/ai-prompt-params.md` (from Stage 3.3)
Mark any inferential gaps. If a section's content is entirely covered by an external file, write a one-paragraph summary in `design.md` with the reference link.

## Cross-Skill Integration

These skills work well with BIE in a loose pipeline — no hard dependency, just recommended sequencing:

| Skill | Role | When to route |
|---|---|---|
| [`prompt-augmentation`](../prompt-augmentation/SKILL.md) | **Stage 3 enrichment** | Feed BIE's AI prompt output (Core Style, Negative Bank, templates) into `prompt-augmentation` with `text-to-image` mode for domain-specific term substitution (optics, lighting, composition, materials). |
| [`frontend-design/design-context-scout`](../frontend-design/design-context-scout/SKILL.md) | **Downstream consumer** | BIE's output in `docs/reference/design.md` (YAML block under `## Visual System` for machine-readable tokens, prose sections for human context) is consumed by `design-context-scout` as a design system source for UI sprint planning. |

## Bundled Resources

- [Meta-Prompt](assets/brand-extract-meta-prompt.md) — copy-pasteable 3-stage prompt for reasoning models
- [Design Standards](references/design-standards.md) — measurable token validation criteria
- [Prompt Design Technique Playbook](references/prompt-design-playbook.md) — 10-technique methodology for designing brand-consistent AI image prompts

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Vague brand output (just "clean and modern") | Input too sparse | Ask user for 3+ reference images |
| Inconsistent palette | Conflicting inputs not resolved | Force primary/secondary hierarchy, don't blend |
| Missing negative constraints | Model skipped rulebook | Re-prompt: "Add DON'T rules for X" |
| Invented details not in inputs | Model hallucinating | Re-prompt with constraint emphasis |
| Missing component states | Model only gave default state | Prompt: "Add hover/active/disabled/loading states" |
| AI prompts too generic | Stage 1 detail not fed into Stage 3 | Re-prompt: "Derive AI prompts from form language, material, and color philosophy in Stage 1" |
| Negative prompt contradicts brand | Generic quality keywords only | Re-prompt: "Add brand-specific forbidden colors/forms/materials to negative" |
| Prompt design methodology missing | Model stopped at templates | Re-prompt: "Add section 3.6 with all 10 techniques, derived from Stage 1 brand identity" |
| Methodology uses generic examples | Model didn't ground in brand specifics | Re-prompt: "Replace generic examples with brand-specific colors, shapes, and concepts from Section B" |
| Shape motifs reused across concepts | No exclusivity enforcement | Re-prompt: "Audit all geometric metaphors — each concept must use a unique shape family. Document forbidden shapes per concept." |

## Checklist

- [ ] User provided 1-10 reference images or brand text
- [ ] Meta-prompt ran with user inputs
- [ ] All 3 stages are produced (Define, Handoff, Generate)
- [ ] Design tokens are in valid JSON
- [ ] Component specs include all states (default/hover/active/disabled/loading)
- [ ] AI prompts include Core Style, Negative Bank, 5 templates, and design methodology (all 10 techniques)
- [ ] Methodology techniques are grounded in Stage 1 brand specifics (not generic examples)
- [ ] Token values meet accessibility minimums (body ≥ 16px, tap ≥ 44px, contrast ≥ 4.5:1)
- [ ] Negative constraints are explicit in both Brand Rulebook and AI Negative Bank
- [ ] Inferred values are explicitly marked as inferences
- [ ] Output ready for designer, front-end dev, content creator, and QA

- [ ] All inline content is written to `docs/reference/design.md` as the single canonical entry point
- [ ] External artifacts (tokens JSON, CSS, Tailwind config, prompt templates) are written to separate files and referenced from `design.md`