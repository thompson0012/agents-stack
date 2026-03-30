# Router Metadata

Use `references/children.json` as the machine-readable inventory for the Labs21 product-suite router.

## Why this file exists

A stage-gated router needs explicit metadata so the agent can:
- see which children exist
- choose among them in a stable order
- know what to do when a child is missing
- disclose prerequisites and fallback behavior instead of silently degrading

Keep `SKILL.md` focused on the router contract. Keep child inventory details here.

## File Shape

```json
{
  "router_name": "labs21-product-suite",
  "purpose": "Route product-development requests through strategy, PRD, and system-design stages without skipping prerequisites.",
  "selection_order": [
    "Stage 1 owns raw ideas, strategy, MVP framing, and blueprints from scratch.",
    "Stage 2 owns PRDs, user stories, acceptance criteria, and edge cases once a blueprint is validated.",
    "Stage 3 owns schema, API, state-flow, and infrastructure design once a PRD is validated."
  ],
  "children": [
    {
      "name": "labs21-chief-architect",
      "target": "labs21-product-suite/labs21-chief-architect",
      "relationship": "routes_to",
      "summary": "Handles raw ideas, strategy, MVP definition, and from-scratch blueprints.",
      "route_when": ["..."],
      "avoid_when": ["..."],
      "requires": [],
      "recommends": [],
      "fallbacks_to": [],
      "install_if_missing": {
        "package": "labs21-product-suite/labs21-chief-architect",
        "notes": "Install this nested child path before routing when the runtime cannot discover nested skills automatically."
      }
    }
  ]
}
```

## Field Rules

- `router_name` must match the router skill frontmatter `name`.
- `purpose` should describe the family boundary in one sentence.
- `selection_order` should be ordered statements that explain how to break ties between siblings.
- `children` is the canonical child inventory.

### Child entry fields

- `name` — stable child label used in router output and cross-references
- `target` — exact child identifier or load target the runtime should hand off to
- `relationship` — how the router relates to the child; usually `routes_to`
- `summary` — one-sentence distinction from sibling skills
- `route_when` — positive signals that select this child
- `avoid_when` — negative signals that rule this child out
- `requires` — local child names or external skill identifiers that must be available before the selected child is honest
- `recommends` — optional companion children or external post-checks worth suggesting when a stated condition is true
- `fallbacks_to` — explicit degraded alternatives, usually another nested child path in the same router family
- `install_if_missing` — nested child-path hint for runtimes that can install missing children on demand

## Design Rules

- Prefer `target` values that stay stable even if the filesystem layout changes.
- Keep `route_when` intent-based, not keyword-stuffed.
- Use `fallbacks_to` sparingly; a silent downgrade is a lie.
- Use `recommends` for honest next steps or companion checks the router should surface conditionally.
- If a child is shared across families, reference it here rather than pretending it has only one true parent.
