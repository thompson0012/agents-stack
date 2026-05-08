# Prompt Design Technique Playbook

Systematic methodology for translating brand identity into AI image generation prompts. Use when designing prompts for Midjourney, DALL-E, Stable Diffusion, or any text-to-image model.

**Goal**: In a strict brand aesthetic framework, use the fewest formal elements to convey the richest conceptual information.

---

## 1. Color Ratio Control & Brand Constraint Internalization

**Principle**: Treat the brand color palette as a hard constraint. Verify before each generation that accent colors do not exceed their allocation (typically 60-30-10 or similar).

**Technique**:
- Declare color ratios explicitly in prompts: `"85% pearl white / 12% clear ice blue / 3% dawn orange"`
- Integrate accent colors through gradients, glows, and shadows — not through solid blocks
- Check: is the accent color acting as a dominant element? If yes, reduce to a rim light, edge glow, or subsurface scatter

**Prompt Keywords**: `"color ratio", "dominant tone X", "accent only as rim light / subtle glow"`

**Negative Prompt**: Forbidden color territories from the brand rulebook — e.g., `"no pure black, no neon, no heavy darks"`

---

## 2. Abstract Concept → Geometric Metaphor Mapping

**Principle**: Extract key nouns from the brand's conceptual vocabulary, then find semantically associated geometric shapes or structures.

**Method**:
1. List core abstract concepts (e.g., "memory," "attention," "collaboration," "openness")
2. For each concept, ask: what shape or structure embodies this?
3. Map concept → geometry:


**The mapping is always brand-specific — never copy the examples below.** The following table is an illustration of method, not a fixed vocabulary:

| Concept | Geometric Metaphor |
|---------|-------------------|
| Memory trace | Curved glass ribbon + branching paths |
| Attention heatmap | Grid + variably-sized glowing hemispheres |
| Protocol handshake | Twin columns facing each other + serrated light arc |
| Open source → commercial | Open cube (floating internal particles) → closed cylinder (solid) |
| Growth / evolution | Spiral, unfurling frond, ascending steps |
| Connection / network | Nodes + threads, lattice, interlocking rings |
| Protection / security | Shield, dome, concentric barriers |
| Precision / accuracy | Crosshair, grid alignment, ruled lines |

**Check**: Does the geometry feel like a natural translation of the brand's specific concept, not an arbitrary or generic symbol?

---

## 3. Shape System Differentiation (Anti-Homogenization)

**Principle**: Assign mutually exclusive geometric motifs to different concepts. No two concepts should share the same shape family.

**Technique**:
- Create a shape assignment table: each concept card gets a unique geometric mother motif
- Enforce: if Card 1 uses **ribbons / branching**, forbid rings, cylinders, spheres in Card 1
- If Card 2 uses **grids / hemispheres**, forbid spirals, tubes, ribbons in Card 2
- If Card 3 uses **twin columns / serrated arcs**, forbid cubes, spheres, ribbons in Card 3

**Why**: Without this rule, generated images converge toward the same generic forms. Differentiation must be designed, not discovered.

**Audit**: After generating all prompts, check — does any geometric motif appear in more than one concept? If yes, replace one.

---

## 4. Material Language Unification + Detail Differentiation

**Principle**: All objects share a fixed material vocabulary, but primary and auxiliary elements get different material assignments.


**The lexicon below is an example only — each brand defines its own materials from Stage 1 B.3.** Do not copy these entries; derive the actual material list from the brand's own visual universe.

- **Frosted glass** — translucent, blurred edges, soft diffusion
- **Ceramic white** — solid, smooth, matte with subtle specular highlights
- **Clear glass** — transparent, refractive edges, crisp reflections
- **Pearl luster** — iridescent, soft gradient sheen
- **Metal accents** — brushed, anodized, fine grain (only for trim, ≤5% area)

**Role-Based Assignment** (brand-specific — derive material roles from Stage 1):
- Primary focal object → solid, opaque material from the brand lexicon (presence)
- Auxiliary / background structures → translucent, recessive material (depth, ambiguity)
- Accent / energy elements → luminous material or brand accent color glow

**Prompt Format**: `"[object]: [material], [surface detail], [light interaction]"`  
Example: `"central form: smooth ceramic white, subtle pearl sheen, soft rim light from upper left"`

---

## 5. Negative Space & Floating Composition

**Principle**: Objects should float in unbounded space, not sit on a surface.

**Technique**:
- All objects must not touch card edges; bottom margin > top margin
- Use extremely subtle projections: `dx=0, dy=6~12, blur=12~20`, ice-blue tinted
- Background: radial gradient with no horizon line, no depth anchor
- Eliminate any ground plane, table surface, or environmental context

**Prompt Keywords**: `"floating composition, no ground plane, radial gradient background, centered in void, subtle shadow beneath, no contact with edges"`

**Negative Prompt**: `"floor, ground, table, surface, horizon line, shadow on ground"`

---

## 6. Dynamic Suggestion (Static Image)

**Principle**: Convey motion and process through asymmetry and directional cues, without actual animation.

**Technique**:
- Asymmetric composition: weight shifted to one side, implied direction
- Directional light: key light from one angle creates flow
- Growth cues: branching, unfurling, ascending trajectories
- Transition cues: particles moving from one state to another (open → closed, scattered → gathered)
- Tension cues: elements balanced at a tilt, just before equilibrium

**Prompt Keywords**: `"implied motion, directional flow, asymmetrical balance, light from upper left, dynamic stillness"`

---

## 7. Restrained Complexity: The 1–3 + 1–2 Rule

**Principle**: Per image, limit to 1–3 primary objects + 1–2 auxiliary structures. Remove everything else.

**Checklist Before Finalizing a Prompt**:
- [ ] Primary objects: 1–3 maximum
- [ ] Auxiliary structures: 1–2 maximum  
- [ ] Removed: extra dots, decorative lines, redundant elements
- [ ] Every remaining element has a conceptual reason to exist

**Anti-Pattern**: Adding rings, particles, grids, and decorative flourishes to "make it look better" → visual noise that dilutes the concept.

---

## 8. Prompt Engineering Tactics (Model-Specific)

### Explicit Negation
Use concrete forbidden-element keywords, not generic quality terms.
- **Wrong**: `"high quality, beautiful"`
- **Right**: `"no rings, no cylinders, no spheres, no grid patterns, no typography, no logos"`

### Material & Lighting Vocabulary
Stable, cross-model keywords. Derive from the brand's actual material lexicon (Stage 1 B.3) — the terms below illustrate the vocabulary pattern, not a fixed list:
- `frosted glass, smooth ceramic, diffuse high-key lighting`
- `soft volumetric glow, subsurface scattering, no hard shadows`
- `clean matte surfaces, subtle specular highlights`

### Color Ratio Declaration
Write proportions directly, using the brand's actual color ratio from Stage 1 B.1: `"X% [primary] / Y% [secondary] / Z% [accent]"`
Models respond more consistently to explicit ratios than to vague terms like "mostly white with hints of blue."

### Aspect Ratio Control
- Hero / banner: `--ar 16:9`
- Card / social square: `--ar 1:1` or `--ar 4:5`
- Presentation slide: `--ar 4:3`
- Mobile wallpaper: `--ar 9:16`

### Tool-Specific Seed & Reference Locking
- Midjourney: `--sref <url>` for style reference images, `--sw 100-800` for adherence
- Stable Diffusion: ControlNet (Depth/Canny) for structural control, LoRA for style
- DALL-E: Subject-first prompting; left-to-right parsing priority

---

## 9. Iterative Refinement Protocol

**Method**: When generated images fail, do not change the brand color/material rules. Adjust only geometry, composition, and layering.

**Refinement Order** (do not skip):
1. **Composition**: adjust object placement, scale, white space ratios
2. **Geometry**: swap the shape motif if it reads wrong
3. **Material assignment**: reassign which object gets which material
4. **Lighting angle**: change key light direction
5. **Color balance**: adjust accent color visibility (more/less glow, opacity)
6. **Last resort**: add one auxiliary element or remove one

**Never change**: brand color palette hex values, material lexicon, the 60-30-10 ratio, or core brand mood.

---

## 10. Semantic Encoding & Brand Easter Eggs

**Principle**: Embed brand meaning (numbers, initials, founding principles) into the geometric rules themselves, not as text labels.

**Technique**:
- If the brand involves the number 21: use 2 circles + 1 square as the shape grammar
- If the brand is about "open research": broken ring + offset point to suggest incompleteness inviting contribution
- If the brand is about "connection": interlocking forms where the negative space between them forms the brand initial
- If the brand is about "layers of meaning": concentric forms where each layer uses a different material

**Constraint**: The encoding must be discoverable but not obvious. It should add depth for those who look closely without distracting those who don't.

**Prompt Implementation**: Do not describe the easter egg in the prompt. Use the geometric rule (`"2 circles and 1 square"`) and let the model execute it; the meaning is for the brand system, not the image model.

---

## Application Workflow

When designing prompts for a new brand:

1. **Extract concepts** from Stage 1 Brand Soul → list 3–5 abstract nouns
2. **Map geometry** using Technique 2 → assign one motif per concept
3. **Enforce exclusivity** using Technique 3 → ensure no motif reuse
4. **Assign materials** using Technique 4 → primary vs auxiliary role
5. **Compose space** using Technique 5 → floating, no edge contact, radial background
6. **Add dynamics** using Technique 6 → one directional element per image
7. **Cap complexity** using Technique 7 → audit and remove excess
8. **Write prompt** using Technique 8 → explicit ratios, material keywords, negations
9. **Generate and audit** against checklist
10. **Refine** using Technique 9 → geometry/composition only, never brand rules
11. **Encode meaning** using Technique 10 → if brand has numeric/symbolic depth

---

## Relationship to Output Sections

| This Playbook Section | Maps To Meta-Prompt Section |
|----------------------|---------------------------|
| Technique 1, 5, 8 | 3.1 Core Style Prompt |
| Technique 8 (negation) | 3.2 Negative Prompt Bank |
| Technique 2, 3, 4, 6, 7, 10 | 3.4 Prompt Templates (content design) |
| Technique 9 | 3.5 Brand Consistency Validation Checklist |
| Technique 8 (params) | 3.3 Tool-Specific Control Parameters |
