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
2. **Strategy / blueprint** — `product-blueprint` (raw ideas, MVP framing, blueprint -> `docs/reference/design.md`)
3. **Requirements** — `requirements-writer` (validated blueprint -> `docs/records/product/requirements.md`)
4. **System design** — `system-architect` (validated requirements -> `docs/records/architecture/implementation.md`)

If the request would skip a prerequisite stage, route to the prerequisite child first and surface the gap.

## Boundary

- This router does not answer the product question itself; it selects the narrowest child that can.
- This family stops at durable product-definition outputs. Once `docs/reference/design.md`, `docs/records/product/requirements.md`, and `docs/records/architecture/implementation.md` exist, defined-feature delivery hands off to the implementation workflow under `using-agents-stack`.
- If the best child is missing at runtime, say to install it. Do not silently substitute.
- If no child fits, say so and answer directly.

## References

- [child inventory](references/children.json)
- [router metadata](references/router-metadata.md)
