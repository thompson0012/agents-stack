---
name: generative-ui
description: Use when building or evaluating model-generated interactive UI in the browser, including schema-driven component rendering, streamed UI, sandboxed HTML experiences, or agent-controlled interface updates.
---

# Generative UI

## Overview
Use this skill when the model is responsible for choosing interface structure, composing components, or updating interface state at runtime. This is not the right skill for a normal hand-authored landing page, SaaS app, or browser game unless the hard part is the generative UI layer itself.

Read [dependency graph](references/dependency-graph.md) for suite integration and [output contracts](references/output-contracts.md) for the supported rendering modes.

## Core Contract
- Start from a design contract, not ad hoc styling. Read the existing token or design source first (`docs/reference/design.md`, an equivalent brand spec, or repo-local token files). If no trustworthy token spec exists and the UI is meant to be reused or shipped, use `using-design/generating-design-tokens` before building the generative layer.
- Keep the model on the UI side of the boundary. The model may choose components or emit safe HTML/schema payloads; the host application owns privileged actions, network access, persistence, and secret-bearing logic.
- Choose one rendering contract before coding: standalone HTML document, typed component schema, or streamed UI. Do not blur those contracts together casually.
- Generated UI must fail honestly. Handle malformed markup, unknown components, missing props, partial streams, empty states, and unsafe payloads with explicit fallback UI.
- Default to allowlists, typed schemas, and sandboxing. Do not run arbitrary model HTML inside the host app's privileged DOM.
- Verify through the real render path before calling the system done.

## When to Use
Use this skill when the request is about:
- prompt-to-UI or agent-rendered browser experiences
- model-selected components, cards, forms, charts, panels, or action surfaces
- sandboxed HTML rendering, schema-driven UI, or streamed UI composition
- mapping tool results or agent state into adaptive interface primitives
- preventing unsafe or hallucinated UI output in a generative renderer

Do not use this skill when:
- the job is a normal website or webapp with hand-authored UI -> use `website-building`
- the job is primarily brand or token creation -> use `using-design/generating-design-tokens`
- the deliverable is mainly a prompt artifact or system prompt -> use `meta-prompting`

## Workflow

### 1. Classify the real job
Decide whether the user needs:
1. an ephemeral standalone UI artifact
2. a reusable renderer/runtime inside an app
3. a streamed UI experience with progressive reveal

If the request is actually a whole website or product build, route to `website-building` and use this skill only when the generative layer is the differentiating problem.

### 2. Lock the design contract
Read the existing design source first:
- `docs/reference/design.md`
- a project brand or token spec
- repo-local token files

If none exists:
- for productized or reusable work: use `using-design/generating-design-tokens`
- for disposable prototypes: fall back to `using-design/design-foundations` deliberately and label the fallback

At minimum establish: color roles, type scale, spacing rhythm, radius, shadow/elevation, motion rules, and empty/error/loading states.

### 3. Define the renderer boundary
Before implementing, write down:
- what the model is allowed to emit
- what the host renders
- what events go back to the model
- which components are allowed
- which props are allowed
- which side effects stay host-owned

If you cannot describe those boundaries in a short table, the design is still too vague.

### 4. Choose the output contract
Use [output contracts](references/output-contracts.md):
- standalone HTML + iframe sandbox for demos or self-contained experiences
- typed component schema for production app integration
- streamed UI for longer-running or progressive workflows

Pick the lightest contract that preserves truth. Do not default to raw HTML when typed components would be safer, and do not introduce a component registry when a disposable sandbox is enough.

### 5. Build the surface
- Prefer interactive components over paragraphs.
- Keep the first screen actionable.
- Encode state changes explicitly: loading, success, error, partial, retry.
- For charts, use a proven library or host-owned component rather than freehand model SVG unless novelty is the point.
- When using HTML generation, output a complete document and keep external dependencies small and explicit.
- When using typed components, validate every model payload before rendering.
- When streaming, send useful skeletons and partial structure early.

### 6. Guard the unsafe edges
- reject or drop unknown components
- strip or sanitize unsafe HTML/attributes
- cap payload size and recursive depth
- keep click/action messages typed and minimal
- let the host map action IDs to real effects
- never let the model invent privileged APIs or hidden state contracts

### 7. QA the actual behavior
Test the real render path:
- initial render
- invalid model output
- empty dataset
- slow or partial stream
- retry or regeneration
- keyboard and focus flow
- mobile layout
- reduced-motion behavior

If the UI is data-heavy, verify the source before polishing the surface.

## Quick Reference
| Situation | Default move |
| --- | --- |
| No trustworthy token spec exists | Use `using-design/generating-design-tokens` first |
| User wants a full website/app/game | Route to `website-building` |
| Ephemeral demo in one artifact | Standalone HTML + sandbox |
| Production in-app generative surfaces | Typed schema + allowlisted components |
| Long-running agent turn | Streamed UI + skeletons |
| Unsafe or malformed payload | Fail closed with fallback UI |

## References
- [dependency graph](references/dependency-graph.md)
- [output contracts](references/output-contracts.md)

## Failure Modes
- treating generative UI as “just build a webapp”
- inventing colors, fonts, or spacing instead of following tokens
- letting raw model HTML touch privileged host DOM
- allowing model output to call real side effects directly
- hiding malformed output behind plausible-looking fallbacks
- generating static prose where an interactive surface is the point

## Final Checklist
- [ ] Real job classified correctly
- [ ] Token/design contract read first
- [ ] Renderer boundary written down
- [ ] Output contract selected deliberately
- [ ] Unsafe payload path handled
- [ ] Loading/error/empty/retry states exist
- [ ] Real render path verified
