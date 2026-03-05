---
name: self-cognitive
description: >
  Structured self-verification, retrospective, and skill extraction.
  USE when the user says: "confidence check", "sanity check", "am I thinking about this right",
  "retrospective", "postmortem", "lessons learned", "what went wrong",
  "make this repeatable", "turn into a skill", "persist this", "extract a workflow".
  Also USE proactively before risky decisions or after failures—do not wait to be asked.
---

# Self-Cognitive Meta Skill

Provide a structured self-cognitive response that verifies reasoning, captures lessons, and produces persistable updates. This skill follows skill-creator writing guidelines.

## Modes

Choose the smallest set that matches the request:
- **Preflight Verification**: Before execution or decisions.
- **Postflight Retro**: After work is done or after errors.
- **Skill Extraction**: When the user wants persistence or repeatability.

## Core Rules

- Separate facts from assumptions.
- State risks and how to validate quickly.
- Calibrate confidence (low/medium/high) with evidence.
- Never include secrets or sensitive data.
- Keep outputs concise; prefer bullets.
- Always include the JSON artifact (see `references/artifacts.json` for full template).
- If this file grows, move detailed guidance to `references/`.

## Iteration Loop

1. Draft with the required template.
2. Compare against required sections and JSON artifact.
3. Capture rationalizations or omissions.
4. Update skill update proposal accordingly.
5. Re-run pressure scenarios until compliant.

## Required Output Template

### Goal
One sentence: what is being verified or improved.

### Current context
- Bullet facts from the conversation.

### Verification
**Assumptions** — list each, mark validated or unvalidated.
**Risks and failure modes** — what breaks and impact.
**Checks** — concrete actions to validate.
**Confidence** — level (low/medium/high), why, and how to raise it.

### Lessons learned
**Technical** | **Process** | **Prompting and coordination** — bullets for each.

### Persistable updates
**Memory summary** — user preferences, project facts, open questions.
**Skill update proposal** — if a target skill exists, propose minimal patch. Otherwise, propose new skill outline.
**Artifacts JSON** — populated JSON per `references/artifacts.json` template.

## Common Mistakes

- Skipping verification to save time.
- Omitting the JSON artifact.
- Mixing assumptions with facts.
- Declaring confidence without evidence.
- Treating the first draft as final instead of iterating.

## Rationalization Table

| Excuse | Reality |
|---|---|
| "Skip verification, we're in a rush." | Speed never justifies omitting required sections. |
| "High-level is enough." | The full template is mandatory. |
| "One pass is enough." | Iteration is required to close gaps. |

## Red Flags — STOP and Restart

- "Skip verification to move faster."
- "I'll add lessons learned later."
- "This is too simple to structure."
- "No JSON needed."

Violating the letter of the rules is violating the spirit of the rules.

## Example

### Goal
Validate whether the deployment plan is safe to execute today.

### Current context
- Deployment touches auth config and rate limits.

### Verification
- **Assumptions**: Rate limit change is backward compatible.
- **Risks**: Auth flow could reject valid tokens.
- **Checks**: Dry-run staging deploy and login.
- **Confidence**: Medium — staging verified, no prod traffic tested. To raise: run canary on 5% traffic.

### Lessons learned
- **Technical**: Staging coverage missed token edge case.
- **Process**: Add token-matrix checklist to deploys.
- **Prompting**: Ask for rollout window upfront.

### Persistable updates
- **Memory**: User wants explicit confidence levels. Auth uses token rotation. Open: canary tooling availability.
- **Skill update**: Draft rollout-checklist skill if repeated.
- **Artifacts JSON**: *(populated per `references/artifacts.json`)*
