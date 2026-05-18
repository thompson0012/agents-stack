# Known Collaboration Patterns

A growing catalog of human-AI collaboration patterns observed across domains. Each pattern is domain-independent and includes a trigger signature—what to look for in a conversation to identify it.

---

## Pattern: Progressive Constraint Refinement

**Signature**: Human starts with fuzzy goal → AI outputs framework → Human selects one node → AI deepens → Human challenges a specific detail → AI reveals principle.

**Trigger in conversation**: At least 3 rounds where each human query narrows scope and each AI response increases explanatory depth.

**Domain examples**:
- Design: "how to make beautiful pages" → "design tokens" → "why 11 color steps?"
- Code review: "is this architecture good?" → "error handling strategy" → "why retry vs circuit breaker?"
- Writing: "how to write better docs" → "information hierarchy" → "why 3 levels not 4?"

**AI protocol rule**: When given a broad goal, output a framework with 3-5 labeled categories before giving specific advice.

---

## Pattern: Reframing Response

**Signature**: Human asks a surface-level "what" or "how many" question. AI does not answer directly but redefines the question's frame.

**Trigger in conversation**: AI's first sentence establishes a new mental model rather than answering the question.

**Domain examples**:
- Design: "why 11 color steps?" → reframed as "interfaces are layered spaces, each elevation needs a corresponding shade"
- Engineering: "why microservices?" → reframed as "the real question is about team autonomy boundaries, not service count"
- Product: "which feature first?" → reframed as "the question is about learning risk, not feature priority"

**AI protocol rule**: When a "why" or "how many" question targets a specific detail, answer by revealing the system dynamics that made that detail necessary.

---

## Pattern: Multi-Dimensional Parallel Unfolding

**Signature**: For each topic, AI covers 4-6 independent dimensions simultaneously (what, why, how, mistakes, tools, verification).

**Trigger in conversation**: AI responses use multi-column tables or clearly labeled parallel sections that can be read in any order.

**Domain examples**:
- Design: Every topic covers 是什么/为什么/怎么做/常见错误/工具/检查清单
- Security review: Threat / Impact / Likelihood / Mitigation / Verification
- API design: Endpoint / Purpose / Input / Output / Errors / Rate limit

**AI protocol rule**: For any substantive topic, structure the response so a reader can enter from any dimension. Use parallel sections, not linear narrative.

---

## Pattern: Boundary Definition by Negation

**Signature**: AI defines what something IS by showing what it is NOT, using ❌ vs ✅ contrast pairs.

**Trigger in conversation**: Paired negative/positive examples appear in close proximity.

**Domain examples**:
- Design: ❌ 硬编码色值 vs ✅ 使用 Token 變數
- Code: ❌ `z-index: 9999` vs ✅ `--z-modal: 200`
- Writing: ❌ "click here" vs ✅ "Download report (PDF, 2MB)"

**AI protocol rule**: When defining a rule, always show at least one violation alongside the correct form. The boundary is clearer through contrast.

---

## Pattern: Closure with Openness

**Signature**: AI ends each response by marking what was covered and offering specific paths for the next depth level.

**Trigger in conversation**: Responses end with "需要我進一步展開..." or "Want me to elaborate on..."

**Domain examples**: Universal—appears in any high-quality AI conversation regardless of domain.

**AI protocol rule**: Never end with "hope this helps." End with 2-3 concrete "next step" options that are natural branches from the current topic.

---

## Pattern: Quantified Intuition

**Signature**: AI converts vague qualitative advice into specific numeric constraints.

**Trigger in conversation**: Numbers appear where convention would use adjectives (e.g., "48-80px between sections" not "leave enough space").

**Domain examples**:
- Design: "60-30-10 color ratio" instead of "balance your colors"
- Performance: "LCP < 2.5s" instead of "make it fast"
- Code review: "functions < 50 lines" instead of "keep it short"

**AI protocol rule**: Whenever giving "quality" or "balance" advice, attach a specific number or range. If you don't know the number, say "I recommend measuring this—start with [X-Y] as a hypothesis."

---

## Pattern: Convergence Chain

**Signature**: Each round of the conversation narrows the scope of inquiry while increasing the depth of understanding—forming a downward-spiraling chain rather than a flat Q&A.

**Trigger in conversation**: The domain vocabulary becomes more specific each round (e.g., "design" → "design system" → "design tokens" → "color token semantics").

**Human strategy**: After receiving a framework, pick the ONE node that contains the most counterintuitive detail. Follow it down. Don't branch horizontally.

---

## Pattern: Meta-Reflection Trigger

**Signature**: Human steps back from domain content and asks "what methodology is emerging from this conversation itself?"

**Trigger in conversation**: Questions like "從對話中，你發現了什麼協作方法論？" or "how should I interact with AI differently based on what we just did?"

**AI protocol rule**: When asked for meta-reflection, execute the four-step extraction: (1) identify reframing moments, (2) catalog structural formats, (3) trace convergence chain, (4) abstract to protocol. This is the methodology-extractor skill itself.
