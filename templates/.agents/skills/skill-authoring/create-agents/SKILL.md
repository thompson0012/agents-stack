---
name: create-agents
description: Use when creating or upgrading reusable agent manifests or agent teams with explicit model profile metadata and harness-style contracts.
---

# Create Agents

Use this skill to author reusable agent manifests for `templates/.agents/agents/` or another shared agent directory.

The job is to make a specialist agent loadable, narrow, and honest about its scope, uncertainty handling, and fallback behavior.

## Core Contract

- Solve one repeatable agent job.
- Keep the manifest portable: discovery metadata up top, execution contract in the body.
- Keep the agent role narrow enough that another agent can tell when to use it.
- Use harness-style language: file-backed truth, explicit uncertainty, and no silent fallback.
- Use `meta-prompting` as the prompt-architecture lens when shaping the agent body.
- If the request is really a skill package (leaf or router), use `create-skill` instead.

## Role Set

For coding work, the default reusable agent set is:

- `task` for bounded implementation or patch work
- `explore` for evidence gathering and codebase discovery
- `plan` for scoping, sequencing, and risk framing
- `librarian` for reusable knowledge, inventories, and convention lookup

Only expand the set when the request proves another specialist is necessary.

## Workflow

1. Define the agent's job, scope boundary, and primary evidence surface.
2. Choose the narrowest role and output contract.
3. Write frontmatter with `name` and `description` only.
4. Write the body with role, core contract, uncertainty labels, fallback behavior, and output shape.
5. If the agent is part of a team, keep shared conventions in `references/` and role-specific behavior in the individual manifest.
6. Add direct evals that test discovery, a near-miss boundary, and a noisy case.

## Uncertainty Protocol

- Label observations as `OBSERVED`, `INFERRED`, or `UNKNOWN`.
- Do not present an inference as a measured fact.
- If a decision depends on missing information, say what is missing and whether a safe default exists.
- If the missing detail changes shared token, contract, or routing behavior, ask before inventing the answer.

## References

- [agent roles](references/agent-roles.md)
- meta-prompting
- [agent template](assets/agent-template.md)

## Evaluation

- Add at least three prompts to `evals/evals.json`.
- Add `evals/trigger-evals.json` when discovery precision matters.
- Compare against a believable baseline, such as the old persona-style manifest or no agent package.

## Final Checklist

- [ ] The agent job is singular and reusable
- [ ] The body explains role, scope, uncertainty, and fallback behavior
- [ ] Shared team conventions live in references, not duplicated prose
- [ ] Evals cover direct, near-miss, and noisy cases
