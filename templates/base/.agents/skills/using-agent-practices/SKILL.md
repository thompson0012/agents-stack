---
name: using-agent-practices
description: Use when the user may need a first-party skill from `.agents/skills` and the right leaf skill or family router is not obvious yet.
---

# Using Agent Practices

Use this skill to route a request to the narrowest correct first-party skill in this repository.

Do not solve the user's substantive task here. Pick the right next skill or decide that no first-party skill is needed.

For the current category map and skill inventory, read `references/category-map.md` when the route is unclear or the suite has changed.

## Core Contract

- Choose exactly one target: a single leaf skill, a family router such as `website-building`, `using-documents`, `using-legal`, `using-reasoning`, `using-sales`, `using-marketing`, `using-research`, or `using-finance`, or no suite skill.
- Prefer the narrowest correct fit over the most impressive fit.
- If no first-party skill clearly adds value, say so and answer directly.
- Do not stack multiple primary suite skills from this router.
- Route to a family router only when the ambiguity is inside that family.

## Category Order

Apply these checks in order.

### 1. Orchestration and continuity
- Need a compacted session state, handoff snapshot, or continuation summary -> `context-compaction`
- Need a confidence check, postmortem, lessons learned, repeatable workflow extraction, or preflight verification -> `self-cognitive`

### 2. Prompt artifact creation
- The requested deliverable is itself a prompt, system prompt, prompt template, or prompt architecture -> `meta-prompting`

### 3. Specialized business and design skills
- Need a startup sanity check, harsh viability simulation, investor-style business-model teardown, launch stress test, or CAC/churn/runway reality check -> `startup-pressure-test`
- Need design tokens, a brand system, or a brand spec from brand inputs -> `generating-design-tokens`
- Need model-generated, streamed, or schema-driven interactive UI in the browser, including sandboxed HTML or agent-rendered components -> `generative-ui`
- Need an Apple-like liquid glass browser effect using CSS/SVG refraction and displacement maps -> `liquid-glass-design`

### 4. Web project routing
- Need help building a web project and the request could plausibly mean an informational site, a fullstack web application, or a browser game -> `website-building`
### 5. Document workflows
- Need help creating, editing, converting, extracting, or QA-ing a document artifact and the request could plausibly mean Word, PDF, PowerPoint, or Excel work -> `using-documents`

### 6. Legal workflows
- Need legal help and the request could plausibly mean commercial contract review or operational privacy-compliance support -> `using-legal`

### 7. Sales workflows
- Need sales help and the request could plausibly mean account research, meeting prep, or personalized outreach -> `using-sales`

### 8. Marketing workflows
- Need marketing help and the request could plausibly mean performance analytics, competitor analysis, or content creation -> `using-marketing`

### 9. Research workflows
- Need research help and the request could plausibly mean broad deep-dive research, market-framework analysis, or investment-oriented research -> `using-research`

### 10. Finance workflows
- Need finance help and the request could plausibly mean audit-control support or finance-data tooling -> `using-finance`

### 11. Reasoning and strategy requests
If the task is mainly about understanding, framing, advising, or scenario-planning a problem, route to `using-reasoning`.

### 12. No suite skill
If none of the above fits cleanly, do not force a suite skill.

## Router Output

Return one of these forms and then invoke the selected skill if needed:

- `Route to context-compaction.`
- `Route to self-cognitive.`
- `Route to meta-prompting.`
- `Route to startup-pressure-test.`
- `Route to generating-design-tokens.`
- `Route to generative-ui.`
- `Route to liquid-glass-design.`
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
- routing to `using-reasoning` for requests that are clearly prompt, continuity, startup, design, web-project, document, or legal work
- sending a request to multiple sibling skills in parallel from this router
- forcing a suite skill onto a simple request that does not benefit from special instructions
- routing model-generated or schema-driven browser UI work to `website-building` when the generative layer itself is the main problem
- routing an ambiguous website request straight to one child when `website-building` should narrow it first
- routing an ambiguous document request straight to one leaf when `using-documents` should narrow it first
- routing an ambiguous legal request straight to one child when `using-legal` should narrow it first
- routing an ambiguous sales request straight to one leaf when `using-sales` should narrow it first
- routing an ambiguous marketing request straight to one leaf when `using-marketing` should narrow it first
- routing an ambiguous research request straight to one leaf when `using-research` should narrow it first
- routing an ambiguous finance request straight to one leaf when `using-finance` should narrow it first
