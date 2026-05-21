---
name: requirements-writer
description: Use when a validated blueprint exists and you need actionable requirements, user stories, and acceptance criteria that become .agents-stack/reference/product/requirements.md.
---

# Requirements Writer

## Placement
This is a nested child under `greenfield-product`; its path is `greenfield-product/requirements-writer/`, and the router selects it before standalone use.

Use this skill to turn a validated blueprint into testable product requirements.

## Core contract

- Start only after the blueprint is validated.
- Stay out of system design and implementation detail.
- Write requirements that another engineer can build from without guessing.
- Produce `.agents-stack/reference/product/requirements.md`.

## Focus

Cover the minimum that makes the PRD honest:

- user stories and jobs to be done
- acceptance criteria
- edge cases and failure states
- non-goals and scope boundaries
- open questions that must be resolved before engineering

## Output

Return requirements that are specific enough to gate implementation and review.
