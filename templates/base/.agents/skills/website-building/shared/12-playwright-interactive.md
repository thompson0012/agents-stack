# Interactive Browser QA

Use this guide when a task needs interactive browser verification through the current browser automation tool. The goal is the same as before: explicit coverage, realistic interaction, and visual evidence that supports the claims you make.

## Core Principle

Do not improvise QA from memory.

Before signoff, build a coverage list from:
- the user's requested requirements,
- the visible features or behaviors you actually implemented,
- the claims you expect to make in the final response.

Anything that appears in any of those three sources should map to at least one QA check.

## Core Workflow

1. Write a brief QA inventory before testing.
2. Start or confirm the local runtime with normal shell commands from the project directory.
3. Open the browser session with the browser automation tool.
4. Navigate to the target URL.
5. Use `observe` to understand the current page and capture stable element IDs before interacting.
6. Run functional QA with normal user actions.
7. Run a separate visual QA pass.
8. Capture screenshots only when they add evidence that observation alone cannot provide.
9. Close the browser session when the task is finished.

## QA Inventory

For each requirement, control, or user-visible claim, note:
- the functional check,
- the state where the visual check must happen,
- the evidence you expect to capture.

Also add at least two exploratory or off-happy-path scenarios that could expose fragile behavior.

## Browser Tool Posture

- Prefer `observe` over screenshots to understand page state.
- Use `click_id`, `type_id`, and `fill_id` when `observe` gives you stable element IDs.
- Use `wait_for_selector` before interacting with dynamic UI.
- Use `evaluate` only to inspect or stage state, not as a substitute for real signoff interactions.
- Use `screenshot` when visual appearance matters or when you need an artifact supporting a claim.
- Keep one browser session open through the QA pass instead of reopening it between every check.

## Example Session Shape

A typical pass uses the browser tool in this order:

1. `open`
2. `goto` the local URL
3. `observe` the page
4. `click_id` or `type_id` through the main flow
5. `observe` again after each meaningful state change
6. `screenshot` only for states that need visual evidence
7. `close`

If the page changed on disk after an edit, reload by navigating to the same URL again or by using `evaluate` to call `location.reload()` and then re-observe.

## Dev Server

Start the server once with the stack's normal shell command and leave it running while you iterate.

Common examples:
- Static preview: use the project's own preview command or a simple local server from the project directory
- Vite or React app: `npm run dev`
- Production sanity check when needed: `npm run build`, then run the built server or preview command the project already defines

Do not restart the server after every edit. Restart only if it actually crashed or the current command no longer reflects the state you need to verify.

## Functional QA

- Use real user controls for signoff: clicks, typing, scrolling, taps, and keyboard input.
- Verify at least one end-to-end critical flow.
- Confirm visible outcomes, not just hidden state.
- Cover every obvious user-facing control at least once before signoff.
- For reversible or stateful controls, test the full cycle: initial state, changed state, return state.
- After the scripted pass, do a short exploratory pass instead of following only the expected path.
- If exploration reveals a new control, state, or claim, add it to the QA inventory and cover it.

## Visual QA

Treat visual QA as separate from functional QA.

- Re-state the user-visible claims and verify each one explicitly.
- Inspect the initial viewport before scrolling.
- Confirm that the first view communicates the product's main promise.
- Inspect all visible regions that matter, not just the main interaction surface.
- Inspect at least one meaningful post-interaction state when the task is interactive.
- For motion-heavy UI, inspect both the settled state and at least one in-transition state.
- For dense interfaces, inspect the densest realistic state you can reach, not just loading or empty states.
- Run a separate pass at the minimum supported viewport or another realistically small viewport.
- Treat clipping, weak contrast, broken layering, awkward spacing, unreadable text, or unstable motion as visual failures even when the DOM technically contains the right elements.

## Viewport Fit Checks

Do not assume the page fits just because the primary widget appears on screen.

Before signoff:
- Define the intended initial view.
- Verify that essential controls and status are visible in that initial view.
- Use screenshots as primary evidence for fit when layout questions matter.
- Support the screenshots with DOM or geometry checks when clipping is a realistic failure mode.
- If a required region is cut off, obscured, or pushed outside the intended viewport, treat that as a bug.

## Signoff Standard

QA is complete only when all of the following are true:
- The functional path passed with normal user input.
- Coverage is explicit against the shared QA inventory.
- The visual pass covered the whole relevant interface.
- Each user-visible claim has matching evidence from the state where that claim matters.
- Viewport-fit checks passed for the intended initial view and any required smaller viewport.
- A short exploratory pass was completed for interactive products.
- The response can include a brief negative confirmation of the main defect classes checked and not found.

## Fresh Evaluator Handoff

When browser-facing work is non-trivial, release-sensitive, or needs independent signoff, finish this builder QA workflow first and then hand off to `software-delivery/frontend-evaluator` for a fresh re-check.

Leave behind:
- the exact start command, URL, and any required credentials, fixtures, or setup notes
- the QA inventory covering requirements, claims, and critical flows
- the states already exercised, evidence pointers that may help orientation, and any known defects or limits

This handoff reduces setup ambiguity; it does not pre-approve the result. The evaluator re-runs the checks from scratch and may still fail the work.

## Common Failure Modes

- **Page will not load:** the local server is not running, is on a different port, or needs more startup time. Re-check the shell command and URL.
- **Selector or element ID is stale:** re-run `observe` after the UI changes.
- **Interaction races the UI:** wait for the relevant selector, text, or loading state before the next action.
- **Screenshot is ambiguous:** capture a focused screenshot of the specific region or re-check after the UI settles.
- **Observation disagrees with a screenshot:** trust the visible defect, investigate the discrepancy, and do not sign off until it is explained.

## Cleanup

Close the browser session when the task is done so the next run starts from a known state.
