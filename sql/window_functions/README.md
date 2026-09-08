# SQL Window Functions

> **Learning Path**: [Stage 04: SQL & Relational Databases](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-04-sql--relational-databases-sql) — **Step 4.4** (Prerequisite: [Step 4.3: Common Table Expressions](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/cte))

Advanced analytical and time-series querying using `OVER (PARTITION BY ... ORDER BY ...)`: ranking variants, top-N group filtering, prior/next value lookups via `LAG` and `LEAD`, cumulative running totals, and sliding window frame aggregations.

---

## Window Function Capabilities

| Category | Functions | Production Application |
|:---|:---|:---|
| **Ranking** | `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` | Top-earner leaderboards, deduplication of log event streams |
| **Bucketing** | `NTILE(k)` | Quartile performance segmentation, tier assignment |
| **Value Offsets** | `LAG()`, `LEAD()` | Period-over-period revenue growth, user session inactivity duration |
| **Sliding Frames** | `ROWS BETWEEN ... PRECEDING AND ...` | 7-day or 3-month moving averages, rolling risk exposure |

---

## Running Demonstrations

Run all Window Functions demonstrations:
```bash
python3 -m sql.window_functions.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m sql.window_functions.run_examples --demo ranking
python3 -m sql.window_functions.run_examples --demo top_earners
python3 -m sql.window_functions.run_examples --demo growth
python3 -m sql.window_functions.run_examples --demo moving
```
