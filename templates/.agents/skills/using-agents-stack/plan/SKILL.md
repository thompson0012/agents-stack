---
name: plan
description: Design architecture: components, API schema, DB model, impact analysis, test strategy.
trigger: When spec.md exists and plan.md does not.
inputs: [CONSTITUTION.md, spec.md]
outputs: [.agents-stack/<id>/plan.md, .agents-stack/<id>/status.json]
boundaries: Design only. No code implementation. Must inspect real code for impact analysis.
---

# Plan Worker

Design the architecture that satisfies the spec. You produce the blueprint that `tasks` breaks down and `implement` executes. No code — only design decisions grounded in the real codebase.

## Output Template: plan.md

```markdown
# Plan: [Brief Title]

**Workstream ID:** `<id>`
**Spec Referenced:** [date or version]

## Architecture Decisions

### Component Diagram
```
[High-level component layout — ASCII or described]
```

### Data Flow
[How data moves through the system — request/response, event flow, state transitions]

### Technology Choices
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [e.g., State management] | [Choice] | [Why this fits] |

## API Design

### Endpoints

#### `METHOD /path/to/resource`
- **Purpose:** [What this endpoint does]
- **Request:** `{ field: type, ... }`
- **Response:** `{ field: type, ... }`
- **Error Codes:** `400` — [condition], `404` — [condition], `500` — [condition]

#### ...

### Schemas
```typescript
// Shared types referenced by endpoints
type Foo = { ... }
```

## Database Schema

### Entities

#### `table_name`
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PK, NOT NULL | Primary key |
| ... | ... | ... | ... |

### Relationships
- `table_a.field` → `table_b.field` (FK, cascade rule)

### Migrations
- [New migration filename and what it adds]
- [Any data migration steps]

## Impact Analysis

Impact analysis must name real files found by inspecting the codebase. No guesswork.

### Files Modified
| File Path | Change Type | Description |
|-----------|-------------|-------------|
| `src/routes/foo.ts` | MODIFY | Add new endpoint handler |
| `src/db/schema.ts` | MODIFY | Add new table definition |
| ... | ... | ... |

### Downstream Effects
- [Module X depends on changed interface Y — mitigation plan]
- [Config/env changes needed — list them]

### Files NOT Touched
| File Path | Reason Excluded |
|-----------|-----------------|
| `src/...` | Out of scope per spec |

## Test Strategy

Map every acceptance criterion to a concrete test approach.

| AC Reference | Test Type | Approach |
|-------------|-----------|----------|
| AC-001 | Unit | Test handler logic with mocked DB |
| AC-002 | Integration | End-to-end API test with test DB |
| AC-003 | E2E | Browser test for user-facing flow |
| ... | ... | ... |

### Coverage Target
- Minimum: 80% (per task Definition of Done)
- Critical paths: 100%

## Risks & Assumptions

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [e.g., DB migration breaks staging] | Medium | High | Run migration in staging first, have rollback plan |

### Assumptions
- [e.g., Authentication middleware already handles sessions]
- [e.g., Rate limiting is handled at the gateway layer]
```

## Workflow

1. Read `spec.md` — understand every user story, edge case, and acceptance criterion
2. Inspect the real codebase for existing file boundaries, patterns, and constraints
3. Design architecture: components, data flow, API surface
4. Design database changes: entities, relationships, migrations
5. Map each AC to a test strategy with the appropriate level (unit/integration/e2e)
6. Perform impact analysis: what real files change, what downstream modules are affected
7. Identify risks and document assumptions explicitly
8. Write `plan.md` to `.agents-stack/<id>/plan.md`
9. Update `status.json`: set `phase: "plan"`

## Quality Bar

- Impact analysis names real files from the codebase, not guessed paths
- Test strategy maps 1:1 to acceptance criteria from spec
- Risks include mitigation, not just identification
- Architecture is actionable — a developer can begin building from this document
- If the codebase reveals a constraint that contradicts spec, flag it explicitly

## Done

`plan.md` exists with architecture decisions, API design, DB schema, real-file impact analysis, and AC-mapped test strategy. `status.json` reflects plan phase.
