# NumPy Fundamentals & Numerical Computing

> **Learning Path**: [Stage 04: SQL](file:///Users/sagarshingare/Documents/python-mastery-repo/sql) ➔ [Stage 05: Data Analytics](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-05-data-analytics--scientific-libraries) ▸ **Step 5.1: NumPy Fundamentals**

Foundations of high-performance numerical computing in Python: N-dimensional array manipulations, trailing dimension broadcasting rules, SIMD vectorization, and memory layout optimization.

---

## Submodule Directory

| Submodule | Focus | Key Highlights |
|:---|:---|:---|
| [`arrays/`](file:///Users/sagarshingare/Documents/python-mastery-repo/numpy_lib/arrays) | Array Manipulation | Reshaping, 2D meshgrids, strided slicing, stacking/splitting, masking, matrix norms |
| [`broadcasting/`](file:///Users/sagarshingare/Documents/python-mastery-repo/numpy_lib/broadcasting) | Dimension Expansion | Broadcasting compatibility rules, feature z-score scaling, loop-free pairwise distance |
| [`vectorization/`](file:///Users/sagarshingare/Documents/python-mastery-repo/numpy_lib/vectorization) | Hardware Acceleration | Ufuncs (ReLU, Sigmoid), `np.select` branching, financial drawdowns, loop benchmark |
| [`optimization/`](file:///Users/sagarshingare/Documents/python-mastery-repo/numpy_lib/optimization) | Memory Efficiency | C vs Fortran layout, in-place `out=` mutation, views vs copies, numeric downcasting |

---

## Running Demonstrations

### 1. Unified Master Demonstration
Execute all NumPy submodules sequentially:
```bash
python3 -m numpy_lib.run_examples --submodule all
# or
python3 -m numpy_lib.examples
```

### 2. Direct Submodule Runners
```bash
# Array creation, slicing, and linear algebra
python3 -m numpy_lib.arrays.run_examples --demo all

# Broadcasting rules and pairwise Euclidean distance
python3 -m numpy_lib.broadcasting.run_examples --demo all

# Vectorized ufuncs and performance benchmarks
python3 -m numpy_lib.vectorization.run_examples --demo all

# Memory layout and numeric dtype downcasting
python3 -m numpy_lib.optimization.run_examples --demo all
```
