---
name: data-exploration
description: Use when profiling an unfamiliar dataset, assessing data quality, documenting schema, or searching for relationships, anomalies, and useful segmentation patterns.
---

# Data Exploration

## Overview
Explore unfamiliar data in a fixed order: structure first, column behavior second, relationships third, and interpretation last. The goal is to understand what the data can honestly support before drawing conclusions.

## When to Use
Use this skill when you need to:
- profile a table or dataset before analysis
- assess completeness, consistency, freshness, or accuracy
- infer grain, keys, and likely joins
- document schema for other analysts
- look for distributions, trends, anomalies, or segments

Do not use it for final causal claims or polished reporting before the data has been profiled.

## Workflow
1. Establish table-level structure.
   - Row count, column count, grain, candidate primary key, update window, and date coverage.
   - Classify columns as identifier, dimension, metric, temporal, text, boolean, or structural.
2. Profile columns systematically.
   - Measure nulls, distinctness, and frequent values for every column.
   - Add type-specific checks for numeric, string, date, and boolean columns.
3. Assess data quality.
   - Look for completeness gaps, formatting inconsistency, placeholder values, impossible values, and stale timestamps.
4. Discover relationships.
   - Identify foreign-key candidates, hierarchies, redundant fields, derived columns, and strong correlations.
5. Look for patterns.
   - Check distributions, time trends, seasonality, change points, anomalies, and meaningful segments.
6. Document what is true.
   - Record schema, relationships, known issues, and common query patterns.

## Quick Reference

### Column Profiling
| Column type | Minimum checks |
| --- | --- |
| All columns | null count/rate, distinct count, cardinality ratio, most common values, least common values |
| Numeric | min, max, mean, median, standard deviation, p1/p5/p25/p75/p95/p99, zero count, unexpected negative count |
| String | min/max/avg length, empty strings, format patterns, case consistency, leading/trailing whitespace |
| Date/Timestamp | min/max date, nulls, future dates, time distribution, missing periods |
| Boolean | true count, false count, null count, true rate |

### Completeness Bands
| Band | Rule | Interpretation |
| --- | --- | --- |
| Complete | >99% non-null | generally safe |
| Mostly complete | 95-99% | inspect null mechanism |
| Incomplete | 80-95% | understand business impact |
| Sparse | <80% | risky without mitigation |

## Quality Checks
### Consistency
Look for:
- the same concept represented in multiple formats
- numbers stored as strings
- mixed date formats
- referential mismatches between parent and child data
- cross-column contradictions such as `status = completed` with no completion timestamp

### Accuracy Red Flags
Investigate:
- placeholders like `0`, `-1`, `999999`, `N/A`, `TBD`, `test`
- suspicious defaults with extreme frequency
- impossible values
- stale operational data
- round-number bias that suggests estimation

### Timeliness
Confirm:
- last update time
- expected refresh cadence
- lag between event time and load time
- missing periods in time-series data

## Pattern Discovery
### Distribution Analysis
Classify numeric behavior as roughly normal, skewed, bimodal, power-law, or suspiciously uniform.

### Temporal Analysis
Check for:
- trends
- seasonality
- day-of-week or holiday effects
- change points
- isolated anomalies

### Segmentation
Start with categorical fields that have a manageable number of distinct values, then compare metric behavior across segments.

### Correlation
Flag strong correlations for investigation, but do not treat them as causal findings.

## Schema Documentation Template
Use this structure when handing the dataset to others:

```markdown
## Table: schema.table_name

**Description**: What the table represents
**Grain**: One row per ...
**Primary Key**: column(s)
**Row Count**: approximate count with date
**Update Frequency**: real-time / hourly / daily / weekly
**Owner**: responsible team or person

### Key Columns
| Column | Type | Description | Example Values | Notes |
| --- | --- | --- | --- | --- |

### Relationships
- joins to ...

### Known Issues
- ...

### Common Query Patterns
- ...
```

## Common Mistakes
- Jumping into charts before confirming grain and keys
- Treating nulls as random when they are actually business-significant
- Ignoring placeholder or default values that dominate a field
- Declaring causation from correlation
- Documenting columns without noting known join paths or data quality traps

## Exploration Checklist
- [ ] Grain and candidate key identified
- [ ] Columns classified by role
- [ ] Column-level profiling completed
- [ ] Quality risks recorded
- [ ] Likely joins and relationships mapped
- [ ] Time coverage and freshness checked
- [ ] Schema notes written for reuse
