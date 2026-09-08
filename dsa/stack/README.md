# Stacks

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.4: Stacks**

LIFO (Last-In First-Out) data structure and monotonic stack problem patterns.

## Key Data Structures & Algorithms

- **`Stack`**: Push, pop, peek, and length in $O(1)$ time.
- **`MinStack`**: Constant-time $O(1)$ `get_min()` tracking using paired minimum stack.
- **`is_balanced`**: Balanced parenthesis verification for `()`, `{}`, and `[]`.
- **`evaluate_postfix`**: Reverse Polish Notation arithmetic calculator.
- **`next_greater_element`**: Monotonic decreasing stack algorithm.

## Quick Start

```python
from dsa.stack import MinStack, is_balanced

assert is_balanced("({[]})") is True

ms = MinStack()
ms.push(10)
ms.push(3)
ms.push(7)
assert ms.get_min() == 3
```
