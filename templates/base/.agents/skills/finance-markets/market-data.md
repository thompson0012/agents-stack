# Market Data Guide

Finance tools are available via `list_external_tools`, `describe_external_tools`, and `call_external_tool` (requires authentication). You **must** call `describe_external_tools(source_id="finance", tool_names=[...])` before any `call_external_tool` call — the system enforces this.

## Reference Date → Parameter Mapping

| Tool                        | Parameter(s) from Reference Date                                                               |
| --------------------------- | ---------------------------------------------------------------------------------------------- |
| `finance_quotes`            | None — only use when reference date is today. Use `finance_ohlcv_histories` for past dates     |
| `finance_ohlcv_histories`   | `end_date_yyyy_mm_dd` = reference date                                                         |
| `finance_financials`        | `as_of_fiscal_year` (always required); `as_of_fiscal_quarter` (required for `period="quarter"`, omit for `period="annual"`) |
| `finance_earnings`          | `as_of_fiscal_year`, `as_of_fiscal_quarter` (always required)                                  |
| `finance_earnings_schedule` | `as_of_fiscal_year`, `as_of_fiscal_quarter` (always required, unless using calendar date mode) |

## Ticker Lookup

Always resolve company names to tickers before fetching data using `finance_tickers_lookup`. Resolves company names, user-provided tickers, stocks, ETFs, indexes, commodities, and crypto. Handles format variations (BRK.B vs BRK-B) and partial/fuzzy names. Full support for international exchanges (.F, .L, .KS, etc.). Standard market tickers may not resolve correctly—always use this tool first.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `queries` | `list[str]` | Yes | - | Array of search queries for any financial instrument. Pass through user's phrasing when possible. Example: for query 'what is the price of NVDA, Re... |

### Examples

```python
# Single company
await call_external_tool(tool_name="finance_tickers_lookup", source_id="finance", arguments={
    "queries": ["Tesla"]
})
```

```python
# Multiple companies
await call_external_tool(tool_name="finance_tickers_lookup", source_id="finance", arguments={
    "queries": ["Apple", "Microsoft", "Meta"]
})
```

**Handling ambiguity:** When lookup returns multiple results, present options to user or use context to disambiguate (e.g., "Meta the social media company" → META).

## Real-Time Quotes

Get current real-time quotes for stocks, cryptocurrencies, ETFs, or indices. Returns a markdown table with one row per symbol containing only the requested fields.

**Only use `finance_quotes` when the reference date is today.** For past reference dates, use `finance_ohlcv_histories` to get the closing price as of that date.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ticker_symbols` | `list[str]` | Yes | - | Array of ticker symbols from a prior tool call (prefer finance_tickers_lookup for ticker resolution). Examples: ["AAPL"], ["GOOGL", "META", "SNAP"]... |
| `fields` | `list[str]` | Yes | - | Required list of quote fields to include. Only request fields needed for the analysis. |

**Valid values:**

**`fields`** (QuoteField): `price`, `currency`, `change`, `changesPercentage`, `marketCap`, `pe`, `eps`, `volume`, `avgVolume`, `dayLow`, `dayHigh`, `yearLow`, `yearHigh`, `previousClose`, `open`, `dividendYieldTTM`, `afterHoursPrice`, `afterHoursChange`, `afterHoursPercentChange`

### Examples

**Basic quote:**
```python
# Basic quote
await call_external_tool(tool_name="finance_quotes", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "fields": ["price", "change", "changesPercentage"]
})
```

**Valuation snapshot:**
```python
# Valuation snapshot
await call_external_tool(tool_name="finance_quotes", source_id="finance", arguments={
    "ticker_symbols": ["AAPL", "MSFT", "GOOGL"],
    "fields": ["price", "marketCap", "pe", "eps", "dividendYieldTTM"]
})
```

**Trading activity:**
```python
# Trading activity
await call_external_tool(tool_name="finance_quotes", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "fields": ["price", "volume", "avgVolume", "dayLow", "dayHigh"]
})
```

## Historical Data (OHLCV)

Get historical price data for stocks, ETFs, crypto, or indices. Returns OHLCV (open, high, low, close, volume) as CSV for any date range. Use this for price history, candlestick charts, and as input for technical indicator calculations. Do NOT search for historical prices—this tool provides them directly.

**Always use the reference date as `end_date_yyyy_mm_dd`.** For past reference dates, this tool replaces `finance_quotes` for price lookups.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ticker_symbols` | `list[str]` | Yes | - | Array of ticker symbols from a prior tool call (prefer finance_tickers_lookup for ticker resolution). Examples: ["MSFT"], ["AAPL", "GOOGL", "MSFT"]... |
| `query` | `str` | Yes | - | Human-readable query describing what price history to fetch (e.g. "Apple stock price history" or "Compare AAPL and MSFT prices"). |
| `start_date_yyyy_mm_dd` | `str` | Yes | - | Start date in YYYY-MM-DD format (e.g. "2024-01-01"). |
| `end_date_yyyy_mm_dd` | `str` | Yes | - | End date in YYYY-MM-DD format (e.g. "2024-12-31"). |
| `time_interval` | `str` | No | None | Optional. Leave unspecified to auto-select optimal interval based on date range. Only specify if user explicitly requests a particular granularity ... |
| `fields` | `list[str]` | Yes | - | Required list of OHLCV price fields to include in the CSV. Only request fields needed for the analysis. |
| `extended_hours` | `bool` | No | False | Set to true to include pre-market and after-hours trading data. Only enable if the user specifically asks for extended hours or after-hours data. |

**Valid values:**

**`time_interval`** (time_interval): `1min`, `5min`, `15min`, `30min`, `1hour`, `4hour`, `1day`, `1week`, `1month`

**`fields`** (PriceField): `open`, `high`, `low`, `close`, `volume`

**`time_interval` values must match the enum exactly.** Common mistakes:

- `"weekly"` → use `"1week"`
- `"monthly"` → use `"1month"`
- `"daily"` → use `"1day"`
- `"hourly"` → use `"1hour"`

### Date Formats

Use ISO format: `YYYY-MM-DD`

### Examples

**Specific date range:**
```python
# Specific date range
await call_external_tool(tool_name="finance_ohlcv_histories", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "start_date_yyyy_mm_dd": "2024-01-01",
    "end_date_yyyy_mm_dd": "2024-06-30"
})
```

**Multiple tickers comparison:**
```python
# Multiple tickers comparison
await call_external_tool(tool_name="finance_ohlcv_histories", source_id="finance", arguments={
    "ticker_symbols": ["AAPL", "MSFT", "GOOGL"],
    "query": "Compare AAPL, MSFT, GOOGL prices",
    "start_date_yyyy_mm_dd": "2024-01-01",
    "end_date_yyyy_mm_dd": "2024-12-31",
    "fields": ["close"]
})
```

**YTD performance:**
```python
# YTD performance
await call_external_tool(tool_name="finance_ohlcv_histories", source_id="finance", arguments={
    "ticker_symbols": ["SPY", "AAPL"],
    "query": "SPY and AAPL YTD performance",
    "start_date_yyyy_mm_dd": "2024-01-01",
    "end_date_yyyy_mm_dd": "2024-12-31",
    "fields": ["close"]
})
```

```
# Calculate: (current_close - first_close) / first_close * 100
```

**Volatility analysis:**

```python
# Fetch daily data, then calculate:
# - Daily returns: (close[i] - close[i-1]) / close[i-1]
# - Annualized volatility: std(daily_returns) * sqrt(252)
```

## Holdings Data

Get holdings data for **US-listed stocks and ETFs only** using `finance_holdings`. Non-US tickers will return no data. Supports three types.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ticker_symbols` | `list[str]` | Yes | - | Array of ticker symbols from a prior tool call (prefer finance_tickers_lookup for ticker resolution). Examples: ["AAPL"], ["NVDA", "AMD", "INTC"], ... |
| `ticker_names` | `list[str]` | Yes | - | Array of company names corresponding to ticker_symbols. |
| `query` | `str` | Yes | - | The original user query about holdings information. |
| `holdings_types` | `list[str]` | No | [] | List of holdings types to retrieve. Can include multiple types. |
| `insider_transactions_months_lookback` | `str` | No | 1 | For insider transactions only: Filter to show only transactions from the last X months. If not specified, defaults to 1 month. Example: insider_tra... |

**Valid values:**

**`holdings_types`** (HoldingsType): `institutional_holders`, `insider_transactions`

### Examples

**ETF Constituents:**
```python
# ETF constituents
await call_external_tool(tool_name="finance_etf_holdings", source_id="finance", arguments={
    "ticker_symbols": ["SPY", "QQQ"],
    "ticker_names": ["SPDR S&P 500 ETF", "Invesco QQQ Trust"],
    "query": "What are the top holdings in SPY and QQQ?"
})
```

**Institutional Holders:**
```python
# Institutional holders
await call_external_tool(tool_name="finance_holdings", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "holdings_types": ["institutional_holders"]
})
```

**Insider Transactions:**
```python
# Insider transactions
await call_external_tool(tool_name="finance_holdings", source_id="finance", arguments={
    "ticker_symbols": ["NVDA"],
    "holdings_types": ["insider_transactions"],
    "insider_transactions_months_lookback": 3
})
```

**Use cases:**

- Portfolio overlap analysis (which stocks appear in multiple ETFs)
- Sector exposure calculation
- Tracking institutional ownership changes
- Monitoring insider buying/selling activity

## Financial Statements

Fetch financial statements (income statement, balance sheet, cash flow) using `finance_financials`. Specify metrics by statement type—only statements with requested metrics are fetched.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ticker_symbols` | `list[str]` | Yes | - | Array of ticker symbols from a prior tool call (prefer finance_tickers_lookup for ticker resolution). Examples: ["NVDA"], ["UNH", "CI", "HUM"], ["R... |
| `period` | `str` | Yes | - | Reporting period. |
| `as_of_fiscal_year` | `str` | No | None | The most recent fiscal year to include. Data goes backward from this year. Omit to use most recent available data. |
| `as_of_fiscal_quarter` | `str` | No | None | The most recent fiscal quarter to include (1-4). Data goes backward from this quarter. Only used with quarter period. |
| `limit` | `int` | No | 1 | Number of periods to fetch going backward from as_of_fiscal_year (or from most recent if omitted) |
| `income_statement_metrics` | `list[str]` | Yes | - | Revenue, profitability, and earnings metrics. |
| `balance_sheet_metrics` | `list[str]` | Yes | - | Assets, liabilities, and equity metrics. |
| `cash_flow_metrics` | `list[str]` | Yes | - | Operating, investing, and financing cash flows. |

**Valid values:**

**`period`** (StatementPeriod): `annual`, `quarter`, `ttm`

**`income_statement_metrics`** (IncomeStatementFields): `revenue`, `costOfRevenue`, `grossProfit`, `researchAndDevelopmentExpenses`, `generalAndAdministrativeExpenses`, `sellingAndMarketingExpenses`, `sellingGeneralAndAdministrativeExpenses`, `otherExpenses`, `operatingExpenses`, `costAndExpenses`, `netInterestIncome`, `interestIncome`, `interestExpense`, `depreciationAndAmortization`, `ebitda`, `ebitdaRatio`, `ebit`, `nonOperatingIncomeExcludingInterest`, `operatingIncome`, `totalOtherIncomeExpensesNet`, `incomeBeforeTax`, `incomeTaxExpense`, `netIncomeFromContinuingOperations`, `netIncomeFromDiscontinuedOperations`, `otherAdjustmentsToNetIncome`, `netIncome`, `netIncomeDeductions`, `bottomLineNetIncome`, `eps`, `epsDiluted`, `weightedAverageSharesOutstanding`, `weightedAverageSharesOutstandingDiluted`

**`balance_sheet_metrics`** (BalanceSheetFields): `cashAndCashEquivalents`, `shortTermInvestments`, `cashAndShortTermInvestments`, `netReceivables`, `accountsReceivables`, `otherReceivables`, `inventory`, `prepaidExpenses`, `otherCurrentAssets`, `totalCurrentAssets`, `propertyPlantEquipmentNet`, `goodwill`, `intangibleAssets`, `goodwillAndIntangibleAssets`, `longTermInvestments`, `taxAssets`, `otherNonCurrentAssets`, `totalNonCurrentAssets`, `otherAssets`, `totalAssets`, `totalPayables`, `accountsPayables`, `otherPayables`, `accruedExpenses`, `shortTermDebt`, `capitalLeaseObligationsCurrent`, `taxPayables`, `deferredRevenue`, `otherCurrentLiabilities`, `totalCurrentLiabilities`, `longTermDebt`, `capitalLeaseObligationsNonCurrent`, `deferredRevenueNonCurrent`, `deferredTaxLiabilitiesNonCurrent`, `otherNonCurrentLiabilities`, `totalNonCurrentLiabilities`, `otherLiabilities`, `capitalLeaseObligations`, `totalLiabilities`, `treasuryStock`, `preferredStock`, `commonStock`, `retainedEarnings`, `additionalPaidInCapital`, `accumulatedOtherComprehensiveIncomeLoss`, `otherStockholdersEquity`, `totalStockholdersEquity`, `totalEquity`, `minorityInterest`, `totalLiabilitiesAndTotalEquity`, `totalInvestments`, `totalDebt`, `netDebt`

**`cash_flow_metrics`** (CashFlowFields): `netIncome`, `depreciationAndAmortization`, `deferredIncomeTax`, `stockBasedCompensation`, `changeInWorkingCapital`, `accountsReceivables`, `inventory`, `accountsPayables`, `otherWorkingCapital`, `otherNonCashItems`, `netCashProvidedByOperatingActivities`, `investmentsInPropertyPlantAndEquipment`, `acquisitionsNet`, `purchasesOfInvestments`, `salesMaturitiesOfInvestments`, `otherInvestingActivities`, `netCashProvidedByInvestingActivities`, `netDebtIssuance`, `longTermNetDebtIssuance`, `shortTermNetDebtIssuance`, `netStockIssuance`, `netCommonStockIssuance`, `commonStockIssuance`, `commonStockRepurchased`, `netPreferredStockIssuance`, `netDividendsPaid`, `commonDividendsPaid`, `preferredDividendsPaid`, `otherFinancingActivities`, `netCashProvidedByFinancingActivities`, `effectOfForexChangesOnCash`, `netChangeInCash`, `cashAtEndOfPeriod`, `cashAtBeginningOfPeriod`, `operatingCashFlow`, `capitalExpenditure`, `freeCashFlow`, `incomeTaxesPaid`, `interestPaid`

**Metric names must match the enum exactly.** Common mistakes:

- `weightedAverageShsOut` → use `weightedAverageSharesOutstanding`
- `weightedAverageShsOutDil` → use `weightedAverageSharesOutstandingDiluted`
- `accountPayables` → use `accountsPayables`
- `dividendsPaid` → use `netDividendsPaid`, `commonDividendsPaid`, or `preferredDividendsPaid`

### Field Formats

- Ratio fields (`ebitdaRatio`, etc.) are decimals: 0.65 = 65%
- `eps`/`epsDiluted` are currency per share: 0.39 = $0.39
- `weightedAverageSharesOutstanding` fields are raw counts
- All other numeric fields are raw currency in `reportedCurrency` (not abbreviated)

### Examples

**Current Data (always pass as_of from reference date):**
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

**Apple's last 5 years FCF:**
```python
# Apple's last 5 years FCF
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "period": "annual",
    "as_of_fiscal_year": 2025,
    "limit": 5,
    "cash_flow_metrics": ["freeCashFlow"]
})
```

**Historical Data (as_of from explicit past reference date):**
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

**Cross-Statement:**
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

**TTM (Trailing Twelve Months):**
```python
# NVDA TTM gross profit
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["NVDA"],
    "period": "ttm",
    "income_statement_metrics": ["grossProfit"]
})
```

**Growth Calculations (fetch multiple periods to compare):**
```python
# Apple YoY revenue growth
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "period": "annual",
    "as_of_fiscal_year": 2025,
    "limit": 2,
    "income_statement_metrics": ["revenue"]
})
```

```
# Calculate: (current - previous) / previous
```

**Derived Metrics (fetch component fields for calculation):**
```python
# Apple debt-to-equity ratio
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "period": "quarter",
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1,
    "limit": 1,
    "balance_sheet_metrics": ["totalDebt", "totalStockholdersEquity"]
})
```

```
# Calculate: totalDebt / totalStockholdersEquity
```

## Earnings Data

Get earnings transcripts and historical earnings metrics using `finance_earnings`. Three usage modes.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ticker_symbol` | `str` | Yes | - | Ticker symbol from a prior tool call (prefer finance_tickers_lookup for ticker resolution). Examples: 'TSLA', 'GOOGL', 'JPM'. |
| `query` | `str` | Yes | - | Human-readable description of the earnings data request |
| `as_of_fiscal_quarter` | `str` | No | None | The most recent fiscal quarter to include (1-4). Data goes backward from this quarter. |
| `as_of_fiscal_year` | `str` | No | None | The most recent fiscal year to include. Data goes backward from this year. Omit to use most recent available data. |
| `limit` | `int` | No | 1 | Number of earnings periods to fetch going backward from as_of period (or from most recent if omitted) |
| `data_types` | `list[str]` | No | ['earnings_history'] | Types of earnings data to retrieve. |

**Valid values:**

**`data_types`** (EarningsDataType): `transcript_full`, `earnings_history`

### Data Types

| Type               | Description                                                 | When to Use                            |
| ------------------ | ----------------------------------------------------------- | -------------------------------------- |
| `transcript_full`  | Full earnings call transcript                               | Earnings call content and analysis     |
| `earnings_history` | Revenue/EPS actuals vs estimates, post-earnings price moves | Beat/miss analysis, historical metrics |

### Examples

**Current Data (always pass as_of from reference date):**
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

**Apple's last 3 earnings calls:**
```python
# Apple's last 3 earnings calls
await call_external_tool(tool_name="finance_earnings", source_id="finance", arguments={
    "ticker_symbol": "AAPL",
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1,
    "limit": 3,
    "data_types": ["transcript_full"]
})
```

**Historical Data (as_of from explicit past reference date):**
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

**Google earnings from 2022 back 4 quarters:**
```python
# Google earnings from 2022 back 4 quarters
await call_external_tool(tool_name="finance_earnings", source_id="finance", arguments={
    "ticker_symbol": "GOOGL",
    "as_of_fiscal_year": 2022,
    "as_of_fiscal_quarter": 4,
    "limit": 4,
    "data_types": ["transcript_full"]
})
```

**Earnings Metrics Only:**
```python
# AAPL earnings beat/miss history
await call_external_tool(tool_name="finance_earnings", source_id="finance", arguments={
    "ticker_symbol": "AAPL",
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1,
    "data_types": ["earnings_history"]
})
```

## Earnings Schedule

Look up earnings release dates and reporting status using `finance_earnings_schedule`. Always pass `as_of_fiscal_year`/`as_of_fiscal_quarter` derived from the reference date, except in calendar date mode (`start_date`/`end_date`).

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `ticker_symbols` | `list[str]` | No | [] | Array of ticker symbols from a prior tool call (prefer finance_tickers_lookup for ticker resolution). Examples: ["MSFT"], ["GOOGL", "META", "SNAP"]... |
| `direction` | `str` | No | None | Historical or future earnings dates. Omit when using date range or fiscal period filters. |
| `start_date` | `str` | No | None | Start of date range (YYYY-MM-DD). Use for calendar-based queries like 'this week' or 'next month'. |
| `end_date` | `str` | No | None | End of date range (YYYY-MM-DD). Use with start_date for calendar-based queries. |
| `as_of_fiscal_year` | `str` | No | None | Fiscal year to look up. Use for period-based queries like 'Q4 2024'. |
| `as_of_fiscal_quarter` | `str` | No | None | Fiscal quarter to look up (1-4). Use with as_of_fiscal_year for specific quarter queries. |
| `limit` | `int` | No | 1 | Number of earnings events to return per ticker. Use >1 for queries like 'last 4 quarters'. |

**Mode rules:** Calendar date mode (`start_date`/`end_date`) and fiscal period mode (`as_of_fiscal_year`/`as_of_fiscal_quarter`) are mutually exclusive. Omit both for default behavior (next upcoming + most recent past).

### Examples

**Calendar (all companies in date range):**
```python
# All earnings this week
await call_external_tool(tool_name="finance_earnings_schedule", source_id="finance", arguments={
    "ticker_symbols": [],
    "start_date": "2025-02-03",
    "end_date": "2025-02-07"
})
```

**Ticker + Date Range:**
```python
# Apple earnings in February
await call_external_tool(tool_name="finance_earnings_schedule", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "start_date": "2025-02-01",
    "end_date": "2025-02-28"
})
```

**Ticker + Fiscal Period:**
```python
# Apple Q4 2024 earnings date
await call_external_tool(tool_name="finance_earnings_schedule", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "as_of_fiscal_year": 2024,
    "as_of_fiscal_quarter": 4
})
```

**Default (next upcoming + most recent past):**
```python
# When does Apple report next?
await call_external_tool(tool_name="finance_earnings_schedule", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "as_of_fiscal_year": 2025,
    "as_of_fiscal_quarter": 1
})
```

**Use cases:**

- "When does AAPL report?" → default mode with ticker
- "Earnings this week" → calendar mode with empty ticker list
- "Did NVDA already report Q3?" → fiscal period mode
- "Last 4 quarters of MSFT earnings dates" → default mode with limit=4

For detailed earnings analysis (transcripts, EPS, beat/miss), use `finance_earnings` instead.
