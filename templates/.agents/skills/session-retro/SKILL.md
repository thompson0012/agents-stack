---
name: session-retro
description: Use when a session is ending — audits the orchestrator-human conversation against agentic-engineering principles, extracts patterns and insights with causal power over future decisions. Trigger via /retro, extract proposal, or orchestrator closure signals.
version: 0.3.0
---

# Session Retro

Closing ritual. Focuses on what the orchestrator-human collaboration taught us. Has write capability — Tier 2 promotes accumulated insights to `docs/reference/` and `docs/records/`.

**Data source**: the conversation itself (decisions, delegation patterns, tool usage).
**Contrast with extract**: extract reads `.harness/<ID>/` workstream artifacts. session-retro reads the conversation. extract and session-retro Tier 1 share `docs/insights/session-log.md` as a common output target.

## Output Files

One writer per file. The file path IS the category — no parsing needed to classify entries.

| File | Writer | Content |
|------|--------|---------|
| `docs/insights/session-log.md` | Tier 1 (and extract) | Per-session retro entries |
| `docs/insights/consolidation-log.md` | Tier 2 | Consolidation run summaries |
| `docs/insights/meta-log.md` | Recursive retro | Reflection-on-reflection entries |

**Why split**: with a single file, Tier 2 reads its own prior consolidation summaries back as input — self-referencing noise. With three files, Tier 2 reads ONLY `session-log.md` (clean per-session input).

## Goals

Two-tier design:

| Tier | Level | Trigger | Data source | Purpose |
|------|-------|---------|-------------|---------|
| 1 | Per-session | `/retro`, orchestrator closure signals, or extract proposal | Conversation context | What did this collaboration session teach us? |
| 2 | Cross-session | Human types `/retro --consolidate` | Accumulated session-log entries | Scan and promote stable patterns to reference/records |

Tier 1 answers: **what did we learn about how we work together?**
Tier 2 answers: **what patterns are stable enough to become project truth?**

Beyond tiers, retro operates at three depths within a session:
- **Content depth**: What domain knowledge was gained? (the "what" of the conversation)
- **Process depth**: What collaboration patterns emerged? (the "how" of the interaction)
- **Meta depth**: What did the act of reflecting itself reveal about how we learn? (recursive — reflection on the reflection)

## Trigger Rules

### Manual
User types `/retro` → run Tier 1.
User types `/retro --consolidate` → run Tier 2.

### From extract
After extract Tier 1 completes, orchestrator asks: "Workstream extracted. Run session retro to capture conversation-level lessons?" If user says yes → run session-retro Tier 1 with extract's workstream context.

### From orchestrator (auto-propose)
Two or more signals present:
- Last 2+ turns were verification / "done" style exchanges
- User said "好了" / "就這樣" / "沒了" / "ok" / "done"
- Multiple files changed and no new work queued
- A `verification-before-completion` pass just completed

Ask "Run session retro?" — one line. If yes → run Tier 1. If no → drop.

## Output Format — Tier 1

Write to `docs/insights/session-log.md`. Each entry (same format also used by recursive retro, written to `meta-log.md`):

```markdown
---
origin: <session-id-or-auto>
date: <ISO-date>
source: session-retro
---

### Decisions (why, not what)
- Reason we chose A over B. Tradeoffs considered.

### Pivot Moments
- When did the human reject the AI's initial framing? What was the redirect?
- What did the second attempt reveal that the first missed?
- If replaying: at what node should the AI have offered a different interpretation?

### Unresolved
- Known gaps, parked work, Phase 2 items. Why parked.

### Pitfalls
- Non-obvious edge cases, dependency surprises, time-wasters. Root cause.

### Patterns
- Reusable method or heuristic. How to recognize when it applies again.

### Charter violations
- Principle(s) violated, anti-pattern matched. Concrete location/decision.

### API surface
- Semantic changes to public API. What was added, deprecated, removed.

### Meta
- What did this retro itself reveal about how we reflect?
- Any reflection structures worth extracting as reusable methods?
```

Omit empty sections. Never pad.

## Format Guidance

Not all insights are best expressed as bullet lists. Match format to cognitive structure:

| Insight type | Use | Example |
|-------------|-----|---------|
| Conditional pattern (when X, do Y; when Z, do W) | **Decision tree** | "When the human says 'why', answer the question behind the question" |
| Mistake with corrective | **❌ vs ✅ contrast table** | "❌ Hard-coded hex → ✅ Token variable" |
| Progressive constraint refinement across turns | **Gradient table** | Show how each turn narrowed from fuzzy goal to precise constraint |
| Cross-cutting meta-insight | **Layered paragraph** | "This pattern appears at content, process, AND meta levels" |

## Execution Flow

### Tier 1 — Per-session retro

1. **Orchestrator** loads this skill.
2. **Orchestrator** prepares a compact context packet for @oracle:
   - Key decisions made this session (what was debated, what was chosen)
   - Files changed (paths only, not content)
   - Notable discussion themes
   - Any known regrets or second-guesses
   - If triggered by extract: include workstream ID and key findings from extract Tier 1
3. **Orchestrator** delegates to @oracle with the context packet + filtering rule.
4. **@oracle** audits, returns structured verdict.
5. **Orchestrator** appends to `docs/insights/session-log.md`.
6. **Orchestrator** reports: "Retro done. N items recorded."
7. **Orchestrator** checks entry count: if count % 5 == 0, suggest: "N sessions recorded. Run `/retro --consolidate` to promote patterns?"
8. **Orchestrator** checks the `### Meta` section: if it contains a concrete reflection structure worth extracting, ask: "This retro surfaced a reflection method itself. Run a recursive retro to capture it?" If yes → run Tier 1 again treating the first retro as the conversation under audit, but write output to `docs/insights/meta-log.md`. Maximum one recursion per session.

### Tier 2 — Cross-session consolidation

Human-triggered only (`/retro --consolidate`). Not auto-proposed without human confirmation.

1. **Orchestrator** reads all entries from `docs/insights/session-log.md`.
2. **Orchestrator** delegates to @oracle with all entries.
3. **@oracle** returns a consolidation plan:
   - **Emerging patterns** — heuristics surfaced repeatedly across sessions
   - **Chronic violations** — principles that keep being broken
   - **Stable decisions** — decisions made consistently (candidates for reference/records)
   - **Meta-patterns** — patterns about pattern-recognition itself (e.g., recurring cognitive blind spots, dimensions AI output systematically omits, types of insight the human consistently fails to extract)
   - **Recommended promotions** — which patterns are stable enough for `docs/reference/` or `docs/records/`, with target path and rationale
4. **Orchestrator** presents the plan to the user:
   - For each promotion candidate: explain why it's stable, where it would go, and what it would change
   - Let user decide which promotions to execute
5. **User reviews and approves/rejects** each promotion.
6. For approved promotions:
   - Write to `docs/reference/` or `docs/records/`
   - Append a consolidation summary entry to `docs/insights/consolidation-log.md` listing what was promoted and where
7. **Orchestrator** reports: "Consolidation done. X items promoted."

## Filtering Rule

Before writing any item, ask: **"Would a future session make a different decision if it knew this?"**

| Record | Don't record |
|--------|-------------|
| Why we chose A over B (future may face same tradeoff) | What we did (git log has it) |
| A surprising pitfall with root cause | File manifests (git diff has them) |
| A reusable method discovered | Conversation summary (context-compaction handles that) |
| A principle we violated and why | Handoff context (@agent-handoff does that) |
| Open questions with clear re-open conditions | Vague "think about this later" notes |

Also ask: **"Was there a moment in this session where human intent and AI response were at different levels—and how was the misalignment discovered and corrected?"** This is the highest-signal retro material because it reveals blind spots shared by both sides.

## Constitution Reference

Audits against:
- **16 principles**: `.agents/skills/agentic-engineering-principles/references/principle-details.md`
- **Anti-patterns**: `.agents/skills/agentic-engineering-principles/references/anti-patterns.md`

## Failure Modes

- **Recording everything.** If every session gets an entry, the log becomes noise. Skip sessions where nothing meets the filter.
- **Vague patterns.** "Test more" is useless. "When mock returns dict not model, mypy won't catch it — validate with isinstance at boundary" is useful.
- **Oracle without context.** If the context packet is too thin, oracle invents violations.
- **Forgetting to propose.** Orchestrator must check trigger signals before final "done" message.
- **Cross-session too early.** Running Tier 2 with 1-2 entries in `session-log.md` has nothing to synthesize. Minimum 5 entries.
- **Tier 2 without human.** Tier 2 promotes to reference/records — only the human can judge what's stable enough. Never auto-execute promotions.
- **Flat retro.** Recording only content-level insights (what was decided) while missing process-level (how the collaboration worked) and meta-level (how we learned to learn). A retro that never surfaces a pivot moment or alignment failure is probably incomplete — it only captured one of three depths.
