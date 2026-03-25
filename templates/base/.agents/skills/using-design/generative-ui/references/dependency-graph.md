# Dependency Graph and Hints

This file makes the suite dependencies explicit without introducing non-standard frontmatter.

## Graph

| Edge | Type | When it applies | Notes |
| --- | --- | --- | --- |
| `using-design/generating-design-tokens -> using-design/generative-ui` | prerequisite producer | No trustworthy design token spec exists yet | The hard dependency is the token artifact. If `docs/reference/design.md` or an equivalent token spec already exists, use that instead of regenerating it. |
| `using-design/design-foundations -> using-design/generative-ui` | fallback reference | Disposable prototype with no project-specific token spec | Use only when the work is exploratory and you label the fallback honestly. |
| `website-building -> generative-ui` | adjacent router | The request is really a full website, webapp, or game and only one layer is generative | Route to `website-building` first when the browser artifact is the main job. |
| `meta-prompting -> generative-ui` | sibling alternative | The deliverable is the prompt or system instruction for the UI generator itself | Prompt artifacts should go to `meta-prompting`, not here. |

## Operational Hints
- Treat design tokens as a prerequisite for any reusable or production-facing generative UI system.
- Existing token docs satisfy the prerequisite; `using-design/generating-design-tokens` is the producer when that artifact is missing.
- Keep this skill focused on generative browser surfaces. If the user really wants a whole site or app, use `website-building` as the primary route.
- Use one rendering contract at a time: standalone HTML, typed schema, or streamed UI.
- Fail closed when the model emits an unsafe or invalid payload.

## Why this is prose, not frontmatter
The current portable skill validator intentionally keeps leaf-skill frontmatter minimal. Dependency hints therefore live in the skill body and bundled references rather than new metadata keys.
