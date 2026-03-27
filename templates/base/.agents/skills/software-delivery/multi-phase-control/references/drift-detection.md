# Drift Detection

How to detect and handle drift from original intent in multi-phase work.

## What Is Drift?

Drift occurs when the current implementation diverges from the original objective without explicit acknowledgment or user acceptance.

Types of drift:

| Type | Example |
|------|---------|
| Scope drift | "We added OAuth because it seemed useful" |
| Priority drift | "Phase 2 became more urgent than Phase 1" |
| Interpretation drift | Original objective was vague, implementation chose wrong interpretation |
| Context loss drift | Session reset, agent forgot original constraints |
| Accumulation drift | Small changes compound without visibility |

## Early Detection Signals

Watch for these drift indicators:

| Signal | What It Means |
|--------|---------------|
| "I'll just also..." | Scope expansion without explicit approval |
| "Actually, let's..." | Direction change without logging |
| File edits outside touched files | Work spilling beyond tracked scope |
| "That's basically done" | Exit criteria not actually verified |
| "I remember we said..." | Relying on memory, not docs |
| "Let me also fix..." | Work expanding beyond phase definition |

## Drift Log Pattern

Every `current-focus.md` should have a drift log:

```markdown
## Drift Log
| Date | Original | Current | Reason | Accepted By |
|------|----------|---------|--------|-------------|
| 2024-03-27 | "Build REST API" | "Add OAuth to REST API" | User requested addition | User (conversation) |
| 2024-03-28 | "Phase 1: Auth" | "Phase 1: Auth + MFA" | MFA was in scope, just not explicit | Implicit |
```

Rules:
- Log any change to objective, scope, or prioritization
- Include why the change happened
- Record who accepted it (user, agent assumption, external requirement)
- Make implicit decisions explicit

## Drift Prevention Patterns

### 1. Preserve Original Verbatim

Record original objective word-for-word from source:

```markdown
## Original Objective
Build a REST API for user management with CRUD operations.
```

NOT paraphrased:
```markdown
## Original Objective
API for users (CRUD).  # Paraphrased, loses precision
```

### 2. Track Current Focus Separately

```markdown
## Original Objective
Build REST API for user management with CRUD operations.

## Current Focus
Building OAuth integration for REST API.

## Drift Explanation
User requested OAuth addition in [conversation link].
```

If original ≠ current, explanation is required.

### 3. Read Before Acting

At session start:
1. Read `current-focus.md` for original objective
2. Read `progress.md` for current state
3. Check drift log for recent changes
4. Confirm current focus aligns with original OR explicit reason exists

### 4. Update on Change

When scope changes:
1. Add entry to drift log
2. Update current focus
3. Get explicit user acceptance for significant changes
4. Update `progress.md` with what changed and why

### 5. Gate Against Drift

Phase exit criteria should include:
- "All work matches current focus"
- "No unlogged scope changes"

## Drift Recovery

When drift is detected:

1. **Stop implementation** — Do not continue on drifted path
2. **Document drift** — Add to drift log with explanation
3. **Confirm with user** — For significant drift, get explicit acceptance
4. **Update or rollback** — Either accept drift (update current focus) or revert to original
5. **Resume with clarity** — Clear direction from accepted state

## Drift vs. Legitimate Change

| Legitimate Change | Drift |
|-------------------|-------|
| User explicitly requests addition | Agent adds "because it's better" |
| Logged in drift log with reason | Not recorded anywhere |
| Current focus updated | Current focus unchanged, work diverged |
| User accepts or agent escalates | Assumed user would want it |
| Entry/exit criteria updated | Gates ignored or redefined implicitly |

## Questions to Ask Before Drifting

- Is this in scope? (Check `current-focus.md`)
- Is this in current focus? (Not just original objective)
- Would user explicitly approve this?
- Is this phase exit criteria still valid?
- Should this be a new phase instead of scope expansion?

If any answer is unclear, **stop and log** before continuing.