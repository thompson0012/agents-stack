# Finance Research Tools

**Do NOT use search_web for stock prices, financial data, or company fundamentals.** Financial data is highly specific, quantitative, and frequently revised — web search returns stale, unstructured snippets that may reflect pre-revision figures. Finance tools return structured, point-in-time accurate data directly from market data providers. Only fall back to web search if finance tools lack the specific data needed.

Finance tools are available via the **connector service** through `list_external_tools(queries=["finance_"])`. All finance tools share the `finance_` prefix.

## Authentication Required

**Important:** The `list_external_tools` and `call_external_tool` endpoints require authentication. Ensure you have valid credentials configured before attempting to access finance tools.

## Reference Date

Every finance query has a **reference date** that determines what data to fetch. ALWAYS derive `as_of` parameters from this date — never omit them.

### Step 1: Identify the Reference Date

- If the user specifies an explicit date (e.g., "as of March 2024"), use that date
- If the user's question implies a time period (e.g., "Q4 2024 results", "last year's revenue", "2023 earnings call"), infer the closest reference date that would return the relevant data
- Otherwise, use the current date/time from the `<context>` block

### Step 2: Map to Fiscal Parameters

Convert the reference date to `as_of_fiscal_year` and `as_of_fiscal_quarter`:

| Reference Date Month | Fiscal Quarter |
| -------------------- | -------------- |
| January–March        | Q1             |
| April–June           | Q2             |
| July–September       | Q3             |
| October–December     | Q4             |

Example: reference date 2024-08-15 → `as_of_fiscal_year=2024, as_of_fiscal_quarter=3`

### Step 3: Map to Calendar Bounds

For `finance_ohlcv_histories`, use the reference date as `end_date_yyyy_mm_dd`.

### Step 4: Past Reference Dates and Quotes

`finance_quotes` returns real-time data only. If the reference date is in the past, use `finance_ohlcv_histories` instead to get the price as of that date.

### Rules

- **ALWAYS** pass `as_of_fiscal_year` and `as_of_fiscal_quarter` to `finance_earnings` and `finance_earnings_schedule`
- **ALWAYS** pass `as_of_fiscal_year` to `finance_financials`; also pass `as_of_fiscal_quarter` for `period="quarter"` but **omit it** for `period="annual"` (annual filings have no quarter dimension)
- **ALWAYS** use the reference date as `end_date_yyyy_mm_dd` for `finance_ohlcv_histories`
- **NEVER** omit `as_of` parameters — "latest" is ambiguous and non-reproducible

## Citations

When presenting data from finance tools, cite the source for each ticker:

`https://perplexity.ai/finance/<TICKER>`

Example: data about Apple → `https://perplexity.ai/finance/AAPL`

Include citations inline or at the end of your response for every ticker whose data you present.

## Discovering Finance Tools

Use `list_external_tools` with a finance query to discover available tools:

```python
finance_tools = await list_external_tools(queries=["finance_"])
```

## Available Finance Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `finance_tickers_lookup` | Resolve ticker symbols (stocks, ETFs, indexes, commodities, crypto, international) | Always use first—standard tickers may not resolve, handles format variations (BRK.B vs BRK-B) and fuzzy names |
| `finance_quotes` | Real-time quotes for stocks, crypto, ETFs, indices | Current price, P/E, market cap, dividend yield. Returns markdown table |
| `finance_ohlcv_histories` | Historical OHLCV data for stocks, ETFs, crypto, indices as CSV | Price history, charts, technical indicators. Do NOT web search for historical prices—use this tool |
| `finance_financials` | Income statement, balance sheet, cash flow | Fundamental analysis, valuation, growth calculations, derived metrics |
| `finance_holdings` | Institutional holders and insider transactions (US-listed only) | Institutional holders, insider transactions. Non-US tickers return no data |
| `finance_etf_holdings` | ETF constituent holdings | ETF constituents, what stocks are in an ETF, ETF breakdown |
| `finance_earnings` | Earnings transcripts, history, and operating metrics | Earnings call transcripts, EPS history, beat/miss metrics. Transcripts often contain segment KPIs, non-GAAP metrics, and management commentary on drivers (take rates, unit economics, mix shifts, GMV, ARR by segment) not available in standardized financial statements. Use as a primary source for company-specific operating metrics |
| `finance_earnings_schedule` | Earnings release dates | When companies report, upcoming/past earnings calendar |
| `finance_company_profile` | Basic company info: industry, sector, CEO, employees, website, description | Company overview, who's the CEO, what industry, employee count. Does NOT include market cap (use quotes) |
| `finance_company_peers` | Peer/comparable companies for a given ticker | Competitors, similar companies, peer comparisons, alternative investments |
| `finance_market_gainers` | Top gaining stocks/crypto today | Top gainers, what's up the most, biggest risers |
| `finance_market_losers` | Top losing stocks/crypto today | Top losers, biggest drops, what's down the most |
| `finance_market_most_active` | Most actively traded stocks today | Most active stocks, highest volume, most traded |
| `finance_market_sentiment` | Overall market sentiment analysis (bullish/bearish/neutral) | Is the market bullish or bearish, market mood, overall sentiment |
| `finance_ticker_sentiment` | Bulls vs bears analysis for a specific stock | Bull/bear case for a stock, controversial views, sentiment on a ticker |
| `finance_politician_list` | List all tracked politicians with stock activity | Which politicians trade stocks, list of tracked congress members |
| `finance_politician_holdings` | A specific politician's full stock portfolio | What stocks does [politician] own, politician's portfolio |
| `finance_politician_trades` | Recent congressional stock transactions | Recent politician trades, congressional stock transactions |
| `finance_politician_ticker_holders` | Which politicians hold a specific stock | Which politicians own [ticker], congressional holders of a stock |
| `finance_watchlist_fetch` | User's Perplexity Finance watchlist (stocks they're *tracking*, not actual brokerage holdings). | User asks about their watchlist or what stocks they're tracking. **Not for actual portfolio holdings** — use the `portfolio_holdings` connected tool for real brokerage positions. |
| `finance_segments` | Segment-level breakdowns and operating KPIs not in financial statements | Revenue models, revenue builds, unit economics, P*Q analysis, key drivers, segment growth, ARPU, GMV, take rate, store count, DAU/MAU |
| `finance_estimates` | Consensus analyst estimates and forward projections | Estimated EPS, revenue, EBITDA for future periods, consensus forecasts |
| `finance_adjusted_metrics` | Adjusted (non-GAAP) financial metrics | Adjusted EPS, adjusted EBITDA, free cash flow, management-reported metrics for valuation and peer comparison |
| `finance_analyst_research` | Analyst consensus price targets and rating changes | Price targets (avg/median/high/low), analyst ratings, upgrades/downgrades, bullish/bearish breakdown |
| `finance_fundamentals` | Pre-computed valuation multiples as daily time-series | P/E ratio, EV/EBITDA, P/S, EV/Revenue, EV/FCF, dividend yield, earnings yield, historical trends, peer comparisons |
| `finance_massive` | Raw Massive API pass-through (options, tick data, macro, and any GET endpoint) | Options chains/contracts, tick-level trades/quotes, treasury yields, inflation data, or any Massive API endpoint not covered by specialized tools above |

## Data Source Routing

### Decision Tree

Follow this order for EVERY public company question. Stop at the first source that answers it:

1. **`finance_financials`** — Standardized income statement, balance sheet, cash flow. Use for: revenue, net income, margins, EPS, debt, cash, inventory, capex, FCF, SBC, dividends, shares outstanding, tax rates, and any ratio derivable from these (ROE, D/E, inventory turnover, payout ratio, FCF margin, CAGR, etc.)

2. **`finance_earnings`** — Earnings call transcripts contain FAR more than just EPS. Use for:
   - **Forward guidance**: revenue ranges, margin targets, capex plans, growth outlook
   - **Non-GAAP metrics**: adjusted EBITDA, non-GAAP gross margin, organic growth
   - **Company-specific KPIs**: ARPU, take rate, GBV, same-store sales, nights booked, loan originations, payment volume, retention rates, subscriber counts, ASMs/RPMs, load factor
   - **Beat/miss analysis**: comparing guidance from quarter N to actuals in quarter N+1
   - **Segment breakdowns**: revenue by geography, product line, or business unit
   - **Strategic commentary**: M&A rationale, restructuring progress, competitive dynamics
   - **Adjusted EBITDA reconciliations**: line-item adjustments from net income
   - **Management Q&A**: analyst questions often surface specific data points

3. **Web search** — Only after finance tools are insufficient. Required for:
   - 10-K/10-Q footnotes (debt maturity schedules, lease obligations, acquisition details)
   - Proxy statements (director compensation, board nominations, executive pay)
   - Prospectus/8-K filings (offering terms, convertible note details, M&A consideration)
   - Risk factor narratives
   - Employee headcount/geographic data
   - Channel/vendor concentration disclosures

### Rules

- Do NOT default to web search for public company analysis
- ALWAYS try `finance_earnings` before web search — transcripts answer ~50% of questions that seem like they need filings
- For questions about guidance vs. actuals, pull transcripts from BOTH the guidance quarter and the results quarter
- For hybrid questions (e.g., take rate = revenue / GBV), combine `finance_financials` for standardized data with `finance_earnings` for company-specific KPIs

## Execution Pattern

All finance tools are called via `call_external_tool` with `source_id="finance"`. You **must** call `describe_external_tools` before `call_external_tool` — the system enforces this.

```python
# 1. Discover finance tools
await list_external_tools(queries=["finance_"])

# 2. Get input schemas (required before calling)
await describe_external_tools(source_id="finance", tool_names=["finance_quotes", "finance_financials"])

# 3. Call any finance tool — always use source_id="finance"
await call_external_tool(tool_name="<tool_name>", source_id="finance", arguments={...})
```

## Workflow: Always Resolve Tickers First

Never assume ticker symbols. Always use `finance_tickers_lookup` before other tools:

```python
# Single company
await call_external_tool(tool_name="finance_tickers_lookup", source_id="finance", arguments={
    "queries": ["Tesla"]
})
```

Then fetch data with the confirmed symbol:

```python
# Basic quote
await call_external_tool(tool_name="finance_quotes", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "fields": ["price", "change", "changesPercentage"]
})
```

## Quick Reference

### Get current quote

```python
# Valuation snapshot
await call_external_tool(tool_name="finance_quotes", source_id="finance", arguments={
    "ticker_symbols": ["AAPL", "MSFT", "GOOGL"],
    "fields": ["price", "marketCap", "pe", "eps", "dividendYieldTTM"]
})
```

### Get historical data

```python
# Specific date range
await call_external_tool(tool_name="finance_ohlcv_histories", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "start_date_yyyy_mm_dd": "2024-01-01",
    "end_date_yyyy_mm_dd": "2024-06-30"
})
```

### Get recent financial data (always pass as_of from reference date)

```python
# Tesla's latest revenue (use quarter for current state)
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["TSLA"],
    "period": "quarter",
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1,
    "limit": 1,
    "income_statement_metrics": ["revenue"]
})
```

### Get historical financial data

```python
# Rivian revenue from 2023 Q3 back 4 quarters
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["RIVN"],
    "period": "quarter",
    "as_of_fiscal_year": 2023,
    "as_of_fiscal_quarter": 3,
    "limit": 4,
    "income_statement_metrics": ["revenue"]
})
```

### Get derived financial metrics

```python
# Apple profitability + cash
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "period": "annual",
    "as_of_fiscal_year": 2025,
    "limit": 1,
    "income_statement_metrics": ["netIncome"],
    "balance_sheet_metrics": ["cashAndCashEquivalents"],
    "cash_flow_metrics": ["freeCashFlow"]
})
```

### Get recent earnings transcript (always pass as_of from reference date)

```python
# Tesla's latest earnings call
await call_external_tool(tool_name="finance_earnings", source_id="finance", arguments={
    "ticker_symbol": "TSLA",
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1,
    "limit": 1,
    "data_types": ["transcript_full"]
})
```

### Get historical earnings transcript

```python
# Microsoft Q4 2024 earnings call
await call_external_tool(tool_name="finance_earnings", source_id="finance", arguments={
    "ticker_symbol": "MSFT",
    "as_of_fiscal_year": 2024,
    "as_of_fiscal_quarter": 4,
    "limit": 1,
    "data_types": ["transcript_full"]
})
```

### Get earnings beat/miss history

```python
# AAPL earnings beat/miss history
await call_external_tool(tool_name="finance_earnings", source_id="finance", arguments={
    "ticker_symbol": "AAPL",
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1,
    "data_types": ["earnings_history"]
})
```

### Get earnings schedule (always pass as_of from reference date)

```python
# When does Apple report next?
await call_external_tool(tool_name="finance_earnings_schedule", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1
})
```

```python
# All earnings this week
await call_external_tool(tool_name="finance_earnings_schedule", source_id="finance", arguments={
    "ticker_symbols": [],
    "start_date": "2025-02-03",
    "end_date": "2025-02-07"
})
```

```python
# Apple Q4 2024 earnings date
await call_external_tool(tool_name="finance_earnings_schedule", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "as_of_fiscal_year": 2024,
    "as_of_fiscal_quarter": 4
})
```

### Get holdings data

```python
# ETF constituents
await call_external_tool(tool_name="finance_etf_holdings", source_id="finance", arguments={
    "ticker_symbols": ["SPY", "QQQ"],
    "ticker_names": ["SPDR S&P 500 ETF", "Invesco QQQ Trust"],
    "query": "What are the top holdings in SPY and QQQ?"
})
```

## Advanced: Raw API Access

For data not covered by the specialized tools above, use `finance_massive` to make direct GET requests to the Massive API. Covers options, tick-level market data, macro-economic indicators, and any other Massive endpoint. Docs are available at https://massive.com/docs/llms.txt

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `pathname` | `str` | Yes | - | The API pathname to request, e.g. '/v3/reference/tickers'. |
| `params` | `object` | No | {} | Optional query parameters to include in the request. |

### Common Endpoints

| Category         | Example Pathname                                                            | Description                 |
| ---------------- | --------------------------------------------------------------------------- | --------------------------- |
| RSI              | `/v1/indicators/rsi/{stockTicker}`                                          | Relative Strength Index     |
| Options chain    | `/v3/snapshot/options/{underlyingAsset}`                                    | Full options chain snapshot |
| Tick trades      | `/v3/trades/{stockTicker}`                                                  | Individual trade records    |
| Tick quotes      | `/v3/quotes/{stockTicker}`                                                  | NBBO quote records          |
| Treasury yields  | `/fed/v1/treasury-yields`                                                   | US Treasury yield curve     |
| Inflation        | `/fed/v1/inflation`                                                         | CPI inflation data          |
| Labor market     | `/fed/v1/labor-market`                                                      | Employment data             |
| Index aggregates | `/v2/aggs/ticker/{indicesTicker}/range/{multiplier}/{timespan}/{from}/{to}` | Index OHLCV bars            |

### Examples

**RSI:**
```python
# Relative Strength Index for TSLA
await call_external_tool(tool_name="finance_massive", source_id="finance", arguments={
    "pathname": "/v1/indicators/rsi/TSLA",
    "params": {"timespan": 21, "limit": 100}
})
```

**Options chain snapshot:**
```python
# Options chain snapshot for a ticker
await call_external_tool(tool_name="finance_massive", source_id="finance", arguments={
    "pathname": "/v3/snapshot/options/AAPL",
    "params": {"contract_type": "call", "limit": "10"}
})
```

**Tick-level trades:**
```python
# Tick-level NVDA trades during earnings release window
await call_external_tool(tool_name="finance_massive", source_id="finance", arguments={
    "pathname": "/v3/trades/NVDA",
    "params": {"timestamp.gte": "2024-11-20T21:00:00Z", "timestamp.lte": "2024-11-20T21:30:00Z", "limit": "1000", "sort": "timestamp", "order": "asc"}
})
```

**Macro-economic data:**
```python
# Treasury yield curve data
await call_external_tool(tool_name="finance_massive", source_id="finance", arguments={
    "pathname": "/fed/v1/treasury-yields",
    "params": {"date.gte": "2024-01-01", "limit": "50"}
})
```

**Important:**

- Always prefer specialized finance tools over raw API access for standard stock/ETF data
- The API key is injected automatically — do not pass `apiKey` in params
- Only GET requests are supported
- Invalid pathnames will be rejected

## Detailed Guides

- **market-data.md** - Fetching quotes, historical prices, handling multiple tickers
- **analysis.md** - DCF valuation, comparables, ratio analysis, portfolio metrics
- **reporting.md** - Formatting tables, charts, and investment reports