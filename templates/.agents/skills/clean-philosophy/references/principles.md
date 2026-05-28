# Principles

> This file contains the full body of each principle. SKILL.md keeps the
> quick-reference version; this is the authoritative reference for when
> deeper justification is needed.

---

## Design Thinking

### 1. Start from consumer, not from capability

```
❌ Ask: What features should the system support?
✅ Ask: What code does the user want to write?
      What API response does the consumer want to read?
      What UI would the user want to interact with?
```

**Execution rule:** Write caller-side code first. Only change the system when
that code doesn't work. Don't design outward from system capabilities.

**Cross-level application:**
- Code: write the function call before implementing the function
- API: design the request/response contract before implementing the endpoint
- UI: sketch the layout before wiring the data
- Process: define the expected outcome before designing the steps

### 2. Add only with a concrete instance; don't guess

Every addition must correspond to a **specific, concrete use case that cannot
be achieved with the existing API**.

```
Don't add:
- "Might need this in the future"
- "Framework X has this pattern so we should too"
- "It feels more complete this way"
```

Guessed requirements are not requirements.

**Why guessing fails:** Every abstraction is a map that selects some details
and omits others. Without a concrete consumer, you don't know which details
matter. The abstraction becomes a map of a territory you've never visited —
it's as likely to mislead as to help. "Make it generic" without two concrete
examples is building a bridge to nowhere.

### 3. Add at the lowest level, not the highest

Fix the gap where you find it. Order of preference:

```
one parameter > one method > one class > one module > one new layer > one new process
```

**Abstraction threshold test:** Before adding a formal abstraction (interface,
new class, new module), run this triage:

| Question | If yes | If no |
|---|---|---|
| Do multiple implementations exist or are concretely planned? | Add abstraction | Keep concrete |
| Does this code need polymorphism (behavior varies by type)? | Add abstraction | Keep concrete |
| Is a test seam genuinely required? | Add abstraction | Keep concrete |

If all three are "no," the abstraction is speculative — delete it or don't
create it.

### 4. Invest proportionally to change frequency

Architectural complexity is a hedge against future change. The question isn't
"is this abstract enough?" but "how often does this change?"

| Change profile | How to treat it |
|---|---|
| **High volatility + high criticality** | Full isolation: interface, bounded context, high test coverage |
| **Low volatility + low criticality** | Keep simple: no ceremony, concrete types, minimal tests |
| **Unknown volatility** | Keep simple until proven otherwise. Let the code tell you it changes often before you invest in protecting it. |

Apply this *before* deciding which layers or abstractions a component needs.
The same codebase should have high-ceremony hotspots and low-ceremony stable
zones — uniformity is a smell.

**Cross-level application:**
- Code: stable business logic gets more test coverage; volatile glue code gets less ceremony
- Architecture: stable domain needs isolation; experimental features stay simple
- Process: established delivery pipeline needs optimization; new process ideas stay lightweight
- API: core resources get full spec; experimental endpoints get minimal doc

### 5. System provides primitives; doesn't compose for the user

Give the fewest possible fundamental building blocks. Let the user compose
them. Don't predict how the user will compose.

**Cross-level application:**
- Code: provide `map`, `filter`, `reduce` — not `transformUsers`, `transformOrders`, etc.
- API: provide `/products`, `/orders` — not `/bulk-export-csv`, `/monthly-report-pdf`
- UI: provide layout primitives, not pre-built page templates for every case
- Architecture: provide plugin hooks, not a predefined plugin catalog

### 6. One line of working code > a page of design doc

Evidence is not "Book X says we need Y." Evidence is "This code doesn't work
because Y is missing."

**Corollary:** A prototype that works is worth more than a specification that
covers every edge case — because the prototype will reveal edge cases the
spec missed.

---

## Architecture Principles

### 7. Core is minimal and never bloats

The core does exactly one thing. All advanced capabilities hang off the core.
Core growing = direction is wrong.

**Litmus test:** Can a developer replace any non-core component without
modifying the kernel? If the answer is "no" for any component, the boundary
between core and protocol is wrong.

**Deciding what goes in core:** Core ≠ Domain. Core = what changes least
often. Volatile business logic needs isolation but doesn't belong in the
"core" — it needs its own bounded context with high test coverage. Stable
infrastructure (data types that have settled, utility functions, established
protocols) belongs in or near the core. Ask: "Would changing this break
everything, or would changing everything break this?" The answer tells you
whether it's core or satellite.

### 8. Plugins mount at timing points, not as subsystems

- Define fixed execution timing points (hooks)
- Plugins declare which point they care about; they don't control when they
  execute
- No plugin management framework
- No plugin registry

This is the architectural embodiment of the **Dependency Polarity Rule**:
the core defines the contract (timing points), plugins implement it.
Dependencies point inward.

### 9. One structure, many purposes

Don't build different subsystems for different problems. Find a unified data
structure that solves multiple needs simultaneously.

One less structure = one less category of synchronization bugs.

**Split boundary:** When a new use case requires twisting the core structure's
semantics to work, that's when to split. Preserving structural semantics >
minimizing structural count.

### 10. Code = configuration

Internal tools don't need a configuration system. Declarative API beats
YAML / JSON / env-var assembly.

**Why:** Configuration adds a layer of indirection that bypasses static
analysis, type checking, and tests. Every configuration point is a decision
deferred to runtime, where it's harder to verify. If you can express the same
variation in code, do it there — the compiler becomes your test.

---

## Decision Discipline

### 11. Evidence threshold

Every removed feature has explicit "bring it back" conditions: how many use
cases, how many users, what pain point. Not "never add it." Means "add it
when there's evidence."

**Testing corollary:** Tests that exercise deprecated paths are safety nets,
not evidence. When validating a new architecture, every test must exercise
the new API surface. Backward-compat tests prove nothing was broken;
kernel-native tests prove the new design actually works.

### 12. Review must include a "cut" step

Reviews default to addition. Finding "what's missing" is easier than finding
"what's extra."

**After every review, ask:**
- What was added?
- What can be removed?

### 13. AI adds; humans subtract

AI tends toward over-design, pattern-mapping, and not cleaning up. The
human's core value isn't generating more design — it's judging which designs
shouldn't exist.

**AI behavior rules:**
- After writing code, actively check for removable code, files, abstraction
  layers
- Don't keep unused code for "completeness"
- Don't introduce indirection layers "that might be useful later"
- Run the Quick Check from SKILL.md before finalizing any output

### 14. Docs growing = direction is wrong

Good design makes documentation shorter. If docs grow after every iteration,
stop and ask why.

**Corollary:** Adding a FAQ section to your docs means something in the
design isn't intuitive enough. Fix the design, not the docs.

### 15. Deprecation must allow gradual migration

Breaking changes must let old and new coexist for at least one version cycle.
User code shouldn't break all at once.

Every deprecated symbol must carry a scheduled removal version:
`@deprecated(since="0.2", remove_in="0.4")`. Without a removal target,
deprecated code becomes permanent dead weight. Backward compatibility is a
safety net, not a storage room.

---

## Debuggability

### 16. System must make failure causes obvious

A failing composition must produce an error message that points to the
specific primitive.

```
❌ "Something went wrong"
✅ "createUser() failed: email already exists (user_service.go:42)"
```

In a minimal system, user code is composed. If the system doesn't tell you
which primitive failed and why, debugging cost turns "give primitives, let
users compose" into punishment.

**Cross-level application:**
- Code: error messages identify the exact call, not just the function
- API: error responses include the specific field that failed validation
- UI: error states explain what went wrong and what the user can do about it
- Process: failure notifications point to the exact step that failed

---

## Performance Boundary

### 17. Naive compositions shouldn't cause orders-of-magnitude performance penalties

If a common composition pattern is more than 3x slower than a hand-rolled
solution, the system should provide a more efficient composition path rather
than forcing users to bypass the system.

---

## Professionalism (from Clean Coder)

### 18. Say no when the ask violates a principle

Agent must be able to push back when a request would produce a violation:

```
User: "Make this function 20 lines shorter by inlining the dependency."
Agent: "That would violate the Dependency Polarity Rule — the business
logic would then directly depend on the database driver, making it
untestable without infrastructure. Instead, I can make the interface
smaller while preserving the boundary."
```

**When to say no:**
- When the request would make the system harder to change than easier
- When the request would introduce a known anti-pattern
- When the request promises "we'll fix it later" (Clean Craftsmanship:
  "later" is a lie)
- When the request asks for an estimate that is dishonest (too optimistic)

**How to say no:**
1. State the principle being violated
2. Explain the consequence in concrete terms (not abstract)
3. Offer an alternative that satisfies the underlying need
4. Let the human make the final decision — but the default answer to
   "ship knowingly broken code" is no.

### 19. Quality bar is non-negotiable

Never ship knowingly broken software. "We'll fix it in the next release" is a
debt that compounds with interest.

**Core disciplines (from Clean Craftsmanship):**
- TDD: tests before code. Not negotiable for production systems.
- Refactoring: leave code cleaner than you found it.
- Simple design: the smallest design that passes the tests.
- Collaborative programming: review before merge (pair or asynchronous).
- Acceptance tests: define "done" objectively, not by opinion.

**What this means for an agent:**
- If you detect a bug during implementation, fix it — don't log it for later
- If the code is too messy to understand, refactor before adding the feature
- If tests are missing, add them — don't assume someone else will
- If a requirement is contradictory, flag it — don't implement the least
  contradictory interpretation

---

## Process (from Clean Agile)

### 20. Process must prove its value

Every ceremony (standup, retro, estimation, planning, review) must have
demonstrable evidence that it accelerates delivery. If it can't or doesn't,
remove it.

**Evidence threshold examples:**
- **Standup:** if blockers are resolved without standup and coordination
  happens async, drop standup
- **Estimation:** if estimates are consistently wrong and never used for
  decision-making, drop estimation
- **Retro:** if action items from retro are never executed, drop retro

**The litmus test:** "If I deleted this process step tomorrow, would anyone
notice within a week?"

---

## UI / API (from Clean Design + Clean API)

### 21. Content over ornament

Every visual element's reason for existence is to communicate information.
If it doesn't communicate, remove it.

**Clean Design principles:**
- **White space:** breathability over density. Don't fill all the space.
- **Two fonts max:** one for headings, one for body. Everything else is
  visual noise.
- **Limited color palette:** 1-2 primary colors, a few purposeful neutrals.
- **Alignment:** grid-based, intentional. Every element should have a reason
  for its position.
- **Consistency:** same animation timing, same visual language across the
  entire surface.

### 22. Consumer over implementation

An API reflects the consumer's use case, not the implementer's schema.

**Clean API principles:**
- **Flat over nested:** avoid deep response structures
- **Nouns not verbs:** `/users` not `/getUsers`
- **Plural names for collections:** `/orders` not `/order`
- **Correct HTTP status codes:** never use `200` for everything
- **Consistent naming:** pick kebab-case or snake_case, stick to it
- **Always document it:** a clean API with no docs is still unusable
