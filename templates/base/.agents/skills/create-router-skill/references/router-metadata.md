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
  "router_name": "using-family",
  "purpose": "Route family requests to the narrowest child.",
  "selection_order": [
    "Time-sensitive operational work before generic background research.",
    "Artifact creation only after enough context exists to do it honestly."
  ],
  "children": [
    {
      "name": "child-a",
      "target": "using-family/child-a",
      "relationship": "routes_to",
      "summary": "Handles the most time-sensitive or concrete child job in the family.",
      "route_when": [
        "A concrete delivery or decision is already in scope.",
        "The user needs this child artifact now."
      ],
      "avoid_when": [
        "The request still needs prerequisite context before this child would be honest."
      ],
      "requires": [],
      "recommends": ["using-family/child-b"],
      "fallbacks_to": ["using-family/child-b"],
      "install_if_missing": {
        "package": "using-family/child-a",
        "notes": "Install the nested child path before routing when the runtime cannot discover nested skills automatically."
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
- `recommends` — optional companion children or external post-checks worth suggesting when a stated condition is true; not a wish list and not a degraded fallback
- `fallbacks_to` — explicit degraded alternatives, usually another nested child path in the same router family
- `install_if_missing` — nested child-path hint for runtimes that can install missing children on demand

## Design Rules

- Prefer `target` values that stay stable even if the filesystem layout changes.
- Keep `route_when` intent-based, not keyword-stuffed.
- Use `fallbacks_to` sparingly. A silent downgrade is a lie.
- Use `recommends` for honest next steps or companion checks the router should surface conditionally. If the route cannot proceed without it, use `requires` instead. If it is a degraded route, use `fallbacks_to`.
- Do not force every relationship into the folder tree. Keep the graph in metadata.
- If a child is shared across families, reference it here rather than pretending it has only one true parent.
