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

If comparison is useful, return 2 to Here is a revised `skill.md` that keeps your original intent but tightens the scope, improves multimodal coverage, and makes the output more portable for agentic or programmatic workflows [web:8].

```md
# Prompt Augmentation

Use this skill when the prompt is too thin to drive good generation, but the underlying subject is already present. Enrich the prompt without redesigning the overall prompt architecture.

## Boundary

This skill expands generation prompts. It does not design system prompts, multi-turn agent behavior, tool orchestration, memory policy, or broader prompt architecture. Route that work to `meta-prompting`.

Use this skill when the user's subject is already clear enough to preserve, but the prompt needs more specificity, control, or production readiness.

Do not use this skill to:
- invent a different concept than the one the user asked for
- convert a simple prompt expansion task into a full prompt framework
- add heavy structure when the target workflow only needs a paste-ready string
- force chain-of-thought style instructions into reasoning models

## Workflow

### 1. Classify the mode

Identify the target generation mode from the request:
- text-to-image
- text-to-video
- text-to-text generation

If relevant, also infer the model class or runtime style:
- standard generative model
- reasoning model
- engine-specific workflow, for example Midjourney, Flux, SDXL, Sora, Runway, Kling, or a custom API pipeline

If the mode is unclear and would materially change the output, ask a clarifying question or state the assumption before finalizing.

For text generation, distinguish between:
- standard LLM prompting, where role, structure, and output shape often help
- reasoning-model prompting, where you should avoid adding "think step by step" style instructions unless the user explicitly wants them

### 2. Preserve the core subject

Lock the user's non-negotiables before expanding:
- main subject, actor, object, or scene
- intended action, transformation, or outcome
- explicit constraints already present
- named style, medium, format, audience, or platform already chosen
- any brand, product, character, or visual identity that must remain intact

Do not swap the subject for a different idea. Add specificity without changing what the prompt is about.

If the original prompt contains ambiguity, resolve it by tightening context rather than replacing the concept.

### 3. Expand the right dimensions

Add only details that improve controllability.

For image prompts, consider:
- subject attributes, pose, expression, wardrobe, materials, or defining features
- composition, framing, camera angle, perspective, and focal emphasis
- setting, environment, season, weather, architecture, or scene context
- lighting direction, color temperature, contrast, atmosphere, and mood
- style, medium, rendering cues, surface detail, and finish
- format cues only when they help, such as aspect ratio or intended crop

For video prompts, consider:
- all relevant image dimensions above
- motion of subject and camera
- pacing, transitions, shot progression, and temporal continuity
- scene dynamics, environmental movement, and cinematic rhythm
- duration-aware specificity when useful, such as opening shot, motion beat, and closing frame

For text generation prompts, consider:
- role or voice
- audience and usage context
- objective and success criteria
- constraints, tone, and exclusions
- desired output shape, for example bullets, memo, table, script, or JSON
- structural delimiters when useful, such as `<context>`, `<task>`, `<constraints>`, or clearly separated labeled sections

For reasoning models, enrich boundary conditions, evaluation criteria, edge cases, and expected output format rather than adding verbose reasoning directives.

### 4. Build useful variants

When variants help, produce a small set with meaningful distance while keeping the same core subject.

Good variant directions include:
- grounded or literal
- cinematic or expressive
- stylized or highly directed
- concise production-ready
- engine-tuned, when a specific generation system is known

Change direction, emphasis, intensity, or composition. Do not change the user's underlying idea.

When the workflow supports positive and negative prompts, write both as plain strings. Negative prompts should target likely failure modes, not ban desired elements.

Examples of useful negatives:
- anatomy or face errors
- cluttered background
- low-detail rendering
- incorrect text
- extra limbs, duplicate subjects, warped hands, muddy lighting

Avoid negatives that accidentally cancel the requested style or subject.

### 5. Apply engine-specific tuning when known

When the target engine is known, adapt the augmentation to that engine's syntax and strengths.

Examples:
- aspect ratio or framing flags
- quality or stylization parameters
- weighted emphasis syntax
- model-specific prompt ordering preferences
- separate fields for prompt, negative prompt, seed, duration, or camera motion

Do not invent engine syntax unless confidence is high. If uncertain, keep the output portable and plain.

### 6. Run a contradiction audit

Before delivering, silently check for:
- style conflicts or mutually exclusive cues
- negatives that exclude desired content
- missing spatial, temporal, or audience context
- overwritten core-subject details
- redundant filler that adds length without control
- token dilution, where extra detail pushes the main subject too far down the prompt
- format mismatch between the prompt and the target model or engine
- unnecessary complexity that reduces paste-ready usability

Patch contradictions before output.

## Delivery

Default to portable output:
- a single enriched prompt when one answer is enough
- labeled variants when comparison helps
- optional negative prompts when the target workflow supports them

Use plain strings by default.

Use structured output only when the user or runtime benefits from it, for example:
- XML-like sections for agentic workflows
- JSON for programmatic pipelines
- separate fields for `prompt`, `negative_prompt`, and `parameters`

When structured output is used, keep it lightweight and easy to paste or parse.

## Output Style

Prefer this order:
1. brief assumption, only if needed
2. enriched prompt
3. optional variants
4. optional negative prompt
5. optional parameters, only when engine-specific details are known and useful

Do not add long explanations unless the user asks for rationale.

## Quality Bar

A good augmented prompt:
- preserves the user's subject
- adds concrete control rather than random decoration
- improves generation reliability
- offers variants only when they are meaningfully different
- avoids contradictions and dead weight
- stays ready to paste into the target workflow
- respects the target model's actual behavior rather than generic prompt folklore

## Heuristics

- Preserve first, enrich second.
- Specific beats verbose.
- Constraints should clarify, not suffocate.
- Only add cinematic language when it improves control.
- Only add structure when it improves parsing or output consistency.
- For reasoning models, specify the task boundaries and success criteria; do not pad with artificial reasoning instructions.
- For image and video, prioritize subject clarity, composition, lighting, and scene coherence before aesthetic flourishes.

## Fail Conditions

Do not treat the augmentation as successful if it:
- changes the subject
- introduces a new visual or narrative concept the user did not imply
- adds contradictory style cues
- bloats the prompt with filler adjectives
- outputs engine syntax that does not match the likely runtime
- turns a simple prompt expansion into a system-prompt rewrite
```

Would you like a second pass that formats this in your existing `skills.md` house style, such as tighter imperative wording and more MCP-friendly sections?