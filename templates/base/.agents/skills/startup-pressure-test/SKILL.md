---
name: startup-pressure-test
description: Use when pressure-testing a startup, launch plan, GTM thesis, or early unit economics with pessimistic but credible assumptions about acquisition, retention, monetization, burn, and runway.
---

# Startup Pressure Test

Use this skill to run a cold-eyed startup viability teardown. The goal is not encouragement. The goal is to discover whether the business survives contact with the market, and what evidence would be required to change the answer.

Adopt the posture of a professional startup pressure tester: calm, skeptical, data-backed, commercially literate, and blunt without being theatrical.

## When This Skill Fits

Route here when the user wants things like:
- a startup sanity check
- a brutal business-model teardown
- a launch or GTM stress test
- a CAC / churn / runway reality check
- an investor-style critique of whether a new startup survives
- a pre-seed viability assessment before building further

Do **not** use this skill for generic market research, standard financial modeling, or product brainstorming without a concrete commercial thesis to test.

## Core Contract

- Treat optimistic claims as unproven until checked.
- Preserve the full commercial arc: **fact check -> archetype pressure branch -> segment choice -> launch simulation -> user behavior -> unit economics -> verdict**.
- Default to a **complete one-pass teardown**. Do not stop at staged checkpoints unless the user explicitly asks to intervene.
- Keep the timeline concrete. Use a short day-based narrative when it sharpens consequences, but do not roleplay for its own sake.
- Prefer median-to-worse assumptions unless the evidence supports better numbers.
- Assume the product can be built, but count build time, founder time, contractor cost, and distribution cost into burn.
- Identify the dominant startup archetype and let its failure mechanics dominate the analysis instead of forcing every company through the same generic funnel.
- Focus on market truth, not product elegance.
- End with a verdict and the smallest next experiment that could overturn it.

## Operating Modes

### Default mode — one-pass teardown
If the user gives a concrete idea, launch plan, or business model, run the full pressure test in one response.

### Optional fork mode — user-requested intervention
Pause only when the user explicitly asks to:
- choose the best early segment before continuing
- compare alternative pricing, channels, or ICPs
- intervene after seeing the first simulation outcome
- rerun the model with revised assumptions

If the user does not ask to intervene, do not invent pauses.

## Intake

If the user has not described the startup yet, open with a concise prompt such as:

> Describe the startup in one paragraph: who the customer is, what the product does, how you expect to acquire users, how you expect to make money, and how much runway you have.

If the user already supplied the idea, do not ask them to repeat it.

## Stage 1 — Fact-Check Gate

Before simulating, extract the factual claims that could meaningfully change the conclusion.

Typical claims to check:
- market size or growth
- whether competitors already exist
- channel access assumptions
- pricing norms
- buyer willingness to pay
- ad-cost assumptions
- regulatory constraints
- sales-cycle assumptions

Use available search tools to verify the highest-impact claims quickly.

### Fact-check process
1. List the concrete factual claims.
2. Verify the highest-impact claims with source-backed search.
3. Separate **verified facts**, **disputed claims**, and **unverified assumptions**.
4. Call out what appears wrong, overstated, outdated, or too weakly evidenced.
5. If a disputed claim cannot be resolved quickly, carry it into the model as an explicit assumption.
6. If interaction is available and the claim matters materially, ask for correction or confirmation.
7. Do not quietly rely on fantasy inputs.

## Stage 2 — Commercial Assumption Map

State what must be true for the startup to work.

Always assess:
- problem intensity
- switching friction
- willingness to pay
- acquisition path realism
- retention risk
- implementation burden on the buyer
- founder execution burden
- sales-cycle or trust barrier

Use plain language. Examples:
- "Pain exists, but willingness to pay is still unproven."
- "This looks like a feature people might try, not a workflow they will pay to keep."
- "The hidden problem is not product demand, but distribution cost."

## Stage 3 — Archetype Detection and Dominant Failure Mechanics

Before ranking segments or simulating launch, identify which startup archetype most strongly determines failure.

Common archetypes:
- **B2B long-sales-cycle** — enterprise, compliance, workflow, procurement, or multi-stakeholder deals
- **Consumer subscription** — habit-dependent products with low price points and high curiosity traffic
- **Marketplace** — two-sided or multi-sided liquidity businesses
- **Regulated or trust-gated startup** — healthcare, fintech, insurance, legal, education, or anything that depends on approval, compliance, or deep buyer trust
- **Usage-based API business** — infrastructure, developer tooling, or embedded workflow products that monetize through volume, throughput, or calls instead of seats
- **Services disguised as software** — products whose onboarding, delivery, or success depends on hidden manual labor
- **Low-ticket ecommerce** — consumer products where gross margin, repeat purchase, logistics, and paid acquisition dominate
- **Creator or media business** — audience-driven businesses that monetize attention through subscriptions, sponsorships, affiliates, or community
- **Developer tool with open-source competition** — devtools where free substitutes or incumbent workflows create monetization drag
- **Fallback generic software / service** — only when none of the above clearly dominates

### Archetype rules

#### B2B long-sales-cycle
Make these questions dominate the model:
- How long is the path from first call to paid contract?
- How many stakeholders, pilots, security reviews, or procurement steps stand between interest and revenue?
- Does founder-led sales become the real bottleneck before product learning catches up?
- How much runway is consumed before enough closed-loop customer evidence exists?

#### Consumer subscription
Make these questions dominate the model:
- Is the user problem frequent enough to become a habit rather than a brief curiosity?
- Does willingness to pay survive once the novelty fades?
- Does churn erase acquired users before CAC payback works?
- Is growth dependent on cheap attention that rarely compounds into retention?

#### Marketplace
Make these questions dominate the model:
- Which side is harder to attract first, and what happens if the other side arrives before liquidity exists?
- What level of density is required before the marketplace feels alive?
- How expensive is trust, vetting, fulfillment, support, or dispute resolution?
- Does the take rate support the operating burden before liquidity is real?

#### Regulated or trust-gated startup
Make these questions dominate the model:
- What must be approved, reviewed, or proven before real usage can occur?
- How much time and cash disappear into compliance, legal review, implementation, and trust-building?
- Can the buyer act quickly, or does the process itself destroy the startup timeline?
- Does the product need evidence, accreditation, or integration depth before anyone meaningful will adopt it?

If more than one archetype fits, choose the dominant one and name the secondary drag explicitly. The dominant branch sets the main simulation logic; the secondary drag is the adjacent mechanic most likely to break the business if the dominant branch does not kill it first.

#### Usage-based API business
Make these questions dominate the model:
- Is integration effort too high relative to the time-to-value the buyer gets?
- Is usage concentrated in a few customers, creating dangerous revenue concentration?
- Do unit economics weaken when heavy users push compute or support cost up faster than pricing?
- Is expansion real, or is the model just hoping developers will scale usage later?

#### Services disguised as software
Make these questions dominate the model:
- How much delivery labor hides behind onboarding, configuration, review, or customer success?
- Is the company pretending to have software margins while actually staffing an agency-like process?
- How quickly does founder or specialist bandwidth become the growth bottleneck?
- Would removing the human layer cause customer value to collapse?

#### Low-ticket ecommerce
Make these questions dominate the model:
- Do gross margins survive shipping, returns, discounts, and creator seeding?
- Is repeat purchase strong enough to rescue paid acquisition?
- Does paid social become an addiction the business cannot economically sustain?
- How much working capital is trapped in inventory before retention is proven?

#### Creator or media business
Make these questions dominate the model:
- Is there enough audience trust to convert attention into paid revenue?
- Does the business depend too heavily on one creator, voice, or publishing cadence?
- Are sponsorship and subscription revenues durable or highly volatile?
- Does the audience want content, or do they want a product the business does not actually own?

#### Developer tool with open-source competition
Make these questions dominate the model:
- Why would teams pay when open-source or incumbent workflows already solve enough of the problem?
- Is adoption broad but monetization weak because developers love the tool more than their budget owner does?
- How strong is workflow lock-in against switching from the status quo?
- Does support, self-hosting complexity, or enterprise hardening eat the margin story?

### Secondary-drag rules

When two archetypes overlap, do not average them into generic startup mush. Use this order:
1. Name the **dominant branch** — the archetype most likely to kill the business first.
2. Name the **secondary drag** — the next failure mechanic that becomes decisive if the dominant branch is somehow survived.
3. Let both appear in the verdict, economics, and next experiment.

Examples:
- marketplace + regulated -> liquidity is usually dominant, trust/compliance is secondary drag
- B2B long-sales + regulated -> buying cycle may be dominant, compliance burden may be the secondary drag
- creator/media + consumer subscription -> audience concentration may dominate, churn may be the secondary drag
- services disguised as software + B2B -> manual delivery burden may dominate, long sales cycle may be the secondary drag

## Stage 4 — Segment Ranking

Rank **3-5 plausible early customer segments**.

For each segment, assess:
- job to be done
- pain level
- current workaround
- urgency
- willingness to pay
- acquisition difficulty
- switching friction
- likely objection
- short verdict

If the user did not specify an exact beachhead, choose the best early segment yourself and explain why the others are worse.

If the user explicitly asks to choose the segment before continuing, pause here and offer:
- A / B / C segment options
- an open-text alternative

Otherwise continue directly into the simulation.

## Stage 5 — Launch Simulation

Simulate the first realistic launch window using pessimistic but defensible funnel math.

Default coverage:
- realistic build cost to reach MVP
- cash remaining at launch
- monthly burn
- runway at launch
- one plausible acquisition attempt
- impressions, clicks, visits, signups, activations, and early retained users

### Default benchmark ranges
Use current source-backed benchmarks when available. If not, default to conservative ranges like these:

| Area | Default range |
| --- | --- |
| Cold-start CTR | `0.5% - 2%` |
| Visit -> signup | `1% - 3%` |
| Free -> paid | `0.5% - 2%` |
| Early monthly churn | `10% - 20%` |
| Paid CAC | uncomfortable, localized, and explicitly justified |

### CAC guidance
State geography and currency clearly. Localize by business type:
- low-ticket B2C: tens to low hundreds of local currency per acquired user
- prosumer / niche SaaS: high tens to several hundreds
- SMB B2B: high hundreds to low thousands
- enterprise pilot sales: thousands to tens of thousands

If you lack a reliable benchmark, say so and choose a conservative number in a credible range.

Do not inflate traction to protect the founder's feelings.

## Stage 6 — User Behavior and Retention Stress

Narrate what the earliest users actually do, then translate that into business meaning.

Typical outcomes:
- curiosity click, then no return
- brief exploration with no emotional reaction
- activation blocked by a workflow mismatch
- value seen, but not enough to justify price
- retention too weak to support paid acquisition

Then state:
- activation quality
- retention rate
- paid conversion rate
- what this implies about product-market fit

Do not confuse usage with viability.

## Stage 7 — Unit Economics and Runway

Maintain a simple operating ledger.

Always track:
- initial funding
- cash balance
- monthly burn
- runway
- MRR once revenue exists
- morale as `High / Strained / Fragile`
- market credibility as `Unknown / Improving / Weak / Damaged`

Use these rules:
- `net burn = operating cost + acquisition spend - recurring revenue`
- `runway = cash balance / net burn`
- if revenue is too small to matter, say so directly
- if net burn improves, verify whether demand is real before treating that as success

If the founder used paid acquisition, show why weak conversion causes CAC to crush the model.

## Stage 8 — Verdict and Next Experiment

Every completed run must end with a verdict.

Allowed verdicts:
- **Proceed, but narrowly**
- **Narrow and retest**
- **Not yet a business**
- **Runway crisis**
- **Structurally broken economics**

Then state:
- the main reason the business breaks
- the strongest remaining reason it might still work
- what evidence would change your mind
- the smallest next experiment that would generate that evidence

Prefer concrete next experiments such as:
- pre-sell before building further
- ask for deposits, not compliments
- recruit the first 10 users manually
- narrow the ICP before writing more code
- test one acquisition channel with real spend and real conversion tracking

Do not end with motivation. End with the verdict and next experiment.

## Required Output Contract

Use this structure unless the user asks for a shorter answer:

```text
[Verdict]
- one-line judgment

[Business in One Sentence]
- what the company does, who pays, and why they might buy

[What Must Be True]
- the core assumptions the business depends on

[Dominant Pressure Branch]
- the startup archetype that governs failure risk and the mechanics it introduces

[Secondary Drag]
- the secondary failure mechanic if another archetype materially compounds the risk; say `none` when not needed

[Fact-Checked Claims vs Assumptions]
- verified facts
- disputed claims
- bracketed assumptions
- sources used

[Best Early Segment]
- ranked segment choice and why it wins

[Launch Simulation]
- build cost
- cash balance
- burn
- runway
- funnel math

[Behavior and Retention Stress]
- what early users actually do
- retention / conversion implications

[Unit Economics Snapshot]
- CAC, conversion, churn, MRR, runway, and economic breakpoints

[180-Day Outcome]
- what the business looks like after realistic market contact

[What Would Change My Mind]
- the evidence required to overturn the verdict

[Next Experiment]
- the smallest concrete test worth running next
```

## Optional Intervention Contract

If the user explicitly asks to intervene midstream, pause only at a real commercial fork and offer:
- A / B / C options
- an open-text alternative
- expected time cost
- cash cost
- downside risk
- rough success probability

Then update the ledger based on the chosen move.

## Response Style

- Write in direct, plain English.
- Be cold-eyed, not theatrical.
- Use numbers whenever possible.
- Explain **why** the business fails or survives.
- Prefer sharp sentences over motivational paragraphs.
- Narrow claims when evidence is weak.

## Common Failure Modes

- treating demand as willingness to pay
- using generous benchmark assumptions without evidence
- stopping at segmentation instead of giving a full verdict
- confusing product engagement with business viability
- ignoring founder time and build cost in burn
- using one generic stress model when the startup archetype clearly changes the real failure mechanism
- failing to name the secondary drag when overlapping archetypes materially compound risk
- hiding uncertainty instead of bracketing assumptions
- giving strategy theater instead of a commercial conclusion

## References

- Add trigger and behavior examples to `evals/evals.json` and `evals/trigger-evals.json`.
- Use current source-backed benchmarks when available; otherwise state the assumption band clearly.

## Final Checklist

- [ ] Highest-impact factual claims were checked or explicitly bracketed
- [ ] Best early segment was chosen or compared
- [ ] Dominant archetype was identified and the simulation followed it
- [ ] Secondary drag was named when overlapping archetypes mattered
- [ ] Launch math is numerical, not hand-wavy
- [ ] Retention and monetization failure modes are explicit
- [ ] Cash, burn, and runway are visible
- [ ] The answer ends with a verdict and next experiment
- [ ] The skill paused only if the user explicitly asked to intervene
