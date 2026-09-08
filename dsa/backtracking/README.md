# Backtracking

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.11: Backtracking**

Constraint satisfaction, combinatorial search spaces, pruning, and state exploration.

## Key Algorithms

- **`solve_n_queens(n)`**: Non-attacking queen placement on an $n \times n$ chessboard with diagonal bitsets.
- **`solve_sudoku(board)`**: 9x9 grid constraint propagation and search.
- **`subset_sum(numbers, target)`**: Finding all combinations summing to target with pruning.
- **`word_search(board, word)`**: 2D grid character path search with in-place visitation masking.
- **`generate_parentheses(n)`**: Generating all Catalan number $C_n$ valid parenthesis configurations.

## Quick Start

```python
from dsa.backtracking import generate_parentheses, solve_n_queens

queens_solutions = solve_n_queens(4)
assert len(queens_solutions) == 2

parens = generate_parentheses(3)
assert len(parens) == 5
```
