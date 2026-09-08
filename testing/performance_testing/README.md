# Performance Testing & Benchmarking

> **Learning Path**: [Stage 07: Testing & Quality Assurance](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-07-testing--quality-assurance) ▸ **Step 7.4: Performance Testing & Benchmarking**

High-precision micro-benchmarking, statistical latency percentiles (p50, p95, p99), throughput calculations, and memory profiling.

## Key Concepts

- **Timing Context Managers**: `time_block()` using `time.perf_counter()`.
- **Statistical Benchmarks**: `benchmark_function()` with warmup iterations and percentile analysis.
- **Memory Profiling**: `profile_memory()` leveraging standard library `tracemalloc`.

## Quick Start

```bash
python -m testing.performance_testing.benchmark_utils
```
