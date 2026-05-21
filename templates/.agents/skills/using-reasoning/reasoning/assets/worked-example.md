# Worked Example: B2B SaaS Retention Decision

## Problem Restatement

A B2B SaaS company must decide whether to allocate its next budget cycle to product feature development or onboarding/support process improvement, as customer retention has declined for three consecutive quarters and internal stakeholders are deadlocked.

## Entry Gate Verification

**Gate 1 — Problem quality:** The problem restates in one sentence. There is a specific decision (budget allocation), a measurable symptom (three quarters of retention decline), and a named conflict (CEO vs VP Customer Success). Pass.

**Gate 2 — Cynefin classification:** Complicated. Retention decline has identifiable causes; expert analysis can distinguish root contributions from symptoms. The problem is not complex (causes are not emergent) or chaotic (the business is not in crisis). Proceed.

## Phase 0 — Framing

### Intuition Record

**First instinct:** Invest in product features. The company is losing to competitors on capability — customers churn when they hit gaps the competitor fills.

**Emotion present:** Frustration with the onboarding team's slow progress and defensiveness.

**What that emotion may be signaling:** The frustration may be displaced accountability. If the product is harder to adopt than competitors', onboarding's "slowness" may be a symptom, not a cause. The emotion also signals identity attachment — the CEO came from product engineering and may equate product investment with strategic seriousness.

### Core Classification

- **Type:** Decision
- **Stakes:** Reversible — budget can be reallocated next quarter; no irrevocable commitment
- **Time tier:** T2 — budget meeting in two weeks; under one day of analysis needed
- **Uncertainty:** Known — retention data exists, but root cause attribution is ambiguous
- **Core tension:** Resource vs Goal — both features and process need budget; the real question is marginal allocation, not either/or

**Framing sentence:** This is a decision problem with reversible stakes, T2 timing, known uncertainty, centered on resource vs goal tension, with likely resistance from the CEO (product bias) and VP Customer Success (process bias).

### Stakeholder Map

- **CEO:** Holds decision power. Prefers product investment. Wants competitive advantage and sees features as the lever. Came from engineering — identity tied to product quality.
- **VP Customer Success:** Has critical information (exit interviews, onboarding drop-off data). Prefers process investment. Sees onboarding gaps daily. Incentivized on NRR.
- **Engineering team:** Advocates for features. More interesting work, better career signaling. No direct incentive tied to retention.
- **Support team:** Wants more resources. Currently overwhelmed by repeat tickets. Has information about what customers actually struggle with, but limited influence on budget decisions.
- **Customers (churned):** Information source but not in the room. Their stated reasons for leaving may differ from revealed reasons (attribution bias in exit surveys).

### Attachment Check

**CEO has strong attachment to product investment path.** Mitigation applied:

- Restate problem in third person: "The company must decide which allocation improves retention most, independent of any individual's preferred direction."
- Treat CEO's preference as a hypothesis: "If product gaps are the primary driver, then customers who hit those gaps should churn at higher rates than customers who struggle with onboarding."
- Flag for bias check during collision (Phase 3).

**VP Customer Success also has attachment** — process investment directly benefits their team's resources and perceived importance. Flag as secondary attachment.

## Phase 1 — Lens Selection

**Routing decisions:**

| Signal | Lens | Included? |
|---|---|---|
| Incentives and budget allocation are central | Economics | Yes |
| Human behavior (adoption, resistance, stakeholder bias) | Psychology | Yes |
| System bottleneck (where retention breaks down) | Engineering | Yes |
| Unmet customer need, onboarding friction | Design Thinking | Yes |
| Feedback loops in retention | Systems Dynamics | No — redundant with Engineering for this scope |
| Competitive response | Game Theory | No — this is an internal allocation, not a competitive move problem |
| Base rates for retention interventions | Probability & Statistics | No — useful but secondary; T2 depth doesn't require it |

**Selected lenses (4):**

1. **Economics** — The problem is fundamentally about resource allocation under competing claims. Who benefits from current spending, and what is the marginal return of each option?
2. **Psychology** — Stakeholder attachments are strong, and customer adoption behavior (not just stated preference) is central. Human lens required.
3. **Engineering** — Retention is a pipeline. Where does it break? Is the bottleneck at onboarding, at feature gaps, or elsewhere?
4. **Design Thinking** — What is the lived experience of the customer who churns? Are we solving for the user we have or the user we wish existed?

**Contraindication checks:**

- Economics: Contraindicated when trust, fear, or identity dominate incentives. Here, identity attachment is present (CEO), but incentives (budget, NRR, competitive position) are the primary mechanism. Keep, but flag identity as a risk.
- Psychology: Contraindicated for structural problems. Retention could be structural (product-market fit erosion). Keep, but ensure Engineering and Economics get equal weight.
- Engineering: Contraindicated when treating humans as machine components. Onboarding is human-mediated. Keep, but do not reduce customers to pipeline steps.
- Design Thinking: Contraindicated for mirror-imaging — projecting own motivations onto users. The CEO's "customers need features" may be mirror-imaging. Keep specifically to counter this.

**Depth tier:** T2 → use Intermediate prompts from lens library.

## Phase 2 — Lens Analysis

### Economics

**Mechanism:** Incentives and marginal returns. The current budget allocation may reflect historical inertia, not current marginal value. The question is not "features or process?" but "where does the next dollar produce more retained revenue?"

**Evidence:**

- Current split: ~75% product engineering, ~15% customer success, ~10% support. This ratio predates the retention decline and has not been adjusted.
- VP Customer Success's team has 4 CSMs for ~200 accounts. Industry benchmark for B2B SaaS at this ARPU is 1:40 — the team is 50% understaffed relative to benchmark.
- Feature requests from churned customers cluster around two capabilities. Competitor parity exists for one; the other is on the roadmap but 2 quarters out.
- Support ticket volume has increased 40% over three quarters while headcount stayed flat.

**Implication:** The marginal return of process investment is likely higher than the marginal return of feature investment right now, because process is severely under-resourced relative to benchmarks and demand, while feature investment is already at high levels with diminishing returns.

**Disconfirming signal:** If churned customers who received strong onboarding support still left at similar rates, then process investment won't help. If customers who never filed a support ticket also churn, the bottleneck is not in support/onboarding.

**What this lens likely misses:** It assumes customers respond to the quality of onboarding and support as rational economic actors. It underweights the possibility that the product itself has become uncompetitive and that better onboarding merely delays inevitable churn.

### Psychology

**Mechanism:** Cognitive biases shaping both stakeholder positions and customer behavior. The CEO's product preference may be driven by identity and confirmation bias, not evidence. Customer churn explanations in exit surveys may be post-rationalizations.

**Evidence:**

- Exit interview data: 60% of churned customers cite "missing features." But only 20% of those had ever used the features they say are missing (revealed vs stated preference gap).
- CEO references specific feature gaps in every discussion but has not seen the full onboarding funnel data. Confirmation bias: seeking evidence that supports product investment.
- Engineering team's feature advocacy correlates with work they find interesting, not with customer-requested features. Sunk cost: they've already designed solutions for the gaps.
- VP Customer Success reports that customers who complete onboarding within 30 days have 85% retention vs 45% for those who don't — but the CEO has not engaged with this data.

**Implication:** The "features vs process" framing may be a false dichotomy created by stakeholder bias. The real question is: at which stage of the customer journey does the highest-value intervention exist? Psychology suggests the answer is early (onboarding), not late (feature gaps), because the revealed behavior data contradicts the stated reasons.

**Disconfirming signal:** If high-touch onboarding customers churn at the same rate as self-serve customers, the onboarding experience is not the psychological lever. If A/B testing shows feature-awareness campaigns (not new features) improve retention, the problem is information, not process.

**What this lens likely misses:** The psychological explanation (bias, identity, post-rationalization) may be correct for stakeholders but wrong for customers. Customers may genuinely need features they haven't used yet because they couldn't discover them in the current UX. Not using a feature ≠ not needing it.

### Engineering

**Mechanism:** Bottleneck analysis. The retention pipeline has stages (sign-up → onboarding → first value → ongoing use → renewal). Find where the throughput drops most sharply.

**Evidence:**

- Funnel data: 90% of signed customers complete onboarding, but only 55% reach "first value" (defined as completing the core workflow within 45 days). The steepest drop is between onboarding completion and first value.
- Time-to-first-value for retained customers: 18 days median. For churned customers: 38 days median. Customers who take longer than 30 days to reach first value churn at 3× the rate.
- Support tickets per customer spike in weeks 3-6 — the "valley of despair" between onboarding and habitual use. Tickets are not about missing features; they cluster around workflow configuration and data migration.
- Feature usage data: retained and churned customers use roughly the same feature set in the first 90 days. The two most-requested missing features are used by <5% of retained customers even when available.

**Implication:** The bottleneck is not at the onboarding step (90% completion) but in the gap between onboarding and first value. This is a process problem, but not the one VP Customer Success is describing. It's not "more CSMs" — it's redesigning the handoff between onboarding and ongoing use so customers reach first value faster.

**Disconfirming signal:** If the 55% first-value rate has been stable for years and only retention changed, the bottleneck is elsewhere. If the feature gap that competitors fill is in the core workflow (not peripheral), Engineering's argument that features unblock first value could be correct.

**What this lens likely misses:** Engineering optimizes throughput, but customers aren't just flowing through a pipeline. Some customers who reach first value still churn for reasons unrelated to the funnel (contract terms, pricing, organizational change). Also, the funnel data is correlational — reaching first value faster may be a marker of customer intent, not a cause of retention.

### Design Thinking

**Mechanism:** Unmet need and lived experience. What job is the customer hiring the product for, and where does the experience fail to deliver on that job?

**Evidence:**

- Customer interviews (15 recent churns): The most common frustration is not "missing features" but "I couldn't get it to work the way I expected within the first month." The expectation gap is between what the sales demo showed and what the product delivers without significant configuration.
- Onboarding NPS is 32 for customers who churn, 67 for those who renew. The experience in the first 45 days is the strongest predictor of renewal intent.
- The two "missing features" cited in exit surveys are both available in the product — they're just not discoverable in the default workflow. Customers don't know the product can do what they want.
- Sales process: demos are highly customized by the sales team, creating an expectation that the self-serve onboarding experience cannot meet.

**Implication:** The core unmet need is not more features or more CSMs — it's alignment between the promised experience (sales demo) and the delivered experience (first 45 days). The "feature gap" is partially an information architecture and discoverability problem. Investing in features would widen the expectation gap further unless the discovery problem is solved first.

**Disconfirming signal:** If customers who received an accurate (un-customized) demo still churn at similar rates, the sales-demo gap is not the primary driver. If adding the two most-requested features to the default workflow significantly improves retention in a test, the feature argument has merit.

**What this lens likely misses:** Design thinking optimizes for the user's experience but may underweight structural constraints. Even if discoverability is the problem, fixing it might require product engineering work (information architecture, workflow redesign) — which means the "process vs features" framing is wrong and the real answer is "features, but different ones than the CEO thinks."

## Phase 2.5 — Transfer

Skip. This problem does not call for reuse, analogy, or cross-domain transfer. It is a specific resource allocation decision, not a pattern-extraction opportunity.

## Phase 3 — Collision

### Agreements

- All four lenses agree that the stated reason for churn ("missing features") does not match revealed behavior. Customers say features; their behavior says something else.
- All four lenses agree that the first 45 days of the customer lifecycle is the critical period. Interventions after that window have lower marginal impact.
- Engineering and Design Thinking converge: the bottleneck is between onboarding completion and first value, and the core problem is an experience gap, not a capability gap.
- Economics and Psychology converge: the current budget allocation is based on historical patterns, not current marginal returns, and is biased toward the status quo of feature investment.

### Contradictions

**Contradiction 1 — What is the bottleneck, really?**
- Engineering says: the process between onboarding and first value (workflow configuration, data migration, the "valley of despair").
- Economics says: the process team is under-resourced; the marginal dollar goes further in customer success.
- Design Thinking says: the problem is discoverability and expectation alignment, which requires product changes (information architecture, workflow redesign), not just more process support.
- Psychology says: the CEO's product preference may be right for the wrong reasons — the product does need changes, but they're UX/IA changes, not the competitive features the CEO is advocating for.

→ Design Thinking and the CEO both want product changes, but completely different ones. This is a real and important disagreement hidden by the surface-level "features vs process" framing.

**Contradiction 2 — Does process investment solve the problem or just mask it?**
- Economics + Psychology: Process investment has higher marginal return and the data supports it.
- Engineering: Process alone won't fix the bottleneck; the workflow itself needs redesign.
- Design Thinking: More CSMs without better tooling just creates more frustrated hand-holding.

→ If the problem is discoverability, adding CSMs is a band-aid. But if discoverability requires engineering work to fix, then the CEO's instinct (product investment) is directionally right but targeted wrong.

**Contradiction 3 — Is "reaching first value faster" causal or correlational?**
- Engineering treats the 18-day vs 38-day time-to-first-value as a causal bottleneck.
- Psychology flags that customers who reach first value faster may simply be more committed or technically capable — the correlation doesn't prove that speeding up first value causes retention.

→ This is unresolved and matters for the recommendation.

### Conflict Resolution Ladder

**Layer 1 — Evidence Weighting**

| Lens | Observed behavior/data? | Base-rate support? | Ruled out alternative? | Score |
|---|---|---|---|---|
| Economics | Yes (+1) — budget ratios, benchmarks, ticket volume | Yes (+1) — industry CSM ratios support understaffing claim | Partial (+0.5) — didn't fully rule out that features could have equal ROI | **2.5** |
| Psychology | Yes (+1) — revealed vs stated preference gap is measured | Partial (+0.5) — bias patterns are well-documented but case-specific | Yes (+1) — feature usage data rules out "customers use what they request" | **2.5** |
| Engineering | Yes (+1) — funnel data, time-to-first-value metrics | Partial (+0.5) — funnel analysis is standard but causality is uncertain | No (0) — did not rule out that fast-first-value customers are self-selecting | **1.5** |
| Design Thinking | Partial (+0.5) — interview data is qualitative, N=15 | No (0) — no base rate for "sales demo / experience gap" as churn driver | Partial (+0.5) — discoverability hypothesis partially rules out feature gap | **1.0** |

**Result:** Economics and Psychology tie at 2.5. Engineering at 1.5. Design Thinking at 1.0. No single lens dominates. Contradiction 1 (what product changes, if any) and Contradiction 3 (causality of time-to-first-value) remain unresolved.

**Risk items carried forward from defeated lenses:**

- From Engineering: the causality question on time-to-first-value (may be selection effect, not causal)
- From Design Thinking: the discoverability problem may require engineering work, which means some product investment is needed — just not the features the CEO wants

→ **Layer 1 does not fully resolve the collision.** Proceed to Layer 2.

**Layer 2 — Assumption Strip**

For the two key remaining contradictions:

*Contradiction 1 — What kind of product changes are needed?*

| Lens position | Must be true for this to hold | Verified? |
|---|---|---|
| CEO/Feature argument | Customers churn because competitors offer specific capabilities that this product lacks | Partially verified — exit surveys cite this, but usage data contradicts it |
| Design Thinking/Discoverability argument | Customers could find and use existing features if the information architecture and default workflow were improved | Unverified — no A/B test or natural experiment confirms this |
| Economics/Process argument | More CSM hours would help customers through the valley of despair | Partially verified — CSM-to-account ratio is below benchmark and ticket volume is high |

*Contradiction 3 — Is fast first-value causal?*

| Lens position | Must be true for this to hold | Verified? |
|---|---|---|
| Engineering (causal) | Speeding up first value will improve retention regardless of customer type | Unverified — no natural experiment or quasi-experiment confirms this |
| Psychology (selection effect) | Customers who reach first value faster are a self-selecting group with higher commitment or capability | Partially verified — this is a well-known confound in funnel analytics |

**Result:** The feature argument depends on stated preference data that revealed preference contradicts — the weakest evidentiary position. The discoverability argument is unverified but testable. The process argument has the most verified assumptions (benchmarks + ticket data). The causality question on first-value is unresolved and both positions depend on unverified assumptions.

→ **Layer 2 partially resolves the collision.** The feature argument is downgraded from "finding" to "inference" — it depends on stated preference data that is contradicted by usage data. The process argument and discoverability argument both survive but remain in tension. Causality of first-value remains an unverified assumption on both sides.

No need for Layer 3 (Testability Check) or Layer 4 (Decision Path) — the collision has been resolved enough to produce a recommendation with explicit uncertainty markers. The key insight from the ladder is: **the "features vs process" framing is wrong. The real allocation question is "process investment + targeted product investment in discoverability, not competitive features."**

### Boundary Scan

- **Outside-view base rate:** What is the base rate for B2B SaaS retention recovery after process investment vs feature investment? The analysis hasn't checked this. [Gap]
- **Unknown stakeholders:** The sales team creates the expectation gap (customized demos) but is not represented in the budget discussion. Their incentives (close deals) may actively conflict with retention (overpromising). [Blind spot]
- **Cultural dynamics:** Engineering sees process work as less valuable than feature work. This cultural bias, not just the CEO's preference, may be driving the allocation inertia. [Hidden constraint]
- **Second-order effect:** If process investment succeeds and retention improves, the CEO may interpret this as "we can now afford to invest in features" and shift budget back, recreating the original imbalance. [Feedback loop risk]
- **Pricing/contract structure:** The analysis hasn't examined whether pricing or contract terms contribute to churn. If customers are on monthly plans with low switching costs, retention may be structurally harder regardless of product or process quality. [Missing lens]

### Mirror-Imaging Check

- "CEO prefers features because he came from engineering" — this is inferred motive, not observed fact. The CEO may genuinely believe features are the competitive lever based on market analysis. Label as inference.
- "Engineering advocates features because the work is more interesting" — partially inferred. Some engineers may genuinely believe features matter most. Label as partial inference.
- "Customers say features but mean something else" — supported by usage data, not purely projected. Keep as evidence-weighted finding.
- "Sales team overpromises to close deals" — plausible but unverified. This is a mirror-image risk: attributing self-serving behavior to sales without evidence. Label as inference requiring validation.

## Phase 4 — Synthesis

### Recommendation

**Allocate 60% of the incremental budget to customer success/support process and 40% to targeted product improvements — but the product work must be scoped to discoverability and first-value acceleration (information architecture, workflow defaults, in-app guidance), not competitive feature parity.**

Specifically:

1. Add 2 CSMs (bringing ratio closer to benchmark) with a mandate to redesign the onboarding-to-first-value handoff.
2. Assign 1 engineering team (2-3 engineers) for one quarter to: redesign the default workflow to surface the two most-requested features that already exist; improve in-app guidance for the "valley of despair" period (weeks 3-6); and close the sales-demo / actual-experience gap by standardizing demo environments.
3. Defer the competitive feature build (the CEO's preferred project) by one quarter. Use the quarter to measure whether discoverability improvements move retention.
4. Include the sales team in the retention working group — they create the expectation that onboarding must deliver on.

### Tradeoff Accepted

- The competitive feature is delayed by one quarter. If a competitor wins a deal specifically because of that feature, this decision will look wrong in hindsight.
- Engineering team morale may dip — discoverability work is less prestigious than new feature development. This needs active management.
- The 60/40 split will not fully satisfy either stakeholder. The CEO gets less product investment than wanted; VP Customer Success gets less than the full process investment requested.

### Most Dangerous Assumption

**That time-to-first-value is causal, not a selection effect.** If customers who reach first value faster are simply more committed or capable, then redesigning the workflow to accelerate first value will not improve retention — it will just change the metric without changing the outcome. This is the single assumption that would make the recommendation wrong.

### First Test

**Run a quasi-experiment on the existing customer base:** Segment customers by time-to-first-value and control for company size, industry, and plan type. If the retention difference persists after controlling for these confounds, the causal interpretation is strengthened. If it disappears, the selection-effect interpretation is correct and the recommendation needs revision.

This test can be completed with existing data in under 3 days.

### What Not To Do Next

**Do not announce a "retention initiative" or set a public retention target before the first test validates the causal assumption.** Premature commitment to a metric creates pressure to game the metric rather than solve the problem. If the team is incentivized on a retention number before the causal mechanism is confirmed, they will optimize for the easiest path to that number (e.g., discounting renewals, extending trials) rather than the actual bottleneck.

### Confidence Level

**Medium.** The analysis converges on process + discoverability as the higher-marginal-return allocation, and the evidence weighting supports this direction. But two critical assumptions remain unverified: (1) causality of time-to-first-value, and (2) whether discoverability improvements will actually surface the features customers need. The recommendation is structured as a reversible bet with a built-in validation test, which is appropriate for medium confidence on a reversible decision.

## Phase 5 — Calibrate

**Did the analysis confirm or overturn the first instinct?**

The first instinct was "invest in product features because customers are leaving for competitors." The analysis overturned this — not by proving the CEO wrong, but by showing that the feature argument depends on stated preference data contradicted by revealed behavior. The direction is partially right (product changes are needed) but the target is wrong (discoverability, not competitive features).

**If it overturned it, what was missed at first glance?**

Two things: (1) the revealed vs stated preference gap — customers say features but their behavior says something else; (2) the fact that the "missing features" already exist in the product and are undiscoverable. The first instinct treated exit survey data as reliable without cross-referencing usage data.

**Does the answer feel hollow?**

No. The collision produced genuine tension (Design Thinking and the CEO both want product changes but for different reasons; Engineering and Psychology disagree on causality). The recommendation is a specific allocation with a test, not a hedge. The tradeoff is explicit and real. The analysis holds weight because the disagreements were preserved, not smoothed over.

## If We Are Wrong

1. **The feature gap is real and urgent.** A competitor launches the missing capability, wins 3-5 key accounts in the next quarter, and the one-quarter delay becomes a critical loss. The discoverability investment was wasted because the product genuinely needed that feature to compete, and the usage data was misleading (customers hadn't used the feature because they couldn't, not because they didn't need it).

2. **Time-to-first-value is a selection effect.** The workflow redesign doesn't move retention. The CSMs improve the experience but can't fix the underlying issue, which is that the product's core value proposition is eroding relative to the market. Process investment becomes a cost center without ROI, and the company has burned a quarter of runway.

3. **The sales team is the primary driver of churn, and neither features nor process fixes it.** The expectation gap created by customized demos is so large that no amount of onboarding improvement can bridge it. The real intervention is sales process reform, which neither stakeholder is advocating for and which the boundary scan identified but the recommendation only partially addresses.

4. **Engineering culture makes the 40% product allocation ineffective.** The engineers assigned to discoverability work treat it as low-priority, deliver superficial changes, and the real bottleneck (workflow configuration complexity) requires a deeper refactor that no one scoped. The process team carries the load but without the product support they need, the 60/40 split fails on both sides.