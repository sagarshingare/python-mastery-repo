# Recursion

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.6: Recursion**

Divide-and-conquer paradigms, recursive base cases, combinatorial generators, and call stack mechanics.

## Key Algorithms

- **`factorial` & `power`**: Base case handling and fast exponentiation ($O(\log n)$).
- **`power_set`**: Generating all $2^n$ subsets of a sequence.
- **`permutations`**: Full $n!$ combinatorial ordering generation.
- **`tower_of_hanoi`**: Classical multi-peg recursive movement strategy.
- **`flood_fill`**: Multi-dimensional matrix grid traversal and boundary replacement.
- **`flatten_nested`**: Arbitrarily deep nested list flattening.

## Quick Start

```python
from dsa.recursion import power, power_set

assert power(2, 10) == 1024
assert len(power_set([1, 2, 3])) == 8
```
