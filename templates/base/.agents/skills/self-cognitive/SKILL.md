---
name: self-cognitive
description: Use when the user asks for a confidence check, retrospective, repeatable workflow extraction, or when a risky decision needs explicit verification before action.
---

# Self-Cognitive

Use this skill to force a verification pass before a risky decision, or to turn completed work into durable lessons and reusable instructions.

## Modes

Choose the smallest mode that fits the request:
- **Preflight verification** — before execution or before committing to a decision.
- **Postflight retrospective** — after work completes or after something goes wrong.
- **Skill extraction** — when the user wants a repeatable workflow, guardrail, or reusable pattern.

## Core Rules

- Separate facts from assumptions.
- State the main risks and how to validate them quickly.
- Calibrate confidence as low, medium, or high and justify it with evidence.
- Add a short disconfirming pass: ask what evidence is missing, what would change the recommendation, and where you should stop instead of proceeding.
- Never include secrets or sensitive data.
- Keep outputs concise; prefer bullets over narrative.
- Include the JSON artifact when the request calls for a persistable record or workflow handoff; the schema lives in `references/artifacts.json`.

## Required Output Template

### Goal
One sentence describing what is being verified, reviewed, or extracted.

### Current context
- Bullet facts from the conversation or work performed.

### Verification
- **Assumptions** — list each assumption and mark it validated or unvalidated.
- **Disconfirming pass** — name the missing evidence, the stop conditions, and what would falsify or materially change the recommendation.
- **Risks and failure modes** — what could break, and what the impact would be.
- **Checks** — concrete actions that would validate the conclusion.
- **Confidence** — low, medium, or high; explain why and what would raise it.

### Lessons learned
- **Technical** — what changed in the system understanding.
- **Process** — what to repeat, stop, or tighten next time.
- **Prompting and coordination** — what would improve future delegation or execution.

### Persistable updates
- **Memory summary** — durable preferences, project facts, and open questions worth carrying forward.
- **Skill update proposal** — the minimal reusable rule, checklist, or skill patch suggested by the work.
- **Artifacts JSON** — populate the schema from `references/artifacts.json` when requested.

## Iteration Loop

1. Draft the response with the required sections.
2. Check whether facts, assumptions, risks, and confidence are clearly separated.
3. Run a short disconfirming pass: look for missing evidence, hidden blockers, stop conditions, and what would change the recommendation.
4. Remove unsupported claims or vague confidence.
5. Tighten the skill update proposal until it is specific enough to reuse.

## Common Mistakes

- Skipping verification because the answer feels obvious.
- Mixing assumptions with established facts.
- Declaring confidence without naming the evidence.
- Writing lessons learned that are too vague to reuse.
- Omitting the structured artifact when the user asked for something persistable.

## Red Flags

If you catch yourself thinking any of the following, stop and restructure the output:
- "I can skip the checks because I already know the answer."
- "High level is enough; the details do not matter."
- "I will add the lessons learned later."
- "Confidence can stay implicit."