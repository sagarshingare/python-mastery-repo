# SQL Join Patterns

> **Learning Path**: [Stage 04: SQL & Relational Databases](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-04-sql--relational-databases-sql) — **Step 4.2** (Prerequisite: [Step 4.1: SQL Fundamentals](file:///Users/sagarshingare/Documents/python-mastery-repo/sql/basics))

Relational joining techniques: `INNER JOIN`, `LEFT OUTER JOIN`, `ANTI-JOIN`, `SELF JOIN` for organizational hierarchies, `CROSS JOIN` Cartesian products, and simulated `FULL OUTER JOIN`.

---

## Join Matrix & Behaviors

| Join Type | Match Condition | Unmatched Handling | Common Production Use Case |
|:---|:---|:---|:---|
| **INNER JOIN** | Left key = Right key | Excluded entirely | Active orders with existing customer accounts |
| **LEFT JOIN** | Left key = Right key | Kept with `NULL` on right | Complete user profile with optional billing address |
| **ANTI-JOIN** | Left key has NO match | Filtered via `WHERE right.id IS NULL` | Detecting churned users or empty departments |
| **SELF JOIN** | Same table aliased | Solves parent-child keys | Manager-employee trees or category hierarchies |
| **CROSS JOIN** | Cartesian product ($M \times N$) | All combinations generated | Product variant matrices (colors $\times$ sizes) |
| **FULL OUTER** | Either side matches | `NULL` padded on missing side | Reconciling discrepancies between two billing ledgers |

---

## Running Demonstrations

Run all Join demonstrations:
```bash
python3 -m sql.joins.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m sql.joins.run_examples --demo inner
python3 -m sql.joins.run_examples --demo left
python3 -m sql.joins.run_examples --demo anti
python3 -m sql.joins.run_examples --demo self
python3 -m sql.joins.run_examples --demo cross
python3 -m sql.joins.run_examples --demo full
```
