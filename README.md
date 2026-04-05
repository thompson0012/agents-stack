# Agents Stack Starter

This scaffold is a file-backed agents-stack project.

## First-session read order

Read only these files first:
1. `README.md`
2. `AGENTS.md`
3. `docs/scripts/init.sh`

Stop there on a fresh start. If the task needs routing, recovery, or state reconciliation, open `docs/reference/harness.md` next. Do not scan the whole tree on the first pass.

## Copy the scaffold

If you are already inside the generated scaffold, skip the copy step and run `./docs/scripts/init.sh`.

```sh
# From the starter source, copy the scaffold into a clean project directory.
cp -R templates/. my-project
cd my-project

# Create any missing baseline files and directories without overwriting work.
./docs/scripts/init.sh
```

If you want to clone the starter from GitHub instead of copying locally:

```sh
npx degit thompson0012/agents-stack/templates new-project && cd new-project && ./docs/scripts/init.sh
```

After that, the repo is ready for truthful initialization work.

The copied scaffold starts blank: no active sprint, no archive history, and no seeded feature backlog.

## What to edit first

1. Set the project name in `docs/live/features.json`.
2. Record the real source goal in `docs/live/roadmap.md` and `docs/live/current-focus.md`.
3. Add the first backlog item only when it is real, bounded, and ready to track.
4. Fill in `docs/reference/architecture.md` and `docs/reference/design.md` with the truth of the new project.

## What lives where

- `AGENTS.md` — the bootstrap contract, first-read guidance, and compact constitutional guardrails.
- `docs/reference/harness.md` — the full operational constitution: safety invariants, ordered routing, resume and retry rules, state-disagreement handling, and archive semantics.
- `docs/live/features.json` — the authoritative backlog and single runnable-sprint selector.
- `docs/live/ideas.md` — pre-sprint exploration and rejected directions.
- `docs/live/progress.md` — reviewed outcomes and durable next actions.
- `docs/live/memory.md` — durable lessons captured after compounding.
- `docs/reference/architecture.md` and `docs/reference/design.md` — stable architecture and design intent placeholders.
- `.harness/<feature-id>/` — sprint-local proposal, contract, execution, review, and status state.
- `docs/archive/*` — PASS-only sprint history after reconciliation.

## Ordered harness flow

`project-initializer -> generator-brainstorm -> generator-proposal -> evaluator-contract-review -> generator-execution -> adversarial-live-review -> state-update -> compound-capture`

Routing is deterministic, not free-form:
- `review.md` always routes to `state-update` before any retry or new proposal work.
- `compound_pending_feature_ids` drains before runnable sprint resume or new backlog selection.
- PASS archives only after `state-update`; FAIL and BLOCKED keep evidence in `.harness/<feature-id>/`.
- `build_failed` and `review_failed` retries require remaining attempt budget and a durable `clean_restore_ref`.

## Notes

- `./docs/scripts/init.sh` is safe to run repeatedly; it only creates missing baseline files.
- `docs/live/features.json` is the source of truth for what is runnable right now.
- `docs/live/ideas.md` is not a runnable schedule.
- If routing, resume, retry, or state disagreement is unclear, open `docs/reference/harness.md` before acting.
