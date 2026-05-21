# Complexity Signals

This reference catalogs patterns of **unnecessary complexity** — code whose cost exceeds its value. These signals are universal: they apply regardless of project scale, domain, language, or product type. Scale (internal_tool / team_service / distributed_product) only affects severity and the burden of proof.

## How to use

For each signal below, ask three questions:

1. **Observation**: Is this signal present in the code?
2. **Problem**: What concrete problem does this code claim to solve?
3. **Evidence**: What proof exists that this problem is real?

If observation = yes, problem = vague, evidence = none → **cut candidate**.

---

## Signal 1: Abstraction Without Consumption

**Pattern**: An interface, abstract class, protocol, or type alias that has only one concrete implementation — and no test double depends on it.

**Why it's harmful**: The abstraction adds indirection (a file, a type definition, a wire-up step) without enabling polymorphism. It costs comprehension without buying extensibility.

**Questions**:
- How many concrete implementations exist **right now**?
- Is there a test that injects a mock/stub through this interface?
- If the answer to both is "1" and "no": the interface is indirection, not abstraction.

**Severity by scale**: 
- `internal_tool`: Almost always cut. Exception: testing a non-trivial external dependency (database, payment gateway).
- `team_service`: Cut unless test doubles are actively used for this interface.
- `distributed_product`: Cut unless the interface has 2+ implementations OR is a documented extension point for external consumers.

---

## Signal 2: Layers Without Distinct Responsibility

**Pattern**: Two or more layers/modules that perform the same operation without adding distinct behavior. The classic form: Facade → UseCase → Service → Repository, where UseCase delegates entirely to Service without transformation, validation, or orchestration.

**Why it's harmful**: Each layer is a hop. The reader must open another file, understand another abstraction, trace another call — to discover that nothing happened.

**Detection**: Trace one operation from entry to work. Count the hops. For each hop: what does this layer do that the next layer doesn't? If the answer is "delegates" or "orchestrates" without naming a specific transformation → the layer is a pass-through.

**Severity by scale**:
- `internal_tool`: 1-2 layers maximum. Cut everything between entry and actual work.
- `team_service`: 2-3 layers if they have distinct, nameable responsibilities.
- `distributed_product`: 3-4 layers justified by team boundaries; still question each.

---

## Signal 3: Future-Proofing Without Trigger

**Pattern**: A design decision justified by a hypothetical future scenario: "we might switch providers," "this could be reused," "the architecture supports adding X later."

**Why it's harmful**: Future-proofing bets complexity now against a scenario that may never arrive. If it doesn't arrive, you paid for nothing — and the complexity accumulated in the meantime resists change.

**Probability test**:
1. Has this scenario ever occurred in this project's history? (not "in general" — in THIS project)
2. Is this scenario a stated requirement from a user or stakeholder?
3. Is there a concrete trigger on the horizon (e.g., contract ending with current provider)?

If "no" to all three: probability is near zero. The future-proofing is YAGNI.

**Severity by scale**:
- `internal_tool`: Probability threshold ~20%. Almost never met for speculative futures.
- `team_service`: ~40%.
- `distributed_product`: ~60%. Still ask — even at this scale, speculation without a trigger is debt.

---

## Signal 4: Pattern Without Problem

**Pattern**: A named design pattern (Repository, Observer, Builder, Strategy, Factory, CQRS, Event Sourcing) present in code without the specific problem that pattern exists to solve.

**Why it's harmful**: Patterns are solutions. Without the problem, they're ceremony. A Repository wrapping an ORM that already provides query methods is not solving a problem — it's duplicating the ORM's interface.

**Detection**: For each pattern found in code:
1. Name the pattern.
2. Name the specific problem it solves — not the generic problem the pattern was designed for, but the concrete pain in THIS codebase.
3. If #2 is "separation of concerns," "best practice," or "extensibility" without a specific scenario → the pattern has no problem.

**Common examples**:
- **Repository** with ORM that already abstracts storage → redundant
- **Factory** for objects with simple constructors → overhead
- **Strategy** with one strategy → indirection
- **Observer** with one subscriber → complexity without benefit
- **CQRS** on CRUD data → reads and writes separated without different models

---

## Signal 5: Configuration Heavier Than Code

**Pattern**: A configuration file, schema, or DSL that's more lines, more complex, or harder to understand than the code it configures.

**Why it's harmful**: Configuration is code that can't be debugged with normal tools. It can't be stepped through, type-checked (usually), or refactored with IDE support. If the config is heavier than the alternative code, it's a net loss.

**Detection**: Compare: the YAML/JSON/TOML config file vs. the equivalent hardcoded constants, a simple dict, or a constructor call. If the config version is longer → it's overhead. If the config version requires a schema definition document → that's overhead too.

**Severity**: Independent of scale. A 200-line YAML for 3 parameters is wrong at any scale.

---

## Signal 6: Modularization Without Coherence

**Pattern**: Files split into units so small that they lose independent meaning. The classic form: one class per file when each class is 20 lines and always imported together.

**Why it's harmful**: File boundaries create cognitive boundaries. Too many small files increases the mental cost of tracing behavior — the reader must assemble the picture from scattered pieces.

**Detection**: For any pair of files, ask:
1. Are they always edited together? (Check git history)
2. Does one make sense without the other?
3. Would merging them create a file that's hard to understand (< ~400 lines)?

If #1 is yes and #2 is no and #3 is no → merge candidate.

**Severity by scale**:
- `internal_tool`: Merge aggressively. 300-400 line single files are fine.
- `team_service`: Merge when files lack independent coherence.
- `distributed_product`: Allow smaller units when team ownership boundaries justify them.

---

## Signal 7: Framework Heavier Than Problem

**Pattern**: A framework, library, or dependency whose learning curve, configuration, constraints, and indirection cost more complexity than it saves. If you can replace it with 50-100 lines of straightforward code, the framework is overhead.

**Why it's harmful**: Frameworks trade learning cost for leverage. When the problem is simple, the trade doesn't pay off — you learn the framework AND solve the problem, when you could have just solved the problem.

**Detection**:
1. What does the framework do that you actually use? (Not what it CAN do — what you USE)
2. How many lines of vanilla code would replicate that subset?
3. How many lines of framework config, glue code, and mental model does it cost?

If #2 < #3, the framework is heavier than the problem.

**Severity**: Independent of scale. DI framework for 5 dependencies is overhead at any scale.

---

## Signal 8: Type Complexity Without Safety Gain

**Pattern**: Complex generics, mapped types, conditional types, or type gymnastics that satisfy the type checker but don't prevent bugs a human would actually make.

**Why it's harmful**: Type systems exist to catch errors. If the type complexity catches only errors that no one makes, it costs readability without buying safety.

**Detection**: For each complex type construct:
1. What specific bug class does it prevent?
2. Has this bug class ever occurred in this project?
3. Would a simpler type (or `any` with a runtime check) be sufficient?

If #1 is vague and #2 is no → the type is safety theater.

**Severity**: Independent of scale.

---

## Signal 9: Asynchrony Without Concurrency

**Pattern**: async/await, Promises, event loops, message queues, or job systems used for flows that are inherently sequential — where B cannot start until A finishes.

**Why it's harmful**: Async code is harder to reason about, debug, and test than sync code. If the flow is sequential, async adds complexity without buying parallelism.

**Detection**: For each async boundary:
1. Is there actual concurrent work happening? (Two things running at the same time)
2. If not, would a synchronous version be simpler AND functionally equivalent?

**Severity**: Independent of scale. A queue for a single background job that runs immediately is overhead.

---

## Signal 10: Error Handling Without Recovery

**Pattern**: Custom error classes, error wrapping chains, error taxonomies, and structured error responses — when every error path ends in "log and return 500."

**Why it's harmful**: Error handling that doesn't enable different recovery behavior is ceremony. If all errors are treated identically, one error type is enough.

**Detection**: For each error class or handling layer:
1. Is there code that branches on this specific error type?
2. Is there different recovery behavior for different error types?
3. If no to both → the error differentiation has no consumer.

**Severity**: Independent of scale.

---

## Signal 11: Documentation Longer Than Comprehension

**Pattern**: Architecture documents, design specs, READMEs, or diagrams that take longer to read than the code they describe.

**Why it's harmful**: Documentation that's heavier than the code it documents has inverted the relationship. The docs should make the code faster to understand, not be a second codebase to maintain.

**Detection**: Compare: reading the design doc vs. reading the entry point and tracing the call path. If the doc takes longer → the code might already be clear enough, or the doc is over-documenting.

**Severity**: A design doc growing from 500 to 1400 lines while the core behavior hasn't changed → strong signal of over-engineering in the design process itself.

---

## Using These Signals in Reviews

### For spec phase
When forming requirements, scan the proposed approach for these signals. If the approach triggers 3+ signals without strong evidence → the spec needs simplification before it is ready for planning.

### For plan phase
Scan the plan scope for these signals. A plan that triggers multiple signals at once (e.g., Repository + Factory + async queue for a simple CRUD endpoint) defines over-engineered scope.

### For prune-review
These signals are the primary detection framework. Scale context modifies severity but doesn't replace signal detection. Answer: "Which signals are present? Where? What's the evidence the code they add is earning its keep?"
