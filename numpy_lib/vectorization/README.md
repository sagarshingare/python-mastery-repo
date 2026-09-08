# NumPy Vectorization Patterns

> **Learning Path**: [Stage 05: Data Analytics & Scientific Libraries](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) — **Step 5.1**

Replacing procedural for-loops with SIMD hardware-accelerated vectorization, multi-branching with `np.select`, non-linear activations (ReLU, Sigmoid), cumulative financial metrics, and performance benchmarking.

---

## Running Demonstrations

Run all Vectorization demonstrations:
```bash
python3 -m numpy_lib.vectorization.run_examples --demo all
```

Or target individual operations:
```bash
python3 -m numpy_lib.vectorization.run_examples --demo conditionals
python3 -m numpy_lib.vectorization.run_examples --demo reductions
python3 -m numpy_lib.vectorization.run_examples --demo benchmark
```
