---
name: clean-philosophy
description: Use when designing APIs, making architectural decisions, adding features, writing code, code review, UI design, process design, or any design decision. Provides a cross-level (code → system → process → practitioner → UI → API) simplification discipline: identify what is essential, protect it from the transient, remove everything else.
version: 2.0.0
---

# Clean Philosophy

> 化繁為簡 — 在每一個層次上，刪到不能再刪，然後停止。

這套哲學適用於 code、architecture、process、UI、API、以及 practitioner 自身行為。
它不告訴你「該做什麼」，而是告訴你「什麼不該做」——因為品質是刪出來的。

## Cross-Level Map

Clean 哲學是 fractal 的。同一條原則在不同層次有不同的實作：

| Level | You're cleaning | Core question | Clean counterpart |
|---|---|---|---|
| **Code** | Functions, classes, names | 這段程式碼的意圖明顯嗎？我可以在不執行的情況下讀懂它嗎？ | Clean Code |
| **Module / Component** | Dependencies, interfaces | 誰變動快、誰變動慢？依賴方向跟變動方向一致嗎？ | Clean Architecture (component) |
| **System** | Layers, boundaries | 政策有沒有被細節汙染？換一個框架要動多少檔案？ | Clean Architecture (layer) |
| **Process** | Iterations, ceremonies | 這個流程證明過自己加速了交付嗎？如果明天刪掉它，誰會發現？ | Clean Agile |
| **Practitioner** | Habits, decisions, communication | 你是在解決問題還是繞過問題？你能不能對不合理的要求說不？ | Clean Coder / Clean Craftsmanship |
| **API** | Endpoints, data structures | consumer 拿到的是不是比他們需要的少？格式有揭露實作細節嗎？ | Clean API |
| **UI** | Elements, layout, color | 使用者第一眼看到的是內容還是裝飾？每一個像素傳遞了資訊嗎？ | Clean Design |

See [references/layers.md](references/layers.md) for the detailed fractal pattern explanation.

## Core Rules

### One Rule Per Level

| # | Level | Rule |
|---|---|---|
| 1 | **Code** | **Useful > Correct.** 最正確的抽象如果沒人用得起來就是錯的。 |
| 2 | **Module** | **Dependencies point toward stability.** 依賴方向必須和變動方向相反。 |
| 3 | **System** | **Policy isolated from detail.** 業務規則不認識框架、資料庫、UI。 |
| 4 | **Process** | **Value delivery > Ceremony.** 任何流程步驟如果無法證明它加速了交付，刪掉它。 |
| 5 | **Practitioner** | **Say no when the ask violates a principle.** 說不是保護原則，不是不配合。 |
| 6 | **API** | **Consumer > Implementation.** Endpoint 反映使用情境，不是資料庫表格。 |
| 7 | **UI** | **Content > Decoration.** 使用者來這裡是為了內容，不是為了漸層陰影。 |

### Cross-level resolution

If a rule at a **higher level** conflicts with a rule at a **lower level**,
the higher-level rule wins. Example: Practitioner "say no" can override Code
"make it small" if the ask would produce a fragmented mess. The levels
in the table above are ordered bottom-to-top — Code is lowest, UI is highest.

## Quick Check (Before Every Decision)

Answer these four questions before committing any design decision:

1. **Consumer first** — 誰在用這個？他們想寫/想看到的東西長什麼樣？
2. **Concrete case** — 哪一個真實的使用案例需要這個？(Not "might need", not "X has this")
3. **Level discipline** — 能不能用更低層級解決？(parameter > method > class > module > new layer > new process > new principle)
4. **Negation** — 加上這個之後，我可以刪掉什麼？

## Decision Tree

```
Adding something?
├─ Does a concrete use case exist? ──NO──→ Don't add
├─ Can existing API handle it? ──YES──→ Don't add
├─ Can it be a parameter instead of a method? ──YES──→ Add parameter
├─ Can it be a method instead of a class? ──YES──→ Add method
├─ Can it be a class instead of a module? ──YES──→ Add class
├─ Can it be a module instead of a new layer? ──YES──→ Add module
├─ Does a higher-level rule forbid this? ──YES──→ Say no (Practitioner rule #5)
└─ None of the above ──→ Consider adding (review negation: what can you delete?)

Keeping something around?
├─ Is it tested through a real use case? ──NO──→ Delete it
├─ Does it have only one implementation? ──YES──→ Inline it (unless the interface isolates a known volatile dependency)
├─ Would the user notice if it disappeared? ──NO──→ Delete it
├─ Does it violate a higher-level principle? ──YES──→ Fix or remove it
└─ None of the above ──→ Keep it (for now)

Making a decision that affects others?
├─ Are you certain the evidence supports it? ──NO──→ Say it's uncertain (range + confidence)
├─ Does the other stakeholder understand the tradeoffs? ──NO──→ Explain in business terms
└─ None of the above ──→ Proceed with confidence
```

## Detailed Principles

See [references/principles.md](references/principles.md) for the full set of principles across design thinking, architecture, decision discipline, debuggability, performance, professionalism, process, and UI/API.

## Anti-Patterns

See [references/anti-patterns.md](references/anti-patterns.md) for patterns to actively avoid, with cross-level examples.

## Execution Mode

When this skill is active:

1. **Before writing code** — run the four quick-check questions
2. **Before designing API / UI / process** — run the same four questions
3. **After writing code** — scan for removable code, unused abstractions, unnecessary indirection
4. **During review** — ask: "What was added, and what can be removed?"
5. **When process grows** — ask: "Does this ceremony accelerate delivery?"
6. **When documentation grows** — ask why. Good design shrinks documentation.
