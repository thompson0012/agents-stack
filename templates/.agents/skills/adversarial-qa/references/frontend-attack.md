# Frontend Attack

Attack browser UIs. This is not about pixel-perfect verification — it's about finding what breaks the user experience under adversarial conditions.

This reference extends the **7-layer framework** from [frontend-qa](../../frontend-qa/SKILL.md). The frontend-qa skill verifies that the UI meets its design contract. This reference finds what breaks it.

## Mindset

The UI works on the happy path with ideal data. Your job is to find what happens when reality doesn't cooperate.

## Attack Patterns

### 1. Extreme Content

Replace every data source with extreme values:

| Attack | What to inject |
|---|---|
| **Empty state** | Remove all data — does the page show a graceful empty state or a broken layout? |
| **Null/undefined fields** | Set specific fields to null — does the page crash on property access? |
| **Maximum length** | Inject 10K-character strings into name, description, bio, title fields |
| **Special characters** | `<script>alert('xss')</script>`, SQL injection attempts, Unicode RTL override characters |
| **Emoji payload** | Long strings of emoji — does line-height stay stable? Does the UI overflow? |
| **Mixed scripts** | Chinese + Arabic + emoji + English in the same text block |
| **Image failures** | Point image URLs to broken endpoints, very large images (10MB+), very slow images (30s load) |
| **Excessive items** | Lists with 0, 1, 1000, 10000 items — does pagination/virtualization work? |
| **HTML injection** | User-generated content that contains HTML tags — is it rendered or escaped? |

### 2. Network Failure Injection

Intercept network at critical moments:

| Moment | Attack | Expected failure mode |
|---|---|---|
| **Page load** | Block all API calls | Graceful offline state vs broken page |
| **Form submission** | Fail the POST request | Show error, keep form data, allow retry vs data loss |
| **After user action** | Fail the response 5s after the action | Optimistic update must roll back |
| **During file upload** | Cut connection at 50% | Partial upload state vs unclear failure |
| **During polling** | Fail every other poll request | Handle intermittent failure gracefully |
| **During streaming** | Drop connection mid-stream | Partial content vs nothing |

### 3. Browser Edge Cases

Test what the user's browser actually does:

| Edge case | What to test |
|---|---|
| **Back/forward navigation** | Navigate away from a form with unsaved data, then press Back — is state preserved? |
| **Tab backgrounding** | Switch tabs while data is loading, come back after 1 minute — does it recover? |
| **Page refresh** | Refresh mid-transaction — is there data loss? |
| **Browser back to cached page** | Navigate to a page, then press Back before it loads — is there a duplicate request? |
| **Print mode** | Open the page in print preview — does the layout hold up? |
| **Zoom** | Zoom to 200%, 400% — does the UI become unusable? |
| **Reduced motion** | Enable prefers-reduced-motion — do animations stop? Are there any flash/movement issues? |
| **Reduced data mode** | Enable prefers-reduced-data / "Data Saver" — are large resources skipped? |

### 4. State Inconsistency

Find every path where UI state can diverge from server state:

| Source of inconsistency | Attack |
|---|---|
| **URL params vs local state** | Manually change URL params after page load — does the page sync or desync? |
| **Multiple tabs** | Open the same resource in two tabs. Modify in tab A, then act in tab B — stale state? |
| **Optimistic updates** | Trigger 5 rapid optimistic updates, then make them all fail — does rollback clean up? |
| **WebSocket/SSR state** | Server pushes an update while user is interacting — does the UI handle merge conflicts? |
| **Authentication state** | Let session expire while user is on a page — does the UI degrade before the API call? |
| **Local storage vs server** | Read from local storage, then server returns different data — which wins? |

### 5. Rapid Interaction

Test the UI under fast, repetitive user actions:

- Double-click a submit button — duplicate submission?
- Click 20 times rapidly on a toggle — correct state after stabilization?
- Switch tabs/sections rapidly — are there in-flight request cancellations? Memory leaks from unmounted components?
- Type rapidly in a search field with debounce — does the final result match the final input?
- Rapidly scroll a virtualized list — blank rows? Flash of content?

### 6. Accessibility Under Stress

Test accessibility not just in ideal conditions:

- Navigate with keyboard while a large dataset is loading — does focus management break?
- Use a screen reader during a loading/error transition — are live regions announced?
- Test with browser font size at "Very Large" (200%) — does text overflow?
- Test with high contrast mode — is all information still visible?
- Test with slow network + screen reader — does the screen reader announce partial content?

## Attack Procedure

1. Identify all user-facing features in scope
2. For each feature, determine what data it displays and accepts
3. Run Extreme Content attacks on every data source
4. Run Network Failure attacks on every network-dependent interaction
5. Run Browser Edge Case attacks on navigation flows
6. Run State Inconsistency attacks on stateful features
7. Run Rapid Interaction attacks on interactive elements
8. Run A11y Under Stress attacks on critical user flows
9. Compile findings

## Integration with frontend-qa

The frontend-qa skill's 7 layers define what "correct" looks like. Use those layers as a starting point — then go beyond them. For each layer:
- **Visual QA**: Now break it with extreme content
- **Interaction QA**: Now break it with rapid interaction
- **Responsive QA**: Now break it with zoom + reduced motion
- **Content QA**: This is already about adversarial content — use it directly
- **Performance QA**: Now break it with network failure at critical moments
