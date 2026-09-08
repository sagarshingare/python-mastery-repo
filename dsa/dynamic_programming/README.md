# Dynamic Programming

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.12: Dynamic Programming**

Top-down memoization and bottom-up tabulation for optimal substructure and overlapping subproblems.

## Key Algorithms

- **Fibonacci (`fibonacci_memo`, `fibonacci_tabulation`)**: Demonstrating exponential $O(2^n)$ reduction to linear $O(n)$.
- **0/1 Knapsack (`knapsack_01`)**: Value maximization under weight constraints using 2D DP matrix.
- **Longest Common Subsequence (`longest_common_subsequence`)**: String similarity and diffing engine.
- **Coin Change (`coin_change`)**: Minimum coins required for target amount.
- **Edit Distance (`edit_distance`)**: Levenshtein distance metric for spellcheckers and NLP.
- **Maximum Subarray Sum (`max_subarray_sum`)**: Kadane's algorithm in $O(n)$ time and $O(1)$ space.

## Quick Start

```python
from dsa.dynamic_programming import edit_distance, knapsack_01

assert knapsack_01([10, 20, 30], [60, 100, 120], 50) == 220
assert edit_distance("kitten", "sitting") == 3
```
