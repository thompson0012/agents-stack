# Skill Design Patterns

Use these patterns when shaping a portable skill package.

## 1. Progressive Disclosure

Keep the package layered.

| Layer | Purpose | Load cost | What belongs there |
| --- | --- | --- | --- |
| Frontmatter | discovery | always loaded | `name`, `description` |
| `SKILL.md` body | execution guide | loaded on trigger | workflow, contracts, quick decisions |
| `references/` | conditional detail | load only when needed | edge cases, schemas, selection rules |
| `scripts/` | deterministic execution | run without reading source when possible | repeatable code |
| `assets/` | copyable artifacts | read only when needed | templates, starter files |

Rule: if detail is not needed for most uses of the skill, move it out of `SKILL.md`.

## 2. Instruction Fidelity by Fragility

Match specificity to failure cost.

| Fragility | Recommended style | Example |
| --- | --- | --- |
| Low | heuristic guidance | "Choose the lightest tool that preserves the output." |
| Medium | parameterized steps | "Run the validator, then fix reported errors before evaluation." |
| High | exact commands or ordered checklists | "Run exactly `python3 scripts/validate.py <skill-dir>` before shipping." |

Over-specifying low-fragility work makes the skill noisy. Under-specifying high-fragility work makes it unreliable.

## 3. Smallest Honest Package

Start at the smallest package that fully tells the truth.

```text
Only discovery + workflow needed         -> SKILL.md
Conditional reference detail needed      -> add references/
Repeated deterministic logic needed      -> add scripts/
Reusable starter artifacts needed        -> add assets/
```

Do not add folders because they look professional. Add them only when they carry their weight.

## 4. Description Pattern

The description decides discovery. Write it as trigger logic, not implementation summary.

Good:
- `Use when creating a reusable skill package or upgrading SKILL.md guidance.`
- `Use when prompts need to route between ambiguous analysis frameworks.`

Bad:
- `Creates folders, writes templates, validates links, and packages zips.`
- `Helpful skill for many tasks.`

## 5. Reference Linking Rule

Link directly from `SKILL.md` to each reference file you expect an agent to use.

Good:
- `references/patterns.md`
- `references/security.md`

Bad:
- `SKILL.md -> references/index.md -> deep/nested/file.md`

If a file matters, link it directly from `SKILL.md`.

## 6. Script Selection Rule

Write a script when at least one of these is true:

- the same logic would be rewritten repeatedly
- exact parsing or validation matters more than prose
- an agent keeps making the same avoidable mistake manually
- the operation is tedious but structurally simple

Do not write a script for judgment-heavy work better expressed as instructions.

## 7. Evaluation Pattern

Use at least three prompt classes:

1. direct trigger
2. ambiguous boundary case
3. noisy or adversarial case

These catch both discovery failures and instruction drift.
