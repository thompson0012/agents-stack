# Clean Philosophy Audit: `.agents/skills/`

**Date:** 2026-05-28
**Scope:** 16 top-level skills (5 routers, 11 leaves) + 22 sub-skills
**Method:** Clean Philosophy cross-level audit — Code, Module, System, Process, API, UI

---

## Part 1 — Individual Skill Scanning

### 1.1 Green (Healthy) — lean, focused, justified

| Skill | Lines | Bundles | Verdict |
|-------|-------|---------|---------|
| **agent-handoff** | 88 | 1 ref + 2 evals | Clean. Minimal, focused, single job. |
| **backend-qa** | 36 | 4 refs | ★ Exemplary. Router-style: thin SKILL.md, heavy lifting in references. |
| **clean-philosophy** | 103 | 3 refs | Clean. Right granularity. |
| **greenfield-product** (router) | 32 | — | Clean. Minimal routing body. |
| **meta-prompting** | 83 | — | Clean. Tight scope, no bloat. |
| **skill-authoring** (router) | 31 | — | Clean. Router stays out of child work. |
| **using-reasoning** (router) | 93 | 2 evals + 1 script | Clean. |
| **market-opportunity-scout** | 90 | — | Clean. |
| **meta-methodology-extraction** | 129 | 2 evals | Clean. |
| **using-agents-stack/release** | 91 | — | Clean. |
| **using-agents-stack/reflect** | 71 | — | Clean. |
| **skill-authoring/create-agents** | 65 | 1 asset + 1 ref + 2 evals | Clean. |
| **using-agents-stack/spec** | 108 | — | Clean. |
| **greenfield-product/spec-pipeline** | 110 | — | Clean. |

**Sub-skills of frontend-design:**
| **design-compounder** | 121 | — | Clean. |

### 1.2 Yellow (Needs Trimming) — too large, but justified domain

| Skill | Lines | Bundles | Issue |
|-------|-------|---------|-------|
| **adversarial-qa** | 171 | 1 asset + 5 refs | Size is borderline. 5 attack references are well-justified. OK. |
| **frontend-qa** | 184 | 3 refs + 2 evals | Borderline. 3 references (framework, playbook, reporting) are justified. |
| **brand-identity-extractor** | 221 | 1 asset + 2 refs + 2 evals | Description is 300+ chars with inline trigger examples. Move triggers to reference. |
| **universal-learning-architect** | 228 | — | Frontmatter has `metadata.version`, `category`, `tags` — not standard. Description doesn't start with "Use when". |
| **using-agents-stack/plan** | 188 | — | Borderline. |
| **using-agents-stack/tasks** | 139 | — | OK. |
| **using-agents-stack/analyze** | 149 | — | OK. |
| **using-agents-stack/prune-review** | 149 | — | OK. |
| **using-reasoning/reasoning** | 202 | 2 assets + 3 refs | Large but justified for 5-phase reasoning workflow. |
| **using-reasoning/reality-check** | 165 | — | OK. |
| **using-reasoning/strategic-foresight** | 226 | — | Large. Could extract reference tables. |
| **frontend-design/design-context-scout** | 290 | — | Large but domain justifies it? Borderline. |
| **frontend-design/design-proposer** | 276 | — | Borderline. |
| **skill-authoring/create-skill** | 236 | 7 assets + 8 refs + 4 scripts | Most over-bundled skill in the repo. 19 support files for a skill-creator. Scripts are particularly speculative — does `package_skill.py` or `scaffold.py` get used regularly? |

### 1.3 Red (Needs Intervention) — overgrown, over-bundled, or poorly structured

| Skill | Lines | Bundles | Issues |
|-------|-------|---------|--------|
| **using-agents-stack/implement** | 427 | — | ★ Worst offender. Contains inline TASK-01, TASK-02 example tasks that should be in a reference template. The RED-GREEN-REFACTOR cycle has 7 phases, most with 10+ lines of prose. At minimum: extract example tasks → template reference (-100L), consolidate phase prose (-80L). Target: ~250L. |
| **greenfield-product/startup-pressure-test** | 425 | 2 evals | ★ Second worst. Has 9 archetype rules (B2B, Consumer, Marketplace, Regulated, API, Services, Ecommerce, Creator, DevTool) inlined — each 30-50 lines. Extract these to a reference file. 9 × 40L = 360L moved out. Target: ~150L. |
| **frontend-design/design-reviewer** | 381 | — | Too large. 381 lines for a review skill. Extract criteria tables to reference. |
| **frontend-design/design-builder** | 357 | — | Too large. Implementation Playbook belongs in a reference. |
| **frontend-design/design-prototype-lab** | 342 | 3 refs | Too large. The 3 reference files (templates) should be enough — trim the prose. |
| **prompt-augmentation** | 237 | **16 refs** | 16 reference files for image/video terminology (camera-movement.md, color-mood.md, film-grammar-editing.md, optics-camera.md, etc.) are excessive for a "prompt enrichment" skill. These belong in a domain-specific image-prompt skill, not here. Clean: move 12 of 16 refs out, keep only 4 cross-cutting ones. |

---

## Part 2 — Overall Repo Scan: Grouping & Consolidation

### 2.1 High-Confidence Grouping Candidates

#### Group A: `qa` router (3 skills)

```
adversarial-qa/   (171L)  ← red-team, break system
frontend-qa/      (184L)  ← browser-based frontend testing
backend-qa/       (36L)   ← API, job, queue, auth testing
```

**Rationale:** All three answer "is this system reliable?" from different angles. The backend-qa is already a thin router-style skill (36L). Grouping them under a `qa` router makes discovery easier and cleanly divides adversarial vs functional vs backend testing.

**Recommendation:** Create `qa/` router with 3 children. **Priority: Medium.**

#### Group B: `prompt-engineering` router (2 skills)

```
meta-prompting/           (83L)   ← prompt architecture, system prompts
prompt-augmentation/      (237L + 16 refs) ← enriching sparse prompts
```

**Rationale:** Both deal with prompt creation. Currently feel like they were split and grew independently. The boundaries are fuzzy — when is "enriching" complete and "architecture" begins?

**Recommendation:** Create `prompt-engineering/` router with 2 children. Use this as an opportunity to trim prompt-augmentation's 16 refs. **Priority: Medium.**

### 2.2 Medium-Confidence Grouping Candidates

#### Group C: Frontend design sub-skill consolidation

```
frontend-design/ has 6 sub-skills totaling ~1,767L:
  design-context-scout   (290L)
  design-proposer        (276L)
  design-builder         (357L)
  design-reviewer        (381L)
  design-compounder      (121L)
  design-prototype-lab   (342L)
```

**Rationale:** 6 sub-skills for one pipeline is excessive. The pipeline is `context → propose → build → review → compound → prototype-lab`. But a pipeline with 6 stages that each require a separate SKILL.md suggests over-granularity.

**Recommendation:** Consolidate to 3:
- `design-scope` (context-scout + proposer: ~300L target)
- `design-build` (builder + prototype-lab: ~400L target)
- `design-verify` (reviewer + compounder: ~300L target)

**Priority: Low** (would improve navigation but high effort).

#### Group D: `using-agents-stack` sub-skill consolidation

```
using-agents-stack/ has 10 sub-skills:
  prune-review   (149L)
  reflect        (71L)
  + 8 pipeline phases
```

**Rationale:** `prune-review` and `reflect` are both "maintenance" operations that happen outside the main pipeline flow. They could be one `using-agents-stack/maintain` child.

**Recommendation:** Merge `prune-review` + `reflect` → `using-agents-stack/maintain` (~220L total). **Priority: Low.**

### 2.3 Other Observations

| Observation | Detail |
|---|---|
| **Orphan directory** | `.agents/skills/references/` is an empty directory, not a skill. Delete it. |
| **adversarial-qa typo** | Directory is `ADversarial-qa/` (capital A, D). All other skill dirs are lowercase. Inconsistent. |
| **frontend-design children.json** | Is a **list** (array) instead of a dict with `children` key. Inconsistent with all other routers (skill-authoring, greenfield-product, using-reasoning use `{"children": [...]}`). |
| **using-agents-stack children.json** format | Need to verify — may also differ. |
| **implement SKILL.md** frontmatter | Has custom YAML fields `trigger`, `inputs`, `outputs`, `boundaries` not following standard `name`/`description` pattern. |

---

## Part 3 — Clean Philosophy Patterns: What Works and What Doesn't

### 3.1 Best Pattern (★)

**`backend-qa`** (36 lines):
- Thin SKILL.md with clear entry-gate questions
- Heavy content in 4 well-named reference files (core.md, framework.md, playbook.md, reporting.md)
- Follows Clean Code principle: SKILL.md is the interface, references are the implementation
- Passes Negation test: "If I removed backend-qa, would anyone notice?" — yes, they'd lose systematic backend validation guidance

### 3.2 Worst Pattern

**`create-skill`** (236L + 19 support files):
- Violates Level Discipline: has scripts for scaffolding, packaging, validating — but is a skill *about* creating skills, not a build tool
- Violates Useful > Correct: does `package_skill.py` solve a real recurring pain, or is it speculative? If agents don't use it, it's dead code
- Violates Content > Decoration: 7 assets + 8 references + 4 scripts = 19 files for a skill that writes other skills. That's a circular dependency warning sign
- Negation test: most of the scripts/assets would go unnoticed if deleted

### 3.3 Over-bundling Trend

Several skills accumulate reference files past the point of diminishing returns:

| Skill | Support files | Likely unused |
|-------|:------------:|:-------------:|
| prompt-augmentation | 16 refs | ~12 (camera, film grammar, optics, temporal pacing, etc. — niche image-gen domain knowledge, not prompt enrichment) |
| create-skill | 7 assets + 8 refs + 4 scripts | ~3 scripts (package_skill.py, scaffold.py — speculative tooling) |
| brand-identity-extractor | 1 asset + 2 refs + 2 evals | 0 (all justified) |

### 3.4 Router Consistency Issues

Of 5 routers, 3 use `{"children": [...]}` format, 1 uses `[...]` (bare list), and 1 needs verification:

| Router | Format | Consistent? |
|--------|--------|:-----------:|
| skill-authoring | `{"router_name","children":[...]}` | ✅ |
| greenfield-product | `{"router_name","children":[...]}` | ✅ |
| using-reasoning | `{"router_name","children":[...]}` | ✅ |
| frontend-design | `[...]` (bare list) | ❌ |
| using-agents-stack | (unknown) | TBD |

---

## Part 4 — Priority Recommendations

### P0 (Do Now)

| # | Action | Rationale |
|---|--------|-----------|
| 1 | Trim `startup-pressure-test`: extract 9 archetype rules → `references/archetypes.md` | Saves ~360L. Target: 150L. |
| 2 | Trim `implement`: extract TASK-01/TASK-02 examples → `references/task-templates.md` | Saves ~100L. Target: ~300L. |
| 3 | Fix `universal-learning-architect` frontmatter: remove metadata/version/category/tags, rewrite description to start with "Use when" | Standard compliance. |
| 4 | Fix `adversarial-qa` directory name: lowercase → `adversarial-qa/` | Consistency. |

### P1 (This Week)

| # | Action | Rationale |
|---|--------|-----------|
| 5 | Trim `prompt-augmentation`: move 12 domain-specific image/gen refs to a sub-directory or archive | 16 refs is excessive. Keep only 4 cross-cutting ones. |
| 6 | Normalize all router `children.json` to `{"children":[...]}` format | Consistency. Fix `frontend-design`. |
| 7 | Remove empty `.agents/skills/references/` directory | Dead directory. |
| 8 | Trim `create-skill` scripts: remove `package_skill.py`, `scaffold.py` unless used | Speculative tooling. Keep `validate.py` and `validate_router.py`. |
| 9 | Trim `design-reviewer`, `design-builder`, `design-prototype-lab` each to ~250L | Extract tables/reference data. |

### P2 (Next Sprint)

| # | Action | Rationale |
|---|--------|-----------|
| 10 | Create `qa/` router for adversarial-qa + frontend-qa + backend-qa | Better discoverability. |
| 11 | Create `prompt-engineering/` router for meta-prompting + prompt-augmentation | Clearer boundaries. |
| 12 | Consolidate `frontend-design` from 6 sub-skills → 3 | Reduce navigation overhead. |
| 13 | Merge `using-agents-stack/prune-review` + `reflect` → `maintain` | Same purpose (maintenance). |

### P3 (Nice to Have)

| # | Action | Rationale |
|---|--------|-----------|
| 14 | Consolidate `using-reasoning` sub-skills (593L total) into one skill with sections | May reduce granularity. Verify after other trims. |
| 15 | Rename `ADversarial-qa` → `adversarial-qa` | Requires updating all references. |

---

## Part 5 — Metrics Summary

```
Total skills:           16 top-level + 22 sub-skills = 38
Total SKILL.md lines:   ~5,800
Total support files:    ~60 (assets, references, scripts, evals)

Green (healthy):        14 skills
Yellow (needs trim):    10 skills  
Red (needs work):       6 skills

Grouping opportunities: 5 identified (qa, prompt-engineering, design, 
                        maintain, using-reasoning)
```

---

_Generated by clean-philosophy audit: Useful > Correct, Content > Decoration, Negation test on every skill._
