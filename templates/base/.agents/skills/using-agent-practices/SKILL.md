---
name: using-agent-practices
description: Use when the user may need a first-party skill from `.agents/skills` and the right leaf skill or family router is not obvious yet.
---

# Using Agent Practices

Use this skill to route a request to the narrowest correct first-party skill in this repository.

Do not solve the user's substantive task here. Pick the right next skill or decide that no first-party skill is needed.

For the current category map and skill inventory, read `references/category-map.md` when the route is unclear or the suite has changed.

## Quick path

If this is your first request or you are not sure where to start, match your situation to a route below. Stop as soon as one stage gives you what you need.

- Need to create or upgrade a reusable skill package or portable skill guidance -> `create-skill`
- Need to create or upgrade a router skill whose main job is choosing among child skills with explicit metadata -> `create-router-skill`
- Need to categorize, prioritize, dedupe, and route support tickets -> `cx-ticket-triage`
- Need to profile an unfamiliar dataset before deeper analysis -> `data-exploration`
- Need chart selection, Python visualization code, or chart-specific accessibility guidance -> `visualization`
- Need harness media generation or transcription CLI work -> `media`
- Unclear problem, goal, or scope -> `using-reasoning`
- Non-trivial software feature work still needs discovery, delivery-control routing, plan review, or strict frontend acceptance -> `software-delivery`
- Need a spec or requirements document before building -> `feature-spec`
- Need design help and are not sure whether the work is foundational design, design tokens, generative UI, or liquid-glass experimentation -> `using-design`
- Coding, debugging, or generic repo-backed execution in an existing repo -> `coding-and-data`
- Building a web project -> `website-building`
- Preflight confidence check or postmortem before a risky decision -> `self-cognitive`

## Core Contract

- Choose exactly one target: a single leaf skill, a family router such as `software-delivery`, `using-design`, `website-building`, `using-documents`, `using-legal`, `using-reasoning`, `using-sales`, `using-marketing`, `using-research`, or `using-finance`, or no suite skill.
- Prefer the narrowest correct fit over the most impressive fit.
- If no first-party skill clearly adds value, say so and answer directly.
- Do not stack multiple primary suite skills from this router.
- Route to a family router only when the ambiguity is inside that family.

## Category Order

Apply these checks in order.

### 1. Orchestration and continuity
- Need a compacted session state, handoff snapshot, or continuation summary -> `context-compaction`
- Need a confidence check, postmortem, lessons learned, repeatable workflow extraction, or preflight verification -> `self-cognitive`
- Need multi-phase control with phase gates, drift tracking, and cross-session persistence for a vision/roadmap that must not drift -> `software-delivery/multi-phase-control`

### 2. Prompt, spec, and skill artifact creation
- The requested deliverable is a system prompt, prompt template, prompt architecture, prompt rubric, or prompt eval plan -> `meta-prompting`
- The request is to enrich a sparse prompt or generate prompt variants for text, image, or video generation while preserving the user's core subject -> `prompt-augmentation`
- The request is to draft or review a feature spec, PRD, or requirements document -> `feature-spec`
- The request is to create or upgrade a reusable leaf skill package, scaffold a skill directory, or rewrite skill guidance into a portable skill package -> `create-skill`
- The request is to create or upgrade a discoverable router skill whose main job is routing across child skills with explicit child metadata, install hints, or fallbacks -> `create-router-skill`

### 3. Specialized business, support, design, and media skills
- Need a startup sanity check, harsh viability simulation, investor-style business-model teardown, launch stress test, or CAC/churn/runway reality check -> `startup-pressure-test`
- Need customer-support ticket triage, categorization, priority/SLA assignment, duplicate checking, or owner routing -> `cx-ticket-triage`
- Need help choosing among design foundations, design tokens, generative browser UI, or liquid-glass experimentation, or the request is broadly about visual systems or design stacks -> `using-design`
- Need help choosing colors, typography, spacing, or chart styling for a visual artifact when no project-specific design system already governs the work -> `using-design/design-foundations`
- Need design tokens, a brand system, or a brand spec from brand inputs -> `using-design/generating-design-tokens`
- Need model-generated, streamed, or schema-driven interactive UI in the browser, including sandboxed HTML or agent-rendered components -> `using-design/generative-ui`
- Need an Apple-like liquid glass browser effect using CSS/SVG refraction and displacement maps -> `using-design/liquid-glass-design`
- Need harness image/video generation, text-to-speech, or audio/video transcription through the documented media CLI commands -> `media`

### 4. Software delivery routing
- Need lifecycle guidance for non-trivial software feature work and the request could plausibly mean discovery, cross-session delivery control, plan review, implementation handoff, strict frontend acceptance, or ship-readiness reflection -> `software-delivery`

### 5. Data exploration and visualization
- Need to profile an unfamiliar dataset, assess data quality, infer grain or joins, document schema, or look for anomalies and useful segments before deeper analysis -> `data-exploration`
- Need chart-type selection, Python visualization code, or chart-specific accessibility guidance -> `visualization`
- Need to delegate repo navigation, code changes, debugging, or generic repo-backed execution once the task is already defined -> `coding-and-data`

### 6. Web project routing
- Need help building a web project and the request could plausibly mean an informational site, a fullstack web application, or a browser game -> `website-building`

### 7. Document workflows
- Need help creating, editing, converting, extracting, or QA-ing a document artifact and the request could plausibly mean Word, PDF, PowerPoint, or Excel work -> `using-documents`

### 8. Legal workflows
- Need legal help and the request could plausibly mean commercial contract review or operational privacy-compliance support -> `using-legal`

### 9. Sales workflows
- Need sales help and the request could plausibly mean account research, meeting prep, or personalized outreach -> `using-sales`

### 10. Marketing workflows
- Need marketing help and the request could plausibly mean performance analytics, competitor analysis, or content creation -> `using-marketing`

### 11. Research workflows
- Need research help and the request could plausibly mean broad deep-dive research, market-framework analysis, or investment-oriented research -> `using-research`

### 12. Finance workflows
- Need finance help and the request could plausibly mean audit-control support or finance-data tooling -> `using-finance`

### 13. Reasoning and strategy requests
If the task is mainly about understanding, framing, advising, or scenario-planning a problem, route to `using-reasoning`.

### 14. No suite skill
If none of the above fits cleanly, do not force a suite skill.

## Router Output

Return one of these forms and then invoke the selected skill if needed:

- `Route to context-compaction.`
- `Route to self-cognitive.`
- `Route to meta-prompting.`
- `Route to prompt-augmentation.`
- `Route to feature-spec.`
- `Route to create-skill.`
- `Route to create-router-skill.`
- `Route to startup-pressure-test.`
- `Route to cx-ticket-triage.`
- `Route to using-design.`
- `Route to using-design/design-foundations.`
- `Route to using-design/generating-design-tokens.`
- `Route to using-design/generative-ui.`
- `Route to using-design/liquid-glass-design.`
- `Route to media.`
- `Route to software-delivery.`
- `Route to data-exploration.`
- `Route to visualization.`
- `Route to coding-and-data.`
- `Route to website-building.`
- `Route to using-documents.`
- `Route to using-legal.`
- `Route to using-sales.`
- `Route to using-marketing.`
- `Route to using-research.`
- `Route to using-finance.`
- `Route to using-reasoning.`
- `No agent-practices skill needed; answer directly.`

Add one sentence explaining why the selected route is the narrowest correct fit.

## Failure Modes to Avoid

- routing to a specialist because of one keyword when the artifact type points elsewhere
- routing to `using-reasoning` for requests that are clearly prompt, continuity, skill-authoring, startup, support-triage, design, media, data-profiling, web-project, document, or legal work
- routing prompt-architecture or system-prompt work to `prompt-augmentation` when the request is really about designing the artifact, not enriching it
- routing reusable leaf-skill creation or upgrades to `feature-spec` or `coding-and-data` instead of `create-skill`
- routing router-package authoring to `create-skill` when the package's main job is family routing, child metadata, or honest install/fallback behavior
- routing support-ticket categorization and owner assignment to `coding-and-data` or `using-reasoning` when `cx-ticket-triage` is the real fit
- sending a request to multiple sibling skills in parallel from this router
- forcing a suite skill onto a simple request that does not benefit from special instructions
- routing a normal site, app, or browser game build to `using-design` when `website-building` owns the build family
- routing an ambiguous design-family request straight to one design leaf when `using-design` should narrow it first
- routing a specific `using-design/generating-design-tokens`, `using-design/generative-ui`, or `using-design/liquid-glass-design` request to `using-design` when a direct leaf is already the narrowest fit
- routing chart-type selection, Python visualization code, or chart-specific accessibility work to `using-design/design-foundations` when `visualization` is the narrower fit
- routing chart-style-only palette, typography, spacing, or layout guidance to `visualization` when `using-design/design-foundations` is the real fit
- routing dataset profiling, schema discovery, or data-quality assessment straight to `coding-and-data` when `data-exploration` is the narrower fit
- routing model-generated or schema-driven browser UI work to `website-building` when the generative layer itself is the main problem
- routing harness media generation or transcription to `using-documents` just because files are involved
- routing PDF, slide, workbook, Word, OCR, or other document-artifact work to `media` when `using-documents` owns the artifact
- routing multi-session runtime control or planner/generator/evaluator requests straight to `self-cognitive` or `website-building` when `software-delivery` should narrow them first
- routing strict independent frontend signoff straight to `website-building` or `self-cognitive` instead of `software-delivery`
- routing an ambiguous website request straight to one child when `website-building` should narrow it first
- routing an ambiguous document request straight to one leaf when `using-documents` should narrow it first
- routing an ambiguous legal request straight to one child when `using-legal` should narrow it first
- routing an ambiguous sales request straight to one leaf when `using-sales` should narrow it first
- routing an ambiguous marketing request straight to one leaf when `using-marketing` should narrow it first
- routing an ambiguous research request straight to one leaf when `using-research` should narrow it first
- routing an ambiguous finance request straight to one leaf when `using-finance` should narrow it first
