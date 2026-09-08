# Pandas Window Functions

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.2**

Time-series smoothing, cumulative metrics, window aggregation, partitioned ranks, and lag/lead differences in Pandas.

---

## Key Patterns

1. **Rolling Windows (`.rolling()`)**: Moving averages, standard deviations, and dynamic min/max volatility bounds.
2. **Expanding Windows (`.expanding()`)**: Lifetime cumulative metrics (`cumsum`, `cummax`, running mean).
3. **Exponential Smoothing (`.ewm()`)**: Exponentially weighted moving average with customizable smoothing span.
4. **Partitioned Ranking (`.rank()`)**: Dense/min/max ranking partitioned across category groups (matching SQL `RANK() OVER (PARTITION BY ...)`).
5. **Lag, Lead & Delta (`.shift()`, `.pct_change()`)**: Period-over-period returns and offset comparisons.

---

## Running Demonstrations

Run all Window demonstrations:
```bash
python3 -m pandas_lib.window_functions.run_examples --demo all
```

Or run targeted operations:
```bash
python3 -m pandas_lib.window_functions.run_examples --demo rolling
python3 -m pandas_lib.window_functions.run_examples --demo expanding
python3 -m pandas_lib.window_functions.run_examples --demo ema
python3 -m pandas_lib.window_functions.run_examples --demo ranking
python3 -m pandas_lib.window_functions.run_examples --demo returns
```
