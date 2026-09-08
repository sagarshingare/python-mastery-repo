# Sliding Window

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.7: Sliding Window**

Fixed and dynamically expanding/contracting contiguous subarray and substring algorithms in $O(n)$ linear time.

## Key Algorithms

- **`max_sum_subarray`**: Fixed-size window of size $k$ computing maximum contiguous sum.
- **`longest_substring_k_distinct`**: Dynamic window tracking maximum length with at most $k$ unique characters.
- **`min_window_substring`**: Finding minimum length window in string $s$ containing all characters of pattern $t$.
- **`max_consecutive_ones`**: Maximum subarray of 1s allowing up to $k$ zero flips.
- **`count_anagram_substrings`**: Locating all anagram starting indices of pattern in string.

## Quick Start

```python
from dsa.sliding_window import max_sum_subarray

assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9
```
