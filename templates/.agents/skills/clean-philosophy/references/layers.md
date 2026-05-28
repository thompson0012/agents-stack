# Cross-Level Layer Map

> Clean 哲學是 fractal 的 — 同一種思考模式在不同層次以不同形式重複出現。

## The Fractal Pattern

每一層的 Clean 哲學都共享這個結構：

```
┌──────────────────────────────────────────────┐
│  1. IDENTIFY what is essential               │
│     (What has enduring value?)               │
├──────────────────────────────────────────────┤
│  2. PROTECT it from the transient            │
│     (What changes around it?)                │
├──────────────────────────────────────────────┤
│  3. REMOVE everything else                   │
│     (What doesn't serve the essential?)      │
└──────────────────────────────────────────────┘
```

---

## The Seven Levels

### Level 1: Code (Clean Code)

| Step | Application |
|---|---|
| **Identify essential** | Business logic, intent, domain concepts |
| **Protect from transient** | Naming reveals intent; IO/UI isolated; tests guard behavior |
| **Remove everything else** | Dead code, duplicate logic, magic numbers, unnecessary comments, speculative parameters |

**Key principle:** *Readability > cleverness.* Code is read ~10x more than written.

### Level 2: Module / Component (Clean Architecture — component principles)

| Step | Application |
|---|---|
| **Identify essential** | Stable abstractions, interfaces that define contracts |
| **Protect from transient** | DIP: inner layers define interfaces, outer layers implement; dependencies point inward |
| **Remove everything else** | Interfaces with one implementation (unless test seam), cycles in dependency graph, unstable components at the center |

**Key principle:** *The stability of a component determines where it sits in the dependency graph.*

### Level 3: System (Clean Architecture — layers)

| Step | Application |
|---|---|
| **Identify essential** | Business rules (entities, use cases) — the policy that makes the business money |
| **Protect from transient** | Concentric layers: policy in the center, frameworks/DB/UI at the edges; Dependency Rule enforces isolation |
| **Remove everything else** | Pass-through layers, premature boundaries, empty abstractions, premature framework integration |

**Key principle:** *A good architecture maximizes the number of decisions not made.*

### Level 4: Process (Clean Agile)

| Step | Application |
|---|---|
| **Identify essential** | Working software delivered to users, feedback loops |
| **Protect from transient** | Fixed iteration cadence; TDD ensures quality doesn't degrade; business-value ordering protects from technical gold-plating |
| **Remove everything else** | Ceremonies that don't accelerate delivery (overgrown standups, estimation theater, pointless status reports) |

**Key principle:** *People and interactions over processes and tools.* The process serves the team, not the other way around.

### Level 5: Practitioner (The Clean Coder / Clean Craftsmanship)

| Step | Application |
|---|---|
| **Identify essential** | Professional integrity: shipping working code, honest communication, continuous learning |
| **Protect from transient** | Say no when needed; estimation with ranges (not single points); TDD as a safety net; QA as non-negotiable |
| **Remove everything else** | Blame culture, heroic overtime, fear-based decisions, avoidance of uncomfortable truths |

**Key principle:** *Professionalism is taking responsibility for the outcome, not just the output.*

### Level 6: API (Clean API)

| Step | Application |
|---|---|
| **Identify essential** | Resources the consumer needs, operations on those resources |
| **Protect from transient** | Nouns not verbs; flat over nested; correct HTTP semantics; consistent naming conventions |
| **Remove everything else** | Internal implementation details leaked into responses, unnecessary nesting, inconsistent formats, missing documentation |

**Key principle:** *A clean API tells the consumer what they can do, not how the server is built.*

### Level 7: UI (Clean Design)

| Step | Application |
|---|---|
| **Identify essential** | Content, information hierarchy, user tasks |
| **Protect from transient** | Two fonts max; 1-2 primary colors; grid-based alignment; consistent spacing system |
| **Remove everything else** | Decorative elements without purpose, excessive colors, mismatched animations, unclear microcopy |

**Key principle:** *Good design is invisible. Bad design screams for attention.*

---

## Fractal Equivalence Table

同一條 Micro-principle 在各層的應用：

| Micro-principle | Code | Module | System | Process | Practitioner | API | UI |
|---|---|---|---|---|---|---|---|
| **SRP: one reason to change** | One function does one thing | One component serves one actor | One layer isolates one concern | One ceremony solves one problem | One commitment means one thing | One endpoint has one resource | One element has one purpose |
| **DIP: depend on abstractions** | Interface injection | Inner layer defines interface | Dependency Rule | Process depends on team, not software | Decisions depend on evidence, not authority | Consumer depends on contract, not implementation | Content depends on grid, not device |
| **DRY: one representation** | No copy-paste code | No duplicated interface contracts | No policy duplicated across layers | No tracking same info in two systems | No saying different things to different people | No same data in two formats | No repeated design tokens |
| **Minimalism: delete > add** | Remove dead code | Remove unused interfaces | Remove pass-through layers | Remove unproven ceremonies | Remove fear-based policies | Remove unused endpoints | Remove decorative pixels |
| **OCP: open for extension** | Strategy pattern | Plugin architecture | Replace outer layer without touching inner | Add iteration without changing process | Add skill without changing ethics | Add field without breaking consumers | Add theme without changing content |

---

## How Levels Interact

```
Higher abstraction
       │
       ▼
   UI ──── Content over decoration
   API ──── Consumer over implementation
   Practitioner ──── Integrity over comfort
   Process ──── Delivery over ceremony
   System ──── Policy over detail
   Module ──── Stable over volatile
   Code ──── Readable over clever
       ▲
       │
Lower abstraction (more concrete)
```

**Conflict resolution:** When a rule at one level contradicts another,
the **higher** level wins. Example: A Clean Architecture principle
(Level 3: separate business rules from framework) should NOT be overridden
by a Clean Code principle (Level 1: extract tiny functions) if the latter
would create so many indirections that the architecture's intent is lost.

Similarly, Practitioner "say no" (Level 5) can override Process "ship on
schedule" (Level 4) if shipping on time would mean shipping knowingly
broken software.
