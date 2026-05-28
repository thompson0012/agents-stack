# Relationship Types

Routers do not model a simple tree. They model a small graph.

## Direct router-to-child relationships

### `routes_to`
The normal case. The router selects one child and hands off.

Use when:
- the child is a leaf skill or narrower family router
- the router must choose among siblings
- the child target should usually be a nested router path like `router-name/child-name`

### `includes`
The router package contains a child package or companion path that belongs under the same umbrella.

Use when:
- the child lives inside the router package
- shared assets or references are part of the family package
- the child is still a real selectable unit, not just prose in the parent
- the child body should say it is a nested member of the router family

## Child-to-child relationships

These live inside each child entry in `references/children.json`.

### `requires`
Hard prerequisite. The selected child is not honest without it.

Use sparingly.

The target may be another child in the same router or an external skill identifier when the prerequisite lives outside the family.

### `recommends`
Helpful companion or post-check, but not mandatory.

Good examples:
- a post-deliverable verification skill
- a visualization companion for a research skill

The target may be another child in the same router or an external skill identifier such as a verification or visualization companion.

### `fallbacks_to`
A weaker but still honest alternative if the preferred child is unavailable.

Rules:
- disclose the downgrade explicitly
- do not claim equivalent coverage
- do not use fallback as a lazy substitute for installing the right child

## Install hints

`install_if_missing` is not a relationship type, but it is part of the routing contract.

Use it when:
- the child may be absent from the local runtime
- the router can truthfully tell the agent what to install

Keep it small:
- `package` — the package or skill name to install
- `notes` — short guidance about when installation is preferred over fallback

## Failure Modes

Avoid these mistakes:
- encoding every nuance in the folder tree instead of the metadata
- treating `recommends` as if it were `requires`
- falling back silently and pretending nothing changed
- listing relationships that the router body never uses
