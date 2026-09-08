# Testing Module

> **Learning Path**: [Stage 07: Testing & Quality Assurance](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-07-testing--quality-assurance) (Prerequisite: [Stage 01: Core Python](file:///Users/sagarshingare/Documents/python-mastery-repo/core_python))

Comprehensive production patterns for testing Python systems: pytest fixtures, unittest.mock isolation, database integration testing with transaction rollback, and micro-benchmarking/memory profiling.

---

## Step-by-Step Learning Sequence

| Step | Subfolder | Focus Area |
|:---|:---|:---|
| **Step 7.1** | [`pytest/`](file:///Users/sagarshingare/Documents/python-mastery-repo/testing/pytest) | Unit testing with Pytest, fixtures, parameterized cases, assertions |
| **Step 7.2** | [`mocking/`](file:///Users/sagarshingare/Documents/python-mastery-repo/testing/mocking) | `MagicMock`, `patch`, `create_autospec`, `side_effect`, `AsyncMock` |
| **Step 7.3** | [`integration_testing/`](file:///Users/sagarshingare/Documents/python-mastery-repo/testing/integration_testing) | SQLite in-memory fixtures, transactional rollback scopes |
| **Step 7.4** | [`performance_testing/`](file:///Users/sagarshingare/Documents/python-mastery-repo/testing/performance_testing) | Latency percentiles (p50/p95/p99), throughput, `tracemalloc` profiling |
| **Step 7.5** | Root Runner | `python -m testing.run_examples` (Live demonstration of all patterns) |

---

## Architecture Overview

```
testing/
├── integration_testing/
│   ├── __init__.py
│   └── integration_patterns.py    # In-memory DB fixtures, transactional rollback
├── mocking/
│   ├── __init__.py
│   └── mock_examples.py           # MagicMock, patch, side_effects, autospec, AsyncMock
├── performance_testing/
│   ├── __init__.py
│   └── benchmark_utils.py         # time_block, benchmark_function, tracemalloc profiler
├── pytest/
│   ├── __init__.py
│   ├── test_core_examples.py      # Integration tests for core language features
│   └── test_python_basics.py      # Tests for Python fundamental primitives
├── run_examples.py                # Combined demonstration runner
├── examples.py                    # Convenience entry point
└── README.md
```

---

## 1. Mocking Strategies (`testing/mocking`)

- **Autospec Verification (`create_autospec`)**: Prevents false positive tests by strictly matching method signatures against the concrete production class.
- **Side Effects**: Simulating intermittent failures, retry sequences (`[False, False, True]`), and dynamic returns.
- **AsyncMock**: Testing asynchronous coroutines and API gateways.
- **Patch Scopes**: Context managers and decorators for isolating environment variables and external I/O.

```python
from unittest.mock import create_autospec
from testing.mocking.mock_examples import PaymentGatewayClient, OrderService

mock_gw = create_autospec(PaymentGatewayClient, instance=True)
mock_gw.charge.return_value = {"success": True, "transaction_id": "tx_123"}
```

---

## 2. Integration Testing (`testing/integration_testing`)

- **Isolated In-Memory Databases**: SQLite in-memory fixtures providing sterile test databases per session.
- **Transaction Rollback Pattern**: Wrapping test cases in `SAVEPOINT` / `ROLLBACK` scopes so mutations never bleed across test boundaries.
- **Cross-Component Workflows**: Verifying repositories, hashing pipelines, and persistence in unison.

```python
from testing.integration_testing import db_session_fixture, transactional_scope, UserRepository

with db_session_fixture() as conn:
    repo = UserRepository(conn)
    repo.create_table()
    with transactional_scope(conn):
        repo.add_user("test", "test@example.com", "pass")
    # After scope exit, user is cleanly rolled back
```

---

## 3. Performance & Micro-benchmarking (`testing/performance_testing`)

- **Statistical Analysis**: Measures `mean`, `median`, `min`, `max`, `p95`, `p99`, and `ops/sec` with warmup passes.
- **Timing Context Managers**: Precise block execution profiling via `time.perf_counter()`.
- **Memory Profiling**: Tracking active byte allocations and peak memory overhead with standard library `tracemalloc`.

```python
from testing.performance_testing import benchmark_function, profile_memory

result = benchmark_function(my_function, iterations=5000)
print(result)
```

---

## Running the Examples and Tests

```bash
# Run testing demonstrations
python -m testing.run_examples

# Run full pytest suite
python -m pytest
```
