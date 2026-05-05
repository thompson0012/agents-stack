# Templates

Canonical templates for all agents-stack harness artifacts. Copy from here; do not construct from memory.

## `.harness/` — sprint-local artifacts

| Template | Created by | Purpose |
|---|---|---|
| `status.json` | generator-proposal | Machine-readable sprint phase, owner, heartbeat, retry budget |
| `sprint_proposal.md` | generator-proposal | Scope, acceptance criteria, risks, non-goals |
| `contract.md` | evaluator-contract-review | Approved execution boundary with AC-### checks |
| `runtime.md` | generator-execution | Environment, build triage, execution log, resume checkpoint |
| `handoff.md` | generator-execution | What changed, how to verify, contract coverage, human gate |
| `review.md` | adversarial-live-review | PASS/FAIL/BLOCKED verdict with before/action/after evidence |
| `qa.md` | adversarial-live-review | Detailed reproduction evidence log (optional) |

## Usage

1. Copy the template into `.harness/<WORKSTREAM-ID>/`
2. Fill `[PLACEHOLDER]` markers
3. Delete HTML comment blocks (`<!-- ... -->`)
4. Do not leave template annotations in the live file

## Migration

Diff an existing `.harness/<WORKSTREAM-ID>/` artifact against its template to detect missing fields or schema drift.
