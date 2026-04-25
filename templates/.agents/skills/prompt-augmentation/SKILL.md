---
name: prompt-augmentation
description: Use when a sparse or under-specified prompt for text, image, or video generation needs enrichment, clearer direction, or useful variants while preserving the user's core subject.
---

# Prompt Augmentation

Use this skill when the prompt is too thin to drive good generation, but the underlying subject is already present. Enrich the prompt without redesigning the user's idea, task structure, or overall prompt architecture.

## Boundary

This skill expands generation prompts. It does not design system prompts, tool orchestration, multi-turn agent behavior, or broader prompt architecture. Route that work to `meta-prompting`.

Do not use this skill when:
- the user needs a full prompt framework rather than a stronger prompt
- the core subject is still unclear or missing
- the task is primarily about agent instructions, policy, memory, routing, or workflow design
- the request is really asking for evaluation, critique, or prompt debugging instead of augmentation

## Goal

Improve controllability, clarity, and output quality while preserving the user's original subject and intent.

A good augmentation:
- keeps the same core subject
- adds concrete control rather than random decoration
- improves generation reliability
- avoids contradictions, clutter, and dead weight
- stays ready to paste into the target workflow

## Workflow

### 1. Classify the mode

Identify the target generation mode first:

- text-to-image
- text-to-video
- text-to-design or UI generation
- text-to-text generation
- text-to-audio or sound design
- 3D or scene generation

For text generation, also classify the model class when possible:

- standard LLM
- reasoning model

If the mode is unclear and would materially change the output, ask a clarifying question or state the assumption before finalizing.

If the target is a reasoning model, do not pad the prompt with "think step by step" style language unless the user explicitly wants that. Instead, strengthen the prompt by improving:
- task boundaries
- success criteria
- evaluation standards
- inputs and constraints
- edge cases
- expected output shape

### 2. Preserve the core subject

Lock the user's non-negotiables before expanding:

- main subject, actor, object, or scene
- intended action, task, or outcome
- explicit constraints already given
- named style, medium, audience, or platform already chosen
- any required format, duration, aspect ratio, or tone already stated

Do not replace the subject with a better idea. Do not drift into a different aesthetic, story, or use case unless the user asked for variants.

Preserve first, then enrich.

### 3. Expand the right dimensions

Add only details that increase control.

For image or visual prompts, consider:
- subject attributes
- pose, expression, wardrobe, props, or materials
- composition and spatial relationships
- setting, era, time of day, weather, or environment
- lighting direction, color, contrast, and mood
- camera angle, lens feel, framing, or perspective
- medium, rendering cues, or surface texture
- aspect ratio or output format when useful

For video prompts, consider:
- motion of subject and camera
- pacing and shot rhythm
- scene progression or transition logic
- environment dynamics such as wind, particles, traffic, or crowd movement
- temporal cues such as slow reveal, tracking shot, or close-up shift
- duration, framing, and loopability when relevant

For text generation prompts, consider:
- role or voice
- audience and context
- objective
- success criteria
- tone and constraints
- structure of the answer
- length expectations
- examples only when they improve precision
- delimiters or sections when they help parsing

Use structure to compartmentalize meaning, not to redesign the whole prompt.

### 3a. Use domain-specific references for visual and design prompts

When augmenting image, video, or design prompts, substitute generic description with precise domain terminology rather than filler adjectives. Read the relevant reference files in this skill's `references/` directory before expanding, and pull precise terms from them.

| Mode | References to consult |
|---|---|
| text-to-image | `references/optics-camera.md`, `references/composition-framing.md`, `references/lighting-atmosphere.md`, `references/medium-rendering.md`, `references/color-mood.md` |
| text-to-video | All image references plus `references/camera-movement.md`, `references/film-grammar-editing.md`, `references/temporal-pacing.md`, `references/continuity-cues.md` |
| text-to-design | `references/typography-terms.md`, `references/layout-grid-systems.md`, `references/ui-component-states.md`, `references/color-system-design.md`, `references/design-system-tokens.md`, `references/accessibility-specs.md` |

Rules when using references:
- Do not dump every term. Select only the ones that increase control for the user's specific subject.
- Replace vague cues with precise ones: "good lighting" → "three-point Rembrandt with soft key and subtle rim"; "camera moves" → "slow dolly-in with rack focus".
- Respect the core subject lock from Step 2. Do not let the reference vocabulary override the user's non-negotiables.
- Cross-check against `references/negative-prompt-pitfalls.md` when writing negative prompts.

When structure helps reliability, prefer lightweight organization such as:
- `<context>`
- `<task>`
- `<constraints>`
- `<output_format>`

Use structure to compartmentalize meaning, not to redesign the whole prompt.

### 4. Match the target engine

If the target model or engine is known, adapt the augmentation to that environment.

Examples:
- diffusion workflows may benefit from concise visual phrasing, composition cues, and optional negative prompts
- video engines may benefit from motion direction, shot sequencing, and temporal continuity cues
- structured LLM pipelines may benefit from explicit sections and output constraints
- reasoning models may benefit from sharper evaluation criteria rather than stylistic padding

When engine-specific parameters are helpful, include them only if the user already uses that workflow or they materially improve control, for example:
- aspect ratio
- duration
- stylization level
- quality settings
- seed or reproducibility hints
- positive and negative prompt separation

Do not force engine syntax when portability matters more.

### 5. Build useful variants

When variants would genuinely help, produce a small set with meaningful distance.

Good variant patterns:
- grounded or literal
- cinematic or expressive
- stylized or highly directed
- minimal or production-ready

Keep the same core subject across all variants. Change emphasis, intensity, framing, or style direction without changing what the prompt is about.

Do not create shallow variants that only swap adjectives.

### 6. Write negatives carefully

When the target workflow supports negative prompts, write them as plain strings.

Negative prompts should remove likely failure modes such as:
- anatomy errors
- cluttered backgrounds
- extra limbs or duplicated subjects
- unreadable text
- muddy lighting
- low-detail surfaces
- inconsistent style
- unwanted artifacts

Do not use negatives that accidentally ban desired features.

### 7. Run a contradiction audit

Before delivering, silently check for:
- style conflicts or mutually exclusive cues
- negatives that suppress desired content
- overwritten core-subject details
- missing spatial, temporal, or audience context
- redundant filler that adds length without control
- token dilution, where too much added detail weakens the main subject
- format mismatch between the prompt and the target engine
- vague quality language that sounds impressive but adds no control

Patch contradictions before output.

## Delivery

Default to portable output.

Use:
- a single enriched prompt when one answer is enough
- labeled variants when comparison helps
- optional negative prompts when the workflow supports them

Prefer plain strings by default.

Use structured output only when the runtime or user clearly benefits from it, such as:
- XML-style sections for downstream parsing
- JSON fields for programmatic pipelines
- separate fields for `prompt`, `negative_prompt`, and `parameters`

Do not add unnecessary scaffolding.

## Output Rules

- Preserve the user's subject.
- Add specificity only where it improves control.
- Stay compatible with the likely target workflow.
- Avoid filler adjectives that do not guide generation.
- Avoid turning augmentation into a full rewrite.
- Avoid hidden assumptions that materially change the result.
- Keep the result ready to paste.

## Quality Bar

A good augmented prompt:
- preserves the user's original idea
- improves controllability
- is more specific without becoming bloated
- contains no obvious contradictions
- uses variants only when they are meaningfully different
- supports the target medium rather than fighting it
- remains concise enough that the primary subject stays dominant

## Default Behavior

If one strong answer is sufficient, return one enriched prompt.
