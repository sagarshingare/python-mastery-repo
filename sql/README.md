# SQL Mastery Module

> **Learning Path**: [Stage 04: SQL & Relational Databases](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-04-sql--relational-databases-sql) (Prerequisite: [Stage 01: Core Python](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python))

Comprehensive relational database concepts, query optimization guidelines, and executable in-memory SQLite demonstration modules covering fundamentals, joins, window functions, CTEs, indexing, and advanced patterns.

---

## Step-by-Step Learning Sequence

| Step | Subfolder | Implementation & Reference | Focus Area |
|:---|:---|:---|:---|
| **Step 4.1** | [`basics/`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/basics) | [`fundamentals.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/basics/fundamentals.py)<br>[`sql_fundamentals.md`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/basics/sql_fundamentals.md) | DDL schema with constraints, DML CRUD, filtering, aggregations, GROUP BY/HAVING, pagination |
| **Step 4.2** | [`joins/`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/joins) | [`join_operations.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/joins/join_operations.py)<br>[`join_patterns.md`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/joins/join_patterns.md) | INNER, LEFT, ANTI-JOIN, SELF JOIN hierarchy, CROSS JOIN, simulated FULL OUTER JOIN |
| **Step 4.3** | [`cte/`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/cte) | [`cte_operations.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/cte/cte_operations.py)<br>[`cte_patterns.md`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/cte/cte_patterns.md) | Modular multi-stage pipelines, recursive number series, recursive org chart traversal |
| **Step 4.4** | [`window_functions/`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/window_functions) | [`window_operations.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/window_functions/window_operations.py)<br>[`window_functions.md`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/window_functions/window_functions.md) | ROW_NUMBER, RANK, DENSE_RANK, NTILE, LAG/LEAD growth, moving average frames |
| **Step 4.5** | [`advanced_queries/`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/advanced_queries) | [`advanced_operations.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/advanced_queries/advanced_operations.py)<br>[`advanced_patterns.md`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/advanced_queries/advanced_patterns.md) | Conditional aggregation pivot, unpivoting, atomic UPSERT, JSON extraction, Gaps & Islands |
| **Step 4.6** | [`optimization/`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/optimization) | [`query_optimizer.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/optimization/query_optimizer.py)<br>[`query_optimization.md`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/optimization/query_optimization.md) | EXPLAIN plans, B-Tree and composite indexing, leftmost prefix rule, sargability |
| **Step 4.7** | Root Runner | [`run_examples.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/run_examples.py)<br>[`examples.py`](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/examples.py) | Unified modular CLI runner executing demonstrations live with formatted outputs |

---

## Architecture Overview

```
sql/
├── basics/
│   ├── __init__.py
│   ├── fundamentals.py          # DDL, CRUD, dynamic filtering, aggregations, pagination
│   ├── run_examples.py          # CLI runner (--demo [crud, filtering, aggregation, pagination, all])
│   ├── examples.py              # Entry point alias
│   ├── sql_fundamentals.md      # Reference documentation
│   └── README.md                # Step 4.1 guide
├── joins/
│   ├── __init__.py
│   ├── join_operations.py       # INNER, LEFT, ANTI, SELF, CROSS, FULL OUTER simulation
│   ├── run_examples.py          # CLI runner (--demo [inner, left, anti, self, cross, full, all])
│   ├── examples.py              # Entry point alias
│   ├── join_patterns.md         # Reference documentation
│   └── README.md                # Step 4.2 guide
├── cte/
│   ├── __init__.py
│   ├── cte_operations.py        # Modular pipelines, sequence generators, recursive tree walkers
│   ├── run_examples.py          # CLI runner (--demo [modular, sequence, hierarchy, all])
│   ├── examples.py              # Entry point alias
│   ├── cte_patterns.md          # Reference documentation
│   └── README.md                # Step 4.3 guide
├── window_functions/
│   ├── __init__.py
│   ├── window_operations.py     # Ranking, top-earners, LAG/LEAD MoM growth, moving frames
│   ├── run_examples.py          # CLI runner (--demo [ranking, top_earners, growth, moving, all])
│   ├── examples.py              # Entry point alias
│   ├── window_functions.md      # Reference documentation
│   └── README.md                # Step 4.4 guide
├── advanced_queries/
│   ├── __init__.py
│   ├── advanced_operations.py   # Pivoting, unpivoting, atomic UPSERT, JSON querying, Gaps & Islands
│   ├── run_examples.py          # CLI runner (--demo [pivot, unpivot, upsert, json, gaps_islands, all])
│   ├── examples.py              # Entry point alias
│   ├── advanced_patterns.md     # Reference documentation
│   └── README.md                # Step 4.5 guide
├── optimization/
│   ├── __init__.py
│   ├── query_optimizer.py       # EXPLAIN plan inspector, B-Tree & composite indexing, sargability
│   ├── run_examples.py          # CLI runner (--demo [explain, indexing, composite, sargability, all])
│   ├── examples.py              # Entry point alias
│   ├── query_optimization.md    # Reference documentation
│   └── README.md                # Step 4.6 guide
├── run_examples.py              # Master CLI runner (--submodule [basics, joins, cte, ...])
├── examples.py                  # Convenience entry point
├── __init__.py
└── README.md
```

---

## Running Demonstrations

### 1. Unified Master Demonstration
Execute all SQL demonstrations across all 6 submodules:
```bash
python3 -m sql.run_examples --submodule all
# or
python3 -m sql.examples
```

Or target any specific submodule:
```bash
python3 -m sql.run_examples --submodule basics
python3 -m sql.run_examples --submodule joins
python3 -m sql.run_examples --submodule cte
python3 -m sql.run_examples --submodule window
python3 -m sql.run_examples --submodule advanced
python3 -m sql.run_examples --submodule optimization
```

### 2. Direct Submodule Runners
Target individual operations within any subfolder:
```bash
# SQL Fundamentals
python3 -m sql.basics.run_examples --demo crud
python3 -m sql.basics.run_examples --demo pagination

# Relational Joins
python3 -m sql.joins.run_examples --demo self
python3 -m sql.joins.run_examples --demo anti

# Common Table Expressions (CTEs)
python3 -m sql.cte.run_examples --demo hierarchy

# Analytical Window Functions
python3 -m sql.window_functions.run_examples --demo growth

# Advanced SQL Patterns
python3 -m sql.advanced_queries.run_examples --demo gaps_islands

# Query Optimization & Indexing
python3 -m sql.optimization.run_examples --demo composite
```
