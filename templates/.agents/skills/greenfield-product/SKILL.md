---
name: greenfield-product
description: Use when starting a new product from a raw idea, pressure-testing startup viability, or moving through blueprint, requirements, and system-design stages that produce durable reference docs.
---

# Greenfield Product

This router owns the optional greenfield product family. It chooses exactly one child skill, hands off cleanly, and does not perform the child workflow inline.

Read [child inventory](references/children.json) for the authoritative stage order, per-child route conditions, prerequisites, and install hints.
Each child lives under `greenfield-product/<child-name>/`, and child SKILL.md files should say they are nested product-family children.

## Stage Order

1. **Startup pressure test** — `startup-pressure-test` (raw idea, GTM realism, CAC/churn/runway, whether the thesis survives contact with the market)
2. **Product spec pipeline** — `spec-pipeline` (strategic blueprint → requirements → system design; three stages in one child)

The `spec-pipeline` child consolidates three formerly separate stages (product-blueprint, requirements-writer, system-architect) into a single pipeline that produces `.agents-stack/reference/design.md`, `.agents-stack/reference/product/requirements.md`, and `.agents-stack/reference/architecture/implementation.md`.

If the request would skip a prerequisite stage, route to the prerequisite stage within the pipeline or to `startup-pressure-test` first.

## Boundary

- This router does not answer the product question itself; it selects the narrowest child that can.
- This family stops at durable product-definition outputs. Once `.agents-stack/reference/design.md`, `.agents-stack/reference/product/requirements.md`, and `.agents-stack/reference/architecture/implementation.md` exist, defined-feature delivery hands off to the implementation workflow under `using-agents-stack`.
- If the best child is missing at runtime, say to install it. Do not silently substitute.
- If no child fits, say so and answer directly.

## References

- [child inventory](references/children.json)
- [router metadata](references/router-metadata.md)
