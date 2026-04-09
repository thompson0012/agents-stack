# Discovery-to-Delivery Pattern

This note captures a useful pattern for broad, artifact-backed initiatives where the first hard problem is understanding what already exists well enough to cut an honest sprint 0. It is guidance, not a new harness contract. If anything here conflicts with `AGENTS.md`, the state-machine reference, or orchestrator-worker rules, those sources win.

## When to use it

Use this pattern when the starting point is a source artifact or partially built system and the work must move from discovery into a first bounded delivery slice without inventing product truth from chat memory.

## Suggested sequence

1. **Ground on the contract and the source artifact**
   - Read `AGENTS.md` first.
   - Read the strongest source artifact that motivated the work: repo files, archived materials, prior notes, screenshots, recordings, or comparable evidence.
   - Treat the artifact as evidence to interpret, not as a substitute for current repo truth.

2. **Extract the workflow and summarize the product**
   - Turn the artifact-backed evidence into a short explanation of what the product does, who it serves, and which workflows appear central.
   - Name major assumptions and unknowns early so later planning does not pretend they were settled.

3. **Broaden with fresh sub-agents when scope widens**
   - If understanding now depends on multiple subsystems, perspectives, or evidence sources, fan out with fresh workers rather than stretching one context window.
   - Merge the returned findings back into one coherent view before routing the next phase.

4. **Publish product definition and explicit gaps**
   - Convert the understanding into durable product truth: requirements, sitemap or module map, and a clear list of missing decisions, unresolved risks, and out-of-scope areas.
   - Keep the gaps explicit. Hidden uncertainty is what makes sprint 0 dishonest.

5. **Calibrate design against live visual references**
   - When visuals matter, compare the intended design system or tokens against live references instead of choosing styles in the abstract.
   - Capture the calibration decisions briefly so implementation does not drift on spacing, color, type, or interaction tone.

6. **Use ASCII diagrams for critical pages and flows**
   - Add compact ASCII diagrams only where structure matters: key pages, navigation, stateful flows, or handoffs between modules.
   - Prefer them when they make scope or sequencing easier to verify before code exists.

7. **Publish roadmap and current-focus truth, then cut the first bounded sprint**
   - Once the initiative is understood, update the durable roadmap and current-focus story before starting serial sprint work.
   - Cut sprint 0 as the smallest slice that can be implemented and verified honestly.
   - The sprint should answer one bounded question, not absorb the whole initiative.

8. **Choose the stack, bootstrap, and verify**
   - Pick the implementation stack that fits the discovered product and repo constraints.
   - Bootstrap only what the slice needs.
   - Verify with the real checks the slice implies: build, startup, and browser or runtime behavior as applicable.

## Agents-stack phase mapping

- `project-initializer` / `generator-brainstorm`: ground the source artifact, summarize the product, and decide whether the candidate is still vague.
- `generator-proposal`: publish the roadmap/current-focus truth and cut the first bounded sprint.
- `generator-execution`: bootstrap the slice and implement the foundation.
- `adversarial-live-review` → `state-update` → `compound-capture`: verify, reconcile, and retain the durable lesson.

## Why it helps

Broad initiatives fail when teams jump from vague evidence straight into implementation. This pattern forces a cleaner handoff between discovery, product definition, design calibration, and the first executable slice. The result is usually a truer roadmap, a smaller sprint 0, and less rework caused by hidden ambiguity.

## Guardrails

- This is a reusable pattern, not a mandatory phase list.
- Use it when the initiative is broad and evidence-heavy; skip or compress steps when the problem is already well bounded.
- Do not treat this note as a replacement for the existing state machine, routing rules, or orchestrator-worker boundaries.
- If the work is still too broad after discovery, route back to brainstorm or proposal refinement rather than forcing sprint 0.
- Do not let roadmap or current-focus notes become a second execution contract; active sprint truth still belongs in the approved sprint-local contract.
