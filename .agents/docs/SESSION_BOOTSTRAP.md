# Session Bootstrap

> **Version**: 1.0.0  
> **Status**: PRODUCTION  
> **Last Updated**: 2026-03-03

Session startup protocol for consistent context loading before execution.

---

## Startup Sequence

1. Read `AGENTS.md` for behavior and approval rules.
2. Read `/.agents/docs/PROGRESS.md` for active state.
3. Read recent `/.agents/docs/LESSONS.md` entries (last 30 days).
4. Read `/.agents/docs/CODEMAP.md` plus last 5 `/.agents/docs/CHANGELOG.md` entries.
5. Load or create the current objective ledger in `/.agents/docs/ledgers/`.
6. Assess risk tier and load additional docs per AGENTS rules.
7. If using swarm mode, load `/.agents/roles/README.md` and relevant role files.

## Output Checklist

Before implementation begins, confirm:
- Active objective and success criteria
- Scope boundaries
- Approval mode (standard or auto-pilot)
- Required verification method
- Escalation conditions

## Notes

- `PRODUCTION` docs are authoritative over templates.
- Do not assume missing data; ask targeted clarifying questions.
- Keep bootstrap lightweight: load only what task risk requires.
