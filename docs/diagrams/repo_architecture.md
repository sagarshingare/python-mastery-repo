# Repository Architecture

This diagram describes the main package structure, core modules, and training paths in the repo.

## Hierarchy View

```mermaid
flowchart TD
  A[python-mastery-repo] --> B[core_python]
  A --> C[leetcode]
  A --> D[pandas_lib]
  A --> E[pyspark]
  A --> F[projects]
  A --> G[docs]
  A --> H[testing]
  B --> B1[basics]
  B --> B2[advanced_patterns]
  B --> B3[async_programming]
  B --> B4[decorators]
  B --> B5[generators]
  B --> B6[iterators]
  B --> B7[context_managers]
  B --> B8[oops]
  C --> C1[easy]
  C --> C2[medium]
  C --> C3[hard]
  D --> D1[basics]
  D --> D2[groupby]
  D --> D3[joins]
  E --> E1[basics]
  E --> E2[transformations]
  E --> E3[interview_questions]
  E --> E4[actions]
  F --> F1[batch_etl_pipeline]
  F --> F2[customer_360]
  F --> F3[streaming_pipeline]
```

## Memory DAG / UI-level map

- `core_python/` contains language fundamentals, advanced patterns, and runtime concepts.
- `leetcode/` contains algorithm practice grouped by difficulty.
- `pandas_lib/` contains pandas exercises and example helpers, isolated from the installed `pandas` package.
- `pyspark/` contains Spark examples for basics, transformations, actions, and interview prep.
- `projects/` contains full sample pipelines and production-style data engineering projects.
- `docs/` contains diagrams, architecture guidance, and interview notes.
- `testing/` contains pytest-based validation of the repository.

## Usage guidance

Use standardized entry files in training modules:

- `python -m core_python.basics.examples`
- `python -m pyspark.basics.examples`
- `python -m core_python.oops.examples`

And use the LeetCode runner directly:

- `python -m leetcode.run_problems list`
