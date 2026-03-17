# Market Research

**Do NOT skip connector discovery for market sizing, company financials, or industry data.** Premium connectors (CB Insights, PitchBook, Statista) provide licensed, structured data that web search cannot match. Always run `list_external_tools(queries=["cb_insights", "pitchbook", "statista", "finance_"])` as the first step before web research. Only fall back to web search when connectors don't cover the topic.

**Critical**: Always produce a complete, substantive report regardless of search result quality. Available evidence combined with domain knowledge is always sufficient to deliver value. A complete report with acknowledged gaps is far more valuable than a truncated or refused response.

## Tools

This skill uses the following tools:

- `search_web` — web research (up to 50 searches per analysis)
- `fetch_url` — retrieve full page content for primary source tracing
- `ask_user_question` — clarify ambiguous queries or missing required inputs
- `share_file` — upload charts and deliver the final report to the user
- `list_external_tools` — discover available data connectors (CB Insights, PitchBook, Statista, etc.)
- `describe_external_tools` — describe a connector's tools before calling them (required before `call_external_tool`)
- `call_external_tool` — query discovered connectors for premium data
- `run_subagent` — parallelize research across framework dimensions; spawn the `data/visualization` subagent to generate charts

---

## Phase 1: Framework Detection

Parse the user's message to identify the subject and match it to a framework using the table below. Check for explicit framework names first, then keyword matches, then infer from intent. If the message is too vague to identify a subject (e.g., "run a market analysis"), use `ask_user_question` to ask: "What would you like to research? You can describe a topic, name a company, or ask a strategic question. I'll pick the best framework automatically — or you can specify one (e.g., 'PESTEL for US digital health')."

| Framework | Keywords | Example Intents |
|---|---|---|
| PESTEL Analysis | pestel, pest analysis, macro-environmental, political economic social technological | "Biggest external risks/forces affecting [industry]?" |
| Technology Adoption / S-Curve | s-curve, adoption curve, technology adoption, diffusion of innovation, hype cycle | "Where is [technology] on the adoption curve?" |
| Porter's Five Forces | porter, five forces, buyer power, supplier power, barriers to entry, threat of substitutes | "Competitive dynamics in [industry]?" |
| Competitive Benchmarking | competitive landscape, benchmarking, compare the top, competitor comparison | "Compare top players in [category]" |
| Perceptual Mapping | perceptual map, positioning map, brand positioning, perception map | "How do consumers perceive [brands] on [dimensions]?" |
| BCG Matrix | bcg matrix, growth-share matrix, stars cash cows, question marks dogs | "Classify [company]'s business units" |
| SWOT Analysis | swot, strengths weaknesses opportunities threats | "[Company]'s strengths and weaknesses?" |
| Business Model Canvas | business model canvas, bmc, value proposition.*revenue streams, nine blocks | "How does [company] make money?" |
| Value Chain Analysis | value chain, primary activities, support activities | "Map [company]'s value chain" |
| Ansoff Matrix | ansoff, market penetration.*product development, diversification.*growth, growth matrix | "Where is [company]'s growth coming from?" |
| TAM / SAM / SOM | tam, sam, som, total addressable market, market sizing, market size | "How big is the market for [product]?" |
| Jobs to Be Done (JTBD) | jobs to be done, jtbd, functional.*emotional.*social jobs, hiring.*firing | "Why do customers buy [product]?" |
**Fallback**: If 2-3 frameworks are plausible, use `ask_user_question` to present candidates with a one-sentence description and why each fits. If no framework can be inferred, present all 12 grouped:
- **Macro**: PESTEL, S-Curve, TAM/SAM/SOM
- **Industry**: Porter's Five Forces, Competitive Benchmarking, Perceptual Mapping
- **Company**: SWOT, Business Model Canvas, Value Chain
- **Growth**: BCG Matrix, Ansoff Matrix, JTBD

---

## Phase 2: Clarification

Once the framework is selected, check for required inputs. Only ask about **missing** required inputs. If all are present, skip to Phase 3.

| Framework | Required | Optional |
|---|---|---|
| PESTEL | industry/sector, geography | timeframe (default: current + 3yr), entity perspective |
| S-Curve | technology or product category | market segment, timeframe, geography |
| Porter's Five Forces | industry, geography | forces to emphasize, sub-segment |
| Competitive Benchmarking | market or product category | specific companies, dimensions, count |
| Perceptual Mapping | product/brand category, two axis dimensions | specific brands, number of brands |
| BCG Matrix | company, business units (3+) | metrics preference, time period |
| SWOT | company or product | timeframe, quadrant emphasis |
| Business Model Canvas | company | canvas blocks to emphasize |
| Value Chain | company | comparison entity, activities to emphasize |
| Ansoff Matrix | company | specific initiative, time period |
| TAM / SAM / SOM | product/service, target market | methodology (top-down/bottom-up), segment, geography |
| JTBD | buyer persona OR product category | job dimensions, industry context |

Use `ask_user_question` to ask for all missing required inputs in a single natural question.

---

## Phase 3: Research Orchestration

### Setup

Initial todo list: (1) Discover connectors, (2) Research context, (3) Research dimensions, (4) Deep-dive key findings, (5) Evaluate coverage & fill gaps, (6) Generate charts, (7) Write report.

### Connector Discovery (mandatory)

Run `list_external_tools(queries=["cb_insights", "pitchbook", "statista", "finance_"])` as the first action, before any web research. Do not skip this step.

For each connector returned, run `describe_external_tools(source_id=<id>, tool_names=[<tool>])` to get the schema, then query via `call_external_tool`. Connector data is higher quality than web search and must be used whenever it covers the topic.

**Minimum connector usage**: If premium connectors are available, the final report must include data from at least one connector. For every framework, query at least one relevant connector:
- **Any framework involving market sizing, statistics, or industry data** → query Statista
- **Any framework involving private companies, funding, or deal data** → query PitchBook or CB Insights
- **Any framework involving startup ecosystems or emerging markets** → query CB Insights
- **Business Model Canvas for a private company** → query PitchBook or CB Insights for financials, funding history, and investor data

**Connector call budget**: `list_external_tools`, `describe_external_tools`, and `call_external_tool` against non-premium sources are always unrestricted. The budget applies only to `call_external_tool` against premium sources (CB Insights, PitchBook, Statista): maximum **5 calls per premium source**, shared across the parent agent and all subagents combined. Before each such call, ask: does this query require licensed data that web search cannot provide? Replace broad exploratory queries, duplicate angles, or low-value lookups with `search_web`. Use premium connector calls for the highest-value data points only.

### Citation

When `call_external_tool` returns results, record the connector name and response URL (if present) alongside the data. Connector-sourced facts must appear in the final report with citations: `[CB Insights](URL)`, `[PitchBook](URL)`, `[Statista](URL)`. If no URL is returned, cite by name only: `CB Insights`. This is required — do not omit connector attribution even when the data is paraphrased or synthesized.

**Passing connectors to subagents**: Subagents do not inherit the parent's connector discovery results or described-tool state. This means:

1. Each subagent **must** call `describe_external_tools(source_id=..., tool_names=[...])` itself before calling `call_external_tool` — even if the parent already described the same tool. Calling `call_external_tool` without first calling `describe_external_tools` in the same subagent session will always fail with an error.
2. Include the available connector `source_id` values and tool names explicitly in the subagent's objective so it knows what to describe and call.

Example subagent instruction: "First call `describe_external_tools(source_id='statista', tool_names=['search'])`, then use `call_external_tool(source_id='statista', tool_name='search', ...)` to query market sizing data before falling back to `search_web`. Use at most 1-2 connector calls for this source — only for data web search cannot provide. Place citations at the end of the paragraph or bullet, after the closing period: `The EU generative AI market was valued at $11.77B in 2024. [Statista](URL)` If no URL is returned, cite by name only: `Statista`. Do not recommend that users access the connector's external portal directly."

### Research Budget & Common Flow

Global budget: **maximum 50 total `search_web` calls per analysis**, shared across the parent agent and all subagents. Allocate roughly:

**Phase 3a — Context (~5 searches)**: "[subject] overview [year]", "[subject] recent news", "[subject] market data key players"

**Phase 3b — Dimensions (~25 searches)**: Targeted searches per framework dimension. **You MUST use `run_subagent` to parallelize research for every framework listed in the Parallelization Strategies table below.** Consult the table, spawn the specified subagents concurrently, and divide the search budget among them (e.g., 5 subagents × ~5 searches each). Only the three frameworks listed under "Sequential frameworks" should be researched without subagents. Each subagent should also flag visualization opportunities — note any quantitative comparisons, trend data, or ranked data suitable for charting, and save the structured data (labels + values) alongside findings.

**Phase 3c — Deep Dives (~10 searches)**: Follow up on most promising URLs via `fetch_url` (government reports, analyst publications, financial filings).

**Phase 3d — Primary Source & Gap-Fill (~10 searches)**:
1. **Primary source tracing**: Follow research-assistant's `fetch_url`-first approach — trace key statistics to original sources (SEC filings, government data, analyst reports).
2. **Named examples**: Include company-level examples and case studies where available from search results.
3. **Query-specific sub-topics**: If the user's query names specific concepts/events, dedicate a search to each.

For A-vs-B comparisons, split budget roughly evenly. For Value Chain comparisons, use interleaved side-by-side structure.

### Parallelization Strategies

| Framework | Parallel Strategy |
|---|---|
| PESTEL | 1 subagent per dimension — 6 concurrent (Political, Economic, Social, Technological, Environmental, Legal) |
| S-Curve | 3 concurrent: adoption data, maturity signals, historical analogues |
| Porter's Five Forces | 1 subagent per force — 5 concurrent |
| Competitive Benchmarking | 1 subagent per competitor |
| Perceptual Mapping | 1 subagent per brand |
| BCG Matrix | 1 subagent per business unit |
| SWOT | 1 subagent per quadrant — 4 concurrent (Strengths, Weaknesses, Opportunities, Threats) |
| Value Chain | 2 concurrent: primary activities, support activities |
| Ansoff Matrix | 1 subagent per quadrant — 4 concurrent (Penetration, Product Dev, Market Dev, Diversification) |
| JTBD | 3 concurrent: functional jobs, emotional/social jobs, switching triggers |
**Sequential frameworks** (dimensions depend on each other — researched by the parent agent, not subagents):
- **TAM/SAM/SOM** — each tier narrows the previous (TAM → SAM → SOM). Query Statista for market sizing data.
- **Business Model Canvas** — blocks are interdependent (e.g., revenue streams depend on customer segments and value propositions). Query PitchBook or CB Insights for funding, valuation, and investor data.

Each subagent researches its dimension independently and writes findings to a workspace file. Every finding must include the source URL so the parent agent can cite it in the final report.

### Per-Framework Research Strategies

| Framework | Dimension Strategy | Priority Sources |
|---|---|---|
| PESTEL | 1 search per dimension (P, E, S, T, E, L) | Gov agencies (BLS, Census, EPA), central banks, World Bank/IMF. Cite legislation by name/number. |
| S-Curve | 3 adoption data + 2 maturity signals + 2 historical analogues | Gartner, IDC, Forrester; McKinsey/BCG; SO/GitHub surveys. Differentiate sub-categories at distinct curve positions. |
| Porter's Five Forces | 1 per force (5) + named players + industry-specific dynamics | Gartner, IDC, Statista. Name specific companies for every force. Include contract-level data when available. |
| Competitive Benchmarking | 2 per competitor + analyst report (Gartner MQ/Forrester Wave) | SEC filings (public); PitchBook (private). Acknowledge data limitations. |
| Perceptual Mapping | 2 consumer perception + 2 per brand + review aggregator | YouGov, J.D. Power, Consumer Reports, Trustpilot/G2. Position on *measured perception*, not attributes. |
| BCG Matrix | 2 per unit + primary financial (10-K segments) + market data | SEC 10-K segment disclosures; Gartner/IDC for market growth. Use **relative** market share. |
| SWOT | 1 per quadrant + company-specific + primary source + competitor data | SEC filings, earnings transcripts, industry analysts. |
| Business Model Canvas | 2 business model + 2 operations + 2 market + named clients | SEC filings/S-1; PitchBook (funding, valuation, investors); CB Insights (company profile); Statista (market size, user stats); industry surveys. |
| Value Chain | 2 per activity cluster + margin analysis + competitive comparison | 10-K/investor presentations; industry cost benchmarks. |
| Ansoff Matrix | 2 current business + 2 growth initiatives + strategy + primary source | Earnings transcripts, investor presentations; market share data. |
| TAM / SAM / SOM | 3 TAM + 2 SAM + 2 SOM + 2 bottom-up inputs + VC/analyst thesis | Gartner, IDC, Statista; VC papers (a16z, Sequoia, Bessemer). |
| JTBD | 2 functional + 2 emotional/social + 2 competitive switching + survey + cases | Bain, McKinsey, Deloitte surveys; enterprise case studies. |

---

## Phase 4: Report & Visualizations

**The markdown report is always the primary deliverable — generate it first, before any other output format.** Even when the user explicitly requests a spreadsheet, slide deck, PDF, or other format, always write the full markdown report first. The markdown report is the source of truth; all other formats are derived from it. Never skip or abbreviate the markdown report because another format was requested.

### Step 1: Generate Charts

Before writing the report, review all research findings and generate charts where they add value. Charts should draw on data from across all research subagents. Deliver each chart to the user via `share_file`.

**When to generate a chart:**
- **Framework-required charts**: Some frameworks mandate specific visualizations (BCG bubble chart, perceptual map scatter plot, Ansoff 2x2 grid, S-curve position chart). Always generate these.
- **Quantitative comparisons**: Market share breakdowns, revenue comparisons, funding timelines, cost structures, or margin analyses with 3+ data points.
- **Trend data**: Time-series data showing growth rates, adoption curves, pricing changes, or market size evolution.
- **Ranked data**: Competitive benchmarking scores, force strength ratings, or risk assessments that can be shown as bar or radar charts.

Skip visualization when data is sparse (fewer than 3 data points), purely qualitative, or already clear in a markdown table.

**For each chart:**
1. Spawn a coding subagent with the `data/visualization` skill. Pass the structured data (labels, values, categories) and desired chart type. The subagent writes Python (matplotlib/seaborn/plotly) to produce a PNG saved to the workspace.
2. Call `share_file` on the PNG to deliver it to the user.

### Step 2: Write the Report

#### File Naming

Write the report to a markdown file using `write`:

```
{framework_slug}_{subject_slug}_{YYYY-MM-DD}.pplx.md
```
- `framework_slug`: lowercase, hyphens (e.g., `pestel`, `porters-five-forces`)
- `subject_slug`: lowercase, underscores, max 5 words

#### Report Structure

Every report must be rigorous and comprehensive — suitable for board presentations or investor memos, not a summary. It follows:
1. `# [Framework]: [Subject]`
2. **Executive summary** (no heading — implied): 2-3 paragraphs, opening sentence states the single most important finding, inverted-pyramid style
3. **Framework-specific body sections** (per the templates below) — each section should be substantive with multiple sourced paragraphs, not just a few bullets
4. **Conclusion**: 2-3 paragraphs — restate core finding, identify 1-2 critical uncertainties, what to watch in next 6-12 months

#### Per-Framework Report Templates

**PESTEL Analysis**: One section per dimension (## Political Factors, ## Economic Factors, ## Social Factors, ## Technological Factors, ## Environmental Factors, ## Legal Factors), each with 3-5 sourced bullets. Then ## Cross-Cutting Themes (2-3 themes spanning multiple dimensions) and ## Strategic Implications.

**Technology Adoption / S-Curve Analysis**: ## S-Curve Framework (1 paragraph defining adoption stages and the chasm). ## Current Adoption Data table (Metric | Value | Source, 4-8 rows). ## S-Curve Positioning Assessment with **Current Position: [Stage]**, 2-3 paragraphs of evidence, and an S-curve chart showing the technology's position on the adoption curve. ## Inflection Indicators with two subsections: Signals of Approaching Mainstream (3-5) and Remaining Barriers (3-5). ## Analogous Technology Curves table (Technology | Time to Mainstream | Current Parallel, 2-3 rows). ## Outlook & Remaining Headroom.

**Porter's Five Forces**: One section per force (## 1. Threat of New Entrants — [H/M/L] through ## 5. Competitive Rivalry — [H/M/L]), each 2-3 paragraphs. Then ## Overall Industry Attractiveness with **Rating: [Attractive/Moderate/Unattractive]** and summary table (Force | Strength | Key Driver). ## Strategic Implications.

**Competitive Benchmarking / Landscape**: ## Market Overview (1-2 paragraphs: size, growth, trends). ## Competitive Landscape table (Company | Revenue/Funding | Headcount | Segment | Key Differentiator). ## Company Profiles (per-company subsection with overview, strengths, weaknesses, target segment, pricing). ## Competitive Dynamics (2-3 paragraphs: concentration, clusters, consolidation). ## Strategic Implications.

**Perceptual Mapping**: ## Axis Definitions (define both axes with measurement criteria). ## Perceptual Map (scatter plot with labeled brand points and quadrant crosshairs). ## Brand Positioning (per-brand subsection: Position [H/M/L] on each axis with 2-3 sentences of evidence). ## Whitespace Analysis (underserved positions). ## Strategic Implications.

**BCG Matrix**: ## Methodology (define relative market share vs. largest competitor and market growth rate). ## BCG Matrix (scatter/bubble chart: X = relative share log reversed, Y = market growth %, bubbles sized by revenue, quadrant labels Stars/Question Marks/Cash Cows/Dogs). ## Unit Classifications (per-unit subsection with Revenue, Revenue Growth, Market Growth, Relative Share, Rationale, Strategic Recommendation). ## Portfolio Analysis (balance, cash flow dynamics, cross-unit synergies). ## Strategic Recommendations.

**SWOT Analysis**: One section per quadrant (## Strengths, ## Weaknesses, ## Opportunities, ## Threats), each labeled (Internal/External, Positive/Negative) with 3-5 sourced bullets. Then ## Cross-Quadrant Analysis (how strengths capture opportunities, weaknesses amplify threats). ## Strategic Implications with 2-3 actionable recommendations.

**Business Model Canvas**: Nine numbered sections (## 1. Customer Segments through ## 9. Cost Structure) with 3-5 bullets each. Then ## Business Model Analysis (2-3 paragraphs on competitive moat, flywheel dynamics, unit economics, vulnerabilities).

**Value Chain Analysis**: ## Primary Activities (subsections: 1. Inbound Logistics, 2. Operations, 3. Outbound Logistics, 4. Marketing & Sales, 5. Service). ## Support Activities (subsections: Technology Development, HR Management, Procurement, Firm Infrastructure). ## Margin Analysis table (Activity | Margin Contribution [H/M/L] | Rationale). ## Vulnerability Assessment table (Activity | Disruption Risk [H/M/L] | Threat Source). ## Strategic Implications.

**Ansoff Matrix**: ## Ansoff Matrix Framework (2x2 grid chart: Market Penetration / Product Development / Market Development / Diversification with key initiatives in each cell). One section per quadrant with 3-5 bullets of specific initiatives with evidence. ## Growth Strategy Assessment with **Primary Growth Vector: [Quadrant]** and 2-3 paragraphs. ## Strategic Implications.

**TAM / SAM / SOM**: ## Methodology (approach: bottom-up/top-down/hybrid with explanation). For each tier (## TAM, ## SAM, ## SOM): bold dollar value (e.g., **TAM = $[X]B**), input table (Input | Value | Source), explicit calculation math, 1 paragraph of context. SAM includes narrowing criteria with % reductions. SOM includes penetration assumptions. ## Market Sizing Summary table (Tier | Value | % of Parent). ## Key Assumptions & Risks.

**Jobs to Be Done (JTBD)**: ## Context (1-2 paragraphs on the persona and situation). ## Functional Jobs (4-6 jobs with context, evidence, how current solutions fail). ## Emotional Jobs (3-5 jobs about desired emotional state). ## Social Jobs (2-4 jobs about desired perception). ## Struggling Moments & Triggers (3-5 specific situations creating demand). ## Hiring & Firing Criteria (why customers hire 3-4 and fire 3-4 solutions). ## Strategic Implications.

#### Formatting Conventions

- **Sourced bullets**: `- **[Title]** — 2-3 sentence analysis. [Source Name](URL)`
- **Inline citations**: Use inline markdown links with the source name as anchor text — never generic words like "source" or raw URLs. Place citations at the end of the paragraph or bullet point, after the closing period, comma-separated: `Revenue rose 8%, consistent with recent filings. [Bloomberg](URL), [SEC](URL)`. Never include a separate References or Citations section. Framework definitions, methodology notes, and clearly labeled analysis/synthesis paragraphs may omit citations, but must not introduce invented statistics or unverifiable claims. This applies to subagent research findings as well — when synthesizing from subagent workspace files, copy the exact citation URLs into the final report. Do not replace `[CB Insights](URL)` with `CB Insights` — the URL must be preserved. Do not use "cashmere.io" as citation link text; always use the publisher name (CB Insights, PitchBook, Statista) as the anchor text. **Connector data (CB Insights, PitchBook, Statista) must always be cited by name, even when no URL is available** — cite as `CB Insights`, `PitchBook`, or `Statista`. These are premium sources and their provenance must be visible in the report.
- **Date your data**: Note year/quarter of financial figures and market data
- **Tables**: Use markdown tables for structured comparisons

---

## Phase 5: Additional file type generation

**Only begin this phase after the markdown report is fully written and saved.** Generate any supplemental formats the user requested (Word doc, PDF, slides, Excel) or that naturally complement the report (e.g., competitive benchmarking data as a spreadsheet). Base all supplemental assets on the completed markdown report — do not research or draft new content for them.

---

## Phase 6: Delivery

After writing the report:
1. Display a **1-3 sentence** summary: the single most important finding and one key implication. Include bullet point with a single short sentence for each top-level section from the report. Keep it short. Include citations.
2. End with a brief prompt asking if they'd like to explore adjacent topics.
3. Use `share_file` to send the report to the user **before** the summary text.


---

## Quality Guidelines

- **Never omit a required dimension.** Every PESTEL gets 6 sections. Every Porter's gets 5 forces. Every SWOT gets 4 quadrants. Every BMC gets 9 blocks.
- **Use correct definitions.** BCG uses relative market share. Ansoff classifies existing vs. new on both axes. JTBD focuses on desired progress, not features.
- **Identify non-obvious dynamics**: second-order effects, cross-dimensional interactions, forward-looking implications.
- When specific sources aren't found, use domain knowledge and note the limitation briefly — never let sourcing gaps prevent a complete report. Never fabricate specific statistics or source citations.
- Prefer tier-1 sources (Gartner, IDC, Forrester, McKinsey, PitchBook, Statista, CB Insights) for market sizing. Acknowledge sourcing limitations for private company data.

---

## Error Handling & Edge Cases

- **Framework mismatch**: If research reveals a poor fit, inform the user and suggest an alternative. Never silently switch.
- **Ambiguous scope**: Default to focused scope (single geography, top 5-10 players). Note what was scoped out in the executive summary.
- **Stale/conflicting data**: Present both figures and note discrepancies. Prefer most recent data. Date all time-sensitive data points.