# Migration Guide

## Purpose
Use this guide for any cutover that changes file layout, schemas, registry fields, or durable ownership while keeping history auditable.

## When to use
- moving docs between folders
- changing names or paths
- promoting drafts to stable reference
- archiving completed work
- migrating a legacy repo to the current harness
- introducing a new durable document class

## Non-goals
- not a source of repo state
- not a second registry
- not a changelog
- not a substitute for `AGENTS.md`
- not a replacement for repo-specific contract or review artifacts

## Read first
1. `AGENTS.md`
2. the current live-state files
3. the active sprint artifacts, if any
4. the affected reference docs
5. any existing records, guides, or archive artifacts
6. any repo-specific migration notes

If a runnable sprint exists, read its local contract/evidence before moving files or changing schemas.

## Generic migration flow

### 1. Inventory
- list every path that might move, split, or disappear
- classify each path by role: live control, record, reference, evidence, guide, or unresolved
- note owners, consumers, and dependencies
- mark ambiguous items for human review instead of guessing
- produce a temporary migration report, but do not turn it into a second registry

### 2. Decide
- choose one destination per path
- decide whether the change is add, modify, move, delete, or keep
- decide whether migration must wait for active work to finish
- decide which compatibility shims are allowed and when they end
- decide what requires human approval

### 3. Backfill
- update registry pointers before removing old paths
- add provenance metadata before or during the move
- preserve one canonical path per concept
- keep temporary aliases explicit and short-lived
- never silently create duplicate sources of truth

### 4. Move or transform
- move durable scoped docs into `docs/records/`
- promote only verified current truth into `docs/reference/`
- keep sprint execution evidence in `.harness/<FEAT-ID>/` or `docs/archive/<FEAT-ID>_<timestamp>/`
- keep guides user-facing and separate from records

### 5. Verify
- every moved doc is still reachable from the registry or backlink path that owns it
- no orphaned durable docs remain
- live control files still tell the truth
- archive remains immutable history
- reference remains current stable truth
- there is still only one tracked-work registry

### 6. Clean up
- remove temporary aliases and redirects
- remove duplicate canonical copies
- append one audit note to the project progress ledger
- close the migration scope when the tree is coherent

## Checklists

### Preflight
- [ ] active work identified
- [ ] ownership known or paused for review
- [ ] target roles decided
- [ ] compatibility window defined
- [ ] human review gates named
- [ ] rollback / restore boundary identified if the migration is risky

### Cutover
- [ ] backfill before move
- [ ] change files in bounded batches
- [ ] keep history append-only
- [ ] update backlinks and registry pointers in the same pass
- [ ] verify before removing old paths
- [ ] do not mutate unrelated live work

### Postflight
- [ ] orphan check passes
- [ ] registry pointers resolve
- [ ] reference docs still represent current truth
- [ ] archive remains immutable
- [ ] audit note appended
- [ ] temporary shims removed
- [ ] any low-confidence ownership items were escalated or recorded for follow-up

## Decision rules
- Repo files win over this guide.
- If the repo has an active sprint, do not mutate its contract or evidence unless migration itself is the sprint.
- If ownership is ambiguous, stop and ask.
- Do not silently create a second registry.
- `docs/records/` is for scoped durable residue.
- `docs/reference/` is for current stable truth.
- `docs/archive/` is for finished evidence.
- `docs/live/` is for control-plane state only.
- `docs/guides/` is for user-facing how-to content.
- Keep a single canonical evidence path per feature or migration target at a time.

## Compatibility shims
- Temporary aliases are allowed only during a named cutover window.
- Compatibility fields must have a removal condition.
- Shims must be explicit, documented, and reversible.
- Temporary copies are allowed only when the original path remains clearly non-canonical.
- Remove shims once consumers are updated.

## Repository-specific notes

### Agents-stack default bindings
- `docs/live/features.json` is the only tracked-work registry.
- `docs/live/progress.md` is the append-only audit trail.
- `docs/live/ideas.md` is pre-proposal exploration.
- `docs/live/roadmap.md` and `docs/live/current-focus.md` are control-plane docs.
- `docs/records/` is durable scoped residue.
- `docs/reference/` is stable current truth.
- `docs/archive/` is immutable PASS history.
- `.harness/<FEAT-ID>/` is active or parked sprint evidence.
- `docs/guides/` is user-facing walkthrough content.
- If a runnable sprint exists, close, park, or escalate it before a bulk migration unless the migration itself is the sprint.
- For template changes, update the source under `templates/` first so generated repos inherit the migration shape.

### Fill in per repo
- Active sprint / blocker:
- Special directories:
- Legacy formats:
- Temporary aliases:
- Human review required for:
- Known consumers that must be updated:
- Paths that must remain immutable:

## Verification done definition
A migration is done when:
- every target path has a clear destination or deliberate keep decision
- every moved item is reachable through its owning registry or backlink
- no durable doc is orphaned
- no temporary shim remains past its cutover window
- the audit trail records what changed
- the repo still tells one coherent story from disk alone
