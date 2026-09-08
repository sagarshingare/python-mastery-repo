"""Performance testing and benchmarking utilities.

Provides high-precision micro-benchmarking, percentile latency analysis (p50, p95, p99),
throughput calculations, and memory profiling using tracemalloc.
"""

from __future__ import annotations

import statistics
import time
import tracemalloc
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Generator


@dataclass
class BenchmarkResult:
    """Summary statistics for benchmark execution."""

    name: str
    iterations: int
    mean_seconds: float
    median_seconds: float
    min_seconds: float
    max_seconds: float
    p95_seconds: float
    p99_seconds: float
    ops_per_second: float

    def __str__(self) -> str:
        return (
            f"Benchmark '{self.name}':\n"
            f"  Iterations: {self.iterations:,}\n"
            f"  Mean:       {self.mean_seconds * 1e6:.2f} µs\n"
            f"  Median:     {self.median_seconds * 1e6:.2f} µs\n"
            f"  Min / Max:  {self.min_seconds * 1e6:.2f} µs / {self.max_seconds * 1e6:.2f} µs\n"
            f"  p95 / p99:  {self.p95_seconds * 1e6:.2f} µs / {self.p99_seconds * 1e6:.2f} µs\n"
            f"  Throughput: {self.ops_per_second:,.0f} ops/sec"
        )


@dataclass
class MemoryProfileResult:
    """Memory allocation profile from tracemalloc."""

    name: str
    current_bytes: int
    peak_bytes: int

    @property
    def peak_kb(self) -> float:
        return self.peak_bytes / 1024.0

    @property
    def peak_mb(self) -> float:
        return self.peak_bytes / (1024.0 * 1024.0)

    def __str__(self) -> str:
        return (
            f"Memory Profile '{self.name}':\n"
            f"  Current: {self.current_bytes:,} bytes\n"
            f"  Peak:    {self.peak_bytes:,} bytes ({self.peak_kb:.2f} KB)"
        )


@contextmanager
def time_block(label: str = "Block") -> Generator[dict[str, float], None, None]:
    """Context manager measuring execution time of an enclosed block."""
    result = {"elapsed_seconds": 0.0}
    start = time.perf_counter()
    try:
        yield result
    finally:
        result["elapsed_seconds"] = time.perf_counter() - start


def benchmark(iterations: int = 1000) -> Callable[..., Any]:
    """Decorator to automatically benchmark a function and print summary."""

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            res = benchmark_function(fn, *args, iterations=iterations, **kwargs)
            print(res)
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def benchmark_function(
    func: Callable[..., Any],
    *args: Any,
    iterations: int = 1000,
    warmup: int = 100,
    name: str | None = None,
    **kwargs: Any,
) -> BenchmarkResult:
    """Benchmark a function across repeated iterations with warmup."""
    bench_name = name or getattr(func, "__name__", "anonymous_func")

    # Warmup runs to allow JIT, CPU cache, and interpreter optimization
    for _ in range(warmup):
        func(*args, **kwargs)

    timings: list[float] = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        func(*args, **kwargs)
        timings.append(time.perf_counter() - t0)

    timings.sort()
    mean_s = statistics.mean(timings)
    median_s = statistics.median(timings)
    min_s = timings[0]
    max_s = timings[-1]

    idx_95 = int(0.95 * iterations)
    idx_99 = int(0.99 * iterations)
    p95_s = timings[min(idx_95, iterations - 1)]
    p99_s = timings[min(idx_99, iterations - 1)]

    ops_per_sec = 1.0 / mean_s if mean_s > 0 else float("inf")

    return BenchmarkResult(
        name=bench_name,
        iterations=iterations,
        mean_seconds=mean_s,
        median_seconds=median_s,
        min_seconds=min_s,
        max_seconds=max_s,
        p95_seconds=p95_s,
        p99_seconds=p99_s,
        ops_per_second=ops_per_sec,
    )


def profile_memory(
    func: Callable[..., Any],
    *args: Any,
    name: str | None = None,
    **kwargs: Any,
) -> tuple[Any, MemoryProfileResult]:
    """Execute a callable while tracking memory allocations via tracemalloc."""
    prof_name = name or getattr(func, "__name__", "anonymous_func")
    tracemalloc.start()
    tracemalloc.reset_peak()
    try:
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    profile = MemoryProfileResult(name=prof_name, current_bytes=current, peak_bytes=peak)
    return result, profile


def run_all() -> None:
    print("\n--- Testing: Performance & Benchmarking Patterns ---")

    # 1. Simple timing context
    with time_block("List creation") as t:
        _ = [x * x for x in range(10_000)]
    print(f"✓ Context manager timing: {t['elapsed_seconds'] * 1e3:.3f} ms")

    # 2. Benchmark comparison: dict comprehension vs loop
    def dict_comprehension() -> dict[int, int]:
        return {i: i * 2 for i in range(100)}

    bench_res = benchmark_function(dict_comprehension, iterations=2000, warmup=200)
    print(bench_res)

    # 3. Memory profiling
    def allocate_strings() -> list[str]:
        return [f"user_data_item_id_{i}" for i in range(10_000)]

    _, mem_res = profile_memory(allocate_strings)
    print(mem_res)


if __name__ == "__main__":
    run_all()
