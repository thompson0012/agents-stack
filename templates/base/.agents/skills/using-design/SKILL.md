---
name: using-design
description: Use when a design-oriented request could plausibly need broad visual-system guidance, a reusable design-token spec, model-generated browser UI, or experimental liquid-glass effects and the agent must choose the narrowest child first.
---

# Using Design

Use this router when the task is primarily about design direction, visual-system definition, or design-specific browser UI work and more than one design child could fit.

Do not perform the child workflow here. Choose the narrowest correct design skill, then hand off.

## Core Contract

- Choose exactly one primary design child or decide that no design child fits.
- Prefer explicit liquid-glass effect work first, then model-generated browser UI, then reusable token-spec generation, then broad design guidance.
- Use `references/children.json` as the source of truth for child boundaries, install hints, and companion recommendations.
- If the best child is missing, say to install it rather than quietly doing weaker work under the wrong child.
- Do not let this router swallow ordinary website-building, generic frontend implementation, or non-design requests.

## Decision Order

| Design Need | Route | Examples |
|---|---|---|
| Experimental liquid-glass optics in the browser | `load_skill("using-design/liquid-glass-design")` | Apple-like glass, SVG displacement maps, CSS refraction, Chromium/Electron glass prototypes |
| Model-generated browser UI | `load_skill("using-design/generative-ui")` | Schema-driven renderers, sandboxed HTML, streamed UI, agent-rendered components |
| Reusable token spec or brand-system artifact | `load_skill("using-design/generating-design-tokens")` | Design token specs, brand systems, design specs, token architecture docs |
| Broad visual-system guidance | `load_skill("using-design/design-foundations")` | Palette, typography, spacing, chart styling, general art direction without an existing token system |

When a request is really about building a normal hand-authored site, dashboard, or product workflow, route to `website-building` instead of forcing a `using-design` child. Use this family only when the design boundary itself is the hard part.

## Router Output

Return one of these forms and then invoke the selected child if needed:

- `Route to using-design/liquid-glass-design.`
- `Route to using-design/generative-ui.`
- `Route to using-design/generating-design-tokens.`
- `Route to using-design/design-foundations.`
- `Install <child-path>, then route to <child-path>.`
- `No using-design child fits; answer directly.`

Add one sentence explaining why the selected child is the narrowest correct fit.

## References

- `references/children.json`

## Family Workflow Boundary

1. The router chooses the narrowest design child.
2. The selected child owns the actual workflow, research, artifacts, and verification.
3. `using-design/design-foundations` is the broad fallback only when no project-specific token system already governs the work and the deliverable is not a token spec.
4. `using-design` does not replace `website-building`; normal website or webapp implementation still belongs there unless the request is specifically about generative UI or experimental glass effects.
