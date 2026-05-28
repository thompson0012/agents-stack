# Scenario Planning Templates

A reference template for strategic foresight — use when a concrete external change or threshold needs scenario planning, such as a launch, pricing move, policy shift, scientific result, cost curve, or market shock, and you want implications, winners and losers, second-order effects, or indicators to watch.

## Core Discipline

- Diagnose the shift; do not paraphrase the announcement.
- Stay concrete. Generic hype and vague futurism are useless.
- Make explicit bets under uncertainty.
- Always include both acceleration paths and failure paths.
- Tie claims to actors, incentives, bottlenecks, and observable indicators.
- Name the human driver when it matters: convenience, status, fear, control, cost, speed, labor savings, or power.
- Answer the user's actual question early; use the framework to sharpen the answer, not bury it.

## Analysis Workflow

### Step 1 — Define the Signal

Identify the real change or, for a hypothetical, the threshold that would make the change real.

Answer these briefly:
- What actually changed, or what specific threshold must be crossed?
- Is this primarily a **capability shift**, **cost shift**, **speed shift**, **interface shift**, **distribution shift**, **regulatory shift**, or **coordination shift**?
- Why now? What technical, economic, behavioral, or regulatory condition unlocked it?
- If this is a cost or hardware shift, what changes in **CapEx vs OpEx**?

Do not describe the product at surface level. State the strategic signal underneath it.

### Step 2 — Identify the Strategic Hinge

Find the assumption that may no longer hold.

Examples:
- "Only large companies can afford this capability."
- "This workflow requires human review at every step."
- "Distribution is the moat."
- "Regulation will move too slowly to matter."

If you cannot name the broken assumption, you have not identified the real story.

### Step 3 — Run Three Scenarios

Always produce three cases unless the user explicitly asks for one:

1. **Base Case** — the change is real, but adoption is bounded.
2. **Upside Case** — the shift compounds faster than consensus expects.
3. **Failure Case** — bottlenecks, regulation, economics, or human behavior prevent escape velocity.

For each scenario, cover:
- 0-12 months
- 1-3 years
- 3-7 years, if the topic warrants it
- A rough likelihood ranking when the evidence is strong enough to support one

State what must be true for each scenario to happen, which constraint or dependency defines it, and what evidence would move it toward or away from the base case. Distinct scenarios must differ by assumptions or constraints, not just by speed.

### Step 4 — War-Game the Actors

Map the likely reactions of the key players, then classify each as a likely **winner**, **loser**, or **pivoter**.

At minimum, consider:
- Users / customers
- Incumbents
- New entrants / challengers
- Infrastructure providers / tool vendors / suppliers
- Regulators / governments
- Labor / professional groups for automation, cost, or workflow shifts

Ask:
- Who moves first, and with what concrete move?
- Who delays, denies, or defends the old model?
- Who benefits quietly even if they are not the headline winner?
- Who looks safe but is actually exposed?
- What countermoves are likely?
- Where do pricing power, margins, distribution control, or bargaining leverage move?

### Step 5 — Trace Higher-Order Effects

Go beyond the direct impact.

- **First-order effects**: immediate operational or market changes
- **Second-order effects**: shifts in behavior, pricing, margins, incentives, regulation, workflows, or market structure
- **Third-order effects**: changes in institutions, culture, labor markets, geopolitics, supply chains, or power concentration that follow clearly from the earlier shifts

If useful, include a short historical rhyme:
- What earlier transition has a similar shape?
- What repeated pattern is showing up again?

Use analogy to clarify, not to force a false equivalence.

### Step 6 — Name Bottlenecks, Risks, and Failure Modes

Do not assume the future arrives cleanly.

Check for:
- Infrastructure, physical, energy, or supply-chain bottlenecks
- Economic friction
- Human trust and adoption barriers
- Regulatory intervention
- Supply constraints
- Security or abuse risks
- Incentive misalignment
- Identity or status resistance from powerful groups

Be explicit about what could kill the thesis, not just slow it down.

### Step 7 — End With Decision Support

Finish with action, not atmosphere.

State:
- What operators, investors, founders, or policymakers should do now, if applicable
- Which indicators move probability toward or away from the base, upside, and failure cases
- End on the indicator list; do not append a fresh conclusion after it

## Output Format

Use this structure by default. If the user asks a narrower question, answer it directly first and then compress or merge sections while preserving the logic.

```text
[Signal]
What changed, and what the real strategic signal is.

[Why This Matters]
The assumption that may stop being true.

[Scenario 1 — Base Case]
Likely path, adoption shape, and consequences.

[Scenario 2 — Upside Case]
What happens if the shift compounds faster than expected.

[Scenario 3 — Failure Case]
What blocks it, stalls it, or reverses it.

[Stakeholder Reactions]
Who wins, loses, or pivots, and how users, incumbents, challengers, infrastructure providers, regulators, and labor groups react.

[Second-Order Effects]
Behavioral, market, or regulatory changes caused by the first wave.

[Third-Order Effects]
Structural shifts in institutions, culture, labor, geopolitics, or power.

[Risks and Bottlenecks]
What could break the thesis or create serious unintended consequences.

[Strategic Takeaway]
The main implication in plain language.

[Indicators to Watch]
Observable, preferably quantifiable signals mapped to base, upside, and failure cases, plus clear falsifiers when they exist. This is the final section.
```

## Quality Bar

- Prefer crisp claims over cloudy prose.
- Explain why each effect follows from incentives, constraints, or behavior.
- Do not hide uncertainty; structure it.
- Do not present all scenarios as equally likely if they are not.
- Keep third-order effects tethered to structural consequences, not sci-fi flourish.
- Front-load the user's direct question when the prompt is narrow, then support it with the framework.
- If the evidence is thin, say what is unknown and what would resolve it.
- Put any closing synthesis in `[Strategic Takeaway]`, then finish on `[Indicators to Watch]`.
- Each major scenario should have at least one indicator that moves probability toward it and one signal that weakens it, when the evidence supports that distinction.
- If the user wants a narrower answer, compress the format but keep the logic.

## Example Triggers

- "OpenAI released X. What does this mean?"
- "War-game the impact of browser agents on SaaS."
- "If humanoid robots fall below $20k, what happens next?"
- "Run scenarios on AI doctors."
- "Who wins and loses if on-device AI gets good enough to replace cloud copilots?"
- "What second-order effects follow from this policy change?"
- "Tabletop exercise: what happens if coding agents become reliable for SMBs?"
