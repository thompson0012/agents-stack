# GUIDELINES.md — How to Write & Think Like an AI Agent

> **Status**: TEMPLATE  
> **Purpose**: Teaching guide for AI documentation and code thinking

This document teaches **how to think** and **how to write** effective documentation. Follow it sequentially like a tutorial, or jump to specific sections as needed.

---

## Part 1: The AI Mindset

### How AI Should Think

**1. Evidence First, Inference Second**
```
❌ Bad: "The API probably uses REST"
✅ Good: "The API uses REST (evidenced by routes in /src/routes/*.ts)"
```

Always ground claims in:
- Code you can see (file contents, structure)
- Explicit user statements
- Project documents marked `STATUS: PRODUCTION`

**2. Explicit Over Implicit**
```
❌ Bad: "Use the standard pattern"
✅ Good: "Use the repository pattern (see UserRepository in src/repos/)"
```

Name the specific thing. Don't assume shared context.

**3. Questions Over Assumptions**
```
❌ Bad: (implements based on guess)
✅ Good: 
ASSUMPTIONS:
- This uses PostgreSQL (correct if wrong)
- Auth is JWT-based (confirm?)
```

State what you're assuming so it can be corrected.

---

### 4. Structure Over Prompting

When AI is powerful, **quality depends on the system you build around it**, not the cleverness of a single prompt.
Treat AI as a **team member with tools**, and organize the work so it can operate safely and verify its results.

**Four workflow layers (outer → inner):**

| Layer | What it does | Why it matters |
|------|-------------|----------------|
| **Parallelize** | Run multiple agents in parallel on independent tasks | Turns AI from a “chat partner” into scalable compute |
| **Persist Rules** | Keep a shared rules file (e.g., CLAUDE.md) that captures mistakes and preferences | Errors compound into improvements over time |
| **Plan First** | Require a plan before execution; iterate on plan until aligned | Prevents costly rewrites and misalignment |
| **Verify Loops** | Always verify with tests, scripts, or UI checks | Feedback loops multiply quality |

**Minimum viable workflow (apply to any task):**
- Split work into parallel subtasks when independent
- Write/maintain project rules in a shared file
- Ask for a plan before edits begin
- Run verification after changes (tests, lint, build, manual check)

**Automation accelerators (optional):**
- **Slash commands** for repeated workflows (e.g., commit → push → PR)
- **Subagents** for follow-up tasks (review, simplify, verify)
- **Hooks** to auto-format or run checks post-edit
- **Permissions** to pre-authorize safe commands
- **MCP tools** to connect logs/metrics and close the feedback loop

> **Sources (for reference):**
> - Boris Cherny’s Claude Code workflow thread (ThreadReader mirror)
> - Anthropic Claude Code docs: subagents + hooks

---

## Part 2: The Writing Process

### Step 1: Before You Write — Gather Evidence

**Ask yourself:**
1. What does the code actually show? (Use grep, file reads)
2. What has the user explicitly said?
3. What do PRODUCTION-status docs tell me?
4. What am I uncertain about?

**Output format:**
```markdown
EVIDENCE GATHERED:
- [fact]: [source]
- [fact]: [source]

UNCERTAINTIES:
- [question]: [impact if wrong]
```

### Step 2: Structure Your Content

**Every document needs:**

| Section | Purpose | Length |
|---------|---------|--------|
| **Context** | Why this exists | 1-2 sentences |
| **Key Points** | What matters most | 3-5 bullets |
| **Details** | Supporting info | As needed |
| **Next Steps** | What happens now | Bullet list |

**Example — Good Structure:**
```markdown
# API Authentication

Context: User login and token management for the REST API.

Key Points:
- JWT tokens with 24h expiry
- Refresh tokens stored in httpOnly cookies
- Rate limiting: 5 attempts per 15 minutes

Details:
[Implementation specifics...]

Next Steps:
- [ ] Implement refresh endpoint
- [ ] Add rate limiting middleware
```

**Example — Bad Structure:**
```markdown
# Auth

Authentication is important for security. We use tokens.
There are many types of tokens. JSON Web Tokens are popular.
They were invented in 2010 and are used by many companies...
```
*(No clear point, buried info, no action items)*

### Step 3: Write for Scannability

**Use visual hierarchy:**
```markdown
## Major Topic

### Sub-topic

Key insight here.

| Approach | Pros | Cons |
|----------|------|------|
| Option A | Fast | Complex |
| Option B | Simple | Slow |

**Decision**: Use Option A because [reason].
```

**Guidelines:**
- Max 3 lines per paragraph
- Use tables for comparisons
- Bold the conclusion/decision
- Code blocks for examples

### Step 4: Label Uncertainty

**When you're inferring:**
```markdown
ASSUMPTION: This uses React hooks (inferred from package.json).
CONFIRM: Is this assumption correct?
```

**When content is example/fictional:**
```markdown
> **EXAMPLE ONLY**: The values below are fictional.
> Replace with real project data.
```

### Step 5: Review Before Saving

**Checklist:**
- [ ] Can someone understand this without asking me questions?
- [ ] Are all claims tied to evidence?
- [ ] Are uncertainties labeled?
- [ ] Is the next action clear?
- [ ] Would I understand this in 6 months?

---

## Part 3: Domain-Specific Guides

### Backend Documentation

**What to document:**

```markdown
# Backend Architecture — [Project Name]

## Overview
[One sentence: what this backend does]

## Key Patterns

### 1. Layer Structure
```
/src
  /routes        # HTTP layer — validates input, calls services
  /services      # Business logic — no HTTP, no DB directly
  /repositories  # Data access — SQL/queries only
  /models        # Types/schemas
```

**Why**: Separation allows testing business logic without HTTP/DB.

### 2. API Conventions

**Routes:**
- Use plural nouns: `/users`, `/projects`
- Actions via HTTP methods, not URLs:
  - `POST /users` (create)
  - `GET /users/:id` (read)
  - `PUT /users/:id` (update)
  - `DELETE /users/:id` (delete)

**Response Format:**
```json
{
  "data": { ... },
  "error": null | { "code": "...", "message": "..." }
}
```

### 3. Error Handling

**Do:**
```typescript
// Service layer throws domain errors
if (!user) throw new NotFoundError('User not found');

// Route layer maps to HTTP status
catch (e) {
  if (e instanceof NotFoundError) return res.status(404).json(...);
}
```

**Don't:**
```typescript
// Mix HTTP and business logic
if (!user) return res.status(404).json(...); // ❌ in service
```

### 4. Security Checklist

Every endpoint must consider:
- [ ] Authentication required?
- [ ] Authorization (who can access)?
- [ ] Input validation (schema)?
- [ ] Rate limiting?
- [ ] SQL injection prevention (parameterized queries)?
```

**How to write it:**
1. Read 3-5 existing files in each layer
2. Extract the common patterns
3. Document the pattern + the "why"
4. Include one concrete example per pattern

---

### Frontend Documentation

**What to document:**

```markdown
# Frontend Architecture — [Project Name]

## Overview
[One sentence: what this frontend is]

## Component Patterns

### 1. File Organization
```
/components
  /Button
    Button.tsx        # Component
    Button.test.tsx   # Tests (co-located)
    Button.module.css # Styles (co-located)
```

**Why**: Finding related files is instant.

### 2. Component Structure

**Template:**
```typescript
// 1. Imports (external first, internal second)
import React from 'react';
import { Button } from './Button';

// 2. Types
interface Props {
  title: string;
  onClick: () => void;
}

// 3. Component
export function Card({ title, onClick }: Props) {
  // State
  const [isOpen, setIsOpen] = useState(false);
  
  // Effects
  useEffect(() => { ... }, []);
  
  // Render
  return (...);
}
```

### 3. Styling Approach

**Use CSS Modules:**
```typescript
import styles from './Button.module.css';

<button className={styles.primary}>...</button>
```

**Naming:**
- `.container` — outer wrapper
- `.item` — repeated elements
- `.active`, `.disabled` — states

### 4. Accessibility Requirements

Every component must:
- [ ] Have semantic HTML (`<button>` not `<div onclick>`)
- [ ] Include labels (`aria-label` if no visible text)
- [ ] Support keyboard navigation
- [ ] Show focus states
- [ ] Maintain 4.5:1 contrast ratio

**Example:**
```tsx
// Good
<button 
  onClick={handleClick}
  aria-label="Close dialog"
  className={styles.closeBtn}
>
  ×
</button>

// Bad
<div onClick={handleClick}>×</div> // ❌ Not keyboard accessible
```

### 5. Performance Targets

- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s
- Component bundle: < 200KB gzipped

**Patterns:**
- Lazy load routes: `const Admin = lazy(() => import('./Admin'))`
- Code split large libraries
- Use `React.memo()` for expensive renders
```

**How to write it:**
1. Look at 3-5 existing components
2. Identify the consistent structure
3. Document as "pattern + example"
4. Include the "why" for each rule

---

## Part 4: Document Templates

### PROGRESS.md — Session State

**Purpose:** Lightweight handoff between sessions.

```markdown
# Session Log

## Current: [Date]
**Focus**: [What we're working on]
**Status**: [In progress / Blocked / Complete]

### Completed
- [x] [Task] — [Brief result]

### In Progress
- [ ] [Task] — [Current status]

### Blockers
- [Issue] — [What's needed to unblock]

### Next Session
- [Priority task]
- [Priority task]
```

**When to update:** End of every session.
**How long:** 5 minutes max. Brief is better.

---

### PRD.md — Product Requirements

**Purpose:** What we're building and why.

```markdown
# [Feature Name]

## Problem
[Current pain point — 1-2 sentences]

## Solution
[What we're building — 1-2 sentences]

## Success Metrics
- [Metric]: [Target]

## Requirements

### Must Have
- [ ] [Requirement]

### Should Have
- [ ] [Requirement]

### Won't Have (Now)
- [ ] [Out of scope item]

## User Flow
1. [Step 1]
2. [Step 2]
```

**Key rule:** Every requirement ties to the Problem or Solution.

---

### DESIGN_TOKEN.md — Design Tokens & Brand System

**Purpose:** Canonical design token definitions derived from brand discovery. Records design principles, color/spacing/typography/radius/shadow/motion tokens, and a validation report.

```markdown
# DESIGN_TOKEN.md

> Brand: [Brand Name]
> Version: 1.0

## Brand Discovery Summary
| Question | Answer |
|---|---|
| Q1 Purpose | [...] |
| Q2 Persona | [...] |
...

## Design Principles
| # | Principle | Source | Token Impact |
...

## Color Tokens
--color-primary: [hex]; /* usage note */
...

## Validation Report
- [ ] WCAG AA contrast verified
- [ ] Principles traceable to tokens
...
```

**When to create:** When generating a brand design system (use `generating-design-tokens` skill).
**Template location:** `.agents/docs/DESIGN_TOKEN.md`
**Key rule:** Every token rationale must cite its discovery source (Q1–Q6 or document name).

---

### TECH_STACK.md — Technology Choices

**Purpose:** What we use and why.

```markdown
# Technology Stack

## Runtime
- **Node.js** v20 (LTS until 2026-04)

## Core Dependencies
| Package | Version | Purpose | Locked |
|---------|---------|---------|--------|
| Next.js | 14.x | Framework | 2024-01-15 |
| Prisma  | 5.x | ORM | 2024-01-15 |

## Constraints
- **Database**: PostgreSQL 15+
- **Browser Support**: Last 2 versions
- **Node Version**: >= 20.0.0

## Prohibited
- ❌ Lodash (use native)
- ❌ Moment.js (use date-fns)
```

**When to lock:** After any significant change. Date-stamp it.

---

## Part 5: Quality Checklist

### Before Submitting Any Document

**Clarity:**
- [ ] First paragraph explains why this exists
- [ ] Every claim has a source or is labeled ASSUMPTION
- [ ] Examples are labeled EXAMPLE if fictional

**Completeness:**
- [ ] Next actions are listed
- [ ] Links to related docs work
- [ ] Status header is correct (TEMPLATE/PRODUCTION)

**Maintainability:**
- [ ] Scannable (headings, tables, bullets)
- [ ] No paragraphs > 3 lines
- [ ] Would make sense to future reader

---

## Quick Reference

**Document Status:**
- `TEMPLATE` — Generic, fill with project info
- `PRODUCTION` — Validated, treat as authoritative
- `EXAMPLES-ONLY` — Fictional, delete before use

**Update Process:**
1. Propose with OLD/NEW/REASON format
2. Wait for approval
3. Apply change
4. Log in LESSONS.md

**Communication Patterns:**
```markdown
ASSUMPTIONS:
- [assumption to verify]

CHANGES:
- [file]: [what changed and why]
```
