---
name: extract
description: Use when a workstream audit passes with no deeper insight — read completed workstream artifacts, propose session-retro to capture lessons from the conversation, then archive.
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

## Output

## Done Criteria

- Workstream artifacts read
- Session-retro proposed (or user declined)
