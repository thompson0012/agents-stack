---
name: create-skill
description: Use when creating a new reusable skill, packaging instructions into a skill directory, or rewriting skill guidance into canonical SKILL.md format.
---

# Create Skill

## Overview
Create a reusable skill as a plain-markdown `SKILL.md` with minimal frontmatter and fast-scanning guidance. The goal is a document another agent can discover quickly and apply without reading a transcript.

## When to Use
Use this skill when the user asks to:
- create a new skill or capability
- package a repeatable workflow into a skill directory
- set up or rewrite a `SKILL.md`
- prepare a skill for reuse or sharing

Do not use it for project-specific one-off instructions that belong in repo docs or task notes.

## Quick Reference

| Item | Requirement |
| --- | --- |
| Directory | `skill-name/` |
| Required file | `SKILL.md` |
| Frontmatter fields | `name`, `description` only |
| `name` | Must match directory name exactly |
| `description` | Starts with `Use when...`; third person; trigger conditions only |
| Body structure | `# Title`, `## Overview`, `## When to Use`, then practical reference sections |

## Workflow
1. Define the skill boundary.
   - Capture the reusable capability, not the story of one past task.
   - Confirm the skill is broad enough to matter again.
2. Choose the name.
   - Keep it aligned to the directory name.
   - Prefer descriptive, hyphenated names.
3. Write the description for discovery.
   - Describe when the skill should be loaded.
   - Include trigger situations, symptoms, or request phrases.
   - Do not summarize the workflow in the description.
4. Draft the body for scanning.
   - Start with a short overview.
   - Add a `When to Use` section with clear bullets.
   - Add only the sections that help execution: checklist, workflow, quick reference, examples, common mistakes.
5. Keep reference material honest.
   - Inline short guidance.
   - Break out only genuinely heavy reference material.
6. Re-read the final markdown.
   - Verify frontmatter is exactly two fields.
   - Verify the document reads like a skill, not a raw note dump.

## Writing Guidelines
- Optimize for discovery first, execution second.
- Prefer bullets, tables, and short numbered steps over prose blocks.
- Preserve the original capability while removing stale platform-specific advice.
- Use one concept per section.
- Explain non-obvious tradeoffs or failure modes, not obvious mechanics.

## Common Mistakes
- Adding extra frontmatter fields beyond `name` and `description`
- Writing a description that explains the process instead of the trigger
- Copying a long transcript into `SKILL.md` without restructuring it
- Keeping obsolete validation or packaging instructions that are not central to the skill
- Creating a skill for a one-off project convention instead of a reusable pattern

## Final Checklist
- [ ] `SKILL.md` is plain markdown
- [ ] Frontmatter contains only `name` and `description`
- [ ] `name` matches the directory name exactly
- [ ] `description` begins with `Use when...`
- [ ] Body has `Overview` and `When to Use`
- [ ] Remaining sections are concise and useful for execution
- [ ] Content reflects the current canonical skill format
