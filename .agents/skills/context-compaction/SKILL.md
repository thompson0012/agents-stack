---
name: context-compaction
description: Use when the conversation context is getting long, approaching token limits, switching sessions, or when asked to summarize/compact the current session state for handoff or continuation.
---

# Context Compaction

## Overview
Transform a long conversation history into a **single canonical state snapshot** that allows seamless continuation — without loss of critical instructions, decisions, or progress. The goal is maximum fidelity at minimum token cost.

## When to Use
- Context window is approaching limits
- Starting a new session to continue existing work
- Handing off to another agent or session
- User asks to "compact", "summarize session", "save state", or "create a handoff"

## Core Principles

1. **Lossless Signal Preservation** — Verbatim accuracy for critical data: file paths, IDs, variable values, constraints, agreed definitions. Never approximate.
2. **Single Canonical Representation** — If a decision evolved, record only the final state. Strip the history of changes, keep only the result.
3. **Lazy Load via Document References** — Do NOT inline full file contents. Reference paths instead: `"re-read when needed: docs/reference/design.md"`. This prevents bloating the compacted context.
4. **Agents.md Instructions are Sacred** — Always extract and preserve active behavioral rules from `AGENTS.md` and session-level overrides.
5. **Objective Drift Awareness** — Record both the original objective AND the current focus objective separately if they have diverged.
6. **Style Normalization** — Strip all emotional tone, hesitation, conversational filler. Output reads like a system log.

## Required Output Format

```markdown
# 📦 Compacted Session State
**Compacted:** [ISO timestamp] | **Est. Tokens:** [count]

<preserve>
## 🏗️ Structural State
| Dimension | Value |
| :--- | :--- |
| **Original Objective** | [What the session was originally opened to do] |
| **Current Focus** | [What is actively being worked on right now] |
| **Phase** | Planning / Development / Debugging / Review / Deployment |
| **CWD** | [Absolute working directory path] |
| **Auto-Pilot** | ON / OFF |
</preserve>

<preserve>
## 📜 Active Agents.md Rules (Session-Level)
- [Any AGENTS.md protocols currently active, e.g. "AUTO-PILOT mode ON", "EMERGENCY override active"]
- [Any user-overridden behaviors explicitly set this session]
- No active overrides: [state this explicitly if none]

→ Full rules: re-read when needed: `AGENTS.md`
</preserve>

## 🧬 Knowledge Graph (Merged & De-duplicated)
- `[entity/variable]`: **[value]**
  - *Definition:* [Synthesized from across the session]
  - *Constraints:* [Hard limits]

## 🧠 Decisions (Compressed)
- **[Topic]** → **[Final Decision]**
  - *Why:* [Core reason — 1 sentence]

## 🚧 Progress & Milestones
- [x] **[Milestone]**: [Result / output data]
- [ ] **[Milestone]**: [Blocker / requirements]

## 📁 File State
| File | Status | Notes |
| :--- | :--- | :--- |
| `[path]` | Modified / Created / Pending | [Brief note] |

→ For full context on any file, re-read the file directly when needed.

## 📋 Open Tasks
- [ ] [Task 1]
- [ ] [Task 2]

## ⚠️ Critical Persistent Info
<!-- Things that MUST NOT be lost between sessions -->
- [e.g., "Invariant: all inputs sanitized before DB write"]
- [e.g., "API key in .env — never commit"]
- [e.g., "Schema: users(id, name, email, created_at)"]

## 🔁 Continue From Here
**Last action:** [Exact last thing the agent did or was doing]
**Next action:** [What must happen first upon resuming]
**Missing info:** [What is still needed from the user, if anything]
```

## Pruning Rules

| Keep | Prune |
| :--- | :--- |
| Final decisions and rationale | History of how decisions evolved |
| Current file paths and status | Old tool output logs |
| Active constraints and invariants | Repeated explanations |
| Agents.md rule overrides | Verbose earlier turns |
| Open tasks | Resolved/cancelled tasks |
| Critical config/values | Intermediate variable states |

**Focus window:** Summarize first 70% at high level. Preserve detail for the most recent 20-30% of the session.

## Lazy Load Pattern

Do NOT inline file or memory contents. Reference them so the resuming session can pull only what it needs.

### Project documents (repo files)

```markdown
→ Re-read when needed: `docs/reference/design.md`
→ Re-read when needed: `docs/reference/implementation.md`
→ Re-read when needed: `docs/live/progress.md`
→ Re-read when needed: `src/auth/middleware.ts` (modified this session)
```

### External / local memory files

The user may have jotted notes during the session to locations outside the repo — scratch files, local note files, or entries written via any memory tool (e.g. AFS, Obsidian, custom scripts). These must also be lazy-referenced, not inlined.

**Scratch / note files — always use absolute path:**
```markdown
→ Re-read when needed: `~/notes/session-2026-03-05.md`
→ Re-read when needed: `/tmp/research-dump.txt`
```

**Memory tool entries — prefer direct file path over a query command:**

If the tool stores entries as files on disk, record the exact file path so the next session can load it directly with a single read — no search, no query overhead:
```markdown
→ Re-read when needed: `/path/to/.memory-store/agents/researcher/memories/mem_abc123.json`
```

If the exact path is unknown, fall back to the tool's query/recall command, but note this requires a search step:
```markdown
→ Recall when needed: `<tool-query-command> --query "[topic]"` (path unknown; search required)
```

**Rule:** Record WHERE the information lives, not WHAT it says. Direct file path > query command > search hint. Choose the option that minimises reads on resume — the next session should not need to open more than ~3 external files to fully reconstruct critical context.

### When to inline (exceptions only)

Inline only if ALL of these are true:
- Content was created/modified this session AND not yet persisted anywhere on disk
- It is short: < 5 lines or a single critical value
- It would be expensive or impossible to rediscover (e.g., a resolved ambiguity, a one-time token)

## Agents.md Preservation Rule

Extract from `AGENTS.md` and the conversation any active session-level overrides:
- AUTO-PILOT ON/OFF status
- EMERGENCY override (log reason)
- Any user-stated behavioral changes ("for this session, skip approval for X")

If none: explicitly state `"No active AGENTS.md session overrides."` — never leave this blank.

## Common Mistakes

| Mistake | Fix |
| :--- | :--- |
| Inlining entire repo files | Use lazy-load path references instead |
| Inlining memory tool entry contents | Record the file path (or fallback query command) |
| Ignoring external scratch/note/memory files written this session | Scan session history for any file writes or memory-tool calls; lazy-reference them |
| Using a query command when the file path is known | File path > query command — avoids search overhead on resume |
| Listing 10+ lazy-load references | Keep to the ~3 most critical; merge or drop the rest |
| Recording decision history | Keep only the final state |
| Vague milestone entries | Include concrete output/result data |
| Omitting original objective | Always record both original + current focus |
| Leaving Agents.md section blank | Explicitly state "no active overrides" |
| Approximating numbers/paths | Copy verbatim or omit entirely |

## Rationalization Table

| Excuse | Reality |
| :--- | :--- |
| "The history is short, no need to compact" | If context is long enough to cause concern, compact it |
| "I'll just summarize loosely" | Loose summaries lose critical constraints — use the format |
| "Agents.md rules are obvious, skip" | Rules must be explicit; next session can't infer session overrides |
| "File contents are important, include them" | Reference paths; inline only if modified and unsaved |
| "Memory tool entries are internal, skip them" | They are external state the next session must know exists |
| "I'll just use the query command, easier" | If the file path is known, use it — one read beats a search |
| "I don't know where the file is" | Scan session history for Write calls or memory-tool invocations |

## Red Flags — STOP and Fix

- Compacted output is longer than 30% of original — prune harder
- Repo file contents inlined instead of referenced by path
- Memory tool entry contents inlined instead of referenced by file path or fallback query
- External scratch/note/memory files written this session not captured at all
- More than ~3 lazy-load references listed — consolidate or drop lower-priority ones
- Original objective missing (only current focus recorded)
- Agents.md section absent or blank
- Decision history included instead of final decision only
