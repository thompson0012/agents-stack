---
name: methodology-extractor
description: Use when the user asks to extract human-AI collaboration methodology from a conversation—questions like "what methodology emerged from this conversation", "how do I replicate this collaboration quality", or "extract the interaction patterns and protocols that made this dialogue effective across domains."
version: 0.1.0
---

# Methodology Extractor

Extract reusable human-AI collaboration patterns from any domain conversation. The output is a **protocol**—a set of behavioral rules an AI can follow to replicate the collaboration quality, independent of the original domain.

## Core Contract

- **Input**: A conversation transcript between human and AI (any domain).
- **Output**: A structured methodology consisting of (a) identified collaboration patterns, (b) the structural formats the AI used to organize knowledge, (c) the human's questioning strategy that triggered depth, and (d) a domain-independent protocol that can be injected into future AI sessions.
- **Constraint**: The extraction must be based on **observable structural features** of the conversation, not subjective quality judgments.
- **Non-negotiable**: Never extract methodology from a single exchange. Only extract when the conversation shows a **progressive deepening arc** (at least 3 rounds of follow-up that increase precision).

## Workflow

### Phase 1 — Verify Extractability

Before extraction, confirm the conversation meets these criteria:

- [ ] At least 3 rounds of human-AI exchange
- [ ] At least one "why" question that forced AI to explain reasoning, not just provide information
- [ ] The AI's responses show structural organization (tables, frameworks, checklists, decision trees), not just prose paragraphs
- [ ] The conversation exhibits a **convergence pattern**: scope narrows while depth increases

If any criterion fails, inform the user that the conversation lacks sufficient signal for methodology extraction, and explain which criterion is unmet.

### Phase 2 — Four-Step Extraction

Execute all four steps. Each step produces output that feeds the next.

#### Step 1: Identify Reframing Moments

Find every point where the AI **did not answer the surface question** but instead **redefined the question** to reveal a deeper frame.

**How to identify**: Look for exchanges where:
- The AI's first sentence does not start by answering "what" but by establishing a new mental model
- The AI uses phrases like "本質上是..." (essentially...), "核心是..." (at its core...), "不是 X 而是 Y" (not X but Y)
- The answer would be valid even if the original question's domain changed

**Output for each reframing moment**:
```
| 人類問 | AI 沒有回答 | AI 重構為 | 重構機制 |
|--------|-----------|----------|---------|
| [surface question] | [what AI avoided saying] | [new frame] | [why this reframe works] |
```

Each reframing moment is a candidate for a cross-domain pattern.

#### Step 2: Extract Structural Formats

Catalog every **non-prose organizational structure** the AI used. Ignore content; focus on form.

| Format | Observed Instances | Cognitive Function |
|--------|-------------------|-------------------|
| Layered tables (3+ columns) | count | Splits concerns into independent dimensions |
| ❌ vs ✅ contrast pairs | count | Defines boundaries through negation |
| Decision trees | count | Makes implicit judgments explicit |
| Phase/step workflows | count | Reveals temporal dependencies |
| Dimension parallel tables (是什么/为什么/怎么做...) | count | Provides multi-entry understanding paths |
| Checklists | count | Converts abstract standards to actionable items |
| Ratio rules (60-30-10, 80/20) | count | Quantifies "feels right" into operational constraints |

**This catalog is the reusable toolkit.** Each format can be prescribed to future AI interactions as an output requirement.

#### Step 3: Trace the Convergence Chain

Map the human's questioning trajectory. The goal is to identify **what questioning strategy** produced the deepening effect.

**Draw the chain**:
```
Round 1: Broad goal → AI gives framework
  └→ Human selects node X from framework
Round 2: Deepen on node X → AI gives sub-framework
  └→ Human challenges specific detail Y ("why this number?")
Round 3: AI reveals principle behind Y → Human asks "what other principles?"
  └→ Human asks for meta-rules
Round 4: AI extracts golden rules → Human tests boundary conditions
  └→ Human asks "does this apply to industry Z?"
...
```

**Extract the questioning strategy**:
- What triggered AI to switch from "information delivery" to "principle explanation"? (Typically: "why" questions targeting a specific, counterintuitive detail)
- What triggered AI to extract meta-rules? (Typically: "what are the general principles behind all these specifics?")
- What triggered AI to map to contexts? (Typically: "does this apply to X?" where X is a boundary case)

**Output**: A set of **trigger questions** that any human can use to deepen any AI conversation.

#### Step 4: Abstract to Protocol

Synthesize Steps 1-3 into a **domain-independent collaboration protocol**.

A protocol has three parts:

**Part A: AI Behavioral Rules** — instructions you would give to another AI to replicate the response quality:
```
1. When given a broad goal, first output a classification framework (3-5 categories). Do not start with specific answers.
2. For each topic, cover six dimensions: what / why / how / common mistakes / tools / verification checklist.
3. End every response with 2-3 specific "next step" options.
4. When the human asks "why" about a specific number or rule, answer with the underlying principle, not the surface justification.
5. Use ❌ vs ✅ contrast pairs to define boundaries of rules.
6. Quantify vague advice: never say "leave enough space"; say "use 48-80px between unrelated sections."
```

**Part B: Human Questioning Strategy** — instructions for the human to maximize depth:
```
1. Start with a fuzzy goal. Accept the framework. Select ONE node to deepen.
2. Within that node, find the most counterintuitive detail. Ask "why this number/specific?"
3. After receiving principles, ask "what other rules exist at this level?"
4. Test the rules: "does this apply to [boundary case]?"
5. Final round: "how do I verify this is correct?"
```

**Part C: Domain-Specific → Domain-Independent Mapping** — show how the original domain patterns translate:
```
[Original domain concept] → [Generalized pattern] → [How to apply in new domain]
```

### Phase 3 — Validate the Extraction

After producing the methodology, run these checks:

1. **Domain substitution test**: Replace all domain-specific terms with placeholders. Does the methodology still make sense?
2. **Reversibility test**: Could you give the extracted protocol to a fresh AI and have it reproduce the conversation quality?
3. **Completeness test**: Does the protocol cover both AI behavior rules AND human questioning strategy? If only one side, it's incomplete.

### Phase 4 — Output Format

Structure the final output as:

```markdown
## Extracted Methodology: [One-line summary]

### Reframing Moments Discovered
[Table from Step 1]

### Structural Format Catalog
[Table from Step 2]

### Convergence Chain & Questioning Strategy
[Diagram + trigger question set from Step 3]

### Reusable Collaboration Protocol
[Part A: AI rules, Part B: Human strategy, Part C: Domain mapping from Step 4]

### Validation
[Results of domain substitution, reversibility, and completeness tests]
```

## When NOT to Use

- Single-exchange Q&A with no follow-up
- Conversations where AI only provided facts, no frameworks
- Conversations where the human asked only "what" questions, never "why"
- Conversations shorter than 3 rounds of exchange

## References

- [patterns.md](references/patterns.md) — Catalog of known collaboration patterns with examples across domains
- [protocol-template.md](references/protocol-template.md) — Blank template for the final protocol output
