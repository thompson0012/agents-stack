# Financial Reporting Guide

## Formatting Conventions

### Currency Values

- Under $1: `$0.45`
- Under $1,000: `$150.25`
- Thousands: `$12.5K`
- Millions: `$1.2M`
- Billions: `$150.5B`
- Trillions: `$2.1T`

### Percentages

- Price changes: `+2.5%` or `-1.3%` (include sign)
- Ratios/yields: `3.5%` (no sign for static values)
- Growth rates: `+15% YoY`

### Large Numbers

Use K/M/B/T suffixes for readability:

- Revenue: `$394.3B` not `$394,328,000,000`
- Volume: `52.3M` not `52,300,000`

## Table Formats

### Quote Summary

```markdown
| Ticker |   Price | Change | Market Cap |  P/E | Div Yield |
| ------ | ------: | -----: | ---------: | ---: | --------: |
| AAPL   | $178.50 |  +1.2% |      $2.8T | 28.5 |      0.5% |
| MSFT   | $385.20 |  -0.3% |      $2.9T | 35.2 |      0.8% |
```

### Financial Comparison

```markdown
| Metric        |  AAPL |  MSFT | GOOGL | Industry Avg |
| ------------- | ----: | ----: | ----: | -----------: |
| Revenue (TTM) | $394B | $236B | $307B |            - |
| Net Margin    | 25.3% | 34.1% | 24.0% |        22.5% |
| ROE           |  147% |   35% |   25% |          28% |
| Debt/Equity   |   1.8 |   0.4 |   0.1 |          0.8 |
```

### Historical Performance

```markdown
| Period  | Return | vs S&P 500 |
| ------- | -----: | ---------: |
| 1 Month |  +5.2% |      +2.1% |
| 3 Month | +12.3% |      +4.5% |
| YTD     | +45.2% |     +20.1% |
| 1 Year  | +52.1% |     +18.3% |
```

## Chart Recommendations

When user needs visualizations, describe the chart type and data:

### Price Charts

- **Line chart**: Single stock price over time
- **Candlestick**: OHLC data for trading analysis
- **Area chart**: Cumulative returns or portfolio value

### Comparisons

- **Bar chart**: Comparing metrics across companies
- **Grouped bar**: Multiple metrics per company
- **Scatter plot**: Two variables (e.g., P/E vs Growth)

### Distributions

- **Histogram**: Return distribution
- **Box plot**: Comparing volatility across assets

## Report Templates

### Quick Stock Summary

```
## [Company Name] ([TICKER])

**Current Price:** $XXX.XX (+X.X%)
**Market Cap:** $X.XB | **P/E:** XX.X | **Div Yield:** X.X%

### Today's Trading
- Open: $XXX.XX | High: $XXX.XX | Low: $XXX.XX
- Volume: X.XM (Avg: X.XM)

### 52-Week Range
$XXX.XX — $XXX.XX (currently at XX% of range)

### Key Metrics
| Metric | Value | vs Sector |
|--------|------:|----------:|
| P/E Ratio | XX.X | +X.X |
| EV/EBITDA | XX.X | -X.X |
| Profit Margin | XX.X% | +X.X% |
```

### Comparative Analysis

```
## Peer Comparison: [Sector/Industry]

### Valuation
| Company | P/E | EV/EBITDA | P/S | P/B |
|---------|----:|----------:|----:|----:|
| [Company A] | ... | ... | ... | ... |

### Profitability
| Company | Gross Margin | Op Margin | Net Margin | ROE |
|---------|-------------:|-----------:|-----------:|----:|
| [Company A] | ... | ... | ... | ... |

### Key Takeaways
1. [Insight about valuation]
2. [Insight about margins]
3. [Recommendation or observation]
```

### DCF Summary

```
## DCF Valuation: [TICKER]

### Assumptions
- Discount Rate (WACC): X.X%
- Terminal Growth Rate: X.X%
- Projection Period: X years

### Free Cash Flow Projections
| Year | FCF | Growth | PV of FCF |
|------|----:|-------:|----------:|
| 2025 | $X.XB | +X% | $X.XB |
| ... | ... | ... | ... |

### Valuation Summary
| Component | Value |
|-----------|------:|
| PV of FCF | $X.XB |
| PV of Terminal Value | $X.XB |
| Enterprise Value | $X.XB |
| Less: Net Debt | ($X.XB) |
| **Equity Value** | **$X.XB** |
| Shares Outstanding | X.XB |
| **Implied Share Price** | **$XXX.XX** |

**Current Price:** $XXX.XX
**Upside/Downside:** +XX% / -XX%
```

## Best Practices

1. **Right-align numbers** in tables for easy comparison
2. **Include context** - absolute values need benchmarks (vs sector, vs history)
3. **Highlight key insights** - don't just dump data, tell the user what matters
4. **Use consistent precision** - don't mix `$1.234B` with `$2B`
5. **Date your data** - Always state the reference date used: "As of Jan 15, 2025" or "TTM ending Q3 2024". Every table and report should make clear what reference date drove the `as_of` parameters
6. **Cite limitations** - note if data is delayed, estimated, or incomplete
7. **Cite sources** - Link each ticker to `https://perplexity.ai/finance/<TICKER>` so users can verify the data
