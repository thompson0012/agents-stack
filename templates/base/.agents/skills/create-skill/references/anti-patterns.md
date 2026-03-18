# Skill Anti-Patterns

These mistakes make skills noisy, brittle, or vendor-locked.

## 1. Workflow in the Description

Bad:
- `Use when you need a skill that scaffolds folders, validates YAML, runs zips, and executes tests.`

Why it fails:
- the description should help discovery, not replace the body
- long workflow summaries reduce trigger precision

Fix:
- describe the request, symptom, or task that should load the skill

## 2. Vendor-Locked Core Instructions

Bad:
- making one platform's package shape, URLs, beta headers, or install model the canonical truth

Why it fails:
- the skill becomes obsolete outside that surface
- portability requires a stable core and optional runtime overlays

Fix:
- keep vendor-specific notes in a dedicated portability reference or runtime appendix

## 3. One Skill Solving Three Different Jobs

Bad:
- one package that tries to be a prompt guide, a deployment guide, and a business policy manual

Why it fails:
- discovery becomes fuzzy
- the body bloats because each job needs different instructions

Fix:
- split by repeatable job, not by theme alone

## 4. Giant `SKILL.md`

Bad:
- dumping every example, edge case, and reference note inline

Why it fails:
- expensive to load
- harder to scan
- conditional detail buries the core workflow

Fix:
- move heavy or conditional detail into `references/`

## 5. Scripts Without Validation

Bad:
- adding helper scripts and assuming they work because they are short

Why it fails:
- tiny scripts still fail on paths, permissions, and malformed input

Fix:
- run the script on at least one success case and one failure case

## 6. Empty Ceremony

Bad:
- adding folders, templates, and checklists that no instruction ever uses

Why it fails:
- bigger package, no extra capability

Fix:
- every file should earn its keep

## 7. Evaluation by Vibes

Bad:
- calling the skill done after reading the markdown once

Why it fails:
- you have not tested discovery, ambiguity, or drift

Fix:
- use explicit prompt scenarios and record what failed

## 8. Overfitting to the Eval Keywords

Bad:
- editing the description by stuffing in every missed phrase from a small trigger set

Why it fails:
- the description becomes brittle keyword bait
- it may score better on the tiny eval set while routing worse in real use

Fix:
- generalize from user intent and competing task boundaries, then rerun both positive and negative cases

## 9. Shipping the Workspace by Accident

Bad:
- bundling benchmark output, review logs, temporary runs, or local artifacts into the archive you share

Why it fails:
- the package gets noisy
- stale outputs confuse the next user
- transient data can leak more than intended

Fix:
- keep run artifacts in a sibling workspace and package only the reusable skill files

## 10. Hidden Family With No Router

Bad:
- burying related child skills in nested folders and assuming the runtime will discover or choose them correctly without a router entrypoint

Why it fails:
- nested children can become effectively invisible
- the folder tree cannot explain install behavior, fallbacks, or typed relationships
- agents end up guessing which child to load, or never loading one at all

Fix:
- add a discoverable top-level router skill
- keep child metadata explicit instead of relying on the directory tree alone
- use a router-specific package when the main job is selection and handoff
