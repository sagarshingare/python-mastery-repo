# Linked Lists

> **Learning Path**: [Stage 02: Data Structures & Algorithms](file:///Users/sagarshingare/Documents/python-mastery-repo/LEARNING_PATH.md#stage-02-data-structures--algorithms) ▸ **Step 2.3: Linked Lists**

Implementations of singly and doubly linked lists with pointer manipulation algorithms.

## Key Data Structures

- **`SinglyLinkedList`**: Prepend ($O(1)$), append ($O(n)$), delete by value/index, reversal, cycle detection.
- **`DoublyLinkedList`**: Prepend ($O(1)$), append ($O(1)$ with tail pointer), bidirectional traversal.

## Quick Start

```python
from dsa.linked_list import SinglyLinkedList, DoublyLinkedList

sll = SinglyLinkedList()
sll.append(10)
sll.append(20)
sll.prepend(5)
sll.reverse()
assert list(sll) == [20, 10, 5]
```
