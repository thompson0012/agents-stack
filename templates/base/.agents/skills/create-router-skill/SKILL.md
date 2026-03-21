---
name: create-router-skill
description: Use when creating or upgrading a discoverable router skill that selects among a related family of child skills, carries explicit child metadata, and handles install-or-fallback behavior honestly.
---

# Create Router Skill

Use this skill to create or upgrade a top-level router package that keeps a skill family discoverable and houses its leaf skills under one explicit family entrypoint.

A router skill is not just a category label. It is a real entrypoint with a narrow job: decide which child skill should handle the request, then hand off cleanly.

Use `create-skill` for leaf skills and single-job packages. Use this skill only when the package's main job is routing across a family.

## Core Contract

- Keep the router itself discoverable. A family hidden in nested folders with no top-level router is easy to miss and hard to load.
- Keep the router honest. It selects and hands off; it does not quietly perform the full child workflow itself.
- Keep child metadata explicit in `references/children.json`. Do not rely on folder names alone to explain routing, dependencies, or fallbacks.
- Keep child leaf skills inside the router package, but keep their full bodies lazy. Initial discovery should need only the router plus the child inventory, not every nested leaf body loaded up front.
- Keep missing-child behavior truthful. Install the right child when possible; otherwise disclose the fallback instead of silently degrading.

## Entry Gate

Before writing files, answer these questions:

1. What family boundary does this router own?
2. Which child skills belong inside that boundary, and in what selection order?
3. Which relationships matter beyond simple routing: `requires` for prerequisites, `recommends` for conditional next steps or companions, or `fallbacks_to` for explicit degraded paths?
4. What should happen if the best child is missing: install, fallback, or answer directly?
5. Does the runtime discover only top-level skills, or can it follow nested children after the router is loaded?
6. What is the believable baseline: no router, a flat list, or an overloaded umbrella skill?

If you cannot answer these from the request and repo context, ask the smallest focused question needed.

## References

Read these before authoring the router package:

- [router metadata](references/router-metadata.md)
- [relationship types](references/relationship-types.md)
- [router skill template](assets/router-skill-template.md)
- [children template](assets/children-template.json)

## Workflow

### Phase 1 — Confirm It Is Really a Router

Create a router skill only when all of these are true:

- the package's main job is choosing among child skills
- the child set forms a stable family worth naming
- discovery or routing fails without an explicit family entrypoint
- the relationships between children matter enough to record

Do not create a router skill for:

- a single leaf skill
- a loose category page with no decision logic
- a giant umbrella that tries to replace its children
- a folder tree that exists only for visual organization

### Phase 2 — Choose the Honest Layout

Default shape:

```text
router-name/
├── SKILL.md
├── references/
│   ├── children.json
│   ├── router-metadata.md
│   └── relationship-types.md
├── scripts/
│   └── validate_router.py
├── assets/
│   ├── router-skill-template.md
│   └── children-template.json
├── evals/
│   ├── evals.json
│   └── trigger-evals.json
├── child-one/
│   └── SKILL.md
└── child-two/
    └── SKILL.md
```

Use this shape when the router needs:
- a stable child inventory
- typed relationships between children
- deterministic validation of routing metadata
- evaluation of both trigger quality and handoff behavior

Keep family-specific child skills inside this package by default so the router path tells the truth about the family boundary. Use an external child target only when the skill is intentionally shared across families.

### Phase 3 — Author the Router `SKILL.md`

The router body should cover only:

1. family boundary
2. selection order
3. missing/install/fallback policy
4. router output format
5. direct links to any bundled references

The router body should not duplicate the full child inventory. Put change-prone child details in `references/children.json`.

A good router output looks like this:

- `Route to router-name/child-a.`
- `Install router-name/child-a, then route to router-name/child-a.`
- `Fallback to router-name/child-b.`
- `No family child fits; answer directly.`

Add one sentence explaining why the selected child is the narrowest correct fit.

### Phase 4 — Record the Child Inventory

Use `references/children.json` as the source of truth for:

- selection order
- child summaries
- positive and negative routing signals
- dependency-like relationships
- install hints
- explicit fallbacks

Use the starter file in [children template](assets/children-template.json).

Rules:

- `router_name` must match the router frontmatter name.
- Each child `name` must be unique.
- Each child needs a stable `target` for handoff.
- Keep `route_when` intent-based and short.
- Use `requires` only for prerequisites that must be present before the route is honest.
- Use `recommends` only for optional next steps or companion skills that become useful under a named condition. Do not use it as a wish list or a hidden fallback.
- Use `fallbacks_to` only for honest degraded paths.
- If a child is shared across families, reference it here instead of inventing duplicate child packages.

### Phase 5 — Validate the Router Package

Run the bundled validator against the router package you are creating:

```bash
python3 scripts/validate_router.py <router-dir>
```

Use `--strict` when warnings should fail the run.

The validator checks:
- router `SKILL.md` frontmatter basics
- local links in the router body
- `references/children.json` shape
- child-name uniqueness
- relationship references to known children
- install hint structure

Fix every reported error before evaluation.

### Phase 6 — Evaluate Triggering and Handoff

Do not stop at structural validation. Test whether the router actually makes better choices than the baseline.

Record at least three task prompts in `evals/evals.json`:

1. direct family match
2. ambiguous family boundary case
3. noisy case with misleading category words

Record trigger checks in `evals/trigger-evals.json` when discovery precision matters.

Baseline options:
- no router at all
- the previous router version
- direct leaf selection from a flat skill list

Review whether the router:
- chose the right child
- disclosed fallback honestly
- avoided solving the child job inline
- made discovery easier rather than noisier

### Phase 7 — Integrate with Leaf Skill Creation

A router does not replace leaf skill creation.

After the router boundary is stable:
- use `create-skill` to author each child leaf package, but place it under the router directory (for example `router-name/child-name/`)
- move existing family leaf skills under the router package when adopting the nested convention
- keep leaf execution guidance in the child package, not in the router
- update the router's `references/children.json` whenever the child set changes

## Evaluation

- Add realistic prompts to `evals/evals.json`.
- Add routing boundary checks to `evals/trigger-evals.json`.
- Compare the router against the believable baseline.
- Patch only the missing rule or metadata. Do not turn the router into a giant encyclopedia.

## Final Checklist

- [ ] The package is truly a router, not a disguised leaf skill or category dump
- [ ] `SKILL.md` stays focused on selection and handoff
- [ ] `references/children.json` is the current source of truth for child metadata
- [ ] Missing/install/fallback behavior is explicit and honest
- [ ] `python3 scripts/validate_router.py <router-dir>` passes
- [ ] `evals/evals.json` and `evals/trigger-evals.json` cover direct, ambiguous, and noisy cases
- [ ] Leaf execution guidance still lives in leaf skills, not the router
