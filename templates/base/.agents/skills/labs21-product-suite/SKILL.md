---
name: labs21-product-suite
description: Use when a user starts a new Labs21 product development workflow or needs to move between strategy, PRD, and system-design phases.
---

# Labs21 Product Suite — Router

## Core Contract

This router owns the stage-gated Labs21 product-development family.
It chooses exactly one child skill, hands off cleanly, and does not perform the child workflow inline.

## Decision Order

1. Raw ideas, strategy, MVP framing, and blueprints from scratch belong to `labs21-chief-architect`.
2. Once a blueprint is validated, PRDs, user stories, acceptance criteria, and edge cases belong to `labs21-prd-writer`.
3. Once a validated PRD exists, schemas, API contracts, state flows, and infrastructure decisions belong to `labs21-system-architect`.
4. If the best child is missing or unavailable, disclose the risk and tell the user what to install or what the nearest honest fallback is.
5. If the requested artifact would skip a prerequisite stage, route to the prerequisite child first.

## Router Output

- `Route to labs21-product-suite/labs21-chief-architect.`
- `Route to labs21-product-suite/labs21-prd-writer.`
- `Route to labs21-product-suite/labs21-system-architect.`
- `Install labs21-product-suite/labs21-chief-architect, then route to labs21-product-suite/labs21-chief-architect.`
- `Install labs21-product-suite/labs21-prd-writer, then route to labs21-product-suite/labs21-prd-writer.`
- `Install labs21-product-suite/labs21-system-architect, then route to labs21-product-suite/labs21-system-architect.`
- `No labs21-product-suite child fits; answer directly.`

## References

- [child inventory](references/children.json)
- [router metadata](references/router-metadata.md)
- [relationship types](references/relationship-types.md)

## Family Workflow Boundary

1. This router owns Stage 1 strategy, Stage 2 product definition, and Stage 3 system design for new Labs21 product work.
2. This router does not answer the substantive product question itself; it selects the narrowest child that can.
3. This router must surface missing prerequisite artifacts instead of silently skipping ahead.
4. This router must hand off to the selected child and continue from that child's workflow.
5. This router must stay truthful about the shipped child set and the order in which the stage gates are evaluated.
