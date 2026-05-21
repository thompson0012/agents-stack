---
name: reasoning
description: Integrated 5-phase reasoning workflow: calibrate state, frame the problem, analyze with lenses, recommend with evidence, verify before acting.
---

# Reasoning

Integrated 5-phase reasoning workflow. Use this when a request needs any combination of state calibration, problem framing, multi-lens analysis, structured advisory, or verification.

This replaces the separate `thinking-ground`, `problem-definition`, `dynamic-problem-solving`, `domain-expert-consultation`, and `self-cognitive` skills. Run only the phases the situation needs; skip the rest.

This is a nested child under `using-reasoning`; its path is `using-reasoning/reasoning/`.

## Core Contract

- Run phases sequentially. Skip any phase the situation does not need.
- Each phase is optional. Enter at the correct phase for the situation.
- Hand off cleanly between phases — output of one is input to the next.
- If a previous phase is still needed, do not jump ahead.
- When the full workflow is done, return the complete output with all relevant phases.

## Phase Selection

| If the situation is... | Start at |
|---|---|
| Emotionally charged, looping, defending an answer | Phase 0 — Calibrate |
| Vague, no clear problem statement, solution-contaminated | Phase 1 — Frame |
| Clear problem, needs rigorous analysis | Phase 2 — Analyze |
| Needs structured recommendation or advisory memo | Phase 3 — Recommend |
| Post-decision, needs verification or pattern extraction | Phase 4 — Verify |
| Just need to separate facts from assumptions before acting | Phase 0 → Phase 4 (skip 1-3) |

---

### Phase 0: Calibrate

Improve reasoning quality before analysis. Use when attachment, urgency, looping, or performative analysis is distorting judgment.

**State Scan** — identify the active distortion using observable signals:
- **Defended**: same conclusion repeated despite counterevidence; objections explained away; morally loaded language
- **Anxious**: urgency exceeds the real deadline; catastrophic language; reversible choices treated as irreversible
- **Performing**: elaborate language without clear next action; complexity grows without understanding
- **Open enough to proceed**: can state counter-case; new evidence changes answer; uncertainty without panic

**Correction protocols** — apply the matching protocol:
- Defended → **Assumption Strip**: name the protected answer; ask "what would have to be true for the opposite to be correct?"
- Anxious → **Deceleration**: name feared outcome precisely; separate real deadline from emotional pressure; classify as reversible/irreversible
- Performing → **Simplicity Test**: restate in plain language; remove decorative depth; force one concrete next step
- Open → proceed to Phase 1 or 2

**Output**: calibrated state label + what changed + next phase

---

### Phase 1: Frame

Turn an unclear situation into a single, solution-neutral problem statement.

**Phase 0 — Capture situation as lived**: Separate observations, interpretations, and attempted fixes.

**Phase 1 — Symptom vs root cause**: 5-Why drill from visible symptom. Branch on multiple plausible causes. Test each candidate: "If solved, does original discomfort disappear?"

**Phase 2 — Reframe five ways**:
1. Flip the subject
2. Zoom out (system view)
3. Zoom in (one component)
4. Flip the assumption (wrong goal)
5. Stakeholder swap

**Phase 3 — Map boundaries**: in scope / out of scope / real constraints / perceived constraints

**Phase 4 — Stakeholder reality check**: each stakeholder's version of the problem + mirror-imaging check

**Phase 5 — Synthesize**: `[SUBJECT] cannot [BEHAVIOR] because [ROOT CAUSE], which leads to [CONSEQUENCE], despite [ATTEMPTED APPROACH].`

**Output**: one problem statement + boundaries + handoff to Phase 2

---

### Phase 2: Analyze

Analyze a clearly defined problem through deliberately chosen lenses. End with tradeoffs and a concrete next action.

**Lens selection** — choose 2-4 from the lens library (`references/lens-library.md`):
- Economics lens: incentives, game theory, market structure
- Systems lens: feedback loops, delays, leverage points
- Psychology lens: cognitive biases, motivation, perception
- Engineering lens: tradeoffs, constraints, composability
- Strategy lens: positioning, moats, optionality
- Organizational lens: power, alignment, coordination costs
- Decision lens: framing effects, status quo bias, escalation
- [14 total — see lens library]

**Analysis**: apply each lens to the problem. Record:
- What each lens reveals
- Where lenses agree and disagree
- What is hidden from each lens

**Lens collision protocol**: when lenses produce conflicting results:
1. Check which lens's assumptions hold in this context
2. Check if the conflict reveals a hidden tradeoff
3. If unresolvable, escalate to tradeoff assessment

**Output**: per-lens findings + collision summary + recommendation direction

---

### Phase 3: Recommend

Produce a structured recommendation, tradeoff evaluation, or decision memo. Use when the problem is clear and the need is advisory.

**Evidence hierarchy**: label every claim as:
- **Direct evidence**: observed, measured, documented
- **Strong inference**: supported by converging evidence
- **Weak inference**: plausible but unsupported
- **Speculation**: no supporting evidence

**Recommendation structure**:
1. Summary recommendation (one sentence)
2. Options considered (2-5, each with tradeoffs)
3. Chosen option + rationale anchored to evidence
4. Unresolved tradeoffs and their impact
5. Next steps and who should act
6. Conditions that would change the recommendation

**Self-check**: could an honest person with the same evidence reach a different conclusion? If yes, the recommendation is premature.

**Output**: decision memo with options, recommendation, evidence, and next steps

---

### Phase 4: Verify

Post-execution verification, retrospective, or reusable pattern extraction.

**Preflight verification** (before acting on the recommendation):
- Separate facts from assumptions
- Confidence calibration: low / medium / high + evidence
- Disconfirming pass: "what evidence is missing that would change the conclusion?"
- Risks and failure modes

**Postflight retrospective** (after action):
- What changed in system understanding
- Process: what to repeat, stop, or tighten
- Prompting/coordination: what would improve future delegation

**Pattern extraction** (optional — when reusable knowledge surfaced):
- One concrete, reusable rule or guardrail
- Who should adopt it and under what conditions
- Suggested format: skill patch, checklist, or decision rule

**Output**: verification statement + optional reusable pattern + confidence

---

## Output Format

Return a consolidated response with sections for each executed phase:

### Phases Executed
- [list which phases ran: 0-calibrate, 1-frame, 2-analyze, 3-recommend, 4-verify]

### [Phase 0 Output — if used]
State: [defended/anxious/performing/open]
Correction: [protocol applied + result]

### [Phase 1 Output — if used]
Problem statement: [one sentence]
Boundaries: [in scope / out of scope]

### [Phase 2 Output — if used]
Lenses used: [...]
Findings: [per lens]
Collision: [where lenses agree/disagree]

### [Phase 3 Output — if used]
Recommendation: [one sentence]
Options: [2-5 with tradeoffs]
Evidence: [hierarchy-labeled]

### [Phase 4 Output — if used]
Verification: [facts vs assumptions, confidence]
Lessons: [technical / process / coordination]
Pattern: [optional — reusable rule or guardrail]

---

## References

- `references/lens-library.md` — 14 analytical lenses with use cases
- `references/bias-inventory.md` — cognitive bias reference
- `references/artifacts.json` — optional structured artifact schema
- `assets/quick-invoke-template.md` — quick-start template
- `assets/worked-example.md` — full worked example

## Failure Modes to Avoid

- Running Phase 2 (Analyze) before Phase 1 (Frame) when the problem is vague — solving the wrong problem is still failure
- Running Phase 3 (Recommend) before Phase 2 (Analyze) — recommendations without analysis are opinions
- Running Phase 0 (Calibrate) unnecessarily — don't pathologize normal reasoning
- Confusing Phase 4 (Verify) with Phase 0 (Calibrate) — verify is post-decision, calibrate is pre-analysis
- Jumping to Phase 3 or 4 when Phase 1 has not been done — premature closure is the most common failure mode
