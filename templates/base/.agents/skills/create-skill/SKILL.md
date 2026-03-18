---
name: create-skill
description: Use when creating a new reusable skill, upgrading an existing skill package, scaffolding a SKILL.md directory, or rewriting skill guidance into a portable LLM-agnostic format.
---

# Create Skill

Use this skill to create or upgrade a reusable skill package that another agent can discover quickly and apply across runtimes.

Build the portable core first. Add runtime-specific metadata, packaging, or tooling only after the core package works without vendor assumptions.

## Core Contract

- Solve one repeatable job. If the work is project-specific or one-off, put it in repo docs instead.
- Keep the canonical core portable: default to `name` and `description` frontmatter only.
- Put trigger conditions in `description`; put workflow, checklists, and edge cases in the body.
- Keep `SKILL.md` lean. Move heavy or conditional detail into `references/`, deterministic code into `scripts/`, and copyable starter files into `assets/`.
- Validate structure before claiming the package is usable.
- Pressure-test the skill with real prompts before calling it done.

## Entry Gate

Before writing files, answer these five questions:

1. What is the single responsibility of the skill?
2. What concrete task fails, repeats, or degrades without it?
3. What runtime capabilities matter: filesystem, shell, network, package install, archive format, sharing model?
4. What does the user provide, and what should the skill produce?
5. How fragile is the workflow: low, medium, or high?

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
| Validation | run `python3 scripts/validate.py <skill-dir>`; see [validate.py](scripts/validate.py) |
| Evaluation | run at least 3 scenario prompts using [eval-template.md](assets/eval-template.md) |

For deeper guidance, read:

- [patterns](references/patterns.md)
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

### Phase 2 — Choose the Smallest Useful Package

Start with the smallest shape that honestly covers the job.

```text
SKILL.md only                 -> simple, stable workflow
SKILL.md + references/        -> heavy or conditional reference detail
SKILL.md + scripts/           -> repeated deterministic code or fragile execution
SKILL.md + assets/            -> templates, starter files, or reusable output inputs
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
- Add runtime-specific metadata only when the target environment explicitly requires it.

#### Body

Write for fast scanning and reliable execution.

Recommended section order:

1. `# Title`
2. short overview
3. core contract or non-negotiables
4. workflow or phase-by-phase steps
5. references to bundled files when needed
6. final checklist or failure modes

Use the instruction style that matches workflow fragility. See [patterns](references/patterns.md) for the exact decision table.

### Phase 4 — Add Bundled Resources

#### `references/`

Use for information another agent may need to read while working:

- selection rules
- edge cases
- domain schemas
- platform notes
- security checklists

Keep references one hop deep from `SKILL.md`. A direct link like [patterns](references/patterns.md) is good. Nested chains are not.

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

### Phase 5 — Validate the Package

Run:

```bash
python3 scripts/validate.py <skill-dir>
```

Fix every reported error before moving on.

Use `--strict` when you want warnings to fail the run.

### Phase 6 — Evaluate the Skill

Do not stop at structural validation. Test whether the skill is actually discoverable and useful.

Create at least three prompt scenarios using [the evaluation template](assets/eval-template.md):

1. direct match — obvious trigger
2. ambiguous near miss — decide whether the skill should trigger
3. noisy or adversarial request — confirm the skill still routes and behaves correctly

For each scenario, capture:

- should the skill trigger
- what output or behavior should happen
- what failed or drifted
- what minimal change fixed the gap

Patch only the missing instruction, example, or resource. Do not bloat the skill with speculative rules.

### Phase 7 — Runtime-Specific Layering

Only after the portable core is solid, add any target-runtime requirements the deployment surface needs.

Use [portability](references/portability.md) to check:

- whether network is available
- whether packages can be installed
- whether shell or code execution exists
- how sharing or packaging works
- which metadata fields are actually required

The portable core should remain readable even if those runtime overlays are removed.

### Phase 8 — Security Review

Before shipping a skill with scripts or external access, review [security](references/security.md).

At minimum verify:

- no secrets are hardcoded
- no script writes outside intended paths
- no hidden network calls or background fetches exist
- remote content is treated as untrusted input

## Final Checklist

- [ ] The skill solves one repeatable job
- [ ] `name` matches directory name exactly
- [ ] `description` starts with `Use when`
- [ ] `description` explains triggers, not the workflow
- [ ] `SKILL.md` stays focused on execution
- [ ] Heavy detail lives in `references/`, `scripts/`, or `assets/` only when justified
- [ ] All linked local files exist
- [ ] `python3 scripts/validate.py <skill-dir>` passes
- [ ] At least 3 evaluation prompts were written and reviewed
- [ ] Runtime-specific details are layered on top of the portable core, not baked into it
- [ ] Security review completed for any executable or external-accessing package

## Failure Modes to Avoid

- creating a skill where project docs were enough
- putting the workflow in `description`
- hard-coding one vendor's runtime assumptions into the core package
- bloating `SKILL.md` with large reference dumps
- adding scripts without validating them
- calling a skill complete after linting structure but before prompt evaluation