# Heaps & Priority Queues

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.9: Heaps & Priority Queues**

Array-backed binary heap implementations, sorting algorithms, and streaming analytics.

## Key Data Structures & Algorithms

- **`MinHeap` & `MaxHeap`**: Complete binary tree maintaining heap invariant via sift-up/sift-down ($O(\log n)$).
- **`heapsort`**: In-place $O(n \log n)$ comparison sort.
- **`top_k_elements`**: Extracting $k$ largest elements in $O(n \log k)$ time.
- **`merge_k_sorted_lists`**: Multi-way sorted stream merging using heap pointers.
- **`find_median_stream`**: Dynamic continuous median tracking over numerical input streams using two balanced heaps.

## Quick Start

```python
from dsa.heaps import MinHeap, top_k_elements

heap = MinHeap()
for x in [40, 10, 30, 5, 20]:
    heap.push(x)

assert heap.pop() == 5
assert top_k_elements([10, 5, 20, 8, 15], 2) == [20, 15]
```
