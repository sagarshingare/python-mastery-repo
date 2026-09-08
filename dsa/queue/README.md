# Queues

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.5: Queues**

FIFO (First-In First-Out) queue implementations, circular buffers, priority queues, and double-ended queues.

## Key Data Structures

- **`Queue`**: Backed by `collections.deque` with $O(1)$ enqueue and dequeue.
- **`CircularQueue`**: Fixed-capacity ring buffer using modular index arithmetic without reallocations.
- **`PriorityQueue`**: Min-heap backed priority queue prioritizing lower priority keys.
- **`Deque`**: Double-ended queue supporting push/pop at both head and tail.

## Quick Start

```python
from dsa.queue import CircularQueue, PriorityQueue

cq = CircularQueue(capacity=3)
cq.enqueue(1)
cq.enqueue(2)
assert cq.dequeue() == 1

pq = PriorityQueue()
pq.push("task_urgent", priority=1)
pq.push("task_later", priority=5)
assert pq.pop() == "task_urgent"
```
