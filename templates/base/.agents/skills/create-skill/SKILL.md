---
name: create-skill
description: Use when creating a new reusable skill, upgrading an existing skill package, scaffolding a SKILL.md directory, or rewriting skill guidance into a portable LLM-agnostic format.
---

# Create Skill

Use this skill to create or upgrade a reusable skill package that another agent can discover quickly and apply across runtimes.

Build the portable core first. Add runtime-specific metadata, packaging, or tooling only after the core package works without vendor assumptions.

If the package's main job is routing across a skill family, preserving discoverability for nested children, or carrying child-selection metadata, do not force that into a leaf skill. Use `create-router-skill` instead.

## Core Contract

- Solve one repeatable job. If the work is project-specific or one-off, put it in repo docs instead.
- Keep the canonical core portable: default to `name` and `description` frontmatter only.
- Put trigger conditions in `description`; put workflow, checklists, and edge cases in the body.
- Keep `SKILL.md` lean. Move heavy or conditional detail into `references/`, deterministic code into `scripts/`, and copyable starter files into `assets/`.
- Validate structure before claiming the package is usable.
- Pressure-test the skill with real prompts before calling it done.
- When evaluation matters, compare the current candidate against an honest baseline instead of grading by vibes.
- Do not overload a leaf skill with family-routing responsibilities. A router is a different job from execution guidance.

## Entry Gate

Before writing files, answer these six questions:

1. What is the single responsibility of the skill?
2. What concrete task fails, repeats, or degrades without it?
3. What runtime capabilities matter: filesystem, shell, network, package install, archive format, sharing model?
4. What does the user provide, and what should the skill produce?
5. What would a believable baseline be: no skill, old skill, or another workflow?
6. How fragile is the workflow: low, medium, or high?

If you cannot answer these from the request and repo context, ask the smallest focused question needed.

## Quick Reference

| Decision | Default |
| --- | --- |
| Directory shape | `skill-name/` with `SKILL.md` required |
| Frontmatter | `name`, `description` only |
| Name style | lowercase letters, numbers, hyphens; match directory exactly |
| Description style | start with `Use when ...`; describe trigger conditions, not the workflow |
| Core body job | explain how to execute the skill, not when to load it |
| Heavy detail | move to `references/` |
| Deterministic repeated logic | move to `scripts/` |
| Starter artifacts | place in `assets/` |
| Task evals | record them in `evals/evals.json` |
| Trigger evals | record them in `evals/trigger-evals.json` when discovery precision matters |
| Validation | run `python3 scripts/validate.py <skill-dir>` |
| Packaging | run `python3 scripts/package_skill.py <skill-dir>` |

For deeper guidance, read:

- [patterns](references/patterns.md)
- [evaluation](references/evaluation.md)
- [eval schemas](references/eval-schemas.md)
- [portability](references/portability.md)
- [security](references/security.md)
- [anti-patterns](references/anti-patterns.md)

## Workflow

### Phase 1 — Define the Boundary

Decide whether the work belongs in a skill at all.

Create a skill only when all of these are true:

- the workflow will recur
- another agent would benefit from the same guidance
- the behavior is broader than one repository convention
- the knowledge is procedural, domain-specific, or tool-specific enough to matter

Do not create a skill for:

- a one-off task summary
- repo-local instructions better kept in `AGENTS.md` or project docs
- obvious best practices with no special context
- a family router whose main job is selecting among child skills and handling install-or-fallback behavior; use `create-router-skill` instead

### Phase 2 — Choose the Smallest Useful Package

Start with the smallest shape that honestly covers the job.

```text
SKILL.md only                 -> simple, stable workflow
SKILL.md + references/        -> heavy or conditional reference detail
SKILL.md + scripts/           -> repeated deterministic code or fragile execution
SKILL.md + assets/            -> templates, starter files, or reusable output inputs
SKILL.md + evals/             -> structured evaluation or baseline comparison matters
```

Use [scaffold.py](scripts/scaffold.py) when creating a new package from scratch: `python3 scripts/scaffold.py <skill-name>`.

### Phase 3 — Author `SKILL.md`

#### Frontmatter

Use the portable default:

```yaml
---
name: skill-name
description: Use when [trigger conditions and symptoms].
---
```

Rules:

- `name` must match the directory name exactly.
- Prefer short action-oriented hyphenated names.
- Keep the description about discovery: when this skill applies, what requests or symptoms should trigger it.
- Do not summarize the workflow in the description.
- Add extra metadata only when the target environment explicitly requires it.

#### Body

Write for fast scanning and reliable execution.

Recommended section order:

1. `# Title`
2. short overview
3. core contract or non-negotiables
4. workflow or phase-by-phase steps
5. references to bundled files when needed
6. final checklist or failure modes

Use the instruction style that matches workflow fragility. See [patterns](references/patterns.md) for the decision table.

### Phase 4 — Add Bundled Resources

#### `references/`

Use for information another agent may need to read while working:

- selection rules
- edge cases
- domain schemas
- platform notes
- security checklists
- evaluation design and review methods

Keep references one hop deep from `SKILL.md`. A direct link like [evaluation](references/evaluation.md) is good. Nested chains are not.

#### `scripts/`

Use for deterministic steps the agent would otherwise rewrite or execute inconsistently.

Script rules:

- prefer standard-library dependencies
- handle missing files and invalid input explicitly
- keep paths relative and scoped
- print actionable failures
- say in `SKILL.md` when to run the script and what success looks like

#### `assets/`

Use for starter templates or files meant to be copied into output, not read as core instructions.

#### `evals/`

Use for structured prompt sets that let you compare the candidate skill against a baseline.

- `evals/evals.json` stores task-level eval prompts
- `evals/trigger-evals.json` stores should-trigger and should-not-trigger discovery checks
- keep generated run outputs outside the skill package; use a sibling workspace or temp directory instead

### Phase 5 — Validate the Package

Run:

```bash
python3 scripts/validate.py <skill-dir>
```

Fix every reported error before moving on.

Use `--strict` when you want warnings to fail the run.

### Phase 6 — Design the Evaluation Set

Do not stop at structural validation. Test whether the skill is actually discoverable and useful.

Start with [evals-template.json](assets/evals-template.json) and, when discovery precision matters, [trigger-evals-template.json](assets/trigger-evals-template.json).

For task evals, record at least three realistic prompts in `evals/evals.json`:

1. direct match — obvious trigger and expected workflow
2. ambiguous near miss — adjacent request that may or may not belong to the skill
3. noisy or adversarial case — extra context, distractions, or misleading keywords

If you are upgrading an existing skill, compare the candidate against the previous version. If you are creating a brand-new skill, compare against doing the task without the skill or with the default workflow.

### Phase 7 — Run, Review, and Compare

See [evaluation](references/evaluation.md) and [eval schemas](references/eval-schemas.md) for the full loop.

At minimum:

- run the same prompts against the candidate and the baseline
- capture outputs separately
- record what succeeded, what drifted, and what cost more time or effort
- if the output is subjective, use [review-template.md](assets/review-template.md) for blind comparison notes before editing the skill again

Patch only the missing instruction, example, or resource. Do not bloat the skill with speculative rules.

### Phase 8 — Tune Discovery and Packaging

If the skill is structurally sound but triggers poorly, use `evals/trigger-evals.json` and the guidance in [evaluation](references/evaluation.md) to refine `description` without stuffing keywords.

When you need to transfer or archive the package, create a generic ZIP archive with [package_skill.py](scripts/package_skill.py):

```bash
python3 scripts/package_skill.py <skill-dir>
```

This packages the folder without making one runtime's archive extension the canonical truth.

### Phase 9 — Runtime-Specific Layering

Only after the portable core is solid, add any target-runtime requirements the deployment surface needs.

Use [portability](references/portability.md) to check:

- whether network is available
- whether packages can be installed
- whether shell or code execution exists
- how sharing or packaging works
- which metadata fields are actually required

The portable core should remain readable even if those runtime overlays are removed.

### Phase 10 — Security Review

Before shipping a skill with scripts or external access, review [security](references/security.md).

At minimum verify:

- no secrets are hardcoded
- no script writes outside intended paths
- no hidden network calls or background fetches exist
- remote content is treated as untrusted input
- generated run artifacts are not accidentally bundled into the archive you ship

## Final Checklist

- [ ] The skill solves one repeatable job
- [ ] `name` matches directory name exactly
- [ ] `description` starts with `Use when`
- [ ] `description` explains triggers, not the workflow
- [ ] `SKILL.md` stays focused on execution
- [ ] Heavy detail lives in `references/`, `scripts/`, `assets/`, or `evals/` only when justified
- [ ] All linked local files exist
- [ ] `python3 scripts/validate.py <skill-dir>` passes
- [ ] `evals/evals.json` contains realistic task cases when evaluation matters
- [ ] Candidate vs baseline comparison was recorded for meaningful changes
- [ ] Runtime-specific details are layered on top of the portable core, not baked into it
- [ ] Security review completed for any executable or external-accessing package

## Failure Modes to Avoid

- creating a skill where project docs were enough
- putting the workflow in `description`
- hard-coding one vendor's runtime assumptions into the core package
- bloating `SKILL.md` with large reference dumps
- adding scripts without validating them
- tweaking the description against a few keywords instead of measuring real trigger behavior
- calling a skill complete after linting structure but before prompt evaluation