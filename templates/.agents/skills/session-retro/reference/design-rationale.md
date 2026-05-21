# Design Rationale: session-retro output files

## Decision
Split `.agents-stack/insights/session-log.md` into three files, each with a single writer.

## Context

Originally, all retro outputs wrote to a single file (`.agents-stack/insights/session-log.md`):
- Tier 1 per-session entries
- Tier 2 consolidation summaries
- Recursive retro entries (v0.3.0)

Tier 2 reads ALL entries to find cross-session patterns. With a single file, it reads its own prior consolidation summaries back as input — self-referencing noise.

## Architecture

```
.agents-stack/insights/
├── session-log.md        ← writer: Tier 1 only. One entry per session retro.
├── consolidation-log.md  ← writer: Tier 2 only. One summary per consolidation run.
└── meta-log.md           ← writer: recursive retro only. Reflection-on-reflection entries.
```

## Why three, not two

| Alternative | Problem |
|-------------|---------|
| session-log + consolidation-log merged | Meta entries are a different scale — they're not about a session, they're about the retro process itself. Mixing them with session entries creates category confusion during Tier 2 reads. |
| Single file with tags | Requires parsing/classification logic in Tier 2. Files as boundary is simpler — the file path IS the category. |

## Read/Write matrix

| File | Written by | Read by |
|------|-----------|---------|
| `session-log.md` | Tier 1 | Tier 2 (to find cross-session patterns) |
| `consolidation-log.md` | Tier 2 | Human (archive of what was promoted) |
| `meta-log.md` | Recursive retro | Human (patterns about retro itself) |

Tier 2 reads ONLY `session-log.md` — clean input, no self-referencing.
