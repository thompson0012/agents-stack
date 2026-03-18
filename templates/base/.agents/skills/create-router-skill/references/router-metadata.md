# Router Metadata

Use `references/children.json` as the router's machine-readable child inventory.

## Why this file exists

A nested folder tree alone is not enough. A discoverable router needs explicit metadata so the agent can:
- see which children exist
- choose among them in a stable order
- know what to do when a child is missing
- disclose fallbacks instead of silently degrading

Keep the router `SKILL.md` focused on selection logic. Put the change-prone child inventory here.

## File Shape

```json
{
  "router_name": "using-reasoning",
  "purpose": "Route analytical requests to the narrowest reasoning child.",
  "selection_order": [
    "Distorted state before vague problem.",
    "Vague problem before analysis."
  ],
  "children": [
    {
      "name": "problem-definition",
      "target": "using-reasoning/problem-definition",
      "relationship": "routes_to",
      "summary": "Turns messy situations into one precise problem statement.",
      "route_when": [
        "Problem is still vague.",
        "Symptoms and proposed solutions are mixed together."
      ],
      "avoid_when": [
        "The problem is already stated clearly and solution-neutrally."
      ],
      "requires": [],
      "recommends": ["self-cognitive"],
      "fallbacks_to": ["dynamic-problem-solving"],
      "install_if_missing": {
        "package": "problem-definition",
        "notes": "Install the child before routing when the runtime cannot discover nested skills."
      }
    }
  ]
}
```

## Field Rules

### Top level
- `router_name` — must match the router skill's frontmatter `name`
- `purpose` — one sentence describing the family boundary
- `selection_order` — ordered statements that tell the router how to break ties between siblings
- `children` — the canonical child inventory

### Child entries
- `name` — stable child label used in router output and cross-references
- `target` — exact child identifier or load target the runtime should hand off to
- `relationship` — how the router relates to the child; usually `routes_to`, sometimes `includes`
- `summary` — one-sentence distinction from sibling skills
- `route_when` — positive signals that select this child
- `avoid_when` — negative signals that rule this child out
- `requires` — local child names or external skill identifiers that must also be available before the selected child is safe to use
- `recommends` — optional companion children or external post-checks worth suggesting
- `fallbacks_to` — explicit degraded alternatives, usually another child in the same router family
- `install_if_missing` — package hint for runtimes that can install missing children on demand

## Design Rules

- Prefer `target` values that stay stable even if the filesystem layout changes.
- Keep `route_when` intent-based, not keyword-stuffed.
- Use `fallbacks_to` sparingly. A silent downgrade is a lie.
- Do not force every relationship into the folder tree. Keep the graph in metadata.
- If a child is shared across families, reference it here rather than pretending it has only one true parent.
