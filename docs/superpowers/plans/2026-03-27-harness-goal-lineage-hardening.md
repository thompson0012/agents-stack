# Harness Goal-Lineage Hardening Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make template live docs inert, add a persistent roadmap/goal-lineage contract, and keep phased work anchored to the original objective across compaction, goal changes, and worktree resumes.

**Architecture:** Introduce `roadmap.md` as the authoritative phase contract. `current-focus.md` stays a short session summary; `progress.md` records state and verification; `runtime.md` records mode, baton, and entry criteria; `roadmap.md` records source goal, plan goal, phase goals, goal changes, and resume rules. The harness skill rehydrates from those artifacts before each phase and treats goal updates as explicit retirement plus replacement. Template live docs remain neutral scaffolds with no seeded prose.

**Tech Stack:** Markdown skill packages, live-doc templates, Python audit/tests, existing `create-skill` / `create-router-skill` validators, repository continuity docs.

---

## Chunk 1: Template scaffolds and roadmap artifact

### Task 1: Make template live docs truly inert

**Files:**
- Modify: `templates/base/docs/live/current-focus.md`
- Modify: `templates/base/docs/live/progress.md`
- Modify: `templates/base/docs/live/runtime.md`
- Modify: `templates/base/docs/live/todo.md`
- Modify: `templates/base/docs/live/qa.md`
- Create: `templates/base/docs/live/roadmap.md`
- Modify: `templates/base/AGENTS.md`
- Modify: `templates/base/docs/reference/architecture.md`
- Modify: `templates/base/docs/reference/codemap.md`
- Modify: `templates/base/docs/reference/memory.md`

- [ ] **Step 1: Write failing template-shape tests**
  - Add `scripts/tests/test_goal_lineage_templates.py` with assertions that the template live docs contain only headings, labels, or table scaffolds and no sample roadmap prose.
  - Include one check that `templates/base/docs/live/roadmap.md` exists and exposes source goal, plan goal, current phase goal, retired goals, worktree, and phase ledger fields.

- [ ] **Step 2: Reduce each live doc to a neutral scaffold**
  - Strip explanatory paragraphs from the template live docs.
  - Keep only the minimal headings and empty labels needed for downstream use.
  - Add the new roadmap scaffold with explicit fields for source goal, plan goal, current phase goal, retired goals, worktree ID, phase status, and exit criteria.

- [ ] **Step 3: Update template guidance and reference docs**
  - Update `templates/base/AGENTS.md` so the read order includes `docs/live/roadmap.md` when work spans compaction or phase handoff.
  - Update the template reference docs to state that roadmap continuity, not chat memory, is the authoritative carrier for phased work.

- [ ] **Step 4: Run the narrow validation first**
  - Run: `python3 -m pytest scripts/tests/test_goal_lineage_templates.py -q`
  - Expected: fail before the scaffold changes, then pass after the files are cleaned up.

### Task 2: Keep the current session recoverable

**Files:**
- Create: `docs/live/roadmap.md`
- Modify: `docs/live/current-focus.md`
- Modify: `docs/live/progress.md`
- Modify: `docs/live/todo.md`
- Modify: `AGENTS.md`

- [ ] **Step 1: Write the session roadmap first**
  - Capture the current source goal and the narrower plan goal for this work.
  - Record the phase ledger so compaction can resume without losing the original objective.

- [ ] **Step 2: Point the short summaries at the roadmap**
  - Keep `current-focus.md` brief and make it point to the roadmap instead of carrying the whole plan in prose.
  - Update `progress.md` and `todo.md` so the next action is obvious after a reset.

- [ ] **Step 3: Update the repo entry order if needed**
  - Make sure the repository-level read order includes the new roadmap when controlled multi-session work is in play.

- [ ] **Step 4: Check the live-doc diff**
  - Run: `git diff --check`
  - Expected: no whitespace or patch-format problems.

---

## Chunk 2: Harness control and routing

### Task 3: Preserve goal lineage in the harness skill

**Files:**
- Modify: `templates/base/.agents/skills/software-delivery/harness-design/SKILL.md`
- Modify: `templates/base/.agents/skills/software-delivery/SKILL.md`
- Modify: `templates/base/.agents/skills/software-delivery/evals/evals.json`
- Modify: `templates/base/.agents/skills/software-delivery/evals/trigger-evals.json`
- Modify: `templates/base/.agents/skills/software-delivery/references/children.json` if the route wording needs to mention roadmap continuity explicitly
- Modify: `templates/base/docs/reference/architecture.md`
- Modify: `templates/base/docs/reference/codemap.md`
- Modify: `templates/base/docs/reference/memory.md`

- [ ] **Step 1: Write failing tests for the control language**
  - Add or extend `scripts/tests/test_harness_goal_lineage.py` so it asserts the harness skill mentions source goal, plan goal, current phase goal, retired goal history, worktree-aware lineage, and the pre-phase rehydration checkpoint.
  - Add routing coverage for prompts that mention roadmap execution, compaction, and “don’t lose the original goal.”

- [ ] **Step 2: Update the harness skill contract**
  - Require the same goal lineage to survive every phase.
  - Require explicit goal retirement and replacement when the user changes direction.
  - Require rehydration from roadmap/current-focus/progress before phase 1 and after every compaction.
  - Make the failure case honest: if the roadmap cannot be rehydrated, stop instead of guessing.

- [ ] **Step 3: Update the stable repo references**
  - Add the new roadmap artifact and goal-lineage invariants to the architecture/codemap/memory docs.
  - Keep the separation between short session summaries and the authoritative roadmap contract clear.

- [ ] **Step 4: Re-run validation**
  - Run:
    - `python3 templates/base/.agents/skills/create-skill/scripts/validate.py templates/base/.agents/skills/software-delivery/harness-design --strict`
    - `python3 templates/base/.agents/skills/create-router-skill/scripts/validate_router.py templates/base/.agents/skills/software-delivery --strict`
    - `python3 -m pytest scripts/tests/test_harness_goal_lineage.py -q`
  - Expected: all pass after the edits.

### Task 4: Add router/eval coverage for roadmap continuity

**Files:**
- Modify: `templates/base/.agents/skills/software-delivery/evals/evals.json`
- Modify: `templates/base/.agents/skills/software-delivery/evals/trigger-evals.json`

- [ ] **Step 1: Add direct coverage for roadmap drift prompts**
  - Include a prompt that says the agent loses the original goal after roadmap execution and compaction.
  - Keep the expected route on `software-delivery/harness-design`.

- [ ] **Step 2: Add trigger coverage for compaction-resume language**
  - Include a trigger that mentions preserving source goals across phases and worktree resumes.
  - Keep the route honest and narrow.

- [ ] **Step 3: Re-run the router validation**
  - Run: `python3 templates/base/.agents/skills/create-router-skill/scripts/validate_router.py templates/base/.agents/skills/software-delivery --strict`
  - Expected: pass with the new eval coverage.

---

## Chunk 3: Enforcement and close-out

### Task 5: Guard against seeded template content

**Files:**
- Modify: `scripts/audit_base_template_skills.py`
- Modify: `scripts/tests/test_audit_base_template_skills.py`
- Modify or create: `scripts/tests/test_goal_lineage_templates.py`

- [ ] **Step 1: Extend the audit to scan the new scaffolds**
  - Reject template live docs that contain sample roadmap prose instead of inert placeholders.
  - Keep the audit portable and path-based.

- [ ] **Step 2: Add a synthetic failure test**
  - Prove the audit rejects seeded template content and accepts the neutral scaffold.
  - Keep the test fixtures small and explicit.

- [ ] **Step 3: Run the full safety sweep**
  - Run:
    - `python3 scripts/audit_base_template_skills.py`
    - `python3 -m pytest scripts/tests -q`
    - `git diff --check`
  - Expected: all pass.

### Task 6: Refresh continuity docs and finish

**Files:**
- Modify: `docs/live/current-focus.md`
- Modify: `docs/live/progress.md`
- Modify: `docs/live/todo.md`

- [ ] **Step 1: Record the plan state clearly**
  - Update the live docs with the current objective, blockers, touched files, and next action.

- [ ] **Step 2: Keep the next handoff explicit**
  - Point the next owner at the saved plan and the roadmap artifact.

- [ ] **Step 3: Confirm no extra reference-doc update is needed beyond the files above**
  - Only add `docs/reference/*` changes if the implementation actually changes a durable repo truth.
