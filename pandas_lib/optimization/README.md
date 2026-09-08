# Pandas Performance & Memory Optimization

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.2**

Techniques for scaling Pandas workflows to massive datasets: dtype downcasting, category types for cardinality compression, chunked streaming, and replacing `apply()` with vectorized primitives.

---

## Optimization Techniques

1. **Dtype Downcasting**: Converting 64-bit integers and floats to `uint8`/`int16`/`float32` via `pd.to_numeric()`, often cutting memory consumption by 50% to 75%.
2. **Category Compression**: Converting repeated text strings into integer categorical codes with lookup pointers.
3. **Chunked Streaming**: Iterating large datasets in fixed batch sizes to bound peak resident set size (RSS) memory.
4. **Vectorization vs Apply**: Leveraging C/Cython optimized SIMD operations instead of Python bytecode interpretation with row-by-row `.apply()`.

---

## Running Demonstrations

Run all Optimization demonstrations:
```bash
python3 -m pandas_lib.optimization.run_examples --demo all
```

Or run targeted demonstrations:
```bash
python3 -m pandas_lib.optimization.run_examples --demo downcast
python3 -m pandas_lib.optimization.run_examples --demo chunk
python3 -m pandas_lib.optimization.run_examples --demo benchmark
```
