# Project Progress Ledger

Record dated sprint outcomes here. Append new entries; do not rewrite history.

Use this ledger for durable audit events, not as a second registry. `docs/live/tracked-work.json` remains the tracked-work source of truth.

Record transitions such as:
- sprint start, pause, escalation, build failure, review failure, PASS archive cutover, and next-action decisions
- record creation in `docs/records/*`
- record promotion into `docs/reference/*`
- record supersession or expiry, with replacement path when one exists

When a record event is tied to tracked work, name the workstream id, record path, and evidence path that justifies it.

## Entry template
- YYYY-MM-DD - EVENT - Workstream: WORKSTREAM-### | none - Paths: `docs/records/...`, `docs/reference/...`, `.harness/...`, or `docs/archive/...` - Notes: brief factual summary