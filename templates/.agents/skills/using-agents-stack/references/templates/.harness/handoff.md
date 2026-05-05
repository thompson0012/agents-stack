# Handoff: [FEATURE-###] [short title]

<!--
  Template: .agents/skills/using-agents-stack/references/templates/.harness/handoff.md
  Owner: generator-execution
  Write this only after build/startup triage passes and the sprint is reviewable.
  This is the human-readable pause boundary and reviewer entry point.
  Delete this comment block before use.
-->

## What Changed

[Summary of implementation: files modified, patterns used, design decisions.]

### Files Changed

- `path/to/file.ts` — [what and why]
- `path/to/other.ts` — [what and why]

## How to Verify

[Exact commands and expected output a reviewer can reproduce.]

```
$ [command]
[expected output or behavior]
```

## Contract Coverage

[Map each AC-### to the verification step that proves it.]

| AC | Verification | Status |
|---|---|---|
| AC-001 | [command / observation] | [verified / partial / unverified] |
| AC-002 | [command / observation] | [verified / partial / unverified] |

## Known Limitations

- [limitation]: [why accepted, future follow-up]

## Risks and Edge Cases

- [risk]: [how it was handled or why it's accepted]

## Resume Instructions

If this sprint is interrupted during review:

1. Read `contract.md` for approved scope
2. Read this handoff for implementation details
3. Run `[verification command]` to confirm the workspace matches

## Human Gate (if awaiting_human)

- **What needs human action**: [exact file, line, or decision]
- **How to tell it's done**: [observable signal]
- **Resume phase after human action**: [next phase]
