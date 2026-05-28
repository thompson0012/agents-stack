---
name: spec-pipeline
description: Use when a raw product idea needs a structured blueprint, testable requirements, and implementation design. Covers the full greenfield definition pipeline: vision → PRD → architecture.
---

# Spec Pipeline

This is a nested child under `greenfield-product`; its path is `greenfield-product/spec-pipeline/`, and the router selects it after startup pressure testing.

Use this skill to move a validated product concept through three stages of specification: strategy blueprint → product requirements → system architecture.

## Pipeline Order

```
Startup pressure test (if needed)
    │
    ▼
Stage 1: Blueprint ──→ .agents-stack/reference/design.md
    │
    ▼
Stage 2: Requirements ──→ .agents-stack/reference/product/requirements.md
    │
    ▼
Stage 3: Architecture ──→ .agents-stack/reference/architecture/implementation.md
    │
    ▼
Pipeline: using-agents-stack (implement)
```

Do not skip a stage. Each stage produces the authoritative input for the next. If the request implies a later stage without a validated earlier one, surface the prerequisite gap.

## Stage 1 — Blueprint

Entry condition: A raw product idea exists. No blueprint yet.

Turn the raw idea into a credible product strategy, MVP boundary, and durable product intent. Produce `.agents-stack/reference/design.md`.

### Core contract
- Stay at strategy and blueprint level.
- Do not write PRDs, requirements, or implementation design.
- If the real question is whether the business survives at all, route to `greenfield-product/startup-pressure-test` first.

### Focus

Cover the minimum that makes the direction honest:

- **Target user and problem** — who is this for, what job does it solve?
- **Why now / why this** — what changed to make this viable?
- **MVP boundary** — the smallest thing that delivers value; what's explicitly out of scope
- **Key differentiators** — why existing solutions don't work
- **Major risks and assumptions** — what must be true for this to succeed
- **Next validation steps** — what to test before committing to full build

### Output

A concise strategy / blueprint artifact with clear boundaries and open questions. Becomes `.agents-stack/reference/design.md`.

---

## Stage 2 — Requirements

Entry condition: Blueprint is validated and exists at `.agents-stack/reference/design.md`.

Turn the validated blueprint into testable product requirements that another engineer can build from without guessing. Produce `.agents-stack/reference/product/requirements.md`.

### Core contract
- Start only after the blueprint is validated.
- Stay out of system design and implementation detail.
- Write requirements that are specific enough to gate implementation and review.

### Focus

Cover the minimum that makes the PRD honest:

- **User stories and jobs to be done** — what does each actor need to accomplish?
- **Acceptance criteria** — specific, verifiable conditions for each story
- **Edge cases and failure states** — what happens when things go wrong
- **Non-goals and scope boundaries** — what this release explicitly excludes
- **Open questions** — what must be resolved before engineering begins

### Output

A PRD that an engineer can implement without renegotiating scope. Becomes `.agents-stack/reference/product/requirements.md`.

---

## Stage 3 — Architecture

Entry condition: PRD is validated at `.agents-stack/reference/product/requirements.md`.

Translate approved requirements into concrete implementation design. Produce `.agents-stack/reference/architecture/implementation.md`.

### Core contract
- Start only after the PRD is validated.
- Do not reopen product scope.
- Design the structural foundation — data model, APIs, state flow, deployment shape.

### Focus

Cover the minimum that makes the architecture buildable:

- **Domain entities and schemas** — core data model, relationships, constraints
- **API contracts and boundaries** — service interfaces, events, integration points
- **State transitions and invariants** — what state machine governs the core flow?
- **Infrastructure and integration assumptions** — deployment targets, external dependencies
- **Implementation risks and ADR-worthy decisions** — what choices constrain future flexibility?

### Output

An implementation design that an engineer can build without renegotiating the PRD. Becomes `.agents-stack/reference/architecture/implementation.md`.
