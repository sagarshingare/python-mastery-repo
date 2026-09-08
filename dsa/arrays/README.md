# Arrays

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.1: Arrays**

Fundamental array algorithms, two-pointer techniques, prefix sums, and hash map lookups.

## Key Algorithms

- **Two Sum**: Hash map single-pass lookup in $O(n)$ time and $O(n)$ space.
- **Brute Force Two Sum**: Nested loop baseline in $O(n^2)$ time.

## Quick Start

```python
from dsa.arrays.array_utils import find_two_sum

indices = find_two_sum([2, 7, 11, 15], 9)
assert indices == (0, 1)
```
