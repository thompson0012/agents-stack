---
name: extract
description: Use when a workstream audit passes with no deeper insight — read completed workstream artifacts, propose session-retro to capture lessons from the conversation, then archive.
trigger: When audit.md exists with PASS verdict and no deeper insight, and extract.md does not exist for this workstream.
inputs: [AGENTS.md, plan.md, tracked-work.json, .harness/<ID>/ — all workstream artifacts (thesis, challenge, response, synthesis, contract, handoff, audit)]
outputs: [.harness/<id>/extract.md, .harness/<id>/status.json]
boundaries: Read-only except extract.md and status.json. Must not write to session-log.md directly. Must not archive — archive is handled by the orchestrator after extract completes.
---

# Extract

After audit PASS + no deeper insight. Run before archive.

Extract does NOT write to session-log.md directly. Its job is to read what happened in the workstream and trigger session-retro, which scans the conversation and writes to session-log.md.

Then archive.

## Required Reads

- `.harness/<ID>/` — all workstream artifacts (thesis, challenge, response, synthesis, contract, handoff, audit)

## What Extract Does

1. Read all workstream artifacts to understand what was accomplished.
2. Ask orchestrator: propose session-retro Tier 1 to capture conversation-level lessons from this session.
   - Provide the workstream ID and key findings as context for session-retro's @oracle audit.
   - If user declines, proceed to archive with nothing extracted.
3. Archive the workstream.

Extract makes no direct writes to session-log.md, docs/reference/, or docs/records/.
Cross-session consolidation to reference/records is handled by session-retro Tier 2 (`/retro --consolidate`), which is human-triggered.

## Output: extract.md

```markdown
# Extract

## Workstream
- ID: [WORKSTREAM-ID]
- Title: [title]

## Summary
[What was accomplished in the workstream — key outcomes]

## Key Findings
[Insights worth preserving from the workstream artifacts]

## Retro Context
[Key topics for session-retro to examine — used by orchestrator to propose Tier 1 retro]
```

## Workflow

1. Read all workstream artifacts (thesis through audit)
2. Write `extract.md` with summary, key findings, and retro context
3. Update `status.json`: `phase: "extract"`
4. Return to orchestrator — orchestrator proposes session-retro, then archives

## Done

- All workstream artifacts read
- `extract.md` written with key findings and retro context
- `status.json` reflects extract phase
- Session-retro ready to be proposed by orchestrator
