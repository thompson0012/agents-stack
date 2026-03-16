# Current Focus

Read after `AGENTS.md` when starting or resuming work. Keep this file limited to the current objective and the bounds for active work.

## Objective

Optimize the five reasoning-suite skills from the iteration-1 benchmark findings, rerun a true `skill-creator`-style A/B comparison against iteration-1 skill snapshots, and preserve the iteration-2 benchmark plus static HTML review output.

## Scope

- Keep the optimized target skill sources under `templates/base/.agents/skills/`.
- Keep the evaluation workspace under `templates/base/.agents/skills/reasoning-suite-workspace/`, including both `iteration-1/` and `iteration-2/`.
- Keep the iteration-2 old-skill snapshots under `templates/base/.agents/skills/reasoning-suite-workspace/iteration-2/skill-snapshot/`.
- Keep the static HTML review artifacts under `templates/base/.agents/skills/reasoning-suite-workspace/html/`.
- Preserve the previously repaired packaging workflow and packaged artifacts in `dist/`.

## Constraints

- Use the `skill-creator` workflow for further iteration: rerun workspace executions, grading, benchmark aggregation, and viewer output rather than ad hoc prose-only checks.
- The current benchmarks capture pass-rate structure only; no time, token, or tool-call metrics were collected for either iteration.
- Do not commit from this task.

## Success Criteria

- `templates/base/.agents/skills/reasoning-suite-workspace/iteration-2/benchmark.json` and `benchmark.md` exist and summarize the rerun against `old_skill`.
- Each iteration-2 run directory contains `outputs/analysis.md`, `transcript.md`, and `grading.json`.
- `templates/base/.agents/skills/reasoning-suite-workspace/html/reasoning-suite-iteration-2-review.html` exists and loads as a static review artifact.