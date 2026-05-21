# Lens Library

Use this file only after `dynamic-problem-solving` has triggered and you know which lenses you need.

Each lens gives you:

- the question it is best at answering
- the situations where it helps most
- the prompts that surface useful signal
- the failure mode that keeps the lens honest

## Biology and Ecology

**Best question:** How does adaptation, selection, and niche fit shape survival?

Use for:
- market positioning
- startup strategy
- organizational adaptation
- ecosystem dependence

Basic prompts (T1 — under 1 hour, or quick screening):
- What niche is actually defendable?
- Is this strategy adapting to the environment or fighting it?
- Which dependencies are symbiotic, parasitic, or fragile?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What niche is actually defendable?
- Is this strategy adapting to the environment or fighting it?
- Which dependencies are symbiotic, parasitic, or fragile?
- What redundancy protects against failure?
- What selective pressure is currently the strongest — and is it stable or shifting?
- How quickly can this organism/organization adapt relative to the rate of environmental change?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What niche is actually defendable?
- Is this strategy adapting to the environment or fighting it?
- Which dependencies are symbiotic, parasitic, or fragile?
- What redundancy protects against failure?
- What selective pressure is currently the strongest — and is it stable or shifting?
- How quickly can this organism/organization adapt relative to the rate of environmental change?
- What is the carrying capacity of this niche, and how close is the current population to it?
- What happens if a keystone species/partner is removed — does the ecosystem collapse or restructure?
- Is this adaptation local optimization at the cost of long-term evolvability?
- What co-evolutionary dynamics are at play — are competitors adapting in response?
- What is the survivorship bias in visible successes — are we seeing only the fit that survived?
- What would an invasive species/disruptor exploit in this ecosystem?

Contraindication:
- DO NOT use when direct causal analysis is available and sufficient — evolutionary metaphors add noise where mechanisms are known
- DO NOT use when the environment is engineered and stable rather than competitive and selecting
- Use with caution when the metaphor of "fitness" could legitimize harmful outcomes as "natural selection"

Failure mode:
- Using evolutionary metaphors where direct causal analysis is needed.

## Design Thinking

**Best question:** What unmet need or friction exists in the lived user experience?

Use for:
- UX issues
- onboarding
- unmet customer needs
- product adoption

Basic prompts (T1 — under 1 hour, or quick screening):
- What job is the user actually hiring this for?
- Where is the emotional or workflow friction?
- What evidence comes from real behavior instead of imagined empathy?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What job is the user actually hiring this for?
- Where is the emotional or workflow friction?
- What evidence comes from real behavior instead of imagined empathy?
- Are we solving for the user we have or the user we wish existed?
- What workaround is the user already doing that signals an unmet need?
- What is the user's actual sequence of actions vs the intended sequence?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What job is the user actually hiring this for?
- Where is the emotional or workflow friction?
- What evidence comes from real behavior instead of imagined empathy?
- Are we solving for the user we have or the user we wish existed?
- What workaround is the user already doing that signals an unmet need?
- What is the user's actual sequence of actions vs the intended sequence?
- What edge cases are being treated as noise but are actually distinct user segments?
- What is the user's broader context — what else competes for their attention at the moment of use?
- How would the least capable user experience this — accessibility, literacy, cognitive load?
- What organizational assumptions about users are untested and widely shared?
- What would users do if this product disappeared tomorrow — would they notice, substitute, or improvise?
- What is the difference between the problem users describe and the problem they actually have?

Contraindication:
- DO NOT use when the problem is fundamentally a constraint problem (resource limits, regulatory walls) rather than a user experience problem
- DO NOT use when "user needs" are secondary to system requirements — safety-critical, compliance-driven, or infrastructure systems
- Use with caution when your user research sample is narrow or self-selected — empathy for a subset is not empathy for the whole

Failure mode:
- Mirror imaging: projecting your own motivations onto users.

## Economics

**Best question:** What incentives and tradeoffs are actually shaping behavior?

Use for:
- pricing
- resource allocation
- market behavior
- incentive design

Basic prompts (T1 — under 1 hour, or quick screening):
- Who benefits from the current state?
- What is the opportunity cost of each option?
- What changes at the margin, not just in total?

Intermediate prompts (T2 — under 1 day, standard analysis):
- Who benefits from the current state?
- What is the opportunity cost of each option?
- What changes at the margin, not just in total?
- Where does information asymmetry distort the outcome?
- What is the actual price signal, and what is distorting it?
- Who bears the externality that others profit from?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- Who benefits from the current state?
- What is the opportunity cost of each option?
- What changes at the margin, not just in total?
- Where does information asymmetry distort the outcome?
- What is the actual price signal, and what is distorting it?
- Who bears the externality that others profit from?
- What happens to marginal behavior if incentives shift — is elasticity high or near-zero?
- Are there principal-agent problems where decision-maker and beneficiary are misaligned?
- What is the tragedy-of-the-commons risk if this resource is unpriced?
- What market failure is present — monopoly, externality, information asymmetry, or public goods?
- How would rational actors game or circumvent this incentive structure?
- What is the second-order incentive effect — what does the incentive discourage that it shouldn't?

Contraindication:
- DO NOT use when behavior is driven primarily by trust, fear, identity, or ideology rather than incentives — economic framing will misread the mechanism
- DO NOT use when the system is a command structure, not a market — prices and incentives may be overridden by authority
- Use with caution when actors have bounded rationality or when cultural norms override economic rationality

Failure mode:
- Assuming people respond cleanly to incentives when trust, fear, or identity dominate.

## Engineering

**Best question:** Where does the system break, bottleneck, or degrade?

Use for:
- process design
- operational issues
- execution failures
- reliability problems

Basic prompts (T1 — under 1 hour, or quick screening):
- What is the bottleneck?
- What is the single point of failure?
- Where is the highest friction?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What is the bottleneck?
- What is the single point of failure?
- Where is the highest friction?
- What failure mode would destroy the whole plan?
- What is the degradation path — does the system fail gracefully or catastrophically?
- Where is the coupling tightest, and what happens when that component changes?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What is the bottleneck?
- What is the single point of failure?
- Where is the highest friction?
- What failure mode would destroy the whole plan?
- What is the degradation path — does the system fail gracefully or catastrophically?
- Where is the coupling tightest, and what happens when that component changes?
- What is the failure mode of the monitoring itself — will you know when the system is degrading?
- What load or stress is the system not designed for, and how likely is it?
- What are the cascading failure paths — which single failure triggers a chain?
- Where does the system assume consistent conditions that may not hold (temperature, load, connectivity)?
- What maintenance is required, and what happens when it is deferred?
- How does the system behave at 10x current scale — where does it break first?

Contraindication:
- DO NOT use when the primary constraints are human — motivation, trust, politics — not system architecture
- DO NOT use when the system is inherently adaptive and cannot be modeled as a fixed pipeline
- Use with caution when treating humans as components — people respond to being optimized in ways machines do not

Failure mode:
- Treating humans like machine components.

## First Principles

**Best question:** Which assumptions are inherited rather than true?

Use for:
- novel problems
- fake constraints
- stale categories
- situations where every existing lens depends on suspect premises

Basic prompts (T1 — under 1 hour, or quick screening):
- What do we know as fact?
- Which assumption, if removed, changes the whole solution space?
- What would this look like if we rebuilt from physics, math, or direct reality?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What do we know as fact?
- Which assumption, if removed, changes the whole solution space?
- What would this look like if we rebuilt from physics, math, or direct reality?
- What mechanism are we extracting before we generalize it?
- What must remain invariant for this principle to transfer?
- How would this principle map into another domain?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What do we know as fact?
- Which assumption, if removed, changes the whole solution space?
- What would this look like if we rebuilt from physics, math, or direct reality?
- What mechanism are we extracting before we generalize it?
- What must remain invariant for this principle to transfer?
- How would this principle map into another domain?
- What would break this transfer or make it non-portable?
- What constraint is "common knowledge" but has never been independently verified?
- What is the earliest point in the reasoning chain where an assumption was introduced — and is it load-bearing?
- What would a contrarian who rejects this assumption build instead?
- What is the cost of being wrong about this assumption — reversible or existential?
- What evidence would compel you to abandon the first-principles conclusion in favor of a conventional one?

Contraindication:
- DO NOT use when the problem domain is well-understood with proven solutions — reinventing from scratch wastes time and repeats known mistakes
- DO NOT use when time pressure demands a proven pattern, not a novel decomposition
- Use with caution when your "first principles" are actually just contrarian intuition dressed up as reasoning — verify the facts are actually facts

Failure mode:
- Over-generalizing a mechanism across domains with incompatible constraints.

## Game Theory

**Best question:** How will other strategic actors respond?

Use for:
- negotiations
- competitive moves
- cooperation problems
- channel conflict

Basic prompts (T1 — under 1 hour, or quick screening):
- What are the players optimizing for?
- What would each player do if only they changed strategy?
- Is this zero-sum, positive-sum, or mixed?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What are the players optimizing for?
- What would each player do if only they changed strategy?
- Is this zero-sum, positive-sum, or mixed?
- Is there first-mover or second-mover advantage?
- What is each player's outside option (BATNA)?
- What information does each player have that others do not?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What are the players optimizing for?
- What would each player do if only they changed strategy?
- Is this zero-sum, positive-sum, or mixed?
- Is there first-mover or second-mover advantage?
- What is each player's outside option (BATNA)?
- What information does each player have that others do not?
- Is the game repeated or one-shot — how does this change the equilibrium?
- What commitment or credibility problem exists — can players credibly threaten or promise?
- What coalition structures are possible — who aligns with whom?
- What is the mechanism by which players observe each other's moves?
- Are there players whose irrationality or miscalculation changes the equilibrium?
- What happens if a new player enters or an existing player exits?

Contraindication:
- DO NOT use when actors are not strategic — if they are driven by habit, emotion, or instinct rather than optimization, game-theoretic equilibrium is meaningless
- DO NOT use when the number of players is very large and undifferentiated — this is a market, not a game
- Use with caution when culture or norms override strategic calculation — the predicted move may not be the culturally acceptable one

Failure mode:
- Assuming stable rational play where norms, fear, or politics dominate.

## History / Analogical Reasoning

**Best question:** What has this looked like before, and what can we learn from the similarities and differences?

Use for:
- strategic decisions with precedent
- avoiding known failure patterns
- identifying repeating cycles
- estimating outcomes when direct data is sparse
- challenging the "this time is different" narrative

Basic prompts (T1 — under 1 hour, or quick screening):
- What is the closest historical parallel to this situation?
- What happened in that case — success, failure, or mixed?
- What was the one thing participants at the time did not see coming?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What is the closest historical parallel to this situation?
- What happened in that case — success, failure, or mixed?
- What was the one thing participants at the time did not see coming?
- How was the historical case similar and different in structure (not just surface)?
- What was the base rate outcome across multiple similar cases?
- What assumptions did historical participants make that turned out wrong?
- What was the critical juncture that determined the outcome?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What is the closest historical parallel to this situation?
- What happened in that case — success, failure, or mixed?
- What was the one thing participants at the time did not see coming?
- How was the historical case similar and different in structure (not just surface)?
- What was the base rate outcome across multiple similar cases?
- What assumptions did historical participants make that turned out wrong?
- What was the critical juncture that determined the outcome?
- Run a structured analogy test: structural similarity (are causal mechanisms the same?), surface similarity (are contexts/actors/technologies comparable?), temporal distance (has the environment changed in ways that break the analogy?), outcome variance (are there cases with different outcomes?).
- What is the "this time is different" narrative, and why might it be wrong?
- What historical counterfactual is most instructive?
- What is the selection bias in the historical record (survivorship bias, recording bias, winner's history)?
- What period or institutional memory is missing from current decision-makers?

Contraindication:
- DO NOT use when the historical case is superficially similar but structurally different — bad analogies are worse than no analogies
- DO NOT use when the base rate is unknown or the historical record is too sparse to establish a pattern
- DO NOT use when the environment has changed fundamentally (technological discontinuities, regime changes)
- Use with caution when the analogy supports a preferred conclusion — historical analogies are easily cherry-picked

Failure mode:
- False analogy: treating structural differences as irrelevant. Cherry-picking: selecting the historical case that supports the preferred narrative and ignoring contradictory precedents.

## Information Theory

**Best question:** What signals are available, what is noise, and how does information flow (or fail to flow) through the system?

Use for:
- communication degradation in organizations
- data quality and signal-to-noise problems
- decision-making under missing or distorted information
- complex systems with multiple relay points
- any situation where "we didn't know" or "that got lost" happens repeatedly

Basic prompts (T1 — under 1 hour, or quick screening):
- What information is missing from this decision?
- What is the most important signal, and how is it being degraded?
- Who has information that others need but do not have?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What information is missing from this decision?
- What is the most important signal, and how is it being degraded?
- Who has information that others need but do not have?
- How many relay hops does critical information travel through? (Each hop is a chance for noise.)
- What feedback channel exists for the sender to know the message was received correctly?
- What information is being sent that is actually noise?
- What is the channel capacity — is the system being overloaded with information it cannot process?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What information is missing from this decision?
- What is the most important signal, and how is it being degraded?
- Who has information that others need but do not have?
- How many relay hops does critical information travel through? (Each hop is a chance for noise.)
- What feedback channel exists for the sender to know the message was received correctly?
- What information is being sent that is actually noise?
- What is the channel capacity — is the system being overloaded with information it cannot process?
- Map the information flow: sender → encoding → channel → decoding → receiver. Where is degradation happening at each step?
- What information is systematically filtered out by organizational incentives or hierarchy? (Information hiding, bad news suppression)
- What is the redundancy in the system — is there a single point of information failure?
- What is the cost of information acquisition vs the cost of information absence?
- What signals exist that are being ignored because they are weak but diagnostically valuable?
- Is the problem one of insufficient information, or of information overload / attention scarcity?
- What would a system look like that was optimized for information fidelity rather than efficiency?

Contraindication:
- DO NOT use when the main problem is misaligned incentives rather than information flow — better signals won't fix people who don't want to hear
- DO NOT use when the information is complete but interpretation is contested — that's a Psychology or Politics problem, not an information problem
- Use with caution in highly political environments — information distortion is often intentional, not accidental, and treating it as a technical problem misses the power dynamics

Failure mode:
- Treating information problems as purely technical when they are actually political or motivational. Over-engineering communication systems when a single direct conversation would solve the problem.

## Legal / Regulatory

**Best question:** What legal, regulatory, or compliance constraints actually determine what is possible?

Use for:
- compliance decisions
- regulatory risk assessment
- contract/liability analysis
- jurisdiction/venue questions
- any problem where "can we do this?" is the real first question

Basic prompts (T1 — under 1 hour, or quick screening):
- What is the relevant legal or regulatory framework?
- What is the worst legally plausible outcome?
- Is this problem really a legal constraint or just a perceived one?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What is the relevant legal or regulatory framework?
- What is the worst legally plausible outcome?
- Is this problem really a legal constraint or just a perceived one?
- What is the enforcement track record for this regulation?
- Where is the regulatory uncertainty — gaps, ambiguity, pending changes?
- Who has standing to challenge this decision legally?
- What is the cost of compliance vs the cost of non-compliance?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What is the relevant legal or regulatory framework?
- What is the worst legally plausible outcome?
- Is this problem really a legal constraint or just a perceived one?
- What is the enforcement track record for this regulation?
- Where is the regulatory uncertainty — gaps, ambiguity, pending changes?
- Who has standing to challenge this decision legally?
- What is the cost of compliance vs the cost of non-compliance?
- What jurisdiction shopping or arbitrage is possible?
- What is the regulatory trend direction — tightening, loosening, or unstable?
- What is the precedent landscape — which cases or rulings set the boundary?
- What would a motivated regulator or plaintiff argue?
- What contractual or liability exposure exists in the supply chain?
- What is the statute of limitations and when does it start?
- What regulatory change would break the current model entirely?

Contraindication:
- DO NOT use as the primary lens when the real question is strategic or competitive — legal is a constraint, not a strategy
- DO NOT use when the legal framework is essentially irrelevant to the outcome (informal economies, norms-governed spaces)
- Use with caution when legal advice is needed but no qualified counsel is available — this lens identifies risks, it does not replace a lawyer

Failure mode:
- Treating regulatory compliance as the ceiling instead of the floor — legal permissibility is not the same as ethical or strategic soundness.

## Philosophy

**Best question:** What values, legitimacy tests, or truth standards are being smuggled in?

Use for:
- ethics conflicts
- fairness disputes
- legitimacy questions
- reasoning quality checks

Basic prompts (T1 — under 1 hour, or quick screening):
- What value conflict is hidden inside this dispute?
- What standard makes one answer more justified than another?
- Is the argument falsifiable?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What value conflict is hidden inside this dispute?
- What standard makes one answer more justified than another?
- Is the argument falsifiable?
- Are we confusing what works with what is acceptable?
- What would the opposing position need to demonstrate to change your mind?
- Whose definition of "fair" is being used, and who does it favor?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What value conflict is hidden inside this dispute?
- What standard makes one answer more justified than another?
- Is the argument falsifiable?
- Are we confusing what works with what is acceptable?
- What would the opposing position need to demonstrate to change your mind?
- Whose definition of "fair" is being used, and who does it favor?
- What is the is-ought gap in this argument — where does descriptive become prescriptive?
- What would a consequentialist, deontologist, and virtue ethicist each conclude — and where do they agree?
- What moral hazard does the preferred position create?
- What rights or obligations are being assumed without justification?
- What would the decision look like from the perspective of the least powerful affected party?
- What truth standard is being applied — correspondence, coherence, pragmatism — and would another standard yield a different answer?

Contraindication:
- DO NOT use when the problem is operational and the values are already settled — philosophical framing delays action without adding clarity
- DO NOT use when there is no genuine value conflict, only an execution problem disguised as one
- Use with caution when philosophical analysis becomes a substitute for making a decision — clarity about values does not require infinite reflection

Failure mode:
- Producing elegant critique without operational guidance.

## Probability and Statistics

**Best question:** What is the uncertainty distribution, not just the most vivid scenario?

Use for:
- forecasting
- risk decisions
- low-signal environments
- prioritization under uncertainty

Basic prompts (T1 — under 1 hour, or quick screening):
- What is the base rate for similar cases?
- What is the expected value, not just the upside?
- Which assumptions dominate the variance?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What is the base rate for similar cases?
- What is the expected value, not just the upside?
- Which assumptions dominate the variance?
- What evidence would update the probability meaningfully?
- What is the confidence interval, not just the point estimate?
- Are the events independent, or is there correlation that changes the distribution?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What is the base rate for similar cases?
- What is the expected value, not just the upside?
- Which assumptions dominate the variance?
- What evidence would update the probability meaningfully?
- What is the confidence interval, not just the point estimate?
- Are the events independent, or is there correlation that changes the distribution?
- What does the fat tail look like — is the worst case 10x the mean or 1000x?
- What is the reference class, and is it the right one — are you grouping with genuinely similar cases?
- What survivorship bias exists in the data you are using to estimate probabilities?
- What is the prior, and how much evidence is needed to overcome it?
- What would a Bayes-optimal decision look like, and how far is the current plan from it?
- What is the value of additional information — at what point does more data stop changing the decision?

Contraindication:
- DO NOT use when the sample size is too small for any meaningful statistical inference — the numbers will look precise but be meaningless
- DO NOT use when the distribution is unknown and possibly unbounded — assuming a normal distribution in a power-law world is catastrophic
- Use with caution when quantitative precision creates false confidence — a precise wrong number is more dangerous than an honest rough estimate

Failure mode:
- Pretending rough estimates are precise forecasts.

## Psychology

**Best question:** What is happening in the human mind that the surface story hides?

Use for:
- user behavior
- team conflict
- negotiation
- adoption resistance

Basic prompts (T1 — under 1 hour, or quick screening):
- Which System 1 reactions are driving behavior?
- What feels like a loss to each actor?
- Which bias is active: confirmation, sunk cost, overconfidence, status quo, attribution?

Intermediate prompts (T2 — under 1 day, standard analysis):
- Which System 1 reactions are driving behavior?
- What feels like a loss to each actor?
- Which bias is active: confirmation, sunk cost, overconfidence, status quo, attribution?
- What is the difference between stated preference and revealed preference?
- What identity threat is this situation posing to each actor?
- What narrative is each person telling themselves to maintain coherence?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- Which System 1 reactions are driving behavior?
- What feels like a loss to each actor?
- Which bias is active: confirmation, sunk cost, overconfidence, status quo, attribution?
- What is the difference between stated preference and revealed preference?
- What identity threat is this situation posing to each actor?
- What narrative is each person telling themselves to maintain coherence?
- What cognitive load is each actor under, and how does it degrade their decision-making?
- What emotional state is the decision-maker in, and how does it bias the outcome?
- What would each actor need to hear to change their mind — and who would they need to hear it from?
- What is the groupthink risk — is dissent being suppressed or self-censored?
- What attachment style or trust model is each actor operating from?
- What would a neutral observer see that the participants cannot?

Contraindication:
- DO NOT use when the problem is structural rather than psychological — if the constraint is real (resource limit, legal barrier, physics), psychologizing it is evasion
- DO NOT use when the problem is a rational conflict of interest — not everything is a misunderstanding or bias
- Use with caution when psychological framing becomes a way to dismiss legitimate concerns as "resistance" or "bias"

Failure mode:
- Over-psychologizing a structural problem.

## Relationship Dynamics

**Best question:** How are trust, face, status, and informal networks shaping the outcome?

Use for:
- founder or executive conflict
- partnerships
- Hong Kong / Asia or other high-context environments
- situations where formal incentives do not explain behavior

Basic prompts (T1 — under 1 hour, or quick screening):
- What relationship debt or trust history exists here?
- Who cannot publicly lose face?
- Which decisions are being made off the formal org chart?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What relationship debt or trust history exists here?
- Who cannot publicly lose face?
- Which decisions are being made off the formal org chart?
- Is indirect communication hiding resistance or disagreement?
- What informal alliance or rivalry is shaping the visible behavior?
- What is the status hierarchy that is not on the org chart?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What relationship debt or trust history exists here?
- Who cannot publicly lose face?
- Which decisions are being made off the formal org chart?
- Is indirect communication hiding resistance or disagreement?
- What informal alliance or rivalry is shaping the visible behavior?
- What is the status hierarchy that is not on the org chart?
- What is the cost of repairing a relationship vs the cost of working around it?
- Who is the trusted broker or intermediary who can move things forward?
- What face-saving exit is available to someone who needs to back down?
- What long-term relational investment is being sacrificed for a short-term transactional win?
- What cultural norms about authority, loyalty, or conflict are shaping what can be said directly?
- What would each party need to feel respected, even if they lose the argument?

Contraindication:
- DO NOT use when the problem is genuinely a resource or capability constraint, not a relational one — sometimes there simply isn't enough money, time, or skill
- DO NOT use when formal incentives and contracts fully explain the behavior — don't over-attribute to culture what is explained by economics
- Use with caution when your cultural knowledge is shallow — misreading face dynamics or trust norms in an unfamiliar context can cause more harm than ignoring them

Failure mode:
- Romanticizing culture and underweighting explicit incentives or hard constraints.

## Systems Dynamics

**Best question:** What feedback loops and delays are shaping the long-term outcome?

Use for:
- market dynamics
- policy effects
- team or product flywheels
- recurring problems

Basic prompts (T1 — under 1 hour, or quick screening):
- What reinforcing loops are amplifying the result?
- What balancing loops are suppressing change?
- Where is there a time delay between action and result?

Intermediate prompts (T2 — under 1 day, standard analysis):
- What reinforcing loops are amplifying the result?
- What balancing loops are suppressing change?
- Where is there a time delay between action and result?
- What second-order effect follows the first fix?
- What stock is being depleted or accumulated that drives the loop?
- Where is the leverage point — the point where a small change shifts the system behavior?

Advanced prompts (T3 — over 1 day, irreversible decisions):
- What reinforcing loops are amplifying the result?
- What balancing loops are suppressing change?
- Where is there a time delay between action and result?
- What second-order effect follows the first fix?
- What stock is being depleted or accumulated that drives the loop?
- Where is the leverage point — the point where a small change shifts the system behavior?
- What happens when the reinforcing loop hits a limit or saturation point?
- What goal-seeking behavior is the system exhibiting, and is the goal the right one?
- What oscillation or overshoot pattern is likely from the delay structure?
- What unintended consequence follows from optimizing one loop in isolation?
- What is the system's boundary — are we excluding feedback from outside it that matters?
- What archetypes are present — fixes that fail, shifting the burden, tragedy of the commons, escalation?

Contraindication:
- DO NOT use when the problem is a simple linear cause-effect that does not involve feedback — systems thinking adds complexity without insight
- DO NOT use when the decision timeframe is too short for feedback loops to matter — a one-shot decision has no dynamics
- Use with caution when the system boundaries are ambiguous — modeling the wrong boundary produces confident but wrong conclusions

Failure mode:
- Becoming too abstract to guide an actual decision.