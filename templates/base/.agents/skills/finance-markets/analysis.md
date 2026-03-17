# Financial Analysis Guide

Before calling any finance tool, you **must** call `describe_external_tools(source_id="finance", tool_names=[...])` — the system enforces this.

## Fetching Financial Statements

### Statement Types

| Type            | Contains                                   |
| --------------- | ------------------------------------------ |
| `income`        | Revenue, expenses, net income, EPS         |
| `balance_sheet` | Assets, liabilities, equity                |
| `cash_flow`     | Operating, investing, financing cash flows |

### Basic Request

```python
# Historical financials for DCF
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "period": "annual",
    "as_of_fiscal_year": 2025,
    "limit": 5,
    "income_statement_metrics": ["revenue", "netIncome"],
    "cash_flow_metrics": ["operatingCashFlow", "capitalExpenditure", "freeCashFlow"]
})
```

### Period Formats

- Annual: `"2024"`, `"2023"`
- Quarterly: `"2024-Q1"`, `"2024-Q2"`
- TTM (trailing twelve months): `"TTM"`

## Ratio Analysis

### Profitability Ratios

Calculate from income statement and balance sheet:

```
Gross Margin = Gross Profit / Revenue
Operating Margin = Operating Income / Revenue
Net Margin = Net Income / Revenue
ROE = Net Income / Shareholders Equity
ROA = Net Income / Total Assets
ROIC = NOPAT / Invested Capital
```

### Liquidity Ratios

```
Current Ratio = Current Assets / Current Liabilities
Quick Ratio = (Current Assets - Inventory) / Current Liabilities
Cash Ratio = Cash / Current Liabilities
```

### Leverage Ratios

```
Debt-to-Equity = Total Debt / Shareholders Equity
Debt-to-EBITDA = Total Debt / EBITDA
Interest Coverage = EBIT / Interest Expense
```

### Calculating Ratios

Fetch the required metrics via `finance_financials`, then calculate ratios locally:

```python
# ROE calculation data
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "period": "annual",
    "as_of_fiscal_year": 2025,
    "limit": 1,
    "income_statement_metrics": ["netIncome"],
    "balance_sheet_metrics": ["totalStockholdersEquity"]
})
```

```
# Calculate ROE locally from the returned data
# ROE = Net Income / Shareholders Equity
```

## Comparable Company Analysis

### Step 1: Identify Peer Group

Identify peer companies based on sector and size (screener is currently unavailable).
Use domain knowledge or external research to select comparable tickers.

### Step 2: Fetch Valuation Multiples

Use `finance_quotes` only when the reference date is today. For past reference dates, use `finance_ohlcv_histories` for price data and `finance_financials` for EPS/market cap.

```python
# Valuation snapshot
await call_external_tool(tool_name="finance_quotes", source_id="finance", arguments={
    "ticker_symbols": ["AAPL", "MSFT", "GOOGL"],
    "fields": ["price", "marketCap", "pe", "eps", "dividendYieldTTM"]
})
```

### Step 3: Fetch Growth Metrics

```python
# Peer group revenue comparison
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL", "MSFT", "GOOGL", "META"],
    "period": "annual",
    "as_of_fiscal_year": 2025,
    "limit": 3,
    "income_statement_metrics": ["revenue"]
})
```

```
# Calculate revenue growth YoY for each
```

### Common Multiples

| Multiple  | Formula                   | Best For                     |
| --------- | ------------------------- | ---------------------------- |
| P/E       | Price / EPS               | Profitable companies         |
| EV/EBITDA | Enterprise Value / EBITDA | Capital-intensive businesses |
| P/S       | Price / Revenue per Share | High-growth, unprofitable    |
| P/B       | Price / Book Value        | Asset-heavy (banks, REITs)   |
| PEG       | P/E / EPS Growth Rate     | Growth-adjusted valuation    |

## DCF Valuation

### Required Inputs

1. **Free Cash Flow projection** - from historical cash flow statements
2. **Discount rate (WACC)** - calculate or use industry average
3. **Terminal growth rate** - typically 2-3% (GDP growth)
4. **Projection period** - typically 5-10 years

### Workflow

```python
# Historical financials for DCF
await call_external_tool(tool_name="finance_financials", source_id="finance", arguments={
    "ticker_symbols": ["AAPL"],
    "period": "annual",
    "as_of_fiscal_year": 2025,
    "limit": 5,
    "income_statement_metrics": ["revenue", "netIncome"],
    "cash_flow_metrics": ["operatingCashFlow", "capitalExpenditure", "freeCashFlow"]
})
```

```python
# 2. Calculate historical FCF locally
# FCF = Operating Cash Flow - CapEx

# 3. Project future FCF (use growth assumptions)

# 4. Calculate present value locally
# Example calculation:
# wacc = 0.10
# fcf_projections = [10e9, 11e9, 12e9, 13e9, 14e9]
# terminal_value = 200e9
# pv = sum(fcf / (1 + wacc)**i for i, fcf in enumerate(fcf_projections, 1))
# pv += terminal_value / (1 + wacc)**5
```

### Terminal Value

Gordon Growth Model:

```
Terminal Value = FCF_final * (1 + g) / (r - g)
```

Where:

- `g` = perpetual growth rate (2-3%)
- `r` = discount rate (WACC)

## Statistical Analysis

For statistical analysis, fetch price history via `finance_ohlcv_histories` and perform calculations locally:

```python
# Correlation analysis data
await call_external_tool(tool_name="finance_ohlcv_histories", source_id="finance", arguments={
    "ticker_symbols": ["AAPL", "MSFT"],
    "query": "AAPL and MSFT price correlation",
    "start_date_yyyy_mm_dd": "2024-01-01",
    "end_date_yyyy_mm_dd": "2024-12-31",
    "fields": ["close"]
})
```

```python
# 2. Calculate locally:
# - Daily returns: (close[i] - close[i-1]) / close[i-1]
# - Correlation between assets
# - Annualized volatility: std(daily_returns) * sqrt(252)
# - Beta: covariance(stock, benchmark) / variance(benchmark)
```

**Common analyses:**

- Correlation between assets
- Beta calculation (regression vs benchmark)
- Sharpe ratio
- Portfolio variance
- Moving averages and technical indicators
