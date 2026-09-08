"""SQL & Relational Databases Mastery Package.

Organized into 6 progressive stages:
- basics: DDL schemas, constraints, CRUD, filtering predicates, grouping, pagination
- joins: INNER, LEFT, ANTI-JOIN, SELF, CROSS, and simulated FULL OUTER JOIN
- cte: Modular non-recursive pipelines, recursive sequence and org tree generation
- window_functions: Analytical ranking, LAG/LEAD comparisons, moving frames
- advanced_queries: Conditional pivot, unpivoting, UPSERT, JSON, Gaps & Islands
- optimization: EXPLAIN QUERY PLAN, single/composite B-Tree indexes, sargability
"""

from . import advanced_queries
from . import basics
from . import cte
from . import joins
from . import optimization
from . import run_examples
from . import window_functions

__all__ = [
    "advanced_queries",
    "basics",
    "cte",
    "joins",
    "optimization",
    "run_examples",
    "window_functions",
]
